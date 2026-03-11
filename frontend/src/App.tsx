import { AuthProvider, useAuth } from "./context/AuthContext";
import { ChatProvider } from "./context/ChatContext";
import { LoginForm } from "./components/LoginForm";
import { KnowledgeLayout } from "./components/knowledge/KnowledgeLayout";

function AppContent() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-text-muted">
        <span>Loading…</span>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginForm />;
  }

  return <KnowledgeLayout />;
}

export default function App() {
  return (
    <AuthProvider>
      <ChatProvider>
        <AppContent />
      </ChatProvider>
    </AuthProvider>
  );
}
