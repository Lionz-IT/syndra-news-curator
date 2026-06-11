import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  timeout: 10_000,
  headers: { "Content-Type": "application/json" },
});

// ── Health ───────────────────────────────────────────────
export interface HealthResponse {
  status: string;
  app: string;
  version: string;
  environment: string;
}

export async function fetchHealth(): Promise<HealthResponse> {
  const { data } = await api.get<HealthResponse>("/health");
  return data;
}

// ── Categories ───────────────────────────────────────────
export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  icon: string | null;
  color: string | null;
  display_order: number;
  parent_id: string | null;
  created_at: string;
  children: Category[];
}

export interface CategoryListResponse {
  items: Category[];
  total: number;
}

export async function fetchCategories(): Promise<CategoryListResponse> {
  const { data } = await api.get<CategoryListResponse>("/categories");
  return data;
}

export async function fetchCategoryBySlug(slug: string): Promise<Category> {
  const { data } = await api.get<Category>(`/categories/${slug}`);
  return data;
}

// ── Articles ─────────────────────────────────────────────
export interface ArticleCategory {
  id: string;
  name: string;
  slug: string;
  icon: string | null;
  color: string | null;
}

export interface Article {
  id: string;
  title: string;
  url: string;
  source: string;
  language: string;
  body: string | null;
  summary: string | null;
  image_url: string | null;
  author: string | null;
  region: string | null;
  raw_tags: string[] | null;
  published_at: string | null;
  created_at: string;
  updated_at: string;
  categories: ArticleCategory[];
  bias_score: number | null;
  bias_label: string | null;
  sdg_tags: string[] | null;
  ai_summary: string | null;
}

export interface ArticleListResponse {
  items: Article[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ArticleFilters {
  source?: string;
  category?: string;
  categories?: string[];
  language?: string;
  region?: string;
  search?: string;
  date_from?: string;
  date_to?: string;
  bias_score_min?: number;
  bias_score_max?: number;
  page?: number;
  page_size?: number;
}

export async function fetchArticles(
  filters: ArticleFilters = {},
): Promise<ArticleListResponse> {
  const params: Record<string, string> = {};
  if (filters.source) params.source = filters.source;
  if (filters.category) params.category = filters.category;
  if (filters.categories?.length)
    params.categories = filters.categories.join(",");
  if (filters.language) params.language = filters.language;
  if (filters.region) params.region = filters.region;
  if (filters.search) params.search = filters.search;
  if (filters.date_from) params.date_from = filters.date_from;
  if (filters.date_to) params.date_to = filters.date_to;
  if (filters.bias_score_min != null)
    params.bias_score_min = String(filters.bias_score_min);
  if (filters.bias_score_max != null)
    params.bias_score_max = String(filters.bias_score_max);
  if (filters.page != null) params.page = String(filters.page);
  if (filters.page_size != null) params.page_size = String(filters.page_size);

  const { data } = await api.get<ArticleListResponse>("/news", { params });
  return data;
}

export async function fetchArticleById(id: string): Promise<Article> {
  const { data } = await api.get<Article>(`/news/${id}`);
  return data;
}

export default api;
