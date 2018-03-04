/* Create a GraphQL Query by using the graphql_ppx */
type user = {
  id: string,
  name: string,
  abbreviation: string,
  photoUrl: string,
  isCurrentUser: Js.boolean
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

/*eventually will be a reducerComponent*/
let component = ReasonReact.statelessComponent("RechatWindow");

module Query = RechatApollo.Instance.Query;

/*let renderChatMessageItem = (message) => {*/
/*Js.log(message);*/
/*let getKey = (msg) =>*/
/*switch msg##id {*/
/*| Some(id) => string_of_int(id)*/
/*| None => "no id"*/
/*};*/
/*<RechatMessageListItem key=(getKey(message)) chatMessage=(message)/>;*/
/*};*/
/*let renderChatWindow = (chatGroup) => {*/
/*let getMessageEdgesArray = (messagesOption) =>*/
/*switch messagesOption {*/
/*| Some(messages) => RechatUtils.arr_only_some(messages#edges)*/
/*| None => [||]*/
/*};*/
/*let getMessageNodesArray = (someMessageEdges) =>*/
/*switch someMessageEdges#node {*/
/*| Some (messageNode) => [|messageNode|]*/
/*| None => [||]*/
/*};*/
/*let messageItems = getMessageEdgesArray(chatGroup##messages)*/
/*|> getMessageNodesArray*/
/*|> Array.map(renderChatMessageItem)*/
/*|> ReasonReact.arrayToElement;*/
/*<div className="RechatWindow">*/
/*<div className="RechatWindow__Header">*/
/*<div className="RechatWindow__HeaderTitle">(RechatUtils.ste("Chat User 1"))</div>*/
/*<div className="RechatWindow__CloseButton">(RechatUtils.ste("X"))</div>*/
/*</div>*/
/*<div className="RechatWindow__MessagesPort">*/
/*(messageItems)*/
/*</div>*/
/*<div className="RechatWindow__Footer">*/
/*<input _type="text" placeholder="Type a message..." className="RechatWindow__Input"/>*/
/*</div>*/
/*</div>*/
/*};*/
/* module Infix = {
     let (>>=) = (value, fn) =>
       switch value {
       | Some(value) => fn(value)
       | None => None
       };
     let (|?) = (value, default) =>
       switch value {
       | None => default
       | Some(value) => value
       };
   };

   open Infix;

   type rechatAvatarProps =
     | PhotoUrl(string)
     | Abbreviation(string);

   type chatUser = {
     id: string,
     name: string,
     avatarProps: rechatAvatarProps,
     isCurrentUser: bool
   };

   type message = {
     id: string,
     text: string,
     author: chatUser
   };

   let getUser = user =>
     List.fold_left(
       (str, item) => Some((str |? "") ++ " - " ++ item),
       Some(""),
       [user##id |? "", user##abbreviation |? "", user##isCurrentUser |? ""]
     );

   let getUserFromUserNodeOpt = userNodeOpt =>
     userNodeOpt >>= getUser |? "error retrieving user";

   let getUsersFromGroup = group => {
     let users = group##users;
     users >>= Array.map(getUserFromUserNodeOpt, edges) |? [||];
   } */
/*let parseMessages = chatGroup =>*/
/*switch chatGroup {*/
/*| Some(chatGroup) =>*/
/*switch chatGroup##messages {*/
/*| Some(messages) =>*/
/*let edges = messages##edges;*/
/*switch edges {*/
/*| Some(edges) =>*/
/*let parsedNodes =*/
/*Js.Array.map(*/
/*node =>*/
/*switch node {*/
/*| Some(node) =>*/
/*let id = node##id;*/
/*let text = node##text;*/
/*let author = node##author;*/
/*switch (id, text, author) {*/
/*| (Some(id), Some(text), Some(author)) =>*/
/*let name = author##name;*/
/*let abbrev = author##abbreviation;*/
/*let isCurrentUser = author##isCurrentUser;*/
/*switch (name, abbrev, isCurrentUser) {*/
/*| (Some(name), Some(abbrev), Some(isCurrentUser)) =>*/
/*id ++ " - " ++ text ++ " - " ++ name ++ " - " ++ abbrev ++ " - "*/
/*| _ => "Error retrieving message 3"*/
/*};*/
/*| _ => "Error retrieving message 2"*/
/*};*/
/*| _ => "Error retrieving message 1"*/
/*},*/
/*edges*/
/*);*/
/*parsedNodes;*/
/*| None => [||]*/
/*};*/
/*| None => [||]*/
/*};*/
/*| None => [||]*/
/*};*/
let logUser = (user: user) => Js.log(user.name);

type users = option({. "edges": array(option({. "node": option(user)}))});

let parseUsers = (users: users) => {
  let someUsers =
    switch users {
    | Some(users) => users##edges
    | None => [|None|]
    };
  Array.fold_left(
    (lst, edge) =>
      switch edge {
      | Some(user) =>
        switch user##node {
        | Some(user) => [user, ...lst]
        | None => lst
        }
      | None => lst
      },
    [],
    someUsers
  );
};

let parseChatGroup = chatGroup =>
  switch chatGroup {
  | Some(chatGroup) => parseUsers(chatGroup##users)
  | None => []
  };

let make = _children => {
  ...component,
  render: (_) => {
    /* let unexpectedError =
       <div>
         (ReasonReact.stringToElement("There was an internal error"))
       </div>;
       */
    let groupQuery = GroupQuery.make(~chatGroupId="Q2hhdEdyb3VwVHlwZTox", ());
    /* Js.log(groupQuery.t); */
    <Query query=groupQuery>
      ...(
           (response, parse) =>
             switch response {
             | Loading => <div> (ReasonReact.stringToElement("Loading")) </div>
             | Failed(error) =>
               <div> (ReasonReact.stringToElement(error)) </div>
             | Loaded(result) =>
               let result = parse(result);
               let chatGroup = result##chatGroup;
               let users = parseChatGroup(chatGroup);
               let usersArray = ArrayLabels.of_list(users);
               /* let parsedUsers = groupOpt >>= getUsersFromGroup |? [||]; */
               <ul>
                 (
                   ReasonReact.arrayToElement(
                     Array.map(
                       user => <li> (RechatUtils.ste(user.name)) </li>,
                       usersArray
                     )
                   )
                 )
               </ul>;
             }
         )
    </Query>;
  }
};