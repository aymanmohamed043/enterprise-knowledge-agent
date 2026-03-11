import { useCallback, useState, type ChangeEvent, type DragEvent } from "react";
import { useAuth } from "../../context/AuthContext";
import { apiUpload } from "../../api/client";

const ALLOWED = ["admin", "hr"];

export function UploadCard() {
  const { user } = useAuth();
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<{
    message: string;
    filename: string;
    ai_insights?: { summary: string; keywords: string };
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const canUpload = user && ALLOWED.includes(user.role);

  const doUpload = useCallback(async (file: File) => {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are allowed.");
      return;
    }
    setError(null);
    setResult(null);
    setUploading(true);
    try {
      const data = await apiUpload(file);
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }, []);

  const onDrop = useCallback(
    (e: DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) doUpload(file);
    },
    [doUpload]
  );

  const onDragOver = useCallback((e: DragEvent) => {
    e.preventDefault();
    setDragging(true);
  }, []);

  const onDragLeave = useCallback((e: DragEvent) => {
    e.preventDefault();
    setDragging(false);
  }, []);

  const onFileInput = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) doUpload(file);
      e.target.value = "";
    },
    [doUpload]
  );

  if (!canUpload) {
    return (
      <div className="rounded-xl border border-border bg-card/60 px-4 py-3 backdrop-blur-sm">
        <p className="text-sm text-text-muted">
          Only Admin and HR can upload documents. Your role: <strong className="text-text-primary">{user?.role}</strong>
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <h2 className="text-sm font-semibold text-text-primary">Upload PDF to Knowledge Base</h2>
      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        className={`relative cursor-pointer rounded-xl border-2 border-dashed bg-card/40 px-4 py-4 text-center backdrop-blur-md transition-all ${
          dragging
            ? "border-accent bg-accent/10 shadow-glow"
            : "border-border hover:border-accent/50 hover:shadow-glow-sm"
        } ${uploading ? "pointer-events-none opacity-80" : ""}`}
      >
        <input
          type="file"
          accept=".pdf,application/pdf"
          onChange={onFileInput}
          disabled={uploading}
          className="absolute inset-0 cursor-pointer opacity-0"
        />
        <div className="flex flex-col items-center gap-1.5">
          <div className="rounded-lg bg-background/60 p-2">
            <PdfIcon className="h-8 w-8 text-accent" />
          </div>
          <p className="text-sm font-medium text-text-primary">
            {uploading ? "Indexing…" : "Drag & Drop a PDF"}
          </p>
          <p className="text-xs text-accent hover:underline">
            …or click to browse
          </p>
        </div>
      </div>
      <p className="text-xs text-text-muted">
        File size limit 10 MB. Supported format: PDF.
      </p>
      {error && <p className="text-sm text-red-400">{error}</p>}
      {result && (
        <div className="rounded-lg border border-border bg-card/60 px-4 py-3">
          <p className="text-sm text-emerald-400">✔ {result.message}</p>
          <p className="text-xs text-text-muted">{result.filename}</p>
        </div>
      )}
    </div>
  );
}

function PdfIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M7 18h2v-2H7v2zm4 0h2v-2h-2v2zm4 0h2v-2h-2v2zM5 22h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2zM5 4h14v16H5V4z" />
    </svg>
  );
}
