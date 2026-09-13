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
    data = base64.b64decode(src.read_text(encoding='utf-8').strip(), validate=True)
    if len(data) < 3000:
        raise SystemExit(f'Asset {name} is unexpectedly small: {len(data)} bytes')
    (ASSETS / name).write_bytes(data)
    print('ASSET', name, len(data))

html = SRC.read_text(encoding='utf-8')

intro_old = '<p>Do terminálu byly doplněny další vizuální karty: symbolické znaky, pozemní hlídkový profil a experimentální letecký stroj. Jde o samostatný obrazový archiv určený pro rychlou orientaci a atmosférické doplnění databáze.</p>'
intro_new = '<p>Do terminálu byly doplněny další vizuální karty: symbolické znaky, pozemní hlídkový profil, experimentální letecký stroj a tři nové personální obrazové záznamy. Jde o samostatný obrazový archiv určený pro rychlou orientaci, identifikaci druhů a atmosférické doplnění databáze.</p>'
if intro_old in html:
    html = html.replace(intro_old, intro_new, 1)

anchor = '''<article class="card full hero-card">
<div class="hero-copy">
<span class="label red">letecký archiv</span>
<h3>Experimentální raketový letoun</h3>
<p>Vizuální záznam ukazuje jednomístný letoun s červenými hvězdami, robustně upravenou pohonnou sekcí a dvojicí jasně zářících trysek. Konstrukce spojuje klasický tvar vrtulového stroje s agresivně přestavěným futuristickým pohonem a působí jako experimentální útočný nebo přepadový typ.</p>
<div class="badges"><span class="badge o">letectvo</span><span class="badge">experimentální stroj</span><span class="badge">červené hvězdy</span><span class="badge">raketový pohon</span></div>
</div>
<div class="media lightbox"><img src="https://res.cloudinary.com/emmgrwto/image/upload/v1789246624/rezervni-posadka/experimental-rocket-plane.png" alt="Experimentální raketový letoun s červenými hvězdami" loading="lazy"><span class="caption">LETECKÝ ARCHIV // EXPERIMENTÁLNÍ STROJ</span></div>
</article>'''

cards = '''
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
</article>'''

if 'A7 // TEMNÁ ELFKA' not in html:
    if anchor not in html:
        raise SystemExit('Image-card insertion anchor not found')
    html = html.replace(anchor, anchor + cards, 1)

old_a7 = '<article class="card half"><span class="label green">ARC-A7-BIO</span><h3>A7 // biologický a služební záznam</h3><p>Potvrzeny jsou čtyři skupiny posádky A7: Elf, Temný Elf, Felisius a člověk. Fialová označuje průzkumnou službu; žluté prvky na fialové velitelskou / vývojovou / testovací roli. Přesná poloha, početní stav a vztah A7 k NII nejsou v tomto zdroji stanoveny.</p></article>'
new_a7 = '<article class="card half"><span class="label green">ARC-A7-BIO</span><h3>A7 // biologický a služební záznam</h3><p>Potvrzeny jsou čtyři skupiny posádky A7: Elf, Temný Elf, Felisius a člověk. Fialová označuje průzkumnou službu; žluté prvky na fialové velitelskou / vývojovou / testovací roli. Nově jsou doplněny také dva přímé obrazové záznamy: elfka a temná elfka. Přesná poloha, početní stav a vztah A7 k NII nejsou v tomto zdroji stanoveny.</p></article>'
if old_a7 in html:
    html = html.replace(old_a7, new_a7, 1)

out = DIST / 'index.html'
out.write_text(html, encoding='utf-8')

for marker in (
    'A7 // TEMNÁ ELFKA',
    'A7 // ELFKA',
    'NII // TAKTICKÝ PROFIL',
    '/assets/a7-temna-elfka.webp',
    '/assets/a7-elfka.webp',
    '/assets/nii-black-profile.webp',
):
    if marker not in html:
        raise SystemExit(f'Missing verification marker: {marker}')

print('OUTPUT_BYTES', out.stat().st_size)
