import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useCategories } from "@/hooks/use-categories";
import { cn } from "@/lib/utils";
import { useRef, useState, useEffect, useCallback } from "react";

interface CategoryNavProps {
  activeCategory?: string;
}

export default function CategoryNav({ activeCategory }: CategoryNavProps) {
  const { t } = useTranslation();
  const { data: categoryData, isLoading } = useCategories();
  const scrollRef = useRef<HTMLElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  const updateScrollState = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    setCanScrollLeft(el.scrollLeft > 2);
    setCanScrollRight(el.scrollLeft + el.clientWidth < el.scrollWidth - 2);
  }, []);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    updateScrollState();
    el.addEventListener("scroll", updateScrollState, { passive: true });
    window.addEventListener("resize", updateScrollState);
    return () => {
      el.removeEventListener("scroll", updateScrollState);
      window.removeEventListener("resize", updateScrollState);
    };
  }, [updateScrollState, categoryData]);

  if (isLoading) {
    return (
      <div className="w-full bg-white dark:bg-gray-950 overflow-hidden">
        <div className="container mx-auto px-4 h-12 flex items-center gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-4 w-24 bg-gray-100 dark:bg-gray-800 rounded animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  if (!categoryData || categoryData.items.length === 0) return null;

  return (
    <div className="relative w-full bg-white dark:bg-gray-950 shadow-[0_1px_0_0_rgba(0,0,0,0.04)] dark:shadow-[0_1px_0_0_rgba(255,255,255,0.04)]">
      {/* Left fade affordance */}
      <div
        className={cn(
          "pointer-events-none absolute left-0 top-0 bottom-0 w-8 z-10 bg-gradient-to-r from-white dark:from-gray-950 to-transparent transition-opacity duration-200",
          canScrollLeft ? "opacity-100" : "opacity-0",
        )}
      />
      {/* Right fade affordance */}
      <div
        className={cn(
          "pointer-events-none absolute right-0 top-0 bottom-0 w-8 z-10 bg-gradient-to-l from-white dark:from-gray-950 to-transparent transition-opacity duration-200",
          canScrollRight ? "opacity-100" : "opacity-0",
        )}
      />

      <nav
        ref={scrollRef}
        className="container mx-auto px-4 h-14 flex items-center gap-6 overflow-x-auto no-scrollbar min-w-0"
      >
        <Link
          to="/feed"
          className={cn(
            "text-sm font-medium transition-colors whitespace-nowrap",
            !activeCategory 
              ? "text-blue-600 dark:text-blue-500 border-b-2 border-blue-600 dark:border-blue-500 pb-4 pt-4" 
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 py-4"
          )}
        >
          {t("common.all_news")}
        </Link>
        {categoryData.items.map((cat) => (
          <Link
            key={cat.id}
            to={`/feed/${cat.slug}`}
            className={cn(
              "text-sm font-medium transition-colors whitespace-nowrap",
              activeCategory === cat.slug
                ? "text-blue-600 dark:text-blue-500 border-b-2 border-blue-600 dark:border-blue-500 pb-4 pt-4"
                : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 py-4"
            )}
            style={activeCategory === cat.slug ? { color: cat.color ?? undefined, borderColor: cat.color ?? undefined } : {}}
          >
            {cat.name}
          </Link>
        ))}
      </nav>
    </div>
  );
}
