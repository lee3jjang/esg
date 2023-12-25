import { TextField, TextFieldProps } from "@mui/material";
import { useField } from "formik";

type TTextFormikFieldProps = {
  name: string;
} & Omit<TextFieldProps, "error" | "helperText">;

export const TextFormikField = ({ name, ...props }: TTextFormikFieldProps) => {
  const [field, { touched, error }] = useField<string>(name);

  return (
    <TextField
      {...field}
      error={touched && Boolean(error)}
      helperText={error}
      {...props}
    />
  );
};
