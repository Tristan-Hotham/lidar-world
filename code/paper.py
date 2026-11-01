"""Builds the short paper (release/paper) from data/layers.json, data/finds.json and img/finds/.
Usage: python3 code/paper.py <DOI>"""
import json, os, re, subprocess, sys, shutil
ROOT = os.path.join(os.path.dirname(__file__), '..')
doi = sys.argv[1] if len(sys.argv) > 1 else '10.5281/zenodo.23866756'
L = json.load(open(os.path.join(ROOT, 'data', 'layers.json')))
F = json.load(open(os.path.join(ROOT, 'data', 'finds.json')))
def tex(s):
    s = str(s)
    for a, b in [('\\', r'\textbackslash{}'), ('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}'), ('~', r'\textasciitilde{}'), ('^', r'\^{}')]:
        s = s.replace(a, b)
    return re.sub(r'"([^"]*)"', r"``\1''", s)
def url(u): return u.replace('%', r'\%').replace('#', r'\#')
byid = {l['id']: l for l in L}
rows = '\n'.join(r'%s & %s & %s & %s\\' % (tex(l['name']), tex(l['res']), tex(l['by']), tex(l['lic'])) for l in sorted(L, key=lambda l: l['name']))
d = os.path.join(ROOT, 'release', 'paper'); os.makedirs(d, exist_ok=True)
figs = []
for i, f in enumerate(F):
    src = os.path.join(ROOT, 'img', 'finds', f['id'] + '.jpg')
    if os.path.exists(src): shutil.copy(src, os.path.join(d, 'f_' + f['id'] + '.jpg'))
    figs.append(r'''\begin{figure}[H]\centering\includegraphics[width=0.86\linewidth]{f_%s.jpg}
\caption*{\textbf{%d. %s}, %s. %s lidar (%s).}\end{figure}
%s \emph{Source: \href{%s}{Wikipedia, %s}.}
''' % (f['id'], i + 1, tex(f['name']), tex(f['place']), tex(byid[f['layer']]['name']), tex(byid[f['layer']]['by']), tex(f['text']), url(f['wiki']), tex(f['wiki'].rsplit('/', 1)[1].replace('_', ' '))))
body = r'''\documentclass[11pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{TeX Gyre Pagella}
\usepackage[a4paper,margin=2.2cm]{geometry}
\usepackage{graphicx,longtable,array,xcolor,float,caption,booktabs}
\usepackage{xurl}
\usepackage[hidelinks]{hyperref}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.55em}
\captionsetup{font=small,labelfont=bf}
\hypersetup{pdftitle={The Bare Earth: a lidar map of the world},pdfauthor={Tristan Hotham}}
\begin{document}
\begin{center}
{\Large\bfseries The Bare Earth\par}\vspace{0.4em}
{\large A lidar map of the world, joining fifteen national lidar surveys to a global shaded relief\par}\vspace{1.1em}
{\large Tristan Hotham\par}\vspace{0.3em}
{\small Independent researcher\\ ORCID: 0000-0003-4931-9349\\ DOI: \href{https://doi.org/@@DOI@@}{@@DOI@@}\par}\vspace{0.7em}
2026
\end{center}
\begin{quote}\small\begin{center}\textbf{Abstract}\end{center}
Airborne lidar has now been flown over all or most of many countries, and a growing number of national agencies publish shaded relief made from it as open web map services. They publish them separately. I join fifteen of these services (England, Flanders, the Netherlands, France, North Rhine-Westphalia, Bavaria, Czechia, Austria, Switzerland, Slovenia, Luxembourg, Spain, Norway, Japan and the United States) in one zoomable web map over a global shaded relief, so that the national survey takes over wherever one exists. Nothing is copied or stored: the page requests images from each publisher as the user moves. I document each service, its detail and licence, explain why several countries with open lidar cannot be included, and give a gallery of @@N@@ places where bare-earth lidar shows what vegetation, crops and time hide: hillforts and oppida, Neolithic mines, a deserted medieval village, First World War craters, a Roman gold mine, burial mounds, karst and landslides. The map is at \url{https://maps.tristanhotham.com/lidar-world/}.
\end{quote}
\section*{1. Lidar and the bare earth}
An airborne lidar scanner fires laser pulses at the ground, typically hundreds of thousands a second, and times each return. Many pulses return from leaves, roofs or crops, but some pass through gaps to the ground. Classifying the returns and keeping the ground points gives a digital terrain model (DTM), the land surface as if vegetation and buildings were removed. Rendered as shaded relief, lit from the north-west by cartographic convention, a DTM shows banks, ditches, mounds and hollows of a few tens of centimetres. This is why lidar has transformed landscape archaeology, especially in woodland, and the study of landslides and other landforms.
\section*{2. The services}
Each national layer is drawn from the publisher's own Web Map Service (WMS) or Web Map Tile Service (WMTS), requested in Web Mercator. I included a service only if it returned images to a page on another origin (cross-origin access), allowed reuse under an open licence or with credit, needed no key, and showed shaded relief or a usable rendering of the terrain model. Table~1 lists the fifteen that qualified. Two need comment. The Dutch AHN service renders the 0.5~m terrain model in colour by height, not as shading; I kept the colour. The Luxembourg service is a tinted shading, which I render in grey. Each layer is clipped to an outline of its country or region from Natural Earth, buffered slightly to keep coasts, and drawn from about zoom 9; tile services with lower zoom levels appear from zoom 5 or 6. Beneath them, the map uses Esri's World Hillshade, which is compiled from the best elevation its makers hold, including some national lidar.
{\small\begin{longtable}{>{\raggedright\arraybackslash}p{2.6cm}>{\raggedright\arraybackslash}p{3.6cm}>{\raggedright\arraybackslash}p{5.8cm}>{\raggedright\arraybackslash}p{3.2cm}}
\caption*{\textbf{Table 1.} National lidar layers on the map.}\\\toprule
Where & Detail & Publisher & Licence\\\midrule
@@ROWS@@
\bottomrule\end{longtable}}
\section*{3. Who is missing}
Scotland, Wales, Ireland, Denmark, Sweden, Finland and New Zealand all have national or near-national lidar that can be downloaded openly. None could be included: some publish no shaded relief service, some require a personal key or token for their map services, and some do not allow cross-origin image requests, which a browser map needs. Scotland's lidar portal, for example, serves the terrain model only as unshaded elevation. In these places the map falls back to the global relief. Making a shaded layer available as an open, keyless WMS or WMTS would be a small step with a large return for public use.
\section*{4. Reading the shading}
All the layers are lit from the north-west, the long-standing convention that matches the expectation that light comes from above; lit from the south, relief tends to invert in the eye. A single light direction has a known weakness: linear features parallel to the light cast almost no shadow and can disappear. Archaeological practice therefore uses several illuminations or illumination-free measures such as slope and sky-view factor. The map shows each publisher's single rendering, so absence of a feature in it is not evidence of absence on the ground.
\section*{5. Gallery}
Each place below was chosen because the lidar shows it clearly and was checked on the map; each note was checked against the Wikipedia article linked. Images are screenshots of the map at the zoom used by the gallery's ``Show on map'' button.
@@FIGS@@
\section*{Data and code}
Map, layer list, coverage outlines, gallery and this paper: \url{https://github.com/Tristan-Hotham/lidar-world} and DOI \href{https://doi.org/@@DOI@@}{@@DOI@@}. Code MIT; text, gallery notes and figures CC BY 4.0. The shaded relief in the figures belongs to the publishers in Table~1, used under their licences; world shaded relief by Esri. The author used an AI system to help draft code and text, and checked every factual claim against the sources given.
\end{document}
'''
body = body.replace('@@ROWS@@', rows).replace('@@FIGS@@', '\n'.join(figs)).replace('@@DOI@@', doi).replace('@@N@@', str(len(F)))
open(os.path.join(d, 'Hotham_The_Bare_Earth.tex'), 'w').write(body)
for _ in range(2): r = subprocess.run(['xelatex', '-interaction=nonstopmode', 'Hotham_The_Bare_Earth.tex'], cwd=d, capture_output=True, text=True)
print(r.stdout[-800:] if 'Output written' not in r.stdout else 'pdf ok')
