[%bs.raw {|require('./app.scss')|}];


let component = ReasonReact.statelessComponent("App");

let make = (_children) => {
  ...component,
  render: (_self) =>
    <div className="App">
      <UsersList/>
    </div>
};
