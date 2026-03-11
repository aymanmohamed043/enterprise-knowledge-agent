import { useCallback, useState, type ChangeEvent, type DragEvent } from "react";
import { useAuth } from "../context/AuthContext";
import { apiUpload } from "../api/client";
import styles from "./UploadPortal.module.css";

const ALLOWED = ["admin", "hr"];

export function UploadPortal() {
  const { user } = useAuth();
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<{ message: string; filename: string; ai_insights?: { summary: string; keywords: string } } | null>(null);
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
      <div className={styles.wrapper}>
        <p className={styles.forbidden}>
          Only Admin and HR can upload documents. Your role: <strong>{user?.role}</strong>
        </p>
      </div>
    );
  }

  return (
    <div className={styles.wrapper}>
      <h3 className={styles.title}>Upload PDF to Knowledge Base</h3>
      <div
        className={`${styles.dropZone} ${dragging ? styles.dragging : ""} ${uploading ? styles.uploading : ""}`}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
      >
        <input
          type="file"
          accept=".pdf,application/pdf"
          onChange={onFileInput}
          disabled={uploading}
          className={styles.input}
        />
        {uploading ? (
          <span>Indexing…</span>
        ) : (
          <span>Drop a PDF here or click to browse</span>
        )}
      </div>
      {error && <p className={styles.error}>{error}</p>}
      {result && (
        <div className={styles.result}>
          <p className={styles.success}>{result.message}</p>
          <p className={styles.filename}>{result.filename}</p>
          {result.ai_insights && (
            <div className={styles.insights}>
              <p><strong>Summary:</strong> {result.ai_insights.summary}</p>
              <p><strong>Keywords:</strong> {result.ai_insights.keywords}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
