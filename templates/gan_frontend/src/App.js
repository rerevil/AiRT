import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import Header from "./header.js"
import SignIn from "./SignIn.js"
import SignUp from "./SignUp.js"
import Home from './Home.js';



export default function BasicExample() {
  return (
    <Router>
      <div id="body">
      <Header/>

        <hr />

        {/*
          A <Routes> looks through all its children <Route>
          elements and renders the first one whose path
          matches the current URL. Use a <Routes> any time
          you have multiple routes, but you want only one
          of them to render at a time
        */}
        <Routes>
          <Route exact path="/" element={<Home />}>
          </Route>
          <Route path="/about" element={<About />}>
          </Route>
          <Route path="/login" element={<SignIn />}>
          </Route>
          <Route path="/signup" element={<SignUp />}>
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
