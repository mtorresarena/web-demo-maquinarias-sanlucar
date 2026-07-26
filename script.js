(() => {
  const header = document.querySelector('[data-header]');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#nav');
  const year = document.querySelector('[data-year]');

  const updateHeader = () => header?.classList.toggle('scrolled', window.scrollY > 24);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav?.setAttribute('data-open', String(open));
    header?.classList.toggle('open', open);
    toggle.querySelector('.sr-only').textContent = open ? 'Cerrar menú' : 'Abrir menú';
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
      toggle.setAttribute('aria-expanded', 'false');
      nav?.setAttribute('data-open', 'false');
      header?.classList.remove('open');
      toggle.focus();
    }
  });

  nav?.addEventListener('click', event => {
    if (event.target.closest('a')) {
      toggle?.setAttribute('aria-expanded', 'false');
      nav.setAttribute('data-open', 'false');
      header?.classList.remove('open');
    }
  });

  if (year) year.textContent = new Date().getFullYear();
})();
