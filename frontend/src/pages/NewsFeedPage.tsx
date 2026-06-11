import { useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { useArticles } from "@/hooks/use-articles";
import { Search } from "lucide-react";
import CategoryNav from "@/components/CategoryNav";
import ArticleCard from "@/components/ArticleCard";
import Pagination from "@/components/Pagination";

export default function NewsFeedPage() {
  const { category } = useParams<{ category: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  
  const page = parseInt(searchParams.get("page") || "1", 10);
  const searchInput = searchParams.get("q") || "";
  const [searchTerm, setSearchTerm] = useState(searchInput);

  const { data, isLoading, isError } = useArticles({
    category,
    search: searchInput,
    page,
    page_size: 12
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const newParams = new URLSearchParams(searchParams);
    if (searchTerm) {
      newParams.set("q", searchTerm);
    } else {
      newParams.delete("q");
    }
    newParams.set("page", "1");
    setSearchParams(newParams);
  };

  const handlePageChange = (newPage: number) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set("page", newPage.toString());
    setSearchParams(newParams);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="flex flex-col min-h-screen">
      <CategoryNav activeCategory={category} />
      
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white capitalize">
            {category ? `${category.replace("-", " ")} News` : "Latest News"}
          </h1>
          
          <form onSubmit={handleSearch} className="relative w-full md:w-96">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="search"
              placeholder="Search articles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-shadow"
            />
          </form>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="h-96 rounded-xl bg-gray-100 dark:bg-gray-800 animate-pulse border border-gray-200 dark:border-gray-800" />
            ))}
          </div>
        ) : isError ? (
          <div className="text-center py-12 text-red-500 bg-red-50 dark:bg-red-900/10 rounded-xl border border-red-200 dark:border-red-900/30">
            Failed to load articles. Please try again later.
          </div>
        ) : data?.items.length === 0 ? (
          <div className="text-center py-12 text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-800">
            No articles found for the given criteria.
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {data?.items.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
            
            {data && (
              <Pagination 
                currentPage={data.page} 
                totalPages={data.total_pages} 
                onPageChange={handlePageChange} 
              />
            )}
          </>
        )}
      </div>
    </div>
  );
}
