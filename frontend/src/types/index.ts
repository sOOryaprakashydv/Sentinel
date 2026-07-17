export type Severity = "Informational" | "Low" | "Medium" | "High" | "Critical";

export interface InvestigationSummary {
  id: number;
  filename: string;
  file_type: string | null;
  size: number;
  sha256: string;
  status: string;
  uploaded_at: string;
  risk_severity: Severity | null;
  risk_score: number | null;
}

export interface TimelineEventOut {
  stage: string;
  status: string;
  message: string | null;
  timestamp: string;
}

export interface InvestigationDetail {
  id: number;
  case_id: number | null;
  filename: string;
  size: number;
  mime: string | null;
  file_type: string | null;
  sha256: string;
  sha1: string;
  md5: string;
  status: string;
  error_message: string | null;
  uploaded_at: string;
  completed_at: string | null;
  timeline_events: TimelineEventOut[];
}

export interface SecurityFinding {
  title: string;
  severity: "info" | "low" | "medium" | "high";
  detail: string;
}

export interface StaticAnalysisOut {
  metadata_json: Record<string, unknown>;
  sections_json: Record<string, unknown>[];
  imports_json: { dll: string; functions: string[] }[];
  exports_json: string[];
  resources_json: Record<string, unknown>[];
  permissions_json: string[];
  certificate_json: Record<string, unknown> | null;
  security_findings_json: SecurityFinding[];
  entropy: number | null;
  compiler: string | null;
  is_packed: boolean;
  yara_matches_json: unknown[];
  created_at: string;
}

export interface IOCOut {
  id: number;
  type: string;
  value: string;
  confidence: number;
  source: string;
  evidence: string | null;
  status: string;
  created_at: string;
}

export interface ThreatIntelResultOut {
  provider: string;
  status: string;
  malware_family: string | null;
  detections: number | null;
  total_engines: number | null;
  confidence: number | null;
  tags_json: string[];
  error_message: string | null;
  queried_at: string;
}

export interface RiskReason {
  rule: string;
  label: string;
  points: number;
}

export interface RiskScoreOut {
  score: number;
  severity: Severity;
  confidence: number;
  reasons_json: RiskReason[];
  created_at: string;
}

export interface MitreMappingOut {
  technique_id: string;
  technique_name: string;
  tactic: string;
  description: string;
  evidence: string;
  confidence: number;
}

export interface AISummaryOut {
  executive_summary: string;
  technical_summary: string;
  recommendations_json: string[];
  confidence: number;
  source: "gemini" | "rule_based_fallback" | "unavailable";
}

export interface ReportOut {
  id: number;
  investigation_id: number;
  format: string;
  status: string;
  generated_at: string;
}

export interface DashboardStats {
  total_investigations: number;
  files_uploaded_today: number;
  high_risk_samples: number;
  critical_alerts: number;
  reports_generated: number;
  threat_intelligence_online: boolean;
  ai_online: boolean;
  recent_uploads: InvestigationSummary[];
}
