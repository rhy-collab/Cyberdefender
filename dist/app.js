'use strict';
const toggle = document.querySelector('.menu-toggle');
const nav = document.getElementById('main-nav');
function closeMenu() { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); toggle.focus(); } });
document.getElementById('contact-button').addEventListener('click', event => {
  const note = document.getElementById('contact-note');
  note.hidden = false;
  event.currentTarget.setAttribute('aria-expanded', 'true');
  note.scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'nearest'});
});
