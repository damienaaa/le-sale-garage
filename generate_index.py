#!/usr/bin/env python3
"""
Génère automatiquement le fichier index.json
à partir des fichiers .md présents dans le dossier objets/
"""

import os
import json
from pathlib import Path

def generate_index():
    objets_dir = Path('objets')
    
    if not objets_dir.exists():
        print("❌ Le dossier 'objets' n'existe pas!")
        return
    
    # Lister tous les fichiers .md
    md_files = sorted([f.name for f in objets_dir.glob('*.md')])
    
    if not md_files:
        print("⚠️  Aucun fichier .md trouvé")
        md_files = []
    
    # Écrire le fichier index.json
    index_path = objets_dir / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(md_files, f, indent=2, ensure_ascii=False)
    
    print(f"✅ index.json généré avec {len(md_files)} fichier(s)")
    for f in md_files:
        print(f"   → {f}")

if __name__ == '__main__':
    generate_index()
