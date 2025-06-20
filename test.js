const assert = require('assert');
const { decodeJWT, isTokenExpired } = require('./decode');

function testDecodeValid() {
  const payload = { id: 123, name: 'test' };
  const base64 = Buffer.from(JSON.stringify(payload)).toString('base64');
  const token = `header.${base64}.signature`;
  const decoded = decodeJWT(token);
  assert.deepStrictEqual(decoded, payload);
}

function testDecodeInvalid() {
  const decoded = decodeJWT('invalid.token');
  assert.strictEqual(decoded, null);
}

function testTokenExpiry() {
  const expiredPayload = { id: 1, exp: Math.floor(Date.now() / 1000) - 10 };
  const expiredBase64 = Buffer.from(JSON.stringify(expiredPayload)).toString('base64');
  const expiredToken = `h.${expiredBase64}.s`;
  const decodedExpired = decodeJWT(expiredToken);
  assert.strictEqual(isTokenExpired(decodedExpired), true);

  const validPayload = { id: 1, exp: Math.floor(Date.now() / 1000) + 10 };
  const validBase64 = Buffer.from(JSON.stringify(validPayload)).toString('base64');
  const validToken = `h.${validBase64}.s`;
  const decodedValid = decodeJWT(validToken);
  assert.strictEqual(isTokenExpired(decodedValid), false);
}

try {
  testDecodeValid();
  testDecodeInvalid();
  testTokenExpiry();
  console.log('All tests passed');
} catch (err) {
  console.error('Test failed');
  console.error(err);
  process.exit(1);
}
