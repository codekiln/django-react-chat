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
let component = ReasonReact.statelessComponent("RechatWindow");

module Query = RechatApollo.Instance.Query;

let renderChatMessageItem = (user) => <RechatMessageListItem key=(user##username) chatUser=(user)/>;

let renderChatWindow = (_) => {
  /*let listItems = Array.map(ChatMessageItem, chatGroup) |> ReasonReact.arrayToElement;*/

  <div className="RechatWindow">
    <div className="header">(RechatUtils.ste("CHAT WINDOW"))</div>
    /*<ul>(listItems)</ul>*/
  </div>
};


let make = (_children) => {
  ...component,
  render: (_) => {
    <div className="RechatWindow">

      <div className="RechatWindow__Header">
        <div className="RechatWindow__HeaderTitle">(RechatUtils.ste("Chat User 1"))</div>
        <div className="RechatWindow__CloseButton">(RechatUtils.ste("X"))</div>
      </div>

      <div className="RechatWindow__MessagesPort">

        <div className="RechatWindow__MessageContainer RechatWindow__MessageContainer--Theirs">
          <div className="RechatWindow__AvatarContainer">
            <MaterialUI.Avatar className="RechatWindow__Avatar">(RechatUtils.ste("TH"))</MaterialUI.Avatar>
          </div>
          <div className="RechatWindow__Message RechatWindow__Message--Theirs">(RechatUtils.ste("A small river named Duden flows by their place and supplies it with the necessary regelialia."))</div>
        </div>

        <div className="RechatWindow__MessageContainer RechatWindow__MessageContainer--Ours">
          <div className="RechatWindow__Message RechatWindow__Message--Ours">(RechatUtils.ste("Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean."))
          </div>
        </div>

        <div className="RechatWindow__MessageContainer RechatWindow__MessageContainer--Theirs">
          <div className="RechatWindow__AvatarContainer">
            <MaterialUI.Avatar className="RechatWindow__Avatar">(RechatUtils.ste("TH"))</MaterialUI.Avatar>
          </div>
          <div className="RechatWindow__Message RechatWindow__Message--Theirs">(RechatUtils.ste("It is a paradisematic country, in which roasted parts of sentences fly into your mouth."))</div>
        </div>

      </div>

      <div className="RechatWindow__Footer">
        <input _type="text" placeholder="Type a message..." className="RechatWindow__Input"/>
      </div>

    </div>
    /*let unexpectedError = <div> (ReasonReact.stringToElement("There was an internal error")) </div>;*/
    /*let usersQuery = UsersQuery.make();*/
    /*<Query query=usersQuery>*/
    /*...((response, parse) => {*/
      /*switch response {*/
         /*| Loading => <div> (ReasonReact.stringToElement("Loading")) </div>*/
         /*| Failed(error) => <div> (ReasonReact.stringToElement(error)) </div>*/
         /*| Loaded(result) => {*/
            /*let chatUsers = parse(result)##chatUsers;*/
            /*switch chatUsers {*/
            /*| Some(chatUsers) => RechatUtils.arr_only_some(chatUsers) |> renderUsersList*/
            /*| None => unexpectedError*/
            /*}*/
         /*}*/
      /*}*/
     /*})*/
  /*</Query>*/
}
};
