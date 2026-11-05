// Menu da telefono
const menuBtn = document.querySelector('.menu-btn');
const nav = document.getElementById('nav');
const setMenu = open => {
  menuBtn.setAttribute('aria-expanded', open);
  nav.classList.toggle('open', open);
  document.body.style.overflow = open ? 'hidden' : '';
};
menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
nav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });

// Ambiti di progetto: chiusi da telefono (si aprono al tocco), sempre aperti da desktop
const desktop = matchMedia('(min-width: 680px)');
const ambiti = document.querySelectorAll('.servizio');
const sistemaAmbiti = () => ambiti.forEach(s => { s.open = desktop.matches; });
desktop.addEventListener('change', sistemaAmbiti);
sistemaAmbiti();
ambiti.forEach(s => s.querySelector('summary').addEventListener('click', e => { if (desktop.matches) e.preventDefault(); }));

// Comparsa morbida degli elementi quando entrano nello schermo
const io = new IntersectionObserver(voci => voci.forEach(v => {
  if (v.isIntersecting) { v.target.classList.add('visto'); io.unobserve(v.target); }
}), { rootMargin: '0px 0px -8% 0px' });
document.querySelectorAll('.rivela').forEach(el => io.observe(el));

// Modulo progetto
// shortcut: nessun invio a un server, la richiesta parte solo via WhatsApp; collegare un backend (o Formspree) quando si va online
const WHATSAPP = '393281348501';
const form = document.getElementById('form-progetto');
const status = document.getElementById('form-status');

// "submit" scatta solo se la validazione HTML5 è passata
form.addEventListener('submit', e => {
  e.preventDefault();
  const d = new FormData(form);
  const righe = [
    `Buongiorno, sono ${d.get('nome')} di ${d.get('azienda')}.`,
    `Vorremmo parlarvi di un progetto: ${d.get('progetto')}.`,
    d.get('tempi') && `Tempi: ${d.get('tempi').toLowerCase()}.`,
    d.get('messaggio'),
    `Recapito: ${d.get('telefono')}${d.get('email') ? ` · ${d.get('email')}` : ''}`,
  ];
  status.querySelector('a').href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(righe.filter(Boolean).join('\n'))}`;
  status.hidden = false;
  status.scrollIntoView({ behavior: 'smooth', block: 'center' });
  form.querySelector('[type=submit]').textContent = 'Aggiorna richiesta';
});
