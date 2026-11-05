"""Esporta in PNG il marchio Fulcrum: icone (favicon, Apple, Android, social) e loghi su fondo trasparente.
Chrome headless disegna l'SVG/HTML a 1024 px, Pillow ritaglia e ridimensiona."""
import subprocess
import tempfile
import sys
from pathlib import Path
from PIL import Image

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCRATCH = Path(tempfile.mkdtemp(prefix="fulcrum-"))  # HTML temporanei e profilo di Chrome
PROGETTO = Path(__file__).resolve().parents[1]  # radice della repo
ICONE = PROGETTO / "fulcrum" / "icone"
LOGHI = PROGETTO / "logo" / "fulcrum"
INK, CARTA, OTTONE, ORO = "#151515", "#f4f2ed", "#9a7b4f", "#c2a272"


def marchio(colore, accento):
    return (f'<rect x="7" y="13" width="50" height="7" rx="3.5" fill="{colore}" transform="rotate(-12 32 16.5)"/>'
            f'<circle cx="32" cy="27" r="6.5" fill="{accento}"/>')


def icona(rx, scala):
    # marchio centrato: il suo centro geometrico è (32, 20.69)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">'
            f'<rect width="100" height="100" rx="{rx}" fill="{INK}"/>'
            f'<g transform="translate(50 50) scale({scala}) translate(-32 -20.69)">{marchio(CARTA, ORO)}</g></svg>')


def pagina(corpo):
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600&display=block">'
            '<style>html,body{margin:0;width:100vw;height:100vh;overflow:hidden;background:transparent}'
            'body{display:flex;align-items:center;justify-content:center;gap:60px}</style></head>'
            f'<body>{corpo}</body></html>')


def logo_orizzontale(colore, accento):
    return pagina(f'<svg viewBox="4 5 56 31" style="width:330px;height:auto">{marchio(colore, accento)}</svg>'
                  f'<span style="font:600 270px/1 \'Instrument Sans\';letter-spacing:-.045em;color:{colore};'
                  f'transform:translateY(-10px)">fulcrum</span>')


def disegna(nome, html, w, h):
    sorgente = SCRATCH / f"{nome}.html"
    sorgente.write_text(html, encoding="utf-8")
    uscita = SCRATCH / f"{nome}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--default-background-color=00000000",
                    f"--user-data-dir={SCRATCH / 'chrome-profilo'}", "--virtual-time-budget=8000",
                    f"--window-size={w},{h}", f"--screenshot={uscita}", sorgente.as_uri()],
                   check=True, capture_output=True, timeout=120)
    return Image.open(uscita).convert("RGBA")


def ritaglia(img, margine=0.04):
    box = img.getbbox()
    assert box, "immagine vuota: il rendering non ha prodotto nulla"
    ritaglio = img.crop(box)
    m = round(max(ritaglio.size) * margine)
    tela = Image.new("RGBA", (ritaglio.width + 2 * m, ritaglio.height + 2 * m), (0, 0, 0, 0))
    tela.paste(ritaglio, (m, m))
    return tela


def larghezza(img, w):
    return img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)


ICONE.mkdir(parents=True, exist_ok=True)
LOGHI.mkdir(parents=True, exist_ok=True)

# Icone: arrotondate per le favicon; a tutto quadrato per Apple, Android e social (sono le piattaforme ad arrotondarle)
arrotondata = disegna("icona-arrotondata", pagina(icona(22, 1.45)), 1024, 1024)
piena = disegna("icona-piena", pagina(icona(0, 1.15)), 1024, 1024)
uscite = {
    ICONE / "favicon-16.png": (arrotondata, 16),
    ICONE / "favicon-32.png": (arrotondata, 32),
    ICONE / "favicon-48.png": (arrotondata, 48),
    ICONE / "apple-touch-icon.png": (piena, 180),
    ICONE / "icon-192.png": (piena, 192),
    ICONE / "icon-512.png": (piena, 512),
    ICONE / "icona-social-1024.png": (piena, 1024),
}
for percorso, (img, lato) in uscite.items():
    img.resize((lato, lato), Image.LANCZOS).save(percorso, optimize=True)
arrotondata.resize((48, 48), Image.LANCZOS).save(PROGETTO / "fulcrum" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# Loghi su fondo trasparente
loghi = {
    "marchio.png": disegna("marchio", pagina(f'<svg viewBox="4 5 56 31" style="width:1400px">{marchio(INK, OTTONE)}</svg>'), 1600, 1000),
    "marchio-chiaro.png": disegna("marchio-chiaro", pagina(f'<svg viewBox="4 5 56 31" style="width:1400px">{marchio(CARTA, ORO)}</svg>'), 1600, 1000),
    "logo-orizzontale.png": disegna("logo", logo_orizzontale(INK, OTTONE), 2000, 600),
    "logo-orizzontale-chiaro.png": disegna("logo-chiaro", logo_orizzontale(CARTA, ORO), 2000, 600),
}
for nome, img in loghi.items():
    larghezza(ritaglia(img), 1200).save(LOGHI / nome, optimize=True)

# Controlli: dimensioni giuste, angoli trasparenti dove devono esserlo, icone piene senza trasparenza
for percorso, (_, lato) in uscite.items():
    im = Image.open(percorso)
    assert im.size == (lato, lato), percorso
    angolo = im.convert("RGBA").getpixel((0, 0))[3]
    assert (angolo == 0) if "favicon" in percorso.name else (angolo == 255), (percorso, angolo)
for nome in loghi:
    im = Image.open(LOGHI / nome).convert("RGBA")
    assert im.width == 1200 and im.getpixel((0, 0))[3] == 0, nome
print("ok:", *[p.name for p in uscite], "favicon.ico", *loghi, sep="\n  ")
