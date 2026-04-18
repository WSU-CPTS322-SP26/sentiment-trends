import topicPlaceholder from "../assets/topic-placeholder.svg";

export function toTitleCase(name) {
  if (!name || typeof name !== "string") return name;
  return name.replace(
    /\w[\w'-]*/g,
    (w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase(),
  );
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

/** Coerce topics.image_url (text[] or occasional string) into a string list. */
function imageUrlList(raw) {
  if (Array.isArray(raw)) return raw;
  if (raw == null) return [];
  if (typeof raw === "string") {
    const t = raw.trim();
    if (!t) return [];
    if (t.startsWith("[")) {
      try {
        const parsed = JSON.parse(t);
        return Array.isArray(parsed) ? parsed : [];
      } catch {
        return [t];
      }
    }
    return [t];
  }
  return [];
}

export function mapApiCardToDisplay(api) {
  const pos = api.positive_pct;
  const neu = api.neutral_pct;
  const neg = api.negative_pct;
  const rawCat = api.category;
  const category = Array.isArray(rawCat) ? rawCat : rawCat ? [rawCat] : [];
  let firstUrl = null;
  for (const u of imageUrlList(api.image_url)) {
    if (typeof u === "string" && u.trim() !== "") {
      firstUrl = u.trim();
      break;
    }
  }
  return {
    id: api.id,
    title: api.title,
    displayTitle: toTitleCase(api.title),
    image: firstUrl ?? topicPlaceholder,
    category,
    searches: api.searches,
    increase_pct: api.increase_pct,
    positive_sentiment: (pos ?? 0) / 100,
    neutral_sentiment: (neu ?? 0) / 100,
    negative_sentiment: (neg ?? 0) / 100,
  };
}
