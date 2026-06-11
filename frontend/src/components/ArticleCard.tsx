import { Link } from "react-router-dom";
import { Clock } from "lucide-react";
import type { Article } from "@/lib/api";

interface ArticleCardProps {
  article: Article;
}

export default function ArticleCard({ article }: ArticleCardProps) {
  const publishedDate = article.published_at 
    ? new Date(article.published_at).toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric"
      })
    : "Recent";

  let biasColor = "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200";
  if (article.bias_score !== null) {
    if (article.bias_score < -0.3) biasColor = "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
    else if (article.bias_score > 0.3) biasColor = "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
    else biasColor = "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300";
  }

  return (
    <article className="flex flex-col h-full bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-md transition-shadow group">
      {article.image_url ? (
        <div className="relative aspect-video w-full overflow-hidden bg-gray-100 dark:bg-gray-800">
          <img 
            src={article.image_url} 
            alt={article.title} 
            className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
        </div>
      ) : (
        <div className="relative aspect-video w-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
          <span className="text-gray-400 dark:text-gray-500">No image</span>
        </div>
      )}

      <div className="flex flex-col flex-1 p-5">
        <div className="flex flex-wrap gap-2 mb-3">
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">
            {article.source}
          </span>
          {article.bias_label && (
            <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${biasColor}`}>
              {article.bias_label}
            </span>
          )}
        </div>

        <Link to={`/article/${article.id}`} className="block group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white leading-tight mb-2 line-clamp-2">
            {article.title}
          </h2>
        </Link>
        
        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 mb-4 flex-1">
          {article.summary || article.body || "No summary available."}
        </p>

        <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-100 dark:border-gray-800">
          <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
            <Clock className="mr-1.5 h-3.5 w-3.5" />
            {publishedDate}
          </div>
          
          <div className="flex gap-2">
            {article.categories.slice(0, 2).map(cat => (
              <Link 
                key={cat.id} 
                to={`/feed/${cat.slug}`}
                className="text-xs font-medium text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400"
                style={cat.color ? { color: cat.color } : {}}
              >
                {cat.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </article>
  );
}
