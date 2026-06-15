import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import type { Article } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";

export function useBookmarks() {
  const { user } = useAuth();
  
  return useQuery<Article[]>({
    queryKey: ["bookmarks"],
    queryFn: async () => {
      const { data } = await api.get<Article[]>("/bookmarks");
      return data;
    },
    enabled: !!user,
  });
}

export function useBookmarkArticle() {
  const queryClient = useQueryClient();
  const { user, openAuthModal } = useAuth();

  return useMutation({
    mutationFn: async ({ articleId, isBookmarked }: { articleId: string; isBookmarked: boolean }) => {
      if (!user) {
        openAuthModal();
        throw new Error("Must be logged in to bookmark");
      }
      
      if (isBookmarked) {
        await api.delete(`/bookmarks/${articleId}`);
      } else {
        await api.post(`/bookmarks/${articleId}`);
      }
      return !isBookmarked;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["bookmarks"] });
    },
  });
}
