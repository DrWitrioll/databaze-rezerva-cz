from pathlib import Path
import re, urllib.request

out=Path('site-full-update-20260913.html')
url='https://res.cloudinary.com/emmgrwto/raw/upload/rezervni-posadka/site-final.html'
html=urllib.request.urlopen(url).read().decode('utf-8')
print('SOURCE_BYTES', len(html.encode('utf-8')))

def repl(old,new,count=None,label='replace'):
    global html
    n=html.count(old)
    if n==0:
        raise SystemExit(f'{label}: marker not found: {old[:120]!r}')
    if count is not None and n < count:
        raise SystemExit(f'{label}: expected at least {count}, found {n}')
    html=html.replace(old,new, count if count is not None else -1)
    print(f'{label}: {n} match(es)')

old='<span>FTL: pouze NII-88 / SOJUZ</span></div>'
new='<span>FTL: pouze NII-88 / SOJUZ</span><span>revize kánonu: 13. 9. 2026</span></div>'
repl(old,new,1,'status revision')

repl('<div class="spec"><b>22</b><span>aktuálně evidováno</span></div>', '<div class="spec"><b>232</b><span>aktuálně evidováno</span></div>',1,'NII hero crew')
repl('<tr><td>Současně evidováno</td><td><strong>22 členů / entit</strong></td></tr>', '<tr><td>Současně evidováno</td><td><strong>232 členů / entit</strong></td></tr>',1,'NII spec crew')
old_metrics='<div class="metric"><strong>22</strong><span>celkem evidováno</span></div>\n<div class="metric"><strong>20</strong><span>fyzicky na palubě</span></div>\n<div class="metric"><strong>1</strong><span>hologram</span></div>\n<div class="metric"><strong>1</strong><span>centrální AI</span></div>'
new_metrics='<div class="metric"><strong>232</strong><span>celkem evidováno</span></div>\n<div class="metric"><strong>230</strong><span>fyzicky na palubě</span></div>\n<div class="metric"><strong>1</strong><span>hologram</span></div>\n<div class="metric"><strong>1</strong><span>centrální AI</span></div>'
repl(old_metrics,new_metrics,1,'crew wave metrics')
repl('U šedesáti pomocných členů nejsou doplněna jména, hodnosti ani specializace.', 'U 210 skupinově vedených členů nejsou doplněna jména, hodnosti ani individuální specializace.',1,'crew gaps')
old_hist='<p>Aktuální databáze eviduje <b>22 členů/entit</b>: původní jmenné jádro 22 záznamů a žádní noví skupinově vedení pomocných členů. NII má přitom konstrukční kapacitu až 420 členů a čtyřletou autonomii při tomto plném stavu.</p>'
new_hist='<p>Aktuální databáze eviduje <b>232 členů/entit</b>: 22 jmenných záznamů a 210 dalších členů vedených skupinově podle druhu. Fyzicky je na palubě 230 osob nebo androidních jednotek; Arnold Rimmer je hologram a Holly centrální AI. NII má konstrukční kapacitu až 420 členů a čtyřletou autonomii při plném projektovaném stavu.</p>'
repl(old_hist,new_hist,1,'history current state')

repl('20 příslušníků vstoupilo do pomocného stavu NII', 've dvou potvrzených vlnách vstoupilo na NII celkem 50 kočko-lidí',1,'diplomacy cats')
cat_row='<tr><td><strong>Kočko-lidé ze stanice</strong></td><td>praktická spolupráce</td><td>ve dvou potvrzených vlnách vstoupilo na NII celkem 50 kočko-lidí</td><td>jména a individuální funkce nejsou určeny</td></tr>'
station_rows=cat_row + '''\n<tr><td><strong>Pso-lidé ze stanice</strong></td><td>praktická spolupráce / členové NII</td><td>ve dvou vlnách přijato celkem 50 pso-lidí</td><td>jména a individuální funkce nejsou určeny</td></tr>
<tr><td><strong>Trpaslíci ze stanice</strong></td><td>praktická spolupráce / členové NII</td><td>ve dvou vlnách přijato celkem 60 trpaslíků</td><td>jména a individuální funkce nejsou určeny</td></tr>
<tr><td><strong>Ještěřané ze stanice</strong></td><td>praktická spolupráce / členové NII</td><td>ve dvou vlnách přijato celkem 50 ještěřanů</td><td>jména a individuální funkce nejsou určeny</td></tr>'''
repl(cat_row,station_rows,1,'diplomacy station species')

repl('<div class="stamp">kontakt: přerušen po pěti FTL skocích</div>', '<div class="stamp">konflikt pokračuje // lokální kontakt NII neurčen</div>',1,'soviet stamp')
old_sov='<article class="card half"><span class="label green">současný stav</span><h3>Bez aktivního kontaktu</h3><p>Po pěti FTL skocích od Helioru nemá NII potvrzený bezprostřední sovětský kontakt. Sovětské síly zůstávají známým nepřítelem z heliorské etapy, ale jejich současná poloha a schopnost sledovat NII nejsou potvrzeny.</p><div class="warning"><b>Neznámé:</b> aktuální poloha sovětské flotily, její přesný početní stav a další operační záměr nejsou potvrzeny.</div></article>'
new_sov='<article class="card half"><span class="label red">současný stav</span><h3>Konflikt se rozšířil mimo Helior</h3><p>Po pěti FTL skocích NII přerušila bezprostřední kontakt s útočníky od Helioru. Pozdější zprávy z mezirasové obchodní sítě však potvrzují, že lodě rozpoznané podle rudé hvězdy a konstrukčních znaků jako sovětské útočí také na planety a stanice této civilizace.</p><div class="warning"><b>Neznámé:</b> přesná poloha hlavních sovětských sil, jejich celkový počet, způsob přesunu mezi vzdálenými bojišti a okamžitá vzdálenost od NII zůstávají nepotvrzené.</div></article>'
repl(old_sov,new_sov,1,'soviet current status')
repl('Databáze však odděluje potvrzenou heliorskou bitvu od dalších hypotetických střetů a nepřidává útoky v jiných systémech bez dějového potvrzení.', 'Databáze odděluje potvrzenou heliorskou bitvu od později potvrzené války proti mezirasové obchodní síti a nepřidává další střety tam, kde příběh neurčil jejich místo, počet lodí nebo výsledek.',1,'soviet dossier')

repl('symbolické znaky, pozemní hlídkový profil, experimentální letecký stroj a bestiární záznam tříhlavého draka.', 'symbolické znaky, pozemní hlídkový profil a experimentální letecký stroj.',1,'dragon archive mention')

ursane_card_end='''<article class="card full hero-card"><div class="hero-copy"><span class="label green">nový druh</span><h3>Ursané</h3><p>Ursané jsou nově zavedený inteligentní druh medvědích humanoidů. Vizuální záznam ukazuje mohutně stavěného příslušníka tohoto druhu s kožešinou, šamansky laděným oděvem, přírodními amulety a symbolikou spojenou s krajinou a kamenem.</p><p>Databáze je v této fázi vede jako samostatný druh. Přesný počet, původní domovina a vztah k NII budou doplněny až podle dalších potvrzených informací.</p><div class="badges"><span class="badge o">Ursané</span><span class="badge">medvědí humanoidi</span><span class="badge">nový druh</span><span class="badge">počet zatím neurčen</span></div></div><div class="media lightbox"><img src="https://res.cloudinary.com/emmgrwto/image/upload/v1789222542/rezervni-posadka/ursane.png" alt="Příslušník druhu Ursané v horské krajině" loading="lazy"><span class="caption">URSANÉ // NOVÝ DRUH</span></div></article>'''
ursane_calendar='''
<article class="card full">
<span class="label green">Ursané // chronologie Protos Singulár</span>
<h3>Kalendář Protos Singulár — 24 měsíců</h3>
<p>Ursanský kalendář používaný pro Protos Singulár má 24 pojmenovaných měsíců. Zdroj potvrzuje jejich pořadí a několik klimatických vazeb, ale neurčuje délku jednotlivých měsíců ani celkový počet dní roku, takže je databáze nedoplňuje odhadem.</p>
<div class="table-wrap"><table><thead><tr><th>#</th><th>Měsíc</th><th>#</th><th>Měsíc</th><th>#</th><th>Měsíc</th><th>#</th><th>Měsíc</th></tr></thead><tbody>
<tr><td>1</td><td><strong>Vargun</strong></td><td>7</td><td><strong>Velrun</strong></td><td>13</td><td><strong>Seldran</strong></td><td>19</td><td><strong>Skovar</strong></td></tr>
<tr><td>2</td><td><strong>Selvar</strong></td><td>8</td><td><strong>Jorvak</strong></td><td>14</td><td><strong>Vejrik</strong></td><td>20</td><td><strong>Drelun</strong></td></tr>
<tr><td>3</td><td><strong>Dromir</strong></td><td>9</td><td><strong>Melyr</strong></td><td>15</td><td><strong>Korvan</strong></td><td>21</td><td><strong>Morvik</strong></td></tr>
<tr><td>4</td><td><strong>Kelvan</strong></td><td>10</td><td><strong>Brasken</strong></td><td>16</td><td><strong>Talvik</strong></td><td>22</td><td><strong>Zelran</strong></td></tr>
<tr><td>5</td><td><strong>Orvik</strong></td><td>11</td><td><strong>Olvar</strong></td><td>17</td><td><strong>Rudren</strong></td><td>23</td><td><strong>Tervan</strong></td></tr>
<tr><td>6</td><td><strong>Targan</strong></td><td>12</td><td><strong>Hurnik</strong></td><td>18</td><td><strong>Jelmar</strong></td><td>24</td><td><strong>Norskar</strong></td></tr>
</tbody></table></div>
<div class="badges"><span class="badge o">24 měsíců</span><span class="badge">Velrun–Jorvak–Melyr // mezi nejteplejšími</span><span class="badge">Norskar // poslední a nejchladnější</span></div>
<div class="warning"><b>Zápis data:</b> běžně například „14. den Talviku, roku 731“, vojensky zkráceně „14 Talvik 731 PS“.</div>
</article>'''
repl(ursane_card_end,ursane_card_end+ursane_calendar,1,'Ursane calendar')

station_security_marker='<article class="card full hero-card">\n<div class="hero-copy">\n<span class="label green">mezirasová stanice // bezpečnost</span>'
a7_block='''<article class="card full">
<span class="label green">A7 // potvrzený biologický registr posádky</span>
<h3>Rasy a služební značení A7</h3>
<p>Záznam A7 potvrzuje čtyři biologické skupiny v posádce: Elfa, Temného Elfa, Felisia a člověka. Tento registr sám o sobě neurčuje jejich počet na NII, politický vztah A7 k NII ani přesné chronologické zařazení kontaktu; tyto údaje proto zůstávají otevřené.</p>
<div class="table-wrap"><table><thead><tr><th>Druh</th><th>Potvrzené znaky</th><th>Potvrzená role / výstroj</th></tr></thead><tbody>
<tr><td><strong>Elf</strong></td><td>světlá kůže, dlouhé špičaté uši</td><td>průzkumník ve fialové výstroji</td></tr>
<tr><td><strong>Temný Elf</strong></td><td>modrá kůže, dlouhé špičaté uši</td><td>velitelská / vývojová / testovací role; fialová výstroj se žlutými prvky pancíře</td></tr>
<tr><td><strong>Felisius</strong></td><td>rysovitý humanoid</td><td>lékař v bílé zdravotnické výstroji</td></tr>
<tr><td><strong>Člověk</strong></td><td>biologicky lidský vzhled</td><td>žena v červené technické výstroji</td></tr>
</tbody></table></div>
<div class="badges"><span class="badge o">fialová // průzkumná služba</span><span class="badge">žluté prvky na fialové // velení / vývoj / testování</span><span class="badge">bílá // potvrzený lékař</span><span class="badge">červená // potvrzená technička</span></div>
<div class="warning"><b>Taxonomická poznámka:</b> Heliořanky jsou samostatný biologický druh. Jejich dlouhé špičaté uši a částečná vizuální podobnost s Elfy z A7 neznamenají společný druh.</div>
</article>
'''
if station_security_marker not in html: raise SystemExit('A7 insertion marker missing')
html=html.replace(station_security_marker,a7_block+station_security_marker,1)
print('A7 block: inserted')

urs_row='<tr><td><strong>Ursané</strong></td><td>medvědí humanoidní druh; mohutná postava, kožešina, kmenová a přírodní symbolika</td><td><span class="state unk">zatím neurčeno</span></td></tr>'
a7_rows=urs_row+'''<tr><td><strong>Elf (A7)</strong></td><td>světlá kůže, dlouhé špičaté uši</td><td><span class="state unk">stav na NII neurčen</span></td></tr><tr><td><strong>Temný Elf (A7)</strong></td><td>modrá kůže, dlouhé špičaté uši</td><td><span class="state unk">stav na NII neurčen</span></td></tr><tr><td><strong>Felisius (A7)</strong></td><td>rysovitý humanoidní druh</td><td><span class="state unk">stav na NII neurčen</span></td></tr>'''
repl(urs_row,a7_rows,1,'A7 species rows')

unknown_location='<article class="card full"><span class="label gray">současná oblast</span><h3>Neznámý prostor</h3><p>Přesná hvězda, číselné souřadnice a úplná mapa současného systému nejsou v kánonu určeny. Databáze proto pouze eviduje, že NII po pěti FTL skocích a následném hledání inteligentního života operuje mimo původně známý lidský prostor.</p></article>'
protos_card='''<article class="card half"><span class="label green">Ursané // chronologický referenční bod</span><h3>Protos Singulár</h3><p>K Protos Singulár je potvrzen ursanský kalendář o 24 měsících. Zdroj zatím neurčuje jeho přesné souřadnice, astronomický typ ani vztah k současné poloze NII, proto jej databáze vede pouze jako potvrzený kulturně-chronologický referenční bod Ursanů.</p><div class="badges"><span class="badge o">24 měsíců</span><span class="badge">souřadnice neurčeny</span><span class="badge">vztah k NII neurčen</span></div></article>'''
repl(unknown_location,protos_card+'\n'+unknown_location,1,'Protos location record')

archive_marker='<!-- EXPANSION: ARCHIVE -->'
archive_add='''<div class="grid">
<article class="card half"><span class="label green">ARC-URS-CAL</span><h3>Ursané // Protos Singulár</h3><p>Chronologický spis potvrzuje 24měsíční ursanský kalendář používaný pro Protos Singulár. Norskar je poslední a nejchladnější měsíc; Velrun, Jorvak a Melyr patří mezi nejteplejší.</p><div class="badges"><span class="badge o">24 měsíců</span><span class="badge">14 Talvik 731 PS</span></div></article>
<article class="card half"><span class="label green">ARC-A7-BIO</span><h3>A7 // biologický a služební záznam</h3><p>Potvrzeny jsou čtyři skupiny posádky A7: Elf, Temný Elf, Felisius a člověk. Fialová označuje průzkumnou službu; žluté prvky na fialové velitelskou / vývojovou / testovací roli. Přesná poloha, početní stav a vztah A7 k NII nejsou v tomto zdroji stanoveny.</p></article>
</div>
'''
if archive_marker not in html: raise SystemExit('archive marker missing')
html=html.replace(archive_marker,archive_add+archive_marker,1)
print('archive A7/Ursane: inserted')

intel_open='<article class="card full"><span class="label gray">otevřené body</span><h3>Co je nutné zjistit dál</h3><div class="table-wrap"><table><thead><tr><th>Otázka</th><th>Aktuální stav</th></tr></thead><tbody>'
intel_prefix='''<article class="card half"><span class="label green">nový biologický spis</span><h3>A7</h3><p>Taxonomie čtyř členů/skupin posádky A7 je potvrzena: Elf, Temný Elf, Felisius a člověk. Nejsou však potvrzeny jejich počty na NII, aktuální poloha A7 ani politický vztah této posádky k NII.</p></article>
<article class="card half"><span class="label green">nový kulturní spis</span><h3>Ursané / Protos Singulár</h3><p>Ursané jsou samostatný medvědí humanoidní druh a databáze nyní zná jejich 24měsíční kalendář používaný pro Protos Singulár. Populace, domovina v astronomickém smyslu, souřadnice a vztah k NII zůstávají nepotvrzené.</p></article>
'''
if intel_open not in html: raise SystemExit('intel marker missing')
html=html.replace(intel_open,intel_prefix+intel_open,1)
print('intel A7/Ursane: inserted')

needle='<tr><td>Souřadnice současného sektoru NII</td><td>neurčeny</td></tr>'
extra=needle+'<tr><td>Přesná poloha a politický status A7</td><td>neurčeno</td></tr><tr><td>Populace, souřadnice a přesný vztah Ursanů / Protos Singulár k NII</td><td>neurčeno</td></tr>'
repl(needle,extra,1,'intel open rows')

repl('<span>kanonický stav: průběžně aktualizovaný</span>', '<span>kanonický stav: revize 13. 9. 2026</span>',1,'footer revision')

assert '<h3>Tříhlavý drak</h3>' not in html
assert 'bestiární záznam tříhlavého draka' not in html
assert 'U šedesáti pomocných členů' not in html
assert 'Aktuální databáze eviduje <b>22 členů/entit</b>' not in html
assert '<b>22</b><span>aktuálně evidováno</span>' not in html
assert 'Kalendář Protos Singulár — 24 měsíců' in html
assert 'Rasy a služební značení A7' in html
assert 'stav osazenstva: 232 evidovaných / 230 fyzických' in html
assert 'revize kánonu: 13. 9. 2026' in html
assert 'URSANÉ // NOVÝ DRUH' in html
assert html.count('<section class="page') == 16
assert html.count('data-tab=') == 16
assert html.count('<script>') == 1 and html.count('</script>') == 1
assert html.strip().endswith('</html>')

out.write_text(html,encoding='utf-8')
print('OUTPUT',out,'bytes',len(html.encode('utf-8')),'lines',html.count('\n')+1)
