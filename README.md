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

