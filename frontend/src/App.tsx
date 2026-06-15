import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppLayout from "@/components/layout/AppLayout";
import HomePage from "@/pages/HomePage";
import NewsFeedPage from "@/pages/NewsFeedPage";
import ArticleDetailPage from "@/pages/ArticleDetailPage";
import { AuthProvider } from "@/contexts/AuthContext";
import AuthModal from "@/components/AuthModal";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <AppLayout>
            <AuthModal />
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/feed" element={<NewsFeedPage />} />
              <Route path="/feed/:category" element={<NewsFeedPage />} />
              <Route path="/article/:id" element={<ArticleDetailPage />} />
            </Routes>
          </AppLayout>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}
