"""Prototype a log-period conditioned phase-warp Cepheid template.

This is a diagnostic trial of the next step after
``diagnose_phase_warp_trial.py``. Instead of letting each target star freely
choose its own warp, this script:

1. Fits monotone registration warps for good FU Cepheid Fourier shapes.
2. Smooths those warp anchors as a function of log10(period).
3. Builds a period-local template in the registered/canonical phase frame.
4. Fits target stars with only mean, amplitude, global phase shift, and robust
   rejection while using the period-predicted warp.

The intent is to test whether the Hertzsprung-progression phase motion can be
handled as a period-conditioned warp rather than as fixed-phase PCA ringing.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

from diagnose_phase_warp_trial import (
    FEATURE_PHASE,
    OUT_DIR,
    ROOT,
    TARGET_STARS,
    CatalogEntry,
    apply_warp,
    cepheid_family,
    coherence_preserving_rejection_mask,
    current_model_at_obs,
    decode_current_i_curve,
    duplicate_phase,
    fit_shape_warp,
    load_catalog,
    load_feature_shapes,
    normalize_shape,
    phase_for,
    periodic_interp,
    percentile_span,
    read_band,
    robust_mad,
    solve_mean_amplitude,
    warp_penalty,
)


CURVE_CACHE = ROOT / "data" / "processed" / "ogle_color_curves.json"
WARP_CACHE = ROOT / "data" / "processed" / "fu_logp_warp_trial_cache_v1.npz"

REFERENCE_LOGP = 1.0
MAX_WARP_TRAINING = 2000
GLOBAL_REGISTRATION_ITERATIONS = 2
TEMPLATE_NEIGHBORS = 96
WARP_SMOOTH_NEIGHBORS = 180
MIN_TEMPLATE_SIGMA = 0.045
MIN_WARP_SIGMA = 0.075


class LogPWarpModel:
    def __init__(
        self,
        *,
        ids: np.ndarray,
        logp: np.ndarray,
        anchors: np.ndarray,
        registered_shapes: np.ndarray,
        reference_template: np.ndarray,
        training_summary: dict[str, object],
    ) -> None:
        self.ids = ids.astype(str)
        self.logp = logp.astype(float)
        self.anchors = anchors.astype(float)
        self.registered_shapes = registered_shapes.astype(float)
        self.reference_template = reference_template.astype(float)
        self.training_summary = training_summary

    def weights_near(self, target_logp: float, neighbor_count: int, minimum_sigma: float) -> tuple[np.ndarray, float]:
        distances = np.abs(self.logp - target_logp)
        order = np.argsort(distances)
        keep = order[: min(neighbor_count, len(order))]
        local_distances = distances[keep]
        sigma = max(minimum_sigma, float(np.percentile(local_distances, 70)) if local_distances.size else minimum_sigma)
        weights = np.exp(-0.5 * (local_distances / sigma) ** 2)
        weights /= float(np.sum(weights))
        full_weights = np.zeros_like(self.logp, dtype=float)
        full_weights[keep] = weights
        return full_weights, sigma

    def predicted_anchors(self, target_logp: float) -> tuple[np.ndarray, float]:
        weights, sigma = self.weights_near(target_logp, WARP_SMOOTH_NEIGHBORS, MIN_WARP_SIGMA)
        anchors = np.average(self.anchors, axis=0, weights=weights)
        anchors[0] = 0.0
        anchors[-1] = 1.0
        anchors = np.maximum.accumulate(anchors)
        anchors /= anchors[-1]
        return anchors, sigma

    def period_template(self, target_logp: float) -> tuple[np.ndarray, float]:
        weights, sigma = self.weights_near(target_logp, TEMPLATE_NEIGHBORS, MIN_TEMPLATE_SIGMA)
        template = np.average(self.registered_shapes, axis=0, weights=weights)
        return normalize_shape(template), sigma


def stratified_training_features(features: list[dict[str, object]], max_count: int) -> list[dict[str, object]]:
    if len(features) <= max_count:
        return features
    ordered = sorted(features, key=lambda feature: float(feature["logp"]))
    selected_indices = np.linspace(0, len(ordered) - 1, max_count, dtype=int)
    return [ordered[int(index)] for index in selected_indices]


def initial_reference_template(features: list[dict[str, object]]) -> np.ndarray:
    logp = np.asarray([float(feature["logp"]) for feature in features], dtype=float)
    shapes = np.vstack([feature["shape"] for feature in features])
    distances = np.abs(logp - REFERENCE_LOGP)
    sigma = max(0.12, float(np.percentile(np.sort(distances)[: min(160, len(distances))], 75)))
    weights = np.exp(-0.5 * (distances / sigma) ** 2)
    weights /= float(np.sum(weights))
    return normalize_shape(np.average(shapes, axis=0, weights=weights))


def fit_global_logp_warp_model(features: list[dict[str, object]]) -> LogPWarpModel:
    training = stratified_training_features(features, MAX_WARP_TRAINING)
    ids = np.asarray([str(feature["id"]) for feature in training])
    logp = np.asarray([float(feature["logp"]) for feature in training], dtype=float)
    shapes = np.vstack([feature["shape"] for feature in training])

    reference = initial_reference_template(training)
    anchors = np.zeros((len(training), 11), dtype=float)
    registered_shapes = np.zeros_like(shapes)
    mean_abs_warps: list[float] = []

    for _ in range(GLOBAL_REGISTRATION_ITERATIONS):
        iteration_warp_sizes: list[float] = []
        for index, shape in enumerate(shapes):
            star_anchors = fit_shape_warp(
                shape,
                reference,
                intervals=10,
                identity_weight=0.32,
                smooth_weight=0.32,
            )
            inverse_phase = np.interp(FEATURE_PHASE, star_anchors, np.linspace(0.0, 1.0, star_anchors.size))
            registered = periodic_interp(shape, inverse_phase)
            anchors[index] = star_anchors
            registered_shapes[index] = registered
            iteration_warp_sizes.append(float(np.mean(np.abs(star_anchors - np.linspace(0.0, 1.0, star_anchors.size)))))
        reference = normalize_shape(np.mean(registered_shapes, axis=0))
        mean_abs_warps.append(float(np.mean(iteration_warp_sizes)))

    summary = {
        "trainingCount": len(training),
        "sourceFeatureCount": len(features),
        "maxWarpTraining": MAX_WARP_TRAINING,
        "referenceLogP": REFERENCE_LOGP,
        "iterations": GLOBAL_REGISTRATION_ITERATIONS,
        "meanAbsWarpByIteration": mean_abs_warps,
        "logPMin": float(np.min(logp)),
        "logPMedian": float(np.median(logp)),
        "logPMax": float(np.max(logp)),
    }
    return LogPWarpModel(
        ids=ids,
        logp=logp,
        anchors=anchors,
        registered_shapes=registered_shapes,
        reference_template=reference,
        training_summary=summary,
    )


def load_or_build_model(features: list[dict[str, object]]) -> LogPWarpModel:
    if WARP_CACHE.exists():
        try:
            with np.load(WARP_CACHE, allow_pickle=False) as payload:
                meta = json.loads(str(payload["meta"].item()))
                if (
                    int(meta.get("maxWarpTraining", -1)) == MAX_WARP_TRAINING
                    and int(meta.get("iterations", -1)) == GLOBAL_REGISTRATION_ITERATIONS
                    and int(payload["anchors"].shape[0]) > 0
                ):
                    return LogPWarpModel(
                        ids=payload["ids"].astype(str),
                        logp=payload["logp"],
                        anchors=payload["anchors"],
                        registered_shapes=payload["registeredShapes"],
                        reference_template=payload["referenceTemplate"],
                        training_summary=meta,
                    )
        except Exception:
            pass

    model = fit_global_logp_warp_model(features)
    WARP_CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        WARP_CACHE,
        ids=model.ids,
        logp=model.logp,
        anchors=model.anchors,
        registeredShapes=model.registered_shapes,
        referenceTemplate=model.reference_template,
        meta=json.dumps(model.training_summary),
    )
    return model


def fit_period_warp_template(
    entry: CatalogEntry,
    photometry: np.ndarray,
    template: np.ndarray,
    anchors: np.ndarray,
) -> dict[str, object]:
    phase = phase_for(entry, photometry[:, 0])
    mag = photometry[:, 1]
    err = photometry[:, 2]
    amp_scale = max(0.05, percentile_span(mag))
    mask = np.ones(phase.size, dtype=bool)
    best_shift = 0.0
    iterations = 0

    def evaluate(shift: float, eval_phase: np.ndarray, eval_mag: np.ndarray, eval_err: np.ndarray) -> tuple[float, float, np.ndarray, np.ndarray]:
        warped_phase = apply_warp(eval_phase + shift, anchors)
        shape = periodic_interp(template, warped_phase)
        mean, amplitude, model = solve_mean_amplitude(shape, eval_mag, eval_err)
        return mean, amplitude, model, shape

    for iteration in range(8):
        iterations = iteration + 1
        phase_fit = phase[mask]
        mag_fit = mag[mask]
        err_fit = err[mask]

        def objective(value: np.ndarray) -> float:
            shift = float(value[0])
            mean, amplitude, model, _ = evaluate(shift, phase_fit, mag_fit, err_fit)
            residual = (mag_fit - model) / amp_scale
            return float(np.mean(residual**2) + 0.0015 * (shift / 0.08) ** 2)

        best_result = None
        for start in np.linspace(best_shift - 0.05, best_shift + 0.05, 7):
            result = minimize(
                objective,
                np.asarray([float(np.clip(start, -0.14, 0.14))]),
                method="L-BFGS-B",
                bounds=[(-0.14, 0.14)],
                options={"maxiter": 120, "ftol": 1e-10},
            )
            if best_result is None or result.fun < best_result.fun:
                best_result = result
        best_shift = float(best_result.x[0]) if best_result is not None else best_shift

        mean, amplitude, _, _ = evaluate(best_shift, phase_fit, mag_fit, err_fit)
        all_shape = periodic_interp(template, apply_warp(phase + best_shift, anchors))
        model = mean + amplitude * all_shape
        residual = mag - model
        next_mask = coherence_preserving_rejection_mask(phase, residual, err, mask)
        if int(next_mask.sum()) < max(20, int(0.55 * phase.size)):
            next_mask = mask
        if np.array_equal(next_mask, mask):
            break
        mask = next_mask

    mean, amplitude, _, _ = evaluate(best_shift, phase[mask], mag[mask], err[mask])
    dense = np.linspace(0.0, 1.0, 1200, endpoint=False)
    model_at_obs = mean + amplitude * periodic_interp(template, apply_warp(phase + best_shift, anchors))
    model_dense = mean + amplitude * periodic_interp(template, apply_warp(dense + best_shift, anchors))
    residual = mag - model_at_obs
    _, kept_mad, kept_rms = robust_mad(residual, mask)
    _, all_mad, all_rms = robust_mad(residual)
    return {
        "mean": mean,
        "amplitude": amplitude,
        "phaseShift": best_shift,
        "mask": mask,
        "modelAtObs": model_at_obs,
        "modelDense": model_dense,
        "residual": residual,
        "iterations": iterations,
        "keptMad": kept_mad,
        "keptRms": kept_rms,
        "allMad": all_mad,
        "allRms": all_rms,
    }


def plot_logp_trial(
    entry: CatalogEntry,
    photometry: np.ndarray,
    model: LogPWarpModel,
    template: np.ndarray,
    anchors: np.ndarray,
    template_sigma: float,
    warp_sigma: float,
    fit: dict[str, object],
    current_curve_entry: dict[str, object],
) -> dict[str, object]:
    phase = phase_for(entry, photometry[:, 0])
    dense = np.linspace(0.0, 1.0, 1200, endpoint=False)
    dense2 = np.r_[dense, dense + 1.0]
    current_dense = decode_current_i_curve(current_curve_entry, entry)
    current_obs = current_model_at_obs(current_curve_entry, entry, phase)
    current_residual = photometry[:, 1] - current_obs if current_obs is not None else np.full(phase.size, np.nan)
    _, current_mad, current_rms = robust_mad(current_residual)

    mask = np.asarray(fit["mask"], dtype=bool)
    residual = np.asarray(fit["residual"], dtype=float)
    model_dense = np.asarray(fit["modelDense"], dtype=float)
    out_path = OUT_DIR / f"{entry.obj_id}_logp_warp_template_trial_two_phase.png"
    summary_path = OUT_DIR / f"{entry.obj_id}_logp_warp_template_trial_two_phase.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(3, 1, figsize=(11, 9.6), sharex=True)
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.075, top=0.885, hspace=0.07)
    fig.suptitle(f"{entry.obj_id} - logP-predicted warp template trial", fontsize=15, fontweight="bold", y=0.985)
    subtitle = (
        f"period={entry.period:.7f} d   logP={math.log10(entry.period):.3f}   mode={entry.mode}/{entry.subtype}   "
        f"template neighbors={TEMPLATE_NEIGHBORS} sigma={template_sigma:.3f}   warp neighbors={WARP_SMOOTH_NEIGHBORS} sigma={warp_sigma:.3f}   "
        f"phase shift={float(fit['phaseShift']):+.4f}   kept/rejected={int(mask.sum())}/{int((~mask).sum())}"
    )
    fig.text(0.5, 0.952, subtitle, ha="center", va="top", fontsize=9.0, color="#3d4652")

    x, y, e = duplicate_phase(phase, photometry[:, 1], photometry[:, 2])
    kept2 = np.r_[mask, mask]
    axes[0].errorbar(x[kept2], y[kept2], yerr=e[kept2], fmt=".", ms=4.2, lw=0.45, elinewidth=0.45, alpha=0.48, color="#2f6f9f", label="retained I photometry")
    if np.any(~kept2):
        axes[0].scatter(x[~kept2], y[~kept2], s=18, marker="x", color="#c43d3d", alpha=0.72, label="trial rejected")
    if current_dense is not None:
        axes[0].plot(dense2, np.r_[current_dense, current_dense], color="#777777", lw=1.7, ls="--", label="current v16 PCA")
    axes[0].plot(dense2, np.r_[model_dense, model_dense], color="black", lw=2.3, label="logP-warp trial")
    axes[0].invert_yaxis()
    axes[0].set_ylabel("I mag")
    axes[0].grid(True, color="#e6e8ec", lw=0.8)
    axes[0].legend(loc="upper right", frameon=True, framealpha=0.92)
    axes[0].text(
        0.012,
        0.035,
        f"current MAD={current_mad:.4f} RMS={current_rms:.4f}   trial kept MAD={float(fit['keptMad']):.4f} RMS={float(fit['keptRms']):.4f}   trial all MAD={float(fit['allMad']):.4f}",
        transform=axes[0].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.8,
        bbox={"boxstyle": "round,pad=0.32", "fc": "white", "ec": "#ccd1d9", "alpha": 0.9},
    )

    axes[1].axhline(0.0, color="#111111", lw=1.0)
    if current_obs is not None:
        xr, yr, _ = duplicate_phase(phase, current_residual)
        axes[1].scatter(xr, yr, s=12, alpha=0.34, color="#777777", label="current residual")
    xr, yr, _ = duplicate_phase(phase, residual)
    axes[1].scatter(xr[kept2], yr[kept2], s=14, alpha=0.52, color="#2f6f9f", label="trial retained residual")
    if np.any(~kept2):
        axes[1].scatter(xr[~kept2], yr[~kept2], s=18, marker="x", color="#c43d3d", alpha=0.72, label="trial rejected residual")
    axes[1].set_ylabel("I residual")
    axes[1].grid(True, color="#e6e8ec", lw=0.8)
    axes[1].legend(loc="upper right", frameon=True, framealpha=0.92)

    warp_dense = apply_warp(dense, anchors)
    knots = np.linspace(0.0, 1.0, len(anchors))
    axes[2].plot(dense2, np.r_[warp_dense, warp_dense + 1.0], color="black", lw=2.0, label="predicted W(logP, phase)")
    axes[2].plot([0, 2], [0, 2], color="#777777", lw=1.4, ls="--", label="identity")
    axes[2].scatter(knots, anchors, color="#2f6f9f", s=22, zorder=3, label="predicted warp knots")
    axes[2].scatter(knots + 1.0, anchors + 1.0, color="#2f6f9f", s=22, zorder=3)
    axes[2].set_ylabel("template phase")
    axes[2].set_xlabel("Pulsation phase")
    axes[2].grid(True, color="#e6e8ec", lw=0.8)
    axes[2].legend(loc="upper left", frameon=True, framealpha=0.92)

    for ax in axes:
        ax.set_xlim(0, 2)
        ax.set_xticks(np.arange(0, 2.01, 0.25))

    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)

    identity, smooth = warp_penalty(anchors)
    summary = {
        "star": entry.obj_id,
        "periodDays": entry.period,
        "logP": math.log10(entry.period),
        "family": cepheid_family(entry),
        "templateNeighbors": TEMPLATE_NEIGHBORS,
        "templateSigma": template_sigma,
        "warpSmoothNeighbors": WARP_SMOOTH_NEIGHBORS,
        "warpSigma": warp_sigma,
        "warpIdentityPenalty": identity,
        "warpSmoothPenalty": smooth,
        "predictedWarpAnchors": [float(value) for value in anchors],
        "trialMean": float(fit["mean"]),
        "trialAmplitude": float(fit["amplitude"]),
        "trialPhaseShift": float(fit["phaseShift"]),
        "trialKept": int(mask.sum()),
        "trialRejected": int((~mask).sum()),
        "trialIterations": int(fit["iterations"]),
        "currentResidualMad": current_mad,
        "currentResidualRms": current_rms,
        "trialKeptResidualMad": float(fit["keptMad"]),
        "trialKeptResidualRms": float(fit["keptRms"]),
        "trialAllResidualMad": float(fit["allMad"]),
        "trialAllResidualRms": float(fit["allRms"]),
        "currentTemplateSource": current_curve_entry.get("templateSource"),
        "currentLightQuality": current_curve_entry.get("lightQuality"),
        "trainingSummary": model.training_summary,
        "image": str(out_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    catalog = load_catalog()
    curves = json.loads(CURVE_CACHE.read_text(encoding="utf-8"))["curves"]
    fu_features = load_feature_shapes(catalog, "FU")
    model = load_or_build_model(fu_features)

    summaries: list[dict[str, object]] = []
    for star_id in TARGET_STARS:
        entry = catalog[star_id]
        photometry = read_band(entry, "I")
        if photometry.size == 0:
            raise RuntimeError(f"No I-band photometry for {star_id}")
        target_logp = math.log10(entry.period)
        anchors, warp_sigma = model.predicted_anchors(target_logp)
        template, template_sigma = model.period_template(target_logp)
        fit = fit_period_warp_template(entry, photometry, template, anchors)
        summaries.append(plot_logp_trial(entry, photometry, model, template, anchors, template_sigma, warp_sigma, fit, curves[star_id]))

    combined_path = OUT_DIR / "logp_warp_trial_examples_summary.json"
    combined_path.write_text(json.dumps({"stars": summaries}, indent=2), encoding="utf-8")
    print(json.dumps({"stars": summaries}, indent=2))


if __name__ == "__main__":
    main()
