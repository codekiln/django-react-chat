// Generated by BUCKLESCRIPT VERSION 2.1.0, PLEASE EDIT WITH CARE
'use strict';

import * as React       from "react";
import * as ReasonReact from "reason-react/src/ReasonReact.js";

((require('./app.scss')));

var component = ReasonReact.statelessComponent("App");

function make(message, _) {
  var newrecord = component.slice();
  newrecord[/* render */9] = (function () {
      return React.createElement("div", {
                  className: "App"
                }, React.createElement("div", {
                      className: "App-header"
                    }, React.createElement("h2", undefined, message)), React.createElement("p", {
                      className: "App-intro"
                    }, "To get started, edit", React.createElement("code", undefined, " src/app.re "), "and save to reload, then jump."));
    });
  return newrecord;
}

export {
  component ,
  make      ,
  
}
/*  Not a pure module */