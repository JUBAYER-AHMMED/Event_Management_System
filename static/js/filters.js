function togglePanel(panelId) {
    document.getElementById('placeholderPanel').classList.add('hidden');
    document.getElementById('categoryPanel').classList.add('hidden');
    document.getElementById('datePanel').classList.add('hidden');

    document.getElementById(panelId).classList.remove('hidden');
}
