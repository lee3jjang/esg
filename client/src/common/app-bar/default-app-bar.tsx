import { useState } from "react";
import { AppBar, IconButton, Toolbar, Typography } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { DefaultDrawer } from "./drawer";
import { menuListItems } from "./menu-list-items";
import { Router } from "../router";

type TDefaultAppBarProps = { className?: string };

export const DefaultAppBar = ({ className }: TDefaultAppBarProps) => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <AppBar className={className} position="static">
        <Toolbar variant="dense">
          <IconButton
            edge="start"
            color="inherit"
            sx={{ mr: 2 }}
            onClick={() => {
              setOpen(true);
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" color="inherit" component="div">
            내 블로그
          </Typography>
          <DefaultDrawer
            open={open}
            menuListItems={menuListItems}
            onClose={() => {
              setOpen(false);
            }}
          />
        </Toolbar>
      </AppBar>
      <Router />
    </>
  );
};
