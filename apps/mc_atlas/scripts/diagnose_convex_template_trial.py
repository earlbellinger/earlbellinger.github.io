"""Diagnostic trial: fit stars as nonnegative mixtures of good-star templates.

This tests a local template dictionary alternative to fixed-phase PCA. For each
target star, the script selects nearby good-star Fourier lightcurves in logP and
fits the target as:

    magnitude = mean + sum_j alpha_j * template_j(phase + shift)

with alpha_j >= 0. After fitting, alpha/sum(alpha) is a convex combination of
real good-star shapes, so the model cannot create PCA-style ringing with signed
positive/negative lobes.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.optimize import lsq_linear

from diagnose_phase_warp_trial import (
    FEATURE_PHASE,
    OUT_DIR,
    ROOT,
    TARGET_STARS,
    CatalogEntry,
    cepheid_family,
    coherence_preserving_rejection_mask,
    current_model_at_obs,
    decode_current_i_curve,
    duplicate_phase,
    load_catalog,
    load_feature_shapes,
    phase_for,
    periodic_interp,
    read_band,
    robust_mad,
)


CURVE_CACHE = ROOT / "data" / "processed" / "ogle_color_curves.json"

DICTIONARY_NEIGHBORS = 128
SHIFT_BOUNDS = (-0.14, 0.14)
RIDGE_STRENGTH = 0.45
PERIOD_RIDGE_STRENGTH = 0.65
EFFECTIVE_ERROR_FLOOR = 0.018
EFFECTIVE_ERROR_CEILING = 0.08


def select_dictionary(entry: CatalogEntry, features: list[dict[str, object]]) -> dict[str, object]:
    target_logp = math.log10(entry.period)
    candidates = [feature for feature in features if str(feature["id"]) != entry.obj_id]
    candidates.sort(key=lambda feature: abs(float(feature["logp"]) - target_logp))
    selected = candidates[: min(DICTIONARY_NEIGHBORS, len(candidates))]
    logp = np.asarray([float(feature["logp"]) for feature in selected], dtype=float)
    shapes = np.vstack([feature["shape"] for feature in selected])
    distances = np.abs(logp - target_logp)
    sigma = max(0.035, float(np.percentile(distances, 70)) if distances.size else 0.035)
    return {
        "selected": selected,
        "logp": logp,
        "shapes": shapes,
        "distances": distances,
        "sigma": sigma,
    }


def evaluate_dictionary_at_phase(shapes: np.ndarray, phase: np.ndarray, shift: float) -> np.ndarray:
    shifted = phase + shift
    columns = [periodic_interp(shape, shifted) for shape in shapes]
    return np.column_stack(columns)


def solve_nonnegative_mix(
    template_values: np.ndarray,
    mag: np.ndarray,
    err: np.ndarray,
    distances: np.ndarray,
    sigma: float,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Solve baseline plus nonnegative template amplitudes for fixed shift."""

    centered_mag = mag - float(np.median(mag))
    effective_err = np.clip(err, EFFECTIVE_ERROR_FLOOR, EFFECTIVE_ERROR_CEILING)
    sqrt_w = 1.0 / effective_err
    matrix = np.column_stack([np.ones(template_values.shape[0]), template_values])
    lhs = matrix * sqrt_w[:, None]
    rhs = centered_mag * sqrt_w

    period_units = distances / max(sigma, 1e-4)
    coefficient_penalty = RIDGE_STRENGTH * (1.0 + PERIOD_RIDGE_STRENGTH * period_units**2)
    penalty = np.zeros((template_values.shape[1], template_values.shape[1] + 1), dtype=float)
    penalty[:, 1:] = np.diag(coefficient_penalty)
    lhs = np.vstack([lhs, penalty])
    rhs = np.concatenate([rhs, np.zeros(template_values.shape[1], dtype=float)])

    lower = np.r_[-np.inf, np.zeros(template_values.shape[1])]
    upper = np.r_[np.inf, np.full(template_values.shape[1], np.inf)]
    result = lsq_linear(lhs, rhs, bounds=(lower, upper), method="trf", max_iter=300, tol=1e-10)
    coeffs = result.x
    mean = float(np.median(mag) + coeffs[0])
    alpha = np.asarray(coeffs[1:], dtype=float)
    model = mean + template_values @ alpha
    return mean, alpha, model


def fit_dictionary_template(entry: CatalogEntry, photometry: np.ndarray, dictionary: dict[str, object]) -> dict[str, object]:
    phase = phase_for(entry, photometry[:, 0])
    mag = photometry[:, 1]
    err = photometry[:, 2]
    shapes = np.asarray(dictionary["shapes"], dtype=float)
    distances = np.asarray(dictionary["distances"], dtype=float)
    sigma = float(dictionary["sigma"])
    mask = np.ones(phase.size, dtype=bool)
    best_shift = 0.0
    best_mean = float(np.median(mag))
    best_alpha = np.zeros(shapes.shape[0], dtype=float)
    best_model = np.full(phase.size, best_mean, dtype=float)
    iterations = 0

    def objective_for_shift(shift: float, local_mask: np.ndarray) -> float:
        values = evaluate_dictionary_at_phase(shapes, phase[local_mask], shift)
        _, alpha, model = solve_nonnegative_mix(values, mag[local_mask], err[local_mask], distances, sigma)
        residual = mag[local_mask] - model
        _, mad, rms = robust_mad(residual)
        active = int(np.sum(alpha > max(1e-4, 0.01 * np.max(alpha) if np.max(alpha) > 0 else 1e-4)))
        entropy = 0.0
        total = float(np.sum(alpha))
        if total > 0:
            weights = alpha / total
            entropy = float(-np.sum(weights[weights > 0] * np.log(weights[weights > 0])))
        return float(rms + 0.12 * mad + 0.0005 * active + 0.0008 * entropy)

    for iteration in range(8):
        iterations = iteration + 1
        coarse_shifts = np.linspace(SHIFT_BOUNDS[0], SHIFT_BOUNDS[1], 43)
        coarse_scores = np.asarray([objective_for_shift(float(shift), mask) for shift in coarse_shifts])
        coarse_best = float(coarse_shifts[int(np.argmin(coarse_scores))])
        bracket_width = 0.018
        lower = max(SHIFT_BOUNDS[0], coarse_best - bracket_width)
        upper = min(SHIFT_BOUNDS[1], coarse_best + bracket_width)
        result = minimize_scalar(
            lambda shift: objective_for_shift(float(shift), mask),
            bounds=(lower, upper),
            method="bounded",
            options={"xatol": 2e-4, "maxiter": 80},
        )
        best_shift = float(result.x if result.success else coarse_best)

        values_masked = evaluate_dictionary_at_phase(shapes, phase[mask], best_shift)
        best_mean, best_alpha, _ = solve_nonnegative_mix(values_masked, mag[mask], err[mask], distances, sigma)
        values_all = evaluate_dictionary_at_phase(shapes, phase, best_shift)
        best_model = best_mean + values_all @ best_alpha
        residual = mag - best_model

        next_mask = coherence_preserving_rejection_mask(phase, residual, err, mask)
        if int(next_mask.sum()) < max(20, int(0.55 * phase.size)):
            next_mask = mask
        if np.array_equal(next_mask, mask):
            break
        mask = next_mask

    dense = np.linspace(0.0, 1.0, 1200, endpoint=False)
    values_dense = evaluate_dictionary_at_phase(shapes, dense, best_shift)
    model_dense = best_mean + values_dense @ best_alpha
    residual = mag - best_model
    _, kept_mad, kept_rms = robust_mad(residual, mask)
    _, all_mad, all_rms = robust_mad(residual)
    total_alpha = float(np.sum(best_alpha))
    weights = best_alpha / total_alpha if total_alpha > 0 else np.zeros_like(best_alpha)
    active_threshold = max(1e-4, 0.01 * float(np.max(best_alpha)) if best_alpha.size and np.max(best_alpha) > 0 else 1e-4)
    active = int(np.sum(best_alpha > active_threshold))
    effective_count = float(1.0 / np.sum(weights**2)) if np.sum(weights**2) > 0 else 0.0
    return {
        "mean": best_mean,
        "alpha": best_alpha,
        "weights": weights,
        "amplitude": total_alpha,
        "activeTemplates": active,
        "effectiveTemplates": effective_count,
        "phaseShift": best_shift,
        "mask": mask,
        "modelAtObs": best_model,
        "modelDense": model_dense,
        "residual": residual,
        "iterations": iterations,
        "keptMad": kept_mad,
        "keptRms": kept_rms,
        "allMad": all_mad,
        "allRms": all_rms,
    }


def plot_dictionary_trial(
    entry: CatalogEntry,
    photometry: np.ndarray,
    dictionary: dict[str, object],
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
    weights = np.asarray(fit["weights"], dtype=float)
    logp = np.asarray(dictionary["logp"], dtype=float)
    selected = list(dictionary["selected"])
    target_logp = math.log10(entry.period)
    out_path = OUT_DIR / f"{entry.obj_id}_convex_template_dictionary_trial_two_phase.png"
    summary_path = OUT_DIR / f"{entry.obj_id}_convex_template_dictionary_trial_two_phase.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(3, 1, figsize=(11, 9.7), sharex=False)
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.08, top=0.885, hspace=0.22)
    fig.suptitle(f"{entry.obj_id} - local nonnegative template dictionary trial", fontsize=15, fontweight="bold", y=0.985)
    subtitle = (
        f"period={entry.period:.7f} d   logP={target_logp:.3f}   mode={entry.mode}/{entry.subtype}   "
        f"neighbors={len(selected)} sigma={float(dictionary['sigma']):.3f}   phase shift={float(fit['phaseShift']):+.4f}   "
        f"active={int(fit['activeTemplates'])} effective={float(fit['effectiveTemplates']):.1f}   kept/rejected={int(mask.sum())}/{int((~mask).sum())}"
    )
    fig.text(0.5, 0.952, subtitle, ha="center", va="top", fontsize=9.0, color="#3d4652")

    x, y, e = duplicate_phase(phase, photometry[:, 1], photometry[:, 2])
    kept2 = np.r_[mask, mask]
    axes[0].errorbar(x[kept2], y[kept2], yerr=e[kept2], fmt=".", ms=4.2, lw=0.45, elinewidth=0.45, alpha=0.48, color="#2f6f9f", label="retained I photometry")
    if np.any(~kept2):
        axes[0].scatter(x[~kept2], y[~kept2], s=18, marker="x", color="#c43d3d", alpha=0.72, label="trial rejected")
    if current_dense is not None:
        axes[0].plot(dense2, np.r_[current_dense, current_dense], color="#777777", lw=1.7, ls="--", label="current v16 PCA")
    model_dense = np.asarray(fit["modelDense"], dtype=float)
    axes[0].plot(dense2, np.r_[model_dense, model_dense], color="black", lw=2.3, label="nonnegative dictionary")
    axes[0].invert_yaxis()
    axes[0].set_xlim(0, 2)
    axes[0].set_xticks(np.arange(0, 2.01, 0.25))
    axes[0].set_ylabel("I mag")
    axes[0].grid(True, color="#e6e8ec", lw=0.8)
    axes[0].legend(loc="upper right", frameon=True, framealpha=0.92)
    axes[0].text(
        0.012,
        0.035,
        f"current MAD={current_mad:.4f} RMS={current_rms:.4f}   dictionary kept MAD={float(fit['keptMad']):.4f} RMS={float(fit['keptRms']):.4f}   all MAD={float(fit['allMad']):.4f}",
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
    axes[1].scatter(xr[kept2], yr[kept2], s=14, alpha=0.52, color="#2f6f9f", label="dictionary retained residual")
    if np.any(~kept2):
        axes[1].scatter(xr[~kept2], yr[~kept2], s=18, marker="x", color="#c43d3d", alpha=0.72, label="dictionary rejected residual")
    axes[1].set_xlim(0, 2)
    axes[1].set_xticks(np.arange(0, 2.01, 0.25))
    axes[1].set_ylabel("I residual")
    axes[1].grid(True, color="#e6e8ec", lw=0.8)
    axes[1].legend(loc="upper right", frameon=True, framealpha=0.92)

    axes[2].axvline(target_logp, color="black", lw=1.6, label="target logP")
    sizes = 20 + 650 * np.sqrt(np.maximum(weights, 0))
    axes[2].scatter(logp, weights, s=sizes, alpha=0.72, color="#2f6f9f", edgecolors="white", linewidths=0.5, label="template weights")
    top = np.argsort(weights)[::-1][:6]
    for rank, index in enumerate(top, 1):
        if weights[index] <= 0:
            continue
        axes[2].annotate(
            str(rank),
            (logp[index], weights[index]),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color="#222222",
        )
    axes[2].set_xlabel("Template log10(period)")
    axes[2].set_ylabel("Convex weight")
    axes[2].set_ylim(-0.03, max(0.08, float(np.max(weights)) * 1.18 if weights.size else 0.08))
    axes[2].grid(True, color="#e6e8ec", lw=0.8)
    axes[2].legend(loc="upper right", frameon=True, framealpha=0.92)

    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)

    top_templates = []
    for index in top[:10]:
        if weights[index] <= 0:
            continue
        feature = selected[int(index)]
        top_templates.append(
            {
                "rank": len(top_templates) + 1,
                "id": str(feature["id"]),
                "weight": float(weights[index]),
                "logP": float(logp[index]),
                "periodDays": float(10 ** logp[index]),
            }
        )

    summary = {
        "star": entry.obj_id,
        "periodDays": entry.period,
        "logP": target_logp,
        "family": cepheid_family(entry),
        "dictionaryNeighbors": len(selected),
        "dictionarySigma": float(dictionary["sigma"]),
        "ridgeStrength": RIDGE_STRENGTH,
        "periodRidgeStrength": PERIOD_RIDGE_STRENGTH,
        "trialMean": float(fit["mean"]),
        "trialAmplitude": float(fit["amplitude"]),
        "trialPhaseShift": float(fit["phaseShift"]),
        "trialActiveTemplates": int(fit["activeTemplates"]),
        "trialEffectiveTemplates": float(fit["effectiveTemplates"]),
        "trialKept": int(mask.sum()),
        "trialRejected": int((~mask).sum()),
        "trialIterations": int(fit["iterations"]),
        "currentResidualMad": current_mad,
        "currentResidualRms": current_rms,
        "trialKeptResidualMad": float(fit["keptMad"]),
        "trialKeptResidualRms": float(fit["keptRms"]),
        "trialAllResidualMad": float(fit["allMad"]),
        "trialAllResidualRms": float(fit["allRms"]),
        "topTemplates": top_templates,
        "currentTemplateSource": current_curve_entry.get("templateSource"),
        "currentLightQuality": current_curve_entry.get("lightQuality"),
        "image": str(out_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    catalog = load_catalog()
    curves = json.loads(CURVE_CACHE.read_text(encoding="utf-8"))["curves"]
    fu_features = load_feature_shapes(catalog, "FU")
    summaries: list[dict[str, object]] = []

    for star_id in TARGET_STARS:
        entry = catalog[star_id]
        photometry = read_band(entry, "I")
        if photometry.size == 0:
            raise RuntimeError(f"No I-band photometry for {star_id}")
        dictionary = select_dictionary(entry, fu_features)
        fit = fit_dictionary_template(entry, photometry, dictionary)
        summaries.append(plot_dictionary_trial(entry, photometry, dictionary, fit, curves[star_id]))

    combined_path = OUT_DIR / "convex_template_dictionary_trial_examples_summary.json"
    combined_path.write_text(json.dumps({"stars": summaries}, indent=2), encoding="utf-8")
    print(json.dumps({"stars": summaries}, indent=2))


if __name__ == "__main__":
    main()
