from pathlib import Path
import shutil

root = Path('.')
dist = root / 'dist'
index = dist / 'index.html'
asset_src = root / 'assets' / 'vampirus-survivors.png'
asset_dst = dist / 'assets' / 'vampirus-survivors.png'

if not index.exists():
    raise SystemExit('dist/index.html not found')
if not asset_src.exists():
    raise SystemExit('Vampirus source image not found')

asset_dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(asset_src, asset_dst)

html = index.read_text(encoding='utf-8')
marker = 'VAMPIRUS // 35 ZACHRÁNĚNÝCH'

article = '''
<article class="card full hero-card">
<div class="hero-copy">
<span class="label red">zvláštní vydání // záchranná operace</span>
<h3>35 přeživších rasy Vampirus zachráněno z trosek nepřátelských lodí</h3>
<p><strong>Databáze Rezerva, archivní zpravodajství.</strong> Po skončení bojové fáze byly v troskách nepřátelských plavidel nalezeny živé členky a členové posádek rasy Vampirus. Záchranné týmy z vraků vyprostily celkem <b>35 přeživších</b>. Přestože ještě krátce předtím patřili k nepřátelským silám, po jejich nalezení byla bojová klasifikace nahrazena zdravotnickým režimem a všichni zachránění byli předáni k ošetření. Archivní karta OSKN MED zaznamenává příslušníky nejméně čtyř flotil a ukazuje několik pacientů ve stavu stabilizace nebo dalšího lékařského sledování.</p>
<p>Rozhodnutí zahájit záchranu nebylo vedeno politickým gestem ani snahou přepsat výsledek bitvy. Šlo o jednoduché pravidlo: člověk či jiná myslící bytost, která už nepokračuje v boji a nachází se v bezprostředním ohrožení života, je nejprve pacientem. Zdravotníci proto pracovali bez ohledu na předchozí příslušnost zachráněných. Část Vampirů utrpěla zranění, vyčerpání a následky pobytu v poškozených částech lodí; někteří byli po základním ošetření stabilizováni, jiní zůstali pod dohledem. Přesný zdravotní stav všech 35 osob databáze zatím nerozepisuje.</p>
<p>Událost zároveň představuje první rozsáhlejší evidovaný kontakt s rasou Vampirus mimo čistě bojový rámec. Záznamy ukazují humanoidní vzhled a velmi vysoký uváděný věk několika zachráněných, avšak databáze z těchto údajů neodvozuje biologickou délku života celého druhu. Stejně tak zatím není potvrzeno, zda se zachránění stanou zajatci, hosty, svědky, uprchlíky nebo zda budou později předáni jiné autoritě. Jisté je pouze to, že z nepřátelských vraků bylo vytaženo 35 živých bytostí, které dostaly šanci přežít.</p>
<p>V archivech zůstává tato operace významná právě tím, že hranice mezi nepřítelem a zachráněným člověkem nebyla zaměněna za hranici mezi životem a smrtí. Boj skončil ve chvíli, kdy začala záchrana. Další osud Vampirů bude doplněn až podle potvrzených událostí.</p>
<div class="badges"><span class="badge o">35 přeživších</span><span class="badge">Vampirus</span><span class="badge">záchrana z vraků</span><span class="badge">OSKN MED</span><span class="badge">1.–4. flotila</span></div>
</div>
<div class="media lightbox"><img src="/assets/vampirus-survivors.png" alt="Databázový záznam zachráněných přeživších rasy Vampirus" loading="lazy"><span class="caption">VAMPIRUS // 35 ZACHRÁNĚNÝCH</span></div>
</article>
'''

if marker not in html:
    intel_start = html.find('<section class="page" id="intel">')
    if intel_start < 0:
        raise SystemExit('Intel section not found')
    open_points = html.find('<article class="card full"><span class="label gray">otevřené body</span>', intel_start)
    if open_points < 0:
        raise SystemExit('Intel insertion point not found')
    html = html[:open_points] + article + html[open_points:]

# Add Vampirus to known species table, but do not count them as NII crew.
row_anchor = '<tr><td><strong>Felisius (A7)</strong></td><td>rysovitý humanoidní druh</td><td><span class="state unk">stav na NII neurčen</span></td></tr>'
vamp_row = '<tr><td><strong>Vampirus</strong></td><td>humanoidní rasa; archiv zachráněných uvádí jednotlivce ve věku 224–338 let, bez odhadu běžné délky života druhu</td><td><b>35 zachráněných</b>; členství v posádce NII nepotvrzeno</td></tr>'
if vamp_row not in html and row_anchor in html:
    html = html.replace(row_anchor, row_anchor + vamp_row, 1)

index.write_text(html, encoding='utf-8')

for check in (marker, '35 přeživších rasy Vampirus', '/assets/vampirus-survivors.png'):
    if check not in html:
        raise SystemExit(f'Missing Vampirus marker: {check}')
print('VAMPIRUS_ARTICLE_OK', index.stat().st_size, asset_dst.stat().st_size)
