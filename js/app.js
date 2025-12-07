// Parser de YAML Front Matter
function parseYAML(yaml) {
    const lines = yaml.split('\n');
    const data = {};
    
    lines.forEach(line => {
        if (line.trim() === '' || line.trim() === '---') return;
        
        const match = line.match(/^([^:]+):\s*(.*)$/);
        if (match) {
            let key = match[1].trim();
            let value = match[2].trim();
            
            // Gérer les tableaux
            if (value.startsWith('[') && value.endsWith(']')) {
                value = value.slice(1, -1).split(',').map(v => v.trim());
            }
            // Gérer les booléens
            else if (value === 'true') value = true;
            else if (value === 'false') value = false;
            // Gérer les nombres
            else if (!isNaN(value) && value !== '') {
                value = parseFloat(value);
            }
            // Retirer les guillemets
            else if ((value.startsWith('"') && value.endsWith('"')) || 
                     (value.startsWith("'") && value.endsWith("'"))) {
                value = value.slice(1, -1);
            }
            
            data[key] = value;
        }
    });
    
    return data;
}

// Parser de fichier Markdown
function parseMarkdown(content) {
    const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
    
    if (!yamlMatch) {
        console.error('Pas de YAML front matter trouvé');
        return null;
    }
    
    const yaml = yamlMatch[1];
    const markdown = content.slice(yamlMatch[0].length).trim();
    
    const data = parseYAML(yaml);
    
    // Parser les sections markdown
    const sections = {};
    const sectionRegex = /##\s+(.+?)\n([\s\S]*?)(?=\n##\s+|$)/g;
    let match;
    
    while ((match = sectionRegex.exec(markdown)) !== null) {
        const title = match[1].trim();
        const content = match[2].trim();
        sections[title] = content;
    }
    
    // Extraire les images
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

// État de l'application
let allProduits = [];
let currentFilter = 'tous';

// Charger tous les produits
async function loadProduits() {
    try {
        // En production, tu devras générer un index.json avec la liste de tes fichiers
        const response = await fetch('objets/index.json');
        const fileList = await response.json();
        
        const promises = fileList.map(async (filename) => {
            const res = await fetch(`objets/${filename}`);
            const content = await res.text();
            const data = parseMarkdown(content);
            return data;
        });
        
        allProduits = await Promise.all(promises);
        displayProduits();
        updateStats();
        
        document.getElementById('loading').style.display = 'none';
    } catch (error) {
        console.error('Erreur lors du chargement:', error);
        document.getElementById('loading').textContent = 
            'Erreur de chargement. Assure-toi d\'avoir un fichier objets/index.json';
    }
}

// Afficher les produits
function displayProduits() {
    const catalogue = document.getElementById('catalogue');
    
    let produits = allProduits;
    if (currentFilter !== 'tous') {
        produits = allProduits.filter(p => p.catégorie === currentFilter);
    }
    
    if (produits.length === 0) {
        catalogue.innerHTML = '';
        document.getElementById('no-results').style.display = 'block';
        return;
    }
    
    document.getElementById('no-results').style.display = 'none';
    
    catalogue.innerHTML = produits.map(produit => {
        const firstImage = produit.images[0] || 'placeholder.jpg';
        const tags = Array.isArray(produit.tags) ? produit.tags : [];
        
        return `
            <a href="produit.html?id=${produit.id}" class="produit-card">
                <img src="photos/${firstImage}" alt="${produit.title}" onerror="this.src='photos/placeholder.jpg'">
                <div class="produit-card-content">
                    <div class="produit-id">#${produit.id}</div>
                    <h3>${produit.title}</h3>
                    <div class="produit-tags">
                        ${tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}
                    </div>
                    <div class="produit-prix">${produit.prix_vente_souhaité}€</div>
                    <span class="produit-statut statut-${produit.statut}">${produit.statut.replace('_', ' ')}</span>
                </div>
            </a>
        `;
    }).join('');
}

// Mettre à jour les stats
function updateStats() {
    const total = allProduits.length;
    const enStock = allProduits.filter(p => p.statut === 'en_stock').length;
    
    document.getElementById('total-objets').textContent = `${total} objet${total > 1 ? 's' : ''}`;
    document.getElementById('en-stock').textContent = `${enStock} en stock`;
}

// Gestion des filtres
document.addEventListener('DOMContentLoaded', () => {
    // Charger les produits
    loadProduits();
    
    // Event listeners pour les filtres
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            displayProduits();
        });
    });
});
