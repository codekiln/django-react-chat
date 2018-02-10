let component = ReasonReact.statelessComponent("RechatUsersListItem");

let make = (~chatUser, _children) => {
  ...component,
  render: (_) => {
    <div> (ReasonReact.stringToElement(chatUser##username)) </div>
  }
};
