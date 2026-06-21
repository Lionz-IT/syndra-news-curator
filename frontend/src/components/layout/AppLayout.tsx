import type { ReactNode } from "react";
import Header from "./Header";

interface AppLayoutProps {
  children: ReactNode;
}

export default function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col">
      <Header />
      <main className="flex-1 flex flex-col">
        {children}
      </main>
      <footer className="bg-white dark:bg-gray-950 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
        <div className="container mx-auto px-4">
          &copy; {new Date().getFullYear()} Syndra AI News Platform.
        </div>
      </footer>
    </div>
  );
}
