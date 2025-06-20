async function verifierToken() {
  // 🚫 Évite une boucle : si on est déjà sur unauthorized.html, on ne vérifie rien
  if (window.location.pathname.endsWith("unauthorized.html")) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const urlToken = params.get("token");
  const storedToken = localStorage.getItem("jwtToken");

  // Si un token est présent dans l'URL, il devient le nouveau token stocké
  if (urlToken) {
    if (urlToken !== storedToken) {
      localStorage.setItem("jwtToken", urlToken);
    }
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

  // Validation supplémentaire auprès de notre serveur pour s'assurer que
  // le token correspond bien au dernier utilisé par cet utilisateur.
  try {
    const validRes = await fetch(`/validate?token=${encodeURIComponent(token)}`);
    const validJson = await validRes.json();
    if (!validJson.ok) {
      console.warn("❌ Token obsolète ou invalide :", validJson.reason);
      localStorage.removeItem("jwtToken");
      window.location.href = "unauthorized.html";
      return;
    }
  } catch (err) {
    console.error("❌ Erreur de validation du token :", err);
    localStorage.removeItem("jwtToken");
    window.location.href = "unauthorized.html";
    return;
  }

  try {
    const response = await fetch("https://diploma.exoteach.com/medibox2-api/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Token": token,
      },
      body: JSON.stringify({
        query: "{ me { id name } }", // requête protégée à adapter selon l’API
      }),
    });

    const json = await response.json();

    if (json.errors) {
      console.warn("❌ Token invalide ou refusé :", json.errors[0].message);
      localStorage.removeItem("jwtToken");
      window.location.href = "unauthorized.html";
    } else {
      console.log("✅ Token valide. Accès autorisé.");
      console.log("Données :", json.data);
    }

  } catch (err) {
    console.error("❌ Erreur de requête :", err);
    localStorage.removeItem("jwtToken");
    window.location.href = "unauthorized.html";
  }
}

// ▶️ Lancer la vérification au chargement
verifierToken();
