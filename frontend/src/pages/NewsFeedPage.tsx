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
    <div className="flex flex-col min-h-screen bg-white dark:bg-gray-950 font-sans">
      <CategoryNav activeCategory={category} />
      
      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <div className="flex flex-col mb-10 gap-6 border-b border-gray-100 dark:border-gray-900 pb-8">
          <h1 className="text-4xl md:text-5xl font-serif font-bold text-gray-900 dark:text-white capitalize tracking-tight">
            {category ? `${category.replace("-", " ")}` : "Latest News"}
          </h1>
          
          <form onSubmit={handleSearch} className="relative w-full">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="search"
              placeholder="Search articles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-3 rounded-full border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-1 focus:ring-gray-300 dark:focus:ring-gray-700 outline-none transition-shadow"
            />
          </form>
        </div>

        {isLoading ? (
          <div className="flex flex-col gap-8">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-40 rounded bg-gray-50 dark:bg-gray-900 animate-pulse border-b border-gray-100 dark:border-gray-800 pb-8" />
            ))}
          </div>
        ) : isError ? (
          <div className="text-center py-12 text-red-500 font-medium">
            Failed to load articles. Please try again later.
          </div>
        ) : data?.items.length === 0 ? (
          <div className="text-center py-12 text-gray-500 dark:text-gray-400 font-serif text-lg">
            No articles found for the given criteria.
          </div>
        ) : (
          <>
            <div className="flex flex-col">
              {data?.items.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
            
            {data && (
              <div className="mt-12 mb-16">
                <Pagination 
                  currentPage={data.page} 
                  totalPages={data.total_pages} 
                  onPageChange={handlePageChange} 
                />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
