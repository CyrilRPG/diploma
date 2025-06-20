const assert = require('assert');
const { decodeJWT } = require('./decode');

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

try {
  testDecodeValid();
  testDecodeInvalid();
  console.log('All tests passed');
} catch (err) {
  console.error('Test failed');
  console.error(err);
  process.exit(1);
}
