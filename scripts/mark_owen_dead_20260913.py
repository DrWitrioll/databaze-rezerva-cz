from pathlib import Path
import re

PATH = Path('dist/index.html')
html = PATH.read_text(encoding='utf-8')

# --- Global current-state counts ---
replacements = {
    'stav osazenstva: 232 evidovaných / 230 fyzických': 'stav osazenstva: 231 aktivních / 229 fyzických',
    '<div class="spec"><b>232</b><span>aktuálně evidováno</span></div>': '<div class="spec"><b>231</b><span>aktuálně aktivních</span></div>',
    '<tr><td>Současně evidováno</td><td><strong>232 členů / entit</strong></td></tr>': '<tr><td>Současně aktivní osazenstvo</td><td><strong>231 členů / entit</strong> <span class="state bad">+ 1 zemřelý archivní záznam</span></td></tr>',
    '<td>420 projektovaně / 232 evidováno</td>': '<td>420 projektovaně / 231 aktivních</td>',
    '<div class="section-head"><div><span class="code">CREW-05 // PERSONÁL</span><h2>Posádka a postavy</h2><p>Jmenné jádro NII tvoří 22 členů/entit včetně Holly a Arnolda Rimmera. K nim byly ve dvou vlnách přijaty další 210 fyzické osoby z mezirasové civilizace: 50 kočko-lidí, 50 pso-lidí, 60 trpaslíků a 50 ještěřanů.</p></div><div class="stamp">232 evidováno // 230 fyzických + hologram + AI</div></div>': '<div class="section-head"><div><span class="code">CREW-05 // PERSONÁL</span><h2>Posádka a postavy</h2><p>Jmenný registr NII obsahuje 22 záznamů včetně Holly, Arnolda Rimmera a zemřelého Owena Mercera. Aktivní jmenné jádro má po Mercerově smrti 21 členů/entit. K nim náleží dalších 210 fyzických osob z mezirasové civilizace: 50 kočko-lidí, 50 pso-lidí, 60 trpaslíků a 50 ještěřanů.</p></div><div class="stamp">231 aktivních // 229 fyzických + hologram + AI // Owen Mercer †</div></div>',
    'Jmenné jádro vzniklo z původního Argusu, pozdějších přírůstků a šesti přeživších z Helioru a má 22 členů/entit. Později NII přijala 60 nových členů z mezirasové stanice a při další evakuaci dalších 150 již vycvičených osob. Současný registr tak eviduje 232 členů/entit.': 'Jmenný registr vznikl z původního Argusu, pozdějších přírůstků a šesti přeživších z Helioru a obsahuje 22 záznamů. Po smrti Owena Mercera je z tohoto jádra aktivních 21 členů/entit. Později NII přijala 60 nových členů z mezirasové stanice a při další evakuaci dalších 150 již vycvičených osob. Současný aktivní stav je tedy 231 členů/entit; archiv personálu nadále uchovává Mercerův záznam.',
    '<div class="metric"><strong class="orange">22</strong><span>jmenné jádro</span></div>': '<div class="metric"><strong class="orange">21</strong><span>aktivní jmenné jádro</span></div>',
    '<span class="label">personální registr</span><h3>22 jmenných záznamů</h3>': '<span class="label">personální registr</span><h3>22 jmenných záznamů // 21 aktivních</h3>',
    '<div class="crew" data-groups="argus"><b>Owen Mercer</b><small>lodní systémy a nouzové postupy</small><span class="type">člověk // palubní systémy</span></div>': '<div class="crew" data-groups="argus"><b>Owen Mercer †</b><small>ZEMŘEL // lodní systémy a nouzové postupy</small><span class="type" style="color:var(--red)">člověk // zemřel</span></div>',
    '<span class="caption">SKUPINOVÝ VIZUÁLNÍ ZÁZNAM // POSÁDKA NII</span>': '<span class="caption">HISTORICKÝ SKUPINOVÝ ZÁZNAM // OWEN MERCER POZDĚJI ZEMŘEL</span>',
    '<article class="deep-card full"><span class="label">personální registr</span><h3>232 evidovaných členů, několik vrstev původu</h3><p>Jmenné jádro tvoří 22 členů/entit. K němu přibylo 210 fyzických členů ze čtyř ras mezirasové civilizace. Celkem je tedy evidováno 232 členů/entit; 230 je fyzicky na palubě, Rimmer je hologram a Holly centrální AI.</p>': '<article class="deep-card full"><span class="label">personální registr</span><h3>231 aktivních členů // 232 personálních záznamů</h3><p>Historický jmenný registr obsahuje 22 členů/entit, ale Owen Mercer je nyní veden jako zemřelý. Aktivních jmenných členů/entit je proto 21. K nim náleží 210 fyzických členů ze čtyř ras mezirasové civilizace. Aktivní stav NII je 231 členů/entit; 229 je fyzických, Rimmer je hologram a Holly centrální AI.</p>',
    '<div class="metric"><strong>232</strong><span>celkem evidováno</span></div>': '<div class="metric"><strong>231</strong><span>aktivních</span></div>',
    '<div class="metric"><strong>230</strong><span>fyzicky na palubě</span></div>': '<div class="metric"><strong>229</strong><span>aktivních fyzických členů</span></div>',
    '<article class="deep-card half"><span class="label">směnová realita</span><h3>22 není projektovaný stav</h3><p>NII pracuje s výrazně menším osazenstvem, než pro jaké byla velká loď navržena. Automatizace, androidi a Holly proto nejsou jen pohodlný bonus, ale důležitá součást provozu a směnového pokrytí.</p></article>': '<article class="deep-card half"><span class="label">směnová realita</span><h3>21 aktivních jmenných členů není projektovaný stav</h3><p>NII pracuje s výrazně menším jmenným jádrem, než pro jaké byla velká loď navržena. Smrt Owena Mercera navíc snížila počet aktivních fyzických členů původního jádra. Automatizace, androidi a Holly proto nejsou jen pohodlný bonus, ale důležitá součást provozu a směnového pokrytí.</p></article>',
    '<p>Současná NII má 232 evidovaných členů/entit: 22členné jmenné jádro a 210 dalších členů ze čtyř ras mezirasové civilizace. Celkem jde o 50 kočko-lidí, 50 pso-lidí, 60 trpaslíků a 50 ještěřanů mimo původní jmenné jádro.</p>': '<p>Současná NII má 231 aktivních členů/entit. Personální archiv obsahuje 232 záznamů, protože Owen Mercer po své smrti zůstává veden historicky. Aktivní jmenné jádro má 21 členů/entit a vedle něj je 210 dalších členů ze čtyř ras mezirasové civilizace: 50 kočko-lidí, 50 pso-lidí, 60 trpaslíků a 50 ještěřanů.</p>',
    '<p>Aktuální databáze eviduje <b>232 členů/entit</b>: 22 jmenných záznamů a 210 dalších členů vedených skupinově podle druhu. Fyzicky je na palubě 230 osob nebo androidních jednotek; Arnold Rimmer je hologram a Holly centrální AI. NII má konstrukční kapacitu až 420 členů a čtyřletou autonomii při plném projektovaném stavu.</p>': '<p>Aktuální databáze vede <b>232 personálních záznamů</b>, z nichž 231 představuje aktivní členy/entity. Owen Mercer je veden jako zemřelý. Aktivních fyzických osob nebo androidních jednotek je 229; Arnold Rimmer je hologram a Holly centrální AI. NII má konstrukční kapacitu až 420 členů a čtyřletou autonomii při plném projektovaném stavu.</p>',
    '<article class="card"><span class="label green">personální stav</span><h3>Osazenstvo</h3><div class="metric-row" style="grid-template-columns:1fr 1fr"><div class="metric"><strong>232</strong><span>evidováno</span></div><div class="metric"><strong>230</strong><span>fyzicky na palubě</span></div></div><p>Součet zahrnuje 20 fyzických členů původního jmenného jádra, 210 dalších fyzických členů ze čtyř ras, hologram Arnolda Rimmera a centrální AI Holly.</p></article>': '<article class="card"><span class="label green">personální stav</span><h3>Osazenstvo</h3><div class="metric-row" style="grid-template-columns:1fr 1fr"><div class="metric"><strong>231</strong><span>aktivních</span></div><div class="metric"><strong>229</strong><span>aktivních fyzických členů</span></div></div><p>Aktivní stav tvoří 19 fyzických členů původního jmenného jádra, 210 dalších fyzických členů ze čtyř ras, hologram Arnolda Rimmera a centrální AI Holly. Owen Mercer je samostatně veden jako zemřelý archivní záznam.</p></article>',
    '<article class="deep-card"><span class="label">personál</span><h3>232 evidovaných</h3><p>Personální stav je součástí inventáře pouze jako operační kapacita, ne jako „majetek“. Aktuálně je vedeno 232 členů/entit; 230 je fyzicky na palubě, Rimmer je hologram a Holly centrální AI.</p></article>': '<article class="deep-card"><span class="label">personál</span><h3>231 aktivních // 232 záznamů</h3><p>Personální stav je součástí inventáře pouze jako operační kapacita, ne jako „majetek“. Aktuálně je aktivních 231 členů/entit; 229 je fyzických, Rimmer je hologram a Holly centrální AI. Owen Mercer zůstává v personálním archivu jako zemřelý.</p></article>',
}

for old, new in replacements.items():
    if old in html:
        html = html.replace(old, new, 1)

# Owen in the detailed personnel table.
html = re.sub(
    r'<tr><td><strong>Owen Mercer</strong></td><td>člověk</td><td>palubní systémy / nouzové postupy</td><td>.*?</td></tr>',
    '<tr><td><strong>Owen Mercer †</strong></td><td>člověk</td><td>palubní systémy / nouzové postupy</td><td><span class="state bad">ZEMŘEL</span> — datum, místo a okolnosti smrti zatím nejsou v databázi určeny</td></tr>',
    html,
    count=1,
)

# Add a canonical status card to the crew section.
crew_marker = '<!-- EXPANSION: CREW -->'
memorial = '''
<article class="card full">
<span class="label red">stavový záznam // ZEMŘEL</span>
<h3>Owen Mercer †</h3>
<p>Owen Mercer, původní člen rezervní posádky KRV-114 Argus a specialista na lodní systémy a nouzové postupy, zemřel. Datum, místo a přesné okolnosti jeho smrti zatím nejsou v dostupném kánonu určeny, proto je databáze nedoplňuje odhadem.</p>
<div class="badges"><span class="badge o">Owen Mercer</span><span class="badge">původní Argus</span><span class="badge">palubní systémy</span><span class="badge" style="border-color:var(--red);color:var(--red)">ZEMŘEL</span></div>
</article>
'''
if 'stavový záznam // ZEMŘEL' not in html and crew_marker in html:
    html = html.replace(crew_marker, memorial + crew_marker, 1)

# Add an undated archive/chronology record; no invented in-universe date.
history_marker = '<section class="page" id="missions">'
history_card = '''
<article class="card half"><span class="label red">datum neurčeno // personální ztráta</span><h3>Úmrtí Owena Mercera</h3><p>Owen Mercer, člen původní jedenáctičlenné posádky Argusu, zemřel. Přesné datum, místo a příčina smrti nejsou zatím potvrzeny. Událost snižuje aktivní stav NII na 231 členů/entit, z toho 229 fyzických.</p><div class="badges"><span class="badge o">Owen Mercer †</span><span class="badge">stav potvrzen</span><span class="badge">okolnosti neurčeny</span></div></article>
'''
if 'Úmrtí Owena Mercera' not in html:
    pos = html.find(history_marker)
    if pos != -1:
        hist_start = html.rfind('<section class="page" id="history">', 0, pos)
        hist_close = html.rfind('</div>\n</section>', hist_start, pos)
        if hist_close != -1:
            html = html[:hist_close] + history_card + html[hist_close:]

# Final safeguards.
required = [
    'Owen Mercer †',
    '231 aktivních',
    '229 fyzických',
    'ZEMŘEL',
]
for marker in required:
    if marker not in html:
        raise SystemExit(f'Missing required Owen-update marker: {marker}')

PATH.write_text(html, encoding='utf-8')
print('OWEN_UPDATE_OK', PATH.stat().st_size)
