import type { StaticAnalysisOut } from "@/types";

const SEVERITY_STYLES: Record<string, string> = {
  high: "badge-critical", medium: "badge-medium", low: "badge-low", info: "badge-info",
};

export default function StaticAnalysisCard({ analysis }: { analysis: StaticAnalysisOut | null }) {
  if (!analysis) {
    return (
      <div className="panel p-5">
        <h2 className="font-display font-semibold text-ink-900 mb-2">Static Analysis</h2>
        <p className="text-sm text-ink-500">Waiting for static analysis to complete…</p>
      </div>
    );
  }

  return (
    <div className="panel p-5">
      <h2 className="font-display font-semibold text-ink-900 mb-4">Static Analysis</h2>

      <div className="flex gap-6 text-sm mb-4">
        <div>
          <div className="text-ink-500 text-xs uppercase tracking-wide">Entropy</div>
          <div className="font-mono text-ink-900">{analysis.entropy?.toFixed(2) ?? "—"}</div>
        </div>
        <div>
          <div className="text-ink-500 text-xs uppercase tracking-wide">Packed</div>
          <div className="font-mono text-ink-900">{analysis.is_packed ? "Yes" : "No"}</div>
        </div>
        <div>
          <div className="text-ink-500 text-xs uppercase tracking-wide">Sections</div>
          <div className="font-mono text-ink-900">{analysis.sections_json.length}</div>
        </div>
        <div>
          <div className="text-ink-500 text-xs uppercase tracking-wide">Imports</div>
          <div className="font-mono text-ink-900">{analysis.imports_json.length}</div>
        </div>
      </div>

      <h3 className="text-xs font-semibold text-ink-500 uppercase tracking-wide mb-2">Security Findings</h3>
      <div className="space-y-2">
        {analysis.security_findings_json.length === 0 && (
          <p className="text-sm text-ink-500">No notable findings.</p>
        )}
        {analysis.security_findings_json.map((f, i) => (
          <div key={i} className="flex items-start gap-2 text-sm border-t border-ink-100 pt-2 first:border-0 first:pt-0">
            <span className={`badge ${SEVERITY_STYLES[f.severity] ?? "badge-info"} shrink-0`}>{f.severity}</span>
            <div>
              <div className="text-ink-900 font-medium">{f.title}</div>
              <div className="text-ink-500 text-xs mt-0.5">{f.detail}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
