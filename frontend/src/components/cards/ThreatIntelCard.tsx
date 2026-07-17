import type { ThreatIntelResultOut } from "@/types";

const STATUS_LABEL: Record<string, string> = {
  success: "Online", not_found: "Not Found", error: "Unavailable",
  not_configured: "Not Configured", rate_limited: "Rate Limited",
};

export default function ThreatIntelCard({ results }: { results: ThreatIntelResultOut[] }) {
  return (
    <div className="panel p-5">
      <h2 className="font-display font-semibold text-ink-900 mb-4">Threat Intelligence</h2>
      <div className="space-y-4">
        {results.map((r) => (
          <div key={r.provider} className="border-t border-ink-100 pt-3 first:border-0 first:pt-0">
            <div className="flex items-center justify-between">
              <div className="font-medium text-ink-900 capitalize">{r.provider}</div>
              <span className={`badge ${r.status === "success" ? "badge-low" : "badge-info"}`}>
                {STATUS_LABEL[r.status] ?? r.status}
              </span>
            </div>
            {r.status === "success" ? (
              <div className="text-sm text-ink-700 mt-1.5 space-y-0.5">
                {r.detections !== null && r.total_engines !== null && (
                  <div>Detections: <span className="font-mono">{r.detections} / {r.total_engines}</span></div>
                )}
                {r.malware_family && <div>Family: <span className="font-medium">{r.malware_family}</span></div>}
                {r.tags_json.length > 0 && <div className="text-xs text-ink-500">{r.tags_json.join(", ")}</div>}
              </div>
            ) : (
              <div className="text-xs text-ink-500 mt-1">{r.error_message ?? "No data available."}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
