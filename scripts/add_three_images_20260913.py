from pathlib import Path
import base64

ROOT = Path('.')
SRC = ROOT / 'site-full-update-20260913.html'
DIST = ROOT / 'dist'
ASSETS = DIST / 'assets'
B64 = ROOT / 'assets_b64'
DIST.mkdir(exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

files = {
    'a7-temna-elfka.webp': B64 / 'a7-temna-elfka.b64',
    'a7-elfka.webp': B64 / 'a7-elfka.b64',
    'nii-black-profile.webp': B64 / 'nii-black-profile.b64',
}
for name, src in files.items():
    raw = ''.join(src.read_text(encoding='utf-8').split())
    raw += '=' * (-len(raw) % 4)
    data = base64.b64decode(raw)
    (ASSETS / name).write_bytes(data)
    print('ASSET', name, len(data))

html = SRC.read_text(encoding='utf-8')

intro_old = 'Do terminálu byly doplněny další vizuální karty: symbolické znaky, pozemní hlídkový profil a experimentální letecký stroj.'
intro_new = 'Do terminálu byly doplněny další vizuální karty: symbolické znaky, pozemní hlídkový profil, experimentální letecký stroj a tři nové personální obrazové záznamy.'
html = html.replace(intro_old, intro_new, 1)

cards = '''
<div class="grid">
<article class="card full hero-card">
<div class="hero-copy">
<span class="label green">A7 // temný elf</span>
<h3>Temná elfka v velitelské výstroji</h3>
<p>Obrazový záznam zachycuje modrokůžou temnou elfku s dlouhými špičatými ušima ve fialové výstroji se žlutými pancéřovými prvky a emblémy KN. Vizuál odpovídá dříve popsané velitelské, vývojové nebo testovací roli v registru A7.</p>
<div class="badges"><span class="badge o">A7</span><span class="badge">Temný Elf</span><span class="badge">fialová výstroj</span><span class="badge">žluté prvky</span></div>
</div>
<div class="media lightbox"><img src="/assets/a7-temna-elfka.webp" alt="Temná elfka ve fialové výstroji se žlutými prvky" loading="lazy"><span class="caption">A7 // TEMNÁ ELFKA</span></div>
</article>
<article class="card full hero-card">
<div class="hero-copy">
<span class="label green">A7 // elf</span>
<h3>Elfka v průzkumné výstroji</h3>
<p>Archivní karta ukazuje světlovlasou elfku s dlouhými špičatými ušima, brýlemi a fialovou výstrojí. Záznam vizuálně zapadá do průzkumné služby A7 a rozšiřuje biologický i služební registr o konkrétní podobu člena této skupiny.</p>
<div class="badges"><span class="badge o">A7</span><span class="badge">Elf</span><span class="badge">průzkumná služba</span><span class="badge">fialová výstroj</span></div>
</div>
<div class="media lightbox"><img src="/assets/a7-elfka.webp" alt="Elfka ve fialové výstroji v interiéru NII" loading="lazy"><span class="caption">A7 // ELFKA</span></div>
</article>
<article class="card full hero-card">
<div class="hero-copy">
<span class="label">bezpečnostní profil // NII</span>
<h3>Žena v černé taktické výstroji</h3>
<p>Tento obrazový záznam zachycuje blond ženu v černé taktické výstroji v průmyslovém koridoru NII. Databáze kartu vede jako atmosférický a identifikační profil člena nebo návštěvníka palubního prostředí; bez dalšího zdroje neurčuje jméno ani přesnou funkci.</p>
<div class="badges"><span class="badge o">NII</span><span class="badge">černá výstroj</span><span class="badge">interiér lodi</span><span class="badge">identita neurčena</span></div>
</div>
<div class="media lightbox"><img src="/assets/nii-black-profile.webp" alt="Žena v černé taktické výstroji v koridoru NII" loading="lazy"><span class="caption">NII // TAKTICKÝ PROFIL</span></div>
</article>
</div>
'''

if 'A7 // TEMNÁ ELFKA' not in html:
    archive_start = html.find('<section class="page" id="archive">')
    diplomacy_start = html.find('<section class="page" id="diplomacy">', archive_start)
    if archive_start < 0 or diplomacy_start < 0:
        raise SystemExit('Archive or diplomacy section not found')
    archive_close = html.rfind('</section>', archive_start, diplomacy_start)
    if archive_close < 0:
        raise SystemExit('Archive closing tag not found')
    html = html[:archive_close] + cards + html[archive_close:]

old = 'Fialová označuje průzkumnou službu; žluté prvky na fialové velitelskou / vývojovou / testovací roli. Přesná poloha, početní stav a vztah A7 k NII nejsou v tomto zdroji stanoveny.'
new = 'Fialová označuje průzkumnou službu; žluté prvky na fialové velitelskou / vývojovou / testovací roli. Nově jsou doplněny také dva přímé obrazové záznamy: elfka a temná elfka. Přesná poloha, početní stav a vztah A7 k NII nejsou v tomto zdroji stanoveny.'
html = html.replace(old, new, 1)

out = DIST / 'index.html'
out.write_text(html, encoding='utf-8')

for marker in ('A7 // TEMNÁ ELFKA', 'A7 // ELFKA', 'NII // TAKTICKÝ PROFIL'):
    if marker not in html:
        raise SystemExit(f'Missing marker: {marker}')
for name in files:
    if not (ASSETS / name).exists():
        raise SystemExit(f'Missing asset: {name}')

print('OUTPUT_BYTES', out.stat().st_size)
