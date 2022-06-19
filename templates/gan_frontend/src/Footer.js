import {
    Link,
    useNavigate 
  } from "react-router-dom";
import { TextField, Toolbar, AppBar, Button } from "@mui/material"
import svg_logo from './logo.svg';

const headersData = [
    {
      label: "Terms of service",
      href: "/",
    },
    {
      label: "Social links",
      href: "/",
    },
    {
      label: "Contact us",
      href: "/",
    },
  ];

const getMenuButtons = () => {
    return headersData.map(({ label, href }) => {
      return (
        <Button
          {...{
            key: label,
            color: "inherit",
            to: href,
            component: Link,
            className: "toolbarBtn"
          }}
        >
          {label}
        </Button>
      );
    });
  };

export default function Header() {
    
  const navigate = useNavigate();
  const displayDesktop = () => {
      return <Toolbar className={"toolbar"}>
              
              <div style={{ flex: 1 }}>
              <Button onClick={() => navigate('/')}>
              <img src={svg_logo} className="App-logo" alt="logo" height="60"/>
              </Button>
              </div>
              <div>{getMenuButtons()}</div>
  </Toolbar>;
  };
  return (
      <header>
      <AppBar  className={"footer"} position="relative" style={{height: 'auto', bottom: 0, marginTop:-100}}>{displayDesktop()}</AppBar>
      </header>
  );
}