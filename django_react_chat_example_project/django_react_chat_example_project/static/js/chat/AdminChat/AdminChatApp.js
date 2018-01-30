import './AdminChatStyle.scss';
import React from 'react'
import ReactDOM from 'react-dom'
import AdminChatGroupSelector from './Containers/AdminChatGroupSelector'
import { instanceOf } from 'prop-types'
import AdminChatConversation from './Components/AdminChatConversation'
import sortBy from 'lodash.sortby'
import Websocket from 'react-websocket'
import uuidv4 from 'uuid/v4'


class AdminChatApp extends React.PureComponent {

  static getChatGroupIdentifier(userIds) {
    return userIds.sort().join('-')
  }

  static getChatGroupDisplayName({users}) {
    return users.filter((user) => !user.isCurrentUser).map((user) => user.name).sort().join(', ')
  }

  static getSortedGroups(groups) {
    return sortBy(groups, 'displayName')
  }

  constructor(props) {
    super(props)

    this.state = {
      users: {},
      currentUser: {},
      groups: {
        // the client side id is the user ids joined by hyphens
        '2-1': {
          // the server side id
          id: 0,
          // the client side id, used in case group hasn't been created on server yet
          clientSideId: '',
          messages: [],
          // all users in chat, including current user
          users: [],
          // just the non-current users
          otherUsers: [],
          selected: true
        }
      },
      selectedGroupClientSideId: '2-1',
    }

    this.onSelectChatGroup = this.onSelectChatGroup.bind(this)
    this.queueNewMessage = this.queueNewMessage.bind(this)
    this.setChatGroups = this.setChatGroups.bind(this)
    this.setChatUsers = this.setChatUsers.bind(this)
    this.onSocketMessage = this.onSocketMessage.bind(this)
    this.onSocketOpen = this.onSocketOpen.bind(this)

    this.requestCreateGroup = this.requestCreateGroup.bind(this)
    this.requestCreateMessage = this.requestCreateMessage.bind(this)
  }

  render() {
    const {users, currentUser, groups, selectedGroupClientSideId: groupId} = this.state
    const selectedGroup = groupId && groups.hasOwnProperty(groupId) && groups[groupId]
    const sortedGroups = AdminChatApp.getSortedGroups(groups)

    return <div id="adminchat-container">
      <div id="adminchat-frame">
        <AdminChatGroupSelector users={users} currentUser={currentUser} groups={sortedGroups}
                                activeGroupId={groupId}
                                onSelectChatGroup={this.onSelectChatGroup}/>
        <AdminChatConversation group={selectedGroup} users={users} currentUser={currentUser}
                               sendMessage={this.queueNewMessage}/>
        <Websocket ref="socket" url={this.props.chatWebsocketEndpoint} onOpen={this.onSocketOpen}
                   onClose={AdminChatApp.onSocketClose} onMessage={this.onSocketMessage} reconnect={true}/>

      </div>
    </div>
  }

  onSelectChatGroup({clientSideId}) {
    this.setState({selectedGroupClientSideId: clientSideId})
  }

  onSocketOpen(obj) {
    console.log('AdminChatApp: websocket opened')
    this.fetchChatUsers()
  }

  static onSocketClose(obj) {
    console.log('AdminChatApp: websocket closed')
  }

  onSocketMessage(msg) {
    const result = JSON.parse(msg)
    console.log(`onSocketMessage received: `, result)
    const {
      gql: {
        data: {
          chatGroups: gqlChatGroups,
          chatUsers: gqlChatUsers,
          createMessage: gqlCreateMessage,
          createGroup: gqlCreateGroup
        }
      }
    } = result

    let {currentUser} = this.setChatUsers(gqlChatUsers)

    if (gqlChatGroups) {
      this.setChatGroups(gqlChatGroups,
        gqlChatUsers ? gqlChatUsers : this.state.users,
        currentUser ? currentUser : this.state.currentUser)
    }

    if (gqlCreateGroup) {
      this.onCreateGroup(gqlCreateGroup)
    }

    if (gqlCreateMessage) {
      this.onCreateMessage(gqlCreateMessage)
    }
  }

  sendSocketMessage(message) {
    // sends message to channels back-end
    const socket = this.refs.socket
    socket.state.ws.send(JSON.stringify(message))
  }

  fetchChatUsers() {
    this.sendSocketMessage({
      chatUsers: [], chatGroups: [], gql: `query {
  chatGroups {
  	id 
  	messages {
  		id 
  		text 
  		author 
		}
    users {
      id
      isCurrentUser
      name
    }
  	
	}
  chatUsers {
    id
    name
    username
    isCurrentUser
    photoUrl
  }
}`
    })
  }

  requestCreateGroup(group) {
    const {currentUserId} = this.state
    const otherUser = group.users.find(({id}) => id !== currentUserId)

    this.sendSocketMessage({
      gql: `mutation {
  createGroup(userId: ${otherUser.id}) {
    status
    formErrors
    chatGroup {
      id
      users {
        id
        username
      }
    }
    notifyUserIds
  }
}
    `
    })

  }

  onCreateGroup(groupResponse) {
    console.log(`onCreateGroup received created group`, groupResponse)
    if (groupResponse.status !== 200) {
      console.log(`onCreateGroup detected group creation failure: ${groupResponse.formErrors}`)
      return
    }
    const {groups} = this.state
    const {chatGroup: newServerGroup} = groupResponse
    const groupUserIds = newServerGroup.users.map(({id}) => id)
    const clientSideId = AdminChatApp.getChatGroupIdentifier(groupUserIds)
    const existingGroup = groups[clientSideId]
    const newClientGroup = {
      ...existingGroup,
      id: newServerGroup.id
    }
    this.setState({
      'groups': {
        ...groups,
        [clientSideId]: newClientGroup
      }
    })

    // we create a new group with a message stored locally
    // so search for the existing group with the unsent message(s) and send them
    // now that we have the new group
    const unsentMessages = existingGroup.messages.filter(({id}) => !id)
    if (unsentMessages) {
      for (const unsentMessage of unsentMessages) {
        this.requestCreateMessage(unsentMessage.text, newClientGroup, unsentMessage.uuid)
      }
    }
  }

  requestCreateMessage(text, group, newUuid) {
    const {id: groupId} = group
    if (groupId) {
      this.sendSocketMessage({
        gql: `mutation {
  createMessage(uuid: "${newUuid}", text: "${text}", chatGroupId: ${groupId}) {
    uuid
    status
    formErrors
    chatMessage {
      id
      text
      author
      chatGroup
    }
    notifyUserIds
  }
}`
      })
    }
  }

  onCreateMessage(newMessageResponse) {
    console.log(`onCreateMessage received created message`, newMessageResponse)
    const {groups, currentUser} = this.state
    const {uuid: newMessageUuid, chatMessage} = newMessageResponse
    let group = Object.values(groups).find(({id}) => id === chatMessage.chatGroup)
    let existingGroup = null
    if (group === undefined) {
      const groupUserIds = [chatMessage.author, currentUser.id]
      const clientSideId = AdminChatApp.getChatGroupIdentifier(groupUserIds)
      existingGroup = groups[clientSideId]
    } else {
      existingGroup = groups[group.clientSideId]
    }
    if (!existingGroup) {
      console.warn(`onCreateMessage received message from unknown user`,
        newMessageResponse)
    }
    const existingMessageFound = existingGroup.messages.find(({uuid}) => uuid === newMessageUuid)
    if (existingMessageFound) {
      existingMessageFound.id = chatMessage.id
    }
    const newMessages = existingMessageFound ? existingGroup.messages : [...existingGroup.messages, chatMessage]

    this.setState({
      'groups': {
        ...groups,
        [group.clientSideId]: {
          ...existingGroup,
          messages: newMessages
        }
      }
    })
  }

  queueNewMessage(text, author = this.state.currentUser.id, groupClientSideId = this.state.selectedGroupClientSideId) {
    if (!groupClientSideId || !this.state.groups.hasOwnProperty(groupClientSideId)) {
      throw new Error(`queueNewMessage tried to send a message to invalid group client side id: ${groupClientSideId}`)
    }
    const group = this.state.groups[groupClientSideId]
    // the uuid of the new message
    const newUuid = uuidv4()

    const createNewMessageApiRequest = () => {
      if (!group.id) {
        this.requestCreateGroup(group)
      } else {
        this.requestCreateMessage(text, group, newUuid)
      }
    }

    // set the new message into component state
    // once it is set then make the api request
    this.setState({
      groups: {
        ...this.state.groups,
        [groupClientSideId]: {
          ...group,
          messages: [...group.messages, {text, author, uuid: newUuid}]
        }
      }
    }, createNewMessageApiRequest);
  }

  setChatUsers(users) {
    if (users) {
      const currentUser = users.find((user) => user.isCurrentUser)
      const otherUsers = {}

      for (const user of users) {
        otherUsers[user.id] = user
      }

      const userChatState = {
        users: otherUsers,
        currentUser: currentUser
      }

      this.setState(userChatState)
      return userChatState
    }
    return {}
  }

  setChatGroups(groups, users = this.state.users, currentUser = this.state.currentUser) {
    const usersArray = Object.values(users).filter((user) => user.id !== currentUser.id);
    const groupsArray = Object.values(groups);
    const {selectedClientSideId} = this.state;

    const clientSideGroups = {};
    const serverGroups = {};

    // create a client side "stub" group for each user we can chat with
    // this will be created on the server upon sending the first message
    for (const otherUser of usersArray) {
      const newUserGroupIdentifier = AdminChatApp.getChatGroupIdentifier([otherUser.id, currentUser.id])
      clientSideGroups[newUserGroupIdentifier] = {
        clientSideId: newUserGroupIdentifier,
        messages: [],
        users: [otherUser],
        displayName: otherUser.name,
        otherUsers: [otherUser],
        selected: newUserGroupIdentifier === selectedClientSideId
      }
    }

    // if server side groups exist, overwrite the client side "stub" groups for each user
    for (const group of groupsArray) {
      const otherUsers = group.users.filter(({id}) => id !== currentUser.id)
      const clientSideId = AdminChatApp.getChatGroupIdentifier(group.users.map(({id}) => id))
      const displayName = AdminChatApp.getChatGroupDisplayName(group)
      const groupWithClientSideId = {
        ...group, clientSideId, displayName, otherUsers,
        selected: clientSideId === selectedClientSideId
      }

      clientSideGroups[clientSideId] = groupWithClientSideId;
      serverGroups[clientSideId] = groupWithClientSideId;
    }

    const newSelectedGroup = selectedClientSideId
      // if we already have a group selected in sidebar, use that.
      ? clientSideGroups[selectedClientSideId]
      : Object.keys(serverGroups).length
        // otherwise, use the first existing server-side group if it exists.
        ? AdminChatApp.getSortedGroups(serverGroups)[0]
        // otherwise, use the first client side user "stub" group, i.e. the first user we haven't chatted with before.
        : AdminChatApp.getSortedGroups(clientSideGroups)[0]

    this.setState({
      groups: clientSideGroups,
      selectedGroupClientSideId: newSelectedGroup.clientSideId
    });
  }
}

// TODO: use react prop types to define component prop dependencies

const webpackBundleName = 'chat.admin_chat'
const context = window.js_context[webpackBundleName]
const domNode = document.getElementById(webpackBundleName)

ReactDOM.render(
  <AdminChatApp {...context}/>
  , domNode)

