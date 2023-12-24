import { gql } from "@apollo/client";

export const CREATE_CALIBRATION_MUTATION = gql`
  mutation CreateCalibration(
    $createCalibrationInput: CreateCalibrationInputType!
  ) {
    createCalibration(createCalibrationInput: $createCalibrationInput) {
      id
    }
  }
`;
