import HomeIcon from "@mui/icons-material/Home";
import TimelineIcon from "@mui/icons-material/Timeline";
import SettingsIcon from "@mui/icons-material/Settings";
import { ReactNode } from "react";

export type TMenuListItemProps = {
  icon: ReactNode;
  primaryText: string;
  path: string;
};

export const menuListItems: TMenuListItemProps[] = [
  { icon: <HomeIcon />, primaryText: "홈", path: "/" },
  {
    icon: <TimelineIcon />,
    primaryText: "모수 추정",
    path: "/calibration",
  },
  { icon: <SettingsIcon />, primaryText: "설정", path: "/settings" },
];
