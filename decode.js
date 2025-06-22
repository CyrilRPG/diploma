function base64UrlToBase64(str) {
  str = str.replace(/-/g, '+').replace(/_/g, '/');
  const pad = str.length % 4;
  if (pad) str += '='.repeat(4 - pad);
  return str;
}

function decodeJWT(token) {
  try {
    const base64Payload = token.split('.')[1];
    const base64 = base64UrlToBase64(base64Payload);
    const jsonPayload = Buffer.from(base64, 'base64').toString();
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

function isTokenExpired(decoded) {
  if (!decoded || typeof decoded.exp !== 'number') {
    return true;
  }
  return decoded.exp * 1000 < Date.now();
}

module.exports = { decodeJWT, isTokenExpired };
