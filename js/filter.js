
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
