document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('dark-mode-toggle');
  const body = document.body;

  function updateIcon() {
    if (!toggle) return;
    if (body.classList.contains('dark-mode')) {
      toggle.classList.remove('fa-moon');
      toggle.classList.add('fa-sun');
    } else {
      toggle.classList.remove('fa-sun');
      toggle.classList.add('fa-moon');
    }
  }

  function applyPreference() {
    // Mode sombre par défaut
    if (localStorage.getItem('darkMode') === null) {
      localStorage.setItem('darkMode', 'true');
    }
    if (localStorage.getItem('darkMode') !== 'false') {
      body.classList.add('dark-mode');
    } else {
      body.classList.remove('dark-mode');
    }
    updateIcon();
  }

  applyPreference();

  if (toggle) {
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      body.classList.toggle('dark-mode');
      localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
      updateIcon();
    });
  }
});
