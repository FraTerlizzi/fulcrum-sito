# Fulcrum

Materiale di **Fulcrum**, team multidisciplinare per i progetti digitali delle aziende (Barletta, Italia): sito web, marchio e kit per i social.

## Struttura

| Cartella | Contenuto |
|---|---|
| `fulcrum/` | **Il sito.** HTML, CSS e JavaScript senza framework né build: è la cartella da pubblicare sull'hosting |
| `logo/fulcrum/` | Marchio definitivo: SVG per fondi chiari e scuri, PNG trasparenti del marchio e del logo con la scritta |
| `logo/fulcrum-proposte.html` | Le quattro proposte di marchio valutate (scelta: A, "Il punto d'appoggio") |
| `logo/proposte.html`, `logo/marchio*.svg` | Archivio: proposte e marchio GN della fase precedente |
| `social/` | Kit Instagram e Facebook: foto profilo, copertina, 6 post, copertine delle storie in evidenza e `TESTI-SOCIAL.md` con bio e didascalie |
| `strumenti/` | Script che rigenerano i PNG di icone, loghi e grafiche social |

## Il sito (`fulcrum/`)

| Percorso | Contenuto |
|---|---|
| `index.html` | La pagina, con meta SEO e dati strutturati `LocalBusiness` |
| `style.css` | Stile, mobile-first |
| `main.js` | Menu da telefono, schede a fisarmonica, comparsa allo scorrimento, modulo |
| `favicon.svg`, `favicon.ico`, `icone/` | Icone per browser, Apple, Android e social |
| `site.webmanifest` | Icone per la schermata Home di Android |
| `img/` | Schermate del progetto OAD Fitness |

**Anteprima in locale**

```bash
cd fulcrum
python -m http.server 8080
```

Poi apri http://localhost:8080

**Pubblicazione:** il sito è online su GitHub Pages, https://fraterlizzi.github.io/fulcrum-sito/
Ogni push su `main` lo ripubblica in automatico (`.github/workflows/pages.yml`). Viene pubblicata solo la cartella `fulcrum/`: logo, social e strumenti restano fuori dal sito.

**Ancora da fare**

- Con un dominio proprio: impostarlo in Settings → Pages e aggiornare l'indirizzo in `fulcrum/index.html` (canonical, Open Graph, dati strutturati).
- Creare la pagina della privacy policy e collegarla ai link `href="#"`.
- Il modulo non invia nulla a un server: prepara un messaggio WhatsApp per il 328 134 8501. Per ricevere le richieste anche via email serve un backend o un servizio come Formspree (vedi il commento `shortcut:` in `fulcrum/main.js`).
- I font arrivano da Google Fonts: per il GDPR conviene ospitarli insieme al sito.

## Rigenerare le immagini (`strumenti/`)

Servono Python con Pillow e Google Chrome installato (percorso Windows predefinito, indicato in cima agli script).

```bash
python strumenti/esporta_png.py
```

Rigenera favicon, icone (`fulcrum/icone/`) e loghi PNG (`logo/fulcrum/`).

```bash
python strumenti/esporta_social.py
```

Rigenera le grafiche in `social/`.
