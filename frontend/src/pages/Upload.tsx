import { useCallback, useState } from "react";
import { useNavigate } from "react-router-dom";
import { LuUploadCloud, LuFile, LuLoaderCircle } from "react-icons/lu";
import { sentinelApi, extractApiError } from "@/services/api";

const SUPPORTED = [".exe", ".dll", ".apk", ".pdf", ".doc(x)", ".xls(x)", ".ppt(x)", ".zip", ".js", ".ps1", ".py", ".bat"];

export default function Upload() {
  const navigate = useNavigate();
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) setFile(dropped);
  }, []);

  const submit = async () => {
    if (!file) return;
    setUploading(true);
    setError(null);
    try {
      const result = await sentinelApi.uploadFile(file);
      navigate(`/investigations/${result.investigation_id}`);
    } catch (err) {
      setError(extractApiError(err));
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl">
      <header className="mb-8">
        <h1 className="text-2xl font-display font-bold text-ink-900">Upload a Suspicious File</h1>
        <p className="text-sm text-ink-500 mt-1">
          Sentinel automatically runs static analysis, IOC extraction, threat intelligence enrichment, risk
          scoring, MITRE mapping, and AI summarization.
        </p>
      </header>

      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`panel border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
          dragging ? "border-primary-500 bg-primary-50" : "border-ink-100"
        }`}
      >
        {file ? (
          <div className="flex flex-col items-center gap-3">
            <LuFile size={36} className="text-primary-600" />
            <div className="font-medium text-ink-900">{file.name}</div>
            <div className="text-xs text-ink-500">{(file.size / 1024).toFixed(1)} KB</div>
            <button onClick={() => setFile(null)} className="text-xs text-ink-500 hover:text-critical-600 underline">
              Remove
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3">
            <LuUploadCloud size={36} className="text-ink-500" />
            <div className="text-ink-700 font-medium">Drag and drop a file here</div>
            <div className="text-xs text-ink-500">or</div>
            <label className="inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white text-sm font-semibold px-4 py-2 rounded-lg cursor-pointer transition-colors">
              Browse Files
              <input
                type="file"
                className="hidden"
                onChange={(e) => e.target.files?.[0] && setFile(e.target.files[0])}
              />
            </label>
          </div>
        )}
      </div>

      <div className="flex flex-wrap gap-1.5 mt-4">
        {SUPPORTED.map((ext) => (
          <span key={ext} className="text-[11px] font-mono bg-ink-100 text-ink-700 px-2 py-1 rounded">
            {ext}
          </span>
        ))}
      </div>

      {error && <div className="mt-4 panel p-3 text-sm text-critical-700 bg-critical-50 border-critical-100">{error}</div>}

      <button
        onClick={submit}
        disabled={!file || uploading}
        className="mt-6 w-full inline-flex items-center justify-center gap-2 bg-primary-600 hover:bg-primary-700 disabled:bg-ink-300 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-colors"
      >
        {uploading ? <><LuLoaderCircle className="animate-spin" size={18} /> Uploading…</> : "Start Investigation"}
      </button>
    </div>
  );
}
