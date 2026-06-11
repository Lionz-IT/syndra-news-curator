import { useHealth } from "@/hooks/use-health";
import { useCategories } from "@/hooks/use-categories";
import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";

export default function HomePage() {
  const { data: health, isLoading: healthLoading, isError: healthError, error } = useHealth();
  const { data: categoryData, isLoading: categoriesLoading } = useCategories();

  return (
    <div className="flex-1 w-full bg-gradient-to-br from-slate-50 to-blue-50 dark:from-gray-950 dark:to-gray-900">
      {/* Hero */}
      <header className="px-4 py-20 text-center">
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 mb-6">
          Universal News, <br className="hidden md:block"/> Unbiased.
        </h1>
        <p className="mt-4 text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-10">
          Syndra aggregates news across every domain and language, providing AI-powered bias detection, smart summaries, and multi-label categorization.
        </p>
        <Link 
          to="/feed" 
          className="inline-flex items-center justify-center px-8 py-4 text-lg font-bold text-white bg-blue-600 rounded-full hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-500/25"
        >
          Read Latest News
          <ArrowRight className="ml-2 h-5 w-5" />
        </Link>
      </header>

      <div className="max-w-6xl mx-auto px-4 space-y-12 pb-24">
        {/* Category Taxonomy Preview */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
              Explore Topics
            </h2>
            <Link to="/feed" className="text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400">
              View all &rarr;
            </Link>
          </div>

          {categoriesLoading && (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {Array.from({ length: 10 }).map((_, i) => (
                <div
                  key={i}
                  className="h-24 rounded-2xl bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-800 animate-pulse"
                />
              ))}
            </div>
          )}

          {categoryData && categoryData.items.length > 0 && (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {categoryData.items.map((cat) => (
                <Link
                  key={cat.id}
                  to={`/feed/${cat.slug}`}
                  className="group flex flex-col items-center justify-center rounded-2xl bg-white dark:bg-gray-900 shadow-sm hover:shadow-md border border-gray-100 dark:border-gray-800 p-6 transition-all hover:-translate-y-1"
                >
                  <span
                    className="text-lg font-bold mb-2 group-hover:scale-110 transition-transform"
                    style={{ color: cat.color ?? undefined }}
                  >
                    {cat.name}
                  </span>
                  {cat.children.length > 0 && (
                    <span className="text-xs text-gray-500 font-medium">
                      {cat.children.length} topics
                    </span>
                  )}
                </Link>
              ))}
            </div>
          )}

          {categoryData && categoryData.items.length === 0 && (
            <p className="text-sm text-gray-400 text-center py-12">
              No categories yet. Wait for the background worker to seed the database.
            </p>
          )}
        </section>

        {/* System Status */}
        <section className="max-w-2xl mx-auto rounded-2xl border border-gray-200 dark:border-gray-800 bg-white/50 dark:bg-gray-900/50 backdrop-blur shadow-sm p-6 space-y-4">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
              System Status
            </h2>
            {healthLoading && (
              <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />
            )}
          </div>

          {healthError && (
            <div className="rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4 text-sm text-red-700 dark:text-red-400">
              <p className="font-bold">Backend unreachable</p>
              <p className="mt-1 opacity-80">
                {error instanceof Error ? error.message : "Connection failed"}
              </p>
            </div>
          )}

          {health && (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500" />
                </span>
                <span className="text-green-700 dark:text-green-400 font-bold">
                  {health.status}
                </span>
              </div>
              <dl className="grid grid-cols-3 gap-3 text-sm">
                <div className="rounded-xl bg-white dark:bg-gray-800 p-3 shadow-sm border border-gray-100 dark:border-gray-700">
                  <dt className="text-xs text-gray-500 dark:text-gray-400 mb-1">App</dt>
                  <dd className="font-semibold">{health.app}</dd>
                </div>
                <div className="rounded-xl bg-white dark:bg-gray-800 p-3 shadow-sm border border-gray-100 dark:border-gray-700">
                  <dt className="text-xs text-gray-500 dark:text-gray-400 mb-1">Version</dt>
                  <dd className="font-semibold">{health.version}</dd>
                </div>
                <div className="rounded-xl bg-white dark:bg-gray-800 p-3 shadow-sm border border-gray-100 dark:border-gray-700">
                  <dt className="text-xs text-gray-500 dark:text-gray-400 mb-1">Environment</dt>
                  <dd className="font-semibold capitalize">{health.environment}</dd>
                </div>
              </dl>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
