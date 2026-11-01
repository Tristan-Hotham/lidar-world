/* The Bare Earth: a lidar map of the world.
   A MapLibre map that shows a global shaded relief and, inside each country or region that publishes one,
   the national lidar hillshade, loaded straight from the publisher's own open web service. */
(function () {
  'use strict';
  const OFM_STYLE = 'https://tiles.openfreemap.org/styles/positron';
  const ESRI_HS = 'https://server.arcgisonline.com/ArcGIS/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}';
  const ESRI_IMG = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
  const DEM = 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png';
  const PAPER = '#EDEBE6', WATER = '#C9D7E1', WATER_LINE = '#8FA9BC', INK = '#26292B';

  function wmsUrl(L) {
    const ts = 512;
    return L.url + '?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&LAYERS=' +
      encodeURIComponent(L.layer) + '&STYLES=' + encodeURIComponent(L.style || '') +
      '&CRS=EPSG:3857&WIDTH=' + ts + '&HEIGHT=' + ts + '&BBOX={bbox-epsg-3857}';
  }
  function sourceFor(L) {
    const s = { type: 'raster', bounds: L.bounds, attribution: L.by + ' (' + L.lic + ')' };
    if (L.kind === 'wms') { s.tiles = [wmsUrl(L)]; s.tileSize = 512; }
    else if (L.kind === 'arcgis') { s.tiles = [L.url]; s.tileSize = 512; }
    else { s.tiles = [L.url]; s.tileSize = L.ts || 256; if (L.maxzoom) s.maxzoom = L.maxzoom; }
    if (L.kind !== 'xyz') s.maxzoom = 19;
    return s;
  }

  // point in (multi)polygon, for the "showing" badge
  function inRing(p, r) { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const a = r[i], b = r[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]) c = !c; } return c; }
  function inGeom(p, g) {
    const polys = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
    return polys.some(pl => inRing(p, pl[0]) && !pl.slice(1).some(h => inRing(p, h)));
  }

  async function create(container, opts) {
    opts = opts || {};
    const [style, layers, coverage, finds] = await Promise.all([
      fetch(OFM_STYLE).then(r => r.json()),
      fetch('data/layers.json').then(r => r.json()),
      fetch('data/coverage.geojson').then(r => r.json()),
      fetch('data/finds.json').then(r => r.json()),
    ]);

    // keep the OpenFreeMap water, boundaries, roads and labels; drop land fills, buildings and parks
    const keep = [];
    for (const l of style.layers) {
      if (l.type === 'background') { l.paint = { 'background-color': PAPER }; keep.push(l); continue; }
      const sl = l['source-layer'] || '';
      if (l.type === 'fill' && sl === 'water') { l.paint = { 'fill-color': WATER, 'fill-opacity': 0.92 }; l.metadata = { g: 'water' }; keep.push(l); continue; }
      if (l.type === 'fill' || l.type === 'fill-extrusion') continue;
      if (l.type === 'line' && sl === 'waterway') { l.paint['line-color'] = WATER_LINE; l.metadata = { g: 'water' }; keep.push(l); continue; }
      if (l.type === 'line' && sl === 'boundary') { l.metadata = { g: 'borders' }; keep.push(l); continue; }
      if (l.type === 'line' && (sl === 'transportation' || sl === 'aeroway')) { l.metadata = { g: 'roads' }; l.layout = Object.assign({}, l.layout, { visibility: 'none' }); keep.push(l); continue; }
      if (l.type === 'symbol') {
        l.metadata = { g: (sl === 'transportation_name') ? 'roads' : 'labels' };
        if (sl === 'transportation_name') l.layout = Object.assign({}, l.layout, { visibility: 'none' });
        if (l.paint) { l.paint['text-color'] = sl === 'water_name' ? '#3F6680' : INK; l.paint['text-halo-color'] = 'rgba(245,244,240,0.92)'; l.paint['text-halo-width'] = 1.6; }
        keep.push(l); continue;
      }
      if (l.type === 'line') continue;
    }
    const bgIdx = keep.findIndex(l => l.type === 'background');
    const raster = [];
    style.sources.esrihs = { type: 'raster', tiles: [ESRI_HS], tileSize: 256, maxzoom: 16,
      attribution: 'World hillshade: Esri, Airbus, USGS, NGA, NASA, CGIAR, NLS, OS, NMA, Geodatastyrelsen, GSA, GSI and the GIS user community' };
    raster.push({ id: 'world-hs', type: 'raster', source: 'esrihs', metadata: { g: 'world' }, paint: { 'raster-fade-duration': 120 } });
    for (const L of layers) {
      style.sources['l-' + L.id] = sourceFor(L);
      const p = { 'raster-fade-duration': 150 };
      if (L.grey) p['raster-saturation'] = -1;
      raster.push({ id: 'lidar-' + L.id, type: 'raster', source: 'l-' + L.id, minzoom: L.minzoom, metadata: { g: 'lidar', lid: L.id }, paint: p });
    }
    style.sources.esriimg = { type: 'raster', tiles: [ESRI_IMG], tileSize: 256, maxzoom: 19, attribution: 'Aerial photos: Esri, Maxar, Earthstar Geographics and the GIS user community' };
    raster.push({ id: 'aerial', type: 'raster', source: 'esriimg', metadata: { g: 'aerial' }, layout: { visibility: 'none' }, paint: { 'raster-opacity': 0.5 } });
    keep.splice(bgIdx + 1, 0, ...raster);

    style.sources.coverage = { type: 'geojson', data: coverage };
    style.sources.finds = { type: 'geojson', data: { type: 'FeatureCollection', features: finds.map((f, i) => ({ type: 'Feature', id: i, properties: { i, name: f.name, n: i + 1 }, geometry: { type: 'Point', coordinates: [f.lon, f.lat] } })) } };
    style.sources.dem = { type: 'raster-dem', tiles: [DEM], tileSize: 256, maxzoom: 15, encoding: 'terrarium', attribution: 'Terrain: AWS Terrain Tiles (Mapzen)' };
    keep.push(
      { id: 'cov-fill', type: 'fill', source: 'coverage', metadata: { g: 'coverage' }, paint: { 'fill-color': '#C2410C', 'fill-opacity': ['interpolate', ['linear'], ['zoom'], 2, 0.10, 8, 0.03, 9, 0] } },
      { id: 'cov-line', type: 'line', source: 'coverage', metadata: { g: 'coverage' }, paint: { 'line-color': '#C2410C', 'line-width': ['interpolate', ['linear'], ['zoom'], 2, 0.8, 9, 1.6], 'line-dasharray': [3, 2], 'line-opacity': 0.85 } },
      { id: 'finds-c', type: 'circle', source: 'finds', metadata: { g: 'finds' }, paint: { 'circle-radius': ['interpolate', ['linear'], ['zoom'], 2, 5, 10, 8, 15, 11], 'circle-color': '#C2410C', 'circle-stroke-color': '#fff', 'circle-stroke-width': 2 } },
      { id: 'finds-n', type: 'symbol', source: 'finds', metadata: { g: 'finds' }, layout: { 'text-field': ['to-string', ['get', 'n']], 'text-font': ['Noto Sans Bold'], 'text-size': ['interpolate', ['linear'], ['zoom'], 2, 8, 10, 10, 15, 12], 'text-allow-overlap': true, 'text-ignore-placement': true }, paint: { 'text-color': '#fff' } },
      { id: 'finds-t', type: 'symbol', source: 'finds', minzoom: 5, metadata: { g: 'finds' }, layout: { 'text-field': ['get', 'name'], 'text-font': ['Noto Sans Bold'], 'text-size': 13, 'text-anchor': 'left', 'text-offset': [1.1, 0], 'text-optional': true }, paint: { 'text-color': '#9A3412', 'text-halo-color': 'rgba(255,255,255,.95)', 'text-halo-width': 2 } }
    );
    style.layers = keep;

    const map = new maplibregl.Map(Object.assign({
      container, style, hash: false, attributionControl: { compact: true }, maxPitch: 75,
      center: [-1.83, 51.18], zoom: 3, cooperativeGestures: false, fadeDuration: 150,
    }, opts.mapOptions || {}));
    await new Promise(r => map.on('load', r));
    map.__lidar = { layers, coverage, finds };
    return map;
  }

  function setGroup(map, g, on) {
    for (const l of map.getStyle().layers) if (l.metadata && l.metadata.g === g) map.setLayoutProperty(l.id, 'visibility', on ? 'visible' : 'none');
  }
  function setLidar(map, id, on) { if (map.getLayer('lidar-' + id)) map.setLayoutProperty('lidar-' + id, 'visibility', on ? 'visible' : 'none'); }

  // which layer is drawing at the centre of the map
  function showing(map) {
    const c = map.getCenter(), z = map.getZoom(), p = [c.lng, c.lat];
    const { layers, coverage } = map.__lidar;
    for (let i = layers.length - 1; i >= 0; i--) {
      const L = layers[i];
      if (map.getLayoutProperty('lidar-' + L.id, 'visibility') === 'none') continue;
      const f = coverage.features.find(f => f.properties.id === L.id);
      if (f && inGeom(p, f.geometry)) return { L, on: z >= L.minzoom };
    }
    return null;
  }

  window.LidarMap = { create, setGroup, setLidar, showing };
})();
