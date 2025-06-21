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

  // Si un token était déjà présent et qu'un autre est fourni dans l'URL,
  // on considère qu'il s'agit d'un lien obsolète
  if (urlToken && storedToken && urlToken !== storedToken) {
    console.warn("❌ Ancien token détecté. Accès refusé.");
    window.location.href = "unauthorized.html";
    return;
  }

  // Si un token est présent dans l'URL, il devient le nouveau token stocké
  if (urlToken) {
    localStorage.setItem("jwtToken", urlToken);
  }

  const token = localStorage.getItem("jwtToken");

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

  if (typeof decoded.exp === "number" && decoded.exp * 1000 < Date.now()) {
    console.warn("❌ Token expiré.");
    window.location.href = "unauthorized.html";
    return;
  }

  try {
    const resp = await fetch(`/validate?token=${encodeURIComponent(token)}`);
    const json = await resp.json();
    if (!json.ok) {
      console.warn("❌ Token refusé :", json.reason);
      window.location.href = "unauthorized.html";
      return;
    }
  } catch (err) {
    console.warn("❌ Erreur de validation du token:", err);
    window.location.href = "unauthorized.html";
    return;
  }

  console.log("✅ Token détecté et validé :", decoded);
}

// ▶️ Lancer la vérification au chargement
verifierToken();
