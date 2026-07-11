import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

export default function NotFoundPage() {
  return (
    <div className="flex-1 flex items-center justify-center bg-white dark:bg-gray-950 px-4 min-h-[60vh]">
      <div className="text-center max-w-md">
        <p className="text-sm font-sans font-medium text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-4">
          404
        </p>
        <h1 className="text-4xl md:text-5xl font-serif font-bold text-gray-900 dark:text-white mb-4">
          Page not found
        </h1>
        <p className="text-gray-600 dark:text-gray-400 font-sans mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 px-6 py-3 bg-black dark:bg-white text-white dark:text-black font-medium text-sm hover:opacity-80 transition-opacity"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Home
        </Link>
      </div>
    </div>
  );
}
