import { useEffect, useState } from "react";
import { sentinelApi } from "@/services/api";

interface HealthInfo {
  status: string;
  version: string;
  threat_intel_configured: boolean;
  ai_configured: boolean;
}

export default function Settings() {
  const [health, setHealth] = useState<HealthInfo | null>(null);

  useEffect(() => {
    sentinelApi.health().then(setHealth).catch(() => {});
  }, []);

  return (
    <div className="max-w-2xl">
      <header className="mb-6">
        <h1 className="text-2xl font-display font-bold text-ink-900">Settings</h1>
        <p className="text-sm text-ink-500 mt-1">
          Sentinel demo configuration is managed via environment variables (.env) on the backend.
          Authentication and multi-user settings are out of scope for this demo build.
        </p>
      </header>

      <div className="panel p-5 space-y-4">
        <Row label="Backend Version" value={health?.version ?? "—"} />
        <Row label="Backend Status" value={health?.status ?? "checking…"} />
        <Row
          label="Threat Intelligence"
          value={health?.threat_intel_configured ? "Configured" : "Not configured (set VT_API_KEY / MALWAREBAZAAR_API_KEY)"}
        />
        <Row
          label="AI Summaries"
          value={health?.ai_configured ? "Gemini configured" : "Using rule-based fallback (set GEMINI_API_KEY)"}
        />
      </div>

      <div className="panel p-5 mt-6">
        <h2 className="font-display font-semibold text-ink-900 mb-2">Environment file</h2>
        <p className="text-sm text-ink-500 leading-relaxed">
          Copy <code className="bg-ink-100 px-1.5 py-0.5 rounded text-xs">.env.example</code> to{" "}
          <code className="bg-ink-100 px-1.5 py-0.5 rounded text-xs">.env</code> in the project root and add your
          API keys, then restart the backend for changes to take effect.
        </p>
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between items-center border-b border-ink-100 pb-3 last:border-0 last:pb-0">
      <span className="text-sm text-ink-500">{label}</span>
      <span className="text-sm font-medium text-ink-900">{value}</span>
    </div>
  );
}
