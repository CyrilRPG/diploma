// Endpoint local pour valider les tokens
const VALIDATE_ENDPOINT = '/validate';

// Clés utilisées dans localStorage
const AUTH_KEY = 'authorized';
const USED_TOKENS_KEY = 'used_tokens';
const VALIDATION_DONE_KEY = 'validation_done';

async function authorizeFromToken() {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');

  // Si déjà validé ou échoué, ne pas revérifier
  if (localStorage.getItem(VALIDATION_DONE_KEY) === 'true') {
    return;
  }

  if (!token) {
    localStorage.setItem(VALIDATION_DONE_KEY, 'true');
    localStorage.removeItem(AUTH_KEY);
    return;
  }

  try {
    const response = await fetch(`${VALIDATE_ENDPOINT}?token=${encodeURIComponent(token)}`);
    const data = await response.json();

    if (data.ok) {
      const usedTokens = JSON.parse(localStorage.getItem(USED_TOKENS_KEY) || '[]');

      if (!usedTokens.includes(token)) {
        usedTokens.push(token);
        localStorage.setItem(USED_TOKENS_KEY, JSON.stringify(usedTokens));
      }

      localStorage.setItem(AUTH_KEY, 'true');
    } else {
      localStorage.removeItem(AUTH_KEY);
    }
  } catch (err) {
    console.error('Token validation failed', err);
    localStorage.removeItem(AUTH_KEY);
  }

  // Validation terminée
  localStorage.setItem(VALIDATION_DONE_KEY, 'true');

  // Nettoyer l'URL après traitement
  window.history.replaceState({}, document.title, window.location.pathname);
}

function checkAccess() {
  const authorized = localStorage.getItem(AUTH_KEY);
  const validated = localStorage.getItem(VALIDATION_DONE_KEY);

  // Si validation déjà faite et non autorisé → rediriger vers unauthorized.html
  if (validated === 'true' && authorized !== 'true') {
    if (!window.location.pathname.endsWith('unauthorized.html')) {
      window.location.replace('unauthorized.html');
    }
  }
}

// À exécuter sur toutes les pages
(async () => {
  await authorizeFromToken();
  checkAccess();
})();
