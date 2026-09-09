export default {
  layout: "post.njk",
  type: "article",
  eleventyComputed: {
    tags: (data) => ["post", data.category].filter(Boolean),
    permalink: (data) => data.permalink || `/guides/${data.page.fileSlug}/`,
  },
};
