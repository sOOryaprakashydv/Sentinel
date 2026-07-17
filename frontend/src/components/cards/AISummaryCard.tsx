import type { AISummaryOut } from "@/types";
import { LuBrainCircuit, LuSparkles } from "react-icons/lu";

export default function AISummaryCard({ summary }: { summary: AISummaryOut | null }) {
  if (!summary) {
    return (
      <div className="panel p-5">
        <h2 className="font-display font-semibold text-ink-900 mb-2">AI Investigation Summary</h2>
        <p className="text-sm text-ink-500">Generating summary…</p>
      </div>
    );
  }

  return (
    <div className="panel p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-display font-semibold text-ink-900 flex items-center gap-2">
          <LuBrainCircuit className="text-primary-600" size={18} /> AI Investigation Summary
        </h2>
        <span className="badge badge-info flex items-center gap-1">
          <LuSparkles size={12} />
          {summary.source === "gemini" ? "Gemini" : "Rule-based"} · {Math.round(summary.confidence * 100)}%
        </span>
      </div>

      <h3 className="text-xs font-semibold text-ink-500 uppercase tracking-wide mb-1.5">Executive Summary</h3>
      <p className="text-sm text-ink-900 mb-4 leading-relaxed">{summary.executive_summary}</p>

      <h3 className="text-xs font-semibold text-ink-500 uppercase tracking-wide mb-1.5">Technical Explanation</h3>
      <pre className="text-sm text-ink-700 whitespace-pre-wrap font-body mb-4 leading-relaxed">
        {summary.technical_summary}
      </pre>

      <h3 className="text-xs font-semibold text-ink-500 uppercase tracking-wide mb-1.5">Recommendations</h3>
      <ul className="text-sm text-ink-900 space-y-1">
        {summary.recommendations_json.map((r, i) => (
          <li key={i} className="flex gap-2">
            <span className="text-primary-600">•</span> {r}
          </li>
        ))}
      </ul>
    </div>
  );
}
