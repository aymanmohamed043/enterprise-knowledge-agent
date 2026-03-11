import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { useAuth } from "./AuthContext";
import { apiChatSend } from "../api/client";

export type Message = {
  id: string;
  sender: "user" | "ai";
  content: string;
  role?: string;
};

export type Conversation = {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
};

const STORAGE_KEY_PREFIX = "knowledgevolt_chats_";
const MAX_CONVERSATIONS = 50;
const TITLE_MAX_LEN = 40;

type ChatContextValue = {
  conversations: Conversation[];
  activeConversation: Conversation | null;
  messages: Message[];
  sendMessage: (text: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  newChat: () => void;
  switchChat: (id: string) => void;
  deleteChat: (id: string) => void;
};

const ChatContext = createContext<ChatContextValue | null>(null);

let idCounter = 0;
function nextId() {
  return `msg-${++idCounter}-${Date.now()}`;
}

function nextChatId() {
  return `chat-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

function getStorageKey(userId: number | undefined): string | null {
  if (userId == null) return null;
  return `${STORAGE_KEY_PREFIX}${userId}`;
}

function loadFromStorage(key: string): Conversation[] {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as Conversation[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveToStorage(key: string, conversations: Conversation[]) {
  try {
    const toSave = conversations.slice(0, MAX_CONVERSATIONS);
    localStorage.setItem(key, JSON.stringify(toSave));
  } catch {
    // ignore
  }
}

export function ChatProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const storageKey = getStorageKey(user?.id);

  // Load from localStorage when user is available
  useEffect(() => {
    if (!storageKey) {
      setConversations([]);
      setActiveId(null);
      return;
    }
    const loaded = loadFromStorage(storageKey);
    setConversations(loaded);
    if (loaded.length > 0 && !activeId) {
      setActiveId(loaded[0].id);
    } else if (loaded.length === 0) {
      setActiveId(null);
    }
  }, [storageKey]);

  // Persist whenever conversations change (for current user)
  useEffect(() => {
    if (!storageKey || conversations.length === 0) return;
    saveToStorage(storageKey, conversations);
  }, [storageKey, conversations]);

  const activeConversation = activeId
    ? conversations.find((c) => c.id === activeId) ?? null
    : null;
  const messages = activeConversation?.messages ?? [];

  const newChat = useCallback(() => {
    const id = nextChatId();
    const newConv: Conversation = {
      id,
      title: "New chat",
      messages: [],
      createdAt: Date.now(),
    };
    setConversations((prev) => [newConv, ...prev]);
    setActiveId(id);
    setError(null);
  }, []);

  const switchChat = useCallback((id: string) => {
    setActiveId(id);
    setError(null);
  }, []);

  const deleteChat = useCallback((id: string) => {
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeId === id) {
      const rest = conversations.filter((c) => c.id !== id);
      setActiveId(rest[0]?.id ?? null);
    }
  }, [activeId, conversations]);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim()) return;

      const userMsg: Message = { id: nextId(), sender: "user", content: text.trim() };

      // If no active chat, create one
      let targetId = activeId;
      if (!targetId) {
        const id = nextChatId();
        const newConv: Conversation = {
          id,
          title: "New chat",
          messages: [],
          createdAt: Date.now(),
        };
        setConversations((prev) => [newConv, ...prev]);
        setActiveId(id);
        targetId = id;
      }

      setConversations((prev) =>
        prev.map((c) =>
          c.id === targetId ? { ...c, messages: [...c.messages, userMsg] } : c
        )
      );
      setIsLoading(true);
      setError(null);

      try {
        const { response, role } = await apiChatSend(text.trim());
        const aiMsg: Message = {
          id: nextId(),
          sender: "ai",
          content: response,
          role,
        };
        setConversations((prev) =>
          prev.map((c) => {
            if (c.id !== targetId) return c;
            const nextMessages = [...c.messages, aiMsg];
            // Set title from first user message when we're adding the first AI reply (c.messages already has 1 user msg)
            const firstUserMsg = c.messages[0];
            const isFirstReply = c.messages.length === 1 && firstUserMsg?.sender === "user";
            const title = isFirstReply
              ? (firstUserMsg.content.trim().slice(0, TITLE_MAX_LEN) || "New chat") + (firstUserMsg.content.trim().length > TITLE_MAX_LEN ? "…" : "")
              : c.title;
            return { ...c, messages: nextMessages, title };
          })
        );
      } catch (e) {
        setError(e instanceof Error ? e.message : "Something went wrong");
      } finally {
        setIsLoading(false);
      }
    },
    [activeId]
  );

  const value: ChatContextValue = {
    conversations,
    activeConversation,
    messages,
    sendMessage,
    isLoading,
    error,
    newChat,
    switchChat,
    deleteChat,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

export function useChat() {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error("useChat must be used within ChatProvider");
  return ctx;
}
