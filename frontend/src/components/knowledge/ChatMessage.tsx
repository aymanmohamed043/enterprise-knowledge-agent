import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Message } from "../../context/ChatContext";

export function ChatMessage({ message }: { message: Message }) {
  const isUser = message.sender === "user";

  return (
    <div
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}
    >
      <div className="flex shrink-0">
        {isUser ? (
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-accent/30 text-sm font-semibold text-accent">
            {message.content.charAt(0)?.toUpperCase() ?? "U"}
          </div>
        ) : (
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-amber-500/20 text-lg">
            ⚡
          </div>
        )}
      </div>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-accent/20 text-text-primary"
            : "bg-card border border-border text-text-primary"
        }`}
      >
        {message.role && !isUser && (
          <p className="mb-1 text-xs uppercase tracking-wide text-text-muted">{message.role}</p>
        )}
        {isUser ? (
          <p className="whitespace-pre-wrap text-sm">{message.content}</p>
        ) : (
          <div className="markdown-preview text-sm text-text-primary [&_p]:mb-2 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_code]:rounded [&_code]:bg-background/60 [&_code]:px-1 [&_pre]:overflow-x-auto [&_pre]:rounded-lg [&_pre]:bg-background/60 [&_pre]:p-3">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                table: ({ children }) => (
                  <div className="my-2 overflow-x-auto rounded-lg border border-border">
                    <table className="min-w-full divide-y divide-border text-sm">{children}</table>
                  </div>
                ),
                th: ({ children }) => (
                  <th className="bg-background/50 px-3 py-2 text-left font-medium text-text-primary">
                    {children}
                  </th>
                ),
                td: ({ children }) => (
                  <td className="px-3 py-2 text-text-muted">{children}</td>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
