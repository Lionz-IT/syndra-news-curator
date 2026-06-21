import { useArticles } from "@/hooks/use-articles";
import { Link } from "react-router-dom";
import ArticleCard from "@/components/ArticleCard";

export default function HomePage() {
  const { data: latestNews, isLoading } = useArticles({ page_size: 10 });
  const { data: techNews } = useArticles({ category: "technology", page_size: 30 });
  const { data: worldNews } = useArticles({ category: "world", page_size: 30 });
  const { data: businessNews } = useArticles({ category: "business", page_size: 30 });

  if (isLoading) {
    return (
      <div className="flex-1 w-full bg-white dark:bg-gray-950 min-h-screen flex items-center justify-center">
        <div className="animate-pulse flex flex-col items-center gap-4">
          <div className="h-8 w-64 bg-gray-200 dark:bg-gray-800 rounded"></div>
          <div className="text-gray-400 font-serif">Loading latest editions...</div>
        </div>
      </div>
    );
  }

  const heroArticle = latestNews?.items.find(a => a.image_url) || latestNews?.items[0];
  const listArticles = latestNews?.items.filter(a => a.id !== heroArticle?.id);

  // Helper untuk mengutamakan artikel bergambar di barisan depan
  const getBestArticles = (items: any[]) => {
    if (!items) return [];
    const withImages = items.filter(a => a.image_url);
    const withoutImages = items.filter(a => !a.image_url);
    return [...withImages, ...withoutImages].slice(0, 4);
  };

  return (
    <div className="flex-1 w-full bg-white dark:bg-gray-950 font-sans pb-24">
      <div className="container mx-auto px-4 mt-8 mb-12">
        <h1 className="text-4xl md:text-6xl font-serif font-bold text-center tracking-tight text-gray-900 dark:text-white">
          Today's Front Page
        </h1>
      </div>

      <div className="container mx-auto px-4 max-w-7xl">
        {heroArticle && (
          <section className="mb-20 pb-12">
            <Link to={`/article/${heroArticle.id}`} className="group block">
              <div className="flex flex-col md:flex-col gap-6 items-center text-center max-w-4xl mx-auto">
                <h2 className="text-4xl md:text-5xl font-serif font-bold text-gray-900 dark:text-white leading-tight group-hover:underline decoration-gray-400">
                  {heroArticle.title}
                </h2>
                
                {heroArticle.image_url && (
                  <div className="w-full aspect-[21/9] bg-gray-100 dark:bg-gray-900 overflow-hidden">
                    <img 
                      src={heroArticle.image_url} 
                      alt="" 
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" 
                    />
                  </div>
                )}
                
                <div className="text-lg md:text-xl text-gray-600 dark:text-gray-400 font-serif max-w-3xl line-clamp-3">
                  {(heroArticle.summary && heroArticle.summary !== "null") 
                    ? <div dangerouslySetInnerHTML={{ __html: heroArticle.summary }} /> 
                    : (heroArticle.body && heroArticle.body !== "null")
                    ? <div dangerouslySetInnerHTML={{ __html: heroArticle.body }} />
                    : "Klik untuk membaca selengkapnya..."}
                </div>
                <div className="text-xs font-sans text-gray-500 uppercase tracking-widest mt-2">
                  {heroArticle.author ? `BY ${heroArticle.author} · ` : ""}
                  {heroArticle.source}
                </div>
              </div>
            </Link>
          </section>
        )}

        {worldNews && worldNews.items.length > 0 && (
          <SectionRow title="World News" articles={getBestArticles(worldNews.items)} categorySlug="world" />
        )}

        {techNews && techNews.items.length > 0 && (
          <SectionRow title="Technology" articles={getBestArticles(techNews.items)} categorySlug="technology" />
        )}

        {businessNews && businessNews.items.length > 0 && (
          <SectionRow title="Business & Finance" articles={getBestArticles(businessNews.items)} categorySlug="business" />
        )}

        <section className="mt-20 max-w-4xl">
          <div className="mb-8">
            <h3 className="text-sm font-bold uppercase tracking-widest text-gray-900 dark:text-white">
              Latest Updates
            </h3>
          </div>
          
          <div className="flex flex-col">
            {listArticles?.map((article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>

          <div className="mt-8 text-center">
            <Link 
              to="/feed" 
              className="inline-block px-6 py-2 border border-gray-300 dark:border-gray-700 text-sm font-semibold rounded hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors"
            >
              Load More Articles
            </Link>
          </div>
        </section>

      </div>
    </div>
  );
}

function SectionRow({ title, articles, categorySlug }: { title: string, articles: any[], categorySlug: string }) {
  return (
    <section className="mb-16">
      <div className="flex items-center justify-between pt-2 mb-6">
        <h3 className="text-xl font-serif font-bold text-gray-900 dark:text-white">
          {title}
        </h3>
        <Link to={`/feed/${categorySlug}`} className="text-xs font-sans font-medium text-gray-500 hover:text-black dark:hover:text-white transition-colors">
          More in {title} &rarr;
        </Link>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {articles.map((article) => (
          <Link key={article.id} to={`/article/${article.id}`} className="group flex flex-col gap-3">
            {article.image_url ? (
              <div className="aspect-[3/2] w-full bg-gray-100 dark:bg-gray-800 overflow-hidden mb-1">
                <img 
                  src={article.image_url} 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                  alt="" 
                />
              </div>
            ) : (
              <div className="w-full h-1 bg-black dark:bg-white mb-2"></div>
            )}
            <div>
              <h4 className="font-serif font-bold text-gray-900 dark:text-gray-100 leading-snug group-hover:underline decoration-gray-400">
                {article.title}
              </h4>
              <div className="text-sm text-gray-500 dark:text-gray-400 font-serif mt-2 line-clamp-3">
                {(article.summary && article.summary !== "null") 
                  ? <div dangerouslySetInnerHTML={{ __html: article.summary }} /> 
                  : (article.body && article.body !== "null")
                  ? <div dangerouslySetInnerHTML={{ __html: article.body }} />
                  : "Read full story..."}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
