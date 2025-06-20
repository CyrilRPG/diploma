const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { decodeJWT } = require('./decode');

const fetchFn = typeof fetch === 'function'
  ? fetch
  : (...args) => import('node-fetch').then(({ default: f }) => f(...args));

const TOKEN_ENDPOINT = 'https://diploma.exoteach.com/medibox2-api/graphql';

// Dictionnaire pour garder en mémoire le dernier token valide pour chaque
// utilisateur. Lorsqu'un nouveau token est validé, l'ancien devient obsolète.
const latestTokens = {};

function sendJSON(res, status, obj) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(obj));
}

async function handleValidate(req, res, query) {
  const token = query.token;
  const decoded = decodeJWT(token);
  const clientId = decoded?.id?.toString();

  if (!token || !decoded || !clientId) {
    sendJSON(res, 200, {
      ok: false,
      reason: 'Token JWT invalide ou non décodable',
      tokenClient: token,
      decodedPayload: decoded
    });
    return;
  }

  if (latestTokens[clientId] && latestTokens[clientId] !== token) {
    sendJSON(res, 200, {
      ok: false,
      reason: 'Token obsolète',
      tokenClient: token
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
      latestTokens[clientId] = token;
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

module.exports = { server };
