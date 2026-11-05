# Fulcrum · sito web

Sito vetrina di **Fulcrum**, team multidisciplinare per i progetti digitali delle aziende (Barletta, Italia).
HTML, CSS e JavaScript senza framework né build: si pubblica così com'è su qualsiasi hosting statico con HTTPS.

## Struttura

| Percorso | Contenuto |
|---|---|
| `index.html` | La pagina, con meta SEO e dati strutturati `LocalBusiness` |
| `style.css` | Stile, mobile-first |
| `main.js` | Menu da telefono, schede a fisarmonica, comparsa allo scorrimento, modulo |
| `favicon.svg`, `favicon.ico`, `icone/` | Icone per browser, Apple, Android e social |
| `site.webmanifest` | Icone per la schermata Home di Android |
| `img/` | Schermate del progetto OAD Fitness |

## Anteprima in locale

```bash
python -m http.server 8080
```

Poi apri http://localhost:8080

## Prima della messa online

- Sostituire `[DOMINIO]` in `index.html` (canonical, Open Graph, dati strutturati) con il dominio definitivo.
- Creare la pagina della privacy policy e collegarla ai link `href="#"`.
- Il modulo non invia nulla a un server: prepara un messaggio WhatsApp per il 328 134 8501. Per ricevere le richieste anche via email serve un backend o un servizio come Formspree (vedi il commento `shortcut:` in `main.js`).
- I font arrivano da Google Fonts: per il GDPR conviene ospitarli insieme al sito.
