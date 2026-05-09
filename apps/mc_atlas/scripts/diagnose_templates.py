from __future__ import annotations

import csv
import base64
import binascii
import json
import math
import tarfile
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "public" / "data" / "magellanic-clouds.json"
CURVE_CACHE = ROOT / "data" / "processed" / "ogle_color_curves.json"
RAW = ROOT / "data" / "raw"
OUT = ROOT / "diagnostics" / "template_quality"
PHOT_CACHE = OUT / "photometry"

IDX = {
    "dataset": 7,
    "location": 8,
    "period": 9,
    "i_mag": 13,
    "mode": 16,
    "id": 17,
    "amplitude": 18,
    "t0": 19,
    "r21": 20,
    "phi21": 21,
    "r31": 22,
    "phi31": 23,
    "subtype": 24,
    "brightness_curve": 27,
    "brightness_quality": 28,
}

DATASET_NAMES = {0: "cepheids", 1: "rrlyrae"}
LABELS = {"cepheids": "Cepheids", "rrlyrae": "RR Lyrae"}
OCVS_PATH = {"cepheids": "cep", "rrlyrae": "rrlyr"}
LOCATIONS = {0: "LMC", 1: "SMC"}
ARCHIVE_PATHS = {
    ("LMC", "cepheids"): RAW / "ogle_photometry" / "lmc_cep_phot.tar.gz",
    ("SMC", "cepheids"): RAW / "ogle_photometry" / "smc_cep_phot.tar.gz",
    ("LMC", "rrlyrae"): RAW / "ogle_photometry" / "lmc_rrlyr_phot.tar.gz",
    ("SMC", "rrlyrae"): RAW / "ogle_photometry" / "smc_rrlyr_phot.tar.gz",
}
SAMPLE_SIZE = 10
WAVEFORM_SAMPLES = 96
LIGHT_CURVE_SCALE = 200
LIGHT_CURVE_ZERO = 128
LIGHT_CURVE_INT16_SCALE = 1000
BASE_URL = "https://ogle.astrouw.edu.pl/ogle/ogle4/OCVS"
PHOTOMETRY_MEMO: dict[str, np.ndarray | None] = {}


def positive_modulo(value: np.ndarray | float, divisor: float) -> np.ndarray | float:
    return ((value % divisor) + divisor) % divisor


def select_period_quantiles(rows: list[list[object]], size: int) -> list[list[object]]:
    ordered = sorted(rows, key=lambda row: float(row[IDX["period"]]))
    if len(ordered) <= size:
        return ordered

    picks: list[list[object]] = []
    used: set[str] = set()
    for fraction in np.linspace(0.05, 0.95, size):
        center = int(round(fraction * (len(ordered) - 1)))
        added = False
        for offset in range(len(ordered)):
            candidates = [center + offset]
            if offset:
                candidates.append(center - offset)
            for index in candidates:
                if 0 <= index < len(ordered):
                    row = ordered[index]
                    obj_id = str(row[IDX["id"]])
                    if obj_id not in used:
                        used.add(obj_id)
                        picks.append(row)
                        added = True
                        break
            if added:
                break
    return picks


def photometry_url(row: list[object]) -> str:
    dataset = DATASET_NAMES[int(row[IDX["dataset"]])]
    location = LOCATIONS[int(row[IDX["location"]])].lower()
    return f"{BASE_URL}/{location}/{OCVS_PATH[dataset]}/phot/I/{row[IDX['id']]}.dat"


def parse_photometry(raw: bytes) -> np.ndarray:
    values = np.fromstring(raw.decode("ascii", errors="ignore"), sep=" ", dtype=float)
    if values.size < 3:
        return np.empty((0, 3), dtype=float)
    rows = values[: values.size - (values.size % 3)].reshape(-1, 3)
    mask = np.isfinite(rows).all(axis=1) & (rows[:, 2] > 0) & (rows[:, 1] < 90)
    return rows[mask]


def fetch_archive_photometry(row: list[object]) -> np.ndarray | None:
    obj_id = str(row[IDX["id"]])
    if obj_id in PHOTOMETRY_MEMO:
        cached = PHOTOMETRY_MEMO[obj_id]
        return None if cached is None else cached.copy()

    dataset = DATASET_NAMES[int(row[IDX["dataset"]])]
    location = LOCATIONS[int(row[IDX["location"]])]
    archive = ARCHIVE_PATHS.get((location, dataset))
    if archive is None or not archive.exists():
        PHOTOMETRY_MEMO[obj_id] = None
        return None

    member_name = f"phot/I/{obj_id}.dat"
    with tarfile.open(archive, "r:gz") as tar:
        try:
            member = tar.getmember(member_name)
        except KeyError:
            PHOTOMETRY_MEMO[obj_id] = None
            return None
        extracted = tar.extractfile(member)
        if extracted is None:
            PHOTOMETRY_MEMO[obj_id] = None
            return None
        data = parse_photometry(extracted.read())
        PHOTOMETRY_MEMO[obj_id] = data
        return data.copy()


def fetch_photometry(row: list[object]) -> np.ndarray:
    dataset = DATASET_NAMES[int(row[IDX["dataset"]])]
    location = LOCATIONS[int(row[IDX["location"]])].lower()
    target = PHOT_CACHE / location / dataset / f"{row[IDX['id']]}.dat"
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        return parse_photometry(target.read_bytes())

    try:
        request = urllib.request.Request(
            photometry_url(row),
            headers={"User-Agent": "mc-atlas-template-diagnostics/1.0"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            target.write_bytes(response.read())
        return parse_photometry(target.read_bytes())
    except Exception:
        archive_data = fetch_archive_photometry(row)
        if archive_data is not None:
            return archive_data
        raise



def load_curve_cache() -> dict[str, dict[str, object]]:
    if not CURVE_CACHE.exists():
        return {}
    payload = json.loads(CURVE_CACHE.read_text(encoding="utf-8"))
    curves = payload.get("curves", payload)
    if not isinstance(curves, dict):
        return {}
    return {str(key): value for key, value in curves.items() if isinstance(value, dict)}


def template_source_label(row: list[object], curve_cache: dict[str, dict[str, object]]) -> str:
    if decode_light_curve(row) is None:
        return "Fourier"
    info = curve_cache.get(str(row[IDX["id"]]), {})
    source_value = str(info.get("templateSource", "fitted"))
    if source_value == "phase-pca99":
        return f"PCA99 Q{row[IDX['brightness_quality']]}"
    if source_value == "pca":
        source_value = "fourier-pca"
    source = source_value.replace("-", " ").upper()
    return f"{source} I Q{row[IDX['brightness_quality']]}"


def browser_flux_waveform(row: list[object]) -> np.ndarray:
    amp = float(row[IDX["amplitude"]])
    r21 = float(row[IDX["r21"]])
    phi21 = float(row[IDX["phi21"]])
    r31 = float(row[IDX["r31"]])
    phi31 = float(row[IDX["phi31"]])

    shape: list[float] = []
    for index in range(WAVEFORM_SAMPLES):
        angle = (index / WAVEFORM_SAMPLES) * math.tau
        shape.append(
            math.cos(angle)
            + r21 * math.cos(2 * angle + phi21)
            + r31 * math.cos(3 * angle + phi31)
        )

    brightest_index = int(np.argmin(shape))
    minimum = min(shape)
    maximum = max(shape)
    midpoint = (maximum + minimum) / 2
    value_range = max(0.001, maximum - minimum)

    waveform = []
    for index in range(WAVEFORM_SAMPLES):
        shifted = shape[(index + brightest_index) % WAVEFORM_SAMPLES]
        magnitude_offset = ((shifted - midpoint) / value_range) * amp
        waveform.append(min(2.9, max(0.36, 10 ** (-0.4 * magnitude_offset))))
    return np.array(waveform, dtype=float)


def decode_light_curve(row: list[object]) -> np.ndarray | None:
    encoded = row[IDX["brightness_curve"]] if len(row) > IDX["brightness_curve"] else None
    if not encoded:
        return None
    try:
        raw = base64.b64decode(str(encoded), validate=True)
    except (ValueError, binascii.Error):
        return None
    if len(raw) < 8:
        return None
    if len(raw) == WAVEFORM_SAMPLES * 2:
        return np.frombuffer(raw, dtype="<i2").astype(float) / LIGHT_CURVE_INT16_SCALE
    return np.array([(value - LIGHT_CURVE_ZERO) / LIGHT_CURVE_SCALE for value in raw], dtype=float)


def sample_periodic(samples: np.ndarray, phase: np.ndarray) -> np.ndarray:
    sample = np.mod(phase, 1.0) * len(samples)
    index = np.floor(sample).astype(int) % len(samples)
    next_index = (index + 1) % len(samples)
    fraction = sample - np.floor(sample)
    return samples[index] * (1 - fraction) + samples[next_index] * fraction


def template_mag_at_phase(row: list[object], phase: np.ndarray) -> np.ndarray:
    fitted = decode_light_curve(row)
    if fitted is not None:
        return sample_periodic(fitted, phase)

    waveform = browser_flux_waveform(row)
    flux = sample_periodic(waveform, phase)
    return -2.5 * np.log10(flux)


def phase_photometry(row: list[object], photometry: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    period = float(row[IDX["period"]])
    t0 = float(row[IDX["t0"]])
    phase = positive_modulo((photometry[:, 0] - t0) / period, 1.0)
    return phase, photometry[:, 1], photometry[:, 2]


def robust_overlay_stats(row: list[object], phase: np.ndarray, mag: np.ndarray, err: np.ndarray) -> dict[str, float]:
    model = template_mag_at_phase(row, phase)
    residual_base = mag - model
    offset = float(np.median(residual_base))
    residual = residual_base - offset

    for _ in range(3):
        mad = float(np.median(np.abs(residual - np.median(residual))))
        sigma = max(0.02, 1.4826 * mad)
        mask = np.abs(residual) < 4 * sigma
        if mask.sum() < 12:
            break
        weights = 1 / np.clip(err[mask], 0.005, 0.2) ** 2
        offset = float(np.average(residual_base[mask], weights=weights))
        residual = residual_base - offset

    mad = float(np.median(np.abs(residual - np.median(residual))))
    sigma = max(0.02, 1.4826 * mad)
    mask = np.abs(residual) < 4 * sigma
    if mask.sum() < 12:
        mask = np.ones_like(residual, dtype=bool)

    rms = float(np.sqrt(np.mean(residual[mask] ** 2)))
    obs_amp = float(np.nanpercentile(mag[mask], 95) - np.nanpercentile(mag[mask], 5))
    tmpl_phase = np.linspace(0, 1, 400, endpoint=False)
    tmpl_mag = template_mag_at_phase(row, tmpl_phase)
    tmpl_amp = float(np.max(tmpl_mag) - np.min(tmpl_mag))
    return {
        "offset": offset,
        "rms_mag": rms,
        "mad_mag": float(1.4826 * mad),
        "n_points": int(mask.sum()),
        "n_total": int(len(mag)),
        "observed_amp_p95_p05": obs_amp,
        "template_amp": tmpl_amp,
        "amp_ratio_template_observed": tmpl_amp / obs_amp if obs_amp > 0 else math.nan,
    }


def quality_label(row: list[object], stats: dict[str, float]) -> str:
    dataset = DATASET_NAMES[int(row[IDX["dataset"]])]
    amp_ratio = stats["amp_ratio_template_observed"]
    rms = stats["rms_mag"]

    if dataset == "cepheids":
        if rms <= 0.055 and 0.75 <= amp_ratio <= 1.25:
            return "good"
        if rms <= 0.09 and 0.6 <= amp_ratio <= 1.45:
            return "ok"
        return "poor"

    if rms <= 0.09 and 0.6 <= amp_ratio <= 1.35:
        return "good"
    if rms <= 0.14 and 0.45 <= amp_ratio <= 1.55:
        return "ok"
    return "poor"


def make_group_plot(
    group_key: tuple[str, str],
    rows: list[list[object]],
    summaries: list[dict[str, object]],
    curve_cache: dict[str, dict[str, object]],
) -> None:
    location, dataset = group_key
    fig, axes = plt.subplots(5, 2, figsize=(12, 15), sharex=True)
    axes = axes.ravel()
    fig.suptitle(f"{location} {LABELS[dataset]}: observed I-band phase curve vs app I-band template", fontsize=15)

    for axis, row in zip(axes, rows):
        template_source = template_source_label(row, curve_cache)
        phot = fetch_photometry(row)
        phase, mag, err = phase_photometry(row, phot)
        stats = robust_overlay_stats(row, phase, mag, err)
        label = quality_label(row, stats)
        summaries.append(
            {
                "location": location,
                "dataset": dataset,
                "id": row[IDX["id"]],
                "subtype": row[IDX["subtype"]] or row[IDX["mode"]] or "",
                "period_days": row[IDX["period"]],
                "t0": row[IDX["t0"]],
                "amplitude_i": row[IDX["amplitude"]],
                "r21": row[IDX["r21"]],
                "phi21": row[IDX["phi21"]],
                "r31": row[IDX["r31"]],
                "phi31": row[IDX["phi31"]],
                "template_source": template_source,
                "photometry_url": photometry_url(row),
                "quality": label,
                **stats,
            }
        )

        order = np.argsort(phase)
        phase_line = np.linspace(0, 1, 500, endpoint=True)
        template = template_mag_at_phase(row, phase_line) + stats["offset"]

        axis.errorbar(
            phase[order],
            mag[order],
            yerr=err[order],
            fmt=".",
            ms=2.3,
            lw=0.35,
            color="#2f5f9f",
            ecolor="#9fb7d6",
            alpha=0.62,
        )
        axis.plot(phase_line, template, color="#d1452f", lw=1.8)
        axis.invert_yaxis()
        axis.set_xlim(0, 1)
        axis.grid(True, alpha=0.22, lw=0.5)
        axis.set_title(
            f"{row[IDX['id']]}  {row[IDX['subtype']]}  P={float(row[IDX['period']]):.3f}d  "
            f"RMS={stats['rms_mag']:.3f}  {label}  {template_source}",
            fontsize=9.5,
        )
        axis.set_ylabel("I mag")

    for axis in axes[len(rows) :]:
        axis.axis("off")
    for axis in axes[-2:]:
        axis.set_xlabel("phase")

    fig.tight_layout(rect=(0, 0, 1, 0.975))
    path = OUT / f"{location.lower()}_{dataset}_template_quality.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)


def candidate_sort_key(row: list[object], curve_cache: dict[str, dict[str, object]], tier: int) -> tuple[float, ...]:
    info = curve_cache.get(str(row[IDX["id"]]), {})
    i_rms = float(info.get("iRms", math.inf))
    raw_rms = float(info.get("rawRms", i_rms))
    n_points = float(info.get("iN", 0))
    residual_span = float(info.get("residualSpan", 0))
    masked = float(info.get("eclipseMasked", 0))

    if tier >= 3:
        return (i_rms, -n_points, raw_rms)
    return (-raw_rms, -residual_span, masked, n_points)


def select_quality_tier_examples(
    groups: dict[tuple[str, str], list[list[object]]],
    curve_cache: dict[str, dict[str, object]],
) -> list[tuple[str, tuple[str, str], list[object]]]:
    examples: list[tuple[str, tuple[str, str], list[object]]] = []
    group_order = [("LMC", "cepheids"), ("SMC", "cepheids"), ("LMC", "rrlyrae"), ("SMC", "rrlyrae")]

    for label, tier in [("high Q3", 3), ("low Q1", 1)]:
        for group_key in group_order:
            candidates = [
                row
                for row in groups.get(group_key, [])
                if len(row) > IDX["brightness_quality"]
                and int(row[IDX["brightness_quality"]] or 0) == tier
                and decode_light_curve(row) is not None
            ]
            candidates.sort(key=lambda row: candidate_sort_key(row, curve_cache, tier))

            for row in candidates[:40]:
                try:
                    phot = fetch_photometry(row)
                except Exception as exc:  # pragma: no cover - diagnostic script
                    print(f"Skipping {row[IDX['id']]} quality example: {exc}")
                    continue
                if len(phot) >= 12:
                    examples.append((label, group_key, row))
                    break

    return examples


def make_quality_tier_plot(
    groups: dict[tuple[str, str], list[list[object]]],
    curve_cache: dict[str, dict[str, object]],
) -> list[dict[str, object]]:
    examples = select_quality_tier_examples(groups, curve_cache)
    if not examples:
        return []

    fig, axes = plt.subplots(2, 4, figsize=(16, 7.5), sharex=True)
    fig.suptitle("99% phase-PCA carrier light curves applied to high- and low-quality OGLE I-band data", fontsize=15)
    example_summaries: list[dict[str, object]] = []

    for axis, (tier_label, group_key, row) in zip(axes.ravel(), examples):
        phot = fetch_photometry(row)
        phase, mag, err = phase_photometry(row, phot)
        stats = robust_overlay_stats(row, phase, mag, err)
        template_source = template_source_label(row, curve_cache)
        info = curve_cache.get(str(row[IDX["id"]]), {})
        phase_offset = float(info.get("pcaPhaseOffset", 0.0))
        flags = info.get("variabilityFlags", [])
        flag_label = ",".join(str(flag) for flag in flags) if isinstance(flags, list) else str(flags or "")

        order = np.argsort(phase)
        phase_line = np.linspace(0, 1, 500, endpoint=True)
        template = template_mag_at_phase(row, phase_line) + stats["offset"]

        axis.errorbar(
            phase[order],
            mag[order],
            yerr=err[order],
            fmt=".",
            ms=2.4,
            lw=0.35,
            color="#345f91" if tier_label.startswith("high") else "#6754a4",
            ecolor="#aebbd0",
            alpha=0.64,
        )
        axis.plot(phase_line, template, color="#d1452f", lw=2.0)
        axis.invert_yaxis()
        axis.set_xlim(0, 1)
        axis.grid(True, alpha=0.22, lw=0.5)
        axis.set_title(
            f"{tier_label}  {group_key[0]} {LABELS[group_key[1]]}\n"
            f"{row[IDX['id']]}  {row[IDX['subtype']]}  P={float(row[IDX['period']]):.3f}d\n"
            f"{template_source}  RMS={float(info.get('iRms', math.nan)):.3f}  raw={float(info.get('rawRms', math.nan)):.3f}  dphi={phase_offset:+.3f}",
            fontsize=8.5,
        )
        axis.set_ylabel("I mag")
        axis.set_xlabel("phase")

        example_summaries.append(
            {
                "tier": tier_label,
                "location": group_key[0],
                "dataset": group_key[1],
                "id": row[IDX["id"]],
                "subtype": row[IDX["subtype"]] or row[IDX["mode"]] or "",
                "period_days": row[IDX["period"]],
                "template_source": template_source,
                "brightness_quality": row[IDX["brightness_quality"]],
                "i_rms": info.get("iRms", ""),
                "raw_rms": info.get("rawRms", ""),
                "i_n": info.get("iN", ""),
                "i_span": info.get("iSpan", ""),
                "residual_span": info.get("residualSpan", ""),
                "eclipse_masked": info.get("eclipseMasked", ""),
                "pca_components": info.get("pcaComponents", ""),
                "pca_raw_rejected": info.get("pcaRawRejected", ""),
                "pca_phase_offset": info.get("pcaPhaseOffset", ""),
                "variability_flags": flag_label,
                "overlay_rms_mag": stats["rms_mag"],
                "overlay_mad_mag": stats["mad_mag"],
                "photometry_url": photometry_url(row),
            }
        )

    for axis in axes.ravel()[len(examples) :]:
        axis.axis("off")

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(OUT / "quality_tier_examples.png", dpi=180)
    plt.close(fig)
    return example_summaries


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    rows = payload["datasets"]["catalog"]
    curve_cache = load_curve_cache()

    groups: dict[tuple[str, str], list[list[object]]] = {}
    for row in rows:
        dataset = DATASET_NAMES[int(row[IDX["dataset"]])]
        location_index = int(row[IDX["location"]])
        if location_index not in LOCATIONS:
            continue
        if row[IDX["amplitude"]] is None:
            continue
        location = LOCATIONS[location_index]
        groups.setdefault((location, dataset), []).append(row)

    summaries: list[dict[str, object]] = []
    selected: dict[tuple[str, str], list[list[object]]] = {}
    for key in [("LMC", "cepheids"), ("SMC", "cepheids"), ("LMC", "rrlyrae"), ("SMC", "rrlyrae")]:
        candidates = select_period_quantiles(groups[key], SAMPLE_SIZE * 3)
        valid: list[list[object]] = []
        for row in candidates:
            try:
                phot = fetch_photometry(row)
            except Exception as exc:  # pragma: no cover - diagnostic script
                print(f"Skipping {row[IDX['id']]}: {exc}")
                continue
            if len(phot) >= 20:
                valid.append(row)
            if len(valid) == SAMPLE_SIZE:
                break
        if len(valid) < SAMPLE_SIZE:
            raise RuntimeError(f"Only found {len(valid)} valid rows for {key}")
        selected[key] = valid

    for key, sample_rows in selected.items():
        make_group_plot(key, sample_rows, summaries, curve_cache)

    fieldnames = list(summaries[0].keys())
    with (OUT / "template_quality_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries)

    quality_examples = make_quality_tier_plot(groups, curve_cache)
    if quality_examples:
        with (OUT / "quality_tier_examples.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(quality_examples[0].keys()))
            writer.writeheader()
            writer.writerows(quality_examples)

    totals: dict[str, dict[str, int]] = {}
    for row in summaries:
        key = f"{row['location']} {row['dataset']}"
        totals.setdefault(key, {"good": 0, "ok": 0, "poor": 0})
        totals[key][str(row["quality"])] += 1
    print(json.dumps(totals, indent=2))
    if quality_examples:
        print(f"Wrote {len(quality_examples)} quality-tier examples")
    print(f"Wrote diagnostics to {OUT}")


if __name__ == "__main__":
    main()
