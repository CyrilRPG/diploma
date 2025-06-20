function decodeJWT(token) {
  try {
    const base64Payload = token.split(".")[1];
    const jsonPayload = atob(base64Payload);
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

async function verifierToken() {
  // 🚫 Évite une boucle : si on est déjà sur unauthorized.html, on ne vérifie rien
  if (window.location.pathname.endsWith("unauthorized.html")) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const urlToken = params.get("token");
  const storedToken = localStorage.getItem("jwtToken");

  // Si un token est présent dans l'URL, il devient le nouveau token stocké
  if (urlToken && urlToken !== storedToken) {
    localStorage.setItem("jwtToken", urlToken);
  }

  const token = localStorage.getItem("jwtToken");

  // Si un token était dans l'URL mais ne correspond plus au dernier token stocké,
  // on considère qu'il est obsolète
  if (urlToken && urlToken !== token) {
    console.warn("❌ Ancien token détecté. Accès refusé.");
    window.location.href = "unauthorized.html";
    return;
  }

  if (!token) {
    console.warn("❌ Aucun token trouvé dans l'URL ou le stockage.");
    window.location.href = "unauthorized.html";
    return;
  }

  const decoded = decodeJWT(token);
  if (!decoded) {
    console.warn("❌ Token illisible.");
    window.location.href = "unauthorized.html";
    return;
  }

  // Aucune validation réseau n'est effectuée pour permettre l'utilisation hors ligne.
  console.log("✅ Token détecté :", decoded);
}

// ▶️ Lancer la vérification au chargement
verifierToken();
