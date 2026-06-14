import { Link } from "react-router-dom";
import type { Article } from "@/lib/api";

interface ArticleCardProps {
  article: Article;
}

export default function ArticleCard({ article }: ArticleCardProps) {
  const publishedDate = article.published_at 
    ? new Date(article.published_at).toLocaleDateString(undefined, {
        month: "short",
        day: "numeric"
      })
    : "";

  let biasColor = "text-gray-500 bg-gray-100 dark:bg-gray-800 dark:text-gray-400";
  if (article.bias_score !== null) {
    if (article.bias_score < -0.3) biasColor = "text-blue-700 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-400";
    else if (article.bias_score > 0.3) biasColor = "text-red-700 bg-red-50 dark:bg-red-900/30 dark:text-red-400";
    else biasColor = "text-purple-700 bg-purple-50 dark:bg-purple-900/30 dark:text-purple-400";
  }

  return (
    <article className="flex items-start gap-4 py-6 border-b border-gray-100 dark:border-gray-800 group">
      <div className="flex-1 min-w-0 flex flex-col justify-center">
        <div className="flex items-center gap-2 mb-2 text-xs font-sans">
          <span className="font-semibold text-gray-900 dark:text-white uppercase tracking-wide">
            {article.source}
          </span>
          <span className="text-gray-400 dark:text-gray-600">&middot;</span>
          {article.bias_label && (
            <span className={`px-1.5 py-0.5 rounded-sm font-medium ${biasColor}`}>
              {article.bias_label}
            </span>
          )}
        </div>

        <Link to={`/article/${article.id}`} className="block">
          <h2 className="text-xl md:text-2xl font-serif font-bold text-gray-900 dark:text-white leading-tight mb-2 group-hover:underline decoration-gray-400 dark:decoration-gray-600 underline-offset-4">
            {article.title}
          </h2>
          <div className="text-gray-600 dark:text-gray-400 font-serif leading-relaxed line-clamp-2 md:line-clamp-3 mb-3 hidden sm:block">
            {(article.summary && article.summary !== "null") 
              ? <div dangerouslySetInnerHTML={{ __html: article.summary }} /> 
              : (article.body && article.body !== "null")
              ? <div dangerouslySetInnerHTML={{ __html: article.body }} />
              : "Ringkasan tidak tersedia."}
          </div>
        </Link>

        <div className="flex items-center gap-3 mt-auto text-sm text-gray-500 dark:text-gray-400 font-sans">
          {publishedDate && <span>{publishedDate}</span>}
          {article.categories.slice(0, 1).map(cat => (
            <Link 
              key={cat.id} 
              to={`/feed/${cat.slug}`}
              className="hover:text-black dark:hover:text-white transition-colors"
            >
              <span className="bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded-full text-xs">
                {cat.name}
              </span>
            </Link>
          ))}
        </div>
      </div>

      {article.image_url && (
        <div className="shrink-0">
          <Link to={`/article/${article.id}`} className="block w-24 h-24 md:w-32 md:h-32 bg-gray-100 dark:bg-gray-800 overflow-hidden">
            <img 
              src={article.image_url} 
              alt="" 
              className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
            />
          </Link>
        </div>
      )}
    </article>
  );
}
