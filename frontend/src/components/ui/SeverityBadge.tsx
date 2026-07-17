import type { Severity } from "@/types";

const STYLES: Record<string, string> = {
  Critical: "badge-critical",
  High: "badge-high",
  Medium: "badge-medium",
  Low: "badge-low",
  Informational: "badge-info",
};

export default function SeverityBadge({ severity }: { severity: Severity | string | null | undefined }) {
  if (!severity) return <span className="badge badge-info">Pending</span>;
  return <span className={`badge ${STYLES[severity] ?? "badge-info"}`}>{severity}</span>;
}
