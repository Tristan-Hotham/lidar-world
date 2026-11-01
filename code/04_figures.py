"""Header, blog images and the Reddit collage, from the map screenshots in qa/shots (taken with ?shot)."""
import json, os
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
FD = os.path.expanduser('~/.fonts/')
def font(n, s, var=None):
    f = ImageFont.truetype(FD + n, s)
    if var:
        try: f.set_variation_by_axes(var)
        except Exception: pass
    return f
INK = (31, 35, 38); HOT = (194, 65, 12); PAPER = (244, 242, 238); MUTED = (98, 104, 109)
F = json.load(open('data/finds.json')); L = {l['id']: l for l in json.load(open('data/layers.json'))}
def shot(i): return Image.open(f'qa/shots/{i}.jpg').convert('RGB')
def cover(im, w, h):
    r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2; return im.crop((x, y, x + w, y + h))

# header 1200x630: Maiden Castle on the right, title on paper at left
H = Image.new('RGB', (1200, 630), PAPER)
H.paste(cover(shot('maiden-wide'), 760, 630), (440, 0))
d = ImageDraw.Draw(H)
d.rectangle([0, 0, 440, 630], fill=PAPER)
d.text((40, 52), 'THE BARE EARTH', font=font('IBMPlexMono-Medium.ttf', 20), fill=HOT)
big = font('FrauncesVar.ttf', 76, [144, 900, 0, 0])
y = 96
for line, col in [('A lidar', INK), ('map of', INK), ('the world', HOT)]:
    d.text((38, y), line, font=big, fill=col); y += 84
d.text((40, y + 22), 'Fifteen national laser surveys\nin one zoomable map, and\n23 places they reveal.', font=font('SourceSerif4-Regular.ttf', 25), fill=INK, spacing=6)
d.text((40, 572), 'Maiden Castle, Dorset · EA lidar', font=font('IBMPlexMono-Regular.ttf', 14), fill=MUTED)
d.text((40, 594), 'maps.tristanhotham.com/lidar-world', font=font('IBMPlexMono-Medium.ttf', 15), fill=INK)
H.save('header.png', optimize=True)

# blog images (png, 1400x933) and a lidar/photo comparison
os.makedirs('release/blog', exist_ok=True)
for i in ['stonehenge', 'grimes-graves', 'verdun', 'daisen', 'skocjan', 'st-helens']:
    cover(shot(i), 1400, 933).save(f'release/blog/b_{i}.png', optimize=True)
def pair(a, b, la, lb, out):
    W, Hh = 1400, 560; im = Image.new('RGB', (W, Hh + 50), PAPER); d = ImageDraw.Draw(im)
    im.paste(cover(shot(a), 690, Hh), (0, 50)); im.paste(cover(shot(b), 690, Hh), (710, 50))
    fm = font('IBMPlexMono-Medium.ttf', 20); d.text((0, 14), la, font=fm, fill=INK); d.text((710, 14), lb, font=fm, fill=HOT)
    im.save(out, optimize=True)
pair('verdun-aerial', 'verdun', 'AERIAL PHOTO', 'LIDAR, SAME PLACE', 'release/blog/b_verdun-compare.png')
pair('maiden-aerial', 'maiden-castle', 'AERIAL PHOTO', 'LIDAR, SAME PLACE', 'img/maiden-compare.png')

# Reddit collage: 2000 wide, 12 tiles in a 3x4 grid, labels on paper strips under each tile, full legend at foot
pick = ['maiden-castle', 'grimes-graves', 'verdun', 'messines', 'old-sarum', 'daisen', 'skocjan', 'st-helens', 'hill-60', 'goldau', 'cahokia', 'vimy']
byid = {f['id']: (i + 1, f) for i, f in enumerate(F)}
cols, tw, th, gap, lab = 3, 640, 427, 20, 70
top = 230
rows = len(pick) // cols
Wd = cols * tw + (cols + 1) * gap
Ht = top + rows * (th + lab + gap) + 170
C = Image.new('RGB', (Wd, Ht), PAPER); d = ImageDraw.Draw(C)
d.text((gap, 40), 'THE BARE EARTH', font=font('IBMPlexMono-Medium.ttf', 26), fill=HOT)
d.text((gap - 2, 74), 'A lidar map of the world: what the ground looks like without the trees', font=font('FrauncesVar.ttf', 50, [144, 900, 0, 0]), fill=INK)
d.text((gap, 150), 'Twelve of 23 places from a map that joins fifteen national lidar surveys. Shaded relief, lit from the top left.', font=font('SourceSerif4-Regular.ttf', 28), fill=MUTED)
ft = font('SourceSerif4-Semibold.ttf', 27); fs = font('IBMPlexMono-Regular.ttf', 18)
for k, i in enumerate(pick):
    n, f = byid[i]; x = gap + (k % cols) * (tw + gap); y = top + (k // cols) * (th + lab + gap)
    C.paste(cover(shot(i), tw, th), (x, y))
    d.text((x, y + th + 8), f'{f["name"]}', font=ft, fill=INK)
    d.text((x, y + th + 42), f'{f["place"]} · {L[f["layer"]]["name"]} lidar', font=fs, fill=MUTED)
yb = Ht - 150
d.line([gap, yb, Wd - gap, yb], fill=INK, width=3)
leg = ('How to read it: each image is a digital terrain model from airborne lidar, the ground with vegetation and buildings removed, '
       'shaded as if lit from the north-west, so banks cast shadows to the bottom right and hollows are dark on their top-left side. '
       'Pale blue is water from OpenStreetMap.')
fl = font('SourceSerif4-Regular.ttf', 22)
words = leg.split(); line = ''; yy = yb + 14
for w in words:
    t = (line + ' ' + w).strip()
    if d.textlength(t, font=fl) > Wd - 2 * gap: d.text((gap, yy), line, font=fl, fill=INK); yy += 30; line = w
    else: line = t
d.text((gap, yy), line, font=fl, fill=INK)
d.text((gap, Ht - 40), 'Lidar: Environment Agency (OGL), IGN France, Digitaal Vlaanderen, GSI Japan, GURS Slovenia, USGS 3DEP, swisstopo. Map: maps.tristanhotham.com/lidar-world · Tristan Hotham, 2026',
       font=font('IBMPlexMono-Regular.ttf', 16), fill=MUTED)
os.makedirs('reddit', exist_ok=True)
C.save('reddit/a_lidar_map_of_the_world.png', optimize=True)
print('ok', C.size)
