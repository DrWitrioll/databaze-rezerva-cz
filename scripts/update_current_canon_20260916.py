from pathlib import Path
import re

root = Path('.')
index = root / 'dist' / 'index.html'
if not index.exists():
    raise SystemExit('dist/index.html not found')
html = index.read_text(encoding='utf-8')

def replace_if(old, new, count=-1):
    global html
    if old in html:
        html = html.replace(old, new, count)
        return True
    return False

def insert_into_section(section_id, fragment, marker):
    global html
    if marker in html:
        return False
    start = html.find(f'<section class="page" id="{section_id}">')
    if start < 0:
        raise SystemExit(f'section {section_id} not found')
    next_start = html.find('<section class="page" id="', start + 10)
    end = next_start if next_start >= 0 else len(html)
    section = html[start:end]
    close = section.rfind('</div>')
    if close < 0:
        raise SystemExit(f'grid close not found in section {section_id}')
    pos = start + close
    html = html[:pos] + fragment + '\n' + html[pos:]
    return True

replace_if('revize kánonu: 13. 9. 2026', 'revize kánonu: 16. 9. 2026')
replace_if('420 m</b><span>délka</span>', '424 m</b><span>délka</span>')
replace_if('≈420 m</b><span>délka NII</span>', '≈424 m</b><span>délka NII</span>')
replace_if('NII je 420 metrů dlouhá', 'NII je 424 metrů dlouhá')
replace_if('NII je přibližně 420 metrů dlouhá', 'NII je 424 metrů dlouhá')
replace_if('FTL: pouze NII-88 / SOJUZ', 'FTL: NII + nové systémy OSKN / HELIOS')
replace_if('<b>NII-88 / Projekt 82-ES „Sojuz“ je jediná loď v kánonu, která má FTL pohon.</b> Lidstvo Argusu, Sověti, Heliorané ani známé lodě mezirasové obchodní frakce FTL pohon nemají.', '<b>NII-88 / Projekt 82-ES „Sojuz“ už není jediným potvrzeným nositelem FTL technologie.</b> V aktuální dějové vrstvě vznikl nadprostorový pohon 88/100 s prvním funkčním prototypem na A7 a následně podprostorový pohon 84/100. Starší civilizace a plavidla tím nejsou automaticky zpětně vybavena FTL.')

factions = '''
<article class="card full"><span class="label red">aktuální hrozba // Custodes Liminis</span><h3>Custodes Liminis — Strážci prahu</h3><p>Custodes Liminis jsou technologicky extrémně vyspělá civilizace, která po tisíce let sleduje jiné společnosti a zasahuje ve chvíli, kdy podle jejích kritérií překročí takzvaný <b>Limen — Práh</b>. Po OSKN a HELIOS požadovaly zastavení reprodukovatelného FTL, warpových systémů, experimentů se singularitami a dalších technologií třídy Limen. Po odmítnutí zahájily <b>Interdictio</b>, zaměřené především proti loděnicím, výzkumným centrům, FTL výrobě a strategické infrastruktuře.</p><p>Po prvních ztrátách bylo Interdictio pouze pozastaveno a prostor OSKN–HELIOS přešel do režimu <b>Recensio</b>. Custodes nyní převážně pozorují další vývoj. Jejich civilizace je tvořena výhradně ženami; nové generace vznikají reprodukčními metodami, které produkují pouze dcery.</p><div class="badges"><span class="badge o">Limen</span><span class="badge">Interdictio pozastaveno</span><span class="badge">Recensio probíhá</span><span class="badge">civilizace pouze žen</span></div></article>
<article class="card half"><span class="label green">spojenec // HELIOS</span><h3>Říše HELIOS</h3><p>HELIOS — Energy and Logistics Orbital Systems — je rozsáhlá mnohosvětová civilizace a hlavní strategický spojenec OSKN. Je několikanásobně větší než OSKN, zahrnuje lidi, mrazivé obry, elfy, temné elfy, trpaslíky, pso-lidi a další druhy a poskytuje obrovské surovinové, výrobní a logistické kapacity.</p><p>V čele stojí <b>Delta 7</b>. Vztah s Danielem Havelem se vyvinul v blízké přátelství a strategické partnerství; OSKN na oplátku dodává vojenské a experimentální technologie a ochranu.</p></article>
<article class="card half"><span class="label green">centrum OSKN</span><h3>OSKN po přesunu na Protos Singulár</h3><p>Současné OSKN už není jen posádka jedné lodi. Jde o obrannou organizaci se silným průmyslovým a vojenským zázemím na Protos Singulár. Organizace vznikla s doktrínou ochrany, záchrany a zastavování hrozeb, ale pod tlakem posledních konfliktů se výrazně militarizovala a centralizovala.</p><p>Jejím vrchním velitelem je <b>Daniel Havel</b>; jeho pravou rukou a faktickou spol velitelkou je <b>Kaelith Reinhard</b>.</p></article>'''
insert_into_section('factions', factions, 'Custodes Liminis — Strážci prahu')

ships = '''
<article class="card full"><span class="label red">OSKN // dreadnought</span><h3>Protector V52</h3><p>Protector V52 je těžký dreadnought navržený pro boj proti protivníkovi schopnému během sekund vyřadit pokročilé lodní systémy. Konstrukce používá decentralizované přežívací citadely, oddělené řízení, izolovanou elektroniku, lokální napájení a několik vrstev obrany. Filozofie je záměrně jednoduchá: když je vyřazena technologicky nejpokročilejší vrstva, pod ní zůstává jednodušší vrstva schopná pokračovat v boji.</p><p>Výzbroj zahrnuje těžkou kinetiku, MAC kanóny, iontové a EMP systémy, termonukleární roje a ochranu proti singularitním a antihmotovým hrozbám. Během Recensia vzrostl počet dokončených lodí až na <b>130 Protectorů V52</b>.</p><div class="metric-row"><div class="metric"><strong>130</strong><span>dokončených Protectorů</span></div><div class="metric"><strong>30</strong><span>nasazeno u Caelum‑9</span></div><div class="metric"><strong>12</strong><span>vysláno za ustupujícími Custodes</span></div><div class="metric"><strong>V52</strong><span>těžký dreadnought OSKN</span></div></div></article>
<article class="card half"><span class="label green">NII // aktuální technický stav</span><h3>NII-88 / Sojuz</h3><p>Aktuální zdroj uvádí délku <b>424 metrů</b>, šířku přibližně 155 metrů a hmotnost kolem 220 000 tun. NII dokáže přistávat na planetách a nese silné pancéřování, částicové štíty a Faradayovu supermřížku.</p><p>Její původní FTL systém umožňuje <b>pět rychlých skoků</b>, po kterých následuje přibližně <b>pětihodinová obnova</b>.</p></article>'''
insert_into_section('ships', ships, '130</strong><span>dokončených Protectorů')

history = '''
<article class="card full"><span class="label red">aktuální dějová vrstva // Custodes</span><h3>Interdictio → Recensio</h3><p>Po odmítnutí ultimáta Custodes zahájily Interdictio. První střety ukázaly schopnost během sekund vyřazovat běžné flotily bez nutnosti lodě fyzicky rozstřílet. Právě tato zkušenost vedla k masové výrobě Protectorů V52.</p><p>Po prvním skutečném střetu byly z vraků zachráněny <b>12 Custodes</b> v kritickém stavu. OSKN s nimi zacházelo jako s pacientkami, bez násilných výslechů a experimentování. Interdictio bylo následně pozastaveno a nahrazeno procesem Recensio — novým vyhodnocením civilizačního potenciálu OSKN a HELIOS.</p><p>Původní model Custodes selhal: místo omezení vojenského rozvoje vzniklo během dalších měsíců nejprve 36 a následně <b>130 dokončených Protectorů V52</b>. Současně přitom OSKN pokračovalo v záchraně poražených protivníků, což narušilo custodský předpoklad, že rychlá militarizace nutně znamená rostoucí agresivitu.</p></article>
<article class="card full"><span class="label red">Caelum‑9 // testovací útok Custodes</span><h3>Bitva u Caelum‑9</h3><p>Custodes vyslaly do soustavy Caelum‑9 v prostoru HELIOSU tři Titány, devět bitevních lodí a dvanáct těžkých křižníků. Operaci označily jako simulaci vojenského úderu a jejím cílem bylo otestovat obranu a zničit několik výzkumných center. Proti nim bylo okamžitě vysláno třicet Protectorů V52 a do boje dorazila také NII.</p><p>NII odpálila plnou salvu <b>10 singularitních hlavic Omega−</b> rozdělených proti deseti různým lodím. Věž Tiger II následně systematicky zasahovala pohonné sekce a vyřazovala další cíle z pohybu. Do boje byly nasazeny také testovací <b>Inverzní kauzální hlavice 120/100 — Paracausal+</b>, vyvinuté temnými elfy a mrazivými obry.</p><p>Custodes se nakonec stáhly. Dvanáct nepoškozených Protectorů dostalo rozkaz ustupující lodě sledovat a sbírat navigační a taktické informace bez vyvolání dalšího střetu.</p></article>'''
insert_into_section('history', history, 'Bitva u Caelum‑9')

missions = '''
<article class="card full"><span class="label green">záchranná operace // Custodes</span><h3>54 zachráněných po Caelum‑9</h3><p>Po stažení custodských sil zahájilo OSKN druhou velkou záchrannou operaci. Každá ozbrojená přeživší dostala výzvu k odložení zbraně; kdo ji odložil, byl chráněn a ošetřen. Popravy zajatých ani dorážení raněných byly výslovně zakázány.</p><p>Z vraků bylo zachráněno <b>54 Custodes</b>. Průzkum současně ukázal, že jejich lodě mají extrémně malé posádky, většinou do třiceti osob, protože většinu provozu zajišťuje automatika. Zachráněné byly převezeny do nemocničního oddělení na NII.</p><div class="metric-row"><div class="metric"><strong>54</strong><span>zachráněných Custodes</span></div><div class="metric"><strong>≤30</strong><span>typická posádka custodské lodi</span></div><div class="metric"><strong>NII</strong><span>nemocniční oddělení</span></div></div></article>'''
insert_into_section('missions', missions, '54 zachráněných po Caelum‑9')

locations = '''
<article class="card full"><span class="label green">domovský svět OSKN</span><h3>Protos Singulár</h3><p>Protos Singulár je současným politickým, průmyslovým a kulturním centrem OSKN. Jde o obrovskou planetu s <b>32hodinovým dnem</b>, sladkovodními oceány a populací přibližně <b>půl miliardy obyvatel</b>. Žijí zde lidé, Ursani, kočko-lidé, Vampirus, pso-lidé a další druhy.</p><p>Po bitvě u Caelum‑9 na Protos Singulár přistála přímo NII i se zachráněnými Custodes na palubě. Samotná možnost planetárního přistání tak velké válečné lodě byla pro pacientky překvapivá stejně jako způsob, jakým s nimi OSKN zacházelo.</p><div class="metric-row"><div class="metric"><strong>32 h</strong><span>délka dne</span></div><div class="metric"><strong>≈0,5 mld.</strong><span>populace</span></div><div class="metric"><strong>sladká voda</strong><span>oceány</span></div><div class="metric"><strong>OSKN</strong><span>hlavní centrum</span></div></div></article>
<article class="card half"><span class="label red">HELIOS // bojiště</span><h3>Caelum‑9</h3><p>Soustava v prostoru HELIOSU, kde proběhl testovací útok Custodes proti výzkumným centrům a následná bitva s třiceti Protectory V52 a NII.</p></article>'''
insert_into_section('locations', locations, 'Protos Singulár</h3>')

research = '''
<article class="card full"><span class="label green">FTL průlom // aktuální vývoj</span><h3>Nadprostorový a podprostorový pohon</h3><p>Během Recensia vznikly dva nové potvrzené FTL principy. <b>Nadprostorový pohon — 88/100, S</b> krátkodobě přesouvá loď do vyšší vrstvy reality s jinou geometrií vzdáleností. První funkční prototyp byl namontován na <b>A7</b>. O týden později vznikl <b>Podprostorový pohon — 84/100, S</b>, využívající naopak nižší prostorovou vrstvu.</p><p>Vznik obou systémů znamená zásadní změnu proti starší archivní vrstvě, ve které byla NII jediným potvrzeným nositelem FTL. NII zůstává unikátní svým původním pětiskokovým systémem, ale už není jedinou lodí spojenou s funkční FTL technologií.</p><div class="table-wrap"><table><thead><tr><th>Systém</th><th>Hodnocení</th><th>Třída</th><th>Potvrzený stav</th></tr></thead><tbody><tr><td><strong>Nadprostorový pohon</strong></td><td><b>88/100</b></td><td>S</td><td>první funkční prototyp na A7</td></tr><tr><td><strong>Podprostorový pohon</strong></td><td><b>84/100</b></td><td>S</td><td>funkční princip potvrzen; konkrétní nosič zde neurčen</td></tr></tbody></table></div></article>
<article class="card full"><span class="label red">zbraňový průlom // Caelum‑9</span><h3>Inverzní kauzální hlavice — 120/100</h3><p>Testovací hlavice vyvinutá společně temnými elfy a mrazivými obry je vedena jako <b>120/100 — Paracausal+</b>. Nenapadá pouze hmotu cíle, ale obrací jeho příčinné vazby. Při bojovém nasazení u Caelum‑9 některé systémy selhaly ještě před fyzickým přiblížením hlavice a jeden custodský Titán byl vyřazen chaotickým zhroucením vlastní kauzality.</p><div class="badges"><span class="badge o">120/100</span><span class="badge">Paracausal+</span><span class="badge">Temní Elfové</span><span class="badge">Mraziví obři</span><span class="badge">bojově ověřeno</span></div></article>'''
insert_into_section('upgrades', research, 'Nadprostorový a podprostorový pohon')

diplomacy = '''
<article class="card full"><span class="label green">Recensio // behaviorální anomálie</span><h3>Proč Custodes přestávají rozumět OSKN</h3><p>Model Custodes očekával, že rychle militarizovaná civilizace bude zároveň agresivnější a méně kontrolovatelná. OSKN však ve stejné době masově vyrábí dreadnoughty, vyvíjí nové FTL a parakauzální zbraně — a současně zachraňuje raněné protivníky, odmítá experimenty na zajatcích a integruje bývalé nepřátele.</p><p>Daniel Havel navštěvuje zachráněné Custodes denně, komunikuje s nimi latinsky a nosí jim knihy, ovoce, seriály a stolní hry. Často jej doprovází <b>Adriana</b>, členka rasy Vampirus, která na NII žije dobrovolně a není vězeň ani pokusný subjekt. Její přítomnost je pro Custodes dalším rozporem vůči jejich historickým modelům druhu Vampirus.</p><div class="badges"><span class="badge o">Recensio</span><span class="badge">záchrana nepřítele</span><span class="badge">Adriana / Vampirus</span><span class="badge">model Custodes selhává</span></div></article>'''
insert_into_section('diplomacy', diplomacy, 'Proč Custodes přestávají rozumět OSKN')

weapons = '''
<article class="card full"><span class="label red">operačně potvrzeno // Caelum‑9</span><h3>Omega− a Paracausal+ v reálném nasazení</h3><p>NII při Caelum‑9 odpálila plnou salvu <b>10 singularitních hlavic Omega−</b>, každou proti jinému cíli. Ve stejné bitvě byly poprvé bojově potvrzeny Inverzní kauzální hlavice 120/100 — Paracausal+. Záznam tak přesouvá oba systémy z čistě katalogové roviny do potvrzeného operačního použití.</p></article>'''
insert_into_section('arsenal', weapons, 'Omega− a Paracausal+ v reálném nasazení')

intel = '''
<article class="card full"><span class="label red">aktuální strategický stav // Recensio</span><h3>Interdictio je pozastavené. Recensio pokračuje.</h3><p>Custodes Liminis po nečekaných ztrátách nepokračují v otevřené ofenzivě, ale celý prostor OSKN–HELIOS nadále sledují a znovu vyhodnocují. Jejich původní model vývoje selhal: místo zpomalení vojenského programu má OSKN již <b>130 dokončených Protectorů V52</b>, rozšiřující se výrobní kapacity, dva nové FTL principy a bojově nasazené parakauzální zbraně.</p><p>Zároveň Custodes pozorují skutečnost, že jejich vlastní ranění jsou zachraňováni, léčeni a chráněni. Po Caelum‑9 bylo zachráněno 54 dalších příslušnic jejich civilizace a NII s nimi následně přistála na Protos Singulár. Největší otevřenou otázkou už proto není pouze další útok, ale výsledek samotného Recensia — tedy jak Custodes klasifikují civilizaci, která kombinuje prudký vojenský růst s ochranou poraženého nepřítele.</p><div class="metric-row"><div class="metric"><strong>130</strong><span>Protectorů V52</span></div><div class="metric"><strong>54</strong><span>zachráněných po Caelum‑9</span></div><div class="metric"><strong>Recensio</strong><span>aktuální režim</span></div><div class="metric"><strong>pozastaveno</strong><span>Interdictio</span></div></div></article>'''
insert_into_section('intel', intel, 'Interdictio je pozastavené. Recensio pokračuje.')

archive = '''
<article class="card half"><span class="label green">ARC-CUSTODES</span><h3>Custodes // záchranné protokoly</h3><p>První střet: 12 zachráněných v kritickém stavu. Caelum‑9: dalších 54 zachráněných. Obě skupiny byly vedeny jako pacientky a databáze výslovně odděluje ošetření od výslechu nebo experimentování.</p></article><article class="card half"><span class="label">ARC-PROTECTOR-V52</span><h3>Výrobní skok OSKN</h3><p>Během Recensia vzrostl stav z 36 Protectorů na 130 dokončených dreadnoughtů a výrobní kapacita pokračuje v růstu.</p></article>'''
insert_into_section('archive', archive, 'ARC-PROTECTOR-V52')

checks = ['Custodes Liminis — Strážci prahu','130</strong><span>dokončených Protectorů','Bitva u Caelum‑9','54 zachráněných po Caelum‑9','Protos Singulár</h3>','Nadprostorový a podprostorový pohon','Inverzní kauzální hlavice — 120/100','Interdictio je pozastavené. Recensio pokračuje.']
for c in checks:
    if c not in html:
        raise SystemExit(f'missing canonical update marker: {c}')

index.write_text(html, encoding='utf-8')
print('CURRENT_CANON_20260916_OK', index.stat().st_size)
