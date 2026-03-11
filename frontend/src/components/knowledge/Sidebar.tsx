import { useAuth } from "../../context/AuthContext";
import { useChat } from "../../context/ChatContext";

type SidebarProps = {
  open?: boolean;
  onClose?: () => void;
};

export function Sidebar({ open = true, onClose }: SidebarProps) {
  const { user, logout } = useAuth();
  const { messages, conversations, activeConversation, newChat, switchChat, deleteChat } = useChat();
  const initial = user?.name?.charAt(0)?.toUpperCase() ?? "U";

  return (
    <>
      {/* Overlay on small screens when sidebar is open */}
      {onClose && open && (
        <button
          type="button"
          aria-label="Close sidebar"
          onClick={onClose}
          className="fixed inset-0 z-20 bg-black/50 backdrop-blur-sm md:hidden"
        />
      )}
      <aside
        className={`
          fixed left-0 top-0 z-30 flex h-screen w-[260px] flex-col rounded-r-2xl rounded-b-2xl border-r border-b border-border bg-card/95 shadow-xl
          transition-transform duration-200 ease-out
          md:translate-x-0
          ${open ? "translate-x-0" : "-translate-x-full"}
        `}
      >
      <div className="flex min-h-0 flex-1 flex-col gap-4 p-4">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold text-amber-400">⚡</span>
            <span className="text-lg font-semibold text-text-primary">KnowledgeVolt</span>
          </div>
          {onClose && (
            <button
              type="button"
              aria-label="Close menu"
              onClick={onClose}
              className="rounded-lg p-1.5 text-text-muted hover:bg-background/50 hover:text-text-primary md:hidden"
            >
              <CloseIcon className="h-5 w-5" />
            </button>
          )}
        </div>

        <button
          type="button"
          onClick={() => { newChat(); onClose?.(); }}
          className="flex w-full items-center justify-center gap-2 rounded-xl border border-border bg-background/50 py-2.5 text-sm font-medium text-text-primary transition-colors hover:border-accent/50 hover:bg-accent/10"
        >
          <NewChatIcon className="h-4 w-4" />
          New chat
        </button>

        <div className="flex flex-col items-center gap-1 rounded-lg bg-background/50 px-3 py-2">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-card border border-border text-lg font-semibold text-text-primary">
            {initial}
          </div>
          <div className="min-w-0 text-center">
            <p className="truncate text-sm font-medium text-text-primary">{user?.name}</p>
            <p className="truncate text-xs text-text-muted">({user?.role})</p>
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <button
            type="button"
            onClick={logout}
            className="flex items-center justify-center gap-2 rounded-xl bg-rose-500/90 px-4 py-2.5 text-sm font-medium text-white shadow-[0_0_16px_rgba(244,63,94,0.4)] transition-all hover:bg-rose-500 hover:shadow-[0_0_20px_rgba(244,63,94,0.5)]"
          >
            <PowerIcon className="h-4 w-4 shrink-0" />
            Sign out
          </button>
          <button
            type="button"
            className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-text-muted transition-colors hover:bg-background/50 hover:text-text-primary"
          >
            <SettingsIcon className="h-4 w-4" />
            Settings
          </button>
        </div>

        <div className="flex min-h-0 flex-1 flex-col border-t border-border pt-3">
          <p className="mb-2 shrink-0 text-xs font-medium text-text-muted">Chat history</p>
          <div className="min-h-0 flex-1 space-y-0.5 overflow-y-auto">
            {conversations.length === 0 ? (
              <p className="text-xs text-text-muted">
                No chats yet. Start a new chat or send a message.
              </p>
            ) : (
              conversations.map((conv) => (
                <div
                  key={conv.id}
                  className="group flex items-center gap-2 rounded-lg px-2 py-1.5"
                >
                  <button
                    type="button"
                    onClick={() => { switchChat(conv.id); onClose?.(); }}
                    className={`min-w-0 flex-1 truncate rounded-lg px-2 py-1.5 text-left text-sm transition-colors ${
                      activeConversation?.id === conv.id
                        ? "bg-accent/20 text-accent"
                        : "text-text-primary hover:bg-background/50"
                    }`}
                    title={conv.title}
                  >
                    {conv.title}
                  </button>
                  <button
                    type="button"
                    onClick={() => deleteChat(conv.id)}
                    aria-label="Delete chat"
                    className="shrink-0 rounded p-1 text-text-muted opacity-0 transition-opacity hover:bg-red-500/20 hover:text-red-400 group-hover:opacity-100"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="shrink-0 border-t border-border pt-3">
          <p className="text-xs text-text-muted">{messages.length} messages in this chat</p>
        </div>
      </div>
    </aside>
    </>
  );
}

function CloseIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  );
}

function NewChatIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
    </svg>
  );
}

function TrashIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg>
  );
}

/** Standard power symbol: circle with line from top */
function PowerIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2v6M12 12m-5 0a5 5 0 1 0 10 0a5 5 0 1 0-10 0" />
    </svg>
  );
}

function SettingsIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
      />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}
