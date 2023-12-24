import {
  Box,
  Breadcrumbs,
  Button,
  Link,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import { useQuery } from "@apollo/react-hooks";
import { CALIBRATION_LIST_QUERY } from "../graphql";

type TCalibrationListPageProps = { className?: string };

export const CalibrationListPage = ({
  className,
}: TCalibrationListPageProps) => {
  const { loading, error, data } = useQuery<{
    calibrationList: {
      id: string;
      title: string;
      baseDate: string;
      createdAt: string;
    }[];
  }>(CALIBRATION_LIST_QUERY);
  if (loading) return <div>loading...</div>;
  if (!data || error) return <div>error</div>;

  return (
    <Box className={className} component="section">
      <Breadcrumbs>
        <Link underline="hover" color="inherit" href="/calibration">
          모수 추정
        </Link>
      </Breadcrumbs>
      <Box sx={{ width: 700 }}>
        <Box display="flex" justifyContent="space-between" marginBottom={2}>
          <Typography variant="h5">모수 추정</Typography>
          <Button variant="contained" size="small" href="/calibration/create">
            모수 추정 생성
          </Button>
        </Box>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>제목</TableCell>
                <TableCell>기준일</TableCell>
                <TableCell>생성일시</TableCell>
                <TableCell>링크</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.calibrationList.map(
                ({ id, title, baseDate, createdAt }) => (
                  <TableRow key={id}>
                    <TableCell>{id}</TableCell>
                    <TableCell>{title}</TableCell>
                    <TableCell>{baseDate}</TableCell>
                    <TableCell>{createdAt}</TableCell>
                    <TableCell>
                      <Button
                        variant="outlined"
                        size="small"
                        href={`calibration/${id}`}
                      >
                        바로가기
                      </Button>
                    </TableCell>
                  </TableRow>
                )
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Box>
  );
};
