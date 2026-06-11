import { useParams, Link } from "react-router-dom";
import { useArticle } from "@/hooks/use-articles";
import { Clock, ExternalLink, ArrowLeft } from "lucide-react";

export default function ArticleDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: article, isLoading, isError } = useArticle(id);

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="h-8 w-64 bg-gray-200 dark:bg-gray-800 rounded animate-pulse mb-8" />
        <div className="h-10 w-full bg-gray-200 dark:bg-gray-800 rounded animate-pulse mb-6" />
        <div className="h-[400px] w-full bg-gray-200 dark:bg-gray-800 rounded-xl animate-pulse mb-8" />
        <div className="space-y-4">
          <div className="h-4 w-full bg-gray-200 dark:bg-gray-800 rounded animate-pulse" />
          <div className="h-4 w-full bg-gray-200 dark:bg-gray-800 rounded animate-pulse" />
          <div className="h-4 w-3/4 bg-gray-200 dark:bg-gray-800 rounded animate-pulse" />
        </div>
      </div>
    );
  }

  if (isError || !article) {
    return (
      <div className="container mx-auto px-4 py-12 text-center text-red-500">
        Article not found or failed to load.
      </div>
    );
  }

  const publishedDate = article.published_at 
    ? new Date(article.published_at).toLocaleDateString(undefined, {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      })
    : "Unknown date";

  let biasColor = "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200";
  if (article.bias_score !== null) {
    if (article.bias_score < -0.3) biasColor = "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
    else if (article.bias_score > 0.3) biasColor = "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
    else biasColor = "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300";
  }

  return (
    <article className="container mx-auto px-4 py-8 max-w-4xl">
      <Link to="/feed" className="inline-flex items-center text-sm font-medium text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 mb-8 transition-colors">
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back to News Feed
      </Link>

      <header className="mb-8">
        <div className="flex flex-wrap gap-2 mb-4">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">
            {article.source}
          </span>
          {article.bias_label && (
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${biasColor}`}>
              Bias: {article.bias_label} ({article.bias_score})
            </span>
          )}
        </div>

        <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white leading-tight mb-6">
          {article.title}
        </h1>

        <div className="flex flex-wrap items-center justify-between gap-4 border-y border-gray-200 dark:border-gray-800 py-4">
          <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4 text-sm text-gray-600 dark:text-gray-400">
            {article.author && (
              <span className="font-medium text-gray-900 dark:text-gray-200">By {article.author}</span>
            )}
            <div className="flex items-center">
              <Clock className="mr-1.5 h-4 w-4" />
              {publishedDate}
            </div>
            {article.region && (
              <span className="uppercase text-xs font-bold tracking-wider">{article.region}</span>
            )}
          </div>
          
          <a 
            href={article.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium transition-colors"
          >
            Read Original <ExternalLink className="ml-2 h-4 w-4" />
          </a>
        </div>
      </header>

      {article.image_url && (
        <figure className="mb-10 rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-800">
          <img 
            src={article.image_url} 
            alt={article.title} 
            className="w-full h-auto object-cover max-h-[600px]"
          />
        </figure>
      )}

      {article.ai_summary && (
        <div className="mb-10 p-6 rounded-xl bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-100 dark:border-blue-900/30">
          <h2 className="text-sm font-bold uppercase tracking-wider text-blue-800 dark:text-blue-300 mb-3 flex items-center">
            <span className="bg-blue-600 text-white rounded px-1.5 py-0.5 mr-2 text-[10px]">AI</span>
            Executive Summary
          </h2>
          <p className="text-gray-800 dark:text-gray-200 leading-relaxed">
            {article.ai_summary}
          </p>
        </div>
      )}

      <div className="prose prose-lg dark:prose-invert max-w-none text-gray-800 dark:text-gray-200">
        {article.body ? (
          <p className="whitespace-pre-wrap leading-relaxed">{article.body}</p>
        ) : article.summary ? (
          <p className="whitespace-pre-wrap leading-relaxed text-xl text-gray-600 dark:text-gray-400">
            {article.summary}
          </p>
        ) : (
          <p className="italic text-gray-500">Full article content not available in the feed. Please read the original source.</p>
        )}
      </div>

      <footer className="mt-12 pt-8 border-t border-gray-200 dark:border-gray-800">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-4">
          Tags & Categories
        </h3>
        <div className="flex flex-wrap gap-2">
          {article.categories.map(cat => (
            <Link 
              key={cat.id} 
              to={`/feed/${cat.slug}`}
              className="px-3 py-1.5 rounded-full text-sm font-medium border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-gray-700 dark:text-gray-300"
            >
              {cat.name}
            </Link>
          ))}
          {article.sdg_tags?.map(sdg => (
            <span 
              key={sdg}
              className="px-3 py-1.5 rounded-full text-sm font-medium bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-400"
            >
              {sdg}
            </span>
          ))}
        </div>
      </footer>
    </article>
  );
}
