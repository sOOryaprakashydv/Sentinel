import type { InvestigationDetail } from "@/types";

export default function FileInfoCard({ investigation }: { investigation: InvestigationDetail }) {
  const rows: [string, string][] = [
    ["Filename", investigation.filename],
    ["Size", `${(investigation.size / 1024).toFixed(1)} KB`],
    ["Type", investigation.file_type ?? "Unknown"],
    ["MIME", investigation.mime ?? "—"],
    ["SHA256", investigation.sha256],
    ["SHA1", investigation.sha1],
    ["MD5", investigation.md5],
    ["Uploaded", new Date(investigation.uploaded_at).toLocaleString()],
  ];

  return (
    <div className="panel p-5">
      <h2 className="font-display font-semibold text-ink-900 mb-4">File Information</h2>
      <dl className="grid grid-cols-1 gap-y-2.5 text-sm">
        {rows.map(([k, v]) => (
          <div key={k} className="flex justify-between gap-4">
            <dt className="text-ink-500 shrink-0">{k}</dt>
            <dd className="text-ink-900 font-mono text-xs text-right break-all">{v}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
