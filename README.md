# 🥑 Le Sale Garage - Site Web

Système de site web pour afficher ton catalogue d'objets à partir de tes fiches Obsidian (.md).

## 📁 Structure du projet

```
sale-garage-web/
├── index.html              # Page d'accueil (catalogue)
├── produit.html            # Template page produit (version dynamique)
├── css/
│   └── style.css           # Styles
├── js/
│   ├── app.js              # Script catalogue (version dynamique)
│   ├── produit.js          # Script produit (version dynamique)
│   └── filter.js           # Script filtres (version statique)
├── objets/                 # Tes fichiers .md d'Obsidian
│   ├── index.json          # Liste des fichiers (auto-généré)
│   └── *.md                # Tes fiches produits
├── photos/                 # Photos de tes objets
│   └── *.jpg
├── generate_static.py      # VERSION 1: Générateur statique
├── generate_index.py       # Génère index.json
└── .github/
    └── workflows/
        └── deploy.yml      # VERSION 3: GitHub Actions
```

## 🚀 Les 3 Versions

### VERSION 1: Statique (Recommandé pour débuter) ⭐

**Avantages:**
- Simple, aucun serveur nécessaire
- Fonctionne partout (double-clic sur index.html)
- Rapide à charger
- Hébergement gratuit facile (Netlify, GitHub Pages, etc.)

**Comment l'utiliser:**

1. Ajoute tes fichiers .md dans le dossier `objets/`
2. Ajoute tes photos dans le dossier `photos/`
3. Lance le générateur:
   ```bash
   python3 generate_static.py
   ```
4. Ouvre `index.html` dans ton navigateur
5. Pour mettre à jour: relance simplement le script après avoir ajouté/modifié des fiches

**Déploiement:**
- Drag & drop tout le dossier sur [Netlify Drop](https://app.netlify.com/drop)
- Ou utilise GitHub Pages (voir VERSION 3)

---

### VERSION 2: Dynamique (Serveur local)

**Avantages:**
- Pas besoin de régénérer après chaque modif
- Les .md sont lus en temps réel

**Inconvénients:**
- Nécessite un serveur web local
- Plus complexe à héberger en production

**Comment l'utiliser:**

1. Génère le fichier index.json:
   ```bash
   python3 generate_index.py
   ```

2. Lance un serveur local:
   ```bash
   # Option 1: Python
   python3 -m http.server 8000
   
   # Option 2: Node.js
   npx http-server
   ```

3. Ouvre http://localhost:8000

4. Chaque fois que tu ajoutes un .md, relance `generate_index.py`

---

### VERSION 3: GitHub Pages (Automatique) 🚀

**Avantages:**
- Totalement automatique
- Push tes .md → site mis à jour
- Hébergement gratuit
- URL personnalisable

**Comment l'utiliser:**

1. **Setup initial:**
   ```bash
   # Initialise un repo git
   git init
   git add .
   git commit -m "Initial commit"
   
   # Crée un repo sur GitHub
   # Puis:
   git remote add origin https://github.com/TON-USERNAME/sale-garage.git
   git branch -M main
   git push -u origin main
   ```

2. **Active GitHub Pages:**
   - Va sur GitHub → Settings → Pages
   - Source: GitHub Actions
   - Sauvegarde

3. **Utilisation quotidienne:**
   ```bash
   # Ajoute/modifie des fichiers .md dans objets/
   # Puis:
   git add objets/
   git commit -m "Ajout nouveaux produits"
   git push
   
   # Le site se met à jour automatiquement en 1-2 minutes!
   ```

4. **Ton site sera accessible à:**
   ```
   https://TON-USERNAME.github.io/sale-garage/
   ```

---

## 📸 Photos

Les photos doivent être nommées exactement comme dans tes fiches .md:

```markdown
## Photos
![[241207-001_vue1.jpg]]
![[241207-001_vue2.jpg]]
```

Assure-toi d'avoir ces fichiers dans le dossier `photos/`:
- `241207-001_vue1.jpg`
- `241207-001_vue2.jpg`

**Conseil:** Utilise une image `placeholder.jpg` pour les objets sans photo.

---

## 🎨 Personnalisation

### Couleurs

Édite `css/style.css` (lignes 1-7):

```css
:root {
    --primary: #2d5016;      /* Vert foncé */
    --secondary: #7fb069;    /* Vert clair */
    --accent: #e6aa68;       /* Orange */
    --dark: #1a1a1a;         /* Noir */
    --light: #f5f5f5;        /* Blanc cassé */
}
```

### Logo / Emoji

Change le 🥑 dans les fichiers HTML (index.html, ligne 12):

```html
<h1>🥑 Le Sale Garage</h1>
```

---

## 🔄 Workflow recommandé

**Pour démarrer (VERSION 1):**

1. Crée tes fiches dans Obsidian
2. Exporte-les dans `objets/`
3. Ajoute les photos dans `photos/`
4. Lance `python3 generate_static.py`
5. Upload sur Netlify

**Quand tu as beaucoup d'objets (VERSION 3):**

1. Setup GitHub Pages
2. Travaille dans Obsidian
3. Copie les nouveaux .md dans `objets/`
4. `git add . && git commit -m "Nouveaux produits" && git push`
5. Attends 2 minutes → site à jour!

---

## 🐛 Problèmes courants

**Les photos ne s'affichent pas:**
- Vérifie que le nom dans le .md correspond exactement au nom du fichier
- Les noms sont sensibles à la casse (majuscules/minuscules)

**Le site ne se met pas à jour (GitHub Pages):**
- Va sur GitHub → Actions → vérifie le workflow
- Attends 2-3 minutes après le push

**Erreur "No module named...":**
- Tu es sûr d'avoir Python 3 installé? Lance `python3 --version`

---

## 📝 Tips

1. **Développe en local avec VERSION 1**, déploie avec VERSION 3 quand tu es prêt
2. **Optimise tes photos** avant de les uploader (max 1000px de large)
3. **Backup ton dossier objets/** régulièrement
4. Utilise le même template pour toutes tes fiches = cohérence

---

## 🆘 Besoin d'aide?

Ouvre un issue sur GitHub ou contacte-moi!

Bon courage avec Le Sale Garage! 🥑✨
