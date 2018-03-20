/*
 let renderChatMessageItem = message => {
   Js.log(message);
   let getKey = msg =>
     switch (msg##id) {
     | Some(id) => string_of_int(id)
     | None => "no id"
     };
   <RechatMessageListItem key=(getKey(message)) chatMessage=message />;
 };

 let renderChatWindow = chatGroup => {
   let getMessageEdgesArray = messagesOption =>
     switch (messagesOption) {
     | Some(messages) => RechatUtils.arr_only_some(messages#edges)
     | None => [||]
     };
   let getMessageNodesArray = someMessageEdges =>
     switch (someMessageEdges#node) {
     | Some(messageNode) => [|messageNode|]
     | None => [||]
     };
   let messageItems =
     getMessageEdgesArray(chatGroup##messages)
     |> getMessageNodesArray
     |> Array.map(renderChatMessageItem)
     |> ReasonReact.arrayToElement;
   <div className="RechatWindow">
     <div className="RechatWindow__Header">
       <div className="RechatWindow__HeaderTitle">
         (RechatUtils.ste("Chat User 1"))
       </div>
       <div className="RechatWindow__CloseButton">
         (RechatUtils.ste("X"))
       </div>
     </div>
     <div className="RechatWindow__MessagesPort"> messageItems </div>
     <div className="RechatWindow__Footer">
       <input
         _type="text"
         placeholder="Type a message..."
         className="RechatWindow__Input"
       />
     </div>
   </div>;
 };*/
type user = {
  id: string,
  name: string,
  abbreviation: string,
  photoUrl: string,
  isCurrentUser: Js.boolean,
};

module GroupQuery = [%graphql
  {|
query GetChatGroup($chatGroupId: ID!){
  chatGroup(id: $chatGroupId) {
    id
    users {
      edges {
        node @bsRecord {
          id
          name
          abbreviation
          photoUrl
          isCurrentUser
        }
      }
    }
    messages {
      edges {
        node {
          id
          text
          author {
            id
          }
        }
      }
    }
  }
}
|}
];

type userObjArr =
  option({. "edges": array(option({. "node": option(user)}))});

let parseUsers = (users: userObjArr) => {
  let someUsers =
    switch (users) {
    | Some(users) => users##edges
    | None => [|None|]
    };
  let buildUserList = (userList, edge) =>
    switch (edge) {
    | Some(userEdge) =>
      switch (userEdge##node) {
      | Some(user) => [user, ...userList]
      | None => userList
      }
    | None => userList
    };
  Array.fold_left(buildUserList, [], someUsers);
};

let getChatGroupUsers = chatGroup =>
  switch (chatGroup) {
  | Some(chatGroup) => parseUsers(chatGroup##users)
  | None => []
  };

module StringMap = Map.Make(String);

let getUserMap = (users: list(user)) => {
  let buildUserMap = (map, user) => StringMap.add(user.id, user, map);
  List.fold_left(buildUserMap, StringMap.empty, users);
};

let renderLoadedResult = result => {
  let chatGroup = result##chatGroup;
  let users = getChatGroupUsers(chatGroup);
  let usersMap = getUserMap(users);
  let usersArray = ArrayLabels.of_list(users);
  let usersLiArMapper = user => <li> (RechatUtils.ste(user.name)) </li>;
  let usersLiArr = Array.map(usersLiArMapper, usersArray);
  <ul> (ReasonReact.arrayToElement(usersLiArr)) </ul>;
};

module Query = RechatApollo.Instance.Query;

/*eventually will be a reducerComponent*/
let rechatWindowComponent = ReasonReact.statelessComponent("RechatWindow");

let make = _children => {
  ...rechatWindowComponent,
  render: (_) => {
    let groupQuery = GroupQuery.make(~chatGroupId="Q2hhdEdyb3VwVHlwZTox", ());
    <Query query=groupQuery>
      ...(
           (response, parse) =>
             switch (response) {
             | Loading =>
               <div> (ReasonReact.stringToElement("Loading")) </div>
             | Failed(error) =>
               <div> (ReasonReact.stringToElement(error)) </div>
             | Loaded(result) =>
               <div> (renderLoadedResult(parse(result))) </div>
             /*| Loaded(_) =>
               <div> (ReasonReact.stringToElement("RESULT")) </div>*/
             }
         )
    </Query>;
  },
};