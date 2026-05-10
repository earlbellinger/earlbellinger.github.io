# Magellanic Cloud Atlas

Interactive static web app for exploring the Large and Small Magellanic Clouds with:

- OGLE-IV Classical Cepheids from Jacyszyn-Dobrzeniecka et al. 2016.
- OGLE-IV RR Lyrae from Jacyszyn-Dobrzeniecka et al. 2017.
- OGLE-IV Anomalous Cepheids from the OCVS, with distances from the Jacyszyn-Dobrzeniecka et al. 2019 Magellanic Bridge period-Wesenheit relation.
- OGLE-III Magellanic Mira variables from the OCVS LPV catalogs, with distances from published Iwanek et al. 2021 mid-infrared means/PLRs where available, AllWISE photometry on the same PLRs where not, and same-cloud neighbor estimates only for stars still missing reliable mid-IR distances.
- XMC red clump distance map from Oden et al. 2025.
- MIST-derived synthetic cluster stars seeded by Perren et al. 2017 and VISCACHA VII Magellanic Cloud cluster parameters.

The app uses a black canvas scene, browser-native JavaScript, and no package manager. Catalog stars are brightened by I-band luminosity derived from distance and magnitude, while point size is scaled by an estimated stellar radius from luminosity plus dereddened `V-I` color. The display is calibrated relative to an approximate red-clump reference of `M_I = -0.25`, using `M_I(Sun)=4.10`, with logarithmic compression so Cepheids and Miras do not wash out the map; per-dataset exposure sliders change camera/display gain for each visible class, not the catalog luminosities themselves. Spectral class is inferred from intrinsic `V-I_0` because most source tables do not include literal spectral-type labels; rendered color subtracts `E(V-I)` before converting to an approximate effective temperature, interpolates the full Mitchell Charity 2-degree sRGB D58 blackbody table, and applies display-only temperature/chroma contrast around the D58 whitepoint. Reddening defaults to Skowron et al. 2021, with He & Huang 2026 distance-dependent 3-D RR Lyrae values used where their partitions cover a star; stars outside both maps use same-cloud k=32 nearest-neighbor imputation from directly matched stars, with same-cloud median only as the sparse-neighborhood fallback.

The red-clump surface brightness is a hybrid visual/physical layer. The smoothed Gaia RC-like density map remains the primary opacity shape, with a red-clump-specific render gain so the current map brightness is the `1x` exposure baseline; the inferred unresolved red-clump count is only used as a bounded brightness nudge so the layer stays order-of-magnitude plausible without overwhelming the catalog stars. A light 3x3 grid smoothing pass and vertex-interpolated red-clump alpha soften cell edges without moving the distance surface. The red-clump surface lives on its own transparent WebGL layer beneath the catalog stars, caches cell alpha during projection rebuilds, and renders as an indexed quad mesh, so panning, clicking, and settled frames use the same compositing while avoiding a full mesh redraw on ordinary pulsation frames.

Stars pulsate with period-driven light curves. Where OGLE epoch photometry is available, `scripts/prepare_data.py` estimates a clipped unmodulated carrier: it median-bins the folded light curve with overlapping phase windows, iterates local MAD rejection, masks eclipse-like one-sided dips, then uses the accepted high-quality targets to build pooled `FO`, `FU`, and `RRab` phase-PCA bases. The basis-target Fourier fits cross-validate orders up to 14 plus a Laplace prior on harmonic amplitudes; a coarse grid initializes the prior strength and decay exponent, then a bounded local optimizer refines both against the held-out phase-bin CV score. Each fitted Fourier carrier is sampled into 1000 phase bins, PCA components are retained until they explain 99% of the variance, and every star is first fit to its median-binned carrier with a small phase-offset search before all raw I-band photometry is brought back for iterative MAD rejection and refitting against the PCA curve. The build writes cached Fourier features, training IDs, PCA components, holdout validation, per-star fit diagnostics, and Blazhko/eclipse candidate flags to `data/processed/` and `diagnostics/`. The browser therefore shows the stable carrier morphology rather than Blazhko modulation or companion eclipses. Stars without a reliable fitted carrier fall back to the current OGLE OCVS `T0`, I-band amplitude, `R21`, `phi21`, `R31`, and `phi31`, then finally to subtype-based defaults with deterministic phase offsets. The speed control is literal: at `1x`, the simulated clock advances in real time. Browser brightness keeps the I-band light-curve shape but rescales its mean-centered magnitude offsets to the catalog `amplitudeV` value, falling back to a V amplitude reconstructed from the fitted V-I curve and then subtype V/I ratios only when `amplitudeV` is missing. The logarithmic amplitude control scales the displayed V-band magnitude amplitude from `1x` to `20x`, defaulting to `10x`; the Cepheid and RR Lyrae presets use `5x` and the Mira preset uses `2x`, then each amplified waveform is renormalized back to its original mean light so the base catalog luminosity is unchanged. Pulsation carries most of that V-band flux multiplier through point area/radius and keeps a smaller opacity component so stars stay visible at faint phase while the area-alpha product still follows the light curve and base size and alpha still come from catalog luminosity. Raw magnitude offsets are converted to flux with only broad numerical safety rails, and the final visual pulse uses unbounded logarithmic compression rather than a finite display cap; the target-panel lightcurve shows the unamplified V-band waveform with the same logarithmic display compression so large-amplitude Miras do not flatten into linear-flux plateaus. When the selected speed would make a star pulsate faster than 2 Hz, the renderer uses that star's mean light instead of animating it, preventing high-speed flicker; paused targets also freeze the target-panel lightcurve marker. The catalog renderer keeps non-variable cluster stars on a retained static WebGL canvas while every variable catalog star redraws on a separate dynamic WebGL canvas. The dataset preset button cycles through Cepheids, RR Lyrae, Miras, and the default view; the default speed uses the precomputed median period across all pulsating catalog stars, while class presets dim the other pulsator families and use class medians unless manually overridden; the Mira preset uses `7,000,000x`. The default view uses a 0.75x-smaller radius baseline; class preset radius multipliers are scaled up to preserve their previously tuned apparent sizes for Cepheids, RR Lyrae, and Miras.

Color pulsation uses fitted OGLE V- and I-band epoch photometry when available. `scripts/prepare_data.py` downloads the OGLE `phot.tar.gz` archives, fits clipped harmonic curves in both filters, applies the I-band PCA phase offset to the V-band fit so color and brightness share the same carrier phase, quality-checks the fits, and stores a compact quantized V-I phase template in the generated JSON. Stars without a usable V/I fit fall back to the template color model; both paths keep phase color offsets in observed V-I but subtract each star's E(V-I) before the blackbody lookup.

## Run

```powershell
python scripts\serve.py 5173
```

Then open `http://localhost:5173/`.

## Refresh Data Asset

The source downloads are stored in `data/raw/`. To rebuild the compact browser asset:

```powershell
python scripts\prepare_data.py
```

The generated atlas JSON is written to `public/data/magellanic-clouds.json`, with compressed siblings at `public/data/magellanic-clouds.json.br` and `public/data/magellanic-clouds.json.gz`. The local server serves Brotli when `Accept-Encoding` includes `br`, gzip when it includes `gzip`, and the raw JSON otherwise. Brotli rebuilds need the Python `brotli` or `brotlicffi` package.

## Refresh XMC Density Proxy

The XMC FITS release contains distances but no density/count layer. To rebuild the approximate visual opacity layer from a stable 5% Gaia DR3 random sample with Oden et al. reddening corrections, dereddened red-clump CMD cuts, and adaptive local proper-motion filtering:

```powershell
python scripts\build_xmc_rc_density_advanced.py
python scripts\apply_xmc_density.py
```

The Gaia query writes `data/processed/xmc_rc_density_counts.json`; `apply_xmc_density.py` smooths those binned counts, folds them into the existing red-clump surface cells as `densityCount` and `densityUnit`, and rewrites the raw, Brotli, and gzip atlas assets. A full `python scripts\prepare_data.py` rebuild also picks up the density file, but it is much slower because it regenerates the pulsation assets.

For a quick legacy sample, `scripts\fetch_xmc_rc_density.py` still builds the older broad 1% Gaia proxy without extinction-aware CMD cuts or local proper-motion filtering.
