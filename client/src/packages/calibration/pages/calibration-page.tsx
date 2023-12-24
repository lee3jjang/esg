import _ from "lodash";
import {
  Box,
  Breadcrumbs,
  Link,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  Typography,
} from "@mui/material";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { CALIBRAITON_QUERY } from "../graphql";

type TCalibrationPageProps = { className?: string };

export const CalibrationPage = ({ className }: TCalibrationPageProps) => {
  const { calibrationId } = useParams<{ calibrationId: string }>();

  const { loading, error, data } = useQuery<{
    calibration: {
      id: string;
      title: string;
      baseDate: string;
      createdAt: string;
    };
  }>(CALIBRAITON_QUERY, {
    variables: { calibrationId },
  });
  if (loading) return <div>loading...</div>;
  if (!data || error) return <div>error</div>;
  const {
    calibration: { id, title, baseDate, createdAt },
  } = data;

  return (
    <div className={className}>
      <Breadcrumbs>
        <Link underline="hover" color="inherit" href="/calibration">
          모수 추정
        </Link>
        모수 추정 상세
      </Breadcrumbs>
      <Box>
        <Typography variant="h5">모수 추정 상세</Typography>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableBody>
              <TableCell>ID</TableCell>
              <TableCell>{id}</TableCell>
            </TableBody>
            <TableBody>
              <TableCell>제목</TableCell>
              <TableCell>{title}</TableCell>
            </TableBody>
            <TableBody>
              <TableCell>기준일</TableCell>
              <TableCell>{baseDate}</TableCell>
            </TableBody>
            <TableBody>
              <TableCell>생성일시</TableCell>
              <TableCell>{createdAt}</TableCell>
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </div>
  );
};
