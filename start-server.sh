#!/bin/bash

echo "🥑 Le Sale Garage - Serveur local"
echo "=================================="
echo ""

# Générer index.json
echo "📋 Génération de index.json..."
python3 generate_index.py

echo ""
echo "🚀 Démarrage du serveur..."
echo "📍 Ouvre ton navigateur à: http://localhost:8000"
echo ""
echo "Appuie sur Ctrl+C pour arrêter"
echo ""

python3 -m http.server 8000
