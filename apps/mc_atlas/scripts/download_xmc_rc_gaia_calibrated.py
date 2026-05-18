from __future__ import annotations

import argparse
import csv
import json
import math
import os
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin

import requests


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RAW_GAIA = ROOT / "data" / "raw" / "gaia"

DEFAULT_CHUNK_DIR = RAW_GAIA / "xmc_rc_gaia_calibrated_chunks"
GAIA_TAP_LOGIN = "https://gea.esac.esa.int/tap-server/login"
GAIA_TAP_ASYNC = "https://gea.esac.esa.int/tap-server/tap/async"
GAIA_TAP_SYNC = "https://gea.esac.esa.int/tap-server/tap/sync"
GAIA_DR3_SOURCE_COUNT = 1_811_709_771
SYNC_RETRY_SECONDS = (30, 90, 180)

TABLES = {
    "source": "gaiadr3.gaia_source",
    "source-lite": "gaiadr3.gaia_source_lite",
}
BASE_COLUMNS = (
    "source_id",
    "ra",
    "dec",
    "l",
    "b",
    "phot_g_mean_mag",
    "bp_rp",
    "pmra",
    "pmdec",
    "parallax",
    "parallax_over_error",
    "ruwe",
)


@dataclass(frozen=True)
class QueryRegion:
    name: str
    spatial_kind: str
    ra_deg: float | None = None
    dec_deg: float | None = None
    radius_deg: float | None = None
    l_min_attr: str | None = None
    l_max_attr: str | None = None
    b_min_attr: str | None = None
    b_max_attr: str | None = None
    pm_mode: str = "single"
    pmra_attr: str | None = None
    pmdec_attr: str | None = None
    pm_radius_attr: str | None = None


CLOUDS = {
    "LMC": QueryRegion(
        name="LMC",
        spatial_kind="circle",
        ra_deg=81.28,
        dec_deg=-69.78,
        radius_deg=30.0,
        pmra_attr="lmc_pmra",
        pmdec_attr="lmc_pmdec",
        pm_radius_attr="lmc_pm_radius",
    ),
    "BRIDGE": QueryRegion(
        name="BRIDGE",
        spatial_kind="galactic_box",
        l_min_attr="bridge_l_min",
        l_max_attr="bridge_l_max",
        b_min_attr="bridge_b_min",
        b_max_attr="bridge_b_max",
        pm_mode="bridge",
    ),
    "SMC": QueryRegion(
        name="SMC",
        spatial_kind="circle",
        ra_deg=13.10,
        dec_deg=-72.82,
        radius_deg=15.0,
        pmra_attr="smc_pmra",
        pmdec_attr="smc_pmdec",
        pm_radius_attr="smc_pm_radius",
    ),
}


def default_output_for_table(table: str) -> Path:
    suffix = "" if table == "source" else "_source_lite"
    return PROCESSED / f"xmc_rc_gaia_calibrated_full{suffix}.csv"


def table_columns(table: str) -> tuple[str, ...]:
    if table == "source":
        return BASE_COLUMNS + ("astrometric_excess_noise",)
    return BASE_COLUMNS


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_cloud_list(value: str) -> list[str]:
    clouds = []
    for raw in value.split(","):
        name = raw.strip().upper()
        if not name:
            continue
        if name not in CLOUDS:
            raise argparse.ArgumentTypeError(f"unknown region {name!r}; expected LMC, BRIDGE, SMC, or a comma list")
        if name not in clouds:
            clouds.append(name)
    if not clouds:
        raise argparse.ArgumentTypeError("at least one cloud is required")
    return clouds


def chunk_bounds(chunk_count: int) -> list[tuple[int, int]]:
    bounds = []
    for index in range(chunk_count):
        lower = math.floor(GAIA_DR3_SOURCE_COUNT * index / chunk_count)
        upper = math.floor(GAIA_DR3_SOURCE_COUNT * (index + 1) / chunk_count)
        bounds.append((lower, upper))
    bounds[-1] = (bounds[-1][0], GAIA_DR3_SOURCE_COUNT)
    return bounds


def chunk_path_for(args: argparse.Namespace, cloud: str, index: int) -> Path:
    table_tag = args.table.replace("-", "_")
    return args.chunk_dir / f"{table_tag}_{cloud.lower()}_ri{args.chunk_count:05d}_{index:05d}.csv"


def manifest_path_for_chunk(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".json")


def count_csv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def validate_csv_header(path: Path, expected_columns: tuple[str, ...]) -> None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
    if tuple(header or ()) != expected_columns:
        raise ValueError(f"{path} has unexpected CSV header: {header!r}")


def chunk_is_complete(
    path: Path,
    expected_columns: tuple[str, ...],
    args: argparse.Namespace,
    cloud: str,
    chunk_index: int,
    lower_random_index: int,
    upper_random_index: int,
) -> bool:
    manifest_path = manifest_path_for_chunk(path)
    if not path.exists() or not manifest_path.exists():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_csv_header(path, expected_columns)
        if manifest.get("status") != "completed":
            return False
        if manifest.get("cloud") != cloud or int(manifest.get("chunk", -1)) != chunk_index:
            return False
        if int(manifest.get("chunkCount", -1)) != args.chunk_count:
            return False
        if manifest.get("sourceTable") != TABLES[args.table]:
            return False
        if int(manifest.get("lowerRandomIndex", -1)) != lower_random_index:
            return False
        if int(manifest.get("upperRandomIndex", -1)) != upper_random_index:
            return False
        if manifest.get("query") != build_query(args, cloud, lower_random_index, upper_random_index).strip():
            return False
        return int(manifest.get("rows", -1)) == count_csv_rows(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return False


def write_chunk_manifest(path: Path, payload: dict[str, object]) -> None:
    manifest_path_for_chunk(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def persistent_user_env(name: str) -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
        return str(value) if value else None
    except OSError:
        return None


def gaia_credentials() -> tuple[str, str] | None:
    username = os.environ.get("GAIA_USER") or persistent_user_env("GAIA_USER")
    password = os.environ.get("GAIA_PASSWORD") or persistent_user_env("GAIA_PASSWORD")
    if username and password:
        return username, password
    return None


def gaia_session() -> tuple[requests.Session, bool]:
    session = requests.Session()
    credentials = gaia_credentials()
    if credentials is None:
        return session, False
    username, password = credentials
    response = session.post(
        GAIA_TAP_LOGIN,
        data={"username": username, "password": password},
        allow_redirects=True,
        timeout=60,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError("Gaia TAP authenticated login failed.") from error
    return session, True


def spatial_condition(args: argparse.Namespace, region_name: str) -> str:
    region = CLOUDS[region_name]
    if region.spatial_kind == "circle":
        return f"""CONTAINS(
    POINT('ICRS', ra, dec),
    CIRCLE('ICRS', {region.ra_deg:.8f}, {region.dec_deg:.8f}, {region.radius_deg:.8f})
  ) = 1"""
    if region.spatial_kind == "galactic_box":
        l_min = float(getattr(args, region.l_min_attr or ""))
        l_max = float(getattr(args, region.l_max_attr or ""))
        b_min = float(getattr(args, region.b_min_attr or ""))
        b_max = float(getattr(args, region.b_max_attr or ""))
        return f"""l BETWEEN {l_min:.8f} AND {l_max:.8f}
  AND b BETWEEN {b_min:.8f} AND {b_max:.8f}"""
    raise ValueError(f"Unsupported spatial kind {region.spatial_kind!r}")


def pm_condition(args: argparse.Namespace, region_name: str) -> str:
    region = CLOUDS[region_name]
    if region.pm_mode == "single":
        pmra = float(getattr(args, region.pmra_attr or ""))
        pmdec = float(getattr(args, region.pmdec_attr or ""))
        pm_radius = float(getattr(args, region.pm_radius_attr or ""))
        return (
            f"POWER(pmra - ({pmra:.6f}), 2) + POWER(pmdec - ({pmdec:.6f}), 2) "
            f"<= POWER({pm_radius:.6f}, 2)"
        )

    if region.pm_mode == "bridge":
        return f"""(
    POWER(pmra - ({args.lmc_pmra:.6f}), 2) + POWER(pmdec - ({args.lmc_pmdec:.6f}), 2) <= POWER({args.bridge_pm_radius:.6f}, 2)
    OR POWER(pmra - ({args.smc_pmra:.6f}), 2) + POWER(pmdec - ({args.smc_pmdec:.6f}), 2) <= POWER({args.bridge_pm_radius:.6f}, 2)
    OR POWER(pmra - ({args.bridge_mid_pmra:.6f}), 2) + POWER(pmdec - ({args.bridge_mid_pmdec:.6f}), 2) <= POWER({args.bridge_mid_pm_radius:.6f}, 2)
  )"""

    raise ValueError(f"Unsupported PM mode {region.pm_mode!r}")


def build_query(
    args: argparse.Namespace,
    cloud: str,
    lower_random_index: int,
    upper_random_index: int,
    *,
    count_only: bool = False,
) -> str:
    astrometric_excess_noise_filter = ""
    if args.table == "source":
        astrometric_excess_noise_filter = (
            f"\n  AND astrometric_excess_noise < {args.astrometric_excess_noise_max:.6f}"
        )

    select_clause = "COUNT(*) AS row_count" if count_only else ",\n  ".join(table_columns(args.table))
    return f"""
SELECT
  {select_clause}
FROM {TABLES[args.table]}
WHERE
  random_index >= {lower_random_index:d}
  AND random_index < {upper_random_index:d}
  AND {spatial_condition(args, cloud)}
  AND phot_g_mean_mag BETWEEN {args.query_g_min:.6f} AND {args.query_g_max:.6f}
  AND bp_rp BETWEEN {args.query_bp_rp_min:.6f} AND {args.query_bp_rp_max:.6f}
  AND ruwe < {args.ruwe_max:.6f}
{astrometric_excess_noise_filter}
  AND parallax IS NOT NULL
  AND parallax_over_error < {args.parallax_over_error_max:.6f}
  AND pmra IS NOT NULL
  AND pmdec IS NOT NULL
  AND {pm_condition(args, cloud)}
"""


def tap_async_query_to_file(
    query: str,
    output: Path,
    timeout: int,
    poll_seconds: float,
    maxrec: int,
    expected_columns: tuple[str, ...],
) -> dict[str, object]:
    session, authenticated = gaia_session()
    job_url = ""
    response = session.post(
        GAIA_TAP_ASYNC,
        data={
            "REQUEST": "doQuery",
            "LANG": "ADQL",
            "FORMAT": "csv",
            "QUERY": query,
            "MAXREC": str(maxrec),
        },
        allow_redirects=False,
        timeout=60,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(response.text) from error

    job_url = urljoin(GAIA_TAP_ASYNC, response.headers.get("Location") or response.url)
    print(f"Gaia TAP job: {job_url} ({'authenticated' if authenticated else 'anonymous'})", flush=True)

    try:
        phase_response = session.post(f"{job_url}/phase", data={"PHASE": "RUN"}, timeout=60)
        try:
            phase_response.raise_for_status()
        except requests.HTTPError as error:
            raise RuntimeError(phase_response.text) from error

        started = time.monotonic()
        last_phase = ""
        while True:
            phase = session.get(f"{job_url}/phase", timeout=60).text.strip().upper()
            if phase == "COMPLETED":
                break
            if phase in {"ERROR", "ABORTED"}:
                error = session.get(f"{job_url}/error", timeout=60).text
                raise RuntimeError(f"Gaia TAP job ended with phase {phase}:\n{error}")
            if time.monotonic() - started > timeout:
                raise TimeoutError(f"Gaia TAP job did not complete within {timeout} seconds; job URL: {job_url}")
            if phase != last_phase:
                print(f"Gaia TAP phase: {phase}", flush=True)
                last_phase = phase
            time.sleep(poll_seconds)

        output.parent.mkdir(parents=True, exist_ok=True)
        part_path = output.with_suffix(output.suffix + ".part")
        with session.get(f"{job_url}/results/result", stream=True, timeout=300) as result:
            try:
                result.raise_for_status()
            except requests.HTTPError as error:
                raise RuntimeError(result.text) from error
            with part_path.open("wb") as handle:
                for chunk in result.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
        part_path.replace(output)
        validate_csv_header(output, expected_columns)
        rows = count_csv_rows(output)
        if rows >= maxrec:
            raise RuntimeError(f"{output} has {rows} rows, which reached MAXREC={maxrec}; chunk may be truncated")
        return {
            "status": "completed",
            "jobUrl": job_url,
            "rows": rows,
            "bytes": output.stat().st_size,
            "seconds": round(time.monotonic() - started, 3),
        }
    finally:
        if job_url:
            try:
                session.delete(job_url, timeout=60)
            except requests.RequestException as error:
                print(f"Warning: could not delete Gaia TAP job {job_url}: {error}", flush=True)


def tap_sync_query_to_file(
    query: str,
    output: Path,
    timeout: int,
    maxrec: int,
    expected_columns: tuple[str, ...],
) -> dict[str, object]:
    started = time.monotonic()
    session, _ = gaia_session()
    output.parent.mkdir(parents=True, exist_ok=True)
    part_path = output.with_suffix(output.suffix + ".part")
    for attempt_index, retry_seconds in enumerate((*SYNC_RETRY_SECONDS, None), start=1):
        try:
            with session.post(
                GAIA_TAP_SYNC,
                data={
                    "REQUEST": "doQuery",
                    "LANG": "ADQL",
                    "FORMAT": "csv",
                    "QUERY": query,
                    "MAXREC": str(maxrec),
                },
                stream=True,
                timeout=(60, timeout),
            ) as result:
                try:
                    result.raise_for_status()
                except requests.HTTPError as error:
                    message = result.text
                    if retry_seconds is not None and result.status_code >= 500:
                        print(
                            f"Gaia TAP sync attempt {attempt_index} failed with HTTP {result.status_code}; "
                            f"retrying in {retry_seconds} seconds.",
                            flush=True,
                        )
                        time.sleep(retry_seconds)
                        continue
                    raise RuntimeError(message) from error
                with part_path.open("wb") as handle:
                    for chunk in result.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            handle.write(chunk)
                break
        except (requests.ConnectionError, requests.Timeout) as error:
            if retry_seconds is None:
                raise
            print(
                f"Gaia TAP sync attempt {attempt_index} failed with {type(error).__name__}; "
                f"retrying in {retry_seconds} seconds.",
                flush=True,
            )
            time.sleep(retry_seconds)
    else:
        raise RuntimeError("Gaia TAP sync query exhausted retry attempts")
    part_path.replace(output)
    validate_csv_header(output, expected_columns)
    rows = count_csv_rows(output)
    if rows >= maxrec:
        raise RuntimeError(f"{output} has {rows} rows, which reached MAXREC={maxrec}; chunk may be truncated")
    return {
        "status": "completed",
        "tapMode": "sync",
        "rows": rows,
        "bytes": output.stat().st_size,
        "seconds": round(time.monotonic() - started, 3),
    }


def concatenate_chunks(
    chunk_records: list[tuple[str, int, Path]],
    output: Path,
    expected_columns: tuple[str, ...],
    force: bool = False,
) -> dict[str, int]:
    if output.exists() and not force:
        print(f"Output already exists; leaving it in place: {output}", flush=True)
        return {
            "rows": count_csv_rows(output),
            "duplicateSourceIds": 0,
        }

    output.parent.mkdir(parents=True, exist_ok=True)
    part_path = output.with_suffix(output.suffix + ".part")
    source_id_index = expected_columns.index("source_id")
    total_rows = 0
    duplicates = 0
    seen_source_ids: set[str] = set()

    with part_path.open("w", encoding="utf-8", newline="") as out_handle:
        writer = csv.writer(out_handle, lineterminator="\n")
        writer.writerow(("cloud",) + expected_columns)
        for cloud, _, chunk in chunk_records:
            validate_csv_header(chunk, expected_columns)
            with chunk.open("r", encoding="utf-8", newline="") as in_handle:
                reader = csv.reader(in_handle)
                next(reader, None)
                for row in reader:
                    source_id = row[source_id_index]
                    if source_id in seen_source_ids:
                        duplicates += 1
                        continue
                    seen_source_ids.add(source_id)
                    writer.writerow((cloud,) + tuple(row))
                    total_rows += 1
    part_path.replace(output)
    return {
        "rows": total_rows,
        "duplicateSourceIds": duplicates,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download the calibrated Gaia DR3 XMC red-clump row set in small, "
            "resumable random_index chunks split by LMC, bridge, and SMC regions."
        )
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--chunk-dir", type=Path, default=DEFAULT_CHUNK_DIR)
    parser.add_argument("--table", choices=tuple(TABLES), default="source")
    parser.add_argument("--clouds", type=parse_cloud_list, default=parse_cloud_list("LMC,BRIDGE,SMC"))
    parser.add_argument("--chunk-count", type=int, default=1000)
    parser.add_argument("--start-chunk", type=int, default=0)
    parser.add_argument("--stop-chunk", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--poll-seconds", type=float, default=20.0)
    parser.add_argument("--maxrec", type=int, default=100_000)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-concat", action="store_true")
    parser.add_argument("--allow-partial-concat", action="store_true")
    parser.add_argument("--query-g-min", type=float, default=18.0)
    parser.add_argument("--query-g-max", type=float, default=20.35)
    parser.add_argument("--query-bp-rp-min", type=float, default=0.65)
    parser.add_argument("--query-bp-rp-max", type=float, default=1.85)
    parser.add_argument("--ruwe-max", type=float, default=1.4)
    parser.add_argument("--astrometric-excess-noise-max", type=float, default=2.0)
    parser.add_argument("--parallax-over-error-max", type=float, default=4.0)
    parser.add_argument("--lmc-pmra", type=float, default=1.776499)
    parser.add_argument("--lmc-pmdec", type=float, default=0.391679)
    parser.add_argument("--lmc-pm-radius", type=float, default=1.5)
    parser.add_argument("--smc-pmra", type=float, default=0.715272)
    parser.add_argument("--smc-pmdec", type=float, default=-1.229752)
    parser.add_argument("--smc-pm-radius", type=float, default=1.2)
    parser.add_argument("--bridge-l-min", type=float, default=282.0)
    parser.add_argument("--bridge-l-max", type=float, default=306.5)
    parser.add_argument("--bridge-b-min", type=float, default=-49.0)
    parser.add_argument("--bridge-b-max", type=float, default=-27.0)
    parser.add_argument("--bridge-pm-radius", type=float, default=2.5)
    parser.add_argument("--bridge-mid-pmra", type=float, default=1.245886)
    parser.add_argument("--bridge-mid-pmdec", type=float, default=-0.419037)
    parser.add_argument("--bridge-mid-pm-radius", type=float, default=2.0)
    args = parser.parse_args()
    if args.output is None:
        args.output = default_output_for_table(args.table)
    return args


def filters_manifest(args: argparse.Namespace) -> dict[str, object]:
    return {
        "queryG": [args.query_g_min, args.query_g_max],
        "queryBpRp": [args.query_bp_rp_min, args.query_bp_rp_max],
        "parallaxOverErrorMax": args.parallax_over_error_max,
        "ruweMax": args.ruwe_max,
        "astrometricExcessNoiseMax": args.astrometric_excess_noise_max if args.table == "source" else None,
        "cloudPm": {
            "LMC": {
                "pmra": args.lmc_pmra,
                "pmdec": args.lmc_pmdec,
                "radiusMasYr": args.lmc_pm_radius,
            },
            "BRIDGE": {
                "lmcPmRadiusMasYr": args.bridge_pm_radius,
                "smcPmRadiusMasYr": args.bridge_pm_radius,
                "midPmra": args.bridge_mid_pmra,
                "midPmdec": args.bridge_mid_pmdec,
                "midPmRadiusMasYr": args.bridge_mid_pm_radius,
            },
            "SMC": {
                "pmra": args.smc_pmra,
                "pmdec": args.smc_pmdec,
                "radiusMasYr": args.smc_pm_radius,
            },
        },
        "footprints": {
            "LMC": {
                "raDeg": CLOUDS["LMC"].ra_deg,
                "decDeg": CLOUDS["LMC"].dec_deg,
                "radiusDeg": CLOUDS["LMC"].radius_deg,
            },
            "BRIDGE": {
                "galacticLonDeg": [args.bridge_l_min, args.bridge_l_max],
                "galacticLatDeg": [args.bridge_b_min, args.bridge_b_max],
            },
            "SMC": {
                "raDeg": CLOUDS["SMC"].ra_deg,
                "decDeg": CLOUDS["SMC"].dec_deg,
                "radiusDeg": CLOUDS["SMC"].radius_deg,
            },
        },
    }


def main() -> None:
    args = parse_args()
    if args.chunk_count <= 0:
        raise ValueError("--chunk-count must be positive")
    if args.start_chunk < 0:
        raise ValueError("--start-chunk must be non-negative")
    stop_chunk = args.stop_chunk if args.stop_chunk is not None else args.chunk_count
    if stop_chunk < args.start_chunk or stop_chunk > args.chunk_count:
        raise ValueError("--stop-chunk must be between --start-chunk and --chunk-count")

    expected_columns = table_columns(args.table)
    bounds = chunk_bounds(args.chunk_count)
    selected_indices = list(range(args.start_chunk, stop_chunk))
    selected_records = [
        (cloud, index, chunk_path_for(args, cloud, index), bounds[index][0], bounds[index][1])
        for cloud in args.clouds
        for index in selected_indices
    ]

    if args.dry_run:
        for cloud, index, _, lower, upper in selected_records:
            print(f"-- {cloud} chunk {index:05d}: random_index [{lower}, {upper})")
            print(build_query(args, cloud, lower, upper).strip())
            print()
        return

    args.chunk_dir.mkdir(parents=True, exist_ok=True)
    completed_rows_this_run = 0
    for cloud, index, chunk_path, lower, upper in selected_records:
        if not args.force and chunk_is_complete(chunk_path, expected_columns, args, cloud, index, lower, upper):
            rows = count_csv_rows(chunk_path)
            completed_rows_this_run += rows
            print(f"{cloud} chunk {index:05d} already complete: {rows} rows", flush=True)
            continue

        print(
            f"Downloading {cloud} chunk {index:05d}/{args.chunk_count - 1:05d}: "
            f"random_index [{lower}, {upper})",
            flush=True,
        )
        query = build_query(args, cloud, lower, upper)
        try:
            result = tap_async_query_to_file(
                query,
                chunk_path,
                args.timeout,
                args.poll_seconds,
                args.maxrec,
                expected_columns,
            )
        except Exception:
            write_chunk_manifest(
                chunk_path,
                {
                    "status": "failed",
                    "cloud": cloud,
                    "chunk": index,
                    "chunkCount": args.chunk_count,
                    "lowerRandomIndex": lower,
                    "upperRandomIndex": upper,
                    "sourceTable": TABLES[args.table],
                    "query": query.strip(),
                    "updatedUnixSeconds": time.time(),
                },
            )
            raise

        result.update(
            {
                "cloud": cloud,
                "chunk": index,
                "chunkCount": args.chunk_count,
                "lowerRandomIndex": lower,
                "upperRandomIndex": upper,
                "sourceTable": TABLES[args.table],
                "columns": list(expected_columns),
                "query": query.strip(),
                "updatedUnixSeconds": time.time(),
            }
        )
        write_chunk_manifest(chunk_path, result)
        completed_rows_this_run += int(result["rows"])
        print(f"{cloud} chunk {index:05d} complete: {result['rows']} rows, {result['bytes']} bytes", flush=True)

    all_records = [
        (cloud, index, chunk_path_for(args, cloud, index), lower, upper)
        for cloud in args.clouds
        for index, (lower, upper) in enumerate(bounds)
    ]
    complete_records = [
        (cloud, index, path)
        for cloud, index, path, lower, upper in all_records
        if chunk_is_complete(path, expected_columns, args, cloud, index, lower, upper)
    ]

    expected_chunks = len(args.clouds) * args.chunk_count
    complete_rows = sum(count_csv_rows(path) for _, _, path in complete_records)
    manifest: dict[str, object] = {
        "source": "Gaia DR3",
        "method": "calibrated-xmc-rc-gaia-download-split-cloud-random-index",
        "sourceTable": TABLES[args.table],
        "columns": ["cloud", *expected_columns],
        "clouds": args.clouds,
        "chunkCount": args.chunk_count,
        "expectedChunks": expected_chunks,
        "completeChunks": len(complete_records),
        "completeRowsBeforeDedupe": complete_rows,
        "selectedRowsThisRun": completed_rows_this_run,
        "output": relative_path(args.output),
        "chunkDir": relative_path(args.chunk_dir),
        "filters": filters_manifest(args),
        "notes": [
            "Chunks are split by random_index and by query region to avoid the slow broad OR footprint query.",
            "The bridge region intentionally uses a broader PM gate to avoid clipping intermediate bridge kinematics.",
            "Output concatenation deduplicates overlapping LMC/bridge/SMC rows by source_id.",
            "Default PM centers are the final iterative-clipping centers measured from the validated 5 percent sample.",
        ],
    }

    can_concat = len(complete_records) == expected_chunks or args.allow_partial_concat
    if can_concat and not args.no_concat:
        concat = concatenate_chunks(complete_records, args.output, expected_columns, force=args.force)
        manifest["outputRows"] = concat["rows"]
        manifest["duplicateSourceIds"] = concat["duplicateSourceIds"]
        manifest["outputBytes"] = args.output.stat().st_size
        print(
            f"Combined {concat['rows']} deduplicated rows into {args.output} "
            f"({concat['duplicateSourceIds']} duplicate source_id rows skipped)",
            flush=True,
        )
    elif len(complete_records) != expected_chunks:
        print(
            f"{len(complete_records)}/{expected_chunks} chunks complete; skipping concatenation for now.",
            flush=True,
        )

    manifest_path = args.output.with_suffix(args.output.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"Wrote manifest {manifest_path}")


if __name__ == "__main__":
    main()
