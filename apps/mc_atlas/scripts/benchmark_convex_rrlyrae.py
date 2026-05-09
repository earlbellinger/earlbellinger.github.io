"""Benchmark the convex template dictionary on RRab lightcurves."""

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


OUT_CACHE = prep.PROCESSED / "convex_rrlyrae_curves_v1.json"
OUT_CSV = prep.ROOT / "diagnostics" / "convex_rrlyrae_batch_diagnostics.csv"
OUT_SUMMARY = prep.ROOT / "diagnostics" / "convex_rrlyrae_batch_summary.json"


def load_rr_feature_group(stars_by_id: dict[str, prep.CatalogStar]) -> dict[str, dict[str, np.ndarray]]:
    with np.load(convex.FEATURE_CACHE, allow_pickle=False) as payload:
        ids = payload["ids"].astype(str)
        shapes = payload["shapes"].astype(float)

    rows: list[tuple[str, float, np.ndarray]] = []
    for index, obj_id in enumerate(ids):
        star = stars_by_id.get(str(obj_id))
        if star is None or star.dataset != "rrlyrae" or star.light_curve is None:
            continue
        if prep.template_family(star) != "RRab":
            continue
        period = float(star.light_curve.get("period", star.period))
        rows.append((str(obj_id), math.log10(period), shapes[index]))
    rows.sort(key=lambda item: item[1])
    return {
        "RRab": {
            "ids": np.asarray([item[0] for item in rows]),
            "logp": np.asarray([item[1] for item in rows], dtype=float),
            "shapes": np.asarray([item[2] for item in rows], dtype=float),
        }
    }


def build_rr_jobs(limit: int | None = None) -> tuple[list[dict[str, Any]], dict[str, dict[str, np.ndarray]]]:
    rr = prep.parse_rr_lyrae(prep.RAW / "ogle_rrlyrae_table2.dat")
    params = prep.load_light_curve_parameters()
    for star in rr:
        star.light_curve = params.get(star.obj_id)
    stars_by_id = {star.obj_id: star for star in rr}
    features = load_rr_feature_group(stars_by_id)
    current_curves = convex.load_current_curves()

    grouped: dict[tuple[str, str], list[prep.CatalogStar]] = {}
    for star in rr:
        if star.light_curve is None or prep.template_family(star) != "RRab":
            continue
        group = prep.photometry_archive_group(star)
        if group is not None:
            grouped.setdefault(group, []).append(star)

    jobs: list[dict[str, Any]] = []
    for group, stars in grouped.items():
        wanted = {star.obj_id for star in stars}
        archive = prep.PHOTOMETRY_ARCHIVES[group]
        photometry = prep.read_photometry_archive(Path(archive["path"]), wanted)
        for star in stars:
            bands = photometry.get(star.obj_id, {})
            phot_i = bands.get("I")
            if phot_i is None or phot_i.shape[0] < 25:
                continue
            period = float(star.light_curve.get("period", star.period))
            t0 = float(star.light_curve["t0"])
            jobs.append(
                {
                    "star": {
                        "id": star.obj_id,
                        "location": star.location,
                        "family": "RRab",
                        "period": period,
                        "logp": math.log10(period),
                        "t0": t0,
                        "iMag": star.i_mag,
                        "vMag": star.v_mag,
                        "vMinusI": star.v_mag - star.i_mag,
                    },
                    "photI": phot_i,
                    "photV": bands.get("V"),
                    "current": current_curves.get(star.obj_id, {}),
                }
            )
            if limit is not None and len(jobs) >= limit:
                return jobs, features
    return jobs, features


def write_rr_outputs(curves: dict[str, dict[str, Any]], rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    OUT_CACHE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CACHE.write_text(
        json.dumps(
            {
                "version": convex.VERSION,
                "samples": convex.SAMPLES,
                "lightEncoding": "int16le",
                "lightScale": prep.LIGHT_CURVE_INT16_SCALE,
                "summary": summary,
                "curves": curves,
            },
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "location",
        "family",
        "period",
        "logP",
        "iN",
        "vN",
        "currentLightQuality",
        "currentColorQuality",
        "hasCurrentColor",
        "currentIMad",
        "dictIMad",
        "currentIRms",
        "dictIRms",
        "dictIKeptMad",
        "dictIKeptRms",
        "dictIRejected",
        "currentVMad",
        "dictVMad",
        "currentVRms",
        "dictVRms",
        "dictVKeptMad",
        "dictVKeptRms",
        "dictVRejected",
        "dictPhaseOffset",
        "dictActive",
        "dictEffective",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--workers", type=int, default=max(1, min(8, (prep.os.cpu_count() or 2) - 1)))
    args = parser.parse_args()

    start = time.perf_counter()
    jobs, features = build_rr_jobs(args.limit)
    failures: dict[str, int] = {}
    rows: list[dict[str, Any]] = []
    curves: dict[str, dict[str, Any]] = {}

    if args.workers <= 1:
        convex.init_worker(features)
        iterator = enumerate((convex.fit_job(job) for job in jobs), 1)
        for index, result in iterator:
            status = str(result.get("status", "unknown"))
            if status == "ok":
                rows.append(result["row"])
                curves[str(result["id"])] = result["curve"]
            else:
                failures[status] = failures.get(status, 0) + 1
            if index % 250 == 0:
                print(f"Processed {index}/{len(jobs)}")
    else:
        with ProcessPoolExecutor(max_workers=args.workers, initializer=convex.init_worker, initargs=(features,)) as executor:
            futures = [executor.submit(convex.fit_job, job) for job in jobs]
            for index, future in enumerate(as_completed(futures), 1):
                result = future.result()
                status = str(result.get("status", "unknown"))
                if status == "ok":
                    rows.append(result["row"])
                    curves[str(result["id"])] = result["curve"]
                else:
                    failures[status] = failures.get(status, 0) + 1
                if index % 250 == 0:
                    print(f"Processed {index}/{len(jobs)}")

    elapsed = time.perf_counter() - start
    summary = convex.build_summary(rows, failures, len(jobs), elapsed)
    summary["target"] = "RRab"
    write_rr_outputs(curves, rows, summary)
    print(json.dumps(summary, indent=2))
    print(f"Wrote {OUT_CACHE}")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
