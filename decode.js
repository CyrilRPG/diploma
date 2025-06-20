function decodeJWT(token) {
  try {
    const base64Payload = token.split('.')[1];
    const jsonPayload = Buffer.from(base64Payload, 'base64').toString();
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
