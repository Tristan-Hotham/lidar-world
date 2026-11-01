# The Bare Earth: a lidar map of the world

**Live map:** https://maps.tristanhotham.com/lidar-world/
**Paper, data and code:** https://doi.org/10.5281/zenodo.23866756

A zoomable world map that joins fifteen national lidar hillshade services (England, Flanders, the Netherlands, France, North Rhine-Westphalia, Bavaria, Czechia, Austria, Switzerland, Slovenia, Luxembourg, Spain, Norway, Japan and the United States) to a global shaded relief, with a gallery of 23 places where lidar shows landscapes hidden by trees, crops and time: hillforts, Roman mines, First World War craters, burial mounds and landslides.

Nothing is copied or stored. The page asks each agency's own open web map service (WMS or WMTS) for shaded relief as you pan and zoom, and draws it with MapLibre GL JS. Each layer is clipped to an outline of its country or region from Natural Earth.

## Layers

See `data/layers.json` for the service address, resolution, publisher and licence of each layer, and the table on the page.

## Files

- `index.html` the page (built by `code/03_build_page.py` from `code/page_template.html`)
- `js/lidar-map.js` the map
- `data/layers.json` the fifteen national services
- `data/coverage.geojson` outlines of the areas each service covers
- `data/finds.json` the 23 places in the gallery, with notes and Wikipedia links
- `code/layers.py`, `code/01_coverage.py`, `code/02_finds.py`, `code/03_build_page.py` build scripts
- `code/paper.py` builds the short paper

## Licences

Code MIT. Text, gallery notes and figures CC BY 4.0. The shaded relief images belong to their publishers and are used under the licences in `data/layers.json`. World shaded relief: Esri World Hillshade. Place names © OpenStreetMap contributors (ODbL), tiles by OpenFreeMap. Coverage outlines: Natural Earth (public domain).

## Cite

Hotham, T. (2026) The Bare Earth: a lidar map of the world. Zenodo. https://doi.org/10.5281/zenodo.23866756

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.
