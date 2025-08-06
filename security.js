const VERIFY_URL = 'https://api.exoteach.com/verifytoken';
const API_KEY = '2a7dd57cabdd18494317dc2e536ae761e781abe418ca16bb95d89f2181a9733f';

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
    const jsonPayload = atob(base64);
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

async function hashToken(str) {
  const buf = new TextEncoder().encode(str);
  const digest = await crypto.subtle.digest('SHA-256', buf);
  return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function verifierToken() {
  if (window.location.pathname.endsWith('unauthorized.html')) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const urlToken = params.get('token');
  const sessionToken = sessionStorage.getItem('jwtToken');
  const token = urlToken || sessionToken;

  if (!token) {
    console.warn('❌ Aucun token trouvé dans l\'URL ou le stockage.');
    window.location.href = 'unauthorized.html';
    return;
  }

  const decoded = decodeJWT(token);
  if (!decoded) {
    console.warn('❌ Token illisible.');
    window.location.href = 'unauthorized.html';
    return;
  }

  if (typeof decoded.exp === 'number' && decoded.exp * 1000 < Date.now()) {
    console.warn('❌ Token expiré.');
    window.location.href = 'unauthorized.html';
    return;
  }

  try {
    const resp = await fetch(VERIFY_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
      },
      body: JSON.stringify({ token }),
    });

    const data = await resp.json();
    if (resp.status !== 200 || data.message !== 'ok') {
      console.warn('❌ Token refusé :', data.message);
      window.location.href = 'unauthorized.html';
      return;
    }

    if (urlToken) {
      sessionStorage.setItem('jwtToken', urlToken);
      const h = await hashToken(urlToken);
      localStorage.setItem('jwtTokenHash', h);
    }
  } catch (err) {
    console.warn('❌ Erreur de validation du token:', err);
    window.location.href = 'unauthorized.html';
    return;
  }

  console.log('✅ Token détecté et validé :', decoded);
}

verifierToken();
