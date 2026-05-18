"""Compare simple 3-D structure models for atlas wireframe choices.

The production wireframes are compact triaxial summaries. This diagnostic checks
whether that summary is competitive against simpler symmetric ellipsoids and
multi-component alternatives, using the same pulsator rows and distance-error
covariances as the atlas-fit wires.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ATLAS = ROOT / "public" / "data" / "magellanic-clouds.json"
DEFAULT_OUT = ROOT / "diagnostics" / "wireframe_model_comparison.json"

POPULATIONS = (
    {"id": "cepheids", "label": "Cepheids", "dataset": 0},
    {"id": "rrlyrae", "label": "RR Lyrae", "dataset": 1},
    {"id": "miras", "label": "Miras", "dataset": 3},
)
CLOUDS = (
    {"id": "lmc", "label": "LMC", "location": 0},
    {"id": "smc", "label": "SMC", "location": 1},
)

JITTER = 1e-5
EIGEN_FLOOR = 0.01
MAX_EM_ITER = 80
EM_TOL = 1e-4


def round_number(value: float, digits: int = 4) -> float | None:
    value = float(value)
    return None if not math.isfinite(value) else round(value, digits)


def stable_unit(value: object) -> float:
    digest = hashlib.sha256(str(value).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "little") / 2**64


def galactic_vector(lon_deg: np.ndarray, lat_deg: np.ndarray, distance: np.ndarray) -> np.ndarray:
    lon = np.deg2rad(lon_deg)
    lat = np.deg2rad(lat_deg)
    cos_lat = np.cos(lat)
    return np.column_stack(
        [
            distance * cos_lat * np.cos(lon),
            distance * cos_lat * np.sin(lon),
            distance * np.sin(lat),
        ]
    )


def positive_semidefinite(covariance: np.ndarray, floor: float = EIGEN_FLOOR) -> np.ndarray:
    covariance = (covariance + covariance.T) * 0.5
    values, vectors = np.linalg.eigh(covariance)
    values = np.maximum(values, floor)
    return (vectors * values) @ vectors.T


def fit_single_gaussian(x: np.ndarray, measurement: np.ndarray) -> dict[str, np.ndarray]:
    mean = x.mean(axis=0)
    centered = x - mean
    covariance = centered.T @ centered / len(x) - measurement.mean(axis=0)
    return {
        "weights": np.array([1.0]),
        "means": mean[None, :],
        "covariances": positive_semidefinite(covariance)[None, :, :],
    }


def isotropic_from_full(full: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    sigma2 = max(EIGEN_FLOOR, float(np.trace(full["covariances"][0]) / 3.0))
    return {
        "weights": np.array([1.0]),
        "means": full["means"],
        "covariances": (np.eye(3) * sigma2)[None, :, :],
    }


def axisymmetric_candidates(full: dict[str, np.ndarray]) -> list[tuple[str, dict[str, np.ndarray]]]:
    covariance = full["covariances"][0]
    values, vectors = np.linalg.eigh((covariance + covariance.T) * 0.5)
    order = np.argsort(values)[::-1]
    values = np.maximum(values[order], EIGEN_FLOOR)
    vectors = vectors[:, order]
    prolate_values = np.array([values[0], (values[1] + values[2]) * 0.5, (values[1] + values[2]) * 0.5])
    oblate_values = np.array([(values[0] + values[1]) * 0.5, (values[0] + values[1]) * 0.5, values[2]])
    prolate = vectors @ np.diag(prolate_values) @ vectors.T
    oblate = vectors @ np.diag(oblate_values) @ vectors.T
    return [
        (
            "axisymmetric-prolate",
            {"weights": np.array([1.0]), "means": full["means"], "covariances": prolate[None, :, :]},
        ),
        (
            "axisymmetric-oblate",
            {"weights": np.array([1.0]), "means": full["means"], "covariances": oblate[None, :, :]},
        ),
    ]


def log_gaussian_eiv(
    x: np.ndarray,
    measurement: np.ndarray,
    mean: np.ndarray,
    covariance: np.ndarray,
) -> np.ndarray:
    total = covariance[None, :, :] + measurement
    total = (total + np.swapaxes(total, 1, 2)) * 0.5 + np.eye(3)[None, :, :] * JITTER
    sign, logdet = np.linalg.slogdet(total)
    if np.any(sign <= 0):
        total[sign <= 0] += np.eye(3) * 1e-3
        sign, logdet = np.linalg.slogdet(total)
    inverse = np.linalg.inv(total)
    delta = x - mean
    mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
    return -0.5 * (3 * np.log(2 * np.pi) + logdet + mahalanobis)


def log_mixture_eiv(
    x: np.ndarray,
    measurement: np.ndarray,
    params: dict[str, np.ndarray],
) -> np.ndarray:
    component_logs = []
    for weight, mean, covariance in zip(params["weights"], params["means"], params["covariances"]):
        component_logs.append(np.log(max(float(weight), 1e-12)) + log_gaussian_eiv(x, measurement, mean, covariance))
    stacked = np.vstack(component_logs).T
    max_log = np.max(stacked, axis=1)
    return max_log + np.log(np.exp(stacked - max_log[:, None]).sum(axis=1))


def fit_gaussian_mixture(
    x: np.ndarray,
    measurement: np.ndarray,
    component_count: int,
    seed: int,
) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = len(x)
    full = fit_single_gaussian(x, measurement)
    covariance = full["covariances"][0]
    values, vectors = np.linalg.eigh(covariance)
    major_axis = vectors[:, np.argmax(values)]
    projected = (x - full["means"][0]) @ major_axis
    cuts = np.quantile(projected, np.linspace(0, 1, component_count + 1)[1:-1])
    labels = np.digitize(projected, cuts)

    weights = []
    means = []
    covariances = []
    for component in range(component_count):
        mask = labels == component
        if mask.sum() < 12:
            mask = rng.random(n) < 1 / component_count
        sub = fit_single_gaussian(x[mask], measurement[mask])
        weights.append(max(float(mask.mean()), 1e-3))
        means.append(sub["means"][0])
        covariances.append(sub["covariances"][0])

    weights = np.asarray(weights)
    weights /= weights.sum()
    params = {
        "weights": weights,
        "means": np.asarray(means),
        "covariances": np.asarray(covariances),
    }
    previous_log_likelihood = -np.inf

    for _iteration in range(MAX_EM_ITER):
        component_logs = []
        for weight, mean, covariance in zip(params["weights"], params["means"], params["covariances"]):
            component_logs.append(
                np.log(max(float(weight), 1e-12)) + log_gaussian_eiv(x, measurement, mean, covariance)
            )
        stacked = np.vstack(component_logs).T
        max_log = np.max(stacked, axis=1)
        log_denominator = max_log + np.log(np.exp(stacked - max_log[:, None]).sum(axis=1))
        log_likelihood = float(log_denominator.sum())
        if log_likelihood - previous_log_likelihood < EM_TOL * max(1.0, abs(previous_log_likelihood)):
            break
        previous_log_likelihood = log_likelihood

        responsibilities = np.exp(stacked - log_denominator[:, None])
        component_weights = responsibilities.sum(axis=0)
        weights = np.maximum(component_weights / n, 1e-5)
        weights /= weights.sum()
        means = []
        covariances = []
        for component in range(component_count):
            if component_weights[component] < 12:
                means.append(x[rng.integers(0, n)])
                covariances.append(full["covariances"][0])
                continue
            resp = responsibilities[:, component]
            mean = (x * resp[:, None]).sum(axis=0) / component_weights[component]
            delta = x - mean
            scatter = np.einsum("n,ni,nj->ij", resp, delta, delta) / component_weights[component]
            mean_measurement = (measurement * resp[:, None, None]).sum(axis=0) / component_weights[component]
            means.append(mean)
            covariances.append(positive_semidefinite(scatter - mean_measurement))
        params = {
            "weights": weights,
            "means": np.asarray(means),
            "covariances": np.asarray(covariances),
        }
    return params


def score_density_model(
    name: str,
    full_params: dict[str, np.ndarray],
    train_params: dict[str, np.ndarray],
    x: np.ndarray,
    measurement: np.ndarray,
    test_mask: np.ndarray,
    parameter_count: int,
) -> dict[str, float | str | int | None]:
    log_likelihood = float(log_mixture_eiv(x, measurement, full_params).sum())
    test_log_likelihood = float(log_mixture_eiv(x[test_mask], measurement[test_mask], train_params).sum())
    n = len(x)
    test_n = int(test_mask.sum())
    return {
        "model": name,
        "parameters": parameter_count,
        "logLikelihood": round_number(log_likelihood, 3),
        "testLogLikelihood": round_number(test_log_likelihood, 3),
        "testLogLikelihoodPerStar": round_number(test_log_likelihood / max(test_n, 1), 5),
        "aic": round_number(2 * parameter_count - 2 * log_likelihood, 2),
        "bic": round_number(parameter_count * math.log(n) - 2 * log_likelihood, 2),
    }


def fit_density_models(
    x: np.ndarray,
    measurement: np.ndarray,
    ids: list[object],
    seed: int,
) -> list[dict[str, float | str | int | None]]:
    train_mask = np.asarray([stable_unit(obj_id) < 0.8 for obj_id in ids])
    test_mask = ~train_mask
    x_train = x[train_mask]
    measurement_train = measurement[train_mask]

    full_gaussian = fit_single_gaussian(x, measurement)
    train_gaussian = fit_single_gaussian(x_train, measurement_train)
    model_specs: list[tuple[str, dict[str, np.ndarray], dict[str, np.ndarray], int]] = [
        ("isotropic-gaussian", isotropic_from_full(full_gaussian), isotropic_from_full(train_gaussian), 4),
        ("triaxial-gaussian", full_gaussian, train_gaussian, 9),
    ]
    full_axis = dict(axisymmetric_candidates(full_gaussian))
    train_axis = dict(axisymmetric_candidates(train_gaussian))
    for name in ("axisymmetric-prolate", "axisymmetric-oblate"):
        model_specs.append((name, full_axis[name], train_axis[name], 7))
    for component_count in (2, 3):
        if len(x_train) >= component_count * 80:
            model_specs.append(
                (
                    f"{component_count}-component-gaussian-mixture",
                    fit_gaussian_mixture(x, measurement, component_count, seed + component_count * 101),
                    fit_gaussian_mixture(x_train, measurement_train, component_count, seed + component_count * 101 + 17),
                    component_count * 9 + component_count - 1,
                )
            )

    scores = [
        score_density_model(name, full_params, train_params, x, measurement, test_mask, parameter_count)
        for name, full_params, train_params, parameter_count in model_specs
    ]
    add_deltas(scores)
    return sorted(scores, key=lambda item: float(item["bic"]))


def design_matrix(xy: np.ndarray, model: str) -> np.ndarray:
    x = xy[:, 0]
    y = xy[:, 1]
    if model == "constant-depth":
        return np.ones((len(xy), 1))
    if model == "tilted-plane":
        return np.column_stack([np.ones(len(xy)), x, y])
    if model == "quadratic-warp":
        x_scale = np.std(x) or 1.0
        y_scale = np.std(y) or 1.0
        xn = x / x_scale
        yn = y / y_scale
        return np.column_stack([np.ones(len(xy)), x, y, xn * xn, xn * yn, yn * yn])
    raise ValueError(model)


def fit_surface_params(
    xyz_local: np.ndarray,
    sigma_z: np.ndarray,
    model: str,
) -> tuple[np.ndarray, float]:
    xy = xyz_local[:, :2]
    z = xyz_local[:, 2]
    design = design_matrix(xy, model)
    scatter2 = max(0.01, float(np.var(z) - np.median(sigma_z) ** 2))
    coefficients = np.zeros(design.shape[1])
    for _iteration in range(30):
        variance = np.maximum(sigma_z**2 + scatter2, 1e-6)
        weights = 1 / variance
        weighted_design = design * np.sqrt(weights)[:, None]
        weighted_z = z * np.sqrt(weights)
        coefficients = np.linalg.lstsq(weighted_design, weighted_z, rcond=None)[0]
        residual = z - design @ coefficients
        next_scatter2 = max(0.01, float(np.average(residual**2, weights=weights) - np.average(sigma_z**2, weights=weights)))
        if abs(next_scatter2 - scatter2) < 1e-5:
            scatter2 = next_scatter2
            break
        scatter2 = 0.6 * scatter2 + 0.4 * next_scatter2
    return coefficients, scatter2


def surface_log_likelihood(
    xyz_local: np.ndarray,
    sigma_z: np.ndarray,
    model: str,
    coefficients: np.ndarray,
    scatter2: float,
) -> tuple[float, float]:
    design = design_matrix(xyz_local[:, :2], model)
    residual = xyz_local[:, 2] - design @ coefficients
    variance = np.maximum(sigma_z**2 + scatter2, 1e-6)
    log_likelihood = float((-0.5 * (np.log(2 * np.pi * variance) + residual**2 / variance)).sum())
    rms = math.sqrt(float(np.mean(residual**2)))
    return log_likelihood, rms


def score_surface_model(
    xyz_local: np.ndarray,
    sigma_z: np.ndarray,
    ids: list[object],
    model: str,
) -> dict[str, float | str | int | None]:
    train_mask = np.asarray([stable_unit(obj_id) < 0.8 for obj_id in ids])
    test_mask = ~train_mask
    full_coefficients, full_scatter2 = fit_surface_params(xyz_local, sigma_z, model)
    train_coefficients, train_scatter2 = fit_surface_params(xyz_local[train_mask], sigma_z[train_mask], model)
    log_likelihood, rms = surface_log_likelihood(xyz_local, sigma_z, model, full_coefficients, full_scatter2)
    test_log_likelihood, _test_rms = surface_log_likelihood(
        xyz_local[test_mask],
        sigma_z[test_mask],
        model,
        train_coefficients,
        train_scatter2,
    )
    parameter_count = design_matrix(xyz_local[:, :2], model).shape[1] + 1
    n = len(xyz_local)
    test_n = int(test_mask.sum())
    return {
        "model": model,
        "parameters": parameter_count,
        "intrinsicScatterKpc": round_number(math.sqrt(full_scatter2), 4),
        "rmsResidualKpc": round_number(rms, 4),
        "testLogLikelihood": round_number(test_log_likelihood, 3),
        "testLogLikelihoodPerStar": round_number(test_log_likelihood / max(test_n, 1), 5),
        "aic": round_number(2 * parameter_count - 2 * log_likelihood, 2),
        "bic": round_number(parameter_count * math.log(n) - 2 * log_likelihood, 2),
    }


def fit_surface_models(
    xyz_local: np.ndarray,
    sigma_z: np.ndarray,
    ids: list[object],
) -> list[dict[str, float | str | int | None]]:
    scores = [
        score_surface_model(xyz_local, sigma_z, ids, "constant-depth"),
        score_surface_model(xyz_local, sigma_z, ids, "tilted-plane"),
        score_surface_model(xyz_local, sigma_z, ids, "quadratic-warp"),
    ]
    add_deltas(scores)
    return sorted(scores, key=lambda item: float(item["bic"]))


def add_deltas(scores: list[dict[str, float | str | int | None]]) -> None:
    for criterion in ("bic", "aic"):
        best = min(float(score[criterion]) for score in scores if score[criterion] is not None)
        for score in scores:
            score[f"delta{criterion.upper()}"] = round_number(float(score[criterion]) - best, 2)
    best_test = max(float(score["testLogLikelihoodPerStar"]) for score in scores if score["testLogLikelihoodPerStar"] is not None)
    for score in scores:
        score["deltaTestLogLikelihoodPerStar"] = round_number(
            best_test - float(score["testLogLikelihoodPerStar"]),
            5,
        )


def finite_row(row: list[object], indexes: dict[str, int]) -> bool:
    required = ("distanceKpc", "galLonDeg", "galLatDeg", "distanceErrorKpc", "x", "y", "z")
    values = [row[indexes[name]] for name in required]
    return all(isinstance(value, (int, float)) and math.isfinite(value) for value in values) and row[indexes["distanceKpc"]] > 0 and row[indexes["distanceErrorKpc"]] > 0


def compare_models(atlas_path: Path) -> dict[str, object]:
    payload = json.loads(atlas_path.read_text(encoding="utf-8"))
    fields = payload["fields"]["catalog"]
    indexes = {name: index for index, name in enumerate(fields)}
    rows = payload["datasets"]["catalog"]
    results = []

    for population_index, population in enumerate(POPULATIONS):
        for cloud_index, cloud in enumerate(CLOUDS):
            subset = [
                row
                for row in rows
                if row[indexes["datasetIndex"]] == population["dataset"]
                and row[indexes["locationIndex"]] == cloud["location"]
                and finite_row(row, indexes)
            ]
            if len(subset) < 80:
                continue

            distance = np.asarray([row[indexes["distanceKpc"]] for row in subset], dtype=float)
            lon = np.asarray([row[indexes["galLonDeg"]] for row in subset], dtype=float)
            lat = np.asarray([row[indexes["galLatDeg"]] for row in subset], dtype=float)
            sigma = np.asarray([row[indexes["distanceErrorKpc"]] for row in subset], dtype=float)
            ids = [row[indexes["id"]] for row in subset]

            position = galactic_vector(lon, lat, distance)
            unit = position / np.linalg.norm(position, axis=1)[:, None]
            measurement = sigma[:, None, None] ** 2 * unit[:, :, None] * unit[:, None, :]
            local = np.asarray(
                [[row[indexes["x"]], row[indexes["y"]], row[indexes["z"]]] for row in subset],
                dtype=float,
            )
            local -= local.mean(axis=0)

            results.append(
                {
                    "populationId": population["id"],
                    "cloudId": cloud["id"],
                    "count": len(subset),
                    "medianDistanceErrorKpc": round_number(float(np.median(sigma)), 4),
                    "densityModels": fit_density_models(
                        position,
                        measurement,
                        ids,
                        seed=1000 + population_index * 100 + cloud_index,
                    ),
                    "lineOfSightSurfaceModels": fit_surface_models(local, sigma, ids),
                }
            )

    return {
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "dataPath": str(atlas_path),
        "notes": [
            "Density models compare full 3-D likelihoods with per-star line-of-sight distance covariance.",
            "Surface models compare conditional line-of-sight fits z=f(x,y) in the atlas tangent frame; compare them to each other, not directly to full-density likelihoods.",
            "AIC/BIC use full-sample fits. Held-out predictive likelihood uses a deterministic object-id split.",
        ],
        "results": results,
    }


def compact_summary(report: dict[str, object]) -> list[dict[str, object]]:
    summary = []
    for result in report["results"]:  # type: ignore[index]
        density_models = result["densityModels"]  # type: ignore[index]
        surface_models = result["lineOfSightSurfaceModels"]  # type: ignore[index]
        summary.append(
            {
                "population": result["populationId"],  # type: ignore[index]
                "cloud": result["cloudId"],  # type: ignore[index]
                "n": result["count"],  # type: ignore[index]
                "bestDensityBic": density_models[0]["model"],
                "bestDensityCv": max(density_models, key=lambda item: item["testLogLikelihoodPerStar"])["model"],
                "bestSurfaceBic": surface_models[0]["model"],
                "bestSurfaceCv": max(surface_models, key=lambda item: item["testLogLikelihoodPerStar"])["model"],
                "densityModels": [
                    [item["model"], item["deltaBIC"], item["testLogLikelihoodPerStar"]]
                    for item in density_models[:5]
                ],
                "surfaceModels": [
                    [item["model"], item["deltaBIC"], item["testLogLikelihoodPerStar"], item["intrinsicScatterKpc"]]
                    for item in surface_models
                ],
            }
        )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas", type=Path, default=DEFAULT_ATLAS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    report = compare_models(args.atlas)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(compact_summary(report), indent=2))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
