import { Link } from "react-router-dom";
import { Menu, Moon, Sun, X, Search, Globe, Languages } from "lucide-react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

export default function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isDark, setIsDark] = useState(false);
  const { t, i18n } = useTranslation();

  // Quick implementation for dark mode toggle (can be enhanced later)
  useEffect(() => {
    if (document.documentElement.classList.contains("dark")) {
      setIsDark(true);
    }
  }, []);

  const toggleDarkMode = () => {
    document.documentElement.classList.toggle("dark");
    setIsDark(!isDark);
  };

  const toggleLanguage = () => {
    const newLang = i18n.language.startsWith("en") ? "id" : "en";
    i18n.changeLanguage(newLang);
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-950/80 backdrop-blur-md">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-2">
            <Globe className="h-6 w-6 text-blue-600 dark:text-blue-500" />
            <span className="text-xl font-bold tracking-tight text-gray-900 dark:text-white">
              Syndra
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
            <Link to="/feed" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              {t("nav.latest_news")}
            </Link>
          </nav>
        </div>

        <div className="flex items-center gap-2 md:gap-4">
          <button 
            className="p-2 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Search"
          >
            <Search className="h-5 w-5" />
          </button>
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
            className="block text-base font-medium text-gray-900 dark:text-gray-100 hover:text-blue-600 dark:hover:text-blue-400"
            onClick={() => setIsMobileMenuOpen(false)}
          >
            {t("nav.latest_news")}
          </Link>
          <button
            onClick={() => {
              toggleLanguage();
              setIsMobileMenuOpen(false);
            }}
            className="flex items-center gap-2 text-base font-medium text-gray-900 dark:text-gray-100 hover:text-blue-600 dark:hover:text-blue-400 uppercase w-full text-left"
          >
            <Languages className="h-4 w-4" />
            Language: {i18n.language.substring(0, 2)}
          </button>
        </div>
      )}
    </header>
  );
}
