/** VADER-style compound is in [-1, 1]. Maps to plain-language labels. */
export function compoundSentimentLabel(score) {
  if (score == null || Number.isNaN(score)) return null;
  if (score >= 0.85) return "Overwhelmingly positive";
  if (score >= 0.6) return "Very positive";
  if (score >= 0.15) return "Somewhat positive";
  if (score >= 0.05) return "Slightly positive";
  if (score > -0.05) return "Neutral";
  if (score > -0.15) return "Slightly negative";
  if (score > -0.6) return "Somewhat negative";
  if (score > -0.85) return "Very negative";
  return "Overwhelmingly negative";
}

/** Most negative to most positive; used to escalate tone when share % aligns with compound. */
const OVERALL_TONE_TIERS = [
  "Overwhelmingly negative",
  "Very negative",
  "Somewhat negative",
  "Slightly negative",
  "Neutral",
  "Slightly positive",
  "Somewhat positive",
  "Very positive",
  "Overwhelmingly positive",
];

function overallToneTierIndex(label) {
  const i = OVERALL_TONE_TIERS.indexOf(label);
  return i === -1 ? null : i;
}

/**
 * Compound alone can sit mid-range while post-level labels are heavily one-sided.
 * When share and compound agree, pull the headline one or more steps (tighter "margins").
 */
export function overallToneLabel(compound, positivePct, negativePct) {
  const base = compoundSentimentLabel(compound);
  if (base == null) return null;
  let idx = overallToneTierIndex(base);
  if (idx == null) return base;

  const neg =
    negativePct != null && !Number.isNaN(Number(negativePct))
      ? Number(negativePct)
      : NaN;
  const pos =
    positivePct != null && !Number.isNaN(Number(positivePct))
      ? Number(positivePct)
      : NaN;

  if (compound != null && compound < 0 && !Number.isNaN(neg)) {
    if (neg >= 90 && compound <= -0.32) {
      idx = Math.min(idx, 0);
    } else if (neg >= 88 && compound <= -0.28) {
      idx = Math.min(idx, 0);
    } else if (neg >= 85 && compound <= -0.25) {
      idx = Math.min(idx, 1);
    } else if (neg >= 78 && compound <= -0.18) {
      idx = Math.min(idx, 2);
    }
  }

  if (compound != null && compound > 0 && !Number.isNaN(pos)) {
    if (pos >= 90 && compound >= 0.32) {
      idx = Math.max(idx, 8);
    } else if (pos >= 88 && compound >= 0.28) {
      idx = Math.max(idx, 8);
    } else if (pos >= 85 && compound >= 0.25) {
      idx = Math.max(idx, 7);
    } else if (pos >= 78 && compound >= 0.18) {
      idx = Math.max(idx, 6);
    }
  }

  return OVERALL_TONE_TIERS[idx];
}

function parseOptionalCompound(raw) {
  if (raw == null || raw === "") return null;
  const n = Number(raw);
  return Number.isNaN(n) ? null : n;
}

/**
 * Homepage cards: same tone ladder and share escalation as the topic page.
 * Uses avg_compound when present; otherwise a net-share heuristic in [-1, 1], except when
 * the neutral bucket clearly wins (then compound defaults to 0). Returns "Mixed sentiment"
 * when top buckets tie; null when there is no data.
 */
export function homepageCardTone(
  avgCompound,
  positiveFrac,
  neutralFrac,
  negativeFrac,
) {
  const p = Math.round((positiveFrac ?? 0) * 100);
  const neu = Math.round((neutralFrac ?? 0) * 100);
  const ne = Math.round((negativeFrac ?? 0) * 100);
  if (p + neu + ne === 0) return null;

  const buckets = [
    { key: "positive", v: p },
    { key: "neutral", v: neu },
    { key: "negative", v: ne },
  ];
  const maxV = Math.max(p, neu, ne);
  const winners = buckets.filter((b) => b.v === maxV && b.v > 0);
  if (winners.length !== 1) return "Mixed sentiment";

  const winner = winners[0].key;
  const stored = parseOptionalCompound(avgCompound);

  let effectiveCompound;
  if (winner === "neutral") {
    effectiveCompound = stored ?? 0;
  } else if (stored != null) {
    effectiveCompound = stored;
  } else {
    effectiveCompound = Math.max(-1, Math.min(1, (p - ne) / 100));
  }

  return overallToneLabel(effectiveCompound, p, ne);
}
