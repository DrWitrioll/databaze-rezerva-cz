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
<p><strong>Databáze Rezerva, archivní zpravodajství.</strong> Po skončení bojové fáze byly v troskách nepřátelských plavidel nalezeny známky života. Záchranné týmy následně vyprostily živé členky a členy posádek rasy Vampirus. Celkem se podařilo zachránit <b>35 osob</b>. Ve chvíli, kdy bylo zřejmé, že už nepokračují v boji a nacházejí se v bezprostředním ohrožení života, byla jejich původní klasifikace nepřátelských bojovníků nahrazena zdravotnickým režimem. Všichni nalezení přeživší byli předáni k ošetření a zařazeni do zdravotnické evidence.</p>
<p>Zveřejněný archivní panel OSKN MED ukazuje pouze část zachráněné skupiny, nikoli všech 35 osob. Záznamy na něm uvádějí příslušníky nejméně první, druhé, třetí a čtvrté flotily Vampirů. Někteří jsou vedeni jako stabilizovaní, jiní zůstávají pod dalším sledováním. Na snímcích jsou patrné následky zranění, vyčerpání a celkově špatného stavu po přežití zkázy nebo těžkého poškození jejich lodí. Přesný zdravotní stav celé skupiny však databáze v současnosti nezná a nebude jej doplňovat odhadem. Stejně tak není potvrzen počet těch, kteří ve vracích zahynuli a už nemohli být zachráněni.</p>
<p>Událost je významná také tím, že představuje první rozsáhlejší evidovaný kontakt s rasou Vampirus mimo čistě bojový rámec. Ještě krátce před záchrannou operací stáli tito lidé na opačné straně konfliktu. Po skončení boje se však situace změnila: odzbrojený, zraněný a bezmocný přeživší už nebyl bezprostředním cílem, ale pacientem. Zdravotnický personál proto postupoval bez ohledu na předchozí příslušnost jednotlivých Vampirů. Samotná skutečnost, že pocházeli z nepřátelských plavidel, nebyla důvodem k odepření pomoci.</p>
<p>Archivní materiál zároveň poskytuje první konkrétnější údaje o samotné rase Vampirus. Zachránění mají převážně humanoidní vzhled, avšak jejich fyziologie a dlouhodobé biologické vlastnosti zatím nejsou v databázi dostatečně popsány. Zvláštní pozornost vyvolávají údaje o věku několika pacientů. Na zveřejněném panelu jsou uvedeny hodnoty od 224 do 338 let. Tento omezený vzorek však nestačí k určení běžné délky života Vampirů ani k vysvětlení jejich způsobu stárnutí. Databáze proto eviduje pouze konkrétní hodnoty z lékařského záznamu a žádný obecný závěr z nich zatím nevyvozuje.</p>
<p>Nejasný zůstává také další status zachráněných. V tuto chvíli není potvrzeno, zda budou po zotavení považováni za válečné zajatce, hosty, svědky, uprchlíky nebo zda budou předáni jiné autoritě. Není rovněž stanoveno, zda některý z nich projeví zájem o spolupráci. Záchranná operace sama o sobě tedy nemění jejich předchozí příslušnost ani automaticky neznamená jejich vstup do posádky NII. V personálním stavu NII proto těchto 35 Vampirů není započítáno.</p>
<p>Jisté je pouze to, že třicet pět příslušníků nepřátelských posádek přežilo zničení nebo těžké poškození svých lodí a bylo z jejich trosek vytaženo živých. V okamžiku, kdy skončila střelba, začala jiná práce — hledání přeživších a snaha udržet je naživu. Pro zdravotníky nebyla rozhodující flotila uvedená v databázi, znak na uniformě ani předchozí strana konfliktu, ale skutečnost, že před nimi ležela myslící bytost, které ještě bylo možné pomoci.</p>
<p>Právě proto se tento případ dostal do Databáze Rezerva jako samostatný zpravodajský záznam. Zachycuje situaci, kdy se hranice mezi nepřítelem a pacientem změnila během několika okamžiků. Další osud všech 35 zachráněných Vampirů zůstává otevřený a bude doplněn až podle potvrzených událostí. Do té doby zůstává tento archiv především svědectvím o tom, že i z trosek nepřátelských lodí mohou být vytaženi lidé, kteří ještě dostanou druhou šanci.</p>
<div class="badges"><span class="badge o">35 přeživších</span><span class="badge">Vampirus</span><span class="badge">záchrana z vraků</span><span class="badge">OSKN MED</span><span class="badge">1.–4. flotila</span></div>
</div>
<div class="media contain lightbox" style="align-self:start;aspect-ratio:16/10;min-height:0"><img src="/assets/vampirus-survivors.png" alt="Databázový záznam zachráněných přeživších rasy Vampirus" loading="lazy"><span class="caption">VAMPIRUS // 35 ZACHRÁNĚNÝCH</span></div>
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

row_anchor = '<tr><td><strong>Felisius (A7)</strong></td><td>rysovitý humanoidní druh</td><td><span class="state unk">stav na NII neurčen</span></td></tr>'
vamp_row = '<tr><td><strong>Vampirus</strong></td><td>humanoidní rasa; archiv zachráněných uvádí jednotlivce ve věku 224–338 let, bez odhadu běžné délky života druhu</td><td><b>35 zachráněných</b>; členství v posádce NII nepotvrzeno</td></tr>'
if vamp_row not in html and row_anchor in html:
    html = html.replace(row_anchor, row_anchor + vamp_row, 1)

index.write_text(html, encoding='utf-8')

for check in (marker, '35 přeživších rasy Vampirus', '/assets/vampirus-survivors.png', 'media contain lightbox'):
    if check not in html:
        raise SystemExit(f'Missing Vampirus marker: {check}')
print('VAMPIRUS_ARTICLE_OK', index.stat().st_size, asset_dst.stat().st_size)
