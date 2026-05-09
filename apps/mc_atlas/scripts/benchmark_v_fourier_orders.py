"""Benchmark V-band harmonic caps against current V/color fits."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import apply_convex_templates as convex  # noqa: E402
import prepare_data as prep  # noqa: E402


OUT_PREFIX = prep.ROOT / "diagnostics" / "v_fourier_order_benchmark"


def robust_stats(residual: np.ndarray) -> tuple[float, float, float]:
    residual = residual[np.isfinite(residual)]
    if residual.size == 0:
        return math.nan, math.nan, math.nan
    center = float(np.median(residual))
    mad = float(1.4826 * np.median(np.abs(residual - center)))
    rms = float(np.sqrt(np.mean(residual * residual)))
    return center, mad, rms


def star_family(star: prep.CatalogStar) -> str:
    return prep.template_family(star)


def load_stars(dataset: str) -> list[prep.CatalogStar]:
    if dataset == "cepheids":
        stars = prep.parse_cepheids(prep.RAW / "ogle_cepheids_table3.dat")
    elif dataset == "rrlyrae":
        stars = prep.parse_rr_lyrae(prep.RAW / "ogle_rrlyrae_table2.dat")
    elif dataset == "anomalousCepheids":
        stars = prep.parse_anomalous_cepheids()
    elif dataset == "all":
        stars = (
            prep.parse_cepheids(prep.RAW / "ogle_cepheids_table3.dat")
            + prep.parse_rr_lyrae(prep.RAW / "ogle_rrlyrae_table2.dat")
            + prep.parse_anomalous_cepheids()
        )
    else:
        raise ValueError(dataset)
    params = prep.load_light_curve_parameters()
    for star in stars:
        star.light_curve = params.get(star.obj_id)
    return [star for star in stars if star.light_curve is not None]


def build_jobs(dataset: str, limit: int | None = None) -> list[dict[str, Any]]:
    stars = load_stars(dataset)
    current_curves = convex.load_current_curves()
    grouped: dict[tuple[str, str], list[prep.CatalogStar]] = {}
    for star in stars:
        group = prep.photometry_archive_group(star)
        if group is not None:
            grouped.setdefault(group, []).append(star)

    jobs: list[dict[str, Any]] = []
    for group, group_stars in grouped.items():
        wanted = {star.obj_id for star in group_stars}
        photometry = prep.read_photometry_archive(Path(prep.PHOTOMETRY_ARCHIVES[group]["path"]), wanted)
        for star in group_stars:
            bands = photometry.get(star.obj_id, {})
            phot_v = bands.get("V")
            if phot_v is None or phot_v.shape[0] < 6:
                continue
            period = float(star.light_curve.get("period", star.period))
            t0 = float(star.light_curve["t0"])
            jobs.append(
                {
                    "id": star.obj_id,
                    "dataset": star.dataset,
                    "location": star.location,
                    "family": star_family(star),
                    "period": period,
                    "t0": t0,
                    "iMag": star.i_mag,
                    "vMinusI": star.v_mag - star.i_mag,
                    "photV": phot_v,
                    "current": current_curves.get(star.obj_id, {}),
                }
            )
            if limit is not None and len(jobs) >= limit:
                return jobs
    return jobs


def fit_v_cap(job: dict[str, Any], cap: int) -> dict[str, Any]:
    dataset = str(job["dataset"])
    fit = prep.fit_band_curve(
        job["photV"],
        float(job["period"]),
        float(job["t0"]),
        cap,
        smoothness=0.08 if dataset != "rrlyrae" else 0.12,
        rms_tolerance=0.007 if dataset != "rrlyrae" else 0.012,
        rms_relative_tolerance=0.12 if dataset != "rrlyrae" else 0.18,
        carrier=True,
        mask_eclipses=True,
    )
    if fit is None:
        return {"cap": cap, "mad": math.nan, "rms": math.nan, "harmonics": 0, "fitSamples": 0}
    phase = np.mod((job["photV"][:, 0] - float(job["t0"])) / float(job["period"]), 1.0)
    model = prep.evaluate_curve(fit["coeffs"], phase)  # type: ignore[arg-type]
    residual = job["photV"][:, 1] - model
    _, mad, rms = robust_stats(residual)
    return {
        "cap": cap,
        "mad": mad,
        "rms": rms,
        "harmonics": int(fit["harmonics"]),
        "fitSamples": int(fit.get("fitSamples", 0)),
    }


def benchmark_job(args: tuple[dict[str, Any], list[int]]) -> dict[str, Any]:
    job, caps = args
    phot_v = job["photV"]
    phase = np.mod((phot_v[:, 0] - float(job["t0"])) / float(job["period"]), 1.0)
    current = job.get("current", {})
    current_model = convex.current_model_v(current, float(job["iMag"]), float(job["vMinusI"]), phase)
    current_residual = phot_v[:, 1] - current_model if current_model is not None else np.full(phot_v.shape[0], np.nan)
    _, current_mad, current_rms = robust_stats(current_residual)

    result: dict[str, Any] = {
        "id": job["id"],
        "dataset": job["dataset"],
        "location": job["location"],
        "family": job["family"],
        "period": job["period"],
        "logP": math.log10(float(job["period"])),
        "vN": int(phot_v.shape[0]),
        "hasCurrentColor": bool(isinstance(current, dict) and "curve" in current),
        "currentColorQuality": int(current.get("quality", 0)) if isinstance(current, dict) else 0,
        "currentVMad": current_mad,
        "currentVRms": current_rms,
    }
    for cap in caps:
        cap_result = fit_v_cap(job, cap)
        result[f"cap{cap}Mad"] = cap_result["mad"]
        result[f"cap{cap}Rms"] = cap_result["rms"]
        result[f"cap{cap}H"] = cap_result["harmonics"]
    finite_caps = [
        cap
        for cap in caps
        if math.isfinite(float(result.get(f"cap{cap}Rms", math.nan)))
    ]
    if finite_caps:
        best_rms_cap = min(finite_caps, key=lambda cap: float(result[f"cap{cap}Rms"]))
        best_mad_cap = min(finite_caps, key=lambda cap: float(result[f"cap{cap}Mad"]))
        result["bestRmsCap"] = best_rms_cap
        result["bestRms"] = result[f"cap{best_rms_cap}Rms"]
        result["bestMadCap"] = best_mad_cap
        result["bestMad"] = result[f"cap{best_mad_cap}Mad"]
    return result


def finite_pairs(rows: list[dict[str, Any]], old: str, new: str) -> tuple[np.ndarray, np.ndarray]:
    old_values: list[float] = []
    new_values: list[float] = []
    for row in rows:
        try:
            a = float(row[old])
            b = float(row[new])
        except (KeyError, TypeError, ValueError):
            continue
        if math.isfinite(a) and math.isfinite(b) and a > 0:
            old_values.append(a)
            new_values.append(b)
    return np.asarray(old_values), np.asarray(new_values)


def comparison(rows: list[dict[str, Any]], old: str, new: str) -> dict[str, Any]:
    old_values, new_values = finite_pairs(rows, old, new)
    if old_values.size == 0:
        return {"count": 0}
    ratio = new_values / old_values
    return {
        "count": int(old_values.size),
        "oldMedian": round(float(np.median(old_values)), 5),
        "newMedian": round(float(np.median(new_values)), 5),
        "medianRatio": round(float(np.median(ratio)), 5),
        "improvedFraction": round(float(np.mean(new_values < old_values)), 4),
        "p10Ratio": round(float(np.percentile(ratio, 10)), 5),
        "p90Ratio": round(float(np.percentile(ratio, 90)), 5),
    }


def build_summary(rows: list[dict[str, Any]], dataset: str, caps: list[int], elapsed: float) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "dataset": dataset,
        "rows": len(rows),
        "caps": caps,
        "elapsedSeconds": round(float(elapsed), 3),
        "overall": {},
        "byFamily": {},
    }
    for cap in caps:
        summary["overall"][f"cap{cap}RmsVsCurrent"] = comparison(rows, "currentVRms", f"cap{cap}Rms")
        summary["overall"][f"cap{cap}MadVsCurrent"] = comparison(rows, "currentVMad", f"cap{cap}Mad")
    summary["overall"]["bestRmsVsCurrent"] = comparison(rows, "currentVRms", "bestRms")
    summary["overall"]["bestMadVsCurrent"] = comparison(rows, "currentVMad", "bestMad")
    for family in sorted({str(row["family"]) for row in rows}):
        family_rows = [row for row in rows if str(row["family"]) == family]
        item: dict[str, Any] = {"count": len(family_rows)}
        for cap in caps:
            item[f"cap{cap}RmsVsCurrent"] = comparison(family_rows, "currentVRms", f"cap{cap}Rms")
            item[f"cap{cap}MadVsCurrent"] = comparison(family_rows, "currentVMad", f"cap{cap}Mad")
            h_values = [int(row.get(f"cap{cap}H", 0)) for row in family_rows if row.get(f"cap{cap}H", 0)]
            if h_values:
                counts = {str(h): h_values.count(h) for h in sorted(set(h_values))}
                item[f"cap{cap}ChosenH"] = counts
        item["bestRmsVsCurrent"] = comparison(family_rows, "currentVRms", "bestRms")
        item["bestMadVsCurrent"] = comparison(family_rows, "currentVMad", "bestMad")
        best_caps = [int(row["bestRmsCap"]) for row in family_rows if "bestRmsCap" in row]
        item["bestRmsCapCounts"] = {str(cap): best_caps.count(cap) for cap in caps}
        summary["byFamily"][family] = item
    return summary


def write_outputs(rows: list[dict[str, Any]], summary: dict[str, Any], dataset: str, caps: list[int]) -> None:
    suffix = dataset
    csv_path = Path(f"{OUT_PREFIX}_{suffix}.csv")
    summary_path = Path(f"{OUT_PREFIX}_{suffix}.json")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "dataset",
        "location",
        "family",
        "period",
        "logP",
        "vN",
        "hasCurrentColor",
        "currentColorQuality",
        "currentVMad",
        "currentVRms",
    ]
    for cap in caps:
        fieldnames.extend([f"cap{cap}Mad", f"cap{cap}Rms", f"cap{cap}H"])
    fieldnames.extend(["bestRmsCap", "bestRms", "bestMadCap", "bestMad"])
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {summary_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["cepheids", "rrlyrae", "anomalousCepheids", "all"], default="cepheids")
    parser.add_argument(
        "--caps",
        default=None,
        help="Comma-separated harmonic caps. Defaults: Cepheid-like 1,2,3,4; rrlyrae/all 1,2,3,4,5",
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--workers", type=int, default=max(1, min(8, (prep.os.cpu_count() or 2) - 1)))
    args = parser.parse_args()

    caps = [int(value) for value in args.caps.split(",")] if args.caps else ([1, 2, 3, 4] if args.dataset in {"cepheids", "anomalousCepheids"} else [1, 2, 3, 4, 5])
    start = time.perf_counter()
    jobs = build_jobs(args.dataset, args.limit)
    rows: list[dict[str, Any]] = []
    if args.workers <= 1:
        for index, job in enumerate(jobs, 1):
            rows.append(benchmark_job((job, caps)))
            if index % 500 == 0:
                print(f"Processed {index}/{len(jobs)}")
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(benchmark_job, (job, caps)) for job in jobs]
            for index, future in enumerate(as_completed(futures), 1):
                rows.append(future.result())
                if index % 500 == 0:
                    print(f"Processed {index}/{len(jobs)}")
    elapsed = time.perf_counter() - start
    summary = build_summary(rows, args.dataset, caps, elapsed)
    write_outputs(rows, summary, args.dataset, caps)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
