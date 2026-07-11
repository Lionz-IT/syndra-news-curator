import DOMPurify from "dompurify";

/**
 * Sanitize an HTML string, stripping dangerous tags/attributes while
 * preserving safe formatting (p, a, strong, em, ul, ol, li, br, h1-h6, img, blockquote).
 */
export function sanitizeHtml(dirty: string | null | undefined): string {
  if (!dirty || dirty === "null") return "";
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: [
      "p", "br", "strong", "b", "em", "i", "u", "a",
      "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6",
      "blockquote", "pre", "code", "img", "figure", "figcaption",
      "span", "div", "sub", "sup",
    ],
    ALLOWED_ATTR: [
      "href", "target", "rel", "src", "alt", "width", "height",
      "class", "id", "title",
    ],
    ADD_ATTR: ["target"],
    FORBID_TAGS: ["script", "style", "iframe", "object", "embed", "form", "input"],
    FORBID_ATTR: ["onerror", "onload", "onclick", "onmouseover"],
  });
}

/**
 * Check whether a nullable string has real content (not just "null" or empty).
 */
export function hasContent(value: string | null | undefined): value is string {
  return !!value && value !== "null" && value.trim().length > 0;
}
