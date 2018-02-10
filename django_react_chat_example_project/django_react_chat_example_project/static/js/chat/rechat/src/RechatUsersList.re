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

let component = ReasonReact.statelessComponent("RechatUsersList");

module Query = RechatApollo.Instance.Query;

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
            | Some(chatUsers) => {
                chatUsers |> Array.map((chatUserOption) => {
                  switch chatUserOption {
                  | Some(chatUser) => <div key=(chatUser##username)> (ReasonReact.stringToElement(chatUser##username)) </div>
                  | None => <div>(ReasonReact.stringToElement("No Users"))</div>
                  }
                }) |> ReasonReact.arrayToElement
              }
            | None => unexpectedError
            }
         }
      }
     })
  </Query>
}
};
