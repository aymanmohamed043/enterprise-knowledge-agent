import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Message } from "../context/ChatContext";
import styles from "./MessageBubble.module.css";

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.sender === "user";

  return (
    <div
      className={`${styles.bubble} ${isUser ? styles.user : styles.ai}`}
      data-sender={message.sender}
    >
      {message.role && !isUser && (
        <span className={styles.role}>{message.role}</span>
      )}
      <div className={styles.content}>
        {isUser ? (
          <p className={styles.text}>{message.content}</p>
        ) : (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            className={styles.markdown}
            components={{
              table: ({ children }) => (
                <div className={styles.tableWrap}>
                  <table className={styles.table}>{children}</table>
                </div>
              ),
              th: ({ children }) => <th className={styles.th}>{children}</th>,
              td: ({ children }) => <td className={styles.td}>{children}</td>,
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
}
