function decodeJWT(token) {
  try {
    const base64Payload = token.split('.')[1];
    const jsonPayload = Buffer.from(base64Payload, 'base64').toString();
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

module.exports = { decodeJWT };
