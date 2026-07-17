import type { TimelineEventOut } from "@/types";
import { LuCircleCheck, LuCircleX, LuLoaderCircle, LuCircle } from "react-icons/lu";

const STAGE_LABELS: Record<string, string> = {
  upload: "Upload", pipeline: "Pipeline", static_analysis: "Static Analysis",
  ioc_extraction: "IOC Extraction", threat_intelligence: "Threat Intelligence",
  risk_scoring: "Risk Score", mitre_mapping: "MITRE ATT&CK", ai_summary: "AI Summary",
};

function StatusIcon({ status }: { status: string }) {
  if (status === "completed") return <LuCircleCheck className="text-success-600" size={16} />;
  if (status === "failed") return <LuCircleX className="text-critical-600" size={16} />;
  if (status === "started") return <LuLoaderCircle className="text-primary-600 animate-spin" size={16} />;
  return <LuCircle className="text-ink-300" size={16} />;
}

export default function TimelineCard({ events }: { events: TimelineEventOut[] }) {
  return (
    <div className="panel p-5">
      <h2 className="font-display font-semibold text-ink-900 mb-4">Investigation Timeline</h2>
      <div className="space-y-3">
        {events.map((e, i) => (
          <div key={i} className="flex items-start gap-3">
            <StatusIcon status={e.status} />
            <div className="flex-1">
              <div className="text-sm text-ink-900 font-medium">
                {STAGE_LABELS[e.stage] ?? e.stage}
                <span className="text-ink-500 font-normal"> — {e.status}</span>
              </div>
              {e.message && <div className="text-xs text-ink-500">{e.message}</div>}
              <div className="text-[11px] text-ink-300">{new Date(e.timestamp).toLocaleTimeString()}</div>
            </div>
          </div>
        ))}
        {events.length === 0 && <p className="text-sm text-ink-500">No events yet.</p>}
      </div>
    </div>
  );
}
