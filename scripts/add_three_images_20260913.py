from pathlib import Path
import json
import urllib.request
import urllib.error

ROOT = Path('.')
SRC = ROOT / 'site-full-update-20260913.html'
DIST = ROOT / 'dist'
ASSETS = DIST / 'assets'
DIST.mkdir(exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

FILES = [
    {
        'share':'FuBrVBf_mJ1B',
        'file_id':'01a09a41f43676fd950749018f2ed839',
        'name':'a7-temna-elfka.png',
    },
    {
        'share':'u-HPMvjSYw5L',
        'file_id':'01a09a424013761b9508955db397e355',
        'name':'a7-elfka.png',
    },
    {
        'share':'q9Ar6KBQETWH',
        'file_id':'01a09a4286b572d996962dc4908b5088',
        'name':'nii-black-profile.png',
    },
]


def json_request(url, method='GET', data=None):
    body = None if data is None else json.dumps(data).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            'User-Agent':'Mozilla/5.0 RezervniPosadkaDeploy/1.0',
            'Accept':'application/json',
            'Content-Type':'application/json',
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))


def find_download_url(obj):
    if isinstance(obj, dict):
        for key in ('downloadUrl','download_url','url'):
            val = obj.get(key)
            if isinstance(val, str) and val.startswith('http'):
                return val
        for v in obj.values():
            got = find_download_url(v)
            if got:
                return got
    elif isinstance(obj, list):
        for v in obj:
            got = find_download_url(v)
            if got:
                return got
    return None


def download_firestorage(share, file_id, dest):
    endpoint = f'https://api.firestorage.ai/prod/file/shares/{share}/files/{file_id}/download'
    errors=[]
    for payload in (None, {}, {'fileId':file_id}):
        try:
            data = json_request(endpoint, method='POST', data=payload)
            url = find_download_url(data)
            if not url:
                raise RuntimeError(f'No downloadUrl in response: {data!r}')
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as r:
                blob = r.read()
            if len(blob) < 100000:
                raise RuntimeError(f'Download too small: {len(blob)} bytes')
            dest.write_bytes(blob)
            print('DOWNLOADED', dest, len(blob))
            return
        except Exception as e:
            errors.append(repr(e))
    listing_url=f'https://api.firestorage.ai/prod/file/shares/{share}/files?maxResults=1000'
    try:
        listing=json_request(listing_url)
        data=json_request(endpoint, method='POST', data={})
        url=find_download_url(data)
        if not url:
            raise RuntimeError(f'No download URL after listing. listing={listing!r} response={data!r}')
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=120) as r:
            blob=r.read()
        if len(blob)<100000:
            raise RuntimeError(f'Download too small after listing: {len(blob)} bytes')
        dest.write_bytes(blob)
        print('DOWNLOADED',dest,len(blob))
        return
    except Exception as e:
        errors.append(repr(e))
    raise RuntimeError('Firestorage download failed: ' + ' | '.join(errors))

for item in FILES:
    download_firestorage(item['share'], item['file_id'], ASSETS/item['name'])

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
<div class="media lightbox"><img src="/assets/a7-temna-elfka.png" alt="Temná elfka ve fialové výstroji se žlutými prvky" loading="lazy"><span class="caption">A7 // TEMNÁ ELFKA</span></div>
</article>
<article class="card full hero-card">
<div class="hero-copy">
<span class="label green">A7 // elf</span>
<h3>Elfka v průzkumné výstroji</h3>
<p>Archivní karta ukazuje světlovlasou elfku s dlouhými špičatými ušima, brýlemi a fialovou výstrojí. Záznam vizuálně zapadá do průzkumné služby A7 a rozšiřuje biologický i služební registr o konkrétní podobu člena této skupiny.</p>
<div class="badges"><span class="badge o">A7</span><span class="badge">Elf</span><span class="badge">průzkumná služba</span><span class="badge">fialová výstroj</span></div>
</div>
<div class="media lightbox"><img src="/assets/a7-elfka.png" alt="Elfka ve fialové výstroji v interiéru NII" loading="lazy"><span class="caption">A7 // ELFKA</span></div>
</article>
<article class="card full hero-card">
<div class="hero-copy">
<span class="label">bezpečnostní profil // NII</span>
<h3>Žena v černé taktické výstroji</h3>
<p>Tento obrazový záznam zachycuje blond ženu v černé taktické výstroji v průmyslovém koridoru NII. Databáze kartu vede jako atmosférický a identifikační profil člena nebo návštěvníka palubního prostředí; bez dalšího zdroje neurčuje jméno ani přesnou funkci.</p>
<div class="badges"><span class="badge o">NII</span><span class="badge">černá výstroj</span><span class="badge">interiér lodi</span><span class="badge">identita neurčena</span></div>
</div>
<div class="media lightbox"><img src="/assets/nii-black-profile.png" alt="Žena v černé taktické výstroji v koridoru NII" loading="lazy"><span class="caption">NII // TAKTICKÝ PROFIL</span></div>
</article>'''

if 'A7 // TEMNÁ ELFKA' not in html:
    if anchor not in html:
        raise SystemExit('Image-card insertion anchor not found')
    html = html.replace(anchor, anchor + cards, 1)

old_a7 = '<article class="card half"><span class="label green">ARC-A7-BIO</span><h3>A7 // biologický a služební záznam</h3><p>Potvrzeny jsou čtyři skupiny posádky A7: Elf, Temný Elf, Felisius a člověk. Fialová označuje průzkumnou službu; žluté prvky na fialové velitelskou / vývojovou / testovací roli. Přesná poloha, početní stav a vztah A7 k NII nejsou v tomto zdroji stanoveny.</p></article>'
new_a7 = '<article class="card half"><span class="label green">ARC-A7-BIO</span><h3>A7 // biologický a služební záznam</h3><p>Potvrzeny jsou čtyři skupiny posádky A7: Elf, Temný Elf, Felisius a člověk. Fialová označuje průzkumnou službu; žluté prvky na fialové velitelskou / vývojovou / testovací roli. Nově jsou doplněny také dva přímé obrazové záznamy: elfka a temná elfka. Přesná poloha, početní stav a vztah A7 k NII nejsou v tomto zdroji stanoveny.</p></article>'
if old_a7 in html:
    html = html.replace(old_a7, new_a7, 1)

(DIST/'index.html').write_text(html, encoding='utf-8')

checks = [
    'A7 // TEMNÁ ELFKA',
    'A7 // ELFKA',
    'NII // TAKTICKÝ PROFIL',
    '/assets/a7-temna-elfka.png',
    '/assets/a7-elfka.png',
    '/assets/nii-black-profile.png',
]
for c in checks:
    if c not in html:
        raise SystemExit(f'Missing verification marker: {c}')
print('OUTPUT_BYTES', (DIST/'index.html').stat().st_size)
