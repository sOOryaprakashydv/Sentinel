import { Route, Routes } from "react-router-dom";
import Layout from "@/components/layout/Layout";
import Dashboard from "@/pages/Dashboard";
import Upload from "@/pages/Upload";
import Investigations from "@/pages/Investigations";
import InvestigationDetail from "@/pages/InvestigationDetail";
import Reports from "@/pages/Reports";
import Settings from "@/pages/Settings";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="upload" element={<Upload />} />
        <Route path="investigations" element={<Investigations />} />
        <Route path="investigations/:id" element={<InvestigationDetail />} />
        <Route path="reports" element={<Reports />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
