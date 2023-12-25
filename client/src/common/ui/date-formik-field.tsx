import { DateField, DateFieldProps } from "@mui/x-date-pickers";
import { useField } from "formik";

type TDateFormikFieldProps = {
  name: string;
} & Omit<DateFieldProps<string>, "error" | "helperText">;

export const DateFormikField = ({ name, ...props }: TDateFormikFieldProps) => {
  const [{ value }, { error, touched }, { setValue }] = useField(name);
  return (
    <DateField
      value={value}
      onChange={setValue}
      error={touched && Boolean(error)}
      helperText={error}
      {...(props as any)}
    />
  );
};
