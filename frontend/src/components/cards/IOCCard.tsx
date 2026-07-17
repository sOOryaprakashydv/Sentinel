import { useMemo, useState } from "react";
import type { IOCOut } from "@/types";

export default function IOCCard({ iocs }: { iocs: IOCOut[] }) {
  const [query, setQuery] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");

  const types = useMemo(() => ["all", ...Array.from(new Set(iocs.map((i) => i.type)))], [iocs]);

  const filtered = iocs.filter((i) => {
    const matchesType = typeFilter === "all" || i.type === typeFilter;
    const matchesQuery = i.value.toLowerCase().includes(query.toLowerCase());
    return matchesType && matchesQuery;
  });

  return (
    <div className="panel p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-display font-semibold text-ink-900">Extracted Indicators ({iocs.length})</h2>
      </div>

      <div className="flex gap-2 mb-4">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search IOC value…"
          className="flex-1 text-sm border border-ink-100 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="text-sm border border-ink-100 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          {types.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>

      <div className="max-h-80 overflow-y-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-ink-500 text-xs uppercase tracking-wide">
              <th className="pb-2 font-medium">Type</th>
              <th className="pb-2 font-medium">Value</th>
              <th className="pb-2 font-medium">Confidence</th>
              <th className="pb-2 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((i) => (
              <tr key={i.id} className="border-t border-ink-100">
                <td className="py-2 text-ink-500">{i.type}</td>
                <td className="py-2 font-mono text-xs text-ink-900 break-all max-w-[240px]">{i.value}</td>
                <td className="py-2 text-ink-700">{Math.round(i.confidence * 100)}%</td>
                <td className="py-2 text-ink-500 capitalize">{i.status}</td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr><td colSpan={4} className="py-6 text-center text-ink-500">No indicators match your filters.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
