import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { sentinelApi } from "@/services/api";
import type { InvestigationSummary } from "@/types";
import SeverityBadge from "@/components/ui/SeverityBadge";

export default function Investigations() {
  const [items, setItems] = useState<InvestigationSummary[] | null>(null);

  useEffect(() => {
    sentinelApi.listInvestigations().then(setItems).catch(() => setItems([]));
  }, []);

  return (
    <div>
      <header className="mb-6">
        <h1 className="text-2xl font-display font-bold text-ink-900">Investigations</h1>
        <p className="text-sm text-ink-500 mt-1">Every file analyzed on this instance.</p>
      </header>

      <div className="panel overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-ink-500 text-xs uppercase tracking-wide bg-surface-secondary">
              <th className="px-5 py-3 font-medium">Filename</th>
              <th className="px-5 py-3 font-medium">SHA256</th>
              <th className="px-5 py-3 font-medium">Type</th>
              <th className="px-5 py-3 font-medium">Status</th>
              <th className="px-5 py-3 font-medium">Risk</th>
              <th className="px-5 py-3 font-medium">Uploaded</th>
            </tr>
          </thead>
          <tbody>
            {items === null && (
              <tr><td colSpan={6} className="px-5 py-8 text-center text-ink-500">Loading…</td></tr>
            )}
            {items?.length === 0 && (
              <tr><td colSpan={6} className="px-5 py-8 text-center text-ink-500">No investigations yet.</td></tr>
            )}
            {items?.map((inv) => (
              <tr key={inv.id} className="border-t border-ink-100 hover:bg-surface-secondary/60">
                <td className="px-5 py-3">
                  <Link to={`/investigations/${inv.id}`} className="font-medium text-primary-700 hover:underline">
                    {inv.filename}
                  </Link>
                </td>
                <td className="px-5 py-3 font-mono text-xs text-ink-500">{inv.sha256.slice(0, 16)}…</td>
                <td className="px-5 py-3 text-ink-500">{inv.file_type ?? "—"}</td>
                <td className="px-5 py-3 text-ink-500 capitalize">{inv.status.replace(/_/g, " ")}</td>
                <td className="px-5 py-3"><SeverityBadge severity={inv.risk_severity} /></td>
                <td className="px-5 py-3 text-ink-500">{new Date(inv.uploaded_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
