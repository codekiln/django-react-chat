import React from 'react'
import OldChatContact from '../Components/OldChatContact'

class OldChatGroupSelector extends React.PureComponent {

  constructor(props) {
    super(props)
    this.state = {
      searchFor: ''
    }
    this.onSearchFor = this.onSearchFor.bind(this)
    this.renderChatGroupItem = this.renderChatGroupItem.bind(this)
  }

  getFilteredChatGroups(groups, searchString) {
    const lowerSearchString = searchString.toLowerCase()
    return Object.values(groups).filter(group => !searchString || group.displayName.toLowerCase().includes(lowerSearchString))
  }

  onSearchFor(event) {
    this.setState({'searchFor': event.target.value})
  }

  // currently only supports one user in a chat group.
  // This could easily be implemented, however.
  renderChatGroupItem = (group) => {
    if (Object.keys(group.otherUsers).length === 1) {
      const user = group.otherUsers[0]
      const isSelected = this.props.activeGroupId === group.clientSideId
      return <li key={user.id} className="contact"
                 onClick={this.props.onSelectChatGroup.bind(null, group)}>
        <OldChatContact {...user} active={isSelected}/>
      </li>
    }
  }

  render() {
    const {groups, currentUser} = this.props
    const {searchFor: searchString} = this.state

    const renderedUserList = this.getFilteredChatGroups(groups, searchString).map(this.renderChatGroupItem);

    return <div id="sidepanel">

      <div id="profile">
        <OldChatContact online={true} {...currentUser} isCurrentUser/>
      </div>

      <div id="oldChat-search">
        <label htmlFor="oldChat-search-input"><i className="fa fa-search" aria-hidden="true"/></label>
        <input id="oldChat-search-input" type="text" placeholder="Search contacts..."
               value={this.state.searchFor} onChange={this.onSearchFor}/>
      </div>

      <div id="contacts">
        <ul>
          {renderedUserList}
        </ul>
      </div>

    </div>
  }

}

export default OldChatGroupSelector;
