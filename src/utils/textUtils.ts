/**
 * Remove acentos e diacríticos de um texto para permitir busca insensível a acentuação.
 * Exemplo: "Ação Caído" -> "acao caido"
 */
export function removeAccents(text: string): string {
  if (!text) return '';
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}
