import { useState, type FormEvent } from "react";
import { useAuth } from "../context/AuthContext";
import styles from "./LoginForm.module.css";

export function LoginForm() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    if (!email.trim()) {
      setError("Enter your work email");
      return;
    }
    setSubmitting(true);
    try {
      await login(email.trim());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign in failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.bgImage} aria-hidden />
      <div className={styles.bgOverlay} aria-hidden />

      <div className={styles.card}>
        <h1 className={styles.title}>Sign In</h1>
        <p className={styles.welcome}>Welcome to KnowledgeVolt</p>

        <form onSubmit={handleSubmit} className={styles.form}>
          <label className={styles.label}>Work Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="johndoe@enterprise.com"
            className={styles.input}
            autoComplete="email"
            disabled={submitting}
          />

          {error && <p className={styles.error}>{error}</p>}

          <button type="submit" className={styles.button} disabled={submitting}>
            {submitting ? "Signing in…" : "Sign In"}
            <span className={styles.buttonIcon} aria-hidden>⚡</span>
          </button>
        </form>

        <div className={styles.links}>
          <a href="#" className={styles.link}>Forgot Password?</a>
          <span className={styles.sep}>|</span>
          <a href="#" className={styles.link}>Request Access</a>
        </div>

        <p className={styles.ssoLabel}>Sign in with SSO</p>
        <div className={styles.ssoIcons}>
          <button type="button" className={styles.ssoBtn} aria-label="SSO provider" disabled title="Coming soon">
            <span className={styles.ssoIconA} />
          </button>
          <button type="button" className={styles.ssoBtn} aria-label="SSO provider" disabled title="Coming soon">
            <span className={styles.ssoIconB} />
          </button>
          <button type="button" className={styles.ssoBtn} aria-label="Sign in with Google" disabled title="Coming soon">
            <span className={styles.ssoGoogle}>G</span>
          </button>
        </div>
      </div>
    </div>
  );
}
