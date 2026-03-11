import { useAuth } from "../context/AuthContext";
import { useChat } from "../context/ChatContext";
import styles from "./ChatSidebar.module.css";

export function ChatSidebar() {
  const { user, logout } = useAuth();
  const { messages, newChat } = useChat();

  return (
    <aside className={styles.sidebar}>
      <div className={styles.header}>
        <h2 className={styles.title}>Chat</h2>
        <span className={styles.role}>{user?.role}</span>
      </div>
      <div className={styles.userRow}>
        <span className={styles.userName}>{user?.name}</span>
        <button type="button" onClick={logout} className={styles.logout}>
          Sign out
        </button>
      </div>
      <div className={styles.sessionInfo}>
        <span>{messages.length} messages in this session</span>
        {messages.length > 0 && (
          <button type="button" onClick={newChat} className={styles.clear}>
            New chat
          </button>
        )}
      </div>
      <div className={styles.historyHint}>
        Recent messages are loaded from the server when you send a new message.
      </div>
    </aside>
  );
}
