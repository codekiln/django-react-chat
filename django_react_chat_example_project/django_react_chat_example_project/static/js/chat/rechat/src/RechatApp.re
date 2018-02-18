[%bs.raw {|require('./RechatApp.scss')|}];


let component = ReasonReact.statelessComponent("RechatApp");

let make = (_children) => {
  ...component,
  render: (_self) =>
    <div className="RechatApp">
      <RechatSidebar/>
      <RechatWindow/>
    </div>
};
