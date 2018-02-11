let component = ReasonReact.statelessComponent("RechatSidebar");

let make = (_children) => {
  ...component,
  render: (_) => {
    <div className="RechatSidebar">
      <RechatUsersList/>
    </div>
  }
}
