const express = require('express');
const app = express();

const fetchFn = typeof fetch === 'function'
  ? fetch
  : (...args) => import('node-fetch').then(({ default: f }) => f(...args));

const TOKEN_ENDPOINT = 'https://diploma.exoteach.com/medibox2-api/graphql';
const EXOATECH_TOKEN = 'TON_X_TOKEN_ICI'; // <-- à remplacer absolument

function decodeJWT(token) {
  try {
    const base64Payload = token.split('.')[1];
    const jsonPayload = Buffer.from(base64Payload, 'base64').toString();
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

app.get('/validate', async (req, res) => {
  const token = req.query.token;
  const decoded = decodeJWT(token);
  const clientId = decoded?.id?.toString();

  if (!token || !decoded || !clientId) {
    return res.json({
      ok: false,
      reason: 'Token JWT invalide ou non décodable',
      tokenClient: token,
      decodedPayload: decoded
    });
  }

  try {
    const response = await fetchFn(TOKEN_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Token': EXOATECH_TOKEN,
      },
      body: JSON.stringify({
        query: `query { me { id email username } }`
      })
    });

    const json = await response.json();
    const exoId = json?.data?.me?.id?.toString();

    if (!exoId) {
      return res.json({
        ok: false,
        reason: 'Réponse Exoatech invalide ou vide',
        debugExoatech: json
      });
    }

    const valid = clientId === exoId;

    return res.json({
      ok: valid,
      tokenClient: token,
      clientId,
      expectedUserId: exoId,
      decodedPayload: decoded,
      reason: valid ? undefined : 'Le clientId ne correspond pas à l’id Exoatech'
    });

  } catch (err) {
    return res.status(500).json({
      ok: false,
      reason: 'Erreur serveur',
      error: err.toString()
    });
  }
});

const PORT = process.env.PORT || 3000;
app.use(express.static(__dirname));
app.listen(PORT, () => {
  console.log(`✅ Serveur lancé sur http://localhost:${PORT}`);
});
