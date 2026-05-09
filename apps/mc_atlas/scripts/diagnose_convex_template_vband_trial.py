"""V-band diagnostic for the local nonnegative template dictionary trial.

The I band carries most of the phase coverage, so this script first fits the
local convex dictionary to I. It then uses the resulting dictionary mixture as a
shared morphology carrier for V, fitting only V mean and amplitude. This avoids
letting sparse V-band data choose arbitrary template mixtures.
"""

from __future__ import annotations

import base64
import json
import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

from diagnose_convex_template_trial import (
    CURVE_CACHE,
    DICTIONARY_NEIGHBORS,
    fit_dictionary_template,
    select_dictionary,
)
from diagnose_phase_warp_trial import (
    OUT_DIR,
    TARGET_STARS,
    CatalogEntry,
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


def evaluate_dictionary_carrier(dictionary: dict[str, object], weights: np.ndarray, phase: np.ndarray, shift: float) -> np.ndarray:
    shapes = np.asarray(dictionary["shapes"], dtype=float)
    if weights.size != shapes.shape[0] or float(np.sum(weights)) <= 0:
        weights = np.zeros(shapes.shape[0], dtype=float)
        weights[0] = 1.0
    values = np.column_stack([periodic_interp(shape, phase + shift) for shape in shapes])
    return values @ weights


def fit_band_to_carrier(phase: np.ndarray, mag: np.ndarray, err: np.ndarray, carrier: np.ndarray) -> dict[str, object]:
    effective_err = np.clip(err, 0.015, 0.12)
    carrier_center = float(np.mean(carrier))
    carrier_scale = float(np.percentile(carrier, 95) - np.percentile(carrier, 5))
    if not math.isfinite(carrier_scale) or carrier_scale <= 1e-4:
        carrier_scale = 1.0
    x = (carrier - carrier_center) / carrier_scale

    def residual(params: np.ndarray) -> np.ndarray:
        mean, amplitude = params
        return (mag - (mean + amplitude * x)) / effective_err

    start = np.asarray([float(np.median(mag)), float(np.percentile(mag, 95) - np.percentile(mag, 5))])
    result = least_squares(residual, start, loss="soft_l1", f_scale=1.4, max_nfev=200)
    mean, amplitude = result.x
    model = mean + amplitude * x
    resid = mag - model
    center, mad, _ = robust_mad(resid)
    sigma = max(0.025, mad, float(np.median(effective_err)))
    display_mask = np.abs(resid - center) <= 4.5 * sigma
    if int(display_mask.sum()) < max(5, int(0.55 * len(display_mask))):
        display_mask[:] = True
    return {
        "mean": float(mean),
        "amplitude": float(amplitude),
        "carrierCenter": carrier_center,
        "carrierScale": carrier_scale,
        "model": model,
        "residual": resid,
        "displayMask": display_mask,
    }


def apply_band_fit(fit: dict[str, object], carrier: np.ndarray) -> np.ndarray:
    x = (carrier - float(fit["carrierCenter"])) / float(fit["carrierScale"])
    return float(fit["mean"]) + float(fit["amplitude"]) * x


def decode_current_color_curve(curve_entry: dict[str, object]) -> np.ndarray | None:
    encoded = curve_entry.get("curve")
    if not isinstance(encoded, str):
        return None
    return (np.frombuffer(base64.b64decode(encoded), dtype=np.uint8).astype(float) - 64.0) / 100.0


def current_v_dense(curve_entry: dict[str, object], entry: CatalogEntry, dense: np.ndarray) -> np.ndarray | None:
    i_dense = decode_current_i_curve(curve_entry, entry)
    if i_dense is None:
        return None
    color = decode_current_color_curve(curve_entry)
    if color is None:
        return i_dense + entry.v_minus_i
    return i_dense + entry.v_minus_i + periodic_interp(color, dense)


def current_v_at_phase(curve_entry: dict[str, object], entry: CatalogEntry, phase: np.ndarray) -> np.ndarray | None:
    i_model = current_model_at_obs(curve_entry, entry, phase)
    if i_model is None:
        return None
    color = decode_current_color_curve(curve_entry)
    if color is None:
        return i_model + entry.v_minus_i
    return i_model + entry.v_minus_i + periodic_interp(color, phase)


def near_simultaneous_color_pairs(entry: CatalogEntry, i_obs: np.ndarray, v_obs: np.ndarray) -> np.ndarray:
    pairs: list[tuple[float, float, float]] = []
    for vt, vm, _ in v_obs:
        j = int(np.argmin(np.abs(i_obs[:, 0] - vt)))
        dt = abs(float(i_obs[j, 0] - vt))
        if dt <= 0.03:
            pairs.append((phase_for(entry, np.asarray([vt]))[0], vm - i_obs[j, 1], dt))
    return np.asarray(pairs, dtype=float) if pairs else np.empty((0, 3), dtype=float)


def plot_star(entry: CatalogEntry, dictionary: dict[str, object], i_fit: dict[str, object], v_fit: dict[str, object], curves: dict[str, object]) -> dict[str, object]:
    i_obs = read_band(entry, "I")
    v_obs = read_band(entry, "V")
    phase_i = phase_for(entry, i_obs[:, 0])
    phase_v = phase_for(entry, v_obs[:, 0])
    dense = np.linspace(0.0, 1.0, 1200, endpoint=False)
    dense2 = np.r_[dense, dense + 1.0]
    weights = np.asarray(i_fit["weights"], dtype=float)
    shift = float(i_fit["phaseShift"])
    i_dense = np.asarray(i_fit["modelDense"], dtype=float)
    carrier_v = evaluate_dictionary_carrier(dictionary, weights, phase_v, shift)
    carrier_dense = evaluate_dictionary_carrier(dictionary, weights, dense, shift)
    v_model_dense = apply_band_fit(v_fit, carrier_dense)
    v_model_at_obs = np.asarray(v_fit["model"], dtype=float)
    color_model_dense = v_model_dense - i_dense
    color_at_v = v_obs[:, 1] - apply_band_fit(
        {
            "mean": i_fit["mean"],
            "amplitude": i_fit["amplitude"],
            "carrierCenter": v_fit["carrierCenter"],
            "carrierScale": v_fit["carrierScale"],
        },
        carrier_v,
    )
    # Use the actual I dense model interpolation for the color points; the
    # carrier-scaled form above is only a fallback if model encoding changes.
    color_at_v = v_obs[:, 1] - np.interp(np.mod(phase_v, 1.0), dense, i_dense, period=1.0)
    color_model_at_v = np.interp(np.mod(phase_v, 1.0), dense, color_model_dense, period=1.0)
    pairs = near_simultaneous_color_pairs(entry, i_obs, v_obs)

    curve_entry = curves[entry.obj_id]
    current_i_dense = decode_current_i_curve(curve_entry, entry)
    current_v_line = current_v_dense(curve_entry, entry, dense)
    current_v_obs = current_v_at_phase(curve_entry, entry, phase_v)
    current_v_resid = v_obs[:, 1] - current_v_obs if current_v_obs is not None else np.full(len(v_obs), np.nan)
    _, current_v_mad, current_v_rms = robust_mad(current_v_resid)
    _, v_mad, v_rms = robust_mad(v_obs[:, 1] - v_model_at_obs)
    _, c_mad, c_rms = robust_mad(color_at_v - color_model_at_v)

    out_path = OUT_DIR / f"{entry.obj_id}_convex_template_vband_trial_two_phase.png"
    summary_path = OUT_DIR / f"{entry.obj_id}_convex_template_vband_trial_two_phase.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(4, 1, figsize=(11, 12.2), sharex=False)
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.065, top=0.9, hspace=0.18)
    fig.suptitle(f"{entry.obj_id} - convex dictionary I carrier applied to V", fontsize=15, fontweight="bold", y=0.99)
    subtitle = (
        f"period={entry.period:.7f} d   logP={math.log10(entry.period):.3f}   neighbors={DICTIONARY_NEIGHBORS}   "
        f"I active={int(i_fit['activeTemplates'])} effective={float(i_fit['effectiveTemplates']):.1f}   "
        f"phase shift={shift:+.4f}   V n={len(v_obs)}"
    )
    fig.text(0.5, 0.958, subtitle, ha="center", va="top", fontsize=9.1, color="#3d4652")

    x_i, y_i, e_i = duplicate_phase(phase_i, i_obs[:, 1], i_obs[:, 2])
    axes[0].errorbar(x_i, y_i, yerr=e_i, fmt=".", ms=4.0, lw=0.45, elinewidth=0.45, alpha=0.42, color="#2f6f9f", label="I photometry")
    if current_i_dense is not None:
        axes[0].plot(dense2, np.r_[current_i_dense, current_i_dense], color="#777777", lw=1.5, ls="--", label="current v16 I")
    axes[0].plot(dense2, np.r_[i_dense, i_dense], color="black", lw=2.2, label="dictionary I")
    axes[0].invert_yaxis()
    axes[0].set_ylabel("I mag")
    axes[0].grid(True, color="#e6e8ec", lw=0.8)
    axes[0].legend(loc="upper right", frameon=True, framealpha=0.92)

    x_v, y_v, e_v = duplicate_phase(phase_v, v_obs[:, 1], v_obs[:, 2])
    mask_v = np.asarray(v_fit["displayMask"], dtype=bool)
    mask_v2 = np.r_[mask_v, mask_v]
    axes[1].errorbar(x_v[mask_v2], y_v[mask_v2], yerr=e_v[mask_v2], fmt=".", ms=4.6, lw=0.5, elinewidth=0.5, alpha=0.58, color="#b45c2a", label="V photometry")
    if np.any(~mask_v2):
        axes[1].scatter(x_v[~mask_v2], y_v[~mask_v2], s=22, marker="x", color="#c43d3d", label="V display outlier")
    if current_v_line is not None:
        label = "current v16 V" if decode_current_color_curve(curve_entry) is not None else "current I + mean V-I"
        axes[1].plot(dense2, np.r_[current_v_line, current_v_line], color="#777777", lw=1.5, ls="--", label=label)
    axes[1].plot(dense2, np.r_[v_model_dense, v_model_dense], color="black", lw=2.2, label="V fit on I carrier")
    axes[1].invert_yaxis()
    axes[1].set_ylabel("V mag")
    axes[1].grid(True, color="#e6e8ec", lw=0.8)
    axes[1].legend(loc="upper right", frameon=True, framealpha=0.92)
    axes[1].text(
        0.012,
        0.035,
        f"current V MAD={current_v_mad:.4f} RMS={current_v_rms:.4f}   carrier V MAD={v_mad:.4f} RMS={v_rms:.4f}",
        transform=axes[1].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.8,
        bbox={"boxstyle": "round,pad=0.32", "fc": "white", "ec": "#ccd1d9", "alpha": 0.9},
    )

    x_c, y_c, _ = duplicate_phase(phase_v, color_at_v)
    axes[2].scatter(x_c, y_c, s=24, alpha=0.58, color="#7b4ab2", label="V - dictionary I at V epochs")
    if len(pairs):
        xp, yp, _ = duplicate_phase(pairs[:, 0], pairs[:, 1])
        axes[2].scatter(xp, yp, s=36, facecolors="none", edgecolors="#178f8f", linewidths=1.2, label=f"near-simultaneous V-I pairs ({len(pairs)})")
    axes[2].plot(dense2, np.r_[color_model_dense, color_model_dense], color="black", lw=2.0, label="carrier color curve")
    axes[2].axhline(entry.v_minus_i, color="#777777", lw=1.2, ls="--", label="catalog mean V-I")
    axes[2].invert_yaxis()
    axes[2].set_ylabel("V - I")
    axes[2].grid(True, color="#e6e8ec", lw=0.8)
    axes[2].legend(loc="upper right", frameon=True, framealpha=0.92)
    axes[2].text(
        0.012,
        0.035,
        f"carrier color MAD={c_mad:.4f} RMS={c_rms:.4f}",
        transform=axes[2].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.8,
        bbox={"boxstyle": "round,pad=0.32", "fc": "white", "ec": "#ccd1d9", "alpha": 0.9},
    )

    logp = np.asarray(dictionary["logp"], dtype=float)
    sizes = 20 + 650 * np.sqrt(np.maximum(weights, 0))
    axes[3].axvline(math.log10(entry.period), color="black", lw=1.6, label="target logP")
    axes[3].scatter(logp, weights, s=sizes, alpha=0.72, color="#2f6f9f", edgecolors="white", linewidths=0.5, label="I template weights")
    top = np.argsort(weights)[::-1][:6]
    for rank, index in enumerate(top, 1):
        if weights[index] <= 0:
            continue
        axes[3].annotate(str(rank), (logp[index], weights[index]), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=8)
    axes[3].set_ylim(-0.03, max(0.08, float(np.max(weights)) * 1.18 if weights.size else 0.08))
    axes[3].set_xlabel("Template log10(period)")
    axes[3].set_ylabel("Convex weight")
    axes[3].grid(True, color="#e6e8ec", lw=0.8)
    axes[3].legend(loc="upper right", frameon=True, framealpha=0.92)

    for ax in axes[:3]:
        ax.set_xlim(0, 2)
        ax.set_xticks(np.arange(0, 2.01, 0.25))
    axes[2].set_xlabel("Pulsation phase")

    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)

    summary = {
        "star": entry.obj_id,
        "periodDays": entry.period,
        "vN": int(len(v_obs)),
        "iActiveTemplates": int(i_fit["activeTemplates"]),
        "iEffectiveTemplates": float(i_fit["effectiveTemplates"]),
        "phaseShift": shift,
        "vMean": float(v_fit["mean"]),
        "vAmplitudeOnCarrier": float(v_fit["amplitude"]),
        "currentVMad": current_v_mad,
        "currentVRms": current_v_rms,
        "carrierVMad": v_mad,
        "carrierVRms": v_rms,
        "carrierColorMad": c_mad,
        "carrierColorRms": c_rms,
        "nearSimultaneousColorPairs": int(len(pairs)),
        "hasCurrentColorCurve": decode_current_color_curve(curve_entry) is not None,
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
        i_obs = read_band(entry, "I")
        v_obs = read_band(entry, "V")
        if i_obs.size == 0 or v_obs.size == 0:
            raise RuntimeError(f"Missing photometry for {star_id}")
        dictionary = select_dictionary(entry, fu_features)
        i_fit = fit_dictionary_template(entry, i_obs, dictionary)
        weights = np.asarray(i_fit["weights"], dtype=float)
        phase_v = phase_for(entry, v_obs[:, 0])
        carrier_v = evaluate_dictionary_carrier(dictionary, weights, phase_v, float(i_fit["phaseShift"]))
        v_fit = fit_band_to_carrier(phase_v, v_obs[:, 1], v_obs[:, 2], carrier_v)
        summaries.append(plot_star(entry, dictionary, i_fit, v_fit, curves))
    combined_path = OUT_DIR / "convex_template_vband_trial_examples_summary.json"
    combined_path.write_text(json.dumps({"stars": summaries}, indent=2), encoding="utf-8")
    print(json.dumps({"stars": summaries}, indent=2))


if __name__ == "__main__":
    main()
