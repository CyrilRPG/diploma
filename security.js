async function verifierToken() {
  // 🚫 Évite une boucle : si on est déjà sur unauthorized.html, on ne vérifie rien
  if (window.location.pathname.endsWith("unauthorized.html")) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

  if (!token) {
    console.warn("❌ Aucun token trouvé dans l'URL.");
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
      window.location.href = "unauthorized.html";
    } else {
      console.log("✅ Token valide. Accès autorisé.");
      console.log("Données :", json.data);
    }

  } catch (err) {
    console.error("❌ Erreur de requête :", err);
    window.location.href = "unauthorized.html";
  }
}

// ▶️ Lancer la vérification au chargement
verifierToken();
