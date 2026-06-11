import { useQuery } from "@tanstack/react-query";
import {
  fetchCategories,
  fetchCategoryBySlug,
  type CategoryListResponse,
  type Category,
} from "@/lib/api";

export function useCategories() {
  return useQuery<CategoryListResponse>({
    queryKey: ["categories"],
    queryFn: fetchCategories,
    staleTime: 5 * 60_000, // categories rarely change
  });
}

export function useCategory(slug: string) {
  return useQuery<Category>({
    queryKey: ["categories", slug],
    queryFn: () => fetchCategoryBySlug(slug),
    enabled: !!slug,
    staleTime: 5 * 60_000,
  });
}
