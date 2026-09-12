import markdownIt from "markdown-it";
import markdownItAnchor from "markdown-it-anchor";

export default function (eleventyConfig) {
  const md = markdownIt({ html: true, linkify: true, typographer: false }).use(markdownItAnchor, {
    level: [2, 3],
    slugify: (s) =>
      s.toLowerCase().trim().replace(/[^a-z0-9\s-]/g, "").replace(/\s+/g, "-"),
  });
  eleventyConfig.setLibrary("md", md);

  eleventyConfig.addPassthroughCopy({ "src/css": "css" });
  eleventyConfig.addPassthroughCopy("src/*.txt"); // indexnow key
  eleventyConfig.addPassthroughCopy({ "src/img": "img" });

  eleventyConfig.addCollection("posts", (api) =>
    api.getFilteredByGlob("src/posts/*.md").sort((a, b) => b.date - a.date)
  );

  eleventyConfig.addFilter("longDate", (d) =>
    new Date(d).toLocaleDateString("en-GB", { year: "numeric", month: "long", day: "numeric" })
  );
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString());
  eleventyConfig.addFilter("rfcDate", (d) => new Date(d).toUTCString());
  eleventyConfig.addFilter("absUrl", (path, base) => new URL(path, base).href);
  eleventyConfig.addFilter("limit", (arr, n) => arr.slice(0, n));
  eleventyConfig.addFilter("wordCount", (content) =>
    (content || "").replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length
  );
  eleventyConfig.addFilter("readTime", (content) => {
    const words = (content || "").replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.round(words / 220));
  });
  eleventyConfig.addFilter("toc", (content) => {
    const out = [];
    const re = /<h2 id="([^"]+)"[^>]*>(.*?)<\/h2>/g;
    let m;
    while ((m = re.exec(content || ""))) out.push({ id: m[1], text: m[2].replace(/<[^>]+>/g, "") });
    return out;
  });
  eleventyConfig.addFilter("inCategory", (posts, slug) =>
    posts.filter((p) => p.data.category === slug)
  );
  eleventyConfig.addFilter("related", (posts, url, category, n = 3) => {
    const same = posts.filter((p) => p.url !== url && p.data.category === category);
    const rest = posts.filter((p) => p.url !== url && p.data.category !== category);
    return [...same, ...rest].slice(0, n);
  });
  eleventyConfig.addFilter("catName", (slug, categories) =>
    (categories.find((c) => c.slug === slug) || {}).name || slug
  );

  return {
    dir: { input: "src", output: "_site", includes: "_includes", data: "_data" },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
}
