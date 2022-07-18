import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import SignIn from "./SignIn.js"
import SignUp from "./SignUp.js"
import Home from './Home.js';
import Me from './Me.js';
import Project from './Project.js';



export default function BasicExample() {
  return (
    <Router>
      <div id="body">

        <hr />

        <Routes>
          <Route exact path="/" element={<Home />}>
          </Route>
          <Route path="/about" element={<About />}>
          </Route>
          <Route path="/login" element={<SignIn />}>
          </Route>
          <Route path="/signup" element={<SignUp />}>
          </Route>
          <Route path="/me" element={<Me />}>
          </Route>
          <Route path="/project" element={<Project />}>
          </Route>
        </Routes>
        
      </div>
      
    </Router>
  );
}

// You can think of these components as "pages"
// in your app.


function About() {
  return (
    <div>
      <h2>About</h2>
    </div>
  );
}

function Dashboard() {
  return (
    <div>
      <h2>Dashboard</h2>
    </div>
  );
}
