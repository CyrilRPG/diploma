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

  // On tente d'abord le token fourni dans l'URL, sinon celui déjà stocké
  const token = urlToken || storedToken;

  if (!token) {
    console.warn("❌ Aucun token trouv\u00e9 dans l'URL ou le stockage.");
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
    if (urlToken && urlToken !== storedToken) {
      // Le nouveau token est valide : on remplace l'ancien stocké
      localStorage.setItem("jwtToken", urlToken);
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
