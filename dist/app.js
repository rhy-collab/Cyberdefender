'use strict';
document.getElementById('contact-button').addEventListener('click', () => {
  const note = document.getElementById('contact-note');
  note.hidden = false;
  note.scrollIntoView({behavior: 'smooth', block: 'nearest'});
});
