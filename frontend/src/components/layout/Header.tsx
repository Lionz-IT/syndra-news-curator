import { Link } from "react-router-dom";
import { Menu, Moon, Sun, X, Search, Globe, Languages, LogIn, UserCircle, LogOut } from "lucide-react";
import { useState, useEffect, useRef, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/contexts/AuthContext";
import { useClickOutside } from "@/hooks/use-click-outside";

function getInitialDarkMode(): boolean {
  const stored = localStorage.getItem("theme");
  if (stored === "dark") return true;
  if (stored === "light") return false;
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

export default function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [isDark, setIsDark] = useState(getInitialDarkMode);
  const { t, i18n } = useTranslation();
  const { user, openAuthModal, logout } = useAuth();

  const userMenuRef = useRef<HTMLDivElement>(null);
  const closeUserMenu = useCallback(() => setIsUserMenuOpen(false), []);
  useClickOutside(userMenuRef, closeUserMenu);

  // Apply dark mode class on mount and changes
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [isDark]);

  // Listen for OS-level preference changes
  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e: MediaQueryListEvent) => {
      if (!localStorage.getItem("theme")) {
        setIsDark(e.matches);
      }
    };
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  const toggleDarkMode = () => {
    setIsDark(prev => !prev);
  };

  const toggleLanguage = () => {
    const newLang = i18n.language.startsWith("en") ? "id" : "en";
    i18n.changeLanguage(newLang);
  };

  return (
    <header className="sticky top-0 z-50 w-full bg-white/95 dark:bg-gray-950/95 backdrop-blur-sm shadow-[0_1px_0_0_rgba(0,0,0,0.05)] dark:shadow-[0_1px_0_0_rgba(255,255,255,0.05)]">
      <div className="container mx-auto px-4 max-w-7xl h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="bg-black dark:bg-white text-white dark:text-black p-1 rounded">
              <Globe className="h-5 w-5" />
            </div>
            <span className="text-xl font-serif font-bold tracking-tight text-gray-900 dark:text-white group-hover:opacity-80 transition-opacity">
              Syndra
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
            <Link to="/feed" className="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
              {t("nav.latest_news")}
            </Link>
          </nav>
        </div>

        <div className="flex items-center gap-2 md:gap-4">
          <Link 
            to="/feed"
            className="hidden md:flex p-2 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Search"
          >
            <Search className="h-5 w-5" />
          </Link>
          <button
            onClick={toggleLanguage}
            className="hidden md:flex items-center gap-1.5 p-2 rounded-full text-sm font-medium text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors uppercase"
            aria-label="Toggle language"
          >
            <Languages className="h-4 w-4" />
            {i18n.language.substring(0, 2)}
          </button>
          <button 
            onClick={toggleDarkMode}
            className="p-2 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Toggle dark mode"
          >
            {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>

          <div className="relative" ref={userMenuRef}>
            {user ? (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                  className="flex items-center gap-2 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                >
                  <UserCircle className="h-5 w-5 text-gray-700 dark:text-gray-300" />
                </button>
                
                {isUserMenuOpen && (
                  <div className="absolute right-0 top-12 w-48 bg-white dark:bg-gray-950 border border-gray-200 dark:border-gray-800 shadow-xl py-2 flex flex-col z-50">
                    <div className="px-4 py-2 border-b border-gray-100 dark:border-gray-800 mb-2">
                      <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                        {user.full_name || user.email.split('@')[0]}
                      </p>
                      <p className="text-xs text-gray-500 truncate">{user.email}</p>
                    </div>
                    <button 
                      onClick={() => { logout(); setIsUserMenuOpen(false); }}
                      className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/10 flex items-center gap-2"
                    >
                      <LogOut className="h-4 w-4" />
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <button
                onClick={openAuthModal}
                className="hidden md:flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-black dark:text-black dark:bg-white rounded hover:opacity-80 transition-opacity"
              >
                <LogIn className="h-4 w-4" />
                Sign In
              </button>
            )}
          </div>
          
          <button 
            className="md:hidden p-2 rounded-md text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 w-full border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 px-4 py-4 space-y-4">
          <Link 
            to="/feed" 
            className="block text-base font-medium text-gray-900 dark:text-gray-100 hover:opacity-70"
            onClick={() => setIsMobileMenuOpen(false)}
          >
            {t("nav.latest_news")}
          </Link>
          <button
            onClick={() => {
              toggleLanguage();
              setIsMobileMenuOpen(false);
            }}
            className="flex items-center gap-2 text-base font-medium text-gray-900 dark:text-gray-100 hover:opacity-70 uppercase w-full text-left"
          >
            <Languages className="h-4 w-4" />
            Language: {i18n.language.substring(0, 2)}
          </button>
          {!user ? (
            <button
              onClick={() => {
                openAuthModal();
                setIsMobileMenuOpen(false);
              }}
              className="flex items-center gap-2 text-base font-medium text-blue-600 dark:text-blue-400 w-full text-left"
            >
              <LogIn className="h-4 w-4" />
              Sign In / Register
            </button>
          ) : (
            <button
              onClick={() => {
                logout();
                setIsMobileMenuOpen(false);
              }}
              className="flex items-center gap-2 text-base font-medium text-red-600 dark:text-red-400 w-full text-left"
            >
              <LogOut className="h-4 w-4" />
              Sign Out
            </button>
          )}
        </div>
      )}
    </header>
  );
}
