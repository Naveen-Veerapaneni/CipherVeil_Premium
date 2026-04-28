/* CipherVeil — Theme Manager */
(function () {
  const KEY = 'cv-theme';

  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem(KEY, t);
  }

  // Restore on load — runs before first paint
  const saved = localStorage.getItem(KEY) || 'dark';
  applyTheme(saved);

  window.toggleTheme = function () {
    const current = document.documentElement.getAttribute('data-theme');
    applyTheme(current === 'dark' ? 'light' : 'dark');
  };
})();
