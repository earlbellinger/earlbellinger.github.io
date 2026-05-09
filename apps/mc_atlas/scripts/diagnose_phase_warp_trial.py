"""Prototype period-local registered templates for Cepheid diagnostics.

This is intentionally diagnostic-only. It uses the existing high-quality
Fourier feature cache as the training set, builds a local FU Cepheid template
near each target period, registers neighboring curves with monotone phase
warps, then robustly fits the registered template to target I-band photometry.
"""

from __future__ import annotations

import base64
import json
import math
import tarfile
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]
FEATURE_CACHE = ROOT / "data" / "processed" / "pca_fourier_feature_cache_v2.npz"
CATALOG_CACHE = ROOT / "public" / "data" / "magellanic-clouds.json"
CURVE_CACHE = ROOT / "data" / "processed" / "ogle_color_curves.json"
PHOTOMETRY_ROOT = ROOT / "data" / "raw" / "ogle_photometry"
OUT_DIR = ROOT / "diagnostics" / "template_quality"

TARGET_STARS = ("OGLE-SMC-CEP-4953", "OGLE-SMC-CEP-4956")
TRAINING_NEIGHBORS = 72
REGISTRATION_ITERATIONS = 2
WARP_INTERVALS = 10
FIT_WARP_INTERVALS = 10
FEATURE_PHASE = np.linspace(0.0, 1.0, 1000, endpoint=False)


@dataclass
class CatalogEntry:
    obj_id: str
    location: str
    dataset: str
    mode: str
    subtype: str
    period: float
    t0: float
    i_mag: float
    v_minus_i: float
    amplitude_i: float


@dataclass
class TrialFit:
    mean: float
    amplitude: float
    phase_shift: float
    anchors: np.ndarray
    mask: np.ndarray
    model_at_obs: np.ndarray
    model_dense: np.ndarray
    residual: np.ndarray
    iterations: int
    rms: float
    mad: float


def percentile_span(values: np.ndarray, low: float = 5.0, high: float = 95.0) -> float:
    if values.size == 0:
        return math.nan
    p_low, p_high = np.percentile(values, [low, high])
    return float(p_high - p_low)


def normalize_shape(values: np.ndarray) -> np.ndarray:
    centered = values - float(np.mean(values))
    span = percentile_span(centered)
    if not math.isfinite(span) or span <= 0:
        return centered
    return centered / span


def periodic_interp(values: np.ndarray, phase: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    xp = np.arange(values.size + 1, dtype=float) / values.size
    yp = np.r_[values, values[0]]
    return np.interp(np.mod(phase, 1.0), xp, yp)


def duplicate_phase(phase: np.ndarray, values: np.ndarray, err: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    x = np.r_[phase, phase + 1.0]
    y = np.r_[values, values]
    if err is None:
        return x, y, None
    return x, y, np.r_[err, err]


def robust_mad(residual: np.ndarray, mask: np.ndarray | None = None) -> tuple[float, float, float]:
    values = residual if mask is None else residual[mask]
    if values.size == 0:
        return math.nan, math.nan, math.nan
    center = float(np.median(values))
    mad = float(1.4826 * np.median(np.abs(values - center)))
    rms = float(np.sqrt(np.mean(values * values)))
    return center, mad, rms


def coherence_preserving_rejection_mask(
    phase: np.ndarray,
    residual: np.ndarray,
    err: np.ndarray,
    current_mask: np.ndarray,
    *,
    sigma_multiplier: float = 4.0,
    local_window: float = 0.055,
    coherent_sigma: float = 1.6,
) -> np.ndarray:
    """Reject isolated residuals while preserving phase-coherent morphology.

    Cepheid bumps can appear as a same-sign residual over a finite phase
    interval when the current template is too rigid. A plain pointwise MAD
    filter erases exactly that signal. This filter only rejects a large
    residual when nearby phases do not show supporting residual structure.
    """

    center, mad, _ = robust_mad(residual, current_mask)
    sigma = max(0.012, mad, float(np.median(np.clip(err[current_mask], 0.008, 0.08))))
    scaled = (residual - center) / sigma
    candidate = np.abs(scaled) > sigma_multiplier
    next_mask = current_mask.copy()
    wrapped_phase = np.mod(phase, 1.0)

    for index in np.flatnonzero(candidate):
        distance = np.abs(wrapped_phase - wrapped_phase[index])
        distance = np.minimum(distance, 1.0 - distance)
        local = distance <= local_window
        if int(local.sum()) < 4:
            next_mask[index] = False
            continue
        same_sign = np.sign(scaled) == np.sign(scaled[index])
        coherent = local & same_sign & (np.abs(scaled) >= coherent_sigma)
        strong = local & same_sign & (np.abs(scaled) >= 0.75 * sigma_multiplier)
        # Protect broad, populated residual structure. Isolated bad points and
        # tiny clumps still get rejected.
        if int(coherent.sum()) >= 5 and int(strong.sum()) >= 2:
            next_mask[index] = True
        else:
            next_mask[index] = False

    return next_mask


def load_catalog() -> dict[str, CatalogEntry]:
    payload = json.loads(CATALOG_CACHE.read_text(encoding="utf-8"))
    fields = payload["fields"]["catalog"]
    idx = {name: i for i, name in enumerate(fields)}
    locations = payload["locations"]
    entries: dict[str, CatalogEntry] = {}
    for row in payload["datasets"]["catalog"]:
        obj_id = str(row[idx["id"]])
        required = (
            row[idx["periodDays"]],
            row[idx["t0HjdMinus2450000"]],
            row[idx["iMag"]],
            row[idx["vMinusI"]],
            row[idx["amplitudeI"]],
        )
        if any(value is None for value in required):
            continue
        dataset_index = int(row[idx["datasetIndex"]])
        location_index = int(row[idx["locationIndex"]])
        dataset = "cepheids" if dataset_index == 0 else "rrlyrae"
        entries[obj_id] = CatalogEntry(
            obj_id=obj_id,
            location=str(locations[location_index]),
            dataset=dataset,
            mode=str(row[idx["mode"]]),
            subtype=str(row[idx["lightCurveSubtype"]]),
            period=float(row[idx["periodDays"]]),
            t0=float(row[idx["t0HjdMinus2450000"]]),
            i_mag=float(row[idx["iMag"]]),
            v_minus_i=float(row[idx["vMinusI"]]),
            amplitude_i=float(row[idx["amplitudeI"]]),
        )
    return entries


def cepheid_family(entry: CatalogEntry) -> str:
    mode = entry.subtype or entry.mode
    if entry.dataset != "cepheids":
        return "RRab"
    if mode.startswith("F"):
        return "FU"
    if "1O" in mode or "2O" in mode:
        return "FO"
    return "FU"


def load_feature_shapes(catalog: dict[str, CatalogEntry], family: str) -> list[dict[str, object]]:
    with np.load(FEATURE_CACHE, allow_pickle=False) as payload:
        ids = payload["ids"].astype(str)
        shapes = payload["shapes"]
        harmonics = payload["harmonics"]
        cv_mse = payload["cvMse"]
    features: list[dict[str, object]] = []
    for index, obj_id in enumerate(ids):
        entry = catalog.get(str(obj_id))
        if entry is None or cepheid_family(entry) != family:
            continue
        features.append(
            {
                "id": str(obj_id),
                "entry": entry,
                "logp": math.log10(entry.period),
                "shape": np.asarray(shapes[index], dtype=float),
                "harmonics": int(harmonics[index]),
                "cvMse": float(cv_mse[index]),
            }
        )
    return features


def parse_ogle_dat(raw_bytes: bytes) -> np.ndarray:
    rows: list[tuple[float, float, float]] = []
    for raw_line in raw_bytes.decode("utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            rows.append((float(parts[0]), float(parts[1]), float(parts[2])))
        except ValueError:
            continue
    return np.asarray(rows, dtype=float) if rows else np.empty((0, 3), dtype=float)


def archive_for(entry: CatalogEntry) -> Path:
    prefix = "smc" if entry.obj_id.startswith("OGLE-SMC") else "lmc"
    kind = "cep" if entry.dataset == "cepheids" else "rrlyr"
    return PHOTOMETRY_ROOT / f"{prefix}_{kind}_phot.tar.gz"


def read_band(entry: CatalogEntry, band: str) -> np.ndarray:
    archive = archive_for(entry)
    with tarfile.open(archive, "r:gz") as tf:
        best: tuple[int, tarfile.TarInfo] | None = None
        for member in tf.getmembers():
            if not member.isfile() or entry.obj_id not in member.name:
                continue
            lower = member.name.lower().replace("\\", "/")
            score = 0
            if f"/{band.lower()}/" in lower:
                score += 10
            if lower.endswith(f"/{entry.obj_id.lower()}.dat"):
                score += 3
            if f".{band.lower()}." in lower or f"_{band.lower()}." in lower:
                score += 2
            if score and (best is None or score > best[0]):
                best = (score, member)
        if best is None:
            return np.empty((0, 3), dtype=float)
        handle = tf.extractfile(best[1])
        if handle is None:
            return np.empty((0, 3), dtype=float)
        return parse_ogle_dat(handle.read())


def phase_for(entry: CatalogEntry, times: np.ndarray) -> np.ndarray:
    return np.mod((times - entry.t0) / entry.period, 1.0)


def anchors_from_raw(raw: np.ndarray, intervals: int) -> np.ndarray:
    if raw.size == intervals - 1:
        raw = np.r_[raw, 0.0]
    shifted = raw - float(np.max(raw))
    increments = np.exp(shifted)
    increments /= float(np.sum(increments))
    return np.r_[0.0, np.cumsum(increments)]


def apply_warp(phase: np.ndarray, anchors: np.ndarray) -> np.ndarray:
    knots = np.linspace(0.0, 1.0, anchors.size)
    return np.interp(np.mod(phase, 1.0), knots, anchors)


def warp_penalty(anchors: np.ndarray) -> tuple[float, float]:
    knots = np.linspace(0.0, 1.0, anchors.size)
    identity = float(np.mean((anchors - knots) ** 2))
    smooth = float(np.mean(np.diff(anchors, n=2) ** 2)) if anchors.size > 3 else 0.0
    return identity, smooth


def fit_shape_warp(
    shape: np.ndarray,
    template: np.ndarray,
    *,
    intervals: int = WARP_INTERVALS,
    identity_weight: float = 0.25,
    smooth_weight: float = 0.25,
) -> np.ndarray:
    sub_index = np.linspace(0, FEATURE_PHASE.size - 1, 260, dtype=int)
    phase = FEATURE_PHASE[sub_index]
    y = shape[sub_index]

    def objective(raw: np.ndarray) -> float:
        anchors = anchors_from_raw(raw, intervals)
        warped_phase = apply_warp(phase, anchors)
        model = periodic_interp(template, warped_phase)
        identity, smooth = warp_penalty(anchors)
        return float(np.mean((y - model) ** 2) + identity_weight * identity + smooth_weight * smooth)

    result = minimize(
        objective,
        np.zeros(intervals - 1, dtype=float),
        method="L-BFGS-B",
        bounds=[(-1.4, 1.4)] * (intervals - 1),
        options={"maxiter": 90, "ftol": 1e-8},
    )
    raw = result.x if result.success or np.isfinite(result.fun) else np.zeros(intervals - 1, dtype=float)
    return anchors_from_raw(raw, intervals)


def build_registered_template(target: CatalogEntry, features: list[dict[str, object]]) -> dict[str, object]:
    target_logp = math.log10(target.period)
    candidates = [feature for feature in features if feature["id"] != target.obj_id]
    candidates.sort(key=lambda feature: abs(float(feature["logp"]) - target_logp))
    selected = candidates[:TRAINING_NEIGHBORS]
    distances = np.asarray([abs(float(feature["logp"]) - target_logp) for feature in selected], dtype=float)
    sigma = max(0.045, float(np.percentile(distances, 70)) if distances.size else 0.045)
    weights = np.exp(-0.5 * (distances / sigma) ** 2)
    weights = weights / float(np.sum(weights))
    shapes = np.vstack([feature["shape"] for feature in selected])

    template = normalize_shape(np.average(shapes, axis=0, weights=weights))
    mean_abs_warp = 0.0
    for _ in range(REGISTRATION_ITERATIONS):
        registered: list[np.ndarray] = []
        warp_sizes: list[float] = []
        for shape in shapes:
            anchors = fit_shape_warp(shape, template)
            inverse_phase = np.interp(FEATURE_PHASE, anchors, np.linspace(0.0, 1.0, anchors.size))
            registered.append(periodic_interp(shape, inverse_phase))
            warp_sizes.append(float(np.mean(np.abs(anchors - np.linspace(0.0, 1.0, anchors.size)))))
        template = normalize_shape(np.average(np.vstack(registered), axis=0, weights=weights))
        mean_abs_warp = float(np.average(warp_sizes, weights=weights))

    return {
        "phase": FEATURE_PHASE,
        "template": template,
        "selected": selected,
        "weights": weights,
        "sigma": sigma,
        "meanAbsTrainingWarp": mean_abs_warp,
    }


def solve_mean_amplitude(shape: np.ndarray, mag: np.ndarray, err: np.ndarray) -> tuple[float, float, np.ndarray]:
    weights = 1.0 / np.clip(err, 0.008, 0.08) ** 2
    matrix = np.column_stack([np.ones(shape.size), shape])
    weighted_matrix = matrix * np.sqrt(weights)[:, None]
    weighted_mag = mag * np.sqrt(weights)
    coeffs, *_ = np.linalg.lstsq(weighted_matrix, weighted_mag, rcond=None)
    model = matrix @ coeffs
    return float(coeffs[0]), float(coeffs[1]), model


def fit_registered_template_to_photometry(entry: CatalogEntry, photometry: np.ndarray, template: np.ndarray) -> TrialFit:
    phase = phase_for(entry, photometry[:, 0])
    mag = photometry[:, 1]
    err = photometry[:, 2]
    amp_scale = max(0.05, percentile_span(mag))
    dense = np.linspace(0.0, 1.0, 1200, endpoint=False)
    mask = np.ones(phase.size, dtype=bool)
    best_params = np.zeros(FIT_WARP_INTERVALS, dtype=float)
    best_params[0] = 0.0
    best_fit: tuple[float, float, np.ndarray, np.ndarray] | None = None
    iterations = 0

    def evaluate(params: np.ndarray, eval_phase: np.ndarray, eval_mag: np.ndarray, eval_err: np.ndarray) -> tuple[float, float, np.ndarray, np.ndarray]:
        shift = float(params[0])
        anchors = anchors_from_raw(params[1:], FIT_WARP_INTERVALS)
        warped_phase = apply_warp(eval_phase + shift, anchors)
        shape = periodic_interp(template, warped_phase)
        mean, amplitude, model = solve_mean_amplitude(shape, eval_mag, eval_err)
        return mean, amplitude, model, shape

    for iteration in range(8):
        iterations = iteration + 1
        phase_fit = phase[mask]
        mag_fit = mag[mask]
        err_fit = err[mask]

        starts = [best_params]
        if iteration == 0:
            for shift in np.linspace(-0.08, 0.08, 9):
                params = np.zeros(FIT_WARP_INTERVALS, dtype=float)
                params[0] = shift
                starts.append(params)

        def objective(params: np.ndarray) -> float:
            mean, amplitude, model, _ = evaluate(params, phase_fit, mag_fit, err_fit)
            residual = (mag_fit - model) / amp_scale
            anchors = anchors_from_raw(params[1:], FIT_WARP_INTERVALS)
            identity, smooth = warp_penalty(anchors)
            shift_penalty = (float(params[0]) / 0.08) ** 2
            # Mild regularization: enough to stop point chasing, not enough to
            # prevent the bump from moving when the full curve supports it.
            return float(
                np.mean(residual**2)
                + 0.012 * identity / (0.08**2)
                + 0.006 * smooth / (0.05**2)
                + 0.001 * shift_penalty
            )

        best_result = None
        for start in starts:
            result = minimize(
                objective,
                start,
                method="L-BFGS-B",
                bounds=[(-0.1, 0.1)] + [(-1.6, 1.6)] * (FIT_WARP_INTERVALS - 1),
                options={"maxiter": 180, "ftol": 1e-9},
            )
            if best_result is None or result.fun < best_result.fun:
                best_result = result
        best_params = best_result.x if best_result is not None else best_params

        mean, amplitude, _, _ = evaluate(best_params, phase_fit, mag_fit, err_fit)
        anchors = anchors_from_raw(best_params[1:], FIT_WARP_INTERVALS)
        all_shape = periodic_interp(template, apply_warp(phase + float(best_params[0]), anchors))
        all_model = mean + amplitude * all_shape
        residual = mag - all_model
        next_mask = coherence_preserving_rejection_mask(phase, residual, err, mask)
        if int(next_mask.sum()) < max(20, int(0.55 * phase.size)):
            next_mask = mask
        best_fit = (mean, amplitude, all_model, residual)
        if np.array_equal(next_mask, mask):
            break
        mask = next_mask

    mean, amplitude, _, _ = evaluate(best_params, phase[mask], mag[mask], err[mask])
    anchors = anchors_from_raw(best_params[1:], FIT_WARP_INTERVALS)
    model_at_obs = mean + amplitude * periodic_interp(template, apply_warp(phase + float(best_params[0]), anchors))
    model_dense = mean + amplitude * periodic_interp(template, apply_warp(dense + float(best_params[0]), anchors))
    residual = mag - model_at_obs
    _, mad, rms = robust_mad(residual, mask)
    return TrialFit(
        mean=mean,
        amplitude=amplitude,
        phase_shift=float(best_params[0]),
        anchors=anchors,
        mask=mask,
        model_at_obs=model_at_obs,
        model_dense=model_dense,
        residual=residual,
        iterations=iterations,
        rms=rms,
        mad=mad,
    )


def decode_current_i_curve(curve_entry: dict[str, object], entry: CatalogEntry) -> np.ndarray | None:
    encoded = curve_entry.get("iCurve")
    if not isinstance(encoded, str):
        return None
    offsets = np.frombuffer(base64.b64decode(encoded), dtype="<i2").astype(float) / 1000.0
    dense = np.linspace(0.0, 1.0, 1200, endpoint=False)
    return entry.i_mag + periodic_interp(offsets, dense)


def current_model_at_obs(curve_entry: dict[str, object], entry: CatalogEntry, phase: np.ndarray) -> np.ndarray | None:
    encoded = curve_entry.get("iCurve")
    if not isinstance(encoded, str):
        return None
    offsets = np.frombuffer(base64.b64decode(encoded), dtype="<i2").astype(float) / 1000.0
    return entry.i_mag + periodic_interp(offsets, phase)


def plot_star(
    entry: CatalogEntry,
    photometry: np.ndarray,
    template_info: dict[str, object],
    trial: TrialFit,
    current_curve_entry: dict[str, object],
) -> dict[str, object]:
    phase = phase_for(entry, photometry[:, 0])
    dense = np.linspace(0.0, 1.0, 1200, endpoint=False)
    dense2 = np.r_[dense, dense + 1.0]
    current_dense = decode_current_i_curve(current_curve_entry, entry)
    current_obs = current_model_at_obs(current_curve_entry, entry, phase)
    current_residual = photometry[:, 1] - current_obs if current_obs is not None else np.full(phase.size, np.nan)
    _, current_mad, current_rms = robust_mad(current_residual)
    _, trial_all_mad, trial_all_rms = robust_mad(trial.residual)

    out_path = OUT_DIR / f"{entry.obj_id}_registered_phase_warp_trial_two_phase.png"
    summary_path = OUT_DIR / f"{entry.obj_id}_registered_phase_warp_trial_two_phase.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(3, 1, figsize=(11, 9.6), sharex=True)
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.075, top=0.885, hspace=0.07)
    fig.suptitle(f"{entry.obj_id} - registered period-local template trial", fontsize=15, fontweight="bold", y=0.985)
    subtitle = (
        f"period={entry.period:.7f} d   mode={entry.mode}/{entry.subtype}   "
        f"training neighbors={len(template_info['selected'])}   logP sigma={float(template_info['sigma']):.3f}   "
        f"target phase shift={trial.phase_shift:+.4f}   kept/rejected={int(trial.mask.sum())}/{int((~trial.mask).sum())}"
    )
    fig.text(0.5, 0.952, subtitle, ha="center", va="top", fontsize=9.2, color="#3d4652")

    x, y, e = duplicate_phase(phase, photometry[:, 1], photometry[:, 2])
    kept2 = np.r_[trial.mask, trial.mask]
    axes[0].errorbar(x[kept2], y[kept2], yerr=e[kept2], fmt=".", ms=4.2, lw=0.45, elinewidth=0.45, alpha=0.48, color="#2f6f9f", label="retained I photometry")
    if np.any(~kept2):
        axes[0].scatter(x[~kept2], y[~kept2], s=18, marker="x", color="#c43d3d", alpha=0.72, label="trial rejected")
    if current_dense is not None:
        axes[0].plot(dense2, np.r_[current_dense, current_dense], color="#777777", lw=1.7, ls="--", label="current v16 PCA")
    axes[0].plot(dense2, np.r_[trial.model_dense, trial.model_dense], color="black", lw=2.3, label="registered warp trial")
    axes[0].invert_yaxis()
    axes[0].set_ylabel("I mag")
    axes[0].grid(True, color="#e6e8ec", lw=0.8)
    axes[0].legend(loc="upper right", frameon=True, framealpha=0.92)
    axes[0].text(
        0.012,
        0.035,
        f"current MAD={current_mad:.4f} RMS={current_rms:.4f}   trial kept MAD={trial.mad:.4f} RMS={trial.rms:.4f}   trial all MAD={trial_all_mad:.4f}",
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
    xr, yr, _ = duplicate_phase(phase, trial.residual)
    axes[1].scatter(xr[kept2], yr[kept2], s=14, alpha=0.52, color="#2f6f9f", label="trial retained residual")
    if np.any(~kept2):
        axes[1].scatter(xr[~kept2], yr[~kept2], s=18, marker="x", color="#c43d3d", alpha=0.72, label="trial rejected residual")
    axes[1].set_ylabel("I residual")
    axes[1].grid(True, color="#e6e8ec", lw=0.8)
    axes[1].legend(loc="upper right", frameon=True, framealpha=0.92)

    knots = np.linspace(0.0, 1.0, trial.anchors.size)
    warp_dense = apply_warp(dense, trial.anchors)
    axes[2].plot(dense2, np.r_[warp_dense, warp_dense + 1.0], color="black", lw=2.0, label="target warp W(phase)")
    axes[2].plot([0, 2], [0, 2], color="#777777", lw=1.4, ls="--", label="identity")
    axes[2].scatter(knots, trial.anchors, color="#2f6f9f", s=22, zorder=3, label="warp knots")
    axes[2].scatter(knots + 1.0, trial.anchors + 1.0, color="#2f6f9f", s=22, zorder=3)
    axes[2].set_ylabel("template phase")
    axes[2].set_xlabel("Pulsation phase")
    axes[2].grid(True, color="#e6e8ec", lw=0.8)
    axes[2].legend(loc="upper left", frameon=True, framealpha=0.92)

    for ax in axes:
        ax.set_xlim(0, 2)
        ax.set_xticks(np.arange(0, 2.01, 0.25))

    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)

    summary = {
        "star": entry.obj_id,
        "periodDays": entry.period,
        "family": cepheid_family(entry),
        "trainingNeighbors": len(template_info["selected"]),
        "trainingLogPSigma": float(template_info["sigma"]),
        "trainingMeanAbsWarp": float(template_info["meanAbsTrainingWarp"]),
        "trialMean": trial.mean,
        "trialAmplitude": trial.amplitude,
        "trialPhaseShift": trial.phase_shift,
        "trialWarpAnchors": [float(value) for value in trial.anchors],
        "trialKept": int(trial.mask.sum()),
        "trialRejected": int((~trial.mask).sum()),
        "trialIterations": trial.iterations,
        "currentResidualMad": current_mad,
        "currentResidualRms": current_rms,
        "trialKeptResidualMad": trial.mad,
        "trialKeptResidualRms": trial.rms,
        "trialAllResidualMad": trial_all_mad,
        "trialAllResidualRms": trial_all_rms,
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
    summaries = []
    for star_id in TARGET_STARS:
        entry = catalog[star_id]
        photometry = read_band(entry, "I")
        if photometry.size == 0:
            raise RuntimeError(f"No I-band photometry for {star_id}")
        template_info = build_registered_template(entry, fu_features)
        trial = fit_registered_template_to_photometry(entry, photometry, np.asarray(template_info["template"], dtype=float))
        summaries.append(plot_star(entry, photometry, template_info, trial, curves[star_id]))
    combined_path = OUT_DIR / "registered_phase_warp_trial_examples_summary.json"
    combined_path.write_text(json.dumps({"stars": summaries}, indent=2), encoding="utf-8")
    print(json.dumps({"stars": summaries}, indent=2))


if __name__ == "__main__":
    main()
