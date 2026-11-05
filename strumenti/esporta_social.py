"""Grafiche social Fulcrum: 6 post Instagram/Facebook (1080x1350), copertina Facebook, copertine delle storie in evidenza.
Chrome headless disegna l'HTML con i font del sito; i file finiscono in sito-giuseppe-napoletano/social/."""
import shutil
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCRATCH = Path(tempfile.mkdtemp(prefix="fulcrum-"))  # HTML temporanei e profilo di Chrome
PROGETTO = Path(__file__).resolve().parents[1]  # radice della repo
SOCIAL = PROGETTO / "social"
IMG_OAD = (PROGETTO / "fulcrum" / "img" / "oadfitness.jpg").as_uri()

MARCHIO = ('<svg viewBox="4 5 56 31" class="m"><rect x="7" y="13" width="50" height="7" rx="3.5" fill="currentColor" '
           'transform="rotate(-12 32 16.5)"/><circle cx="32" cy="27" r="6.5" fill="var(--ottone)"/></svg>')
ICONE = {  # tratti delle icone del sito (viewBox 24)
    "chi-siamo": None,
    "progetti": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "metodo": '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>',
    "contatti": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
}

CSS = """
:root{--carta:#f4f2ed;--bianco:#fbfaf7;--ink:#151515;--grafite:#5f5b55;--filo:#dcd7cd;--notte:#1f2c3f;--ottone:#9a7b4f}
*{box-sizing:border-box}
html,body{margin:0;width:100vw;height:100vh;overflow:hidden}
body{font-family:'Instrument Sans',sans-serif;-webkit-font-smoothing:antialiased}
p,h1,h2,ul,ol{margin:0}
.tela{width:100%;height:100%;padding:96px;display:flex;flex-direction:column}
.chiaro{background:var(--carta);color:var(--ink)}
.bianco{background:var(--bianco);color:var(--ink)}
.scuro{background:var(--ink);color:var(--carta);--ottone:#c2a272;--grafite:#a8a39a;--filo:#2e2e2e}
.testa{display:flex;align-items:center;gap:18px;font:600 42px/1 'Instrument Sans';letter-spacing:-.045em}
.testa .m{width:76px}
.piede{display:flex;justify-content:space-between;padding-top:34px;border-top:1.5px solid var(--filo);font:500 22px/1 'Instrument Sans';letter-spacing:.2em;text-transform:uppercase;color:var(--grafite)}
.serif{font-family:'Instrument Serif',serif;font-weight:400;letter-spacing:-.015em}
em{font-style:italic;color:var(--notte)} .scuro em{color:#9fb0c9}
.etichetta{font:500 24px/1 'Instrument Sans';letter-spacing:.2em;text-transform:uppercase;color:var(--ottone)}
.corpo{margin:auto 0}
.testo{font-size:34px;line-height:1.42;color:var(--grafite)}
.pill{display:inline-block;margin:0 14px 16px 0;padding:14px 28px;border:1.5px solid var(--filo);border-radius:999px;font-size:30px}
.righe{list-style:none;padding:0;margin-top:44px;border-top:1.5px solid var(--filo)}
.righe li{display:flex;gap:28px;align-items:center;padding:22px 0;border-bottom:1.5px solid var(--filo);font-size:38px}
.righe li::before{content:"";flex:none;width:22px;height:2px;background:var(--ottone)}
.passi{list-style:none;padding:0;margin-top:48px;counter-reset:p}
.passi li{counter-increment:p;display:grid;grid-template-columns:90px 1fr;padding:26px 0;border-top:1.5px solid var(--filo)}
.passi li::before{content:counter(p) ".";grid-row:span 2;font:italic 400 64px/1 'Instrument Serif';color:var(--ottone)}
.passi b{font-size:40px;font-weight:600;letter-spacing:-.01em}
.passi span{font-size:29px;line-height:1.4;color:var(--grafite)}
"""


def pagina(corpo):
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600'
            '&family=Instrument+Serif:ital@0;1&display=block">'
            f'<style>{CSS}</style></head><body>{corpo}</body></html>')


def post(classe, corpo):
    return pagina(f'<div class="tela {classe}"><div class="testa">{MARCHIO}fulcrum</div>{corpo}'
                  '<div class="piede"><span>Barletta · Puglia</span><span>Progetti digitali per le aziende</span></div></div>')


POST = {
    "post-1-presentazione": post("scuro", """<div class="corpo">
        <p class="etichetta">Team multidisciplinare per le aziende</p>
        <h1 class="serif" style="font-size:136px;line-height:.98;margin-top:30px">Il punto d'appoggio dei vostri <em>progetti</em>.</h1></div>"""),
    "post-2-archimede": post("chiaro", """<div class="corpo">
        <p class="serif" style="font-size:118px;line-height:1.02">“Datemi un punto d'appoggio e solleverò il mondo.”</p>
        <p class="etichetta" style="margin-top:40px;color:var(--grafite)">Archimede</p></div>
        <p class="testo" style="max-width:820px;margin-bottom:64px">Per un'azienda il punto d'appoggio è un progetto fatto bene. Noi lavoriamo per costruirlo.</p>"""),
    "post-3-squadra": post("bianco", """<div class="corpo">
        <h2 class="serif" style="font-size:120px;line-height:1">Un solo interlocutore. <em>Tutta la squadra.</em></h2>
        <p class="testo" style="margin:40px 0 44px;max-width:840px">Professionisti con competenze diverse sullo stesso progetto, dall'analisi alla manutenzione.</p>
        <div><span class="pill">Analisi</span><span class="pill">Design</span><span class="pill">Sviluppo software</span><span class="pill">Cloud e DevOps</span><span class="pill">Comunicazione</span></div></div>"""),
    "post-4-progetti": post("scuro", """<div class="corpo">
        <p class="etichetta">Progetti per le aziende</p>
        <h2 class="serif" style="font-size:108px;line-height:1;margin-top:26px">Che progetti <em>seguiamo</em>.</h2>
        <ul class="righe"><li>Piattaforme web e aree riservate</li><li>Gestionali e processi</li><li>Prenotazioni e agende</li>
        <li>Integrazioni tra sistemi</li><li>Infrastruttura e continuità</li><li>Identità e presenza digitale</li></ul></div>"""),
    "post-5-metodo": post("chiaro", """<div class="corpo">
        <p class="etichetta">Metodo</p>
        <h2 class="serif" style="font-size:108px;line-height:1;margin-top:26px">Come nasce un <em>progetto</em>.</h2>
        <ol class="passi">
          <li><b>Ascolto</b><span>Analizziamo obiettivi, processi e vincoli della vostra azienda.</span></li>
          <li><b>Proposta</b><span>Struttura, tempi e costi chiari, prima di iniziare.</span></li>
          <li><b>Realizzazione</b><span>Lavoriamo per fasi: vedete e provate ogni avanzamento.</span></li>
          <li><b>Continuità</b><span>Dopo il rilascio restiamo al vostro fianco.</span></li></ol></div>"""),
    "post-6-oad-fitness": post("bianco", f"""<div class="corpo">
        <p class="etichetta">Lavori realizzati</p>
        <h2 class="serif" style="font-size:108px;line-height:1;margin-top:26px">OAD <em>Fitness</em></h2>
        <p class="testo" style="margin:18px 0 40px">Piattaforma gestionale per un centro sportivo.</p>
        <img src="{IMG_OAD}" style="display:block;width:100%;border:1.5px solid var(--filo);border-radius:14px">
        <div style="margin-top:40px"><span class="pill">Area riservata iscritti</span><span class="pill">Strumenti per la direzione</span><span class="pill">Infrastruttura cloud</span></div></div>"""),
}

# Copertina Facebook 1640x856: il contenuto resta nella fascia centrale, visibile sia da computer sia da telefono
LEVA = """<svg viewBox="0 0 480 330" style="width:480px;flex:none"><line x1="20" y1="300" x2="460" y2="300" stroke="#dcd7cd" stroke-width="1.5" stroke-linecap="round"/>
<circle cx="170" cy="270" r="30" fill="#9a7b4f"/><line x1="56" y1="206.2" x2="440" y2="296.4" stroke="#151515" stroke-width="9" stroke-linecap="round"/>
<rect x="64" y="140" width="72" height="72" rx="12" fill="#fbfaf7" stroke="#151515" stroke-width="1.5" transform="rotate(13.22 100 212)"/></svg>"""
COPERTINA = pagina(f"""<div class="chiaro" style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;gap:110px;padding:0 160px">
  <div><p class="etichetta">Team multidisciplinare per le aziende</p>
  <h1 class="serif" style="font-size:104px;line-height:1;margin-top:26px;max-width:820px">Il punto d'appoggio dei vostri <em>progetti</em>.</h1></div>{LEVA}</div>""")


def evidenza(nome, tratti):
    simbolo = (MARCHIO.replace('class="m"', 'style="width:420px"') if tratti is None else
               f'<svg viewBox="0 0 24 24" style="width:300px" fill="none" stroke="#c2a272" stroke-width="1.3" '
               f'stroke-linecap="round" stroke-linejoin="round">{tratti}</svg>')
    return pagina(f'<div class="scuro" style="width:100%;height:100%;display:grid;place-items:center">{simbolo}</div>')


def disegna(nome, html, w, h, destinazione):
    sorgente = SCRATCH / f"social-{nome}.html"
    sorgente.write_text(html, encoding="utf-8")
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", f"--user-data-dir={SCRATCH / 'chrome-profilo'}",
                    "--virtual-time-budget=8000", f"--window-size={w},{h}", f"--screenshot={destinazione}", sorgente.as_uri()],
                   check=True, capture_output=True, timeout=120)
    im = Image.open(destinazione)
    assert im.size == (w, h), (destinazione, im.size)


for nome, html in POST.items():
    disegna(nome, html, 1080, 1350, SOCIAL / "post" / f"{nome}.png")
disegna("copertina", COPERTINA, 1640, 856, SOCIAL / "facebook" / "copertina-facebook.png")
for nome, tratti in ICONE.items():
    disegna(f"evidenza-{nome}", evidenza(nome, tratti), 1080, 1920, SOCIAL / "instagram" / f"evidenza-{nome}.png")
shutil.copy(PROGETTO / "fulcrum" / "icone" / "icona-social-1024.png", SOCIAL / "foto-profilo.png")
print("ok:", *sorted(p.relative_to(SOCIAL).as_posix() for p in SOCIAL.rglob("*.png")), sep="\n  ")
