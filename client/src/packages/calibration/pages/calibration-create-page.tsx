import _ from "lodash";
import { Box, Breadcrumbs, Link } from "@mui/material";
import { ErrorMessage, Field, Form, Formik } from "formik";
import { useMutation } from "react-apollo";
import { CREATE_CALIBRATION_MUTATION } from "../graphql";

type TCalibrationCreatePageProps = { className?: string };

export const CalibrationCreatePage = ({
  className,
}: TCalibrationCreatePageProps) => {
  const [mutate] = useMutation(CREATE_CALIBRATION_MUTATION);

  return (
    <Box className={className} component="section">
      <Breadcrumbs>
        <Link underline="hover" color="inherit" href="/calibration">
          모수 추정
        </Link>
        모수 추정 생성
      </Breadcrumbs>
      <Formik
        initialValues={{ title: "", baseDate: "" }}
        validate={({ title, baseDate }) => {
          const errors: { title?: string; baseDate?: string } = {};

          if (!title) {
            errors.title = "제목을 입력하세요.";
          }
          if (!baseDate) {
            errors.baseDate = "기준일을 입력하세요.";
          }

          return errors;
        }}
        onSubmit={async ({ title, baseDate }, { setSubmitting, resetForm }) => {
          await mutate({
            variables: { createCalibrationInput: { title, baseDate } },
          });
          setSubmitting(false);
          resetForm();
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <Box display="flex" flexDirection="column" gap={1}>
              <Field type="text" name="title" />
              <ErrorMessage name="title" component="div" />
              <Field type="baseDate" name="baseDate" />
              <ErrorMessage name="baseDate" component="div" />
              <button type="submit" disabled={isSubmitting}>
                생성
              </button>
            </Box>
          </Form>
        )}
      </Formik>
    </Box>
  );
};
