'use strict';
const toggle=document.querySelector('.menu-toggle'),nav=document.getElementById('main-nav');
if(toggle&&nav){const close=()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false')};toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){close();toggle.focus()}})}
