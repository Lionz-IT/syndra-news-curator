import { useQuery, keepPreviousData } from "@tanstack/react-query";
import {
  fetchArticles,
  fetchArticleById,
  type ArticleFilters,
} from "@/lib/api";

export function useArticles(filters: ArticleFilters = {}) {
  return useQuery({
    queryKey: ["articles", filters],
    queryFn: () => fetchArticles(filters),
    placeholderData: keepPreviousData,
    staleTime: 60_000,
  });
}

export function useArticle(id: string | undefined) {
  return useQuery({
    queryKey: ["article", id],
    queryFn: () => fetchArticleById(id!),
    enabled: !!id,
    staleTime: 120_000,
  });
}
