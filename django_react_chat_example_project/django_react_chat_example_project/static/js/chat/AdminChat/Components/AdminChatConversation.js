import React from 'react'
import AdminChatContact from './AdminChatContact'
import AdminChatInput from '../Containers/AdminChatInput'


class AdminChatConversation extends React.Component {

  static authorStreakReducer(streaks = [], {text: messageText, ...messageInfo}) {
    const {author: streakAuthor, messages: streakMessages} = streaks.length ? streaks[streaks.length - 1] : {}
    if (streakAuthor === messageInfo.author) {
      streakMessages.push(messageText)
    } else {
      streaks.push({...messageInfo, messages: [messageText]})
    }
    return streaks
  }

  constructor(props) {
    super(props)
    this.renderMessageStreak = this.renderMessageStreak.bind(this)
  }

  componentDidMount() {
    this.scrollToBottom();
  }

  componentDidUpdate() {
    this.scrollToBottom()
  }

  render() {
    const {group: {messages, otherUsers} = {}, currentUser} = this.props;
    const renderedMessages = (messages && messages.length)
      ? messages.reduce(AdminChatConversation.authorStreakReducer, []).map(this.renderMessageStreak)
      : (<li className="info"><p>You haven't chatted yet.</p></li>)
    const selectedUser = otherUsers && otherUsers[0]

    return <div className="content">
      <div className="contact-profile">
        <AdminChatContact {...selectedUser}/>
      </div>
      <div className="messages">
        <ul>
          {renderedMessages}
        </ul>
        <div style={{clear: 'both'}} ref={el => this.scrollEnd = el}/>
      </div>
      <AdminChatInput onSubmit={this.props.sendMessage}/>
    </div>
  }

  scrollToBottom = () => {
    this.scrollEnd.scrollIntoView({behavior: 'smooth', block: 'end'})
  }

  renderMessageStreak = ({id: messageId, author: authorId, messages, uuid}) => {
    const isOtherUser = authorId !== this.props.currentUser.id
    const renderedMessages = messages.map((msg, index) => <p key={index}>{msg}</p>)

    return <li key={messageId || uuid} className={isOtherUser ? 'received' : 'sent'}>
      {isOtherUser && <AdminChatContact {...this.props.users[authorId]} size={20} hideName/>}
      {renderedMessages}
    </li>
  }
}

export default AdminChatConversation;
