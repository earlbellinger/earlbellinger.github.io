from __future__ import annotations

import base64
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import prepare_data as prep


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "public" / "data" / "magellanic-clouds.json"
OUT_DIR = ROOT / "diagnostics" / "color_fit_extremes"

IDX = {
    "period": 9,
    "v_minus_i": 11,
    "dataset": 7,
    "location": 8,
    "id": 17,
    "amplitude_i": 18,
    "t0": 19,
    "mode": 24,
    "color_curve": 25,
    "quality": 26,
}

LOCATION_NAMES = {0: "LMC", 1: "SMC"}
DATASET_NAMES = {0: "cepheids", 1: "rrlyrae"}


def decode_color_curve(encoded: str) -> np.ndarray:
    raw = np.frombuffer(base64.b64decode(encoded), dtype=np.uint8).astype(float)
    return (raw - prep.COLOR_CURVE_ZERO) / prep.COLOR_CURVE_SCALE


def max_phase_gap(phase: np.ndarray) -> float:
    if phase.size < 2:
        return 1.0
    ordered = np.sort(np.mod(phase, 1.0))
    gaps = np.diff(np.concatenate([ordered, [ordered[0] + 1.0]]))
    return float(np.max(gaps))


def phot_phase(photometry: np.ndarray, period: float, t0: float) -> np.ndarray:
    return np.mod((photometry[:, 0] - t0) / period, 1.0)


def p95p05(values: np.ndarray) -> float:
    return float(np.percentile(values, 95) - np.percentile(values, 5))


def amplitude(values: np.ndarray) -> float:
    return float(np.max(values) - np.min(values))


def summarize_fit(row: list[object], photometry: dict[str, np.ndarray]) -> dict[str, object] | None:
    period = float(row[IDX["period"]])
    t0_value = row[IDX["t0"]]
    if t0_value is None:
        return None
    t0 = float(t0_value)
    dataset = DATASET_NAMES[int(row[IDX["dataset"]])]
    max_harmonics = 6 if dataset == "rrlyrae" else 5

    v_fit = prep.fit_band_curve(photometry["V"], period, t0, max_harmonics)
    i_fit = prep.fit_band_curve(photometry["I"], period, t0, max_harmonics)
    if v_fit is None or i_fit is None:
        return None

    phase = np.linspace(0, 1, 512, endpoint=False)
    v_model = prep.evaluate_curve(v_fit["coeffs"], phase)  # type: ignore[arg-type]
    i_model = prep.evaluate_curve(i_fit["coeffs"], phase)  # type: ignore[arg-type]
    color = v_model - i_model
    color_offset = color - np.mean(color)

    v_phase = phot_phase(photometry["V"], period, t0)
    i_phase = phot_phase(photometry["I"], period, t0)
    encoded_curve = row[IDX["color_curve"]]
    stored_offset = decode_color_curve(str(encoded_curve)) if encoded_curve else np.array([])

    return {
        "id": row[IDX["id"]],
        "dataset": dataset,
        "location": LOCATION_NAMES[int(row[IDX["location"]])],
        "mode": row[IDX["mode"]],
        "period": period,
        "catalogVI": float(row[IDX["v_minus_i"]]),
        "quality": int(row[IDX["quality"]]),
        "storedColorP95P05": p95p05(stored_offset) if stored_offset.size else None,
        "storedColorMinMax": amplitude(stored_offset) if stored_offset.size else None,
        "fitColorP95P05": p95p05(color_offset),
        "fitColorMinMax": amplitude(color_offset),
        "vObsP95P05": p95p05(photometry["V"][:, 1]),
        "iObsP95P05": p95p05(photometry["I"][:, 1]),
        "vModelP95P05": p95p05(v_model),
        "iModelP95P05": p95p05(i_model),
        "vModelMinMax": amplitude(v_model),
        "iModelMinMax": amplitude(i_model),
        "vRms": float(v_fit["rms"]),
        "iRms": float(i_fit["rms"]),
        "vN": int(v_fit["n"]),
        "iN": int(i_fit["n"]),
        "vTotalN": int(v_fit["nTotal"]),
        "iTotalN": int(i_fit["nTotal"]),
        "vHarmonics": int(v_fit["harmonics"]),
        "iHarmonics": int(i_fit["harmonics"]),
        "vPhaseBins": int(v_fit["phaseBins"]),
        "iPhaseBins": int(i_fit["phaseBins"]),
        "vMaxPhaseGap": max_phase_gap(v_phase),
        "iMaxPhaseGap": max_phase_gap(i_phase),
    }


def world_to_pixel(value: float, low: float, high: float, start: int, end: int, invert: bool = False) -> int:
    if high <= low:
        return (start + end) // 2
    t = (value - low) / (high - low)
    if invert:
        t = 1 - t
    return int(round(start + t * (end - start)))


def draw_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    points: tuple[np.ndarray, np.ndarray],
    line: tuple[np.ndarray, np.ndarray],
    y_label: str,
    color: tuple[int, int, int],
    invert_y: bool,
    font: ImageFont.ImageFont,
) -> None:
    x0, y0, x1, y1 = box
    pad_left, pad_top, pad_right, pad_bottom = 46, 24, 12, 30
    plot = (x0 + pad_left, y0 + pad_top, x1 - pad_right, y1 - pad_bottom)
    draw.rectangle(box, outline=(205, 205, 205), width=1)
    draw.text((x0 + 8, y0 + 5), title, fill=(20, 20, 20), font=font)
    draw.text((x0 + 8, y1 - 20), y_label, fill=(80, 80, 80), font=font)

    point_phase, point_value = points
    line_phase, line_value = line
    all_values = np.concatenate([point_value, line_value])
    low = float(np.percentile(all_values, 1))
    high = float(np.percentile(all_values, 99))
    padding = max(0.03, (high - low) * 0.12)
    low -= padding
    high += padding

    for frac in (0, 0.25, 0.5, 0.75, 1.0):
        x = world_to_pixel(frac * 2, 0, 2, plot[0], plot[2])
        draw.line((x, plot[1], x, plot[3]), fill=(235, 235, 235))
    for frac in (0, 0.5, 1.0):
        y = int(round(plot[1] + frac * (plot[3] - plot[1])))
        draw.line((plot[0], y, plot[2], y), fill=(235, 235, 235))

    draw.rectangle(plot, outline=(150, 150, 150), width=1)
    draw.text((plot[0], plot[3] + 8), "phase", fill=(80, 80, 80), font=font)

    px = [
        world_to_pixel(float(phase), 0, 2, plot[0], plot[2])
        for phase in line_phase
    ]
    py = [
        world_to_pixel(float(value), low, high, plot[1], plot[3], invert=invert_y)
        for value in line_value
    ]
    draw.line(list(zip(px, py)), fill=color, width=2)

    for phase, value in zip(np.concatenate([point_phase, point_phase + 1]), np.concatenate([point_value, point_value])):
        x = world_to_pixel(float(phase), 0, 2, plot[0], plot[2])
        y = world_to_pixel(float(value), low, high, plot[1], plot[3], invert=invert_y)
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(35, 35, 35))


def draw_fit_plot(row: list[object], photometry: dict[str, np.ndarray], summary: dict[str, object], path: Path) -> None:
    width, height = 1250, 760
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    period = float(row[IDX["period"]])
    t0 = float(row[IDX["t0"]])
    dataset = DATASET_NAMES[int(row[IDX["dataset"]])]
    max_harmonics = 6 if dataset == "rrlyrae" else 5
    v_fit = prep.fit_band_curve(photometry["V"], period, t0, max_harmonics)
    i_fit = prep.fit_band_curve(photometry["I"], period, t0, max_harmonics)
    if v_fit is None or i_fit is None:
        return

    phase = np.linspace(0, 2, 900, endpoint=True)
    phase_single = np.mod(phase, 1.0)
    v_model = prep.evaluate_curve(v_fit["coeffs"], phase_single)  # type: ignore[arg-type]
    i_model = prep.evaluate_curve(i_fit["coeffs"], phase_single)  # type: ignore[arg-type]
    color_offset = (v_model - i_model) - np.mean(v_model - i_model)

    title = (
        f"{row[IDX['id']]}  {summary['location']} {summary['dataset']} {summary['mode']}  "
        f"P={period:.5f} d  Q{summary['quality']}"
    )
    metrics = (
        f"V-I p95-p05={summary['fitColorP95P05']:.3f} mag, peak-to-peak={summary['fitColorMinMax']:.3f} mag | "
        f"V: n={summary['vN']}/{summary['vTotalN']} h={summary['vHarmonics']} rms={summary['vRms']:.3f} gap={summary['vMaxPhaseGap']:.2f} | "
        f"I: n={summary['iN']}/{summary['iTotalN']} h={summary['iHarmonics']} rms={summary['iRms']:.3f} gap={summary['iMaxPhaseGap']:.2f}"
    )
    draw.text((18, 12), title, fill=(10, 10, 10), font=font)
    draw.text((18, 32), metrics, fill=(60, 60, 60), font=font)

    top = 62
    panel_h = 215
    gap = 14
    panel_w = width - 36
    x0 = 18

    v_phase = phot_phase(photometry["V"], period, t0)
    i_phase = phot_phase(photometry["I"], period, t0)
    draw_panel(
        draw,
        (x0, top, x0 + panel_w, top + panel_h),
        "V band folded photometry and harmonic fit",
        (v_phase, photometry["V"][:, 1]),
        (phase, v_model),
        "mag",
        (44, 102, 204),
        True,
        font,
    )
    draw_panel(
        draw,
        (x0, top + panel_h + gap, x0 + panel_w, top + panel_h * 2 + gap),
        "I band folded photometry and harmonic fit",
        (i_phase, photometry["I"][:, 1]),
        (phase, i_model),
        "mag",
        (204, 99, 44),
        True,
        font,
    )

    empty_points = (np.array([], dtype=float), np.array([], dtype=float))
    draw_panel(
        draw,
        (x0, top + panel_h * 2 + gap * 2, x0 + panel_w, top + panel_h * 3 + gap * 2),
        "Derived V-I offset from independent V and I fits",
        empty_points,
        (phase, color_offset),
        "mag",
        (175, 64, 145),
        False,
        font,
    )
    image.save(path)


def make_montage(paths: list[Path], out_path: Path) -> None:
    if not paths:
        return
    thumbs: list[Image.Image] = []
    for path in paths:
        image = Image.open(path)
        image.thumbnail((610, 370))
        canvas = Image.new("RGB", (620, 380), (255, 255, 255))
        canvas.paste(image, ((620 - image.width) // 2, (380 - image.height) // 2))
        thumbs.append(canvas)

    cols = 2
    rows = math.ceil(len(thumbs) / cols)
    montage = Image.new("RGB", (cols * 620, rows * 380), (245, 245, 245))
    for idx, thumb in enumerate(thumbs):
        montage.paste(thumb, ((idx % cols) * 620, (idx // cols) * 380))
    montage.save(out_path)


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    catalog = payload["datasets"]["catalog"]
    by_id = {row[IDX["id"]]: row for row in catalog}

    fitted: list[dict[str, object]] = []
    for row in catalog:
        if not row[IDX["color_curve"]] or int(row[IDX["quality"]] or 0) <= 0:
            continue
        curve = decode_color_curve(str(row[IDX["color_curve"]]))
        fitted.append(
            {
                "id": row[IDX["id"]],
                "dataset": DATASET_NAMES[int(row[IDX["dataset"]])],
                "location": LOCATION_NAMES.get(int(row[IDX["location"]]), "Other"),
                "quality": int(row[IDX["quality"]]),
                "p95p05": p95p05(curve),
                "minmax": amplitude(curve),
            }
        )

    top_by_p95 = sorted(fitted, key=lambda item: float(item["p95p05"]), reverse=True)[:18]
    top_by_minmax = sorted(fitted, key=lambda item: float(item["minmax"]), reverse=True)[:18]
    top_cepheids_p95 = [
        item
        for item in sorted(fitted, key=lambda item: float(item["p95p05"]), reverse=True)
        if item["dataset"] == "cepheids"
    ][:10]
    top_cepheids_minmax = [
        item
        for item in sorted(fitted, key=lambda item: float(item["minmax"]), reverse=True)
        if item["dataset"] == "cepheids"
    ][:10]
    target_ids = []
    for item in top_by_p95 + top_by_minmax + top_cepheids_p95 + top_cepheids_minmax:
        obj_id = str(item["id"])
        if obj_id not in target_ids:
            target_ids.append(obj_id)

    grouped: dict[tuple[str, str], set[str]] = {}
    for obj_id in target_ids:
        row = by_id[obj_id]
        group = (LOCATION_NAMES[int(row[IDX["location"]])], DATASET_NAMES[int(row[IDX["dataset"]])])
        grouped.setdefault(group, set()).add(obj_id)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    photometry_by_id: dict[str, dict[str, np.ndarray]] = {}
    for group, wanted in grouped.items():
        archive = prep.PHOTOMETRY_ARCHIVES[group]
        photometry_by_id.update(prep.read_photometry_archive(archive["path"], wanted))  # type: ignore[arg-type]

    summaries: list[dict[str, object]] = []
    plot_paths: list[Path] = []
    plot_by_id: dict[str, Path] = {}
    for obj_id in target_ids:
        row = by_id[obj_id]
        photometry = photometry_by_id.get(obj_id)
        if not photometry or "V" not in photometry or "I" not in photometry:
            continue
        summary = summarize_fit(row, photometry)
        if summary is None:
            continue
        summaries.append(summary)
        plot_path = OUT_DIR / f"{obj_id}.png"
        draw_fit_plot(row, photometry, summary, plot_path)
        plot_paths.append(plot_path)
        plot_by_id[obj_id] = plot_path

    summary_path = OUT_DIR / "high_span_audit.json"
    summary_path.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    make_montage(plot_paths[:16], OUT_DIR / "high_span_montage.png")
    make_montage(
        [plot_by_id[str(item["id"])] for item in top_by_p95[:16] if str(item["id"]) in plot_by_id],
        OUT_DIR / "high_p95_montage.png",
    )
    make_montage(
        [plot_by_id[str(item["id"])] for item in top_by_minmax[:16] if str(item["id"]) in plot_by_id],
        OUT_DIR / "high_peak_to_peak_montage.png",
    )
    make_montage(
        [plot_by_id[str(item["id"])] for item in top_cepheids_p95[:8] if str(item["id"]) in plot_by_id],
        OUT_DIR / "high_cepheid_montage.png",
    )

    print(json.dumps(summaries[:20], indent=2))
    print(f"Wrote {summary_path}")
    print(f"Wrote {OUT_DIR / 'high_span_montage.png'}")


if __name__ == "__main__":
    main()
