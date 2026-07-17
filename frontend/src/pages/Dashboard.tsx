import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  LuFolderOpen, LuUpload, LuTriangleAlert, LuFileWarning, LuFileText,
  LuWifi, LuWifiOff, LuBrainCircuit,
} from "react-icons/lu";
import { sentinelApi } from "@/services/api";
import type { DashboardStats } from "@/types";
import StatCard from "@/components/ui/StatCard";
import SeverityBadge from "@/components/ui/SeverityBadge";

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    sentinelApi.getDashboardStats().then(setStats).catch(() => setError("Could not load dashboard data."));
  }, []);

  return (
    <div>
      <header className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-display font-bold text-ink-900">Sentinel Dashboard</h1>
          <p className="text-sm text-ink-500 mt-1">Overview of every investigation on this instance.</p>
        </div>
        <Link
          to="/upload"
          className="inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white text-sm font-semibold px-4 py-2.5 rounded-lg transition-colors"
        >
          <LuUpload size={16} /> New Investigation
        </Link>
      </header>

      {error && <div className="panel p-4 mb-6 text-critical-700 bg-critical-50 border-critical-100">{error}</div>}

      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <StatCard label="Total Investigations" value={stats?.total_investigations ?? "—"} icon={LuFolderOpen} tone="primary" />
        <StatCard label="Uploaded Today" value={stats?.files_uploaded_today ?? "—"} icon={LuUpload} tone="neutral" />
        <StatCard label="High Risk Samples" value={stats?.high_risk_samples ?? "—"} icon={LuFileWarning} tone="warning" />
        <StatCard label="Critical Alerts" value={stats?.critical_alerts ?? "—"} icon={LuTriangleAlert} tone="critical" />
        <StatCard label="Reports Generated" value={stats?.reports_generated ?? "—"} icon={LuFileText} tone="success" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 panel p-5">
          <h2 className="font-display font-semibold text-ink-900 mb-4">Recent Uploads</h2>
          {!stats ? (
            <div className="text-sm text-ink-500">Loading…</div>
          ) : stats.recent_uploads.length === 0 ? (
            <div className="text-sm text-ink-500">No investigations yet. Upload a file to get started.</div>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-ink-500 text-xs uppercase tracking-wide">
                  <th className="pb-2 font-medium">Filename</th>
                  <th className="pb-2 font-medium">Type</th>
                  <th className="pb-2 font-medium">Status</th>
                  <th className="pb-2 font-medium">Risk</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_uploads.map((inv) => (
                  <tr key={inv.id} className="border-t border-ink-100 hover:bg-surface-secondary/60">
                    <td className="py-2.5">
                      <Link to={`/investigations/${inv.id}`} className="font-medium text-primary-700 hover:underline">
                        {inv.filename}
                      </Link>
                    </td>
                    <td className="py-2.5 text-ink-500">{inv.file_type ?? "—"}</td>
                    <td className="py-2.5 text-ink-500 capitalize">{inv.status.replace(/_/g, " ")}</td>
                    <td className="py-2.5"><SeverityBadge severity={inv.risk_severity} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="panel p-5">
          <h2 className="font-display font-semibold text-ink-900 mb-4">System Status</h2>
          <div className="space-y-3 text-sm">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-ink-700">
                {stats?.threat_intelligence_online ? <LuWifi className="text-success-600" /> : <LuWifiOff className="text-ink-500" />}
                Threat Intelligence
              </span>
              <span className={stats?.threat_intelligence_online ? "text-success-700 font-medium" : "text-ink-500"}>
                {stats?.threat_intelligence_online ? "Online" : "Not Configured"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-ink-700">
                <LuBrainCircuit className={stats?.ai_online ? "text-success-600" : "text-ink-500"} />
                AI Summaries
              </span>
              <span className={stats?.ai_online ? "text-success-700 font-medium" : "text-ink-500"}>
                {stats?.ai_online ? "Gemini" : "Rule-based fallback"}
              </span>
            </div>
          </div>
          <p className="text-xs text-ink-500 mt-4 leading-relaxed">
            Sentinel remains fully functional even without external API keys configured — investigations still run
            through static analysis, IOC extraction, risk scoring, and MITRE mapping.
          </p>
        </div>
      </div>
    </div>
  );
}
