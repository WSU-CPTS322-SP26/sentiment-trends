import topicPlaceholder from "../assets/topic-placeholder.svg";

export function toTitleCase(name) {
  if (!name || typeof name !== "string") return name;
  return name.replace(/\w[\w'-]*/g, (w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase());
}

// all first, then only category labels that appear on at least one card
export function categoriesFromCards(cards) {
  const nav = [{ id: "all", label: "All", href: "/" }];
  const seen = new Set();
  for (const c of cards) {
    for (const lab of c.category) {
      if (lab && typeof lab === "string") seen.add(lab);
    }
  }
  const sorted = [...seen].sort((a, b) => a.localeCompare(b));
  for (const label of sorted) {
    nav.push({
      id: label,
      label,
      href: `/?category=${encodeURIComponent(label)}`,
    });
  }
  return nav;
}

export function mapApiCardToDisplay(api) {
  const pos = api.positive_pct;
  const neu = api.neutral_pct;
  const neg = api.negative_pct;
  const rawCat = api.category;
  const category = Array.isArray(rawCat)
    ? rawCat
    : rawCat
      ? [rawCat]
      : [];
  return {
    id: api.id,
    title: api.title,
    displayTitle: toTitleCase(api.title),
    image: topicPlaceholder,
    category,
    positive_sentiment: (pos ?? 0) / 100,
    neutral_sentiment: (neu ?? 0) / 100,
    negative_sentiment: (neg ?? 0) / 100,
  };
}