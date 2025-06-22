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
const fs = require('fs');
const path = require('path');

const revokedFile = path.join(__dirname, 'revokedTokens.json');

function loadServer() {
  delete require.cache[require.resolve('./server')];
  return require('./server');
}

let { server, setFetch, _testing } = loadServer();

function createToken(payload) {
  const base64 = Buffer.from(JSON.stringify(payload)).toString('base64');
  return `h.${base64}.s`;
}

function startServer(srvInstance = server) {
  return new Promise((resolve) => {
    const srv = srvInstance.listen(0, () => resolve(srv));
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

async function testValidateSub() {
  const payload = { sub: 321, exp: Math.floor(Date.now() / 1000) + 60 };
  const token = createToken(payload);
  const srv = await startServer();
  setFetch(async () => ({
    json: async () => ({ data: { me: { id: '321' } } })
  }));

  const result = await requestValidate(srv, token);
  srv.close();
  setFetch(undefined);
  assert.strictEqual(result.ok, true);
}

async function testValidateExpiry() {
  const payload = { id: 123, exp: Math.floor(Date.now() / 1000) + 60 };
  const token = createToken(payload);
  const srv = await startServer();
  setFetch(async () => ({ json: async () => ({ data: { me: { id: '123' } } }) }));

  const result1 = await requestValidate(srv, token);
  assert.strictEqual(result1.ok, true);

  const { validTokens, revokedTokens } = _testing;
  const rec = validTokens.get(token);
  rec.expiresAt = Date.now() - 1000; // expire manually

  const result2 = await requestValidate(srv, token);
  assert.strictEqual(result2.ok, false);
  assert.strictEqual(revokedTokens.has(token), true);

  srv.close();
  setFetch(undefined);
}

async function testRevokedPersistence() {
  fs.writeFileSync(revokedFile, '[]');
  _testing.revokedTokens.clear();

  ({ server, setFetch, _testing } = loadServer());
  let srv = await startServer(server);
  setFetch(async () => ({ json: async () => ({ data: { me: { id: '123' } } }) }));

  const token = createToken({ id: 123, exp: Math.floor(Date.now() / 1000) + 60 });
  const res1 = await requestValidate(srv, token);
  assert.strictEqual(res1.ok, true);

  _testing.revokeToken(token);
  srv.close();
  setFetch(undefined);

  ({ server, setFetch, _testing } = loadServer());
  srv = await startServer(server);
  setFetch(async () => ({ json: async () => ({ data: { me: { id: '123' } } }) }));

  const res2 = await requestValidate(srv, token);
  assert.strictEqual(res2.ok, false);

  srv.close();
  setFetch(undefined);
}

async function testTokenReplacement() {
  fs.writeFileSync(revokedFile, '[]');
  ({ server, setFetch, _testing } = loadServer());
  const srv = await startServer(server);
  setFetch(async () => ({ json: async () => ({ data: { me: { id: '123' } } }) }));

  const now = Math.floor(Date.now() / 1000);
  const oldToken = createToken({ id: 123, exp: now + 300 });
  let res = await requestValidate(srv, oldToken);
  assert.strictEqual(res.ok, true);

  const newToken = createToken({ id: 123, exp: now + 400 });
  res = await requestValidate(srv, newToken);
  assert.strictEqual(res.ok, true);
  assert.strictEqual(_testing.revokedTokens.has(oldToken), true);

  srv.close();
  setFetch(undefined);
}

async function testObsoleteToken() {
  fs.writeFileSync(revokedFile, '[]');
  ({ server, setFetch, _testing } = loadServer());
  const srv = await startServer(server);
  setFetch(async () => ({ json: async () => ({ data: { me: { id: '123' } } }) }));

  const now = Math.floor(Date.now() / 1000);
  const recentToken = createToken({ id: 123, exp: now + 200 });
  let res = await requestValidate(srv, recentToken);
  assert.strictEqual(res.ok, true);

  const oldToken = createToken({ id: 123, exp: now + 100 });
  res = await requestValidate(srv, oldToken);
  assert.strictEqual(res.ok, false);
  assert.strictEqual(res.reason, 'Token obsolète');
  assert.strictEqual(_testing.revokedTokens.has(recentToken), false);
  assert.strictEqual(_testing.validTokens.has(recentToken), true);

  srv.close();
  setFetch(undefined);
}

async function runTests() {
  testDecodeValid();
  testDecodeInvalid();
  testTokenExpiry();
  await testValidate(true);
  await testValidateSub();
  await testValidate(false);
  await testValidateExpiry();
  await testTokenReplacement();
  await testObsoleteToken();
  await testRevokedPersistence();
}

runTests().then(() => {
  console.log('All tests passed');
}).catch(err => {
  console.error('Test failed');
  console.error(err);
  process.exit(1);
});
