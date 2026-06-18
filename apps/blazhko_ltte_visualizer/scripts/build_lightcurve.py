from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OGLE_RESULTS_DIR = ROOT.parent / "results" / "OGLE-BLG-RRLYR-07497_two_modulation"
BLAZHKO_SUMMARY_PATH = OGLE_RESULTS_DIR / "fit_summary.json"
BLAZHKO_AMPLITUDE_PATH = OGLE_RESULTS_DIR / "posterior_amplitude_phase_summary.csv"
BLAZHKO_BETA_DRAWS_PATH = OGLE_RESULTS_DIR / "posterior_beta_draws.npy"
LTTE_SUMMARY_PATH = DATA_DIR / "ltte_fit_summary.json"
OUTPUT_PATH = DATA_DIR / "theoretical_lightcurve.json"
JS_OUTPUT_PATH = DATA_DIR / "theoretical_lightcurve.js"


def load_amplitude_rows(path: Path) -> dict[str, dict[str, float | str]]:
    rows: dict[str, dict[str, float | str]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            converted: dict[str, float | str] = {}
            for key, value in row.items():
                if key in {"key", "family"}:
                    converted[key] = value
                else:
                    converted[key] = float(value)
            rows[str(row["key"])] = converted
    return rows


def component_for_term(family: str, order: int) -> tuple[int, int, int]:
    if family == "harmonic":
        return order, 0, 0
    if family == "modulation":
        return 0, order, 0
    if family == "modulation2":
        return 0, 0, order
    if family == "triplet_minus":
        return order, -1, 0
    if family == "triplet_plus":
        return order, 1, 0
    if family == "triplet2_minus":
        return order, 0, -1
    if family == "triplet2_plus":
        return order, 0, 1
    raise ValueError(f"Unknown Fourier term family: {family}")


def make_two_mod_entries(blazhko_summary: dict[str, object]) -> list[dict[str, object]]:
    refined = blazhko_summary["refined_model"]
    best = blazhko_summary["best_model_after_refined_neighborhood"]
    assert isinstance(refined, dict)
    assert isinstance(best, dict)

    f0 = float(refined["f0"])
    fm1 = float(refined["fm1"])
    fm2 = float(refined["fm2"])
    n = int(best["n"])
    r1 = int(best["r1"])
    q1 = int(best["q1"])
    s2 = int(best["s2"])
    q2 = int(best["q2"])

    entries: list[dict[str, object]] = []

    def append(key: str, family: str, order: int, frequency: float) -> None:
        k, p, q = component_for_term(family, order)
        entries.append(
            {
                "key": key,
                "family": family,
                "order": order,
                "frequency_d_c": frequency,
                "k": k,
                "p": p,
                "q": q,
            }
        )

    for order in range(1, n + 1):
        append(f"H{order}", "harmonic", order, order * f0)

    for order in range(1, r1 + 1):
        append(f"M{order}", "modulation", order, order * fm1)

    for order in range(1, q1 + 1):
        append(f"T{order}-", "triplet_minus", order, order * f0 - fm1)
        append(f"T{order}+", "triplet_plus", order, order * f0 + fm1)

    for order in range(1, s2 + 1):
        append(f"N{order}", "modulation2", order, order * fm2)

    for order in range(1, q2 + 1):
        append(f"U{order}-", "triplet2_minus", order, order * f0 - fm2)
        append(f"U{order}+", "triplet2_plus", order, order * f0 + fm2)

    return entries


def term_payload(entry: dict[str, object], beta: np.ndarray, index: int, phase_zero_days: float) -> dict[str, object]:
    sin_coeff = float(beta[1 + 2 * index])
    cos_coeff = float(beta[2 + 2 * index])
    frequency = float(entry["frequency_d_c"])
    return {
        **entry,
        "phase_constant_cycles": float((frequency * phase_zero_days) % 1.0),
        "sin_coeff_mag": sin_coeff,
        "cos_coeff_mag": cos_coeff,
        "amplitude_mag": math.hypot(sin_coeff, cos_coeff),
        "phase_rad": math.atan2(cos_coeff, sin_coeff),
    }


def ogle_unmodulated_lightcurve(
    blazhko_summary: dict[str, object], entries: list[dict[str, object]], beta: np.ndarray
) -> dict[str, object]:
    refined = blazhko_summary["refined_model"]
    metadata = blazhko_summary["metadata"]
    assert isinstance(refined, dict)
    assert isinstance(metadata, dict)

    period = float(refined["p0"])
    frequency = float(refined["f0"])
    phase_reference_days = float(refined["t_phase_zero"])

    phase = np.linspace(0.0, 1.0, 1200, endpoint=False)
    time = phase_reference_days + phase * period
    mag = np.full_like(phase, float(beta[0]), dtype=float)
    terms: list[dict[str, float | int | str]] = []

    for term_index, entry in enumerate(entries):
        if entry["family"] != "harmonic":
            continue

        order = int(entry["order"])
        sin_coeff = float(beta[1 + 2 * term_index])
        cos_coeff = float(beta[2 + 2 * term_index])
        angle = 2.0 * np.pi * order * frequency * time
        mag += sin_coeff * np.sin(angle) + cos_coeff * np.cos(angle)
        terms.append(
            {
                "key": f"H{order}",
                "order": order,
                "frequency_d_c": order * frequency,
                "sin_coeff_mag": sin_coeff,
                "cos_coeff_mag": cos_coeff,
                "amplitude_mag": math.hypot(sin_coeff, cos_coeff),
                "phase_rad": math.atan2(cos_coeff, sin_coeff),
            }
        )

    # Keep phase 0 at maximum brightness, matching the display convention.
    min_index = int(np.argmin(mag))
    phase_shift = float(phase[min_index])
    mag = np.roll(mag, -min_index)
    phase_zero_days = phase_reference_days + phase_shift * period

    return {
        "source": "OGLE-BLG-RRLYR-07497_two_modulation unmodulated harmonic fit",
        "source_label": "OGLE-07497 Fourier fit",
        "period_days": period,
        "phase_zero_days": phase_zero_days,
        "phase": [round(float(value), 7) for value in phase],
        "mag_i": [round(float(value), 7) for value in mag],
        "raw": {
            "phase": [round(float(value), 7) for value in phase[::4]],
            "mag_i": [round(float(value), 7) for value in mag[::4]],
        },
        "mean_mag_i": float(np.mean(mag)),
        "min_mag_i": float(np.min(mag)),
        "max_mag_i": float(np.max(mag)),
        "mean_catalog_i": float(metadata["mean_i_mag"]),
        "fourier_terms": terms,
    }


def fourier_model_payload(entries: list[dict[str, object]], beta: np.ndarray, phase_zero_days: float) -> dict[str, object]:
    return {
        "beta0_mag": float(beta[0]),
        "phase_zero_days": phase_zero_days,
        "terms": [term_payload(entry, beta, index, phase_zero_days) for index, entry in enumerate(entries)],
    }


def modulation_defaults(blazhko_summary: dict[str, object]) -> dict[str, object]:
    refined = blazhko_summary["refined_model"]
    assert isinstance(refined, dict)
    amplitude_rows = load_amplitude_rows(BLAZHKO_AMPLITUDE_PATH)

    h1_amp = float(amplitude_rows["H1"]["amplitude_q50"])

    def one(index: int) -> dict[str, float | int]:
        if index == 1:
            minus_key, plus_key, pure_key, period_key = "T1-", "T1+", "M1", "pb1"
        else:
            minus_key, plus_key, pure_key, period_key = "U1-", "U1+", "N1", "pb2"

        minus = float(amplitude_rows[minus_key]["amplitude_q50"])
        plus = float(amplitude_rows[plus_key]["amplitude_q50"])
        pure = amplitude_rows[pure_key]
        phase_q50_rad = float(pure["phase_q50_rad"])
        amp_depth = (minus + plus) / h1_amp
        phase_cycles = abs(plus - minus) / (2.0 * math.pi * h1_amp)
        return {
            "period_days": float(refined[period_key]),
            "amplitude_depth": amp_depth,
            "phase_shift_cycles": phase_cycles,
            "mean_shift_mag": float(pure["amplitude_q50"]),
            "phase_offset": (phase_q50_rad / (2.0 * math.pi)) % 1.0,
        }

    return {
        "star_id": str(blazhko_summary["metadata"]["star_id"]),
        "pulsation_period_days": float(refined["p0"]),
        "period1": one(1),
        "period2": one(2),
        "source": str(BLAZHKO_SUMMARY_PATH),
    }


def ltte_defaults(ltte_summary: dict[str, object]) -> dict[str, object]:
    fit = ltte_summary["fit"]
    assert isinstance(fit, dict)
    return {
        "star_id": str(ltte_summary["star_id"]),
        "pulsation_period_days": float(ltte_summary["reference_ephemeris"]["pulsation_period_d"]),
        "orbital_period_days": float(fit["porb_d"]),
        "t_peri_hjd_minus_2450000": float(fit["tperi_hjd_minus_2450000"]),
        "eccentricity": float(fit["e"]),
        "omega_deg": float(fit["omega_deg"]),
        "asini_au": float(fit["asini_au"]),
        "ltte_amp_days": float(fit["ltte_amp_d"]),
        "source": str(LTTE_SUMMARY_PATH),
    }


def main() -> None:
    blazhko_summary = json.loads(BLAZHKO_SUMMARY_PATH.read_text(encoding="utf-8"))
    ltte_summary = json.loads(LTTE_SUMMARY_PATH.read_text(encoding="utf-8"))
    entries = make_two_mod_entries(blazhko_summary)
    beta = np.median(np.load(BLAZHKO_BETA_DRAWS_PATH), axis=0)

    lightcurve = ogle_unmodulated_lightcurve(blazhko_summary, entries, beta)
    payload = {
        "source_model": str(BLAZHKO_SUMMARY_PATH),
        "source_coefficients": str(BLAZHKO_BETA_DRAWS_PATH),
        "source_label": "OGLE-BLG-RRLYR-07497 unmodulated Fourier fit",
        "lightcurve": lightcurve,
        "fourier_model": fourier_model_payload(entries, beta, float(lightcurve["phase_zero_days"])),
        "defaults": {
            "blazhko": modulation_defaults(blazhko_summary),
            "ltte": ltte_defaults(ltte_summary),
        },
    }
    json_payload = json.dumps(payload, indent=2)
    OUTPUT_PATH.write_text(json_payload, encoding="utf-8")
    JS_OUTPUT_PATH.write_text(f"window.RRLYRAE_LIGHTCURVE_DATA = {json_payload};\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT_PATH),
                "js_output": str(JS_OUTPUT_PATH),
                "period_days": lightcurve["period_days"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
