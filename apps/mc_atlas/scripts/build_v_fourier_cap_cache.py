"""Build compact V-band Fourier curve caches with a fixed harmonic cap."""

from __future__ import annotations

import argparse
import base64
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
import benchmark_v_fourier_orders as vbench  # noqa: E402
import prepare_data as prep  # noqa: E402


VERSION = 1
SAMPLES = prep.COLOR_CURVE_SAMPLES
SCALE = prep.LIGHT_CURVE_INT16_SCALE
OUT_TEMPLATE = prep.PROCESSED / "v_fourier_cap{cap}_curves_v1.json"


def encode_offsets(offsets: np.ndarray) -> str:
    lower = np.iinfo(np.int16).min / SCALE
    upper = np.iinfo(np.int16).max / SCALE
    quantized = np.rint(np.clip(offsets, lower, upper) * SCALE).astype("<i2")
    return base64.b64encode(quantized.tobytes()).decode("ascii")


def robust_stats(residual: np.ndarray) -> tuple[float, float, float]:
    residual = residual[np.isfinite(residual)]
    if residual.size == 0:
        return math.nan, math.nan, math.nan
    center = float(np.median(residual))
    mad = float(1.4826 * np.median(np.abs(residual - center)))
    rms = float(np.sqrt(np.mean(residual * residual)))
    return center, mad, rms


def round_number(value: float, digits: int = 6) -> float | None:
    if not math.isfinite(value):
        return None
    return round(float(value), digits)


def build_curve_for_job(args: tuple[dict[str, Any], int]) -> dict[str, Any]:
    job, cap = args
    fit = prep.fit_band_curve(
        job["photV"],
        float(job["period"]),
        float(job["t0"]),
        cap,
        smoothness=0.08 if str(job["dataset"]) != "rrlyrae" else 0.12,
        rms_tolerance=0.007 if str(job["dataset"]) != "rrlyrae" else 0.012,
        rms_relative_tolerance=0.12 if str(job["dataset"]) != "rrlyrae" else 0.18,
        carrier=True,
        mask_eclipses=True,
    )
    if fit is None:
        return {"id": job["id"], "status": "fit_failed"}

    phase = np.mod((job["photV"][:, 0] - float(job["t0"])) / float(job["period"]), 1.0)
    model_at_obs = prep.evaluate_curve(fit["coeffs"], phase)  # type: ignore[arg-type]
    residual = job["photV"][:, 1] - model_at_obs
    _, mad, rms = robust_stats(residual)
    dense_phase = np.linspace(0.0, 1.0, SAMPLES, endpoint=False)
    dense = prep.evaluate_curve(fit["coeffs"], dense_phase)  # type: ignore[arg-type]
    mean = float(np.mean(dense))
    return {
        "id": job["id"],
        "status": "ok",
        "curve": {
            "vMean": round_number(mean, 6),
            "vCurve": encode_offsets(dense - mean),
            "vAmplitude": round_number(float(prep.peak_to_peak(dense)), 6),
            "vRms": round_number(rms, 6),
            "vMad": round_number(mad, 6),
            "vN": int(job["photV"].shape[0]),
            "vH": int(fit["harmonics"]),
            "vFitSamples": int(fit.get("fitSamples", 0)),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=3)
    parser.add_argument("--dataset", choices=["cepheids", "rrlyrae", "anomalousCepheids", "all"], default="all")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--workers", type=int, default=max(1, min(8, (prep.os.cpu_count() or 2) - 1)))
    args = parser.parse_args()

    start = time.perf_counter()
    datasets = ["cepheids", "anomalousCepheids", "rrlyrae"] if args.dataset == "all" else [args.dataset]
    jobs: list[dict[str, Any]] = []
    for dataset in datasets:
        remaining = None if args.limit is None else max(0, args.limit - len(jobs))
        if remaining == 0:
            break
        jobs.extend(vbench.build_jobs(dataset, remaining))

    curves: dict[str, dict[str, Any]] = {}
    failures: dict[str, int] = {}
    if args.workers <= 1:
        for index, job in enumerate(jobs, 1):
            result = build_curve_for_job((job, args.cap))
            status = str(result.get("status", "unknown"))
            if status == "ok":
                curves[str(result["id"])] = result["curve"]
            else:
                failures[status] = failures.get(status, 0) + 1
            if index % 500 == 0:
                print(f"Processed {index}/{len(jobs)}")
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(build_curve_for_job, (job, args.cap)) for job in jobs]
            for index, future in enumerate(as_completed(futures), 1):
                result = future.result()
                status = str(result.get("status", "unknown"))
                if status == "ok":
                    curves[str(result["id"])] = result["curve"]
                else:
                    failures[status] = failures.get(status, 0) + 1
                if index % 500 == 0:
                    print(f"Processed {index}/{len(jobs)}")

    elapsed = time.perf_counter() - start
    summary = {
        "version": VERSION,
        "cap": args.cap,
        "datasets": datasets,
        "jobs": len(jobs),
        "fitCount": len(curves),
        "failures": failures,
        "elapsedSeconds": round_number(elapsed, 3),
    }
    out = Path(str(OUT_TEMPLATE).format(cap=args.cap))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "version": VERSION,
                "samples": SAMPLES,
                "cap": args.cap,
                "vEncoding": "int16le",
                "vScale": SCALE,
                "summary": summary,
                "curves": curves,
            },
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
