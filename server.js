const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { decodeJWT, isTokenExpired } = require('./decode');

let fetchFn = typeof fetch === 'function'
  ? fetch
  : (...args) => import('node-fetch').then(({ default: f }) => f(...args));

function setFetch(fn) {
  fetchFn = fn;
}

const TOKEN_ENDPOINT = 'https://diploma.exoteach.com/medibox2-api/graphql';

// Durée de validité de chaque token stocké (8h)
const TOKEN_VALIDITY_MS = 8 * 60 * 60 * 1000;

// Fichier où sont mémorisés les tokens expirés ou révoqués
const REVOKED_FILE = path.join(__dirname, 'revokedTokens.json');

// Dictionnaire pour garder en mémoire le dernier token valide pour chaque
// utilisateur. Lorsqu'un nouveau token est validé, l'ancien devient obsolète.
// Map storing last token and its time (exp or iat) for each user
const latestTokens = {};
// Tokens valides temporairement (token -> { userId, expiresAt })
const validTokens = new Map();
// Ensemble des tokens expirés/révoqués
let revokedTokens = new Set();

try {
  const data = fs.readFileSync(REVOKED_FILE, 'utf8');
  revokedTokens = new Set(JSON.parse(data));
} catch {
  revokedTokens = new Set();
}

function saveRevokedTokens() {
  try {
    fs.writeFileSync(
      REVOKED_FILE,
      JSON.stringify([...revokedTokens], null, 2)
    );
  } catch {
    // ignore write errors
  }
}

function purgeExpiredTokens() {
  const now = Date.now();
  for (const [tok, rec] of validTokens) {
    if (now > rec.expiresAt) {
      revokeToken(tok);
    }
  }
}

setInterval(purgeExpiredTokens, 60 * 60 * 1000);

function getTokenTime(decoded) {
  if (decoded && typeof decoded.exp === 'number') {
    return decoded.exp;
  }
  if (decoded && typeof decoded.iat === 'number') {
    return decoded.iat;
  }
  return 0;
}

function revokeToken(token) {
  revokedTokens.add(token);
  validTokens.delete(token);
  saveRevokedTokens();
}

function sendJSON(res, status, obj) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(obj));
}

async function handleValidate(req, res, query) {
  const token = query.token;
  if (revokedTokens.has(token)) {
    sendJSON(res, 200, {
      ok: false,
      reason: 'Token expir\u00e9',
      tokenClient: token
    });
    return;
  }

  let decoded = decodeJWT(token);
  const clientId = (decoded?.id ?? decoded?.sub)?.toString();

  const record = validTokens.get(token);
  if (record && Date.now() > record.expiresAt) {
    revokeToken(token);
    sendJSON(res, 200, {
      ok: false,
      reason: 'Token expir\u00e9',
      tokenClient: token
    });
    return;
  }

  if (!token || !decoded || !clientId || isTokenExpired(decoded)) {
    revokeToken(token);
    sendJSON(res, 200, {
      ok: false,
      reason: 'Token JWT invalide ou non décodable',
      tokenClient: token,
      decodedPayload: decoded
    });
    return;
  }



  try {
    const response = await fetchFn(TOKEN_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Token': token,
      },
      body: JSON.stringify({
        query: `query { me { id email username } }`
      })
    });

    const json = await response.json();
    const exoId = json?.data?.me?.id?.toString();

    if (!exoId) {
      sendJSON(res, 200, {
        ok: false,
        reason: 'Réponse Exoatech invalide ou vide',
        debugExoatech: json
      });
      return;
    }

    const valid = clientId === exoId;

    if (valid) {
      const newTime = getTokenTime(decoded);
      const current = latestTokens[clientId];
      if (current) {
        if (newTime > current.time) {
          if (current.token !== token) {
            revokeToken(current.token);
          }
          latestTokens[clientId] = { token, time: newTime };
        } else if (current.token !== token) {
          sendJSON(res, 200, { ok: false, reason: 'Token obsolète' });
          return;
        }
      } else {
        latestTokens[clientId] = { token, time: newTime };
      }
      validTokens.set(token, { userId: clientId, expiresAt: Date.now() + TOKEN_VALIDITY_MS });
    }

    sendJSON(res, 200, {
      ok: valid,
      tokenClient: token,
      clientId,
      expectedUserId: exoId,
      decodedPayload: decoded,
      reason: valid ? undefined : "Le clientId ne correspond pas à l’id Exoatech"
    });
  } catch (err) {
    sendJSON(res, 500, {
      ok: false,
      reason: 'Erreur serveur',
      error: err.toString()
    });
  }
}

function getContentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case '.html': return 'text/html';
    case '.js': return 'application/javascript';
    case '.css': return 'text/css';
    case '.png': return 'image/png';
    case '.jpg':
    case '.jpeg': return 'image/jpeg';
    case '.svg': return 'image/svg+xml';
    default: return 'application/octet-stream';
  }
}

function serveFile(res, filePath) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': getContentType(filePath) });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  if (pathname === '/validate') {
    handleValidate(req, res, parsedUrl.query);
    return;
  }

  const anatMatch = pathname.match(/^\/anatapp(\d+)\.html$/);
  if (anatMatch) {
    const file = `anatapp${anatMatch[1]}.html`;
    const filePath = path.join(__dirname, 'Anatomie_App', file);
    serveFile(res, filePath);
    return;
  }

  let filePath = path.join(__dirname, pathname);
  if (pathname === '/' || pathname === '') {
    filePath = path.join(__dirname, 'index.html');
  }

  serveFile(res, filePath);
});

const PORT = process.env.PORT || 3000;
if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`✅ Serveur lancé sur http://localhost:${PORT}`);
  });
}

module.exports = {
  server,
  setFetch,
  _testing: { validTokens, revokedTokens, revokeToken, purgeExpiredTokens }
};
