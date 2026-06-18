# Blazhko and LTTE Visualizer

Static web app for exploring a theoretical RR Lyrae light curve with optional Blazhko modulation and light travel time effect phase shifts.

The browser reads `data/theoretical_lightcurve.json`, generated from the OGLE-based Fourier template and fitted default parameters by:

```bash
python .\scripts\build_lightcurve.py
```

You can also open `index.html` directly in Chrome. The app includes `data/theoretical_lightcurve.js` as a local-file data wrapper because Chrome blocks `fetch()` requests to JSON files from `file://` pages.

Run locally from this directory with:

```bash
python -m http.server 8765
```
