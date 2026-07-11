import { useState, useEffect, useRef, useCallback } from "react";
import { X } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import api from "@/lib/api";

export default function AuthModal() {
  const { isAuthModalOpen, closeAuthModal, login } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const modalRef = useRef<HTMLDivElement>(null);
  const previouslyFocused = useRef<HTMLElement | null>(null);

  // Store previously focused element and auto-focus the modal on open
  useEffect(() => {
    if (isAuthModalOpen) {
      previouslyFocused.current = document.activeElement as HTMLElement;
      // Focus the first input after a frame so the DOM is ready
      requestAnimationFrame(() => {
        const firstInput = modalRef.current?.querySelector<HTMLInputElement>(
          "input:not([type=hidden])"
        );
        firstInput?.focus();
      });
    } else {
      // Restore focus when modal closes
      previouslyFocused.current?.focus();
    }
  }, [isAuthModalOpen]);

  // Close on Escape key
  useEffect(() => {
    if (!isAuthModalOpen) return;
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") closeAuthModal();
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [isAuthModalOpen, closeAuthModal]);

  // Focus trap — keep Tab cycling inside the modal
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key !== "Tab" || !modalRef.current) return;

      const focusable = modalRef.current.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (focusable.length === 0) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    },
    [],
  );

  if (!isAuthModalOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);
        
        const { data } = await api.post("/auth/login", formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        });
        await login(data.access_token);
      } else {
        await api.post("/auth/register", {
          email,
          password,
          full_name: fullName
        });
        
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);
        const { data } = await api.post("/auth/login", formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        });
        await login(data.access_token);
      }
      closeAuthModal();
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: { detail?: string } } };
      setError(axiosErr.response?.data?.detail || "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackdropClick = (e: React.MouseEvent) => {
    // Only close when clicking the backdrop itself, not the modal content
    if (e.target === e.currentTarget) closeAuthModal();
  };

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="auth-modal-title"
    >
      <div
        ref={modalRef}
        onKeyDown={handleKeyDown}
        className="relative w-full max-w-md bg-white dark:bg-gray-950 p-8 shadow-2xl font-sans border border-gray-200 dark:border-gray-800"
      >
        <button 
          onClick={closeAuthModal}
          className="absolute top-4 right-4 p-2 text-gray-400 hover:text-black dark:hover:text-white transition-colors"
          aria-label="Close"
        >
          <X className="h-5 w-5" />
        </button>
        
        <h2 id="auth-modal-title" className="text-3xl font-serif font-bold text-gray-900 dark:text-white mb-2 text-center">
          {isLogin ? "Welcome back." : "Join Syndra."}
        </h2>
        
        <div className="flex justify-center gap-6 mb-8 text-sm font-medium border-b border-gray-100 dark:border-gray-800 pb-2">
          <button 
            className={`pb-2 ${isLogin ? "text-black dark:text-white border-b-2 border-black dark:border-white" : "text-gray-400 hover:text-gray-900"}`}
            onClick={() => { setIsLogin(true); setError(""); }}
          >
            Sign In
          </button>
          <button 
            className={`pb-2 ${!isLogin ? "text-black dark:text-white border-b-2 border-black dark:border-white" : "text-gray-400 hover:text-gray-900"}`}
            onClick={() => { setIsLogin(false); setError(""); }}
          >
            Create Account
          </button>
        </div>

        {error && (
          <div className="mb-6 p-3 text-sm text-red-600 bg-red-50 border border-red-100 text-center" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {!isLogin && (
            <div>
              <label htmlFor="auth-fullname" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Full Name</label>
              <input 
                id="auth-fullname"
                type="text" 
                required 
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 text-gray-900 dark:text-white focus:outline-none focus:border-black dark:focus:border-white transition-colors"
              />
            </div>
          )}
          <div>
            <label htmlFor="auth-email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email Address</label>
            <input 
              id="auth-email"
              type="email" 
              required 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 text-gray-900 dark:text-white focus:outline-none focus:border-black dark:focus:border-white transition-colors"
            />
          </div>
          <div>
            <label htmlFor="auth-password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
            <input 
              id="auth-password"
              type="password" 
              required 
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 text-gray-900 dark:text-white focus:outline-none focus:border-black dark:focus:border-white transition-colors"
            />
          </div>
          
          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full bg-black text-white dark:bg-white dark:text-black py-3 px-4 font-medium hover:opacity-80 transition-opacity disabled:opacity-50 mt-4"
          >
            {isLoading ? "Please wait..." : isLogin ? "Sign In" : "Create Account"}
          </button>
        </form>
      </div>
    </div>
  );
}
