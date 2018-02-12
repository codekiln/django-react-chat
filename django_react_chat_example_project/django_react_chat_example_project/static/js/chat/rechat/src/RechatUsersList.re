/* Create a GraphQL Query by using the graphql_ppx */
module UsersQuery = [%graphql {|
  query {
      chatUsers {
          id
          name
          username
          isCurrentUser
          photoUrl
      }
  }
|}];

/*eventually will be a reducerComponent*/
let component = ReasonReact.statelessComponent("RechatUsersList");

module Query = RechatApollo.Instance.Query;

let renderUsersListItem = (user) => <RechatUsersListItem key=(user##username) chatUser=(user)/>;

let renderUsersList = (chatUsers) => {
  let listItems = Array.map(renderUsersListItem, chatUsers) |> ReasonReact.arrayToElement;

  <div className="users-list">
    <div className="header">(RechatUtils.ste("CONTACTS"))</div>
    <ul>(listItems)</ul>
  </div>
};


let make = (_children) => {
  ...component,
  render: (_) => {
    let unexpectedError = <div> (ReasonReact.stringToElement("There was an internal error")) </div>;
    let usersQuery = UsersQuery.make();
    <Query query=usersQuery>
    ...((response, parse) => {
      switch response {
         | Loading => <div> (ReasonReact.stringToElement("Loading")) </div>
         | Failed(error) => <div> (ReasonReact.stringToElement(error)) </div>
         | Loaded(result) => {
            let chatUsers = parse(result)##chatUsers;
            switch chatUsers {
            | Some(chatUsers) => RechatUtils.arr_only_some(chatUsers) |> renderUsersList
            | None => unexpectedError
            }
         }
      }
     })
  </Query>
}
};
