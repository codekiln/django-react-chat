let component = ReasonReact.statelessComponent("RechatUsersListItem");

let make = (~chatUser, _children) => {
  ...component,
  render: (_) => {
    <MaterialUI.ListItem>
      <MaterialUI.ListItemText primary=(chatUser##username)/>
    </MaterialUI.ListItem>
  }
};
