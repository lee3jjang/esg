import { Breadcrumbs, Link } from "@mui/material";
import { SampleDataGrid } from "./sample-data-grid";

type THomePageProps = { className?: string };

export const HomePage = ({ className }: THomePageProps) => {
  return (
    <div className={className}>
      <Breadcrumbs>
        <Link underline="hover" color="inherit" href="/">
          홈
        </Link>
      </Breadcrumbs>
      <SampleDataGrid />
    </div>
  );
};
