const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const crypto = require('crypto');
const { decodeJWT, isTokenExpired } = require('./decode');

// Durée de validité de chaque token stocké (8h)
const TOKEN_VALIDITY_MS = 8 * 60 * 60 * 1000;

// Fichier où sont mémorisés les tokens expirés ou révoqués
const REVOKED_FILE = path.join(__dirname, 'revokedTokens.json');
// Durée de conservation des tokens révoqués (30 jours)
const REVOKED_RETENTION_MS = 30 * 24 * 60 * 60 * 1000;
// Nombre maximal de tokens révoqués conservés
const REVOKED_MAX_SIZE = 1000;
// Durée de validité d'un linkToken (1h)
const LINK_TOKEN_MS = 60 * 60 * 1000;

// Dictionnaire pour garder en mémoire le dernier token valide pour chaque
// utilisateur. Lorsqu'un nouveau token est validé, l'ancien devient obsolète.
// Map storing last token and its time (exp or iat) for each user
const latestTokens = {};
// Tokens valides temporairement (token -> { userId, expiresAt })
const validTokens = new Map();
// Map des tokens révoqués (hash -> timestamp)
let revokedTokens = new Map();
// Map des linkTokens actifs (linkToken -> { exoToken, expiresAt })
const linkTokens = new Map();

try {
  const data = fs.readFileSync(REVOKED_FILE, 'utf8');
  const parsed = JSON.parse(data);
  if (Array.isArray(parsed)) {
    if (typeof parsed[0] === 'string') {
      revokedTokens = new Map(parsed.map(t => [t, Date.now()]));
    } else {
      revokedTokens = new Map(parsed.map(r => [r.token, r.revokedAt]));
    }
  } else {
    revokedTokens = new Map();
  }
} catch {
  revokedTokens = new Map();
}

function saveRevokedTokens() {
  try {
    const arr = [...revokedTokens.entries()].map(([token, revokedAt]) => ({
      token,
      revokedAt
    }));
    fs.writeFileSync(REVOKED_FILE, JSON.stringify(arr, null, 2));
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

function cleanupRevokedTokens() {
  const now = Date.now();
  for (const [hash, ts] of revokedTokens) {
    if (now - ts > REVOKED_RETENTION_MS) {
      revokedTokens.delete(hash);
    }
  }
  enforceRevokedLimit();
  saveRevokedTokens();
}

function enforceRevokedLimit() {
  if (revokedTokens.size <= REVOKED_MAX_SIZE) {
    return;
  }
  const entries = [...revokedTokens.entries()].sort((a, b) => a[1] - b[1]);
  const excess = revokedTokens.size - REVOKED_MAX_SIZE;
  for (let i = 0; i < excess; i++) {
    revokedTokens.delete(entries[i][0]);
  }
}

setInterval(purgeExpiredTokens, 60 * 60 * 1000);
setInterval(cleanupRevokedTokens, 24 * 60 * 60 * 1000);

function getTokenTime(decoded) {
  if (decoded && typeof decoded.exp === 'number') {
    return decoded.exp;
  }
  if (decoded && typeof decoded.iat === 'number') {
    return decoded.iat;
  }
  return 0;
}

function hashToken(token) {
  return crypto.createHash('sha256').update(token).digest('hex');
}

function revokeToken(token) {
  const hash = hashToken(token);
  revokedTokens.set(hash, Date.now());
  validTokens.delete(token);
  enforceRevokedLimit();
  saveRevokedTokens();
}

async function verifyExoToken(token) {
  const decoded = decodeJWT(token);
  const clientId = (decoded?.id ?? decoded?.sub ?? decoded?.creatorUserId)?.toString();

  if (!token || !decoded || !clientId || isTokenExpired(decoded)) {
    return { ok: false, reason: 'Token JWT invalide ou non décodable', decoded, clientId };
  }

  return { ok: true, clientId, exoId: clientId, decoded };
}


function sendJSON(res, status, obj) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(obj));
}

async function handleValidate(req, res, query) {
  let token = query.token;
  const link = query.link;
  if (link) {
    const info = linkTokens.get(link);
    if (!info || info.expiresAt < Date.now()) {
      linkTokens.delete(link);
      sendJSON(res, 200, { ok: false, reason: 'Link expir\u00e9' });
      return;
    }
    token = info.exoToken;
  }

  const tokenHash = hashToken(token);
  if (revokedTokens.has(tokenHash)) {
    sendJSON(res, 200, {
      ok: false,
      reason: 'Token expir\u00e9',
      tokenClient: token
    });
    return;
  }

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

  const verify = await verifyExoToken(token);
  if (!verify.ok) {
    if (verify.isError) {
      sendJSON(res, 500, verify);
    } else {
      revokeToken(token);
      sendJSON(res, 200, {
        ok: false,
        reason: verify.reason,
        tokenClient: token,
        decodedPayload: verify.decoded
      });
    }
    return;
  }

  const { clientId, exoId, decoded } = verify;
  const valid = verify.ok;

    if (valid) {
      const newTime = getTokenTime(decoded);
      const current = latestTokens[clientId];
      if (!current || newTime >= current.time) {
        if (current && current.token !== token) {
          revokeToken(current.token);
        }
        latestTokens[clientId] = { token, time: newTime };
        validTokens.set(token, {
          userId: clientId,
          expiresAt: Date.now() + TOKEN_VALIDITY_MS,
        });
      } else if (current.token !== token) {
        revokeToken(token);
        sendJSON(res, 200, {
          ok: false,
          reason: 'Token obsolète',
          tokenClient: token
        });
        return;
      }
    }

    sendJSON(res, 200, {
      ok: valid,
      tokenClient: token,
      clientId,
      expectedUserId: exoId,
      decodedPayload: decoded,
      reason: valid ? undefined : "Le clientId ne correspond pas à l’id Exoatech"
    });
}

async function handleGenerateLink(req, res, query) {
  const token = query.token;
  const verify = await verifyExoToken(token);
  if (!verify.ok) {
    sendJSON(res, 200, { ok: false, reason: verify.reason });
    return;
  }
  const link = crypto.randomBytes(16).toString('hex');
  linkTokens.set(link, { exoToken: token, expiresAt: Date.now() + LINK_TOKEN_MS });
  sendJSON(res, 200, { ok: true, linkToken: link, expiresAt: Date.now() + LINK_TOKEN_MS });
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

  if (pathname === '/generate-link') {
    handleGenerateLink(req, res, parsedUrl.query);
    return;
  }

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
const HOST = process.env.HOST || '0.0.0.0';
if (require.main === module) {
  server.listen(PORT, HOST, () => {
    console.log(`✅ Serveur lancé sur http://${HOST}:${PORT}`);
  });
}

module.exports = {
  server,
  _testing: { validTokens, revokedTokens, revokeToken, purgeExpiredTokens, linkTokens }
};
