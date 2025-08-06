#!/usr/bin/env bash
set -euo pipefail

# Script d'installation de Node.js et déploiement d'une application avec PM2
# Usage : ./setup_pm2.sh [url_du_depot] [dossier_cible]

REPO_URL="${1:-https://github.com/votre-utilisateur/votre-repo.git}"
TARGET_DIR="${2:-app}"

echo "Mise à jour des paquets..."
sudo apt-get update -y

echo "Installation des dépendances système..."
sudo apt-get install -y curl git

echo "Installation de Node.js (NodeSource 18.x)..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

echo "Installation de PM2..."
sudo npm install -g pm2

echo "Clonage du dépôt Git..."
git clone "$REPO_URL" "$TARGET_DIR"
cd "$TARGET_DIR"

echo "Installation des dépendances Node.js..."
npm install

echo "Démarrage de l'application avec PM2..."
pm2 start server.js --name diploma-app

# Configurer PM2 pour se lancer au démarrage
pm2 startup systemd -u "$(whoami)" --hp "$HOME"
pm2 save
