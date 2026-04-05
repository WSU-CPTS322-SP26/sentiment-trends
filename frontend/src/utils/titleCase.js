export function toTitleCase(name) {
  if (!name || typeof name !== "string") return name;
  return name.replace(/\w[\w'-]*/g, (w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase());
}