// Utiliser les mêmes fonctions de parsing que app.js
function parseYAML(yaml) {
    const lines = yaml.split('\n');
    const data = {};
    
    lines.forEach(line => {
        if (line.trim() === '' || line.trim() === '---') return;
        
        const match = line.match(/^([^:]+):\s*(.*)$/);
        if (match) {
            let key = match[1].trim();
            let value = match[2].trim();
            
            if (value.startsWith('[') && value.endsWith(']')) {
                value = value.slice(1, -1).split(',').map(v => v.trim());
            }
            else if (value === 'true') value = true;
            else if (value === 'false') value = false;
            else if (!isNaN(value) && value !== '') {
                value = parseFloat(value);
            }
            else if ((value.startsWith('"') && value.endsWith('"')) || 
                     (value.startsWith("'") && value.endsWith("'"))) {
                value = value.slice(1, -1);
            }
            
            data[key] = value;
        }
    });
    
    return data;
}

function parseMarkdown(content) {
    const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
    
    if (!yamlMatch) {
        console.error('Pas de YAML front matter trouvé');
        return null;
    }
    
    const yaml = yamlMatch[1];
    const markdown = content.slice(yamlMatch[0].length).trim();
    
    const data = parseYAML(yaml);
    
    const sections = {};
    const sectionRegex = /##\s+(.+?)\n([\s\S]*?)(?=\n##\s+|$)/g;
    let match;
    
    while ((match = sectionRegex.exec(markdown)) !== null) {
        const title = match[1].trim();
        const content = match[2].trim();
        sections[title] = content;
    }
    
    const images = [];
    const imageRegex = /!\[\[([^\]]+)\]\]/g;
    while ((match = imageRegex.exec(markdown)) !== null) {
        images.push(match[1]);
    }
    
    data.sections = sections;
    data.images = images;
    data.title = markdown.match(/^#\s+(.+)/m)?.[1] || 'Sans titre';
    
    return data;
}

// Charger et afficher le produit
async function loadProduit() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    if (!productId) {
        document.getElementById('loading').textContent = 'Aucun produit spécifié';
        return;
    }
    
    try {
        const response = await fetch(`objets/${productId}.md`);
        if (!response.ok) throw new Error('Produit non trouvé');
        
        const content = await response.text();
        const produit = parseMarkdown(content);
        
        displayProduit(produit);
        document.getElementById('loading').style.display = 'none';
        
    } catch (error) {
        console.error('Erreur:', error);
        document.getElementById('loading').textContent = 'Produit introuvable';
    }
}

function displayProduit(produit) {
    // Mettre à jour le titre de la page
    document.getElementById('page-title').textContent = `${produit.title} - Le Sale Garage`;
    
    const container = document.getElementById('produit-detail');
    const tags = Array.isArray(produit.tags) ? produit.tags : [];
    
    // Générer les miniatures
    const thumbsHTML = produit.images.map((img, index) => 
        `<img src="photos/${img}" alt="${produit.title} ${index + 1}" 
              class="thumb ${index === 0 ? 'active' : ''}" 
              onclick="changeMainImage('photos/${img}', this)"
              onerror="this.src='photos/placeholder.jpg'">`
    ).join('');
    
    // Parser la description commerciale
    const description = produit.sections['Description commerciale'] || 'Aucune description disponible';
    
    // Parser les dimensions
    const dimensions = produit.sections['Dimensions'] || '';
    
    container.innerHTML = `
        <div class="produit-detail-container">
            <div class="produit-images">
                <img id="main-image" 
                     src="photos/${produit.images[0] || 'placeholder.jpg'}" 
                     alt="${produit.title}" 
                     class="produit-image-main"
                     onerror="this.src='photos/placeholder.jpg'">
                <div class="produit-image-thumbs">
                    ${thumbsHTML}
                </div>
            </div>
            
            <div class="produit-info">
                <div class="produit-id">#${produit.id}</div>
                <h2>${produit.title}</h2>
                
                <div class="produit-tags">
                    ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
                
                <div class="info-section">
                    <h3>Prix</h3>
                    <div class="produit-prix">${produit.prix_vente_souhaité}€</div>
                    <span class="produit-statut statut-${produit.statut}">
                        ${produit.statut.replace('_', ' ')}
                    </span>
                </div>
                
                <div class="info-section">
                    <h3>Description</h3>
                    <p>${description}</p>
                </div>
                
                ${dimensions ? `
                <div class="info-section">
                    <h3>Dimensions</h3>
                    <div style="white-space: pre-line;">${dimensions}</div>
                </div>
                ` : ''}
                
                <div class="info-section">
                    <h3>Informations</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">Catégorie</span>
                            <span class="info-value">${produit.catégorie || 'Non spécifié'}</span>
                        </div>
                        ${produit.sous_catégorie ? `
                        <div class="info-item">
                            <span class="info-label">Type</span>
                            <span class="info-value">${produit.sous_catégorie}</span>
                        </div>
                        ` : ''}
                        <div class="info-item">
                            <span class="info-label">Acquisition</span>
                            <span class="info-value">${produit.date_acquisition || 'N/A'}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Lieu</span>
                            <span class="info-value">${produit.lieu_acquisition || 'N/A'}</span>
                        </div>
                    </div>
                </div>
                
                ${produit.sections['État'] ? `
                <div class="info-section">
                    <h3>État</h3>
                    <div style="white-space: pre-line;">${produit.sections['État']}</div>
                </div>
                ` : ''}
                
                ${produit.sections['Notes perso'] ? `
                <div class="info-section">
                    <h3>Histoire de l'objet</h3>
                    <p>${produit.sections['Notes perso']}</p>
                </div>
                ` : ''}
            </div>
        </div>
    `;
}

// Changer l'image principale
function changeMainImage(src, thumbElement) {
    document.getElementById('main-image').src = src;
    
    // Mettre à jour les classes active
    document.querySelectorAll('.thumb').forEach(thumb => {
        thumb.classList.remove('active');
    });
    thumbElement.classList.add('active');
}

// Charger le produit au chargement de la page
document.addEventListener('DOMContentLoaded', loadProduit);
