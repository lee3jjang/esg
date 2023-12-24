import ReactDOM from "react-dom/client";
import { ThemeProvider } from "@mui/material";
import { DefaultAppBar, theme } from "./common";
import { ApolloProvider } from "react-apollo";
import { client } from "./core";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ApolloProvider client={client}>
    <ThemeProvider theme={theme}>
      <DefaultAppBar />
    </ThemeProvider>
  </ApolloProvider>
);
