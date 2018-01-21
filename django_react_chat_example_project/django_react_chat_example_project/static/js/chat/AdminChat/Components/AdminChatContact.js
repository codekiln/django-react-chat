import React from 'react'
import Avatar from 'react-avatar'

class AdminChatContact extends React.PureComponent {

  render() {
    const {online, photoUrl, name, isCurrentUser, active, hideName, size} = this.props

    const nameSection = hideName ? "" : <div className="meta"><p className="name">{name || '(Anonymous)'}</p></div>
    const contactClass = `adminchat-contact ${isCurrentUser ? 'current-user' : 'other-user'} ${active ? 'active' : 'inactive'}`

    return <div className={contactClass}>
      <div className="wrap">
        <span className={`contact-status ${online ? 'online' : 'offline'}`}/>
        <Avatar name={name} src={photoUrl} size={size ? size : 40} maxInitials={2} round
                className={`adminchat-avatar ${online ? 'online' : 'offline'}`}/>
        {nameSection}
      </div>
    </div>
  }
}

export default AdminChatContact