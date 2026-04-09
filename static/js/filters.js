document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('rightPanel').style.display = 'none';
});

function togglePanel(panelId) {
    const rightPanel = document.getElementById('rightPanel');
    const allPanels = ['categoryPanel', 'datePanel'];

    const isOpen = rightPanel.style.display === 'block';
    const isSame = rightPanel.dataset.active === panelId;

    if (isOpen && isSame) {
        rightPanel.style.display = 'none';
        rightPanel.dataset.active = '';
        return;
    }

    allPanels.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
    });

    const target = document.getElementById(panelId);
    if (target) {
        target.style.display = 'flex';
        rightPanel.style.display = 'block';
        rightPanel.dataset.active = panelId;
    }
}

document.addEventListener('click', function (e) {
    const rightPanel = document.getElementById('rightPanel');
    const filterButtons = document.getElementById('filterButtons');
    if (!rightPanel.contains(e.target) && !filterButtons.contains(e.target)) {
        rightPanel.style.display = 'none';
        rightPanel.dataset.active = '';
    }
});

function filterCategories() {
    const searchTerm = document.getElementById('categorySearch').value.toLowerCase().trim();
    document.querySelectorAll('.category-item').forEach(function (item) {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(searchTerm) ? 'flex' : 'none';
    });
}