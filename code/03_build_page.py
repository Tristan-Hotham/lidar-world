"""Fill the page template with the coverage table, the gallery and the source list."""
import json, html, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
L = json.load(open('data/layers.json')); F = json.load(open('data/finds.json'))
t = open('code/page_template.html').read()
e = html.escape
rows = ''.join(f'<tr><td>{e(l["name"])}</td><td>{e(l["res"])}</td><td><a href="{e(l["link"])}">{e(l["by"])}</a></td><td>{e(l["lic"])}</td><td><button data-fly="{l["id"]}">Go</button></td></tr>\n'
               for l in sorted(L, key=lambda l: l['name']))
byid = {l['id']: l for l in L}
cards = []
for i, f in enumerate(F):
    alt = f'Lidar shaded relief of {f["name"]}, {f["place"]}'
    cards.append(f'<article class="find" id="find-{f["id"]}"><img src="img/finds/{f["id"]}.jpg" alt="{e(alt)}" loading="lazy" width="600" height="400">'
                 f'<div class="b"><h3><i>{i+1}</i>{e(f["name"])}</h3><div class="pl">{e(f["place"])} · {e(byid[f["layer"]]["name"])} lidar</div>'
                 f'<p>{e(f["text"])}</p><div class="acts"><button data-find="{f["id"]}">Show on map</button><a href="{e(f["wiki"])}">Wikipedia</a></div></div></article>')
src = ''.join(f'<li>{e(l["name"])}: <a href="{e(l["link"])}">{e(l["by"])}</a>, {e(l["res"])}. Licence: {e(l["lic"])}.</li>' for l in sorted(L, key=lambda l: l['name']))
t = (t.replace('{{COVERAGE_ROWS}}', rows).replace('{{FINDS}}', '\n'.join(cards)).replace('{{SOURCES}}', src)
       .replace('{{FULLSCREEN}}', open('code/fullscreen_snippet.html').read()))
assert '{{' not in t
open('index.html', 'w').write(t)
print('ok', len(t))
