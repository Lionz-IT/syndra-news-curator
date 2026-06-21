import { Link } from "react-router-dom";
import { useCategories } from "@/hooks/use-categories";
import { cn } from "@/lib/utils";

interface CategoryNavProps {
  activeCategory?: string;
}

export default function CategoryNav({ activeCategory }: CategoryNavProps) {
  const { data: categoryData, isLoading } = useCategories();

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
    <div className="w-full bg-white dark:bg-gray-950 overflow-x-auto no-scrollbar shadow-[0_1px_0_0_rgba(0,0,0,0.04)] dark:shadow-[0_1px_0_0_rgba(255,255,255,0.04)]">
      <nav className="container mx-auto px-4 h-14 flex items-center gap-6 min-w-max">
        <Link
          to="/feed"
          className={cn(
            "text-sm font-medium transition-colors whitespace-nowrap",
            !activeCategory 
              ? "text-blue-600 dark:text-blue-500 border-b-2 border-blue-600 dark:border-blue-500 pb-4 pt-4" 
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 py-4"
          )}
        >
          All News
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
