/* let renderChatMessageItem = message => {
     Js.log(message);
     let getKey = msg =>
       switch (msg##id) {
       | Some(id) => string_of_int(id)
       | None => "no id"
       };
     <RechatMessageListItem key=(getKey(message)) chatMessage=message />;
   }; */
/* let renderChatWindow = chatGroup => {
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
   }; */
type user = {
  id: string,
  name: string,
  abbreviation: string,
  photoUrl: string,
  isCurrentUser: Js.boolean,
};

type author = {id: string};

type message = {
  id: string,
  author,
  text: string,
};

module StringMap = Map.Make(String);

let getUserMap = (uzers: list(user)) => {
  let userMapBuilder = (map, uzer: user) =>
    StringMap.add(uzer.id, uzer, map);
  List.fold_left(userMapBuilder, StringMap.empty, uzers);
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
        node @bsRecord {
          id
          text
          author @bsRecord {
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

type messagesObjArr =
  option({. "edges": array(option({. "node": option(message)}))});

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

let parseMessages = (messages: messagesObjArr) => {
  let someMessages =
    switch (messages) {
    | Some(messages) => messages##edges
    | None => [|None|]
    };
  let buildMessageList = (messageList, edge) =>
    switch (edge) {
    | Some(messageEdge) =>
      switch (messageEdge##node) {
      | Some(message) => [message, ...messageList]
      | None => messageList
      }
    | None => messageList
    };
  let newMessages = Array.fold_left(buildMessageList, [], someMessages);
  newMessages;
};

let getChatGroupUsers = chatGroup =>
  switch (chatGroup) {
  | Some(chatGroup) => parseUsers(chatGroup##users)
  | None => []
  };

let getChatGroupMessages = chatGroup =>
  switch (chatGroup) {
  | Some(chatGroup) => parseMessages(chatGroup##messages)
  | None => []
  };

let renderLoadedResult = result => {
  let chatGroup = result##chatGroup;
  Js.log(chatGroup);
  let users = getChatGroupUsers(chatGroup);
  let messages = getChatGroupMessages(chatGroup);
  Js.log(messages);
  let usersMap = getUserMap(users);
  /* let usersArray = ArrayLabels.of_list(users); */
  let messagesArray = ArrayLabels.of_list(messages);
  /* let usersLiArMapper = user => <li> (RechatUtils.ste(user.name)) </li>; */
  let messageLiArMapper = (msg: message) => {
    let user = StringMap.find(msg.author.id, usersMap);
    let msgStr = user.name ++ ": " ++ msg.text;
    <li key=msg.id> (RechatUtils.ste(msgStr)) </li>;
  };
  /* let usersLiArr = Array.map(usersLiArMapper, usersArray); */
  let messageLiArr = Array.map(messageLiArMapper, messagesArray);
  <div> <ul> (ReasonReact.arrayToElement(messageLiArr)) </ul> </div>;
  /* <ul> (ReasonReact.arrayToElement(usersLiArr)) </ul> */
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