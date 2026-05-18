from __future__ import annotations

import csv
import math
import statistics
import urllib.error
import urllib.request
from bisect import bisect_left
from pathlib import Path
from typing import Any


REFERENCE_PATH = Path(__file__).resolve().parent / "reference" / "eclipsing_binary_distances.tsv"
RAW_OGLE_ECL_DIR = Path("data") / "raw" / "ogle_ecl"
LIGHT_CURVE_SAMPLE_COUNT = 256
CATALOG_JULIAN_DATE_OFFSET = 2_450_000.0
DEFAULT_VIEW_AXIS_ROTATION_DEGREES = 15.0

EQ_TO_GAL = (
    (-0.0548755604162154, -0.8734370902348850, -0.4838350155487132),
    (0.4941094278755837, -0.4448296299600112, 0.7469822444972189),
    (-0.8676661490190047, -0.1980763734312015, 0.4559837761750669),
)

FIELDS = [
    "x",
    "y",
    "z",
    "id",
    "ocvsId",
    "cloud",
    "raDeg",
    "decDeg",
    "galLonDeg",
    "galLatDeg",
    "distanceKpc",
    "distanceErrorKpc",
    "distanceModulus",
    "distanceModulusStatError",
    "distanceModulusSystematicError",
    "centerCorrectionMag",
    "sourceId",
    "quality",
    "periodDays",
    "t0HjdMinus2450000",
    "primaryRadiusSolar",
    "secondaryRadiusSolar",
    "equivalentRadiusSolar",
    "primaryTeffK",
    "secondaryTeffK",
    "primaryLuminositySolar",
    "secondaryLuminositySolar",
    "systemLuminositySolar",
    "lightCurveBand",
    "lightCurveFluxSamples",
    "lightCurveQuality",
    "notes",
]

ECL_CATALOG_URLS = {
    "lmc": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/ecl/ecl.dat",
    "smc": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/ecl/ecl.dat",
}

SOURCE_ENTRIES = [
    {
        "name": "Pietrzynski et al. 2019 LMC late-type eclipsing-binary distances",
        "url": "https://www.nature.com/articles/s41586-019-0999-4",
    },
    {
        "name": "Graczyk et al. 2020 SMC late-type eclipsing-binary distances",
        "url": "https://arxiv.org/abs/2010.08754",
    },
    {
        "name": "Graczyk et al. 2018 LMC late-type eclipsing-binary parameters",
        "url": "https://arxiv.org/abs/1805.04952",
    },
    {
        "name": "OGLE-IV OCVS eclipsing-binary light curves",
        "url": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/",
    },
]


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def round_number(value: float | None, digits: int = 3) -> float | None:
    if value is None or not math.isfinite(value):
        return None
    rounded = round(value, digits)
    if rounded == 0:
        return 0
    return rounded


def distance_modulus_to_kpc(mu0: float) -> float:
    return 10 ** ((mu0 - 10) / 5)


def distance_error_from_modulus(distance_kpc: float, error_mag: float | None) -> float | None:
    if error_mag is None or not math.isfinite(error_mag) or error_mag <= 0:
        return None
    return (math.log(10) / 5) * distance_kpc * error_mag


def combined_modulus_error(*errors: float | None) -> float | None:
    valid = [error for error in errors if error is not None and math.isfinite(error) and error > 0]
    if not valid:
        return None
    return math.sqrt(sum(error * error for error in valid))


def hms_to_degrees(value: str) -> float:
    parts = [float(part) for part in value.strip().replace(" ", ":").split(":")]
    if len(parts) != 3:
        raise ValueError(f"Expected HH:MM:SS value, got {value!r}")
    return (parts[0] + parts[1] / 60 + parts[2] / 3600) * 15


def dms_to_degrees(value: str) -> float:
    text = value.strip().replace(" ", ":")
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-")
    parts = [float(part) for part in text.split(":")]
    if len(parts) != 3:
        raise ValueError(f"Expected DD:MM:SS value, got {value!r}")
    return sign * (parts[0] + parts[1] / 60 + parts[2] / 3600)


def mat_vec_mul(matrix: tuple[tuple[float, float, float], ...], vector: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(sum(row[index] * vector[index] for index in range(3)) for row in matrix)  # type: ignore[return-value]


def transpose_matrix(matrix: tuple[tuple[float, float, float], ...]) -> tuple[tuple[float, float, float], ...]:
    return tuple(tuple(matrix[row][column] for row in range(3)) for column in range(3))


def vector_length(vector: tuple[float, float, float]) -> float:
    return math.sqrt(sum(component * component for component in vector))


def galactic_to_equatorial_vector(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    return mat_vec_mul(transpose_matrix(EQ_TO_GAL), vector)


def equatorial_vector_to_ra_dec(vector: tuple[float, float, float]) -> tuple[float, float]:
    radius = vector_length(vector)
    if radius == 0:
        return 0.0, 0.0
    ra = math.degrees(math.atan2(vector[1], vector[0])) % 360
    dec = math.degrees(math.asin(max(-1, min(1, vector[2] / radius))))
    return ra, dec


def equatorial_to_galactic_vector(ra_deg: float, dec_deg: float, distance: float) -> tuple[float, float, float]:
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    eq = (
        math.cos(dec) * math.cos(ra),
        math.cos(dec) * math.sin(ra),
        math.sin(dec),
    )
    gal = mat_vec_mul(EQ_TO_GAL, eq)
    return (gal[0] * distance, gal[1] * distance, gal[2] * distance)


def lon_lat_from_vector(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    radius = vector_length(vector)
    if radius == 0:
        return 0.0, 0.0, 0.0
    lon = math.degrees(math.atan2(vector[1], vector[0])) % 360
    lat = math.degrees(math.asin(max(-1, min(1, vector[2] / radius))))
    return lon, lat, radius


def make_basis(origin: tuple[float, float, float]) -> dict[str, tuple[float, float, float]]:
    radius = vector_length(origin)
    radial = tuple(component / radius for component in origin)
    ra, dec = equatorial_vector_to_ra_dec(galactic_to_equatorial_vector(radial))
    ra_rad = math.radians(ra)
    dec_rad = math.radians(dec)
    east = mat_vec_mul(EQ_TO_GAL, (-math.sin(ra_rad), math.cos(ra_rad), 0.0))
    north = mat_vec_mul(
        EQ_TO_GAL,
        (
            -math.sin(dec_rad) * math.cos(ra_rad),
            -math.sin(dec_rad) * math.sin(ra_rad),
            math.cos(dec_rad),
        ),
    )
    axis_angle = math.radians(DEFAULT_VIEW_AXIS_ROTATION_DEGREES)
    axis_cos = math.cos(axis_angle)
    axis_sin = math.sin(axis_angle)
    ogle_x = tuple(east[i] * axis_cos - north[i] * axis_sin for i in range(3))
    ogle_y = tuple(east[i] * axis_sin + north[i] * axis_cos for i in range(3))
    return {"east": ogle_x, "north": ogle_y, "radial": radial}


def project_local(
    vector: tuple[float, float, float],
    origin: tuple[float, float, float],
    basis: dict[str, tuple[float, float, float]],
) -> tuple[float, float, float]:
    delta = tuple(vector[i] - origin[i] for i in range(3))
    return tuple(sum(delta[i] * basis[key][i] for i in range(3)) for key in ("east", "north", "radial"))  # type: ignore[return-value]


def payload_origin(payload: dict[str, Any]) -> tuple[float, float, float]:
    raw = payload.get("meta", {}).get("coordinateCenters", {}).get("sampleGalacticVectorKpc")
    if isinstance(raw, list) and len(raw) == 3 and all(isinstance(value, (int, float)) for value in raw):
        return float(raw[0]), float(raw[1]), float(raw[2])
    catalog = payload.get("datasets", {}).get("catalog", [])
    if catalog:
        total = [0.0, 0.0, 0.0]
        count = 0
        for row in catalog:
            try:
                total[0] += float(row[0])
                total[1] += float(row[1])
                total[2] += float(row[2])
                count += 1
            except (TypeError, ValueError, IndexError):
                continue
        if count:
            return total[0] / count, total[1] / count, total[2] / count
    distance = float(payload.get("meta", {}).get("originDistanceKpc") or 50)
    return 0.0, 0.0, distance


def reference_rows(path: Path = REFERENCE_PATH) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def ocvs_cloud(ocvs_id: str) -> str | None:
    text = ocvs_id.upper()
    if "LMC" in text:
        return "lmc"
    if "SMC" in text:
        return "smc"
    return None


def download_if_missing(url: str, path: Path) -> bool:
    if path.exists() and path.stat().st_size > 0:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
    except (urllib.error.URLError, TimeoutError, OSError):
        return False
    if not data:
        return False
    path.write_bytes(data)
    return True


def ecl_catalog_path(root: Path, cloud: str) -> Path:
    return root / RAW_OGLE_ECL_DIR / f"{cloud}_ecl.dat"


def load_ogle_ecl_catalog(root: Path, cloud: str) -> dict[str, dict[str, float]]:
    path = ecl_catalog_path(root, cloud)
    url = ECL_CATALOG_URLS.get(cloud)
    if url:
        download_if_missing(url, path)
    catalog: dict[str, dict[str, float]] = {}
    if not path.exists():
        return catalog
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        parts = raw_line.split()
        if len(parts) < 5:
            continue
        try:
            period = float(parts[3])
            t0 = float(parts[4])
        except ValueError:
            continue

        def optional_float(index: int) -> float:
            try:
                return float(parts[index])
            except (ValueError, IndexError):
                return math.nan

        try:
            catalog[parts[0]] = {
                "iMag": optional_float(1),
                "vMag": optional_float(2),
                "period": period,
                "t0": t0,
                "amplitudeI": optional_float(5),
                "amplitudeV": optional_float(6),
            }
        except IndexError:
            continue
    return catalog


def photometry_path(root: Path, ocvs_id: str, band: str) -> Path:
    return root / RAW_OGLE_ECL_DIR / "phot" / band / f"{ocvs_id}.dat"


def photometry_url(ocvs_id: str, band: str) -> str | None:
    cloud = ocvs_cloud(ocvs_id)
    if not cloud:
        return None
    return f"https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/{cloud}/ecl/phot/{band}/{ocvs_id}.dat"


def read_photometry(path: Path) -> list[tuple[float, float, float | None]]:
    rows: list[tuple[float, float, float | None]] = []
    if not path.exists():
        return rows
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            time = float(parts[0])
            mag = float(parts[1])
            err = float(parts[2]) if len(parts) > 2 else None
        except ValueError:
            continue
        if math.isfinite(time) and math.isfinite(mag):
            rows.append((time, mag, err if err is not None and math.isfinite(err) else None))
    return rows


def quantile(values: list[float], fraction: float) -> float:
    if not values:
        return math.nan
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = max(0, min(1, fraction)) * (len(ordered) - 1)
    low = math.floor(position)
    high = math.ceil(position)
    amount = position - low
    return ordered[low] * (1 - amount) + ordered[high] * amount


def fill_periodic_bins(values: list[float | None]) -> list[float]:
    known = [(index, value) for index, value in enumerate(values) if value is not None and math.isfinite(value)]
    if not known:
        return [1.0] * len(values)
    if len(known) == 1:
        return [float(known[0][1])] * len(values)
    indices = [index for index, _value in known]
    extended = [(index - len(values), value) for index, value in known] + known + [
        (index + len(values), value) for index, value in known
    ]
    extended_indices = [index for index, _value in extended]
    filled: list[float] = []
    for index, value in enumerate(values):
        if value is not None and math.isfinite(value):
            filled.append(float(value))
            continue
        position = bisect_left(extended_indices, index)
        left_index, left_value = extended[max(0, position - 1)]
        right_index, right_value = extended[min(len(extended) - 1, position)]
        span = max(1, right_index - left_index)
        amount = (index - left_index) / span
        filled.append(float(left_value) * (1 - amount) + float(right_value) * amount)
    return filled


def binned_light_curve_samples(
    root: Path,
    ocvs_id: str,
    period: float | None,
    t0: float | None,
    *,
    download_light_curves: bool = True,
) -> tuple[list[float], str]:
    if not ocvs_id or period is None or period <= 0 or t0 is None:
        return [], "missing"

    path = photometry_path(root, ocvs_id, "I")
    url = photometry_url(ocvs_id, "I")
    if download_light_curves and url:
        download_if_missing(url, path)
    photometry = read_photometry(path)
    if len(photometry) < 8:
        return [], "missing"

    times = [time for time, _mag, _err in photometry]
    mags = [mag for _time, mag, _err in photometry]
    t0_local = t0 - CATALOG_JULIAN_DATE_OFFSET if statistics.median(times) < 1_000_000 and t0 > 2_400_000 else t0
    baseline_mag = quantile(mags, 0.16)
    bins: list[list[float]] = [[] for _ in range(LIGHT_CURVE_SAMPLE_COUNT)]
    for time, mag, _err in photometry:
        phase = ((time - t0_local) / period) % 1
        bin_index = min(LIGHT_CURVE_SAMPLE_COUNT - 1, int(phase * LIGHT_CURVE_SAMPLE_COUNT))
        flux = 10 ** (-0.4 * (mag - baseline_mag))
        if math.isfinite(flux):
            bins[bin_index].append(max(0.02, min(1.8, flux)))

    raw = [statistics.median(values) if values else None for values in bins]
    filled = fill_periodic_bins(raw)
    bright_reference = quantile([value for value in filled if math.isfinite(value)], 0.98)
    if not math.isfinite(bright_reference) or bright_reference <= 0:
        bright_reference = max(filled) if filled else 1.0
    samples = [round_number(max(0.02, min(1.0, value / bright_reference)), 4) or 1.0 for value in filled]
    measured_bins = sum(1 for value in raw if value is not None)
    quality = "ogle-i-binned" if measured_bins >= LIGHT_CURVE_SAMPLE_COUNT * 0.25 else "ogle-i-sparse"
    return samples, quality


def t0_minus_offset(t0: float | None) -> float | None:
    if t0 is None:
        return None
    return t0 - CATALOG_JULIAN_DATE_OFFSET if t0 > 2_400_000 else t0


def build_anchor_rows(
    payload: dict[str, Any],
    *,
    root: Path,
    download_light_curves: bool = True,
) -> tuple[list[list[Any]], dict[str, Any]]:
    origin = payload_origin(payload)
    basis = make_basis(origin)
    ecl_catalogs = {
        "lmc": load_ogle_ecl_catalog(root, "lmc"),
        "smc": load_ogle_ecl_catalog(root, "smc"),
    }

    rows: list[list[Any]] = []
    light_curve_count = 0
    for source_row in reference_rows(root / REFERENCE_PATH.relative_to(Path(__file__).resolve().parent.parent)):
        object_id = source_row["id"].strip()
        ocvs_id = source_row["ocvsId"].strip()
        cloud = source_row["cloud"].strip()
        ra_deg = hms_to_degrees(source_row["raHms"])
        dec_deg = dms_to_degrees(source_row["decDms"])
        mu0 = parse_float(source_row["distanceModulus"])
        stat_error = parse_float(source_row["distanceModulusStatError"])
        systematic_error = parse_float(source_row["distanceModulusSystematicError"])
        distance = parse_float(source_row["distanceKpc"])
        if distance is None and mu0 is not None:
            distance = distance_modulus_to_kpc(mu0)
        if distance is None:
            raise ValueError(f"No distance for {object_id}")
        explicit_distance_error = parse_float(source_row["distanceKpcError"])
        combined_error = combined_modulus_error(stat_error, systematic_error)
        distance_error = (
            explicit_distance_error
            if explicit_distance_error is not None
            else distance_error_from_modulus(distance, combined_error)
        )
        ecl_catalog = ecl_catalogs.get(ocvs_cloud(ocvs_id) or "", {})
        ecl_entry = ecl_catalog.get(ocvs_id, {})
        period = parse_float(source_row["periodDays"]) or ecl_entry.get("period")
        t0 = parse_float(source_row["t0Hjd"]) or ecl_entry.get("t0")
        primary_radius = parse_float(source_row["primaryRadiusSolar"])
        secondary_radius = parse_float(source_row["secondaryRadiusSolar"])
        primary_luminosity = parse_float(source_row["primaryLuminositySolar"])
        secondary_luminosity = parse_float(source_row["secondaryLuminositySolar"])
        equivalent_radius = (
            math.sqrt((primary_radius or 0) ** 2 + (secondary_radius or 0) ** 2)
            if primary_radius is not None or secondary_radius is not None
            else None
        )
        system_luminosity = (
            (primary_luminosity or 0) + (secondary_luminosity or 0)
            if primary_luminosity is not None or secondary_luminosity is not None
            else None
        )
        vector = equatorial_to_galactic_vector(ra_deg, dec_deg, distance)
        x, y, z = project_local(vector, origin, basis)
        lon, lat, _distance = lon_lat_from_vector(vector)
        samples, light_curve_quality = binned_light_curve_samples(
            root,
            ocvs_id,
            period,
            t0,
            download_light_curves=download_light_curves,
        )
        if samples:
            light_curve_count += 1

        rows.append(
            [
                round_number(x, 3),
                round_number(y, 3),
                round_number(z, 3),
                object_id,
                ocvs_id or None,
                cloud,
                round_number(ra_deg, 6),
                round_number(dec_deg, 6),
                round_number(lon, 6),
                round_number(lat, 6),
                round_number(distance, 3),
                round_number(distance_error, 3),
                round_number(mu0, 3),
                round_number(stat_error, 3),
                round_number(systematic_error, 3),
                round_number(parse_float(source_row["centerCorrectionMag"]), 3),
                source_row["sourceId"].strip(),
                source_row["quality"].strip(),
                round_number(period, 7),
                round_number(t0_minus_offset(t0), 4),
                round_number(primary_radius, 2),
                round_number(secondary_radius, 2),
                round_number(equivalent_radius, 2),
                round_number(parse_float(source_row["primaryTeffK"]), 0),
                round_number(parse_float(source_row["secondaryTeffK"]), 0),
                round_number(primary_luminosity, 1),
                round_number(secondary_luminosity, 1),
                round_number(system_luminosity, 1),
                "I" if samples else None,
                samples,
                light_curve_quality,
                source_row["notes"].strip(),
            ]
        )

    summary = {
        "eclipsingBinaryDistances": len(rows),
        "eclipsingBinaryLightCurves": light_curve_count,
        "eclipsingBinaryLightCurveSamples": LIGHT_CURVE_SAMPLE_COUNT,
    }
    return rows, summary


def append_unique(values: list[Any], value: Any) -> None:
    if value not in values:
        values.append(value)


def update_bounds(payload: dict[str, Any], rows: list[list[Any]]) -> None:
    if not rows:
        return
    bounds = payload.setdefault("bounds", {})
    for axis, index in (("x", 0), ("y", 1), ("z", 2)):
        values = [float(row[index]) for row in rows if row[index] is not None]
        if not values:
            continue
        existing = bounds.get(axis)
        if isinstance(existing, list) and len(existing) == 2:
            values.extend([float(existing[0]), float(existing[1])])
        bounds[axis] = [round_number(min(values), 3), round_number(max(values), 3)]


def apply_eclipsing_binary_distance_anchors(
    payload: dict[str, Any],
    *,
    root: Path | str | None = None,
    download_light_curves: bool = True,
) -> dict[str, Any]:
    root_path = Path(root) if root is not None else Path(__file__).resolve().parent.parent
    rows, summary = build_anchor_rows(payload, root=root_path, download_light_curves=download_light_curves)
    payload.setdefault("fields", {})["eclipsingBinaryDistances"] = FIELDS
    payload.setdefault("datasets", {})["eclipsingBinaryDistances"] = rows
    payload.setdefault("counts", {}).update(summary)
    update_bounds(payload, rows)

    meta = payload.setdefault("meta", {})
    generated_from = meta.setdefault("generatedFrom", [])
    if isinstance(generated_from, list):
        append_unique(generated_from, "Late-type detached eclipsing-binary geometric distance anchors")
    meta["eclipsingBinaryDistanceNote"] = (
        "Curated late-type detached eclipsing binaries from Pietrzynski et al. 2019 for the LMC "
        "and Graczyk et al. 2020 for the SMC. Distance errors use the published kpc uncertainty "
        "when provided, otherwise the quadrature sum of statistical and systematic distance-modulus "
        "errors. Glyph size uses sqrt(R1^2+R2^2), color blends published component Teff by luminosity, "
        "and secure OGLE-IV OCVS matches carry a 256-bin I-band relative-flux eclipse curve for display dimming."
    )

    sources = payload.setdefault("sources", [])
    if isinstance(sources, list):
        existing_names = {source.get("name") for source in sources if isinstance(source, dict)}
        for source in SOURCE_ENTRIES:
            if source["name"] not in existing_names:
                sources.append(source)
                existing_names.add(source["name"])
    return summary
