(function() {
    const toggleDarkMode = (isDark) => {
        document.querySelectorAll('.d2-figure').forEach(el => {
            el.classList.toggle('d2-dark-mode', isDark);
        });
    };
    const darkModeMql = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
    if (darkModeMql) {
        toggleDarkMode(darkModeMql.matches);
        darkModeMql.addEventListener('change', e => toggleDarkMode(e.matches));
    }
})();
