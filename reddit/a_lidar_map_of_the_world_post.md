# Reddit post: A lidar map of the world

**Suggested subreddits:** r/MapPorn, r/dataisbeautiful (as [OC]), r/archaeology, r/geography, r/gis

**Title:** I joined 15 countries' national lidar surveys into one zoomable map of the world. This is what the ground looks like with the trees taken away [OC]

**Body:**

Lidar is a laser fired from a plane hundreds of thousands of times a second. Keep only the pulses that reach the ground and you get the bare earth: the land with every tree, crop and building lifted off. Light it from the top left and every bank and ditch throws a shadow.

Lots of countries publish their lidar openly, but each in its own viewer. I put fifteen of them in one map (England, Flanders, the Netherlands, France, NRW and Bavaria, Czechia, Austria, Switzerland, Slovenia, Luxembourg, Spain, Norway, Japan and the US) over a world shaded relief, with a gallery of 23 places: hillforts, Neolithic flint mines, the craters of Messines, Vimy and Verdun under forest, Japan's largest burial mound, Cahokia, karst sinkholes and three landslides. There's an aerial photo layer you can fade in to see how much the camera misses.

Interactive map: https://maps.tristanhotham.com/lidar-world/

Write-up: https://blog.tristanhotham.com/2026/10/31/lidar-world/

Paper, data and code: https://doi.org/10.5281/zenodo.23866756

**Data:** Environment Agency (OGL v3), IGN France LiDAR HD, Digitaal Vlaanderen, AHN/PDOK, swisstopo, Kartverket, USGS 3DEP, GSI Japan, IGN Spain, basemap.at, ČÚZK, Bavarian survey, Geobasis NRW, GURS Slovenia, Luxembourg ACT; Esri World Hillshade for everywhere else. **Tools:** MapLibre GL JS, Python. Images are screenshots of the map.

Scotland, Wales, Ireland, Denmark, Sweden and NZ have open lidar too, but none publish a keyless shaded web layer a map like this can load, so they fall back to the coarse world relief.

**First comment (for r/dataisbeautiful):** Source and tools as above. Each layer is loaded live from the agency's own WMS/WMTS, nothing is copied; coverage outlines are from Natural Earth.
