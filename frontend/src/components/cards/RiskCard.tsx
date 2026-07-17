import type { RiskScoreOut } from "@/types";
import SeverityBadge from "@/components/ui/SeverityBadge";

const SEVERITY_COLOR: Record<string, string> = {
  Critical: "#dc2626", High: "#ea580c", Medium: "#d97706", Low: "#16a34a", Informational: "#6b7280",
};

export default function RiskCard({ risk }: { risk: RiskScoreOut | null }) {
  if (!risk) {
    return (
      <div className="panel p-5">
        <h2 className="font-display font-semibold text-ink-900 mb-2">Risk Score</h2>
        <p className="text-sm text-ink-500">Calculating…</p>
      </div>
    );
  }

  const color = SEVERITY_COLOR[risk.severity] ?? "#6b7280";

  return (
    <div className="panel p-5">
      <h2 className="font-display font-semibold text-ink-900 mb-4">Risk Score</h2>
      <div className="flex items-center gap-5">
        <div className="text-5xl font-display font-extrabold" style={{ color }}>{risk.score}</div>
        <div>
          <SeverityBadge severity={risk.severity} />
          <div className="text-xs text-ink-500 mt-1.5">Confidence: {Math.round(risk.confidence * 100)}%</div>
        </div>
      </div>

      <div className="mt-4 h-2.5 rounded-full bg-ink-100 overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${risk.score}%`, background: color }} />
      </div>

      <div className="mt-4 space-y-1.5">
        {risk.reasons_json.map((r) => (
          <div key={r.rule} className="flex items-center justify-between text-sm">
            <span className="text-ink-700">✔ {r.label}</span>
            <span className="text-ink-500 font-mono text-xs">+{r.points}</span>
          </div>
        ))}
        {risk.reasons_json.length === 0 && (
          <p className="text-sm text-ink-500">No rule matches — no significant risk indicators were found.</p>
        )}
      </div>
    </div>
  );
}
