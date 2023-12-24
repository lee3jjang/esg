import { Box, Drawer, DrawerProps, List, styled } from "@mui/material";
import { DrawerMenuListItem } from "./drawer-menu-list-item";
import { TMenuListItemProps } from "../menu-list-items";

type TDefaultDrawerProps = {
  className?: string;
  menuListItems: TMenuListItemProps[];
} & DrawerProps;

export const DefaultDrawer = styled(
  ({ className, menuListItems, ...drawerProps }: TDefaultDrawerProps) => {
    return (
      <Drawer anchor="left" {...drawerProps}>
        <Box sx={{ width: 300 }}>
          <List>
            {menuListItems.map((value, index) => (
              <DrawerMenuListItem key={index} {...value} />
            ))}
          </List>
        </Box>
      </Drawer>
    );
  }
)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
}));
