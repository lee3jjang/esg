import { Breadcrumbs, Link } from "@mui/material";

type TSettingsPageProps = { className?: string };

export const SettingsPage = ({ className }: TSettingsPageProps) => {
  return (
    <div className={className}>
      <Breadcrumbs>
        <Link underline="hover" color="inherit" href="/settings">
          설정
        </Link>
      </Breadcrumbs>
      Settings Page
    </div>
  );
};
