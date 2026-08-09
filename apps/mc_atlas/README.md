# Magellanic Cloud Atlas

Magellanic Cloud Atlas is an interactive 3-D explorer of stars, clusters, and red-clump structure across the Large and Small Magellanic Clouds. Visit [earlbellinger.com/apps/mc_atlas/](https://earlbellinger.com/apps/mc_atlas/).

The deployed red-clump layer is an uncertainty-convolved observed-distance likelihood volume built from the 2,349,340-star Gaia catalog supplied by Slater Oden. The exact point-estimate v1 volume and the prior surface products remain preserved under `data/processed/legacy/` and are intentionally excluded from the public app payload. This observed likelihood field is not a deconvolved physical-density inference and should not be used to measure intrinsic line-of-sight thickness.

The superseded independent Gaia/Oden reproduction and publication-grade research pipeline is preserved for provenance on the `codex/archive-rc-reproduction-2026-08-08` branch. The production branch intentionally retains only the author-catalog volume builders used to regenerate the deployed red-clump products.

Run the app locally with `python scripts\serve.py 5173`.
