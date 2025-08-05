# Diplome Flashcard

Cette application Node.js sert des fichiers statiques et propose un endpoint `/validate`.

## Développement local

```bash
npm install
npm start
```

## Déploiement sur OVH

- Le fichier `.ovhconfig` configure l'environnement Node.js (version 20) et la production.
- Les fichiers statiques se trouvent dans le dossier `public`.
- Définir les variables d'environnement `EXOATECH_TOKEN` et `TOKEN_ENDPOINT` via l'interface OVH ou un fichier `.env` non commité.
