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

const http = require('http');
const { server, setFetch } = require('./server');

function createToken(payload) {
  const base64 = Buffer.from(JSON.stringify(payload)).toString('base64');
  return `h.${base64}.s`;
}

function startServer() {
  return new Promise((resolve) => {
    const srv = server.listen(0, () => resolve(srv));
  });
}

function requestValidate(srv, token) {
  const port = srv.address().port;
  return new Promise((resolve, reject) => {
    http.get(`http://localhost:${port}/validate?token=${encodeURIComponent(token)}`,
      res => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(JSON.parse(data)));
      })
      .on('error', reject);
  });
}

async function testValidate(okExpected) {
  const payload = { id: 123, exp: Math.floor(Date.now() / 1000) + 60 };
  const token = createToken(payload);
  const srv = await startServer();
  setFetch(async () => ({
    json: async () => ({ data: { me: { id: okExpected ? '123' : '999' } } })
  }));

  const result = await requestValidate(srv, token);
  srv.close();
  setFetch(undefined);
  assert.strictEqual(result.ok, okExpected);
}

async function runTests() {
  testDecodeValid();
  testDecodeInvalid();
  testTokenExpiry();
  await testValidate(true);
  await testValidate(false);
}

runTests().then(() => {
  console.log('All tests passed');
}).catch(err => {
  console.error('Test failed');
  console.error(err);
  process.exit(1);
});
