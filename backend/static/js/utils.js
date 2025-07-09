export function getCSRFToken() {
  const token = document.querySelector('meta[name="csrf-token"]');

  return token ? token.getAttribute("content") : null;
}
