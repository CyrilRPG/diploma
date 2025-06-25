function getFavorites() {
  try {
    return JSON.parse(localStorage.getItem('favorites') || '[]');
  } catch (e) {
    return [];
  }
}

function saveFavorites(favs) {
  localStorage.setItem('favorites', JSON.stringify(favs));
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
