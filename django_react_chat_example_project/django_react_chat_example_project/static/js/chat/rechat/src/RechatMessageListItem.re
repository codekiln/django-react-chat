let component = ReasonReact.statelessComponent("RechatUsersListItem");

let make = (~chatMessage, _children) => {
  ...component,
  render: (_) => {
    <li>
      <a className="chatgroup-link" rel="ignore">
        <div className="chatgroup-item">
          <div className="avatar-container">
            <div className="avatar"></div>
          </div>
          <div className="status-container">
            <div className="status-indicator">
              <span></span>
            </div>
          </div>
          <div className="name">(ReasonReact.stringToElement(chatMessage##text))</div>
          <div className="rightBuffer"></div>
        </div>
      </a>
    </li>
  }
};
