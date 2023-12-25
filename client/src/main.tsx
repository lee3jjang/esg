import ReactDOM from "react-dom/client";
import { ThemeProvider } from "@mui/material";
import { DefaultAppBar, theme } from "./common";
import { ApolloProvider } from "react-apollo";
import { client } from "./core";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ApolloProvider client={client}>
    <ThemeProvider theme={theme}>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DefaultAppBar />
      </LocalizationProvider>
    </ThemeProvider>
  </ApolloProvider>
);
