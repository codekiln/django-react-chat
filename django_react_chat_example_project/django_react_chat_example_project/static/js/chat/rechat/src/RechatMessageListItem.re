let component = ReasonReact.statelessComponent("RechatUsersListItem");

let make = (~chatMessage, _children) => {
  ...component,
  render: (_) => {
    <div className="RechatWindow__MessageContainer RechatWindow__MessageContainer--Theirs">
      <div className="RechatWindow__AvatarContainer">
        <MaterialUI.Avatar className="RechatWindow__Avatar">
          (RechatUtils.ste("TH"))
        </MaterialUI.Avatar>
      </div>
      <div className="RechatWindow__Message RechatWindow__Message--Theirs">
        (RechatUtils.ste(chatMessage##text))
      </div>
    </div>
  }
};
