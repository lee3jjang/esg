import { gql } from "@apollo/client";

export const CALIBRATION_LIST_QUERY = gql`
  query CalibrationList {
    calibrationList {
      id
      title
      baseDate
      createdAt
    }
  }
`;

export const CALIBRAITON_QUERY = gql`
  query Calibration($calibrationId: ID!) {
    calibration(calibrationId: $calibrationId) {
      id
      title
      baseDate
      createdAt
    }
  }
`;
