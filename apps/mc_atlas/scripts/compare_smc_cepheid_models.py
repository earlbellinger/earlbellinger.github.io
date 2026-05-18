"""Compare simple SMC Cepheid density models with distance-error propagation.

The goal is diagnostic model comparison, not production atlas generation.  All
models are fit in the atlas local coordinate frame and evaluate held-out
likelihood with each star's quoted distance uncertainty projected into that
frame.  The curved/tapered/skew models are deliberately simple approximations:
they are useful for deciding whether a cleaner non-Gaussian body model is worth
promoting into the production annotation builder.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_annotation_structures as bas  # noqa: E402


OUT = ROOT / "diagnostics" / "smc_cepheid_model_comparison.json"
DF_GRID = (3.0, 4.0, 6.0, 10.0, 20.0, 50.0)
FOLD_COUNT = 5
SEED = 20260514
P = 3


def load_smc_cepheids() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray]]:
    payload = json.loads(bas.DEFAULT_ATLAS.read_text(encoding="utf-8"))
    indexes = {name: index for index, name in enumerate(payload["fields"]["catalog"])}
    origin = np.asarray(payload["meta"]["coordinateCenters"]["sampleGalacticVectorKpc"], dtype=float)
    basis = bas.make_basis(origin)
    arrays = bas.subset_arrays(payload, indexes, "cepheids", "smc")
    local = arrays["local"]  # type: ignore[assignment]
    position = arrays["position"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    measurement = bas.local_measurement_covariances(position, sigma, basis)
    return local, measurement, sigma, basis


def slogdet_inverse(covariances: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    covariances = (covariances + np.swapaxes(covariances, -1, -2)) * 0.5
    covariances = covariances + np.eye(P)[None, :, :] * 1e-7
    sign, logdet = np.linalg.slogdet(covariances)
    if np.any(sign <= 0):
        covariances[sign <= 0] += np.eye(P) * 1e-4
        sign, logdet = np.linalg.slogdet(covariances)
    return logdet, np.linalg.inv(covariances)


def log_t_eiv(local: np.ndarray, measurement: np.ndarray, mean: np.ndarray, covariance: np.ndarray, df: float) -> np.ndarray:
    total = covariance[None, :, :] + measurement
    logdet, inverse = slogdet_inverse(total)
    delta = local - mean
    mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
    norm = math.lgamma((df + P) * 0.5) - math.lgamma(df * 0.5) - 0.5 * P * math.log(df * math.pi)
    return norm - 0.5 * logdet - 0.5 * (df + P) * np.log1p(mahalanobis / df)


def log_gaussian_diag_coords(
    coords: np.ndarray,
    measurement: np.ndarray,
    variances: np.ndarray,
) -> np.ndarray:
    total = np.diag(variances)[None, :, :] + measurement
    logdet, inverse = slogdet_inverse(total)
    mahalanobis = np.einsum("ni,nij,nj->n", coords, inverse, coords)
    return -0.5 * (P * math.log(2 * math.pi) + logdet + mahalanobis)


def log_t_diag_coords(coords: np.ndarray, measurement: np.ndarray, variances: np.ndarray, df: float) -> np.ndarray:
    total = np.diag(variances)[None, :, :] + measurement
    logdet, inverse = slogdet_inverse(total)
    mahalanobis = np.einsum("ni,nij,nj->n", coords, inverse, coords)
    norm = math.lgamma((df + P) * 0.5) - math.lgamma(df * 0.5) - 0.5 * P * math.log(df * math.pi)
    return norm - 0.5 * logdet - 0.5 * (df + P) * np.log1p(mahalanobis / df)


def fit_student_t(local: np.ndarray, measurement: np.ndarray) -> dict[str, object]:
    best: dict[str, object] | None = None
    for df in DF_GRID:
        mean, covariance = bas.weighted_eiv_gaussian(local, measurement, np.ones(len(local)))
        previous = -np.inf
        for iteration in range(80):
            total = covariance[None, :, :] + measurement
            _logdet, inverse = slogdet_inverse(total)
            delta = local - mean
            mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
            weights = (df + P) / (df + np.maximum(mahalanobis, 0))
            mean, covariance = bas.weighted_eiv_gaussian(local, measurement, weights)
            log_likelihood = float(log_t_eiv(local, measurement, mean, covariance, df).sum())
            if iteration > 4 and log_likelihood - previous < 1e-6 * max(1.0, abs(previous)):
                break
            previous = log_likelihood
        candidate = {
            "name": f"student_t_df_{df:g}",
            "df": df,
            "mean": mean,
            "covariance": covariance,
            "log_likelihood": float(log_t_eiv(local, measurement, mean, covariance, df).sum()),
            "parameter_count": 10,
            "iterations": iteration + 1,
        }
        if best is None or candidate["log_likelihood"] > best["log_likelihood"]:  # type: ignore[operator]
            best = candidate
    assert best is not None
    return best


def fit_t_plus_tail(local: np.ndarray, measurement: np.ndarray) -> dict[str, object]:
    seeds = bas.fit_eiv_gmm_model_selection(local, measurement)[1]
    seed_weights = seeds["weights"]  # type: ignore[assignment]
    seed_means = seeds["means"]  # type: ignore[assignment]
    seed_covariances = seeds["covariances"]  # type: ignore[assignment]
    body_index = int(np.argmax(seed_weights))
    tail_index = 1 - body_index
    best: dict[str, object] | None = None
    for df in DF_GRID:
        weights = np.array([float(seed_weights[body_index]), float(seed_weights[tail_index])])
        weights /= weights.sum()
        body_mean = np.array(seed_means[body_index], dtype=float)
        body_covariance = np.array(seed_covariances[body_index], dtype=float)
        tail_mean = np.array(seed_means[tail_index], dtype=float)
        tail_covariance = np.array(seed_covariances[tail_index], dtype=float)
        previous = -np.inf
        responsibilities = np.zeros((len(local), 2), dtype=float)
        for iteration in range(100):
            body_log = math.log(max(weights[0], 1e-12)) + log_t_eiv(local, measurement, body_mean, body_covariance, df)
            tail_log = math.log(max(weights[1], 1e-12)) + bas.log_gaussian_eiv_local(local, measurement, tail_mean, tail_covariance)
            stacked = np.column_stack([body_log, tail_log])
            denominator = bas.logsumexp_rows(stacked)
            responsibilities = np.exp(stacked - denominator[:, None])
            robust = responsibilities[:, 0]
            total = body_covariance[None, :, :] + measurement
            _logdet, inverse = slogdet_inverse(total)
            delta = local - body_mean
            mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
            body_weights = robust * (df + P) / (df + np.maximum(mahalanobis, 0))
            body_mean, body_covariance = bas.weighted_eiv_gaussian(local, measurement, body_weights)
            tail_mean, tail_covariance = bas.weighted_eiv_gaussian(local, measurement, responsibilities[:, 1])
            weights = np.maximum(responsibilities.sum(axis=0) / len(local), 1e-5)
            weights /= weights.sum()
            log_likelihood = float(denominator.sum())
            if iteration > 4 and log_likelihood - previous < 1e-6 * max(1.0, abs(previous)):
                break
            previous = log_likelihood
        body_log = math.log(max(weights[0], 1e-12)) + log_t_eiv(local, measurement, body_mean, body_covariance, df)
        tail_log = math.log(max(weights[1], 1e-12)) + bas.log_gaussian_eiv_local(local, measurement, tail_mean, tail_covariance)
        log_likelihood = float(bas.logsumexp_rows(np.column_stack([body_log, tail_log])).sum())
        candidate = {
            "name": f"student_t_primary_gaussian_secondary_df_{df:g}",
            "df": df,
            "weights": weights,
            "body_mean": body_mean,
            "body_covariance": body_covariance,
            "tail_mean": tail_mean,
            "tail_covariance": tail_covariance,
            "responsibilities": responsibilities,
            "log_likelihood": log_likelihood,
            "parameter_count": 20,
            "iterations": iteration + 1,
        }
        if best is None or log_likelihood > best["log_likelihood"]:  # type: ignore[operator]
            best = candidate
    assert best is not None
    return best


def pca_frame(mean: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(bas.positive_semidefinite(covariance))
    order = np.argsort(values)[::-1]
    vectors = vectors[:, order]
    for index in range(P):
        pivot = int(np.argmax(np.abs(vectors[:, index])))
        if vectors[pivot, index] < 0:
            vectors[:, index] *= -1
    return vectors


def rotate_measurement(measurement: np.ndarray, frame: np.ndarray) -> np.ndarray:
    return np.einsum("ab,nbc,cd->nad", frame.T, measurement, frame)


def weighted_polyfit(x: np.ndarray, y: np.ndarray, weights: np.ndarray, degree: int) -> np.ndarray:
    design = np.column_stack([x**power for power in range(degree + 1)])
    sqrt_weights = np.sqrt(np.maximum(weights, 1e-9))
    lhs = design * sqrt_weights[:, None]
    rhs = y * sqrt_weights
    return np.linalg.lstsq(lhs, rhs, rcond=None)[0]


def fit_curved_body_tail(local: np.ndarray, measurement: np.ndarray) -> dict[str, object]:
    seed = fit_t_plus_tail(local, measurement)
    body_resp = seed["responsibilities"][:, 0]  # type: ignore[index]
    body_mean = seed["body_mean"]  # type: ignore[assignment]
    body_covariance = seed["body_covariance"]  # type: ignore[assignment]
    frame = pca_frame(body_mean, body_covariance)
    coords = (local - body_mean) @ frame
    rotated_measurement = rotate_measurement(measurement, frame)
    cy = weighted_polyfit(coords[:, 0], coords[:, 1], body_resp, 2)
    cz = weighted_polyfit(coords[:, 0], coords[:, 2], body_resp, 2)
    fitted_y = cy[0] + cy[1] * coords[:, 0] + cy[2] * coords[:, 0] ** 2
    fitted_z = cz[0] + cz[1] * coords[:, 0] + cz[2] * coords[:, 0] ** 2
    residual = np.column_stack([coords[:, 0], coords[:, 1] - fitted_y, coords[:, 2] - fitted_z])
    body_variance = np.maximum(((residual**2) * body_resp[:, None]).sum(axis=0) / body_resp.sum(), [0.12, 0.05, 0.05])
    tail_weights = 1 - body_resp
    tail_mean, tail_covariance = bas.weighted_eiv_gaussian(local, measurement, tail_weights)
    mixture_weights = np.array([float(body_resp.sum() / len(local)), float(tail_weights.sum() / len(local))])
    return {
        "name": "quadratic_principal_axis_primary_gaussian_secondary",
        "body_mean": body_mean,
        "frame": frame,
        "cy": cy,
        "cz": cz,
        "body_variance": body_variance,
        "tail_mean": tail_mean,
        "tail_covariance": tail_covariance,
        "weights": mixture_weights / mixture_weights.sum(),
        "parameter_count": 24,
    }


def log_curved_body_tail(model: dict[str, object], local: np.ndarray, measurement: np.ndarray) -> np.ndarray:
    body_mean = model["body_mean"]  # type: ignore[assignment]
    frame = model["frame"]  # type: ignore[assignment]
    coords = (local - body_mean) @ frame
    cy = model["cy"]  # type: ignore[assignment]
    cz = model["cz"]  # type: ignore[assignment]
    fitted_y = cy[0] + cy[1] * coords[:, 0] + cy[2] * coords[:, 0] ** 2
    fitted_z = cz[0] + cz[1] * coords[:, 0] + cz[2] * coords[:, 0] ** 2
    residual = np.column_stack([coords[:, 0], coords[:, 1] - fitted_y, coords[:, 2] - fitted_z])
    measurement_rot = rotate_measurement(measurement, frame)
    weights = model["weights"]  # type: ignore[assignment]
    body_log = math.log(max(float(weights[0]), 1e-12)) + log_gaussian_diag_coords(
        residual,
        measurement_rot,
        model["body_variance"],  # type: ignore[arg-type]
    )
    tail_log = math.log(max(float(weights[1]), 1e-12)) + bas.log_gaussian_eiv_local(
        local,
        measurement,
        model["tail_mean"],  # type: ignore[arg-type]
        model["tail_covariance"],  # type: ignore[arg-type]
    )
    return bas.logsumexp_rows(np.column_stack([body_log, tail_log]))


def fit_tapered_body_tail(local: np.ndarray, measurement: np.ndarray) -> dict[str, object]:
    seed = fit_t_plus_tail(local, measurement)
    body_resp = seed["responsibilities"][:, 0]  # type: ignore[index]
    body_mean = seed["body_mean"]  # type: ignore[assignment]
    body_covariance = seed["body_covariance"]  # type: ignore[assignment]
    frame = pca_frame(body_mean, body_covariance)
    coords = (local - body_mean) @ frame
    rotated_measurement = rotate_measurement(measurement, frame)
    t_scale = max(float(np.sqrt(np.average(coords[:, 0] ** 2, weights=body_resp))), 0.5)
    x = (coords[:, 0] / t_scale) ** 2
    base_variance = []
    slope = []
    for axis in (1, 2):
        y = np.maximum(coords[:, axis] ** 2 - rotated_measurement[:, axis, axis], 0.02)
        design = np.column_stack([np.ones(len(x)), x])
        sqrt_weights = np.sqrt(np.maximum(body_resp, 1e-9))
        coeff = np.linalg.lstsq(design * sqrt_weights[:, None], y * sqrt_weights, rcond=None)[0]
        base_variance.append(max(float(coeff[0]), 0.02))
        slope.append(max(float(coeff[1]), 0.0))
    variance_t = max(float(np.average(coords[:, 0] ** 2 - rotated_measurement[:, 0, 0], weights=body_resp)), 0.05)
    tail_weights = 1 - body_resp
    tail_mean, tail_covariance = bas.weighted_eiv_gaussian(local, measurement, tail_weights)
    mixture_weights = np.array([float(body_resp.sum() / len(local)), float(tail_weights.sum() / len(local))])
    return {
        "name": "tapered_triaxial_primary_gaussian_secondary",
        "body_mean": body_mean,
        "frame": frame,
        "variance_t": variance_t,
        "base_variance": np.asarray(base_variance),
        "slope": np.asarray(slope),
        "t_scale": t_scale,
        "tail_mean": tail_mean,
        "tail_covariance": tail_covariance,
        "weights": mixture_weights / mixture_weights.sum(),
        "parameter_count": 24,
    }


def log_tapered_body_tail(model: dict[str, object], local: np.ndarray, measurement: np.ndarray) -> np.ndarray:
    body_mean = model["body_mean"]  # type: ignore[assignment]
    frame = model["frame"]  # type: ignore[assignment]
    coords = (local - body_mean) @ frame
    measurement_rot = rotate_measurement(measurement, frame)
    x = (coords[:, 0] / float(model["t_scale"])) ** 2
    base_variance = model["base_variance"]  # type: ignore[assignment]
    slope = model["slope"]  # type: ignore[assignment]
    logs = []
    for index in range(len(local)):
        variances = np.array(
            [
                float(model["variance_t"]),
                float(base_variance[0] + slope[0] * x[index]),
                float(base_variance[1] + slope[1] * x[index]),
            ]
        )
        logs.append(log_gaussian_diag_coords(coords[index : index + 1], measurement_rot[index : index + 1], variances)[0])
    body_log = np.asarray(logs)
    weights = model["weights"]  # type: ignore[assignment]
    body_log = math.log(max(float(weights[0]), 1e-12)) + body_log
    tail_log = math.log(max(float(weights[1]), 1e-12)) + bas.log_gaussian_eiv_local(
        local,
        measurement,
        model["tail_mean"],  # type: ignore[arg-type]
        model["tail_covariance"],  # type: ignore[arg-type]
    )
    return bas.logsumexp_rows(np.column_stack([body_log, tail_log]))


def fit_split_t_body_tail(local: np.ndarray, measurement: np.ndarray) -> dict[str, object]:
    seed = fit_t_plus_tail(local, measurement)
    body_resp = seed["responsibilities"][:, 0]  # type: ignore[index]
    body_mean = seed["body_mean"]  # type: ignore[assignment]
    body_covariance = seed["body_covariance"]  # type: ignore[assignment]
    frame = pca_frame(body_mean, body_covariance)
    coords = (local - body_mean) @ frame
    rotated_measurement = rotate_measurement(measurement, frame)
    side = coords[:, 0] >= 0
    variance_negative = max(float(np.average(coords[~side, 0] ** 2 - rotated_measurement[~side, 0, 0], weights=body_resp[~side])), 0.05)
    variance_positive = max(float(np.average(coords[side, 0] ** 2 - rotated_measurement[side, 0, 0], weights=body_resp[side])), 0.05)
    residual_variance = np.maximum(
        ((coords[:, 1:] ** 2 - np.stack([rotated_measurement[:, 1, 1], rotated_measurement[:, 2, 2]], axis=1)) * body_resp[:, None]).sum(axis=0)
        / body_resp.sum(),
        [0.02, 0.02],
    )
    tail_weights = 1 - body_resp
    tail_mean, tail_covariance = bas.weighted_eiv_gaussian(local, measurement, tail_weights)
    mixture_weights = np.array([float(body_resp.sum() / len(local)), float(tail_weights.sum() / len(local))])
    return {
        "name": "split_student_t_primary_gaussian_secondary",
        "df": seed["df"],
        "body_mean": body_mean,
        "frame": frame,
        "variance_negative": variance_negative,
        "variance_positive": variance_positive,
        "residual_variance": residual_variance,
        "tail_mean": tail_mean,
        "tail_covariance": tail_covariance,
        "weights": mixture_weights / mixture_weights.sum(),
        "parameter_count": 23,
    }


def log_split_t_body_tail(model: dict[str, object], local: np.ndarray, measurement: np.ndarray) -> np.ndarray:
    body_mean = model["body_mean"]  # type: ignore[assignment]
    frame = model["frame"]  # type: ignore[assignment]
    coords = (local - body_mean) @ frame
    measurement_rot = rotate_measurement(measurement, frame)
    body_logs = []
    for index, row in enumerate(coords):
        var0 = float(model["variance_positive"] if row[0] >= 0 else model["variance_negative"])
        variances = np.array([var0, *model["residual_variance"]])  # type: ignore[list-item]
        body_logs.append(log_t_diag_coords(coords[index : index + 1], measurement_rot[index : index + 1], variances, float(model["df"]))[0])
    weights = model["weights"]  # type: ignore[assignment]
    body_log = math.log(max(float(weights[0]), 1e-12)) + np.asarray(body_logs)
    tail_log = math.log(max(float(weights[1]), 1e-12)) + bas.log_gaussian_eiv_local(
        local,
        measurement,
        model["tail_mean"],  # type: ignore[arg-type]
        model["tail_covariance"],  # type: ignore[arg-type]
    )
    return bas.logsumexp_rows(np.column_stack([body_log, tail_log]))


def evaluate_known_model(name: str, parameter_count: int, log_likelihood: float, n: int, extra: dict[str, object] | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "name": name,
        "parameterCount": parameter_count,
        "logLikelihood": log_likelihood,
        "AIC": 2 * parameter_count - 2 * log_likelihood,
        "BIC": parameter_count * math.log(n) - 2 * log_likelihood,
    }
    if extra:
        result.update(extra)
    return result


def fit_models(local: np.ndarray, measurement: np.ndarray) -> dict[str, dict[str, object]]:
    n = len(local)
    models: dict[str, dict[str, object]] = {}
    gmm_candidates = bas.fit_eiv_gmm_model_selection(local, measurement)
    for candidate in gmm_candidates:
        weights = candidate["weights"]  # type: ignore[assignment]
        means = candidate["means"]  # type: ignore[assignment]
        covariances = candidate["covariances"]  # type: ignore[assignment]
        key = f"eiv_gmm_{candidate['componentCount']}"
        models[key] = evaluate_known_model(
            key,
            int(candidate["parameterCount"]),
            float(candidate["logLikelihood"]),
            n,
            {
                "weights": [round_number(float(weight), 4) for weight in weights],
                "componentCount": int(candidate["componentCount"]),
                "predict": lambda x, m, w=weights, mu=means, cov=covariances: bas.log_eiv_mixture_local(x, m, w, mu, cov),
            },
        )
    student = fit_student_t(local, measurement)
    models["student_t"] = evaluate_known_model(
        "student_t",
        int(student["parameter_count"]),
        float(student["log_likelihood"]),
        n,
        {
            "df": float(student["df"]),
            "predict": lambda x, m, mean=student["mean"], cov=student["covariance"], df=student["df"]: log_t_eiv(x, m, mean, cov, float(df)),
        },
    )
    t_tail = fit_t_plus_tail(local, measurement)
    models["student_t_primary_gaussian_secondary"] = evaluate_known_model(
        "student_t_primary_gaussian_secondary",
        int(t_tail["parameter_count"]),
        float(t_tail["log_likelihood"]),
        n,
        {
            "df": float(t_tail["df"]),
            "weights": [round_number(float(weight), 4) for weight in t_tail["weights"]],  # type: ignore[index]
            "predict": lambda x, m, model=t_tail: bas.logsumexp_rows(
                np.column_stack(
                    [
                        math.log(max(float(model["weights"][0]), 1e-12))  # type: ignore[index]
                        + log_t_eiv(x, m, model["body_mean"], model["body_covariance"], float(model["df"])),  # type: ignore[arg-type]
                        math.log(max(float(model["weights"][1]), 1e-12))  # type: ignore[index]
                        + bas.log_gaussian_eiv_local(x, m, model["tail_mean"], model["tail_covariance"]),  # type: ignore[arg-type]
                    ]
                )
            ),
        },
    )
    curved = fit_curved_body_tail(local, measurement)
    curved_ll = float(log_curved_body_tail(curved, local, measurement).sum())
    models["curved_primary_gaussian_secondary"] = evaluate_known_model(
        "curved_primary_gaussian_secondary",
        int(curved["parameter_count"]),
        curved_ll,
        n,
        {
            "weights": [round_number(float(weight), 4) for weight in curved["weights"]],  # type: ignore[index]
            "predict": lambda x, m, model=curved: log_curved_body_tail(model, x, m),
        },
    )
    tapered = fit_tapered_body_tail(local, measurement)
    tapered_ll = float(log_tapered_body_tail(tapered, local, measurement).sum())
    models["tapered_primary_gaussian_secondary"] = evaluate_known_model(
        "tapered_primary_gaussian_secondary",
        int(tapered["parameter_count"]),
        tapered_ll,
        n,
        {
            "weights": [round_number(float(weight), 4) for weight in tapered["weights"]],  # type: ignore[index]
            "predict": lambda x, m, model=tapered: log_tapered_body_tail(model, x, m),
        },
    )
    split = fit_split_t_body_tail(local, measurement)
    split_ll = float(log_split_t_body_tail(split, local, measurement).sum())
    models["split_student_t_primary_gaussian_secondary"] = evaluate_known_model(
        "split_student_t_primary_gaussian_secondary",
        int(split["parameter_count"]),
        split_ll,
        n,
        {
            "df": float(split["df"]),
            "weights": [round_number(float(weight), 4) for weight in split["weights"]],  # type: ignore[index]
            "predict": lambda x, m, model=split: log_split_t_body_tail(model, x, m),
        },
    )
    return models


def round_number(value: float, digits: int = 6) -> float:
    rounded = round(float(value), digits)
    return 0.0 if rounded == -0.0 else rounded


def main() -> None:
    local, measurement, sigma, _basis = load_smc_cepheids()
    n = len(local)
    models = fit_models(local, measurement)
    full_rows = []
    best_bic = min(float(model["BIC"]) for model in models.values())
    for name, model in models.items():
        full_rows.append(
            {
                key: value
                for key, value in model.items()
                if key not in {"predict"}
            }
            | {"deltaBIC": float(model["BIC"]) - best_bic}
        )
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(n)
    folds = np.array_split(perm, FOLD_COUNT)
    heldout = {name: 0.0 for name in models}
    fold_rows = []
    for fold_index, test_index in enumerate(folds):
        train_mask = np.ones(n, dtype=bool)
        train_mask[test_index] = False
        train_index = np.where(train_mask)[0]
        train_models = fit_models(local[train_index], measurement[train_index])
        row: dict[str, object] = {"fold": fold_index, "nTest": int(len(test_index))}
        for name, model in train_models.items():
            predict: Callable[[np.ndarray, np.ndarray], np.ndarray] = model["predict"]  # type: ignore[assignment]
            log_likelihood = float(predict(local[test_index], measurement[test_index]).sum())
            heldout[name] += log_likelihood
            row[name] = round_number(log_likelihood, 2)
        fold_rows.append(row)
    heldout_rows = [
        {
            "name": name,
            "heldoutLogLikelihood": round_number(value, 2),
            "heldoutLogLikelihoodPerStar": round_number(value / n, 6),
        }
        for name, value in sorted(heldout.items(), key=lambda item: item[1], reverse=True)
    ]
    output = {
        "population": "SMC Cepheids",
        "count": n,
        "medianDistanceErrorKpc": round_number(float(np.median(sigma)), 3),
        "notes": [
            "EIV means quoted distance uncertainties are included as per-star measurement covariance.",
            "Curved, tapered, and split-t models use simple local coordinate approximations and should be read as diagnostics.",
            "Mixture-model likelihood ratio p-values are not reported because regular LRT assumptions fail for mixtures.",
        ],
        "fullSample": sorted(full_rows, key=lambda item: float(item["BIC"])),
        "folds": fold_rows,
        "heldout": heldout_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
