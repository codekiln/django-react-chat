let component = ReasonReact.statelessComponent("RechatUsersListItem");

let make = (~chatUser, _children) => {
  ...component,
  render: (_) => {
    <li>(ReasonReact.stringToElement(chatUser##username))</li>
  }
};
