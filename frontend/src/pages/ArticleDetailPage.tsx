import { useParams, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useArticle } from "@/hooks/use-articles";
import { ExternalLink, ArrowLeft, BookmarkPlus, BookmarkCheck, Play, Square } from "lucide-react";
import { useBookmarks, useBookmarkArticle } from "@/hooks/use-bookmarks";
import { sanitizeHtml, hasContent } from "@/lib/sanitize";
import { useState, useEffect } from "react";

export default function ArticleDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { t } = useTranslation();
  const { data: article, isLoading, isError } = useArticle(id);
  
  const { data: bookmarks } = useBookmarks();
  const { mutate: toggleBookmark } = useBookmarkArticle();
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [speechSynthesis] = useState(() => window.speechSynthesis);

  const isBookmarked = article ? (bookmarks?.some(b => b.id === article.id) || false) : false;

  useEffect(() => {
    return () => {
      speechSynthesis.cancel();
    };
  }, [speechSynthesis]);

  const toggleSpeech = () => {
    if (isPlaying) {
      speechSynthesis.cancel();
      setIsPlaying(false);
    } else if (article) {
      const textToRead = `${article.title}. ${article.ai_summary || article.body || article.summary}`;
      const utterance = new SpeechSynthesisUtterance(textToRead);
      utterance.lang = article.language === "en" ? "en-US" : "id-ID";
      utterance.onend = () => setIsPlaying(false);
      speechSynthesis.speak(utterance);
      setIsPlaying(true);
    }
  };

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
        {t("article.not_found")}
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
    : t("article.unknown_date");

  let biasColor = "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200";
  if (article.bias_score !== null) {
    if (article.bias_score < -0.3) biasColor = "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
    else if (article.bias_score > 0.3) biasColor = "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
    else biasColor = "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300";
  }

  return (
    <article className="container mx-auto px-4 py-12 max-w-2xl font-sans bg-white dark:bg-gray-950 min-h-screen">
      <Link to="/feed" className="inline-flex items-center text-sm font-medium text-gray-400 hover:text-gray-900 dark:text-gray-500 dark:hover:text-white mb-12 transition-colors">
        <ArrowLeft className="mr-2 h-4 w-4" />
        {t("article.back")}
      </Link>

      <header className="mb-10">
        <div className="flex flex-wrap items-center gap-3 mb-6 font-sans text-xs tracking-wider uppercase">
          <span className="font-semibold text-gray-900 dark:text-white">
            {article.source}
          </span>
          <span className="text-gray-300 dark:text-gray-700">&middot;</span>
          {article.bias_label && (
            <span className={`px-2 py-0.5 rounded-sm ${biasColor}`}>
              {t("article.bias")}: {article.bias_label} ({article.bias_score})
            </span>
          )}
        </div>

        <h1 className="text-4xl md:text-5xl lg:text-6xl font-serif font-bold text-gray-900 dark:text-white leading-[1.1] mb-8 tracking-tight">
          {article.title}
        </h1>

        <div className="flex items-center justify-between py-6 mb-2">
          <div className="flex flex-col gap-1 text-sm text-gray-500 dark:text-gray-400">
            {article.author && (
              <span className="font-medium text-gray-900 dark:text-white">{article.author}</span>
            )}
            <div className="flex items-center gap-2">
              <span>{publishedDate}</span>
              {article.region && (
                <>
                  <span className="text-gray-300 dark:text-gray-700">&middot;</span>
                  <span className="uppercase tracking-wider">{article.region}</span>
                </>
              )}
            </div>
          </div>
          
          <div className="flex gap-2">
            <button 
              onClick={toggleSpeech}
              className="inline-flex items-center p-2 rounded-full hover:bg-gray-50 dark:hover:bg-gray-900 text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              title={isPlaying ? t("article.stop_reading") : t("article.read_aloud")}
            >
              {isPlaying ? <Square className="h-5 w-5 fill-current" /> : <Play className="h-5 w-5 fill-current" />}
            </button>
            <button 
              onClick={() => toggleBookmark({ articleId: article.id, isBookmarked })}
              className="inline-flex items-center p-2 rounded-full hover:bg-gray-50 dark:hover:bg-gray-900 text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              title={isBookmarked ? t("article.remove_bookmark") : t("article.save_article")}
            >
              {isBookmarked ? <BookmarkCheck className="h-5 w-5 text-blue-600 dark:text-blue-400" /> : <BookmarkPlus className="h-5 w-5" />}
            </button>
            <a 
              href={article.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center p-2 rounded-full hover:bg-gray-50 dark:hover:bg-gray-900 text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              title={t("article.read_original")}
            >
              <ExternalLink className="h-5 w-5" />
            </a>
          </div>
        </div>
      </header>

      {article.image_url && (
        <figure className="mb-12">
          <img 
            src={article.image_url} 
            alt={article.title}
            className="w-full h-auto object-cover max-h-[500px]"
            onError={(e) => { (e.target as HTMLImageElement).parentElement!.style.display = "none"; }}
          />
        </figure>
      )}

      {article.ai_summary && (
        <div className="mb-12 p-6 bg-gray-50 dark:bg-gray-900/50 border-l-2 border-gray-300 dark:border-gray-700">
          <h2 className="text-xs font-bold uppercase tracking-widest text-gray-500 dark:text-gray-400 mb-3 flex items-center">
            {t("article.ai_summary")}
          </h2>
          <p className="font-serif text-lg text-gray-800 dark:text-gray-200 leading-relaxed">
            {article.ai_summary}
          </p>
        </div>
      )}

      <div className="prose prose-lg md:prose-xl dark:prose-invert max-w-none text-gray-800 dark:text-gray-200 font-serif leading-relaxed">
        {hasContent(article.body) ? (
          <div dangerouslySetInnerHTML={{ __html: sanitizeHtml(article.body) }} />
        ) : hasContent(article.summary) ? (
          <div dangerouslySetInnerHTML={{ __html: sanitizeHtml(article.summary) }} className="text-2xl font-light text-gray-600 dark:text-gray-400" />
        ) : (
          <p className="italic text-gray-400">
            {t("article.full_text_unavailable")}
          </p>
        )}
      </div>

      <footer className="mt-16 pt-8 pb-24">
        <div className="flex flex-wrap gap-2">
          {article.categories.map(cat => (
            <Link 
              key={cat.id} 
              to={`/feed/${cat.slug}`}
              className="px-4 py-2 rounded-full text-xs font-sans font-medium bg-gray-100 dark:bg-gray-900 hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors text-gray-600 dark:text-gray-300"
            >
              {cat.name}
            </Link>
          ))}
          {article.sdg_tags?.map(sdg => (
            <span 
              key={sdg}
              className="px-4 py-2 rounded-full text-xs font-sans font-medium bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400"
            >
              {sdg}
            </span>
          ))}
        </div>
      </footer>
    </article>
  );
}
