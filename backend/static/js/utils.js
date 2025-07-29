export function getCSRFToken() {
  const token = document.querySelector('meta[name="csrf-token"]');

  return token ? token.getAttribute("content") : null;
}

export function parseDate(isoString) {
  const date = new Date(isoString);

  // padStart로 자리수 맞춤 (e.g. 07 → 07)
  const formatted =
    date.getFullYear() +
    "-" +
    String(date.getMonth() + 1).padStart(2, "0") +
    "-" +
    String(date.getDate()).padStart(2, "0");

  return formatted;
}

export function formatDate(dateString) {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}
