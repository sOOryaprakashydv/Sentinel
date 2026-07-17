import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { LuDownload, LuLoaderCircle } from "react-icons/lu";
import { sentinelApi, extractApiError } from "@/services/api";
import type { ReportOut } from "@/types";

const FORMATS: { key: "pdf" | "html" | "csv" | "json"; label: string }[] = [
  { key: "pdf", label: "PDF" },
  { key: "html", label: "HTML" },
  { key: "csv", label: "CSV" },
  { key: "json", label: "JSON" },
];

export default function Reports() {
  const [searchParams] = useSearchParams();
  const investigationParam = searchParams.get("investigation");
  const [investigationId, setInvestigationId] = useState(investigationParam ?? "");
  const [reports, setReports] = useState<ReportOut[]>([]);
  const [generating, setGenerating] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = () => sentinelApi.listReports().then(setReports).catch(() => {});

  useEffect(() => { refresh(); }, []);

  const generate = async (format: "pdf" | "html" | "csv" | "json") => {
    const id = Number(investigationId);
    if (!id) { setError("Enter a valid investigation ID first."); return; }
    setGenerating(format);
    setError(null);
    try {
      await sentinelApi.generateReport(id, format);
      await refresh();
    } catch (err) {
      setError(extractApiError(err));
    } finally {
      setGenerating(null);
    }
  };

  return (
    <div>
      <header className="mb-6">
        <h1 className="text-2xl font-display font-bold text-ink-900">Reports</h1>
        <p className="text-sm text-ink-500 mt-1">Generate and download investigation reports in multiple formats.</p>
      </header>

      <div className="panel p-5 mb-6">
        <h2 className="font-display font-semibold text-ink-900 mb-3">Generate a Report</h2>
        <div className="flex gap-3 items-end flex-wrap">
          <div>
            <label className="block text-xs text-ink-500 mb-1">Investigation ID</label>
            <input
              value={investigationId}
              onChange={(e) => setInvestigationId(e.target.value)}
              placeholder="e.g. 12"
              className="text-sm border border-ink-100 rounded-lg px-3 py-2 w-40 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          {FORMATS.map((f) => (
            <button
              key={f.key}
              onClick={() => generate(f.key)}
              disabled={generating !== null}
              className="inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 disabled:bg-ink-300 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors"
            >
              {generating === f.key ? <LuLoaderCircle className="animate-spin" size={14} /> : null}
              {f.label}
            </button>
          ))}
        </div>
        {error && <p className="text-sm text-critical-600 mt-3">{error}</p>}
      </div>

      <div className="panel overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-ink-500 text-xs uppercase tracking-wide bg-surface-secondary">
              <th className="px-5 py-3 font-medium">Report ID</th>
              <th className="px-5 py-3 font-medium">Investigation</th>
              <th className="px-5 py-3 font-medium">Format</th>
              <th className="px-5 py-3 font-medium">Generated</th>
              <th className="px-5 py-3 font-medium">Download</th>
            </tr>
          </thead>
          <tbody>
            {reports.length === 0 && (
              <tr><td colSpan={5} className="px-5 py-8 text-center text-ink-500">No reports generated yet.</td></tr>
            )}
            {reports.map((r) => (
              <tr key={r.id} className="border-t border-ink-100 hover:bg-surface-secondary/60">
                <td className="px-5 py-3 text-ink-500">#{r.id}</td>
                <td className="px-5 py-3 text-ink-500">#{r.investigation_id}</td>
                <td className="px-5 py-3 uppercase text-ink-700 font-medium">{r.format}</td>
                <td className="px-5 py-3 text-ink-500">{new Date(r.generated_at).toLocaleString()}</td>
                <td className="px-5 py-3">
                  <a
                    href={sentinelApi.downloadReportUrl(r.investigation_id, r.format)}
                    className="inline-flex items-center gap-1 text-primary-700 hover:underline"
                  >
                    <LuDownload size={14} /> Download
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
