
import {
    Link
  } from "react-router-dom";
import { TextField, Toolbar, AppBar, Button } from "@mui/material"

const headersData = [
    {
      label: "My images",
      href: "/images",
    },
    {
      label: "My Account",
      href: "/account",
    },
    {
      label: "Login",
      href: "/login",
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
const logo_ = 'temp logo'

const displayDesktop = () => {
    return <Toolbar className={"toolbar"}>
            <div style={{ flex: 1 }}>{logo_}</div>
            <div>{getMenuButtons()}</div>
</Toolbar>;
};
return (
    <header>
    <AppBar  className={"header"}>{displayDesktop()}</AppBar>
    </header>
);
}