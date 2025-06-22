document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('dark-mode-toggle');
  const body = document.body;

  function applyPreference() {
    if (localStorage.getItem('darkMode') === 'true') {
      body.classList.add('dark-mode');
    } else {
      body.classList.remove('dark-mode');
    }
  }

  applyPreference();

  if (toggle) {
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      body.classList.toggle('dark-mode');
      localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
    });
  }
});
