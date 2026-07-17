import axios from "axios";
import type {
  AISummaryOut, DashboardStats, InvestigationDetail, InvestigationSummary,
  IOCOut, MitreMappingOut, ReportOut, RiskScoreOut, StaticAnalysisOut,
  ThreatIntelResultOut,
} from "@/types";

const api = axios.create({ baseURL: "/api/v1" });

export interface ApiError {
  success: false;
  error: string;
  code: string;
}

export function extractApiError(err: unknown): string {
  if (axios.isAxiosError(err) && err.response?.data?.error) {
    return err.response.data.error as string;
  }
  return "Something went wrong. Please try again.";
}

export const sentinelApi = {
  health: () => api.get("/health").then((r) => r.data),

  uploadFile: (file: File, caseId?: number) => {
    const form = new FormData();
    form.append("file", file);
    const params = caseId ? { case_id: caseId } : {};
    return api
      .post<{ investigation_id: number; status: string; filename: string }>("/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
        params,
      })
      .then((r) => r.data);
  },

  listInvestigations: () => api.get<InvestigationSummary[]>("/investigations").then((r) => r.data),

  getInvestigation: (id: number) => api.get<InvestigationDetail>(`/investigations/${id}`).then((r) => r.data),

  getStaticAnalysis: (id: number) => api.get<StaticAnalysisOut>(`/investigations/${id}/static`).then((r) => r.data),

  getIocs: (id: number) => api.get<{ total: number; items: IOCOut[] }>(`/investigations/${id}/iocs`).then((r) => r.data),

  getThreatIntel: (id: number) =>
    api.get<{ results: ThreatIntelResultOut[]; online: boolean }>(`/investigations/${id}/threat-intelligence`).then((r) => r.data),

  getRisk: (id: number) => api.get<RiskScoreOut>(`/investigations/${id}/risk`).then((r) => r.data),

  getMitre: (id: number) =>
    api.get<{ total: number; items: MitreMappingOut[] }>(`/investigations/${id}/mitre`).then((r) => r.data),

  getAISummary: (id: number) => api.get<AISummaryOut>(`/investigations/${id}/summary`).then((r) => r.data),

  getDashboardStats: () => api.get<DashboardStats>("/dashboard/stats").then((r) => r.data),

  generateReport: (id: number, format: "pdf" | "html" | "csv" | "json") =>
    api.post<ReportOut>(`/reports/${id}/generate`, { format }).then((r) => r.data),

  downloadReportUrl: (id: number, format: string) => `/api/v1/reports/${id}/download?fmt=${format}`,

  listReports: () => api.get<ReportOut[]>("/reports").then((r) => r.data),
};
