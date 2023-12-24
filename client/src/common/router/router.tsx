import { BrowserRouter, Route, Routes } from "react-router-dom";
import {
  CalibrationListPage,
  HomePage,
  SettingsPage,
  CalibrationPage,
  CalibrationCreatePage,
} from "../../packages";

export const Router = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/calibration" element={<CalibrationListPage />} />
      <Route path="/calibration/:calibrationId" element={<CalibrationPage />} />
      <Route path="/calibration/create" element={<CalibrationCreatePage />} />
      <Route path="/settings" element={<SettingsPage />} />
    </Routes>
  </BrowserRouter>
);
