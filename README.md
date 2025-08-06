# Diploma Flashcard

Cette application fournit un petit serveur de validation de tokens Exoatech.

## Prérequis
- Node.js \>= 18

## Installation
```bash
npm install
```

## Lancement du serveur
```bash
npm start
```
Le serveur s'ex\u00e9cute par d\u00e9faut sur [http://localhost:3000](http://localhost:3000).

## Tests
```bash
npm test
```
Tous les tests doivent afficher `All tests passed`.

## Fonctionnement
- `/validate?token=TOKEN` v\u00e9rifie un token Exoatech ou `/validate?link=LINKTOKEN` pour utiliser un lien temporaire.
- `/generate-link?token=TOKEN` g\u00e9n\u00e8re un `linkToken` valable une heure.
- Le serveur conserve uniquement le token le plus r\u00e9cent par utilisateur et r\u00e9voque les plus anciens.
- Les tokens r\u00e9voqu\u00e9s sont conserv\u00e9s 30 jours et le fichier est nettoy\u00e9
  automatiquement d\u00e8s qu'il d\u00e9passe 1000 entr\u00e9es.

## D\u00e9ploiement avec PM2 sur Debian 12
Pour un environnement de production sur un VPS (ex. Hetzner) utilisant Debian\u00a012, vous pouvez g\u00e9rer le processus avec [PM2](https://pm2.keymetrics.io/).

1. Installer PM2 globalement\u00a0:
   ```bash
   npm install -g pm2
   ```
2. D\u00e9marrer l'application avec la configuration fournie\u00a0:
   ```bash
   pm2 start ecosystem.config.js
   ```
3. Configurer PM2 pour red\u00e9marrer le service au d\u00e9marrage du serveur\u00a0:
   ```bash
   pm2 startup systemd
   pm2 save
   ```
PM2 utilisera le fichier `ecosystem.config.js` pour lancer `server.js` sur le port\u00a03000 et red\u00e9marrera automatiquement le processus en cas de crash ou de red\u00e9marrage du serveur.

