import {
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import { ReactNode } from "react";

type TDrawerMenuItemProps = {
  className?: string;
  icon: ReactNode;
  primaryText: string;
  path: string;
};

export const DrawerMenuListItem = ({
  className,
  icon,
  path,
  primaryText,
}: TDrawerMenuItemProps) => (
  <ListItem className={className} disablePadding>
    <ListItemButton href={path}>
      <ListItemIcon>{icon}</ListItemIcon>
      <ListItemText primary={primaryText} />
    </ListItemButton>
  </ListItem>
);
