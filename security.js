function base64UrlToBase64(str) {
  str = str.replace(/-/g, '+').replace(/_/g, '/');
  const pad = str.length % 4;
  if (pad) str += '='.repeat(4 - pad);
  return str;
}

function decodeJWT(token) {
  try {
    const base64Payload = token.split(".")[1];
    const base64 = base64UrlToBase64(base64Payload);
    const jsonPayload = atob(base64);
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

async function hashToken(str) {
  const buf = new TextEncoder().encode(str);
  const digest = await crypto.subtle.digest('SHA-256', buf);
  return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function verifierToken() {
  // 🚫 Évite une boucle : si on est déjà sur unauthorized.html, on ne vérifie rien
  if (window.location.pathname.endsWith("unauthorized.html")) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const urlToken = params.get("token");
  const urlLink = params.get("link");
  const sessionToken = sessionStorage.getItem("jwtToken");
  const sessionLink = sessionStorage.getItem("linkToken");

  const token = urlToken || sessionToken;
  const link = urlLink || sessionLink;

  if (!token && !link) {
    console.warn("❌ Aucun token trouv\u00e9 dans l'URL ou le stockage.");
    window.location.href = "unauthorized.html";
    return;
  }

  const decoded = token ? decodeJWT(token) : null;
  if (!decoded && token) {
    console.warn("❌ Token illisible.");
    window.location.href = "unauthorized.html";
    return;
  }
  const clientId = decoded ? (decoded?.id ?? decoded?.sub ?? decoded?.creatorUserId)?.toString() : null;
  if (token && !clientId) {
    console.warn("❌ Token sans identifiant utilisateur.");
    window.location.href = "unauthorized.html";
    return;
  }

  if (decoded && typeof decoded.exp === "number" && decoded.exp * 1000 < Date.now()) {
    console.warn("❌ Token expiré.");
    window.location.href = "unauthorized.html";
    return;
  }

  try {
    const query = token ? `token=${encodeURIComponent(token)}` : `link=${encodeURIComponent(link)}`;
    const resp = await fetch(`/validate?${query}`);
    const json = await resp.json();
    if (!json.ok) {
      console.warn("❌ Token refusé :", json.reason);
      window.location.href = "unauthorized.html";
      return;
    }
    if (urlToken) {
      sessionStorage.setItem("jwtToken", urlToken);
      const h = await hashToken(urlToken);
      localStorage.setItem("jwtTokenHash", h);
    } else if (urlLink) {
      sessionStorage.setItem("linkToken", urlLink);
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
