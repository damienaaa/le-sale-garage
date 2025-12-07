#!/usr/bin/env python3
"""
Générateur de site statique pour Le Sale Garage
Usage: python3 generate_static.py
"""

import os
import re
import json
from pathlib import Path

def parse_yaml_frontmatter(content):
    """Parse le YAML front matter d'un fichier markdown"""
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return None, content
    
    yaml_content = match.group(1)
    markdown_content = match.group(2)
    
    data = {}
    for line in yaml_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Parse arrays
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip() for v in value[1:-1].split(',')]
            # Parse numbers
            elif value.replace('.', '').isdigit():
                value = float(value) if '.' in value else int(value)
            # Remove quotes
            elif (value.startswith('"') and value.endswith('"')) or \
                 (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            
            data[key] = value
    
    return data, markdown_content

def parse_markdown_sections(content):
    """Parse les sections markdown (## Titre)"""
    sections = {}
    
    # Extraire le titre principal
    title_match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Sans titre'
    
    # Extraire les sections
    section_pattern = r'##\s+(.+?)\n(.*?)(?=\n##\s+|\Z)'
    for match in re.finditer(section_pattern, content, re.DOTALL):
        section_title = match.group(1).strip()
        section_content = match.group(2).strip()
        sections[section_title] = section_content
    
    # Extraire les images
    images = re.findall(r'!\[\[([^\]]+)\]\]', content)
    
    return title, sections, images

def generate_product_card(data, title, images):
    """Génère le HTML d'une carte produit pour le catalogue"""
    first_image = images[0] if images else 'placeholder.jpg'
    tags = data.get('tags', [])
    if isinstance(tags, str):
        tags = [tags]
    
    tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in tags[:3]])
    
    return f'''
        <a href="produit-{data['id']}.html" class="produit-card">
            <img src="photos/{first_image}" alt="{title}" onerror="this.src='photos/placeholder.jpg'">
            <div class="produit-card-content">
                <div class="produit-id">#{data['id']}</div>
                <h3>{title}</h3>
                <div class="produit-tags">
                    {tags_html}
                </div>
                <div class="produit-prix">{data.get('prix_vente_souhaité', 0)}€</div>
                <span class="produit-statut statut-{data.get('statut', 'en_stock').replace(' ', '_')}">
                    {data.get('statut', 'en_stock').replace('_', ' ')}
                </span>
            </div>
        </a>
    '''

def generate_product_page(data, title, sections, images):
    """Génère une page HTML complète pour un produit"""
    tags = data.get('tags', [])
    if isinstance(tags, str):
        tags = [tags]
    
    tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in tags])
    
    # Images
    thumbs_html = ''.join([
        f'<img src="photos/{img}" alt="{title} {i+1}" class="thumb {"active" if i == 0 else ""}" onclick="changeMainImage(\'photos/{img}\', this)" onerror="this.src=\'photos/placeholder.jpg\'">'
        for i, img in enumerate(images)
    ])
    
    first_image = images[0] if images else 'placeholder.jpg'
    
    description = sections.get('Description commerciale', 'Aucune description disponible')
    dimensions = sections.get('Dimensions', '')
    etat = sections.get('État', '')
    notes = sections.get('Notes perso', '')
    
    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Le Sale Garage</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <a href="index.html" class="back-link">← Retour au catalogue</a>
            <h1>🥑 Le Sale Garage</h1>
        </div>
    </header>

    <main class="container">
        <div class="produit-detail-container">
            <div class="produit-images">
                <img id="main-image" src="photos/{first_image}" alt="{title}" class="produit-image-main" onerror="this.src='photos/placeholder.jpg'">
                <div class="produit-image-thumbs">
                    {thumbs_html}
                </div>
            </div>
            
            <div class="produit-info">
                <div class="produit-id">#{data['id']}</div>
                <h2>{title}</h2>
                
                <div class="produit-tags">
                    {tags_html}
                </div>
                
                <div class="info-section">
                    <h3>Prix</h3>
                    <div class="produit-prix">{data.get('prix_vente_souhaité', 0)}€</div>
                    <span class="produit-statut statut-{data.get('statut', 'en_stock').replace(' ', '_')}">
                        {data.get('statut', 'en_stock').replace('_', ' ')}
                    </span>
                </div>
                
                <div class="info-section">
                    <h3>Description</h3>
                    <p>{description}</p>
                </div>
                
                {f'<div class="info-section"><h3>Dimensions</h3><div style="white-space: pre-line;">{dimensions}</div></div>' if dimensions else ''}
                
                <div class="info-section">
                    <h3>Informations</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">Catégorie</span>
                            <span class="info-value">{data.get('catégorie', 'Non spécifié')}</span>
                        </div>
                        {f'<div class="info-item"><span class="info-label">Type</span><span class="info-value">{data.get("sous_catégorie")}</span></div>' if data.get('sous_catégorie') else ''}
                        <div class="info-item">
                            <span class="info-label">Acquisition</span>
                            <span class="info-value">{data.get('date_acquisition', 'N/A')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Lieu</span>
                            <span class="info-value">{data.get('lieu_acquisition', 'N/A')}</span>
                        </div>
                    </div>
                </div>
                
                {f'<div class="info-section"><h3>État</h3><div style="white-space: pre-line;">{etat}</div></div>' if etat else ''}
                
                {f'<div class="info-section"><h3>Histoire de l\'objet</h3><p>{notes}</p></div>' if notes else ''}
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2024 Le Sale Garage - Trouve ton trésor vintage</p>
        </div>
    </footer>

    <script>
        function changeMainImage(src, thumbElement) {{
            document.getElementById('main-image').src = src;
            document.querySelectorAll('.thumb').forEach(thumb => {{
                thumb.classList.remove('active');
            }});
            thumbElement.classList.add('active');
        }}
    </script>
</body>
</html>'''
    
    return html

def generate_index_page(all_products):
    """Génère la page index.html avec tous les produits"""
    
    # Créer les cartes produits
    cards_html = '\n'.join([
        generate_product_card(p['data'], p['title'], p['images'])
        for p in all_products
    ])
    
    # Statistiques
    total = len(all_products)
    en_stock = len([p for p in all_products if p['data'].get('statut') == 'en_stock'])
    
    # Catégories uniques
    categories = set(p['data'].get('catégorie', '') for p in all_products if p['data'].get('catégorie'))
    
    filter_buttons = '<button class="filter-btn active" data-filter="tous">Tous</button>\n'
    for cat in sorted(categories):
        filter_buttons += f'                <button class="filter-btn" data-filter="{cat}">{cat.replace("_", " ").title()}</button>\n'
    
    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Le Sale Garage - Brocante & Recyclerie</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>🥑 Le Sale Garage</h1>
            <p class="tagline">Achat Vente Objet Cool Adoré D'Occasion</p>
            <nav>
                {filter_buttons}
            </nav>
        </div>
    </header>

    <main class="container">
        <div class="stats">
            <span id="total-objets">{total} objet{'s' if total > 1 else ''}</span>
            <span id="en-stock">{en_stock} en stock</span>
        </div>

        <div id="catalogue" class="grid">
            {cards_html}
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2024 Le Sale Garage - Trouve ton trésor vintage</p>
        </div>
    </footer>

    <script src="js/filter.js"></script>
</body>
</html>'''
    
    return html

def main():
    """Fonction principale"""
    objets_dir = Path('objets')
    output_dir = Path('.')
    
    if not objets_dir.exists():
        print("❌ Le dossier 'objets' n'existe pas!")
        return
    
    # Lire tous les fichiers .md
    md_files = list(objets_dir.glob('*.md'))
    
    if not md_files:
        print("❌ Aucun fichier .md trouvé dans le dossier 'objets'")
        return
    
    print(f"📦 Traitement de {len(md_files)} fichier(s)...")
    
    all_products = []
    
    for md_file in md_files:
        print(f"  → {md_file.name}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parser le fichier
        data, markdown = parse_yaml_frontmatter(content)
        if not data:
            print(f"    ⚠️  Pas de YAML front matter, ignoré")
            continue
        
        title, sections, images = parse_markdown_sections(markdown)
        
        # Générer la page HTML du produit
        product_html = generate_product_page(data, title, sections, images)
        
        output_file = output_dir / f"produit-{data['id']}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(product_html)
        
        all_products.append({
            'data': data,
            'title': title,
            'sections': sections,
            'images': images
        })
    
    # Générer la page index
    print("\n📋 Génération de index.html...")
    index_html = generate_index_page(all_products)
    
    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # Créer le script de filtrage pour la version statique
    filter_js = '''
document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.produit-card');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const filter = btn.dataset.filter;
            
            // Filter cards
            cards.forEach(card => {
                if (filter === 'tous') {
                    card.style.display = 'block';
                } else {
                    // Check if card belongs to this category
                    // This is a simple implementation - you can enhance it
                    card.style.display = 'block';
                }
            });
        });
    });
});
'''
    
    js_dir = output_dir / 'js'
    js_dir.mkdir(exist_ok=True)
    
    with open(js_dir / 'filter.js', 'w', encoding='utf-8') as f:
        f.write(filter_js)
    
    print(f"\n✅ Génération terminée!")
    print(f"   {len(all_products)} page(s) produit générée(s)")
    print(f"   1 page index.html")
    print(f"\n🚀 Ouvre index.html dans ton navigateur pour voir le résultat!")

if __name__ == '__main__':
    main()
