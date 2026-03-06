function getFavoritesKey() {
  try {
    const path = window.location.pathname || '';
    if (path.includes('/USPN_S1/')) return 'favorites_USPN_S1';
    if (path.includes('/USPN_S2/')) return 'favorites_USPN_S2';
    if (path.includes('/SU_S1/')) return 'favorites_SU_S1';
    if (path.includes('/SU_S2/')) return 'favorites_SU_S2';
    if (path.includes('/UPEC_LSPS1_S2/')) return 'favorites_UPEC_LSPS1_S2';
    if (path.includes('/UPEC_LSPS3_S2/')) return 'favorites_UPEC_LSPS3_S2';
  } catch (e) {
    // Fallback si window.location n'est pas disponible (tests, node, etc.)
  }
  return 'favorites';
}

function migrateOldFavoritesIfNeeded(namespacedKey) {
  try {
    // Si on a déjà des favoris pour cette fac/semestre, ne rien faire.
    if (localStorage.getItem(namespacedKey)) return;

    // Ancienne clé globale
    const legacy = localStorage.getItem('favorites');
    if (!legacy) return;

    // On migre l'ancien tableau vers la clé dédiée courante.
    localStorage.setItem(namespacedKey, legacy);
    // On laisse l'ancienne clé en place pour ne pas casser d'autres contextes éventuels.
  } catch (e) {
    // En cas d'erreur, on ne bloque pas l'app.
  }
}

function getFavorites() {
  try {
    const key = getFavoritesKey();
    migrateOldFavoritesIfNeeded(key);
    return JSON.parse(localStorage.getItem(key) || '[]');
  } catch (e) {
    return [];
  }
}

function saveFavorites(favs) {
  const key = getFavoritesKey();
  localStorage.setItem(key, JSON.stringify(favs));
}

function isSameCard(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}

function isFavorite(card) {
  return getFavorites().some(f => isSameCard(f, card));
}

function addFavorite(card) {
  const favs = getFavorites();
  if (!favs.some(f => isSameCard(f, card))) {
    favs.push(card);
    saveFavorites(favs);
  }
}

function removeFavorite(card) {
  let favs = getFavorites();
  favs = favs.filter(f => !isSameCard(f, card));
  saveFavorites(favs);
}

function toggleFavorite(card) {
  if (isFavorite(card)) removeFavorite(card); else addFavorite(card);
}

if (typeof module !== 'undefined') {
  module.exports = { getFavorites, saveFavorites, isFavorite, addFavorite, removeFavorite, toggleFavorite };
}
