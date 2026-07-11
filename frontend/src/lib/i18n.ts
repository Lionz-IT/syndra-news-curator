import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

const resources = {
  en: {
    translation: {
      nav: {
        latest_news: "Latest News",
      },
      common: {
        search: "Search...",
        read_more: "Read More",
        loading: "Loading...",
        loading_editions: "Loading latest editions...",
        no_summary: "No summary available.",
        click_to_read: "Click to read more...",
        read_full_story: "Read full story...",
        load_more: "Load More Articles",
        no_articles: "No articles found for the given criteria.",
        failed_load: "Failed to load articles. Please try again later.",
        search_articles: "Search articles...",
        all_news: "All News",
        more_in: "More in {{section}}",
      },
      article: {
        back: "Back",
        ai_summary: "AI Summary",
        read_original: "Read Original",
        save_article: "Save Article",
        remove_bookmark: "Remove Bookmark",
        read_aloud: "Read Aloud",
        stop_reading: "Stop Reading",
        not_found: "Article not found or failed to load.",
        full_text_unavailable:
          "Full article text is not available in this public feed. Please click the \"Read Original\" button above to read the full story on the source website.",
        bias: "Bias",
        unknown_date: "Unknown date",
      },
      page: {
        not_found_code: "404",
        not_found_title: "Page not found",
        not_found_description:
          "The page you're looking for doesn't exist or has been moved.",
        back_home: "Back to Home",
      },
      error: {
        title: "Something went wrong",
        description:
          "An unexpected error occurred. Please try refreshing the page.",
        refresh: "Refresh Page",
      },
      pagination: {
        page_of: "Page {{current}} of {{total}}",
      },
    },
  },
  id: {
    translation: {
      nav: {
        latest_news: "Berita Terkini",
      },
      common: {
        search: "Cari...",
        read_more: "Baca Selengkapnya",
        loading: "Memuat...",
        loading_editions: "Memuat edisi terbaru...",
        no_summary: "Ringkasan tidak tersedia.",
        click_to_read: "Klik untuk membaca selengkapnya...",
        read_full_story: "Baca cerita lengkap...",
        load_more: "Muat Lebih Banyak Artikel",
        no_articles: "Tidak ada artikel yang ditemukan untuk kriteria tersebut.",
        failed_load: "Gagal memuat artikel. Silakan coba lagi nanti.",
        search_articles: "Cari artikel...",
        all_news: "Semua Berita",
        more_in: "Lainnya di {{section}}",
      },
      article: {
        back: "Kembali",
        ai_summary: "Ringkasan AI",
        read_original: "Baca Asli",
        save_article: "Simpan Artikel",
        remove_bookmark: "Hapus Bookmark",
        read_aloud: "Baca dengan Suara",
        stop_reading: "Berhenti Membaca",
        not_found: "Artikel tidak ditemukan atau gagal dimuat.",
        full_text_unavailable:
          "Teks artikel penuh tidak tersedia di feed publik ini. Silakan klik tombol \"Baca Asli\" di atas untuk membaca berita selengkapnya langsung di situs sumber.",
        bias: "Bias",
        unknown_date: "Tanggal tidak diketahui",
      },
      page: {
        not_found_code: "404",
        not_found_title: "Halaman tidak ditemukan",
        not_found_description:
          "Halaman yang Anda cari tidak ada atau telah dipindahkan.",
        back_home: "Kembali ke Beranda",
      },
      error: {
        title: "Terjadi kesalahan",
        description:
          "Terjadi kesalahan tak terduga. Silakan coba muat ulang halaman.",
        refresh: "Muat Ulang Halaman",
      },
      pagination: {
        page_of: "Halaman {{current}} dari {{total}}",
      },
    },
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: "en",
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
