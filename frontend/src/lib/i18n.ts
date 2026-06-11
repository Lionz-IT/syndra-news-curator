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
