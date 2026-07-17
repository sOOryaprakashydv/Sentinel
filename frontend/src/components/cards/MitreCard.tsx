import type { MitreMappingOut } from "@/types";

export default function MitreCard({ mappings }: { mappings: MitreMappingOut[] }) {
  return (
    <div className="panel p-5">
      <h2 className="font-display font-semibold text-ink-900 mb-4">MITRE ATT&amp;CK</h2>
      {mappings.length === 0 ? (
        <p className="text-sm text-ink-500">No techniques were mapped from the available evidence.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {mappings.map((m) => (
            <div key={m.technique_id} className="border border-ink-100 rounded-lg p-3.5">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-semibold text-primary-700">{m.technique_id}</span>
                <span className="text-xs text-ink-500">{Math.round(m.confidence * 100)}%</span>
              </div>
              <div className="font-medium text-ink-900 text-sm mt-1">{m.technique_name}</div>
              <div className="text-xs text-ink-500 mt-1">{m.tactic}</div>
              <div className="text-xs text-ink-700 mt-2 leading-relaxed">{m.evidence}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
