module.exports = {
  apps: [
    {
      name: 'diploma-server',
      script: './server.js',
      env: {
        PORT: 3000
      },
      autorestart: true,
      watch: false
    }
  ]
};
