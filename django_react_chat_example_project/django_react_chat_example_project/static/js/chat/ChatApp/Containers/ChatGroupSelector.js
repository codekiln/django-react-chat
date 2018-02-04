import React from 'react'
import { graphql } from 'react-apollo'
import groupsAndUsersQuery from './groupsAndUsers.graphql'

const query = groupsAndUsersQuery;

class GroupChatSelector extends React.Component {
  render() {
    let {data} = this.props
    if (data.loading) {
      return <div>Loading...</div>
    }
    console.log(data);
    return (
      <div>
        {data.chatUsers.map((item, index) => (
          <p key={item.id}>
            {item.name}
          </p>
        ))}
      </div>
    )
  }
}

GroupChatSelector = graphql(query)(GroupChatSelector)

export default GroupChatSelector
