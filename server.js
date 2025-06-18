const express = require('express');
const app = express();
// Ensure fetch is available across Node versions
const fetchFn =
  typeof fetch === 'function'
    ? fetch
    : (...args) => import('node-fetch').then(({ default: f }) => f(...args));

const TOKEN_ENDPOINT = 'https://diploma.exoteach.com/medibox2-api/graphql';

app.get('/validate', async (req, res) => {
  const clientToken = req.query.token;
  if (!clientToken) {
    return res.json({ ok: false });
  }

  try {
    const response = await fetchFn(TOKEN_ENDPOINT);
    if (!response.ok) {
      console.error('Failed to fetch token', await response.text());
      return res.status(500).json({ ok: false });
    }

    const serverToken = (await response.text()).trim();
    const valid = clientToken === serverToken;
    res.json({ ok: valid });
  } catch (err) {
    console.error(err);
    res.status(500).json({ ok: false });
  }
});

const PORT = process.env.PORT || 3000;
app.use(express.static(__dirname));
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
