from __future__ import annotations

import json
import math
import struct
import base64
import bisect
import csv
import gzip
import hashlib
import os
import re
import tarfile
import urllib.parse
import urllib.request
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "public" / "data"
PROCESSED = ROOT / "data" / "processed"

M_SUN_I = 4.10
T_SUN = 5772
LOG_G_SUN = 4.438
SUN_V_MINUS_I = 0.69
BLACKBODY_V_NM = 550.0
BLACKBODY_I_NM = 806.0
PLANCK_HC_OVER_K_M = 0.01438776877
V_MINUS_I_TEMPERATURE_ANCHORS = (
    (-0.15, 12000.0),
    (0.05, 9500.0),
    (0.25, 7600.0),
    (0.45, 6500.0),
    (0.75, 5600.0),
    (1.15, 4500.0),
    (1.8, 3400.0),
    (2.4, 3000.0),
    (3.2, 2600.0),
    (4.2, 2200.0),
)
ACTIVE_V_MINUS_I_TEMPERATURE_ANCHORS = V_MINUS_I_TEMPERATURE_ANCHORS

EQ_TO_GAL = (
    (-0.0548755604162154, -0.8734370902348850, -0.4838350155487132),
    (0.4941094278755837, -0.4448296299600112, 0.7469822444972189),
    (-0.8676661490190047, -0.1980763734312015, 0.4559837761750669),
)
DEFAULT_VIEW_AXIS_ROTATION_DEGREES = 15.0

SPECTRAL_CLASSES = [
    {"id": "B", "label": "B / blue-white", "color": "#6f97ff", "range": "V-I < 0.05"},
    {"id": "A", "label": "A / white-blue", "color": "#80a4ff", "range": "0.05-0.25"},
    {"id": "F", "label": "F / cool white", "color": "#a5c1ff", "range": "0.25-0.45"},
    {"id": "G", "label": "G / near white", "color": "#e4eeff", "range": "0.45-0.75"},
    {"id": "K", "label": "K / warm white", "color": "#ffd697", "range": "0.75-1.15"},
    {"id": "M", "label": "M / amber", "color": "#ffac3e", "range": "V-I >= 1.15"},
]

LOCATION_INDEX = {"LMC": 0, "SMC": 1, "BRIDGE": 2, "MBR": 2, "OUT": 3}
MEAN_METALLICITY_FEH_BY_LOCATION = {
    "LMC": -0.4,
    "SMC": -0.7,
    "Bridge": -0.55,
    "Outer": -0.8,
}
DATASET_INDEX = {
    "cepheids": 0,
    "rrlyrae": 1,
    "anomalousCepheids": 2,
    "miras": 3,
}
CEPHEID_LIKE_DATASETS = {"cepheids", "anomalousCepheids"}
OGLE_ACEP_LMC_DISTANCE_KPC = 49.59
OGLE_ACEP_WESENHEIT_COEFFICIENT = 1.55
OGLE_ACEP_LMC_PL_WESENHEIT = {
    "F": (-2.960, 16.599),
    "1O": (-3.297, 16.041),
}
MIRA_CLOUD_DISTANCES_KPC = {
    "LMC": 49.59,
    "SMC": 62.44,
}
MIRA_CLOUD_DISTANCE_ERRORS_KPC = {
    "LMC": math.sqrt(0.09**2 + 0.54**2),
    "SMC": math.sqrt(0.47**2 + 0.81**2),
}
MIRA_DISTANCE_DIR = RAW / "mira_distances"
IWANEK2021_MIRA_TABLE = MIRA_DISTANCE_DIR / "iwanek2021_apj919_99_table3_mrt.txt"
LMC_MIRA_ALLWISE_XMATCH = MIRA_DISTANCE_DIR / "lmc_miras_allwise_xmatch.csv"
SMC_MIRA_ALLWISE_XMATCH = MIRA_DISTANCE_DIR / "smc_miras_allwise_xmatch.csv"
IWANEK2021_MIRA_TABLE_URL = "https://content.cld.iop.org/journals/0004-637X/919/2/99/revision1/apjac10c5t3_mrt.txt"
CDS_XMATCH_URL = "http://cdsxmatch.u-strasbg.fr/xmatch/api/v1/sync"
MIRA_EXTINCTION_AV_PER_EVI = 2.5
MIRA_MIDIR_EXTINCTION_AV = {
    "W1": 0.039,
    "W2": 0.026,
    "W3": 0.040,
    "S36": 0.037,
    "S45": 0.026,
    "S58": 0.019,
    "S80": 0.025,
}
MIRA_ALLWISE_MAG_ERROR_FLOOR = {
    "W1": 0.12,
    "W2": 0.12,
    "W3": 0.18,
}
MIRA_DISTANCE_VALID_RANGE_KPC = (20.0, 110.0)
MIRA_PLR_LOGP_PIVOT = 2.3
MIRA_PLR_O_RICH_LINEAR_LOGP_MAX = 2.6
MIRA_LOCAL_NEIGHBOR_K = 32
MIRA_LOCAL_NEIGHBOR_MIN_NEIGHBORS = 8
MIRA_LOCAL_NEIGHBOR_MAX_ANGULAR_DEG = 1.5
MIRA_LOCAL_NEIGHBOR_ERROR_FLOOR_KPC = 2.0
MIRA_PULSATION_FIT_VERSION = 3
MIRA_PULSATION_FITS_CACHE = PROCESSED / "mira_multiperiodic_fits_v3.json"
MIRA_TEMPERATURE_CACHE = PROCESSED / "mira_literature_temperatures_v1.json"
MIRA_TEMPERATURE_CACHE_VERSION = 1
MIRA_TEMPERATURE_MATCH_MAX_ARCSEC = 2.0
MIRA_LITERATURE_TEMPERATURE_RANGE_K = (1000, 5000)
MIRA_TEMPERATURE_SOURCES = (
    {
        "id": "jones2017_teff_mcd",
        "label": "Jones+2017 SAGE-Spec LMC TeffMcD",
        "url": "https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J%2FMNRAS%2F470%2F3250",
    },
    {
        "id": "ruffle2015_tmcd",
        "label": "Ruffle+2015 SAGE-Spec SMC Tmcd",
        "url": "https://vizier.unistra.fr/cgi-bin/VizieR-3?-source=J%2FMNRAS%2F451%2F3504",
    },
    {
        "id": "riebel2012_grams_teff",
        "label": "Riebel+2012 GRAMS LMC Teff",
        "url": "https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/ApJ/753/71?format=html&tex=true",
    },
    {
        "id": "iwanek2021_tstar",
        "label": "Iwanek+2021 Mira SED Tstar",
        "url": "https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J%2FApJS%2F257%2F23",
    },
)
MIRA_PULSATION_MIN_AMPLITUDE = 0.04
MIRA_PULSATION_MIN_POINTS = 20
MIRA_PULSATION_MIN_V_POINTS = 14
MIRA_PULSATION_FETCH_WORKERS = 16
MIRA_PULSATION_FIT_USER_AGENT = "mc-atlas-mira-pulsation/1.0"
MIRA_V_PRIOR_SOURCE = "learned-mira-v-prior-v1"
MIRA_V_PRIOR_ASSISTED_SOURCE = "ogle-lpv-v-multisine-prior-v1"
MIRA_V_PRIOR_MIN_SAMPLES = 18
MIRA_V_PRIOR_LOGP_SCALE = 0.22
MIRA_PLR_COEFFICIENTS = {
    "C": {
        "W1": {"a0": -7.471, "a0Err": 0.033, "a1": -4.198, "a1Err": 0.074, "a2": 0.0, "a2Err": 0.0, "scatter": 0.258},
        "W2": {"a0": -7.561, "a0Err": 0.038, "a1": -6.445, "a1Err": 0.094, "a2": 0.0, "a2Err": 0.0, "scatter": 0.326},
        "W3": {"a0": -7.932, "a0Err": 0.058, "a1": -9.040, "a1Err": 0.164, "a2": 0.0, "a2Err": 0.0, "scatter": 0.584},
        "S36": {"a0": -7.743, "a0Err": 0.037, "a1": -4.147, "a1Err": 0.091, "a2": 0.0, "a2Err": 0.0, "scatter": 0.344},
        "S45": {"a0": -7.702, "a0Err": 0.041, "a1": -5.780, "a1Err": 0.106, "a2": 0.0, "a2Err": 0.0, "scatter": 0.406},
        "S58": {"a0": -7.689, "a0Err": 0.047, "a1": -7.183, "a1Err": 0.130, "a2": 0.0, "a2Err": 0.0, "scatter": 0.494},
        "S80": {"a0": -7.786, "a0Err": 0.050, "a1": -8.329, "a1Err": 0.143, "a2": 0.0, "a2Err": 0.0, "scatter": 0.541},
    },
    "O_LINEAR": {
        "W1": {"a0": -7.249, "a0Err": 0.025, "a1": -3.807, "a1Err": 0.066, "a2": 0.0, "a2Err": 0.0, "scatter": 0.116},
        "W2": {"a0": -7.447, "a0Err": 0.027, "a1": -3.794, "a1Err": 0.096, "a2": 0.0, "a2Err": 0.0, "scatter": 0.170},
        "W3": {"a0": -8.226, "a0Err": 0.036, "a1": -3.900, "a1Err": 0.210, "a2": 0.0, "a2Err": 0.0, "scatter": 0.365},
        "S36": {"a0": -7.404, "a0Err": 0.027, "a1": -3.522, "a1Err": 0.103, "a2": 0.0, "a2Err": 0.0, "scatter": 0.236},
        "S45": {"a0": -7.507, "a0Err": 0.028, "a1": -3.290, "a1Err": 0.111, "a2": 0.0, "a2Err": 0.0, "scatter": 0.256},
        "S58": {"a0": -7.685, "a0Err": 0.028, "a1": -3.313, "a1Err": 0.111, "a2": 0.0, "a2Err": 0.0, "scatter": 0.254},
        "S80": {"a0": -7.882, "a0Err": 0.029, "a1": -3.473, "a1Err": 0.131, "a2": 0.0, "a2Err": 0.0, "scatter": 0.303},
    },
    "O_QUADRATIC": {
        "W1": {"a0": -7.224, "a0Err": 0.026, "a1": -3.749, "a1Err": 0.075, "a2": -1.810, "a2Err": 0.154, "scatter": 0.128},
        "W2": {"a0": -7.408, "a0Err": 0.027, "a1": -3.679, "a1Err": 0.102, "a2": -2.911, "a2Err": 0.207, "scatter": 0.173},
        "W3": {"a0": -8.142, "a0Err": 0.037, "a1": -3.459, "a1Err": 0.224, "a2": -6.107, "a2Err": 0.422, "scatter": 0.383},
        "S36": {"a0": -7.383, "a0Err": 0.028, "a1": -3.648, "a1Err": 0.115, "a2": -2.201, "a2Err": 0.239, "scatter": 0.267},
        "S45": {"a0": -7.477, "a0Err": 0.029, "a1": -3.430, "a1Err": 0.123, "a2": -2.895, "a2Err": 0.257, "scatter": 0.287},
        "S58": {"a0": -7.664, "a0Err": 0.029, "a1": -3.568, "a1Err": 0.128, "a2": -2.736, "a2Err": 0.256, "scatter": 0.300},
        "S80": {"a0": -7.837, "a0Err": 0.030, "a1": -4.037, "a1Err": 0.270, "a2": -4.363, "a2Err": 0.201, "scatter": 0.315},
    },
}
RECLASSIFIED_CLASSICAL_CEPHEIDS = {
    "OGLE-SMC-CEP-4957",
    "OGLE-LMC-CEP-3376",
    "OGLE-SMC-CEP-4954",
}
BRIDGE_ANOMALOUS_CEPHEIDS = {
    "OGLE-LMC-ACEP-084",
    "OGLE-LMC-ACEP-085",
    "OGLE-SMC-ACEP-100",
    "OGLE-SMC-ACEP-102",
    "OGLE-SMC-ACEP-104",
    "OGLE-SMC-ACEP-105",
    "OGLE-SMC-ACEP-106",
    "OGLE-SMC-ACEP-107",
    "OGLE-SMC-ACEP-108",
    "OGLE-SMC-ACEP-109",
    "OGLE-SMC-ACEP-120",
    "OGLE-LMC-ACEP-146",
    "OGLE-LMC-ACEP-147",
}
BRIDGE_ANOMALOUS_MANUAL_STARS = [
    {
        "id": "OGLE-GAL-ACEP-028",
        "mode": "F",
        "period": 1.1589986,
        "iMag": 15.892,
        "vMag": 16.350,
        "ra": "04:01:38.02",
        "dec": "-69:28:40.5",
        "distance": 28.18,
    },
]
COLOR_CURVE_SAMPLES = 96
COLOR_CURVE_QUALITY_SAMPLES = 512
COLOR_CURVE_SCALE = 100
COLOR_CURVE_ZERO = 64
LIGHT_CURVE_SCALE = 200
LIGHT_CURVE_ZERO = 128
LIGHT_CURVE_INT16_SCALE = 1000
COLOR_CURVE_VERSION = 17
PCA_FEATURE_SAMPLES = 1000
PCA_VARIANCE_TARGET = 0.99
PCA_MIN_BASIS_CURVES = 24
PCA_TRAINING_CSV = ROOT / "diagnostics" / "template_cv_chi2_i_gt200_v_gt40_gap010.csv"
TEMPLATE_FAMILY_FUNDAMENTAL = "FUNDAMENTAL"
TEMPLATE_FAMILY_FIRST_OVERTONE = "FIRST_OVERTONE"
PCA_FAMILIES = (TEMPLATE_FAMILY_FUNDAMENTAL, TEMPLATE_FAMILY_FIRST_OVERTONE)
PCA_FEATURE_CACHE_VERSION = 2
PCA_FEATURE_CACHE = PROCESSED / "pca_fourier_feature_cache_v2.npz"
PCA_FEATURE_CACHE_META = PROCESSED / "pca_fourier_feature_cache_v2.json"
PCA_TRAINING_SELECTION_OUT = PROCESSED / "pca_training_selection.json"
PCA_BASIS_COMPONENTS_OUT = PROCESSED / "pca_basis_components_v17.npz"
PCA_BASIS_SUMMARY_OUT = ROOT / "diagnostics" / "pca_basis_summary.json"
PCA_VALIDATION_OUT = ROOT / "diagnostics" / "pca_holdout_validation.csv"
PCA_STAR_DIAGNOSTICS_OUT = ROOT / "diagnostics" / "pca_star_fit_diagnostics.csv"
PCA_VALIDATION_FRACTION = 0.1
PCA_PHASE_OFFSET_LIMIT = 0.035
PCA_PHASE_OFFSET_STEPS = 15
PCA_PHASE_OFFSET_REFINE_STEP = 0.004
PCA_FEATURE_WORKERS = max(1, min(8, (os.cpu_count() or 2) - 1))
PCA_FEATURE_CHUNK_SIZE = 32
PCA_RAW_REJECTION_SIGMA = 3.5
PCA_RAW_REJECTION_ITERATIONS = 8
PCA_EMPIRICAL_PRIOR_BASE_STRENGTH = 0.004
PCA_EMPIRICAL_PRIOR_MAX_STRENGTH = 0.035
PCA_EMPIRICAL_PRIOR_MIN_SCALE = 0.045
PCA_EMPIRICAL_PRIOR_POWER = 1.15
FOURIER_PCA_MAX_HARMONICS = 14
FOURIER_PCA_CV_FOLDS = 4
FOURIER_PCA_LAPLACE_POWER = 1.75
FOURIER_PCA_LAPLACE_POWERS = (1.25, 1.75, 2.25)
FOURIER_PCA_LAPLACE_EPS = 0.035
FOURIER_PCA_LAPLACE_STRENGTHS = (0.0003, 0.001, 0.003, 0.01)
FOURIER_PCA_OPTIMIZER_ROUNDS = 6
FOURIER_PCA_STRENGTH_BOUNDS = (5e-5, 0.05)
FOURIER_PCA_POWER_BOUNDS = (0.8, 3.0)
COLOR_CURVE_CACHE = PROCESSED / "ogle_color_curves.json"
FIT_DIAGNOSTICS = ROOT / "diagnostics" / "color_fit_quality.json"
XMC_DENSITY_COUNTS = PROCESSED / "xmc_rc_density_counts.json"
XMC_DENSITY_SMOOTH_SIGMA_CELLS = 2.4
XMC_DENSITY_SMOOTH_RADIUS_CELLS = 8
REDDENING_DIR = RAW / "reddening"
SKOWRON_REDDENING_TSV = REDDENING_DIR / "skowron_2021_apjs252_23_table1.tsv"
HE_HUANG_LMC_GEOJSON = REDDENING_DIR / "lmc_partitions.geojson"
HE_HUANG_SMC_GEOJSON = REDDENING_DIR / "smc_partitions.geojson"
SKOWRON_REDDENING_SOURCE = "Skowron+2021"
HE_HUANG_REDDENING_SOURCE = "He&Huang2026"
NO_REDDENING_SOURCE = "none"
IMPUTED_NEAREST_REDDENING_SOURCE = "imputed:nearest"
IMPUTED_MEDIAN_REDDENING_SOURCE = "imputed:median"
SKOWRON_REDDENING_BIN_DEG = 0.25
SKOWRON_REDDENING_MAX_NEAREST_DEG = 1.0
IMPUTED_REDDENING_K = 32
IMPUTED_REDDENING_MIN_NEIGHBORS = 8
IMPUTED_REDDENING_MAX_DISTANCE_KPC = 8.0
IMPUTED_REDDENING_ERROR_FLOOR = 0.03
IMPUTED_MEDIAN_REDDENING_ERROR_FLOOR = 0.05
MIST_DIR = ROOT / "data" / "mist"
PERREN_CLUSTER_TABLE = RAW / "perren_vizier_clusters.dat"
PERREN_ASTECA_TABLE = RAW / "perren_asteca_output_final.dat"
MIST_CLUSTER_ISOCHRONE_CACHE = PROCESSED / "mist_cluster_isochrones_v1.npz"
MIST_CLUSTER_ISOCHRONE_CACHE_VERSION = 1
MIST_VI_TEMPERATURE_CACHE = PROCESSED / "mist_vi_temperature_calibration_v1.json"
MIST_VI_TEMPERATURE_CACHE_VERSION = 1
MIST_VI_TEMPERATURE_PHASE_MAX = 5
MIST_VI_TEMPERATURE_COLOR_MIN = -0.35
MIST_VI_TEMPERATURE_COLOR_MAX = 4.2
MIST_VI_TEMPERATURE_BIN_WIDTH = 0.05
MIST_VI_TEMPERATURE_MIN_BIN_COUNT = 5
MIST_VI_LUMINOSITY_TEMPERATURE_CACHE = PROCESSED / "mist_vi_luminosity_temperature_calibration_v1.json"
MIST_VI_LUMINOSITY_TEMPERATURE_CACHE_VERSION = 1
MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MIN = -2.0
MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MAX = 6.0
MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_STEP = 0.1
MIST_VI_LUMINOSITY_TEMPERATURE_VALUE_SCALE = 10000
CLUSTER_SYNTHETIC_MASS_CUTOFF = 0.5
CLUSTER_POINT_LUMINOSITY_CUTOFF = 1.0
CLUSTER_GLOW_BIN_COUNT = 12
CLUSTER_SPATIAL_RADIUS_CONTAINMENT_FRACTION = 0.82
CLUSTER_SPATIAL_TRUNCATION_RADIUS_MULTIPLIER = 3.0
CLUSTER_KING_MAX_TIDAL_RADIUS_MULTIPLIER = 8.0
CLUSTER_EFF_MAX_LOG_AGE = 8.5
CLUSTER_EFF_GAMMA = 2.7
CLUSTER_EFF_TRUNCATION_RADIUS_MULTIPLIER = 4.0
CLUSTER_DEFAULT_CORE_RADIUS_FRACTION = 0.33
CLUSTER_MIN_CORE_RADIUS_FRACTION = 0.04
CLUSTER_MAX_CORE_RADIUS_FRACTION = 0.85
CLUSTER_SPATIAL_CDF_GRID_SIZE = 2048
CLUSTER_HR_COLOR_MIN = -0.5
CLUSTER_HR_COLOR_MAX = 3.2
CLUSTER_HR_COLOR_BIN_COUNT = 64
CLUSTER_HR_LOG_LUMINOSITY_MIN = -2.0
CLUSTER_HR_LOG_LUMINOSITY_MAX = 6.0
CLUSTER_HR_LOG_LUMINOSITY_BIN_COUNT = 72
CLUSTER_IMF_MIN_MASS = 0.1
CLUSTER_IMF_MAX_MASS = 100.0
CLUSTER_IMF_GRID_SIZE = 18000
CLUSTER_ISOCHRONE_AGE_MIN = 5.0
CLUSTER_ISOCHRONE_AGE_STEP = 0.05
CLUSTER_ISOCHRONE_AGE_COUNT = 107
CLUSTER_ISOCHRONE_SAMPLE_OFFSETS = (-1.0, -0.5, 0.0, 0.5, 1.0)
CLUSTER_ISOCHRONE_UNCERTAINTY_SIGMA = 1.0
CLUSTER_RENDER_PHASE_MAX = 5

PHOTOMETRY_ARCHIVES = {
    ("LMC", "cepheids"): {
        "path": RAW / "ogle_photometry" / "lmc_cep_phot.tar.gz",
        "url": "https://www.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/cep/phot.tar.gz",
    },
    ("SMC", "cepheids"): {
        "path": RAW / "ogle_photometry" / "smc_cep_phot.tar.gz",
        "url": "https://www.astrouw.edu.pl/ogle/ogle4/OCVS/smc/cep/phot.tar.gz",
    },
    ("LMC", "rrlyrae"): {
        "path": RAW / "ogle_photometry" / "lmc_rrlyr_phot.tar.gz",
        "url": "https://www.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/rrlyr/phot.tar.gz",
    },
    ("SMC", "rrlyrae"): {
        "path": RAW / "ogle_photometry" / "smc_rrlyr_phot.tar.gz",
        "url": "https://www.astrouw.edu.pl/ogle/ogle4/OCVS/smc/rrlyr/phot.tar.gz",
    },
    ("LMC", "anomalousCepheids"): {
        "path": RAW / "ogle_photometry" / "lmc_acep_phot.tar.gz",
        "url": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/acep/phot.tar.gz",
    },
    ("SMC", "anomalousCepheids"): {
        "path": RAW / "ogle_photometry" / "smc_acep_phot.tar.gz",
        "url": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/acep/phot.tar.gz",
    },
}

CATALOG_SOURCE_FILES = {
    RAW / "ogle_params" / "lmc_acep" / "ident.dat": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/acep/ident.dat",
    RAW / "ogle_params" / "lmc_acep" / "acepF.dat": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/acep/acepF.dat",
    RAW / "ogle_params" / "lmc_acep" / "acep1O.dat": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/lmc/acep/acep1O.dat",
    RAW / "ogle_params" / "smc_acep" / "ident.dat": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/acep/ident.dat",
    RAW / "ogle_params" / "smc_acep" / "acepF.dat": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/acep/acepF.dat",
    RAW / "ogle_params" / "smc_acep" / "acep1O.dat": "https://ftp.astrouw.edu.pl/ogle/ogle4/OCVS/smc/acep/acep1O.dat",
    RAW / "ogle_lpv" / "lmc" / "ident.dat": "https://ftp.astrouw.edu.pl/ogle/ogle3/OIII-CVS/lmc/lpv/ident.dat",
    RAW / "ogle_lpv" / "lmc" / "Miras.dat": "https://ftp.astrouw.edu.pl/ogle/ogle3/OIII-CVS/lmc/lpv/Miras.dat",
    RAW / "ogle_lpv" / "smc" / "ident.dat": "https://ftp.astrouw.edu.pl/ogle/ogle3/OIII-CVS/smc/lpv/ident.dat",
    RAW / "ogle_lpv" / "smc" / "Miras.dat": "https://ftp.astrouw.edu.pl/ogle/ogle3/OIII-CVS/smc/lpv/Miras.dat",
    IWANEK2021_MIRA_TABLE: IWANEK2021_MIRA_TABLE_URL,
}


def photometry_archive_group(star: "CatalogStar") -> tuple[str, str] | None:
    if star.dataset not in {"cepheids", "rrlyrae", "anomalousCepheids"}:
        return None
    if star.obj_id.startswith("OGLE-LMC"):
        return ("LMC", star.dataset)
    if star.obj_id.startswith("OGLE-SMC"):
        return ("SMC", star.dataset)
    if star.location in {"LMC", "SMC"}:
        return (star.location, star.dataset)
    return None


@dataclass
class CatalogStar:
    dataset: str
    location: str
    obj_id: str
    period: float
    i_mag: float
    v_mag: float
    ra: float
    dec: float
    distance: float
    vector: tuple[float, float, float]
    distance_error: float | None = None
    distance_source: str | None = None
    age: float | None = None
    feh: float | None = None
    mode: str | None = None
    light_curve: dict[str, float | str] | None = None
    brightness_curve: str | None = None
    brightness_curve_quality: int = 0
    color_curve: str | None = None
    color_curve_quality: int = 0
    v_amplitude: float | None = None
    mira_pulsation: dict[str, object] | None = None
    mira_teff: int | None = None
    mira_teff_source_index: int | None = None
    reddening_evi: float = 0.0
    reddening_evi_error: float | None = None
    reddening_source: str = NO_REDDENING_SOURCE
    reddening_partition_id: int | None = None


@dataclass(frozen=True)
class ReddeningEstimate:
    evi: float
    error: float | None
    source: str
    partition_id: int | None = None


@dataclass
class ClusterParameters:
    name: str
    galaxy: str
    ra: float
    dec: float
    radius_pc: float
    feh: float
    e_feh: float
    log_age: float
    e_log_age: float
    ebv: float
    e_ebv: float
    mu0: float
    e_mu0: float
    mass: float
    e_mass: float
    ci: float | None = None
    prob_cl: float | None = None
    fc: int | None = None
    core_radius_pc: float | None = None
    tidal_radius_pc: float | None = None
    king_concentration: float | None = None
    quality_flags: str = "none"
    age_outlier: bool = False
    iso_specs: list[tuple[float, float, str]] | None = None


@dataclass
class MistIsochrone:
    feh: float
    log_age: float
    label: str
    initial_mass: np.ndarray
    star_mass: np.ndarray
    i_luminosity: np.ndarray
    radius: np.ndarray
    v_minus_i: np.ndarray
    temperature: np.ndarray
    spectral: np.ndarray


@dataclass(frozen=True)
class SkowronReddeningCell:
    ra: float
    dec: float
    evi: float
    error: float | None
    box_deg: float


@dataclass(frozen=True)
class HeHuangPartition:
    partition_id: int
    rings: tuple[tuple[tuple[float, float], ...], ...]
    bbox: tuple[float, float, float, float]
    a: float
    b: float
    a_err: float
    b_err: float
    mean_evi: float | None
    mean_evi_err: float | None


def hms_to_degrees(value: str) -> float:
    parts = [float(part) for part in value.split(":")]
    return (parts[0] + parts[1] / 60 + parts[2] / 3600) * 15


def dms_to_degrees(value: str) -> float:
    sign = -1 if value.strip().startswith("-") else 1
    clean = value.strip().lstrip("+-")
    parts = [float(part) for part in clean.split(":")]
    return sign * (parts[0] + parts[1] / 60 + parts[2] / 3600)


def mat_vec_mul(matrix: tuple[tuple[float, float, float], ...], vector: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(sum(row[i] * vector[i] for i in range(3)) for row in matrix)  # type: ignore[return-value]


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


def galactic_to_vector(lon_deg: float, lat_deg: float, distance: float) -> tuple[float, float, float]:
    lon = math.radians(lon_deg)
    lat = math.radians(lat_deg)
    return (
        distance * math.cos(lat) * math.cos(lon),
        distance * math.cos(lat) * math.sin(lon),
        distance * math.sin(lat),
    )


def vector_to_lon_lat(vector: tuple[float, float, float]) -> tuple[float, float]:
    radius = vector_length(vector)
    lon = math.degrees(math.atan2(vector[1], vector[0])) % 360
    lat = math.degrees(math.asin(vector[2] / radius))
    return lon, lat


def transpose_matrix(matrix: tuple[tuple[float, float, float], ...]) -> tuple[tuple[float, float, float], ...]:
    return tuple(tuple(matrix[row][column] for row in range(3)) for column in range(3))  # type: ignore[return-value]


def galactic_to_equatorial_vector(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    return mat_vec_mul(transpose_matrix(EQ_TO_GAL), vector)


def equatorial_vector_to_ra_dec(vector: tuple[float, float, float]) -> tuple[float, float]:
    radius = vector_length(vector)
    ra = math.degrees(math.atan2(vector[1], vector[0])) % 360
    dec = math.degrees(math.asin(vector[2] / radius))
    return ra, dec


def vector_length(vector: tuple[float, float, float]) -> float:
    return math.sqrt(sum(component * component for component in vector))


def spectral_index(v_minus_i: float) -> int:
    if v_minus_i < 0.05:
        return 0
    if v_minus_i < 0.25:
        return 1
    if v_minus_i < 0.45:
        return 2
    if v_minus_i < 0.75:
        return 3
    if v_minus_i < 1.15:
        return 4
    return 5


def luminosity_from_i(i_mag: float, distance_kpc: float) -> float:
    distance_modulus = 5 * math.log10(distance_kpc) + 10
    absolute_i = i_mag - distance_modulus
    return 10 ** (-0.4 * (absolute_i - M_SUN_I))


def temperature_from_v_minus_i_anchors(
    v_minus_i: float,
    anchors: tuple[tuple[float, float], ...] | list[tuple[float, float]],
) -> float:
    if v_minus_i <= anchors[0][0]:
        return anchors[0][1]
    for (left_color, left_temp), (right_color, right_temp) in zip(anchors, anchors[1:]):
        if v_minus_i <= right_color:
            fraction = (v_minus_i - left_color) / (right_color - left_color)
            log_left = math.log(left_temp)
            log_right = math.log(right_temp)
            return math.exp(log_left + fraction * (log_right - log_left))
    return anchors[-1][1]


def effective_temperature_from_v_minus_i(v_minus_i: float) -> float:
    # Approximate display temperature from intrinsic V-I; this is still only a
    # visual radius estimate, not a physical stellar-parameter fit.
    return temperature_from_v_minus_i_anchors(v_minus_i, ACTIVE_V_MINUS_I_TEMPERATURE_ANCHORS)


def set_v_minus_i_temperature_anchors(anchors: list[tuple[float, float]] | tuple[tuple[float, float], ...]) -> None:
    global ACTIVE_V_MINUS_I_TEMPERATURE_ANCHORS
    clean = tuple(
        (float(v_minus_i), float(temperature))
        for v_minus_i, temperature in anchors
        if math.isfinite(float(v_minus_i)) and math.isfinite(float(temperature)) and float(temperature) > 0
    )
    if len(clean) >= 2:
        ACTIVE_V_MINUS_I_TEMPERATURE_ANCHORS = tuple(sorted(clean, key=lambda item: item[0]))


def radius_from_luminosity_and_color(luminosity: float, v_minus_i: float) -> float:
    temperature = effective_temperature_from_v_minus_i(v_minus_i)
    return math.sqrt(max(luminosity, 0.001)) * (T_SUN / temperature) ** 2


def blackbody_lambda_ratio(temperature: float, wavelength_nm: float, reference_temperature: float = T_SUN) -> float:
    wavelength_m = wavelength_nm * 1e-9
    x = PLANCK_HC_OVER_K_M / (wavelength_m * max(temperature, 1.0))
    x_ref = PLANCK_HC_OVER_K_M / (wavelength_m * reference_temperature)
    if x > 700:
        return 0.0
    return math.expm1(x_ref) / math.expm1(x)


def i_band_luminosity_from_radius_temperature(radius_solar: float, temperature: float) -> float:
    return max(0.0, radius_solar) ** 2 * blackbody_lambda_ratio(temperature, BLACKBODY_I_NM)


def v_minus_i_from_temperature(temperature: float) -> float:
    v_ratio = blackbody_lambda_ratio(temperature, BLACKBODY_V_NM)
    i_ratio = blackbody_lambda_ratio(temperature, BLACKBODY_I_NM)
    sun_v_ratio = blackbody_lambda_ratio(T_SUN, BLACKBODY_V_NM)
    sun_i_ratio = blackbody_lambda_ratio(T_SUN, BLACKBODY_I_NM)
    if i_ratio <= 0 or sun_i_ratio <= 0 or v_ratio <= 0 or sun_v_ratio <= 0:
        return 2.5
    flux_ratio = (v_ratio / i_ratio) / (sun_v_ratio / sun_i_ratio)
    return clamp_float(SUN_V_MINUS_I - 2.5 * math.log10(flux_ratio), (-0.35, 3.0))


def valid_reddening_evi(value: float | None) -> bool:
    return value is not None and math.isfinite(value) and 0 <= value <= 1.0


def finite_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def angular_ra_delta_deg(left: float, right: float) -> float:
    return ((left - right + 180) % 360) - 180


def angular_distance_sq_deg(ra: float, dec: float, cell_ra: float, cell_dec: float) -> float:
    delta_ra = angular_ra_delta_deg(ra, cell_ra)
    delta_dec = dec - cell_dec
    cos_dec = math.cos(math.radians((dec + cell_dec) * 0.5))
    return (delta_ra * cos_dec) ** 2 + delta_dec**2


class SkowronReddeningMap:
    def __init__(self, cells: list[SkowronReddeningCell], bin_deg: float = SKOWRON_REDDENING_BIN_DEG):
        self.cells = cells
        self.bin_deg = bin_deg
        self.ra_bins = int(math.ceil(360 / bin_deg))
        self.bins: dict[tuple[int, int], list[SkowronReddeningCell]] = {}
        for cell in cells:
            self.bins.setdefault(self._bin_key(cell.ra, cell.dec), []).append(cell)

    @classmethod
    def from_tsv(cls, path: Path) -> "SkowronReddeningMap":
        cells: list[SkowronReddeningCell] = []
        if not path.exists():
            return cls(cells)

        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 11 or not parts[0].isdigit():
                continue
            try:
                box_arcmin = float(parts[1])
                ra = float(parts[2]) % 360
                dec = float(parts[3])
                evi = float(parts[4])
                lower_err = float(parts[5])
                upper_err = float(parts[6])
            except ValueError:
                continue
            if not valid_reddening_evi(evi):
                continue
            cells.append(
                SkowronReddeningCell(
                    ra=ra,
                    dec=dec,
                    evi=evi,
                    error=(lower_err + upper_err) * 0.5,
                    box_deg=box_arcmin / 60,
                )
            )
        return cls(cells)

    def _bin_key(self, ra: float, dec: float) -> tuple[int, int]:
        ra_bin = int(math.floor((ra % 360) / self.bin_deg)) % self.ra_bins
        dec_bin = int(math.floor((dec + 90) / self.bin_deg))
        return ra_bin, dec_bin

    def query(self, ra: float, dec: float) -> ReddeningEstimate | None:
        if not self.cells:
            return None

        ra_bin, dec_bin = self._bin_key(ra, dec)
        max_bin_radius = int(math.ceil(SKOWRON_REDDENING_MAX_NEAREST_DEG / self.bin_deg)) + 2
        best_cell: SkowronReddeningCell | None = None
        best_distance_sq = float("inf")

        for dx in range(-max_bin_radius, max_bin_radius + 1):
            for dy in range(-max_bin_radius, max_bin_radius + 1):
                for cell in self.bins.get(((ra_bin + dx) % self.ra_bins, dec_bin + dy), []):
                    distance_sq = angular_distance_sq_deg(ra, dec, cell.ra, cell.dec)
                    if distance_sq < best_distance_sq:
                        best_cell = cell
                        best_distance_sq = distance_sq

        if best_cell is None:
            return None

        max_allowed = max(SKOWRON_REDDENING_MAX_NEAREST_DEG, best_cell.box_deg * 1.5)
        if math.sqrt(best_distance_sq) > max_allowed:
            return None

        return ReddeningEstimate(
            evi=best_cell.evi,
            error=best_cell.error,
            source=SKOWRON_REDDENING_SOURCE,
        )


def point_on_segment(point: tuple[float, float], left: tuple[float, float], right: tuple[float, float]) -> bool:
    px, py = point
    x1, y1 = left
    x2, y2 = right
    cross = (px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)
    if abs(cross) > 1e-10:
        return False
    dot = (px - x1) * (px - x2) + (py - y1) * (py - y2)
    return dot <= 1e-10


def point_in_ring(point: tuple[float, float], ring: tuple[tuple[float, float], ...]) -> bool:
    x, y = point
    inside = False
    for left, right in zip(ring, ring[1:]):
        if point_on_segment(point, left, right):
            return True
        x1, y1 = left
        x2, y2 = right
        if (y1 > y) != (y2 > y):
            x_intersect = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x <= x_intersect:
                inside = not inside
    return inside


def polygon_contains(point: tuple[float, float], rings: tuple[tuple[tuple[float, float], ...], ...]) -> bool:
    if not rings or not point_in_ring(point, rings[0]):
        return False
    return not any(point_in_ring(point, ring) for ring in rings[1:])


class HeHuangReddeningMap:
    def __init__(self, partitions: list[HeHuangPartition]):
        self.partitions = partitions

    @classmethod
    def from_geojson_files(cls, paths: list[Path]) -> "HeHuangReddeningMap":
        partitions: list[HeHuangPartition] = []
        for path in paths:
            if not path.exists():
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            for feature in payload.get("features", []):
                geometry = feature.get("geometry", {})
                if geometry.get("type") != "Polygon":
                    continue
                coordinates = geometry.get("coordinates", [])
                rings: list[tuple[tuple[float, float], ...]] = []
                for ring in coordinates:
                    points = tuple((float(point[0]), float(point[1])) for point in ring)
                    if len(points) >= 4:
                        rings.append(points)
                if not rings:
                    continue

                props = feature.get("properties", {})
                a = finite_float(props.get("a"))
                b = finite_float(props.get("b"))
                a_err = finite_float(props.get("a_err"))
                b_err = finite_float(props.get("b_err"))
                partition_id = props.get("id")
                if a is None or b is None or a_err is None or b_err is None or partition_id is None:
                    continue

                all_points = [point for ring in rings for point in ring]
                ra_values = [point[0] for point in all_points]
                dec_values = [point[1] for point in all_points]
                partitions.append(
                    HeHuangPartition(
                        partition_id=int(partition_id),
                        rings=tuple(rings),
                        bbox=(min(ra_values), max(ra_values), min(dec_values), max(dec_values)),
                        a=a,
                        b=b,
                        a_err=a_err,
                        b_err=b_err,
                        mean_evi=finite_float(props.get("mean_evi")),
                        mean_evi_err=finite_float(props.get("mean_evi_err")),
                    )
                )
        return cls(partitions)

    def query(self, ra: float, dec: float, distance: float) -> ReddeningEstimate | None:
        normalized_ra = ra % 360
        query_points = [(normalized_ra, dec)]
        if normalized_ra > 180:
            query_points.append((normalized_ra - 360, dec))
        for partition in self.partitions:
            min_ra, max_ra, min_dec, max_dec = partition.bbox
            point = next(
                (
                    candidate
                    for candidate in query_points
                    if min_ra <= candidate[0] <= max_ra and min_dec <= candidate[1] <= max_dec
                ),
                None,
            )
            if point is None:
                continue
            if not polygon_contains(point, partition.rings):
                continue

            if partition.a < 0 and valid_reddening_evi(partition.mean_evi):
                evi = partition.mean_evi
                evi_err = partition.mean_evi_err
            else:
                evi = partition.a * distance + partition.b
                evi_err = math.sqrt((distance * partition.a_err) ** 2 + partition.b_err**2)

            if not valid_reddening_evi(evi):
                return None
            return ReddeningEstimate(
                evi=float(evi),
                error=float(evi_err) if evi_err is not None and math.isfinite(evi_err) else None,
                source=HE_HUANG_REDDENING_SOURCE,
                partition_id=partition.partition_id,
            )
        return None


def star_distance_sq_kpc(left: CatalogStar, right: CatalogStar) -> float:
    return sum((left.vector[index] - right.vector[index]) ** 2 for index in range(3))


def weighted_median(values: list[float], weights: list[float]) -> float:
    ordered = sorted(zip(values, weights), key=lambda item: item[0])
    half_weight = sum(weights) * 0.5
    cumulative = 0.0
    for value, weight in ordered:
        cumulative += weight
        if cumulative >= half_weight:
            return value
    return ordered[-1][0]


def robust_sigma(values: list[float], center: float | None = None) -> float:
    if len(values) < 2:
        return 0.0
    reference = center if center is not None else float(np.median(values))
    deviations = [abs(value - reference) for value in values]
    return 1.4826 * float(np.median(deviations))


def reddening_error_from_neighbors(
    values: list[float],
    errors: list[float | None],
    estimate: float,
    floor: float,
) -> float:
    finite_errors = [error for error in errors if error is not None and math.isfinite(error) and error >= 0]
    median_error = float(np.median(finite_errors)) if finite_errors else 0.0
    scatter = robust_sigma(values, estimate)
    return max(floor, math.sqrt(scatter**2 + median_error**2))


def impute_reddening(
    star: CatalogStar,
    direct_by_location: dict[str, list[CatalogStar]],
    median_by_location: dict[str, ReddeningEstimate],
) -> ReddeningEstimate | None:
    direct_neighbors = direct_by_location.get(star.location, [])
    neighbors: list[tuple[float, CatalogStar]] = []
    for neighbor in direct_neighbors:
        distance = math.sqrt(star_distance_sq_kpc(star, neighbor))
        if distance <= IMPUTED_REDDENING_MAX_DISTANCE_KPC:
            neighbors.append((distance, neighbor))

    neighbors.sort(key=lambda item: item[0])
    selected = neighbors[:IMPUTED_REDDENING_K]
    if len(selected) >= IMPUTED_REDDENING_MIN_NEIGHBORS:
        values = [neighbor.reddening_evi for _, neighbor in selected]
        errors = [neighbor.reddening_evi_error for _, neighbor in selected]
        weights = [1 / max(distance, 0.05) for distance, _ in selected]
        evi = weighted_median(values, weights)
        return ReddeningEstimate(
            evi=evi,
            error=reddening_error_from_neighbors(values, errors, evi, IMPUTED_REDDENING_ERROR_FLOOR),
            source=IMPUTED_NEAREST_REDDENING_SOURCE,
        )

    return median_by_location.get(star.location)


def assign_reddening(stars: list[CatalogStar]) -> dict[str, int | float | dict[str, int]]:
    skowron = SkowronReddeningMap.from_tsv(SKOWRON_REDDENING_TSV)
    he_huang = HeHuangReddeningMap.from_geojson_files([HE_HUANG_LMC_GEOJSON, HE_HUANG_SMC_GEOJSON])
    source_counts = {
        SKOWRON_REDDENING_SOURCE: 0,
        HE_HUANG_REDDENING_SOURCE: 0,
        IMPUTED_NEAREST_REDDENING_SOURCE: 0,
        IMPUTED_MEDIAN_REDDENING_SOURCE: 0,
        NO_REDDENING_SOURCE: 0,
    }
    direct_matches: list[CatalogStar] = []
    missing_matches: list[CatalogStar] = []

    for star in stars:
        estimate = skowron.query(star.ra, star.dec)
        override = he_huang.query(star.ra, star.dec, star.distance)
        if override is not None:
            estimate = override

        if estimate is None:
            star.reddening_evi = 0.0
            star.reddening_evi_error = None
            star.reddening_source = NO_REDDENING_SOURCE
            star.reddening_partition_id = None
            missing_matches.append(star)
        else:
            star.reddening_evi = estimate.evi
            star.reddening_evi_error = estimate.error
            star.reddening_source = estimate.source
            star.reddening_partition_id = estimate.partition_id
            direct_matches.append(star)

    direct_by_location: dict[str, list[CatalogStar]] = {}
    for star in direct_matches:
        direct_by_location.setdefault(star.location, []).append(star)

    median_by_location: dict[str, ReddeningEstimate] = {}
    for location, location_stars in direct_by_location.items():
        values = [star.reddening_evi for star in location_stars]
        errors = [star.reddening_evi_error for star in location_stars]
        median_evi = float(np.median(values))
        median_by_location[location] = ReddeningEstimate(
            evi=median_evi,
            error=reddening_error_from_neighbors(
                values,
                errors,
                median_evi,
                IMPUTED_MEDIAN_REDDENING_ERROR_FLOOR,
            ),
            source=IMPUTED_MEDIAN_REDDENING_SOURCE,
        )

    imputed_matches = 0
    for star in missing_matches:
        estimate = impute_reddening(star, direct_by_location, median_by_location)
        if estimate is None:
            continue
        star.reddening_evi = estimate.evi
        star.reddening_evi_error = estimate.error
        star.reddening_source = estimate.source
        star.reddening_partition_id = estimate.partition_id
        imputed_matches += 1

    values: list[float] = []
    for star in stars:
        if star.reddening_source != NO_REDDENING_SOURCE:
            values.append(star.reddening_evi)
        source_counts[star.reddening_source] = source_counts.get(star.reddening_source, 0) + 1

    return {
        "reddeningCorrectedStars": len(values),
        "reddeningMapMatchedStars": len(direct_matches),
        "reddeningImputedStars": imputed_matches,
        "reddeningMissingStars": source_counts.get(NO_REDDENING_SOURCE, 0),
        "reddeningSkowronCells": len(skowron.cells),
        "reddeningHeHuangPartitions": len(he_huang.partitions),
        "reddeningImputationK": IMPUTED_REDDENING_K,
        "reddeningImputationMinNeighbors": IMPUTED_REDDENING_MIN_NEIGHBORS,
        "reddeningImputationMaxDistanceKpc": IMPUTED_REDDENING_MAX_DISTANCE_KPC,
        "reddeningSourceCounts": source_counts,
        "reddeningMedianEVI": round_number(float(np.median(values)), 3) if values else 0.0,
        "reddeningMeanEVI": round_number(float(np.mean(values)), 3) if values else 0.0,
    }


def round_number(value: float, digits: int = 3) -> float:
    return round(value, digits)


def stable_unit_interval(value: str) -> float:
    digest = hashlib.sha1(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def stable_seed_int(value: str) -> int:
    digest = hashlib.blake2s(value.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest[:4], "big")


def percentile_span(values: np.ndarray, low: float = 5, high: float = 95) -> float:
    return float(np.percentile(values, high) - np.percentile(values, low))


def peak_to_peak(values: np.ndarray) -> float:
    return float(np.max(values) - np.min(values))


def max_phase_gap(phase: np.ndarray) -> float:
    if phase.size < 2:
        return 1.0
    ordered = np.sort(np.mod(phase, 1.0))
    gaps = np.diff(np.concatenate([ordered, [ordered[0] + 1.0]]))
    return float(np.max(gaps))


def periodic_distance(phase: np.ndarray, center: float) -> np.ndarray:
    return np.abs(((phase - center + 0.5) % 1.0) - 0.5)


def interpolate_periodic(sample_phase: np.ndarray, sample_values: np.ndarray, phase: np.ndarray) -> np.ndarray:
    if sample_phase.size == 0:
        return np.zeros_like(phase)
    if sample_phase.size == 1:
        return np.full_like(phase, float(sample_values[0]), dtype=float)
    order = np.argsort(sample_phase)
    ordered_phase = sample_phase[order]
    ordered_values = sample_values[order]
    extended_phase = np.concatenate([ordered_phase - 1.0, ordered_phase, ordered_phase + 1.0])
    extended_values = np.concatenate([ordered_values, ordered_values, ordered_values])
    return np.interp(np.mod(phase, 1.0), extended_phase, extended_values)


def carrier_sample_count(point_count: int) -> int:
    return int(min(COLOR_CURVE_SAMPLES, max(24, round(math.sqrt(max(point_count, 1)) * 4))))


def carrier_samples_from_folded(phase: np.ndarray, mag: np.ndarray, err: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None:
    if phase.size < 8:
        return None

    sample_count = carrier_sample_count(int(phase.size))
    centers = np.linspace(0, 1, sample_count, endpoint=False)
    target_points = 3 if phase.size < 80 else 5
    phases: list[float] = []
    mags: list[float] = []
    errs: list[float] = []
    counts: list[int] = []

    for center in centers:
        distance = periodic_distance(phase, float(center))
        if distance.size < target_points:
            continue
        sorted_distance = np.sort(distance)
        half_width = max(0.5 / sample_count, float(sorted_distance[target_points - 1]) * 1.05)
        half_width = min(0.09, half_width)
        mask = distance <= half_width
        if int(mask.sum()) < 2:
            continue

        local_mag = mag[mask]
        local_err = err[mask]
        local_keep = np.ones(local_mag.size, dtype=bool)
        for _ in range(4):
            kept_mag = local_mag[local_keep]
            if kept_mag.size < 2:
                break
            center_mag = float(np.median(kept_mag))
            mad = float(np.median(np.abs(kept_mag - center_mag)))
            median_error = float(np.median(np.clip(local_err[local_keep], 0.006, 0.25)))
            sigma = max(0.012, 1.4826 * mad, median_error)
            next_keep = np.abs(local_mag - center_mag) <= 4.0 * sigma
            if int(next_keep.sum()) < 2:
                break
            if np.array_equal(next_keep, local_keep):
                break
            local_keep = next_keep

        local_mag = local_mag[local_keep]
        local_err = local_err[local_keep]
        if local_mag.size < 2:
            continue

        median_mag = float(np.median(local_mag))
        mad = float(np.median(np.abs(local_mag - median_mag)))
        scatter = 1.4826 * mad
        count = int(local_mag.size)
        median_error = float(np.median(np.clip(local_err, 0.006, 0.25)))
        effective_error = max(0.012, scatter / math.sqrt(count), median_error / math.sqrt(count))
        phases.append(float(center))
        mags.append(median_mag)
        errs.append(effective_error)
        counts.append(count)

    if len(phases) < 8:
        return None
    return (
        np.asarray(phases, dtype=float),
        np.asarray(mags, dtype=float),
        np.asarray(errs, dtype=float),
        np.asarray(counts, dtype=int),
    )


def eclipse_mask_from_carrier(phase: np.ndarray, mag: np.ndarray, err: np.ndarray) -> tuple[np.ndarray, str | None]:
    carrier = carrier_samples_from_folded(phase, mag, err)
    if carrier is None:
        return np.ones(phase.size, dtype=bool), None

    carrier_phase, carrier_mag, _, _ = carrier
    local_carrier = interpolate_periodic(carrier_phase, carrier_mag, phase)
    residual = mag - local_carrier
    centered = residual - float(np.median(residual))
    p01, p16, p84, p99 = np.percentile(centered, [1, 16, 84, 99])
    central_span = float(p84 - p16)
    median_error = float(np.median(np.clip(err, 0.006, 0.25)))
    bright_tail = float(-p01)
    faint_tail = float(p99)
    threshold = max(0.16, central_span * 3.0, median_error * 10)
    dip_mask = centered > threshold
    dip_fraction = float(np.mean(dip_mask))

    if 0 < dip_fraction < 0.12 and faint_tail > max(0.24, bright_tail * 1.7, central_span * 3.0):
        return ~dip_mask, "eclipse-like residuals"
    return np.ones(phase.size, dtype=bool), None


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def parse_parameter_file(path: Path, subtype: str) -> dict[str, dict[str, float | str]]:
    rows: dict[str, dict[str, float | str]] = {}
    if not path.exists():
        return rows

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 11:
            continue

        period = parse_float(parts[3])
        period_error = parse_float(parts[4])
        t0 = parse_float(parts[5])
        amplitude = parse_float(parts[6])
        r21 = parse_float(parts[7])
        phi21 = parse_float(parts[8])
        r31 = parse_float(parts[9])
        phi31 = parse_float(parts[10])

        if None in (period, t0, amplitude, r21, phi21, r31, phi31):
            continue

        rows[parts[0]] = {
            "period": period,
            "periodError": period_error or 0.0,
            "t0": t0,
            "amplitude": amplitude,
            "r21": r21,
            "phi21": phi21,
            "r31": r31,
            "phi31": phi31,
            "subtype": subtype,
        }
    return rows


def load_light_curve_parameters() -> dict[str, dict[str, float | str]]:
    roots = {
        "lmc_cep": {
            "cepF.dat": "F",
            "cep1O.dat": "1O",
            "cep2O.dat": "2O",
            "cepF1O.dat": "F/1O",
            "cep1O2O.dat": "1O/2O",
            "cepF1O2O.dat": "F/1O/2O",
            "cep1O2O3O.dat": "1O/2O/3O",
            "cep1O3O.dat": "1O/3O",
            "cep2O3O.dat": "2O/3O",
        },
        "smc_cep": {
            "cepF.dat": "F",
            "cep1O.dat": "1O",
            "cep2O.dat": "2O",
            "cepF1O.dat": "F/1O",
            "cep1O2O.dat": "1O/2O",
            "cep1O2O3O.dat": "1O/2O/3O",
        },
        "lmc_rrlyr": {
            "RRab.dat": "RRab",
            "RRc.dat": "RRc",
            "RRd.dat": "RRd",
            "aRRd.dat": "aRRd",
        },
        "smc_rrlyr": {
            "RRab.dat": "RRab",
            "RRc.dat": "RRc",
            "RRd.dat": "RRd",
            "aRRd.dat": "aRRd",
        },
        "lmc_acep": {
            "acepF.dat": "F",
            "acep1O.dat": "1O",
        },
        "smc_acep": {
            "acepF.dat": "F",
            "acep1O.dat": "1O",
        },
    }

    parameters: dict[str, dict[str, float | str]] = {}
    base = RAW / "ogle_params"
    for folder, files in roots.items():
        for file_name, subtype in files.items():
            parameters.update(parse_parameter_file(base / folder / file_name, subtype))
    return parameters


def download_catalog_source_files() -> None:
    for path, url in CATALOG_SOURCE_FILES.items():
        if path.exists() and path.stat().st_size > 100:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(url, headers={"User-Agent": "mc-atlas-data-prep/1.0"})
        with urllib.request.urlopen(request, timeout=300) as response:
            path.write_bytes(response.read())


def download_photometry_archives() -> None:
    for archive in PHOTOMETRY_ARCHIVES.values():
        path = Path(archive["path"])
        if path.exists() and path.stat().st_size > 100:
            continue

        path.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(str(archive["url"]), headers={"User-Agent": "mc-atlas-data-prep/1.0"})
        with urllib.request.urlopen(request, timeout=900) as response:
            path.write_bytes(response.read())


def parse_photometry(raw: bytes) -> np.ndarray:
    values = np.fromstring(raw.decode("ascii", errors="ignore"), sep=" ", dtype=float)
    if values.size < 3:
        return np.empty((0, 3), dtype=float)
    values = values[: (values.size // 3) * 3].reshape(-1, 3)
    mask = np.isfinite(values).all(axis=1) & (values[:, 1] < 90) & (values[:, 2] > 0) & (values[:, 2] < 1)
    return values[mask]


def read_photometry_archive(path: Path, wanted_ids: set[str]) -> dict[str, dict[str, np.ndarray]]:
    photometry: dict[str, dict[str, np.ndarray]] = {}
    if not wanted_ids:
        return photometry

    with tarfile.open(path, "r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue
            parts = member.name.split("/")
            if len(parts) != 3 or parts[0] != "phot" or parts[1] not in {"V", "I"}:
                continue

            obj_id = Path(parts[2]).stem
            if obj_id not in wanted_ids:
                continue

            extracted = tar.extractfile(member)
            if extracted is None:
                continue
            data = parse_photometry(extracted.read())
            if data.size:
                photometry.setdefault(obj_id, {})[parts[1]] = data
    return photometry


def design_matrix(phase: np.ndarray, harmonics: int) -> np.ndarray:
    columns = [np.ones_like(phase)]
    for harmonic in range(1, harmonics + 1):
        angle = math.tau * harmonic * phase
        columns.append(np.cos(angle))
        columns.append(np.sin(angle))
    return np.column_stack(columns)


def weighted_fit(
    phase: np.ndarray,
    mag: np.ndarray,
    err: np.ndarray,
    harmonics: int,
    smoothness: float = 0.0,
    laplace_strength: float = 0.0,
    laplace_power: float = FOURIER_PCA_LAPLACE_POWER,
    laplace_epsilon: float = FOURIER_PCA_LAPLACE_EPS,
) -> tuple[np.ndarray, np.ndarray, float]:
    matrix = design_matrix(phase, harmonics)
    weights = 1 / np.clip(err, 0.006, 0.25) ** 2
    sqrt_weights = np.sqrt(weights)
    weighted_matrix_base = matrix * sqrt_weights[:, None]
    weighted_mag_base = mag * sqrt_weights
    penalty_scale = float(np.sum(weights) / max(1, len(weights)))

    def solve_with_penalties(coeffs_for_laplace: np.ndarray | None = None) -> np.ndarray:
        penalties = [0.0]
        for harmonic in range(1, harmonics + 1):
            ridge_penalty = float(harmonic**4) * smoothness
            laplace_penalty = 0.0
            if laplace_strength > 0 and coeffs_for_laplace is not None:
                cos_coeff = float(coeffs_for_laplace[2 * harmonic - 1])
                sin_coeff = float(coeffs_for_laplace[2 * harmonic])
                amplitude = math.sqrt(cos_coeff * cos_coeff + sin_coeff * sin_coeff + laplace_epsilon * laplace_epsilon)
                laplace_penalty = laplace_strength * float(harmonic**laplace_power) / amplitude
            penalties.extend([ridge_penalty + laplace_penalty, ridge_penalty + laplace_penalty])

        if any(penalty > 0 for penalty in penalties):
            penalty_matrix = np.diag(np.sqrt(np.asarray(penalties) * penalty_scale))
            weighted_matrix = np.vstack([weighted_matrix_base, penalty_matrix])
            weighted_mag = np.concatenate([weighted_mag_base, np.zeros(len(penalties))])
        else:
            weighted_matrix = weighted_matrix_base
            weighted_mag = weighted_mag_base
        solution, *_ = np.linalg.lstsq(weighted_matrix, weighted_mag, rcond=None)
        return solution

    coeffs = solve_with_penalties(None)
    if laplace_strength > 0:
        for _ in range(6):
            next_coeffs = solve_with_penalties(coeffs)
            if np.max(np.abs(next_coeffs - coeffs)) < 1e-5:
                coeffs = next_coeffs
                break
            coeffs = next_coeffs

    residual = mag - matrix @ coeffs
    rms = float(math.sqrt(np.average(residual**2, weights=weights)))
    return coeffs, residual, rms


def harmonic_cap_for_coverage(max_harmonics: int, n_points: int, phase_gap: float) -> int:
    cap = max_harmonics
    if n_points < 30:
        cap = min(cap, 2)
    elif n_points < 70:
        cap = min(cap, 3)
    elif n_points < 140:
        cap = min(cap, 4)
    if phase_gap > 0.28:
        cap = min(cap, 3)
    elif phase_gap > 0.22:
        cap = min(cap, 4)
    return max(1, cap)


def fit_band_curve(
    photometry: np.ndarray,
    period: float,
    t0: float,
    max_harmonics: int,
    smoothness: float = 0.0,
    rms_tolerance: float = 0.0,
    rms_relative_tolerance: float = 0.0,
    carrier: bool = False,
    mask_eclipses: bool = False,
) -> dict[str, object] | None:
    if photometry.shape[0] < 8 or not math.isfinite(period) or period <= 0:
        return None

    raw_phase = np.mod((photometry[:, 0] - t0) / period, 1.0)
    raw_mag = photometry[:, 1]
    raw_err = photometry[:, 2]
    order = np.argsort(raw_phase)
    raw_phase = raw_phase[order]
    raw_mag = raw_mag[order]
    raw_err = raw_err[order]

    eclipse_reason = None
    eclipse_mask = np.ones(raw_phase.size, dtype=bool)
    if mask_eclipses:
        eclipse_mask, eclipse_reason = eclipse_mask_from_carrier(raw_phase, raw_mag, raw_err)
    kept_phase = raw_phase[eclipse_mask]
    kept_mag = raw_mag[eclipse_mask]
    kept_err = raw_err[eclipse_mask]
    if kept_phase.size < 8:
        return None

    if carrier:
        carrier_samples = carrier_samples_from_folded(kept_phase, kept_mag, kept_err)
        if carrier_samples is None:
            return None
        phase, mag, err, carrier_counts = carrier_samples
    else:
        phase, mag, err = kept_phase, kept_mag, kept_err
        carrier_counts = np.ones_like(phase, dtype=int)

    order = np.argsort(phase)
    phase = phase[order]
    mag = mag[order]
    err = err[order]
    carrier_counts = carrier_counts[order]

    phase_bins = int(np.count_nonzero(np.histogram(kept_phase, bins=8, range=(0, 1))[0]))
    if phase_bins < 3:
        return None
    phase_gap = max_phase_gap(kept_phase)
    observed_span = percentile_span(kept_mag)

    best: dict[str, object] | None = None
    candidate_max = harmonic_cap_for_coverage(min(max_harmonics, max(1, (len(mag) - 3) // 4)), len(mag), phase_gap)
    candidates: list[dict[str, object]] = []
    for harmonics in range(1, candidate_max + 1):
        mask = np.ones(len(mag), dtype=bool)
        coeffs = np.zeros(2 * harmonics + 1)
        residual = np.zeros(len(mag))
        rms = math.inf

        for _ in range(4):
            coeffs, residual_masked, rms = weighted_fit(phase[mask], mag[mask], err[mask], harmonics, smoothness)
            residual = mag - design_matrix(phase, harmonics) @ coeffs
            center = float(np.median(residual[mask]))
            sigma = max(0.012, 1.4826 * float(np.median(np.abs(residual[mask] - center))))
            next_mask = np.abs(residual - center) <= 4.0 * sigma
            if next_mask.sum() < max(7, 2 * harmonics + 3):
                break
            if np.array_equal(next_mask, mask):
                break
            mask = next_mask

        n = int(mask.sum())
        if n < max(7, 2 * harmonics + 3):
            continue
        residual_fit = residual[mask]
        rss = float(np.sum(residual_fit**2))
        bic = n * math.log(max(rss / n, 1e-8)) + len(coeffs) * math.log(n)
        raw_residual = kept_mag - evaluate_curve(coeffs, kept_phase)
        raw_rms = float(np.sqrt(np.mean(raw_residual**2)))
        candidates.append(
            {
                "coeffs": coeffs,
                "harmonics": harmonics,
                "rms": rms,
                "rawRms": raw_rms,
                "n": int(kept_phase.size),
                "nTotal": int(raw_phase.size),
                "fitSamples": n,
                "fitPhase": phase.copy(),
                "fitMag": mag.copy(),
                "fitErr": err.copy(),
                "fitMask": mask.copy(),
                "carrier": carrier,
                "eclipseMasked": int(raw_phase.size - kept_phase.size),
                "eclipseReason": eclipse_reason,
                "phaseBins": phase_bins,
                "maxPhaseGap": phase_gap,
                "observedSpan": observed_span,
                "bic": bic,
            }
        )

    if not candidates:
        return None

    if rms_tolerance > 0 or rms_relative_tolerance > 0:
        best_rms = min(float(candidate["rms"]) for candidate in candidates)
        tolerance = max(rms_tolerance, best_rms * rms_relative_tolerance)
        eligible = [candidate for candidate in candidates if float(candidate["rms"]) <= best_rms + tolerance]
        return min(eligible, key=lambda candidate: (int(candidate["harmonics"]), float(candidate["bic"])))

    best = min(candidates, key=lambda candidate: float(candidate["bic"]))

    return best


def evaluate_curve(coeffs: np.ndarray, phase: np.ndarray) -> np.ndarray:
    harmonics = (len(coeffs) - 1) // 2
    return design_matrix(phase, harmonics) @ coeffs


def encode_color_curve(offsets: np.ndarray) -> str:
    quantized = np.rint(np.clip(offsets, -0.63, 0.63) * COLOR_CURVE_SCALE + COLOR_CURVE_ZERO).astype(np.uint8)
    return base64.b64encode(bytes(quantized)).decode("ascii")


def encode_light_curve(magnitude_offsets: np.ndarray) -> str:
    lower = np.iinfo(np.int16).min / LIGHT_CURVE_INT16_SCALE
    upper = np.iinfo(np.int16).max / LIGHT_CURVE_INT16_SCALE
    quantized = np.rint(np.clip(magnitude_offsets, lower, upper) * LIGHT_CURVE_INT16_SCALE).astype("<i2")
    return base64.b64encode(quantized.tobytes()).decode("ascii")


def decode_color_curve(encoded: str) -> np.ndarray:
    return (np.frombuffer(base64.b64decode(encoded), dtype=np.uint8).astype(float) - COLOR_CURVE_ZERO) / COLOR_CURVE_SCALE


def decode_light_curve(encoded: str) -> np.ndarray:
    return np.frombuffer(base64.b64decode(encoded), dtype="<i2").astype(float) / LIGHT_CURVE_INT16_SCALE


def v_amplitude_from_curve_fit(fit: dict[str, object]) -> float | None:
    if "iCurve" not in fit or "curve" not in fit:
        return None
    try:
        i_offsets = decode_light_curve(str(fit["iCurve"]))
        color_offsets = decode_color_curve(str(fit["curve"]))
    except (ValueError, TypeError):
        return None
    if i_offsets.shape != color_offsets.shape or i_offsets.size == 0:
        return None
    amplitude = peak_to_peak(i_offsets + color_offsets)
    return amplitude if math.isfinite(amplitude) and amplitude > 0 else None


def pulsation_mode(star: CatalogStar) -> str:
    if star.light_curve and "subtype" in star.light_curve:
        return str(star.light_curve["subtype"])
    return str(star.mode or "")


def max_template_harmonics(star: CatalogStar) -> int:
    mode = pulsation_mode(star)
    overtone = "1O" in mode or "2O" in mode or "RRc" in mode or "RRd" in mode
    if cepheid_like(star):
        return 3 if overtone else 4
    return 3 if overtone else 5


def template_family(star: CatalogStar) -> str:
    mode = pulsation_mode(star)
    if "RRc" in mode or "RRd" in mode:
        return TEMPLATE_FAMILY_FIRST_OVERTONE
    if "RRab" in mode or mode.startswith("F"):
        return TEMPLATE_FAMILY_FUNDAMENTAL
    if "1O" in mode or "2O" in mode:
        return TEMPLATE_FAMILY_FIRST_OVERTONE
    return TEMPLATE_FAMILY_FUNDAMENTAL


def curve_from_fit(fit: dict[str, object], phase: np.ndarray) -> np.ndarray:
    return evaluate_curve(fit["coeffs"], phase)  # type: ignore[arg-type]


def normalized_shape(values: np.ndarray) -> tuple[np.ndarray, float] | None:
    centered = values - float(np.mean(values))
    amplitude = percentile_span(centered)
    if not math.isfinite(amplitude) or amplitude < 0.025:
        return None
    return centered / amplitude, amplitude


def padded_coefficients(coeffs: np.ndarray, max_harmonics: int) -> np.ndarray:
    target = np.zeros(2 * max_harmonics + 1, dtype=float)
    target[: min(len(target), len(coeffs))] = coeffs[: min(len(target), len(coeffs))]
    target[0] = 0.0
    return target


def phase_stratified_folds(phase: np.ndarray, fold_count: int) -> np.ndarray:
    folds = np.zeros(len(phase), dtype=int)
    order = np.argsort(phase)
    folds[order] = np.arange(len(phase)) % fold_count
    return folds


def clamp_float(value: float, bounds: tuple[float, float]) -> float:
    return min(bounds[1], max(bounds[0], value))


def fit_fourier_coefficients_cv(
    phase: np.ndarray,
    values: np.ndarray,
    err: np.ndarray,
    max_harmonics: int = FOURIER_PCA_MAX_HARMONICS,
) -> dict[str, object] | None:
    if len(phase) < 14:
        return None

    fold_count = min(FOURIER_PCA_CV_FOLDS, max(2, len(phase) // 10))
    folds = phase_stratified_folds(phase, fold_count)
    fold_masks = [(folds != fold, folds == fold) for fold in range(fold_count)]
    score_cache: dict[tuple[int, int, int], tuple[float, float] | None] = {}
    candidates: list[dict[str, float | int]] = []
    harmonic_cap = min(max_harmonics, max(1, (len(phase) - 4) // 3))

    def cv_score(harmonics: int, laplace_strength: float, laplace_power: float) -> tuple[float, float] | None:
        strength = clamp_float(laplace_strength, FOURIER_PCA_STRENGTH_BOUNDS)
        power = clamp_float(laplace_power, FOURIER_PCA_POWER_BOUNDS)
        cache_key = (harmonics, int(round(math.log(strength) * 1_000_000)), int(round(power * 1_000_000)))
        if cache_key in score_cache:
            return score_cache[cache_key]

        fold_scores: list[float] = []
        for train, valid in fold_masks:
            if int(train.sum()) < max(8, 2 * harmonics + 4) or int(valid.sum()) == 0:
                continue
            coeffs, _, _ = weighted_fit(
                phase[train],
                values[train],
                err[train],
                harmonics,
                laplace_strength=strength,
                laplace_power=power,
            )
            residual = values[valid] - evaluate_curve(coeffs, phase[valid])
            weights = 1 / np.clip(err[valid], 0.02, 0.3) ** 2
            fold_scores.append(float(np.average(residual**2, weights=weights)))

        if len(fold_scores) < max(2, fold_count - 1):
            score_cache[cache_key] = None
            return None

        cv_mse = float(np.mean(fold_scores))
        cv_se = float(np.std(fold_scores, ddof=1) / math.sqrt(len(fold_scores))) if len(fold_scores) > 1 else 0.0
        score_cache[cache_key] = (cv_mse, cv_se)
        return score_cache[cache_key]

    for harmonics in range(1, harmonic_cap + 1):
        if len(phase) < 2 * harmonics + 6:
            continue
        for laplace_power in FOURIER_PCA_LAPLACE_POWERS:
            for laplace_strength in FOURIER_PCA_LAPLACE_STRENGTHS:
                score = cv_score(harmonics, laplace_strength, laplace_power)
                if score is None:
                    continue
                cv_mse, cv_se = score
                candidates.append(
                    {
                        "harmonics": harmonics,
                        "laplaceStrength": laplace_strength,
                        "laplacePower": laplace_power,
                        "cvMse": cv_mse,
                        "cvSe": cv_se,
                    }
                )

    if not candidates:
        return None

    best = min(candidates, key=lambda candidate: (float(candidate["cvMse"]), -int(candidate["harmonics"])))
    harmonics = int(best["harmonics"])
    grid_cv_mse = float(best["cvMse"])
    grid_cv_se = float(best["cvSe"])
    log_strength = math.log(float(best["laplaceStrength"]))
    laplace_power = float(best["laplacePower"])
    best_score = (grid_cv_mse, grid_cv_se)
    optimized = False
    log_bounds = (math.log(FOURIER_PCA_STRENGTH_BOUNDS[0]), math.log(FOURIER_PCA_STRENGTH_BOUNDS[1]))
    log_step = math.log(3.0)
    power_step = 0.35

    for _ in range(FOURIER_PCA_OPTIMIZER_ROUNDS):
        improved = False
        best_trial = (log_strength, laplace_power, best_score)
        for delta_log, delta_power in [
            (-log_step, 0.0),
            (log_step, 0.0),
            (0.0, -power_step),
            (0.0, power_step),
            (-log_step, -power_step),
            (-log_step, power_step),
            (log_step, -power_step),
            (log_step, power_step),
        ]:
            trial_log_strength = clamp_float(log_strength + delta_log, log_bounds)
            trial_power = clamp_float(laplace_power + delta_power, FOURIER_PCA_POWER_BOUNDS)
            score = cv_score(harmonics, math.exp(trial_log_strength), trial_power)
            if score is None:
                continue
            if score[0] < best_trial[2][0] - max(1e-8, best_trial[2][0] * 1e-4):
                best_trial = (trial_log_strength, trial_power, score)
                improved = True

        if improved:
            log_strength, laplace_power, best_score = best_trial
            optimized = True
        else:
            log_step *= 0.5
            power_step *= 0.5
            if log_step < 0.03 and power_step < 0.02:
                break

    laplace_strength = math.exp(log_strength)
    coeffs, residual, rms = weighted_fit(
        phase,
        values,
        err,
        harmonics,
        laplace_strength=laplace_strength,
        laplace_power=laplace_power,
    )
    return {
        "coeffs": padded_coefficients(coeffs, max_harmonics),
        "harmonics": harmonics,
        "laplaceStrength": laplace_strength,
        "laplacePower": laplace_power,
        "cvMse": float(best_score[0]),
        "cvSe": float(best_score[1]),
        "gridCvMse": grid_cv_mse,
        "gridCvSe": grid_cv_se,
        "optimized": optimized,
        "rms": rms,
    }


def fourier_pca_curve(coeffs: np.ndarray, phase: np.ndarray) -> np.ndarray:
    harmonics = (len(coeffs) - 1) // 2
    return evaluate_curve(coeffs, phase)


def pca_basis_at_phase(basis: dict[str, np.ndarray], phase: np.ndarray) -> np.ndarray:
    columns = [np.ones_like(phase)]

    if "coeffMean" in basis:
        columns.append(fourier_pca_curve(basis["coeffMean"], phase))
        for component in basis["coeffComponents"]:
            columns.append(fourier_pca_curve(component, phase))
        return np.column_stack(columns)

    columns.append(interpolate_periodic(basis["phase"], basis["mean"], phase))
    for component in basis["components"]:
        columns.append(interpolate_periodic(basis["phase"], component, phase))
    return np.column_stack(columns)


def fit_pca_samples(
    basis: dict[str, np.ndarray],
    phase: np.ndarray,
    mag: np.ndarray,
    err: np.ndarray,
    phase_shift: float = 0.0,
    prior_strength: float | None = None,
    use_prior: bool = True,
) -> tuple[np.ndarray, float] | None:
    if phase.size < 8:
        return None

    matrix = pca_basis_at_phase(basis, phase + phase_shift)
    finite = np.isfinite(matrix).all(axis=1) & np.isfinite(mag) & np.isfinite(err) & (err > 0)
    if int(finite.sum()) < 8:
        return None

    matrix = matrix[finite]
    mag = mag[finite]
    err = err[finite]
    weights = 1 / np.clip(err, 0.01, 0.25) ** 2
    sqrt_weights = np.sqrt(weights)
    weighted_matrix = matrix * sqrt_weights[:, None]
    weighted_mag = mag * sqrt_weights
    penalties = np.zeros(matrix.shape[1])
    if matrix.shape[1] > 2:
        component_order = np.arange(1, matrix.shape[1] - 1, dtype=float)
        penalty_scale = float(np.sum(weights) / max(1, len(weights)))
        penalties[2:] = 0.015 * (component_order**1.4) * penalty_scale
        weighted_matrix = np.vstack([weighted_matrix, np.diag(np.sqrt(penalties))])
        weighted_mag = np.concatenate([weighted_mag, np.zeros(matrix.shape[1])])

        if use_prior and prior_strength is not None and prior_strength > 0:
            prior_mean = basis.get("priorMean")
            prior_scale = basis.get("priorScale")
            if (
                isinstance(prior_mean, np.ndarray)
                and isinstance(prior_scale, np.ndarray)
                and prior_mean.shape[0] >= matrix.shape[1] - 2
                and prior_scale.shape[0] >= matrix.shape[1] - 2
            ):
                prior_mean = prior_mean[: matrix.shape[1] - 2]
                prior_scale = np.clip(prior_scale[: matrix.shape[1] - 2], PCA_EMPIRICAL_PRIOR_MIN_SCALE, None)
                order_weight = component_order**PCA_EMPIRICAL_PRIOR_POWER
                prior_rows = np.zeros((matrix.shape[1] - 2, matrix.shape[1]), dtype=float)
                prior_weight = np.sqrt(prior_strength * penalty_scale * order_weight) / prior_scale
                for index, weight in enumerate(prior_weight):
                    prior_rows[index, 1] = -prior_mean[index] * weight
                    prior_rows[index, index + 2] = weight
                weighted_matrix = np.vstack([weighted_matrix, prior_rows])
                weighted_mag = np.concatenate([weighted_mag, np.zeros(prior_rows.shape[0])])

    coeffs, *_ = np.linalg.lstsq(weighted_matrix, weighted_mag, rcond=None)
    residual = mag - matrix @ coeffs
    rms = float(math.sqrt(np.average(residual**2, weights=weights)))
    return coeffs, rms


def initial_phase_offset_grid() -> np.ndarray:
    return np.linspace(-PCA_PHASE_OFFSET_LIMIT, PCA_PHASE_OFFSET_LIMIT, PCA_PHASE_OFFSET_STEPS)


def local_phase_offset_grid(center: float) -> np.ndarray:
    offsets = np.asarray([center - PCA_PHASE_OFFSET_REFINE_STEP, center, center + PCA_PHASE_OFFSET_REFINE_STEP], dtype=float)
    return np.clip(offsets, -PCA_PHASE_OFFSET_LIMIT, PCA_PHASE_OFFSET_LIMIT)


def fit_pca_samples_with_phase_grid(
    basis: dict[str, np.ndarray],
    phase: np.ndarray,
    mag: np.ndarray,
    err: np.ndarray,
    phase_offsets: np.ndarray,
    prior_strength: float | None = None,
    use_prior: bool = True,
) -> tuple[np.ndarray, float, float] | None:
    best: tuple[np.ndarray, float, float] | None = None
    for phase_shift in phase_offsets:
        fit = fit_pca_samples(
            basis,
            phase,
            mag,
            err,
            float(phase_shift),
            prior_strength=prior_strength,
            use_prior=use_prior,
        )
        if fit is None:
            continue
        coeffs, rms = fit
        if best is None or rms < best[1]:
            best = (coeffs, rms, float(phase_shift))
    return best


def pca_fit_payload(
    basis: dict[str, np.ndarray],
    coeffs: np.ndarray,
    rms: float,
    raw_rms: float,
    raw_kept: int = 0,
    raw_rejected: int = 0,
    iterations: int = 0,
    phase_shift: float = 0.0,
    prior_strength: float = 0.0,
) -> dict[str, object]:
    dense_phase = np.linspace(0, 1, COLOR_CURVE_SAMPLES, endpoint=False)
    dense_model = pca_basis_at_phase(basis, dense_phase + phase_shift) @ coeffs
    quality_phase = np.linspace(0, 1, COLOR_CURVE_QUALITY_SAMPLES, endpoint=False)
    quality_model = pca_basis_at_phase(basis, quality_phase + phase_shift) @ coeffs
    component_count = int(basis.get("componentCount", np.asarray([len(basis.get("components", []))]))[0])
    return {
        "coeffs": coeffs,
        "rms": rms,
        "rawRms": raw_rms,
        "rawKept": raw_kept,
        "rawRejected": raw_rejected,
        "iterations": iterations,
        "phaseOffset": phase_shift,
        "pcaComponents": component_count,
        "priorStrength": prior_strength,
        "densePhase": dense_phase,
        "denseModel": dense_model,
        "qualityPhase": quality_phase,
        "qualityModel": quality_model,
        "source": "phase-pca99-empirical-prior" if prior_strength > 0 else "phase-pca99",
    }


def pca_prior_strength_from_fit(fit: dict[str, object]) -> float:
    fit_n = max(1, int(fit.get("n", 0)))
    gap = float(fit.get("maxPhaseGap", 1.0))
    observed_span = max(0.03, float(fit.get("observedSpan", 0.0)))
    rms = float(fit.get("rms", fit.get("rawRms", 0.0)))
    normalized_rms = rms / observed_span
    sparse_factor = clamp_float((120.0 / fit_n) ** 0.6, (0.35, 2.4))
    gap_factor = clamp_float(gap / 0.12, (0.35, 2.4))
    noise_factor = clamp_float(normalized_rms / 0.055, (0.5, 2.0))
    strength = PCA_EMPIRICAL_PRIOR_BASE_STRENGTH * sparse_factor * gap_factor * noise_factor
    return clamp_float(strength, (0.0, PCA_EMPIRICAL_PRIOR_MAX_STRENGTH))


def refine_pca_with_raw_photometry(
    basis: dict[str, np.ndarray],
    initial_coeffs: np.ndarray,
    initial_phase_shift: float,
    raw_photometry: np.ndarray,
    period: float,
    t0: float,
    prior_strength: float = 0.0,
) -> dict[str, object] | None:
    if raw_photometry.size == 0 or raw_photometry.shape[0] < 8:
        return None

    phase = np.mod((raw_photometry[:, 0] - t0) / period, 1.0)
    mag = raw_photometry[:, 1]
    err = raw_photometry[:, 2]
    finite = np.isfinite(phase) & np.isfinite(mag) & np.isfinite(err) & (err > 0)
    phase = phase[finite]
    mag = mag[finite]
    err = err[finite]
    if phase.size < 8:
        return None

    coeffs = initial_coeffs.copy()
    phase_shift = initial_phase_shift
    mask = np.ones(phase.size, dtype=bool)
    column_count = pca_basis_at_phase(basis, phase[:1]).shape[1]
    min_points = min(phase.size, max(8, min(column_count + 2, 24)))
    rms = math.inf
    iterations = 0

    for iteration in range(PCA_RAW_REJECTION_ITERATIONS):
        model = pca_basis_at_phase(basis, phase + phase_shift) @ coeffs
        residual = mag - model
        active_residual = residual[mask]
        if active_residual.size < min_points:
            break
        center = float(np.median(active_residual))
        mad = float(np.median(np.abs(active_residual - center)))
        median_error = float(np.median(np.clip(err[mask], 0.006, 0.25)))
        sigma = max(0.012, 1.4826 * mad, median_error)
        proposed_mask = mask & (np.abs(residual - center) <= PCA_RAW_REJECTION_SIGMA * sigma)
        if int(proposed_mask.sum()) < min_points:
            proposed_mask = mask

        fit = fit_pca_samples_with_phase_grid(
            basis,
            phase[proposed_mask],
            mag[proposed_mask],
            err[proposed_mask],
            local_phase_offset_grid(phase_shift),
            prior_strength=prior_strength,
        )
        if fit is None:
            break
        coeffs, rms, phase_shift = fit
        iterations = iteration + 1

        if np.array_equal(proposed_mask, mask):
            break
        mask = proposed_mask

    final_model = pca_basis_at_phase(basis, phase + phase_shift) @ coeffs
    final_residual = mag - final_model
    final_weights = 1 / np.clip(err, 0.01, 0.25) ** 2
    raw_rms = float(math.sqrt(np.average(final_residual**2, weights=final_weights)))
    if math.isinf(rms) and int(mask.sum()) >= 8:
        retained_weights = final_weights[mask]
        rms = float(math.sqrt(np.average(final_residual[mask] ** 2, weights=retained_weights)))

    return {
        "coeffs": coeffs,
        "rms": rms,
        "rawRms": raw_rms,
        "rawKept": int(mask.sum()),
        "rawRejected": int(phase.size - mask.sum()),
        "iterations": iterations,
        "phaseOffset": phase_shift,
    }


def fit_pca_carrier(
    fit: dict[str, object],
    basis: dict[str, np.ndarray],
    raw_photometry: np.ndarray | None = None,
    period: float | None = None,
    t0: float | None = None,
) -> dict[str, object] | None:
    phase = fit.get("fitPhase")
    mag = fit.get("fitMag")
    err = fit.get("fitErr")
    if not isinstance(phase, np.ndarray) or not isinstance(mag, np.ndarray) or not isinstance(err, np.ndarray):
        return None
    if phase.size < 8:
        return None
    fit_mask = fit.get("fitMask")
    if isinstance(fit_mask, np.ndarray) and fit_mask.shape == phase.shape and int(fit_mask.sum()) >= 8:
        keep = fit_mask.astype(bool)
        phase = phase[keep]
        mag = mag[keep]
        err = err[keep]

    prior_strength = pca_prior_strength_from_fit(fit)
    first_fit = fit_pca_samples_with_phase_grid(
        basis,
        phase,
        mag,
        err,
        initial_phase_offset_grid(),
        prior_strength=prior_strength,
    )
    if first_fit is None:
        return None

    coeffs, rms, phase_shift = first_fit
    raw_rms = float(fit.get("rawRms", rms))
    raw_kept = 0
    raw_rejected = 0
    iterations = 0

    if raw_photometry is not None and period is not None and t0 is not None:
        refined = refine_pca_with_raw_photometry(
            basis,
            coeffs,
            phase_shift,
            raw_photometry,
            period,
            t0,
            prior_strength=prior_strength,
        )
        if refined is not None:
            coeffs = refined["coeffs"]  # type: ignore[assignment]
            rms = float(refined["rms"])
            raw_rms = float(refined["rawRms"])
            raw_kept = int(refined["rawKept"])
            raw_rejected = int(refined["rawRejected"])
            iterations = int(refined["iterations"])
            phase_shift = float(refined["phaseOffset"])

    return pca_fit_payload(
        basis,
        coeffs,
        rms,
        raw_rms,
        raw_kept,
        raw_rejected,
        iterations,
        phase_shift,
        prior_strength=prior_strength,
    )


def safe_positive_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed) or parsed <= 0:
        return None
    return parsed


def load_pca_training_selection(stars: list[CatalogStar]) -> tuple[dict[str, set[str]], dict[str, object]]:
    stars_by_id = {star.obj_id: star for star in stars}
    selected_by_family: dict[str, set[str]] = {family: set() for family in PCA_FAMILIES}
    summary: dict[str, object] = {
        "source": str(PCA_TRAINING_CSV.relative_to(ROOT)) if PCA_TRAINING_CSV.exists() else None,
        "selection": "better-than-median combined log chi2 within the accepted 40/0.22 category groups",
        "priorGroups": {},
        "families": {family: {"selected": 0} for family in PCA_FAMILIES},
        "selectedTotal": 0,
    }
    if not PCA_TRAINING_CSV.exists():
        summary["selection"] = "fallback: all basis-eligible stars; accepted chi2 CSV was not found"
        return selected_by_family, summary

    grouped_scores: dict[str, list[tuple[str, float]]] = {}
    with PCA_TRAINING_CSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            obj_id = str(row.get("id", ""))
            star = stars_by_id.get(obj_id)
            if star is None:
                continue
            i_chi2 = safe_positive_float(str(row.get("i_cv_chi2", "")))
            v_chi2 = safe_positive_float(str(row.get("v_cv_chi2", "")))
            if i_chi2 is None or v_chi2 is None:
                continue
            prior_group = "/".join(
                [
                    str(row.get("location", star.location)),
                    str(row.get("dataset", star.dataset)),
                    str(row.get("family", template_family(star))),
                ]
            )
            combined = math.log(i_chi2) + math.log(v_chi2)
            grouped_scores.setdefault(prior_group, []).append((obj_id, combined))

    prior_group_summary: dict[str, dict[str, object]] = {}
    for prior_group, entries in sorted(grouped_scores.items()):
        scores = np.asarray([score for _, score in entries], dtype=float)
        median_score = float(np.median(scores))
        selected_entries = [(obj_id, score) for obj_id, score in entries if score < median_score]
        for obj_id, _ in selected_entries:
            family = template_family(stars_by_id[obj_id])
            selected_by_family.setdefault(family, set()).add(obj_id)
        prior_group_summary[prior_group] = {
            "scored": len(entries),
            "medianCombinedLogChi2": round_number(median_score, 4),
            "selected": len(selected_entries),
        }

    family_summary: dict[str, dict[str, int]] = {}
    for family in PCA_FAMILIES:
        family_summary[family] = {"selected": len(selected_by_family.get(family, set()))}
    summary["priorGroups"] = prior_group_summary
    summary["families"] = family_summary
    summary["selectedTotal"] = sum(item["selected"] for item in family_summary.values())
    return selected_by_family, summary


def pca_feature_signature(fit: dict[str, object]) -> str:
    fields = [
        PCA_FEATURE_CACHE_VERSION,
        PCA_FEATURE_SAMPLES,
        FOURIER_PCA_MAX_HARMONICS,
        FOURIER_PCA_CV_FOLDS,
        FOURIER_PCA_LAPLACE_POWERS,
        FOURIER_PCA_LAPLACE_STRENGTHS,
        int(fit.get("n", 0)),
        int(fit.get("nTotal", 0)),
        int(fit.get("harmonics", 0)),
        round_number(float(fit.get("maxPhaseGap", 0.0)), 6),
        round_number(float(fit.get("rms", 0.0)), 6),
        round_number(float(fit.get("rawRms", 0.0)), 6),
        round_number(float(fit.get("observedSpan", 0.0)), 6),
        int(fit.get("eclipseMasked", 0)),
    ]
    return hashlib.sha1(json.dumps(fields, sort_keys=True).encode("utf-8")).hexdigest()


def load_pca_feature_cache() -> dict[str, dict[str, object]]:
    if not PCA_FEATURE_CACHE.exists() or not PCA_FEATURE_CACHE_META.exists():
        return {}
    try:
        meta = json.loads(PCA_FEATURE_CACHE_META.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if meta.get("version") != PCA_FEATURE_CACHE_VERSION or meta.get("samples") != PCA_FEATURE_SAMPLES:
        return {}

    try:
        with np.load(PCA_FEATURE_CACHE, allow_pickle=False) as payload:
            ids = payload["ids"].astype(str)
            signatures = payload["signatures"].astype(str)
            shapes = payload["shapes"]
            harmonics = payload["harmonics"]
            optimized = payload["optimized"].astype(bool)
            cv_mse = payload["cvMse"] if "cvMse" in payload.files else np.full(len(ids), np.nan)
            laplace_strength = payload["laplaceStrength"] if "laplaceStrength" in payload.files else np.full(len(ids), np.nan)
            laplace_power = payload["laplacePower"] if "laplacePower" in payload.files else np.full(len(ids), np.nan)
    except Exception:
        return {}

    cache: dict[str, dict[str, object]] = {}
    for index, obj_id in enumerate(ids):
        cache[str(obj_id)] = {
            "shape": shapes[index],
            "signature": str(signatures[index]),
            "harmonics": int(harmonics[index]),
            "optimized": bool(optimized[index]),
            "cvMse": float(cv_mse[index]),
            "laplaceStrength": float(laplace_strength[index]),
            "laplacePower": float(laplace_power[index]),
        }
    return cache


def save_pca_feature_cache(features_by_id: dict[str, dict[str, object]]) -> None:
    if not features_by_id:
        return
    PROCESSED.mkdir(parents=True, exist_ok=True)
    ids = sorted(features_by_id)
    shapes = np.vstack([features_by_id[obj_id]["shape"] for obj_id in ids])  # type: ignore[list-item]
    np.savez_compressed(
        PCA_FEATURE_CACHE,
        ids=np.asarray(ids),
        signatures=np.asarray([features_by_id[obj_id]["signature"] for obj_id in ids]),
        shapes=shapes,
        harmonics=np.asarray([int(features_by_id[obj_id]["harmonics"]) for obj_id in ids], dtype=np.int16),
        optimized=np.asarray([bool(features_by_id[obj_id]["optimized"]) for obj_id in ids], dtype=bool),
        cvMse=np.asarray([float(features_by_id[obj_id].get("cvMse", math.nan)) for obj_id in ids], dtype=float),
        laplaceStrength=np.asarray([float(features_by_id[obj_id].get("laplaceStrength", math.nan)) for obj_id in ids], dtype=float),
        laplacePower=np.asarray([float(features_by_id[obj_id].get("laplacePower", math.nan)) for obj_id in ids], dtype=float),
    )
    meta = {
        "version": PCA_FEATURE_CACHE_VERSION,
        "samples": PCA_FEATURE_SAMPLES,
        "count": len(ids),
        "maxHarmonics": FOURIER_PCA_MAX_HARMONICS,
        "workers": PCA_FEATURE_WORKERS,
    }
    PCA_FEATURE_CACHE_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def pca_feature_from_fit(fit: dict[str, object], feature_phase: np.ndarray) -> dict[str, object] | None:
    fit_phase = fit.get("fitPhase")
    fit_mag = fit.get("fitMag")
    fit_err = fit.get("fitErr")
    if not isinstance(fit_phase, np.ndarray) or not isinstance(fit_mag, np.ndarray) or not isinstance(fit_err, np.ndarray):
        return None
    fit_mask = fit.get("fitMask")
    if isinstance(fit_mask, np.ndarray) and fit_mask.shape == fit_phase.shape and int(fit_mask.sum()) >= 8:
        keep = fit_mask.astype(bool)
        fit_phase = fit_phase[keep]
        fit_mag = fit_mag[keep]
        fit_err = fit_err[keep]

    normalized = normalized_shape(fit_mag)
    if normalized is None:
        return None
    _, amplitude = normalized
    centered = fit_mag - float(np.mean(fit_mag))
    cv_fit = fit_fourier_coefficients_cv(
        fit_phase,
        centered / amplitude,
        np.clip(fit_err / amplitude, 0.02, 0.3),
    )
    if cv_fit is not None:
        sampled = evaluate_curve(cv_fit["coeffs"], feature_phase)  # type: ignore[arg-type]
        harmonic_count = int(cv_fit["harmonics"])
        optimized = bool(cv_fit["optimized"])
        cv_mse = float(cv_fit["cvMse"])
        laplace_strength = float(cv_fit["laplaceStrength"])
        laplace_power = float(cv_fit["laplacePower"])
    else:
        sampled = curve_from_fit(fit, feature_phase)
        harmonic_count = int(fit.get("harmonics", 0))
        optimized = False
        cv_mse = math.nan
        laplace_strength = math.nan
        laplace_power = math.nan

    sampled_normalized = normalized_shape(sampled)
    if sampled_normalized is None:
        return None
    shape, _ = sampled_normalized
    return {
        "shape": shape,
        "harmonics": harmonic_count,
        "optimized": optimized,
        "cvMse": cv_mse,
        "laplaceStrength": laplace_strength,
        "laplacePower": laplace_power,
    }


def compute_pca_feature_chunk_worker(
    args: tuple[list[tuple[str, str, dict[str, object], str]], np.ndarray],
) -> list[tuple[str, dict[str, object] | None]]:
    jobs, feature_phase = args
    results: list[tuple[str, dict[str, object] | None]] = []
    for obj_id, family, fit, signature in jobs:
        feature = pca_feature_from_fit(fit, feature_phase)
        if feature is not None:
            feature["id"] = obj_id
            feature["family"] = family
            feature["signature"] = signature
        results.append((obj_id, feature))
    return results


def basis_from_feature_list(
    family: str,
    features: list[dict[str, object]],
    feature_phase: np.ndarray,
) -> tuple[dict[str, np.ndarray] | None, dict[str, object]]:
    family_info: dict[str, object] = {
        "usableTraining": len(features),
        "components": 0,
        "varianceExplained": 0.0,
        "medianHarmonics": None,
        "optimizedFraction": None,
    }
    if len(features) < PCA_MIN_BASIS_CURVES:
        return None, family_info

    matrix = np.vstack([feature["shape"] for feature in features])  # type: ignore[list-item]
    mean = np.mean(matrix, axis=0)
    centered = matrix - mean
    _, singular_values, vt = np.linalg.svd(centered, full_matrices=False)
    variance = singular_values**2
    variance_total = float(np.sum(variance))
    if variance_total <= 0 or not math.isfinite(variance_total):
        return None, family_info

    cumulative = np.cumsum(variance) / variance_total
    component_count = int(np.searchsorted(cumulative, PCA_VARIANCE_TARGET) + 1)
    component_count = max(1, min(component_count, vt.shape[0]))
    harmonics = [int(feature["harmonics"]) for feature in features]
    optimized = [bool(feature["optimized"]) for feature in features]
    basis = {
        "phase": feature_phase,
        "mean": mean,
        "components": vt[:component_count],
        "componentCount": np.asarray([component_count], dtype=int),
        "varianceExplained": np.asarray([float(cumulative[component_count - 1])]),
    }
    prior_coefficients: list[np.ndarray] = []
    projection_err = np.full(feature_phase.size, 0.02, dtype=float)
    for feature in features:
        shape = feature.get("shape")
        if not isinstance(shape, np.ndarray):
            continue
        fit = fit_pca_samples(basis, feature_phase, shape, projection_err, use_prior=False)
        if fit is None:
            continue
        coeffs, _ = fit
        if len(coeffs) < component_count + 2 or abs(float(coeffs[1])) < 1e-4:
            continue
        prior_coefficients.append(coeffs[2 : component_count + 2] / float(coeffs[1]))

    prior_summary: dict[str, object] | None = None
    if len(prior_coefficients) >= PCA_MIN_BASIS_CURVES:
        coefficient_matrix = np.vstack(prior_coefficients)
        prior_mean = np.median(coefficient_matrix, axis=0)
        prior_mad = 1.4826 * np.median(np.abs(coefficient_matrix - prior_mean), axis=0)
        robust_p16, robust_p84 = np.percentile(coefficient_matrix, [16, 84], axis=0)
        percentile_scale = 0.5 * (robust_p84 - robust_p16)
        prior_scale = np.maximum.reduce(
            [
                prior_mad,
                percentile_scale,
                np.full(component_count, PCA_EMPIRICAL_PRIOR_MIN_SCALE, dtype=float),
            ]
        )
        basis["priorMean"] = prior_mean
        basis["priorScale"] = prior_scale
        basis["priorCount"] = np.asarray([len(prior_coefficients)], dtype=int)
        prior_summary = {
            "count": len(prior_coefficients),
            "medianAbsMean": round_number(float(np.median(np.abs(prior_mean))), 5),
            "medianScale": round_number(float(np.median(prior_scale)), 5),
            "minScale": round_number(float(np.min(prior_scale)), 5),
            "maxScale": round_number(float(np.max(prior_scale)), 5),
        }
    family_info.update(
        {
            "usableTraining": len(features),
            "components": component_count,
            "varianceExplained": round_number(float(cumulative[component_count - 1]), 5),
            "medianHarmonics": round_number(float(np.median(harmonics)), 3),
            "optimizedFraction": round_number(float(np.mean(optimized)), 3),
            "coefficientPrior": prior_summary,
        }
    )
    return basis, family_info


def validate_pca_basis(
    family: str,
    basis: dict[str, np.ndarray] | None,
    holdout_features: list[dict[str, object]],
    feature_phase: np.ndarray,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    if basis is None or not holdout_features:
        return {"holdout": len(holdout_features), "medianRms": None, "p95Rms": None, "medianAmplitudeRatio": None}, []

    err = np.full(feature_phase.size, 0.02, dtype=float)
    rows: list[dict[str, object]] = []
    for feature in holdout_features:
        shape = feature["shape"]  # type: ignore[assignment]
        if not isinstance(shape, np.ndarray):
            continue
        fit = fit_pca_samples(basis, feature_phase, shape, err)
        if fit is None:
            continue
        coeffs, rms = fit
        model = pca_basis_at_phase(basis, feature_phase) @ coeffs
        amplitude_ratio = percentile_span(model) / max(percentile_span(shape), 1e-6)
        residual = shape - model
        rows.append(
            {
                "family": family,
                "id": str(feature.get("id", "")),
                "rms": rms,
                "p95AbsResidual": float(np.percentile(np.abs(residual), 95)),
                "amplitudeRatio": amplitude_ratio,
                "harmonics": int(feature.get("harmonics", 0)),
                "optimized": bool(feature.get("optimized", False)),
            }
        )

    if not rows:
        return {"holdout": len(holdout_features), "medianRms": None, "p95Rms": None, "medianAmplitudeRatio": None}, rows

    rms_values = np.asarray([float(row["rms"]) for row in rows], dtype=float)
    amplitude_ratios = np.asarray([float(row["amplitudeRatio"]) for row in rows], dtype=float)
    summary = {
        "holdout": len(holdout_features),
        "validated": len(rows),
        "medianRms": round_number(float(np.median(rms_values)), 5),
        "p95Rms": round_number(float(np.percentile(rms_values, 95)), 5),
        "medianAmplitudeRatio": round_number(float(np.median(amplitude_ratios)), 5),
        "p05AmplitudeRatio": round_number(float(np.percentile(amplitude_ratios, 5)), 5),
        "p95AmplitudeRatio": round_number(float(np.percentile(amplitude_ratios, 95)), 5),
    }
    return summary, rows


def write_pca_basis_components(bases: dict[str, dict[str, np.ndarray]]) -> None:
    if not bases:
        return
    PROCESSED.mkdir(parents=True, exist_ok=True)
    payload: dict[str, np.ndarray] = {}
    for family, basis in bases.items():
        payload[f"{family}_phase"] = basis["phase"]
        payload[f"{family}_mean"] = basis["mean"]
        payload[f"{family}_components"] = basis["components"]
        payload[f"{family}_varianceExplained"] = basis["varianceExplained"]
        if "priorMean" in basis and "priorScale" in basis:
            payload[f"{family}_priorMean"] = basis["priorMean"]
            payload[f"{family}_priorScale"] = basis["priorScale"]
            payload[f"{family}_priorCount"] = basis.get("priorCount", np.asarray([0], dtype=int))
    np.savez_compressed(PCA_BASIS_COMPONENTS_OUT, **payload)


def write_pca_validation_rows(rows: list[dict[str, object]]) -> None:
    PCA_VALIDATION_OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["family", "id", "rms", "p95AbsResidual", "amplitudeRatio", "harmonics", "optimized"]
    with PCA_VALIDATION_OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_pca_bases(
    stars: list[CatalogStar],
    i_fits: dict[str, dict[str, object]],
    training_ids_by_family: dict[str, set[str]],
) -> tuple[dict[str, dict[str, np.ndarray]], dict[str, object]]:
    feature_phase = np.linspace(0, 1, PCA_FEATURE_SAMPLES, endpoint=False)
    use_training_selection = any(training_ids_by_family.get(family) for family in PCA_FAMILIES)
    grouped_features: dict[str, list[dict[str, object]]] = {family: [] for family in PCA_FAMILIES}
    skipped: dict[str, int] = {"missingFit": 0, "notSelected": 0, "featureFailed": 0, "fallbackQuality": 0}
    feature_cache = load_pca_feature_cache()
    feature_jobs: list[tuple[str, str, dict[str, object], str]] = []

    for star in stars:
        family = template_family(star)
        if family not in grouped_features:
            continue
        if use_training_selection and star.obj_id not in training_ids_by_family.get(family, set()):
            skipped["notSelected"] += 1
            continue
        fit = i_fits.get(star.obj_id)
        if fit is None:
            skipped["missingFit"] += 1
            continue
        if not use_training_selection:
            fit_mag = fit.get("fitMag")
            if not isinstance(fit_mag, np.ndarray):
                skipped["fallbackQuality"] += 1
                continue
            normalized = normalized_shape(fit_mag)
            if normalized is None:
                skipped["fallbackQuality"] += 1
                continue
            _, amplitude = normalized
            score = float(fit.get("rawRms", fit["rms"])) / max(amplitude, 0.03)
            if int(fit["n"]) < 40 or float(fit["maxPhaseGap"]) > 0.22 or score > (0.32 if star.dataset == "rrlyrae" else 0.22):
                skipped["fallbackQuality"] += 1
                continue

        signature = pca_feature_signature(fit)
        cached_feature = feature_cache.get(star.obj_id)
        if cached_feature is not None and cached_feature.get("signature") == signature:
            feature = dict(cached_feature)
        else:
            feature_jobs.append((star.obj_id, family, fit, signature))
            continue
        feature["id"] = star.obj_id
        feature["family"] = family
        grouped_features[family].append(feature)

    computed_features = 0
    if feature_jobs:
        chunks = [
            feature_jobs[index : index + PCA_FEATURE_CHUNK_SIZE]
            for index in range(0, len(feature_jobs), PCA_FEATURE_CHUNK_SIZE)
        ]
        if __name__ == "__main__" and PCA_FEATURE_WORKERS > 1:
            with ProcessPoolExecutor(max_workers=PCA_FEATURE_WORKERS) as executor:
                futures = [executor.submit(compute_pca_feature_chunk_worker, (chunk, feature_phase)) for chunk in chunks]
                feature_results = (result for future in as_completed(futures) for result in future.result())
                for obj_id, feature in feature_results:
                    if feature is None:
                        skipped["featureFailed"] += 1
                        continue
                    family = str(feature["family"])
                    grouped_features[family].append(feature)
                    feature_cache[obj_id] = feature
                    computed_features += 1
        else:
            for chunk in chunks:
                for obj_id, feature in compute_pca_feature_chunk_worker((chunk, feature_phase)):
                    if feature is None:
                        skipped["featureFailed"] += 1
                        continue
                    family = str(feature["family"])
                    grouped_features[family].append(feature)
                    feature_cache[obj_id] = feature
                    computed_features += 1
        save_pca_feature_cache(feature_cache)

    bases: dict[str, dict[str, np.ndarray]] = {}
    validation_rows: list[dict[str, object]] = []
    summary: dict[str, object] = {
        "featureSamples": PCA_FEATURE_SAMPLES,
        "varianceTarget": PCA_VARIANCE_TARGET,
        "minimumBasisCurves": PCA_MIN_BASIS_CURVES,
        "trainingSelectionApplied": use_training_selection,
        "featureCache": {
            "path": str(PCA_FEATURE_CACHE.relative_to(ROOT)),
            "version": PCA_FEATURE_CACHE_VERSION,
            "workers": PCA_FEATURE_WORKERS,
            "hits": sum(len(features) for features in grouped_features.values()) - computed_features,
            "computed": computed_features,
        },
        "skipped": skipped,
        "families": {},
    }
    family_summary: dict[str, dict[str, object]] = {}

    for family in PCA_FAMILIES:
        features = grouped_features.get(family, [])
        selected_count = len(training_ids_by_family.get(family, set())) if use_training_selection else None
        holdout = [
            feature
            for feature in features
            if stable_unit_interval(f"pca-validation:{feature.get('id', '')}") < PCA_VALIDATION_FRACTION
        ]
        holdout_ids = {str(feature.get("id", "")) for feature in holdout}
        training = [feature for feature in features if str(feature.get("id", "")) not in holdout_ids]
        validation_basis, _ = basis_from_feature_list(family, training, feature_phase)
        validation_summary, rows = validate_pca_basis(family, validation_basis, holdout, feature_phase)
        validation_rows.extend(rows)

        basis, family_info = basis_from_feature_list(family, features, feature_phase)
        family_info["selectedTraining"] = selected_count
        family_info["validation"] = validation_summary
        if basis is not None:
            bases[family] = basis
        family_summary[family] = family_info

    summary["families"] = family_summary
    write_pca_basis_components(bases)
    write_pca_validation_rows(validation_rows)
    PCA_BASIS_SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    PCA_BASIS_SUMMARY_OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return bases, summary


def significant_extrema_count(values: np.ndarray) -> int:
    extrema: list[tuple[int, float]] = []
    for index, value in enumerate(values):
        previous_value = values[index - 1]
        next_value = values[(index + 1) % len(values)]
        if (value > previous_value and value > next_value) or (value < previous_value and value < next_value):
            extrema.append((index, float(value)))

    if len(extrema) <= 2:
        return len(extrema)

    span = peak_to_peak(values)
    min_prominence = max(0.025, span * 0.055)
    significant = 0
    for index, (_, value) in enumerate(extrema):
        previous_value = extrema[index - 1][1]
        next_value = extrema[(index + 1) % len(extrema)][1]
        if min(abs(value - previous_value), abs(value - next_value)) >= min_prominence:
            significant += 1
    return significant


def residual_diagnostics(photometry: np.ndarray, period: float, t0: float, fit: dict[str, object], model: np.ndarray) -> dict[str, float | bool | str]:
    phase = np.mod((photometry[:, 0] - t0) / period, 1.0)
    mag = photometry[:, 1]
    model_phase = np.linspace(0, 1, len(model), endpoint=False)
    residual = mag - interpolate_periodic(model_phase, model, phase)
    center = float(np.median(residual))
    centered = residual - center
    p01, p05, p10, p16, p84, p90, p95, p99 = np.percentile(centered, [1, 5, 10, 16, 84, 90, 95, 99])
    central_span = float(p84 - p16)
    mid_span = float(p90 - p10)
    broad_span = float(p95 - p05)
    model_span = percentile_span(model)
    median_error = float(np.median(np.clip(photometry[:, 2], 0.006, 0.25)))
    faint_tail = float(p99)
    bright_tail = float(-p01)
    dip_threshold = max(0.12, central_span * 2.75, median_error * 8)
    dip_fraction = float(np.mean(centered > dip_threshold))
    eclipse_like = bool(
        dip_fraction > 0
        and dip_fraction < 0.12
        and faint_tail > max(0.18, bright_tail * 1.8, central_span * 3.0, median_error * 10)
    )

    return {
        "centralSpan": central_span,
        "midSpan": mid_span,
        "broadSpan": broad_span,
        "faintTail": faint_tail,
        "brightTail": bright_tail,
        "dipFraction": dip_fraction,
        "medianError": median_error,
        "modelSpan": model_span,
        "eclipseLike": eclipse_like,
    }


def variability_flags_from_fit(
    fit: dict[str, object],
    diagnostics: dict[str, float | bool | str],
    pca_fit: dict[str, object] | None,
) -> list[str]:
    flags: list[str] = []
    n_total = int(fit.get("nTotal", fit.get("n", 0)))
    eclipse_masked = int(fit.get("eclipseMasked", 0))
    rejected_fraction = 0.0
    if pca_fit is not None:
        raw_kept = int(pca_fit.get("rawKept", 0))
        raw_rejected = int(pca_fit.get("rawRejected", 0))
        if raw_kept + raw_rejected > 0:
            rejected_fraction = raw_rejected / (raw_kept + raw_rejected)
        if abs(float(pca_fit.get("phaseOffset", 0.0))) > 0.02:
            flags.append("phase_offset")

    if bool(diagnostics.get("eclipseLike", False)) or eclipse_masked > max(2, int(0.01 * max(n_total, 1))):
        flags.append("eclipse_candidate")

    central_span = float(diagnostics.get("centralSpan", 0.0))
    broad_span = float(diagnostics.get("broadSpan", 0.0))
    model_span = float(diagnostics.get("modelSpan", 0.0))
    if (
        "eclipse_candidate" not in flags
        and rejected_fraction > 0.06
        and broad_span > max(0.10, central_span * 2.1, model_span * 0.18)
    ):
        flags.append("blazhko_candidate")

    return flags


def light_curve_rejection_reason(star: CatalogStar, fit: dict[str, object], model: np.ndarray, diagnostics: dict[str, float | bool | str]) -> str | None:
    model_span = float(diagnostics["modelSpan"])
    harmonics = int(fit["harmonics"])
    n = int(fit["n"])

    if model_span < 0.015 or not math.isfinite(model_span):
        return "flat carrier"
    if harmonics >= 4 and n < 80:
        return "underconstrained high-order fit"
    if int(fit.get("eclipseMasked", 0)) > max(20, int(0.18 * int(fit["nTotal"]))):
        return "too many eclipse-like points"

    return None


def quality_for_light_curve_fit(
    star: CatalogStar,
    i_fit: dict[str, object],
    i_model: np.ndarray,
    diagnostics: dict[str, float | bool | str],
) -> int:
    rms = float(i_fit["rms"])
    phase_bins = int(i_fit["phaseBins"])
    n = int(i_fit["n"])
    harmonics = int(i_fit["harmonics"])
    phase_gap = float(i_fit["maxPhaseGap"])
    observed_span = float(i_fit["observedSpan"])
    model_span = percentile_span(i_model)
    peak_span = peak_to_peak(i_model)
    extrema = significant_extrema_count(i_model)
    overfit = model_span > observed_span * 1.3 + 0.04
    mode = pulsation_mode(star)
    allowed_extrema = 4 if cepheid_like(star) or "RRab" in mode or mode == "" else 3

    if not math.isfinite(model_span) or model_span < 0.015 or peak_span > 2.4:
        return 0
    if phase_gap > 0.34 or phase_bins < 3 or n < 8:
        return 0
    if extrema > allowed_extrema:
        return 0
    if n < 40 and harmonics > 2:
        return 0
    if n < 90 and harmonics > 3:
        return 0
    if overfit and (n < 60 or harmonics >= 5):
        return 0
    if light_curve_rejection_reason(star, i_fit, i_model, diagnostics):
        return 0

    if cepheid_like(star):
        if n >= 80 and phase_bins >= 7 and rms <= 0.035 and phase_gap <= 0.16:
            return 3
        if n >= 32 and phase_bins >= 6 and rms <= 0.07 and phase_gap <= 0.24:
            return 2
        if n >= 12 and phase_bins >= 4 and rms <= 0.12:
            return 1
        return 0

    if n >= 120 and phase_bins >= 7 and rms <= 0.055 and phase_gap <= 0.18:
        return 3
    if n >= 36 and phase_bins >= 6 and rms <= 0.105 and phase_gap <= 0.26:
        return 2
    if n >= 12 and phase_bins >= 4 and rms <= 0.16:
        return 1
    return 0


def quality_for_color_fit(
    v_fit: dict[str, object],
    i_fit: dict[str, object],
    color_offsets: np.ndarray,
    catalog_color: float,
    v_model: np.ndarray,
    i_model: np.ndarray,
) -> int:
    v_rms = float(v_fit["rms"])
    i_rms = float(i_fit["rms"])
    color_span = percentile_span(color_offsets)
    color_peak = peak_to_peak(color_offsets)
    v_bins = int(v_fit["phaseBins"])
    i_bins = int(i_fit["phaseBins"])
    v_n = int(v_fit["n"])
    i_n = int(i_fit["n"])
    v_harmonics = int(v_fit["harmonics"])
    v_gap = float(v_fit["maxPhaseGap"])
    v_observed_span = float(v_fit["observedSpan"])
    v_model_span = percentile_span(v_model)
    v_overfit = v_model_span > v_observed_span * 1.25 + 0.05

    if not math.isfinite(catalog_color) or color_span > 0.66 or color_peak > 0.86 or color_span < 0.005:
        return 0
    if v_n < 12 and color_span > 0.45:
        return 0
    if v_n < 18 and color_span > 0.55:
        return 0
    if v_gap > 0.2 and color_span > 0.55:
        return 0
    if v_gap > 0.22 and v_harmonics >= 5:
        return 0
    if v_harmonics >= 5 and v_n < 35 and color_span > 0.55:
        return 0
    if v_overfit and color_span > 0.5:
        return 0
    if v_n >= 18 and i_n >= 40 and v_bins >= 6 and i_bins >= 7 and v_rms <= 0.055 and i_rms <= 0.045 and v_gap <= 0.18:
        return 3
    if v_n >= 12 and i_n >= 24 and v_bins >= 5 and i_bins >= 6 and v_rms <= 0.09 and i_rms <= 0.075:
        return 2
    if v_n >= 8 and i_n >= 14 and v_bins >= 4 and i_bins >= 4 and v_rms <= 0.16 and i_rms <= 0.13:
        return 1
    return 0


def fit_i_carrier_for_star(star: CatalogStar, photometry: dict[str, np.ndarray]) -> dict[str, object] | None:
    if star.light_curve is None or "I" not in photometry:
        return None

    period = float(star.light_curve.get("period", star.period))
    t0 = float(star.light_curve["t0"])
    max_harmonics = max_template_harmonics(star)
    return fit_band_curve(
        photometry["I"],
        period,
        t0,
        max_harmonics,
        smoothness=0.08 if cepheid_like(star) else 0.12,
        rms_tolerance=0.007 if cepheid_like(star) else 0.012,
        rms_relative_tolerance=0.12 if cepheid_like(star) else 0.18,
        carrier=True,
        mask_eclipses=True,
    )


def fit_color_curve_for_star(
    star: CatalogStar,
    photometry: dict[str, np.ndarray],
    i_fit: dict[str, object] | None = None,
    pca_basis: dict[str, np.ndarray] | None = None,
) -> dict[str, object] | None:
    if star.light_curve is None or "I" not in photometry:
        return None

    period = float(star.light_curve.get("period", star.period))
    t0 = float(star.light_curve["t0"])
    max_harmonics = max_template_harmonics(star)
    if i_fit is None:
        i_fit = fit_i_carrier_for_star(star, photometry)
    if i_fit is None:
        return None

    quality_phase = np.linspace(0, 1, COLOR_CURVE_QUALITY_SAMPLES, endpoint=False)
    pca_fit = fit_pca_carrier(i_fit, pca_basis, photometry["I"], period, t0) if pca_basis is not None else None
    quality_i_model = pca_fit["qualityModel"] if pca_fit is not None else curve_from_fit(i_fit, quality_phase)
    quality_i_fit = dict(i_fit)
    if pca_fit is not None:
        quality_i_fit["rms"] = float(pca_fit["rms"])
        quality_i_fit["rawRms"] = float(pca_fit["rawRms"])
    i_diagnostics = residual_diagnostics(photometry["I"], period, t0, quality_i_fit, quality_i_model)
    variability_flags = variability_flags_from_fit(quality_i_fit, i_diagnostics, pca_fit)
    rejection_reason = light_curve_rejection_reason(star, quality_i_fit, quality_i_model, i_diagnostics)
    if rejection_reason:
        return {
            "rejectReason": rejection_reason,
            "iRms": round_number(float(quality_i_fit["rms"]), 4),
            "iN": int(i_fit["n"]),
            "iH": int(i_fit["harmonics"]),
            "iSpan": round_number(percentile_span(quality_i_model), 4),
            "residualSpan": round_number(float(i_diagnostics["centralSpan"]), 4),
        }

    light_quality = quality_for_light_curve_fit(star, quality_i_fit, quality_i_model, i_diagnostics)
    if light_quality <= 0:
        return {
            "rejectReason": "failed quality gate",
            "iRms": round_number(float(quality_i_fit["rms"]), 4),
            "iN": int(i_fit["n"]),
            "iH": int(i_fit["harmonics"]),
            "iSpan": round_number(percentile_span(quality_i_model), 4),
            "residualSpan": round_number(float(i_diagnostics["centralSpan"]), 4),
        }

    phase = np.linspace(0, 1, COLOR_CURVE_SAMPLES, endpoint=False)
    i_model = pca_fit["denseModel"] if pca_fit is not None else curve_from_fit(i_fit, phase)
    i_offsets = i_model - float(np.mean(i_model))
    result: dict[str, object] = {
        "iCurve": encode_light_curve(i_offsets),
        "lightQuality": light_quality,
        "iRms": round_number(float(pca_fit["rms"] if pca_fit is not None else i_fit["rms"]), 4),
        "iN": int(i_fit["n"]),
        "iH": int(i_fit["harmonics"]),
        "iSpan": round_number(percentile_span(quality_i_model), 4),
        "iPeakSpan": round_number(peak_to_peak(quality_i_model), 4),
        "iExtrema": significant_extrema_count(quality_i_model),
        "residualSpan": round_number(float(i_diagnostics["centralSpan"]), 4),
        "rawRms": round_number(float(quality_i_fit["rawRms"]), 4),
        "eclipseMasked": int(i_fit.get("eclipseMasked", 0)),
        "templateSource": str(pca_fit["source"]) if pca_fit is not None else "carrier-harmonic",
        "variabilityFlags": variability_flags,
    }
    if pca_fit is not None:
        result.update(
            {
                "pcaComponents": int(pca_fit["pcaComponents"]),
                "pcaRawKept": int(pca_fit["rawKept"]),
                "pcaRawRejected": int(pca_fit["rawRejected"]),
                "pcaIterations": int(pca_fit["iterations"]),
                "pcaPhaseOffset": round_number(float(pca_fit["phaseOffset"]), 6),
                "pcaPriorStrength": round_number(float(pca_fit.get("priorStrength", 0.0)), 6),
            }
        )

    phase_offset = float(pca_fit.get("phaseOffset", 0.0)) if pca_fit is not None else 0.0
    if "V" in photometry:
        v_fit = fit_band_curve(
            photometry["V"],
            period,
            t0 - phase_offset * period,
            max_harmonics,
            smoothness=0.08 if cepheid_like(star) else 0.12,
            rms_tolerance=0.007 if cepheid_like(star) else 0.012,
            rms_relative_tolerance=0.12 if cepheid_like(star) else 0.18,
            carrier=True,
            mask_eclipses=True,
        )
        if v_fit is not None:
            quality_v_model = evaluate_curve(v_fit["coeffs"], quality_phase + phase_offset)  # type: ignore[arg-type]
            quality_color_curve = quality_v_model - quality_i_model
            quality_color_offsets = quality_color_curve - float(np.mean(quality_color_curve))
            catalog_color = star.v_mag - star.i_mag
            color_quality = quality_for_color_fit(v_fit, quality_i_fit, quality_color_offsets, catalog_color, quality_v_model, quality_i_model)
            if color_quality > 0:
                v_model = evaluate_curve(v_fit["coeffs"], phase + phase_offset)  # type: ignore[arg-type]
                color_curve = v_model - i_model
                color_offsets = color_curve - float(np.mean(color_curve))
                result.update(
                    {
                        "curve": encode_color_curve(color_offsets),
                        "quality": color_quality,
                        "vRms": round_number(float(v_fit["rms"]), 4),
                        "vN": int(v_fit["n"]),
                        "vH": int(v_fit["harmonics"]),
                        "span": round_number(percentile_span(quality_color_offsets), 4),
                        "peakSpan": round_number(peak_to_peak(quality_color_offsets), 4),
                        "vAmplitude": round_number(peak_to_peak(v_model), 4),
                        "sharedPhaseOffset": round_number(phase_offset, 6),
                    }
                )

    return result


def load_color_curve_cache() -> dict[str, dict[str, object]] | None:
    if not COLOR_CURVE_CACHE.exists():
        return None
    try:
        payload = json.loads(COLOR_CURVE_CACHE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if payload.get("version") != COLOR_CURVE_VERSION or payload.get("samples") != COLOR_CURVE_SAMPLES:
        return None
    return payload.get("curves", {})


def write_color_curve_cache(curves: dict[str, dict[str, object]], summary: dict[str, object]) -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": COLOR_CURVE_VERSION,
        "samples": COLOR_CURVE_SAMPLES,
        "scale": COLOR_CURVE_SCALE,
        "zero": COLOR_CURVE_ZERO,
        "lightEncoding": "int16le",
        "lightScale": LIGHT_CURVE_INT16_SCALE,
        "summary": summary,
        "curves": curves,
    }
    COLOR_CURVE_CACHE.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    FIT_DIAGNOSTICS.parent.mkdir(parents=True, exist_ok=True)
    FIT_DIAGNOSTICS.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def write_pca_star_diagnostics(rows: list[dict[str, object]]) -> None:
    PCA_STAR_DIAGNOSTICS_OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "location",
        "dataset",
        "family",
        "lightQuality",
        "colorQuality",
        "iRms",
        "rawRms",
        "iN",
        "iSpan",
        "pcaComponents",
        "pcaRawRejected",
        "pcaPhaseOffset",
        "pcaPriorStrength",
        "variabilityFlags",
    ]
    with PCA_STAR_DIAGNOSTICS_OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_color_curve_cache(stars: list[CatalogStar]) -> dict[str, dict[str, object]]:
    download_photometry_archives()
    curves: dict[str, dict[str, object]] = {}
    summary: dict[str, object] = {
        "version": COLOR_CURVE_VERSION,
        "samples": COLOR_CURVE_SAMPLES,
        "groups": {},
        "qualityCounts": {"1": 0, "2": 0, "3": 0},
        "lightQualityCounts": {"1": 0, "2": 0, "3": 0},
        "lightRejectionCounts": {},
        "variabilityFlagCounts": {},
        "fitCount": 0,
        "lightFitCount": 0,
        "missingOrRejected": 0,
        "missingLightOrRejected": 0,
    }

    grouped: dict[tuple[str, str], list[CatalogStar]] = {}
    for star in stars:
        group = photometry_archive_group(star)
        if group is not None:
            grouped.setdefault(group, []).append(star)

    group_photometry: dict[tuple[str, str], dict[str, dict[str, np.ndarray]]] = {}
    i_fits: dict[str, dict[str, object]] = {}
    for group, group_stars in grouped.items():
        archive = PHOTOMETRY_ARCHIVES[group]
        wanted = {star.obj_id for star in group_stars}
        photometry = read_photometry_archive(Path(archive["path"]), wanted)
        group_photometry[group] = photometry
        for star in group_stars:
            fit = fit_i_carrier_for_star(star, photometry.get(star.obj_id, {}))
            if fit is not None:
                i_fits[star.obj_id] = fit

    training_ids_by_family, training_summary = load_pca_training_selection([star for group_stars in grouped.values() for star in group_stars])
    PCA_TRAINING_SELECTION_OUT.parent.mkdir(parents=True, exist_ok=True)
    PCA_TRAINING_SELECTION_OUT.write_text(
        json.dumps(
            {
                "summary": training_summary,
                "idsByFamily": {family: sorted(training_ids_by_family.get(family, set())) for family in PCA_FAMILIES},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    pca_bases, pca_summary = build_pca_bases(
        [star for group_stars in grouped.values() for star in group_stars],
        i_fits,
        training_ids_by_family,
    )
    summary["pcaTrainingSelection"] = training_summary
    summary["pcaBases"] = pca_summary

    star_diagnostics: list[dict[str, object]] = []
    for group, group_stars in grouped.items():
        photometry = group_photometry.get(group, {})
        group_summary = {
            "stars": len(group_stars),
            "withPhotometry": len(photometry),
            "fit": 0,
            "lightFit": 0,
            "qualityCounts": {"1": 0, "2": 0, "3": 0},
            "lightQualityCounts": {"1": 0, "2": 0, "3": 0},
            "lightRejectionCounts": {},
            "variabilityFlagCounts": {},
            "medianVRms": None,
            "medianIRms": None,
            "medianColorSpan": None,
            "medianISpan": None,
        }
        v_rms_values: list[float] = []
        i_rms_values: list[float] = []
        span_values: list[float] = []
        i_span_values: list[float] = []

        for star in group_stars:
            basis = pca_bases.get(template_family(star))
            fit = fit_color_curve_for_star(star, photometry.get(star.obj_id, {}), i_fits.get(star.obj_id), basis)
            if fit is None:
                continue
            if "rejectReason" in fit:
                reason = str(fit["rejectReason"])
                group_rejections = group_summary["lightRejectionCounts"]  # type: ignore[assignment]
                summary_rejections = summary["lightRejectionCounts"]  # type: ignore[assignment]
                group_rejections[reason] = group_rejections.get(reason, 0) + 1
                summary_rejections[reason] = summary_rejections.get(reason, 0) + 1
                continue
            curves[star.obj_id] = fit
            light_quality_key = str(fit["lightQuality"])
            group_summary["lightQualityCounts"][light_quality_key] += 1  # type: ignore[index]
            summary["lightQualityCounts"][light_quality_key] += 1  # type: ignore[index]
            group_summary["lightFit"] += 1  # type: ignore[operator]
            summary["lightFitCount"] += 1  # type: ignore[operator]
            i_rms_values.append(float(fit["iRms"]))
            i_span_values.append(float(fit["iSpan"]))
            flags = [str(flag) for flag in fit.get("variabilityFlags", [])] if isinstance(fit.get("variabilityFlags", []), list) else []
            group_flags = group_summary["variabilityFlagCounts"]  # type: ignore[assignment]
            summary_flags = summary["variabilityFlagCounts"]  # type: ignore[assignment]
            for flag in flags:
                group_flags[flag] = group_flags.get(flag, 0) + 1
                summary_flags[flag] = summary_flags.get(flag, 0) + 1
            star_diagnostics.append(
                {
                    "id": star.obj_id,
                    "location": star.location,
                    "dataset": star.dataset,
                    "family": template_family(star),
                    "lightQuality": int(fit["lightQuality"]),
                    "colorQuality": int(fit.get("quality", 0)),
                    "iRms": fit["iRms"],
                    "rawRms": fit["rawRms"],
                    "iN": fit["iN"],
                    "iSpan": fit["iSpan"],
                    "pcaComponents": fit.get("pcaComponents", 0),
                    "pcaRawRejected": fit.get("pcaRawRejected", 0),
                    "pcaPhaseOffset": fit.get("pcaPhaseOffset", 0),
                    "pcaPriorStrength": fit.get("pcaPriorStrength", 0),
                    "variabilityFlags": "|".join(flags),
                }
            )

            if "quality" in fit:
                quality_key = str(fit["quality"])
                group_summary["qualityCounts"][quality_key] += 1  # type: ignore[index]
                summary["qualityCounts"][quality_key] += 1  # type: ignore[index]
                group_summary["fit"] += 1  # type: ignore[operator]
                summary["fitCount"] += 1  # type: ignore[operator]
                v_rms_values.append(float(fit["vRms"]))
                span_values.append(float(fit["span"]))

        if i_rms_values:
            group_summary["medianIRms"] = round_number(float(np.median(i_rms_values)), 4)
            group_summary["medianISpan"] = round_number(float(np.median(i_span_values)), 4)
        if v_rms_values:
            group_summary["medianVRms"] = round_number(float(np.median(v_rms_values)), 4)
            group_summary["medianColorSpan"] = round_number(float(np.median(span_values)), 4)
        summary["groups"][f"{group[0]}_{group[1]}"] = group_summary  # type: ignore[index]

    summary["missingOrRejected"] = len(stars) - int(summary["fitCount"])
    summary["missingLightOrRejected"] = len(stars) - int(summary["lightFitCount"])
    write_pca_star_diagnostics(star_diagnostics)
    write_color_curve_cache(curves, summary)
    return curves


def apply_color_curves(stars: list[CatalogStar]) -> dict[str, object]:
    curves = load_color_curve_cache()
    if curves is None:
        curves = build_color_curve_cache(stars)

    quality_counts = {"1": 0, "2": 0, "3": 0}
    light_quality_counts = {"1": 0, "2": 0, "3": 0}
    for star in stars:
        fit = curves.get(star.obj_id)
        if fit is None:
            continue
        if "iCurve" in fit:
            star.brightness_curve = str(fit["iCurve"])
            star.brightness_curve_quality = int(fit["lightQuality"])
            light_quality_counts[str(star.brightness_curve_quality)] += 1
        if "curve" in fit:
            star.color_curve = str(fit["curve"])
            star.color_curve_quality = int(fit["quality"])
            star.v_amplitude = finite_float(fit.get("vAmplitude")) or v_amplitude_from_curve_fit(fit)
            quality_counts[str(star.color_curve_quality)] += 1

    return {
        "fittedColorCurves": sum(quality_counts.values()),
        "colorCurveQuality": quality_counts,
        "colorCurveSamples": COLOR_CURVE_SAMPLES,
        "fittedBrightnessCurves": sum(light_quality_counts.values()),
        "brightnessCurveQuality": light_quality_counts,
        "brightnessCurveSamples": COLOR_CURVE_SAMPLES,
    }


def cepheid_like(star: CatalogStar) -> bool:
    return star.dataset in CEPHEID_LIKE_DATASETS


def anomalous_cepheid_distance(period: float, i_mag: float, v_mag: float, mode: str) -> float:
    pl_mode = "1O" if "1O" in mode else "F"
    slope, intercept = OGLE_ACEP_LMC_PL_WESENHEIT[pl_mode]
    observed_w = i_mag - OGLE_ACEP_WESENHEIT_COEFFICIENT * (v_mag - i_mag)
    lmc_w = slope * math.log10(period) + intercept
    return OGLE_ACEP_LMC_DISTANCE_KPC * (10 ** (0.2 * (observed_w - lmc_w)))


def parse_acep_ident(path: Path) -> dict[str, tuple[str, float, float]]:
    rows: dict[str, tuple[str, float, float]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        rows[parts[0]] = (parts[1], hms_to_degrees(parts[2]), dms_to_degrees(parts[3]))
    return rows


def parse_anomalous_cepheids() -> list[CatalogStar]:
    stars: list[CatalogStar] = []
    files = [
        ("LMC", RAW / "ogle_params" / "lmc_acep" / "ident.dat", RAW / "ogle_params" / "lmc_acep" / "acepF.dat", "F"),
        ("LMC", RAW / "ogle_params" / "lmc_acep" / "ident.dat", RAW / "ogle_params" / "lmc_acep" / "acep1O.dat", "1O"),
        ("SMC", RAW / "ogle_params" / "smc_acep" / "ident.dat", RAW / "ogle_params" / "smc_acep" / "acepF.dat", "F"),
        ("SMC", RAW / "ogle_params" / "smc_acep" / "ident.dat", RAW / "ogle_params" / "smc_acep" / "acep1O.dat", "1O"),
    ]
    ident_cache: dict[Path, dict[str, tuple[str, float, float]]] = {}
    seen: set[str] = set()

    for cloud, ident_path, data_path, file_mode in files:
        ident = ident_cache.setdefault(ident_path, parse_acep_ident(ident_path))
        for line in data_path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 11:
                continue
            obj_id = parts[0]
            i_mag = parse_float(parts[1])
            v_mag = parse_float(parts[2])
            period = parse_float(parts[3])
            if i_mag is None or v_mag is None or period is None:
                continue
            ident_row = ident.get(obj_id)
            if ident_row is None:
                continue
            mode, ra, dec = ident_row
            mode = mode or file_mode
            distance = anomalous_cepheid_distance(period, i_mag, v_mag, mode)
            location = "BRIDGE" if obj_id in BRIDGE_ANOMALOUS_CEPHEIDS else cloud
            stars.append(
                CatalogStar(
                    dataset="anomalousCepheids",
                    location=location,
                    obj_id=obj_id,
                    period=period,
                    i_mag=i_mag,
                    v_mag=v_mag,
                    ra=ra,
                    dec=dec,
                    distance=distance,
                    vector=equatorial_to_galactic_vector(ra, dec, distance),
                    mode=mode,
                )
            )
            seen.add(obj_id)

    for row in BRIDGE_ANOMALOUS_MANUAL_STARS:
        obj_id = str(row["id"])
        if obj_id in seen:
            continue
        ra = hms_to_degrees(str(row["ra"]))
        dec = dms_to_degrees(str(row["dec"]))
        distance = float(row["distance"])
        stars.append(
            CatalogStar(
                dataset="anomalousCepheids",
                location="OUT",
                obj_id=obj_id,
                period=float(row["period"]),
                i_mag=float(row["iMag"]),
                v_mag=float(row["vMag"]),
                ra=ra,
                dec=dec,
                distance=distance,
                vector=equatorial_to_galactic_vector(ra, dec, distance),
                mode=str(row["mode"]),
            )
        )

    return stars


def parse_lpv_ident(path: Path, cloud: str) -> dict[str, dict[str, str | float]]:
    rows: dict[str, dict[str, str | float]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if cloud == "LMC":
            obj_id = line[0:18].strip()
            subtype = line[37:42].strip()
            evolution = line[43:46].strip()
            chemistry = line[47:48].strip()
            ra_text = f"{line[50:52].strip()}:{line[53:55].strip()}:{line[56:61].strip()}"
            dec_text = f"{line[62:63].strip()}{line[63:65].strip()}:{line[66:68].strip()}:{line[69:73].strip()}"
            if not obj_id or not subtype or "::" in ra_text or "::" in dec_text:
                continue
        else:
            obj_id = line[0:18].strip()
            subtype = line[37:42].strip()
            evolution = ""
            chemistry = line[43:44].strip()
            ra_text = f"{line[46:48].strip()}:{line[49:51].strip()}:{line[52:57].strip()}"
            dec_text = f"{line[58:59].strip()}{line[59:61].strip()}:{line[62:64].strip()}:{line[65:69].strip()}"
            if not obj_id or not subtype or "::" in ra_text or "::" in dec_text:
                continue
        rows[obj_id] = {
            "subtype": subtype,
            "evolution": evolution,
            "chemistry": chemistry,
            "ra": hms_to_degrees(ra_text),
            "dec": dms_to_degrees(dec_text),
        }
    return rows


def chemistry_label(chemistry: str) -> str:
    if chemistry == "C":
        return "C-rich"
    if chemistry == "O":
        return "O-rich"
    return "unknown chemistry"


def stable_unit_interval(value: str) -> float:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def mira_component_payload(
    periods: list[float | None],
    amplitudes: list[float | None],
) -> dict[str, object]:
    component_periods: list[float] = []
    component_amplitudes: list[float] = []
    for period, amplitude in zip(periods, amplitudes):
        if period is None or amplitude is None:
            continue
        if not (math.isfinite(period) and math.isfinite(amplitude)):
            continue
        if period <= 0 or amplitude < MIRA_PULSATION_MIN_AMPLITUDE:
            continue
        component_periods.append(float(period))
        component_amplitudes.append(float(amplitude))
    return {
        "periods": component_periods,
        "amplitudesI": component_amplitudes,
        "phasesI": [],
        "quality": 0,
        "source": "ogle-lpv-catalog-components",
    }


def parse_miras_for_cloud(cloud: str, ident_path: Path, mira_path: Path) -> list[CatalogStar]:
    ident = parse_lpv_ident(ident_path, cloud)
    raw_rows: list[tuple[str, float, float | None, float, float, float | None, float | None, float | None, float | None, dict[str, str | float]]] = []
    color_samples: dict[str, list[float]] = {}
    for line in mira_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        obj_id = parts[0]
        ident_row = ident.get(obj_id)
        i_mag = parse_float(parts[1])
        v_mag = parse_float(parts[2])
        period = parse_float(parts[3])
        amplitude = parse_float(parts[4])
        period2 = parse_float(parts[5]) if len(parts) > 5 else None
        amplitude2 = parse_float(parts[6]) if len(parts) > 6 else None
        period3 = parse_float(parts[7]) if len(parts) > 7 else None
        amplitude3 = parse_float(parts[8]) if len(parts) > 8 else None
        if ident_row is None or i_mag is None or period is None or amplitude is None:
            continue
        raw_rows.append((obj_id, i_mag, v_mag, period, amplitude, period2, amplitude2, period3, amplitude3, ident_row))
        chemistry = str(ident_row.get("chemistry") or "")
        if v_mag is not None:
            color_samples.setdefault(chemistry, []).append(v_mag - i_mag)

    median_color = {
        chemistry: float(np.median(values))
        for chemistry, values in color_samples.items()
        if values
    }
    median_color.setdefault("O", 3.0)
    median_color.setdefault("C", 3.8)
    default_color = float(np.median([value for values in color_samples.values() for value in values])) if color_samples else 3.2
    distance = MIRA_CLOUD_DISTANCES_KPC[cloud]
    stars: list[CatalogStar] = []
    for obj_id, i_mag, v_mag, period, amplitude, period2, amplitude2, period3, amplitude3, ident_row in raw_rows:
        chemistry = str(ident_row.get("chemistry") or "")
        if v_mag is None:
            v_mag = i_mag + median_color.get(chemistry, default_color)
        ra = float(ident_row["ra"])
        dec = float(ident_row["dec"])
        mode = chemistry_label(chemistry)
        mira_pulsation = mira_component_payload(
            [period, period2, period3],
            [amplitude, amplitude2, amplitude3],
        )
        stars.append(
            CatalogStar(
                dataset="miras",
                location=cloud,
                obj_id=obj_id,
                period=period,
                i_mag=i_mag,
                v_mag=v_mag,
                ra=ra,
                dec=dec,
                distance=distance,
                vector=equatorial_to_galactic_vector(ra, dec, distance),
                mode=mode,
                light_curve={
                    "period": period,
                    "periodError": 0.0,
                    "t0": stable_unit_interval(f"{obj_id}-mira-phase") * period,
                    "amplitude": amplitude,
                    "r21": 0.0,
                    "phi21": 0.0,
                    "r31": 0.0,
                    "phi31": 0.0,
                    "subtype": f"Mira {mode}",
                },
                mira_pulsation=mira_pulsation,
            )
        )
    return stars


def parse_miras() -> list[CatalogStar]:
    return parse_miras_for_cloud(
        "LMC",
        RAW / "ogle_lpv" / "lmc" / "ident.dat",
        RAW / "ogle_lpv" / "lmc" / "Miras.dat",
    ) + parse_miras_for_cloud(
        "SMC",
        RAW / "ogle_lpv" / "smc" / "ident.dat",
        RAW / "ogle_lpv" / "smc" / "Miras.dat",
    )


def source_index_for_mira_temperature(source_id: str) -> int:
    for index, source in enumerate(MIRA_TEMPERATURE_SOURCES):
        if source["id"] == source_id:
            return index
    raise KeyError(source_id)


def valid_mira_literature_temperature(value: object) -> int | None:
    temperature = finite_float(value)
    if temperature is None:
        return None
    lower, upper = MIRA_LITERATURE_TEMPERATURE_RANGE_K
    if not (lower <= temperature <= upper):
        return None
    return int(round(temperature))


def fetch_vizier_tsv_rows(source: str, columns: str) -> list[dict[str, str]]:
    params = {
        "-source": source,
        "-out": columns,
        "-out.max": "unlimited",
    }
    url = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "mc-atlas-data-prep/1.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        text = response.read().decode("utf-8", errors="replace")

    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    if not lines:
        return []

    header = lines[0].split("\t")
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        cells = line.split("\t")
        if len(cells) != len(header):
            continue
        if all(not cell.strip() or set(cell.strip()) <= {"-"} for cell in cells):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def add_exact_mira_temperature_estimate(
    estimates: dict[str, dict[str, int]],
    obj_id: str,
    temperature: int | None,
    source_index: int,
) -> None:
    if temperature is None or not obj_id:
        return
    estimates.setdefault(obj_id, {"teff": temperature, "sourceIndex": source_index})


def mira_temperature_position_buckets(
    stars: list[CatalogStar],
    bucket_arcsec: float = 10.0,
) -> dict[tuple[int, int], list[CatalogStar]]:
    buckets: dict[tuple[int, int], list[CatalogStar]] = {}
    for star in stars:
        key = (int(star.ra * 3600.0 // bucket_arcsec), int(star.dec * 3600.0 // bucket_arcsec))
        buckets.setdefault(key, []).append(star)
    return buckets


def add_coordinate_mira_temperature_estimates(
    estimates: dict[str, dict[str, int]],
    stars: list[CatalogStar],
    rows: list[dict[str, str]],
    source_index: int,
    temperature_column: str,
    ra_column: str = "_RA",
    dec_column: str = "_DE",
) -> None:
    buckets = mira_temperature_position_buckets(stars)
    bucket_arcsec = 10.0
    max_distance_deg = MIRA_TEMPERATURE_MATCH_MAX_ARCSEC / 3600.0
    best_by_star: dict[str, tuple[float, int]] = {}
    for row in rows:
        temperature = valid_mira_literature_temperature(row.get(temperature_column))
        ra = finite_float(row.get(ra_column))
        dec = finite_float(row.get(dec_column))
        if temperature is None or ra is None or dec is None:
            continue

        key = (int(ra * 3600.0 // bucket_arcsec), int(dec * 3600.0 // bucket_arcsec))
        for delta_ra in range(-1, 2):
            for delta_dec in range(-1, 2):
                for star in buckets.get((key[0] + delta_ra, key[1] + delta_dec), []):
                    distance_sq = angular_distance_sq_deg(star.ra, star.dec, ra, dec)
                    if distance_sq > max_distance_deg**2:
                        continue
                    best = best_by_star.get(star.obj_id)
                    if best is None or distance_sq < best[0]:
                        best_by_star[star.obj_id] = (distance_sq, temperature)

    for obj_id, (_, temperature) in best_by_star.items():
        if obj_id not in estimates:
            estimates[obj_id] = {"teff": temperature, "sourceIndex": source_index}


def build_mira_literature_temperature_lookup(miras: list[CatalogStar]) -> dict[str, dict[str, int]]:
    if MIRA_TEMPERATURE_CACHE.exists():
        try:
            cached = json.loads(MIRA_TEMPERATURE_CACHE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            cached = None
        if (
            isinstance(cached, dict)
            and cached.get("version") == MIRA_TEMPERATURE_CACHE_VERSION
            and isinstance(cached.get("estimates"), dict)
        ):
            return cached["estimates"]

    estimates: dict[str, dict[str, int]] = {}
    lmc_miras = [star for star in miras if star.location == "LMC"]

    jones_index = source_index_for_mira_temperature("jones2017_teff_mcd")
    for row in fetch_vizier_tsv_rows("J/MNRAS/470/3250/table2", "OGLE3ID,TeffMcD"):
        obj_id = row.get("OGLE3ID", "").strip()
        add_exact_mira_temperature_estimate(
            estimates,
            obj_id,
            valid_mira_literature_temperature(row.get("TeffMcD")),
            jones_index,
        )

    ruffle_index = source_index_for_mira_temperature("ruffle2015_tmcd")
    for row in fetch_vizier_tsv_rows("J/MNRAS/451/3504/table2", "LPV,Tmcd"):
        lpv_id = row.get("LPV", "").strip()
        if not lpv_id:
            continue
        try:
            obj_id = f"OGLE-SMC-LPV-{int(lpv_id):05d}"
        except ValueError:
            continue
        add_exact_mira_temperature_estimate(
            estimates,
            obj_id,
            valid_mira_literature_temperature(row.get("Tmcd")),
            ruffle_index,
        )

    riebel_index = source_index_for_mira_temperature("riebel2012_grams_teff")
    add_coordinate_mira_temperature_estimates(
        estimates,
        lmc_miras,
        fetch_vizier_tsv_rows("J/ApJ/753/71/table3", "Name,Cl,Teff,_RA,_DE"),
        riebel_index,
        "Teff",
    )

    iwanek_index = source_index_for_mira_temperature("iwanek2021_tstar")
    for row in fetch_vizier_tsv_rows("J/ApJS/257/23/gold", "ID,Tstar"):
        obj_id = row.get("ID", "").strip()
        if obj_id in estimates:
            continue
        add_exact_mira_temperature_estimate(
            estimates,
            obj_id,
            valid_mira_literature_temperature(row.get("Tstar")),
            iwanek_index,
        )

    MIRA_TEMPERATURE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    MIRA_TEMPERATURE_CACHE.write_text(
        json.dumps(
            {
                "version": MIRA_TEMPERATURE_CACHE_VERSION,
                "sources": MIRA_TEMPERATURE_SOURCES,
                "estimates": estimates,
            },
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    return estimates


def apply_mira_literature_temperatures(miras: list[CatalogStar]) -> dict[str, object]:
    estimates = build_mira_literature_temperature_lookup(miras)
    source_counts = {source["id"]: 0 for source in MIRA_TEMPERATURE_SOURCES}
    matched = 0
    for star in miras:
        estimate = estimates.get(star.obj_id)
        if estimate is None:
            continue
        temperature = valid_mira_literature_temperature(estimate.get("teff"))
        source_index = estimate.get("sourceIndex")
        if temperature is None or not isinstance(source_index, int) or not (0 <= source_index < len(MIRA_TEMPERATURE_SOURCES)):
            continue
        star.mira_teff = temperature
        star.mira_teff_source_index = source_index
        source_counts[MIRA_TEMPERATURE_SOURCES[source_index]["id"]] += 1
        matched += 1

    return {
        "miraLiteratureTemperatureEstimates": matched,
        "miraLiteratureTemperatureSourceCounts": {
            source_id: count
            for source_id, count in source_counts.items()
            if count
        },
    }


def distance_modulus_to_kpc(distance_modulus: float) -> float:
    return 10 ** ((distance_modulus - 10.0) / 5.0)


def kpc_to_distance_modulus(distance_kpc: float) -> float:
    return 5.0 * math.log10(distance_kpc) + 10.0


def distance_error_from_modulus(distance_kpc: float, modulus_error: float) -> float:
    return distance_kpc * math.log(10) * modulus_error / 5.0


def modulus_error_from_distance(distance_kpc: float, distance_error_kpc: float | None) -> float:
    if distance_error_kpc is None or distance_kpc <= 0:
        return 0.0
    return 5.0 * distance_error_kpc / (math.log(10) * distance_kpc)


def mira_component_arrays(star: CatalogStar) -> tuple[list[float], list[float]]:
    payload = star.mira_pulsation or {}
    periods_raw = payload.get("periods", [])
    amplitudes_raw = payload.get("amplitudesI", [])
    periods: list[float] = []
    amplitudes: list[float] = []
    if not isinstance(periods_raw, list) or not isinstance(amplitudes_raw, list):
        return periods, amplitudes
    for period, amplitude in zip(periods_raw, amplitudes_raw):
        try:
            period_value = float(period)
            amplitude_value = float(amplitude)
        except (TypeError, ValueError):
            continue
        if not (math.isfinite(period_value) and math.isfinite(amplitude_value)):
            continue
        if period_value <= 0 or amplitude_value < MIRA_PULSATION_MIN_AMPLITUDE:
            continue
        periods.append(period_value)
        amplitudes.append(amplitude_value)
    return periods, amplitudes


def synchronize_mira_primary_period(star: CatalogStar, period: float) -> None:
    if star.mira_pulsation is None:
        return
    periods, amplitudes = mira_component_arrays(star)
    if not periods:
        return
    periods[0] = float(period)
    star.mira_pulsation["periods"] = periods
    star.mira_pulsation["amplitudesI"] = amplitudes


def mira_photometry_url(star: CatalogStar, band: str = "I") -> str:
    cloud = "lmc" if star.location == "LMC" or star.obj_id.startswith("OGLE-LMC") else "smc"
    return f"https://ftp.astrouw.edu.pl/ogle/ogle3/OIII-CVS/{cloud}/lpv/phot/{band}/{star.obj_id}.dat"


def mira_model_offsets(times: np.ndarray, periods: list[float], amplitudes: list[float], phases: list[float]) -> np.ndarray:
    offsets = np.zeros(times.shape, dtype=float)
    for period, amplitude, phase in zip(periods, amplitudes, phases):
        offsets += 0.5 * float(amplitude) * np.sin((math.tau * times / float(period)) + float(phase))
    return offsets


def phase_wrap(value: float) -> float:
    return float(((value + math.pi) % math.tau) - math.pi)


def weighted_circular_mean(values: list[float], weights: list[float]) -> float:
    if not values:
        return 0.0
    sin_sum = sum(weight * math.sin(value) for value, weight in zip(values, weights))
    cos_sum = sum(weight * math.cos(value) for value, weight in zip(values, weights))
    if abs(sin_sum) + abs(cos_sum) <= 1e-12:
        return 0.0
    return phase_wrap(math.atan2(sin_sum, cos_sum))


def circular_mad(values: list[float], weights: list[float], center: float) -> float:
    if not values:
        return math.pi
    deviations = [abs(phase_wrap(value - center)) for value in values]
    return 1.4826 * weighted_median(deviations, weights)


def refine_mira_phases(
    times: np.ndarray,
    mags: np.ndarray,
    periods: list[float],
    amplitudes: list[float],
    phases: list[float],
    mask: np.ndarray,
) -> tuple[list[float], float]:
    if not periods:
        return phases, float(np.median(mags))

    phases_array = np.asarray(phases, dtype=float)
    if phases_array.size != len(periods) or not np.isfinite(phases_array).all():
        phases_array = np.zeros(len(periods), dtype=float)
    periods_array = np.asarray(periods, dtype=float)
    semi_amplitudes = 0.5 * np.asarray(amplitudes, dtype=float)
    masked_times = times[mask]
    masked_mags = mags[mask]
    angle_by_component = np.vstack([math.tau * masked_times / period for period in periods_array])

    offset = float(np.median(masked_mags - mira_model_offsets(masked_times, periods, amplitudes, phases_array.tolist())))
    for radius in (math.pi, 0.55, 0.18):
        for component_index in range(len(periods)):
            current = (
                offset
                + np.sum(
                    semi_amplitudes[:, None] * np.sin(angle_by_component + phases_array[:, None]),
                    axis=0,
                )
            )
            current -= semi_amplitudes[component_index] * np.sin(
                angle_by_component[component_index] + phases_array[component_index]
            )
            target = masked_mags - current
            grid = phases_array[component_index] + np.linspace(-radius, radius, 65)
            trial = semi_amplitudes[component_index] * np.sin(angle_by_component[component_index][None, :] + grid[:, None])
            score = np.mean((target[None, :] - trial) ** 2, axis=1)
            phases_array[component_index] = float(grid[int(np.argmin(score))])
        offsets = mira_model_offsets(masked_times, periods, amplitudes, phases_array.tolist())
        offset = float(np.median(masked_mags - offsets))

    phases_array = ((phases_array + math.pi) % math.tau) - math.pi
    return phases_array.tolist(), offset


def fit_mira_multiperiodic_model(star: CatalogStar, photometry: np.ndarray) -> dict[str, object]:
    periods, amplitudes = mira_component_arrays(star)
    if not periods:
        return {"id": star.obj_id, "status": "no_components"}
    if photometry.shape[0] < MIRA_PULSATION_MIN_POINTS:
        return {"id": star.obj_id, "status": "too_few_points", "nI": int(photometry.shape[0])}

    times = np.asarray(photometry[:, 0], dtype=float)
    mags = np.asarray(photometry[:, 1], dtype=float)
    errs = np.clip(np.asarray(photometry[:, 2], dtype=float), 0.01, 0.35)
    design_columns = [np.ones_like(times)]
    for period in periods:
        angle = math.tau * times / period
        design_columns.append(np.sin(angle))
        design_columns.append(np.cos(angle))
    design = np.column_stack(design_columns)

    base_weights = 1.0 / np.square(errs)
    weights = base_weights.copy()
    coeffs = np.zeros(design.shape[1], dtype=float)
    for _ in range(5):
        sqrt_weights = np.sqrt(weights)
        try:
            coeffs = np.linalg.lstsq(design * sqrt_weights[:, None], mags * sqrt_weights, rcond=None)[0]
        except np.linalg.LinAlgError:
            return {"id": star.obj_id, "status": "linear_fit_failed", "nI": int(photometry.shape[0])}
        residuals = mags - design @ coeffs
        center = float(np.median(residuals))
        sigma = max(1.4826 * float(np.median(np.abs(residuals - center))), 0.03)
        robust = np.minimum(1.0, (4.0 * sigma) / np.maximum(np.abs(residuals - center), 1e-6))
        weights = base_weights * robust

    phases: list[float] = []
    fitted_amplitudes: list[float] = []
    for component_index in range(len(periods)):
        sin_coeff = float(coeffs[1 + component_index * 2])
        cos_coeff = float(coeffs[2 + component_index * 2])
        phases.append(math.atan2(cos_coeff, sin_coeff))
        fitted_amplitudes.append(2.0 * math.hypot(sin_coeff, cos_coeff))

    phases, offset = refine_mira_phases(times, mags, periods, amplitudes, phases, np.ones(times.shape, dtype=bool))
    model = offset + mira_model_offsets(times, periods, amplitudes, phases)
    residuals = mags - model
    center = float(np.median(residuals))
    sigma = max(1.4826 * float(np.median(np.abs(residuals - center))), 0.04)
    mask = np.abs(residuals - center) <= max(4.0 * sigma, 0.22)
    if int(np.sum(mask)) >= max(MIRA_PULSATION_MIN_POINTS, int(0.55 * times.size)):
        phases, offset = refine_mira_phases(times, mags, periods, amplitudes, phases, mask)
        model = offset + mira_model_offsets(times, periods, amplitudes, phases)
        residuals = mags - model

    rms = float(np.sqrt(np.mean(np.square(residuals))))
    mad = 1.4826 * float(np.median(np.abs(residuals - np.median(residuals))))
    primary_amplitude = max(float(amplitudes[0]), 1e-6)
    rms_ratio = rms / primary_amplitude
    quality = 1
    if photometry.shape[0] >= 80 and rms_ratio <= 0.25:
        quality = 3
    elif photometry.shape[0] >= 40 and rms_ratio <= 0.45:
        quality = 2

    model_dense_time = np.linspace(float(np.min(times)), float(np.max(times)), 512)
    model_span = peak_to_peak(mira_model_offsets(model_dense_time, periods, amplitudes, phases))
    return {
        "id": star.obj_id,
        "status": "ok",
        "periods": [round_number(value, 6) for value in periods],
        "amplitudesI": [round_number(value, 4) for value in amplitudes],
        "phasesI": [round_number(float(value), 6) for value in phases],
        "quality": quality,
        "nI": int(photometry.shape[0]),
        "rms": round_number(rms, 4),
        "mad": round_number(mad, 4),
        "rmsOverPrimaryAmplitude": round_number(rms_ratio, 4),
        "modelSpanI": round_number(model_span, 4),
        "fittedAmplitudesI": [round_number(value, 4) for value in fitted_amplitudes],
        "source": "ogle-lpv-multisine-v1",
    }


def mira_v_prior_arrays(prior: dict[str, object] | None, count: int) -> tuple[list[float], list[float], list[float], list[int]] | None:
    if prior is None:
        return None
    amplitudes_raw = prior.get("amplitudesV")
    phases_raw = prior.get("phasesV")
    scales_raw = prior.get("coefficientScales")
    counts_raw = prior.get("sampleCounts")
    if not (isinstance(amplitudes_raw, list) and isinstance(phases_raw, list)):
        return None
    amplitudes: list[float] = []
    phases: list[float] = []
    scales: list[float] = []
    sample_counts: list[int] = []
    for index in range(count):
        amplitude = finite_float(amplitudes_raw[index]) if index < len(amplitudes_raw) else None
        phase = finite_float(phases_raw[index]) if index < len(phases_raw) else None
        if amplitude is None or phase is None or amplitude <= 0:
            return None
        scale = finite_float(scales_raw[index]) if isinstance(scales_raw, list) and index < len(scales_raw) else None
        count_raw = counts_raw[index] if isinstance(counts_raw, list) and index < len(counts_raw) else 0
        try:
            sample_count = int(count_raw)
        except (TypeError, ValueError):
            sample_count = 0
        amplitudes.append(amplitude)
        phases.append(phase_wrap(phase))
        scales.append(max(0.08, scale if scale is not None else 0.22 * amplitude))
        sample_counts.append(max(0, sample_count))
    return amplitudes, phases, scales, sample_counts


def mira_v_prior_only_fit(periods: list[float], prior: dict[str, object], n_v: int) -> dict[str, object] | None:
    prior_arrays = mira_v_prior_arrays(prior, len(periods))
    if prior_arrays is None:
        return None
    amplitudes, phases, _, sample_counts = prior_arrays
    dense_times = np.linspace(0.0, max(periods) if periods else 1.0, 1024)
    model_span = peak_to_peak(mira_model_offsets(dense_times, periods, amplitudes, phases))
    if not math.isfinite(model_span) or model_span <= 0:
        return None
    return {
        "amplitudesV": [round_number(value, 4) for value in amplitudes],
        "phasesV": [round_number(value, 6) for value in phases],
        "qualityV": 1,
        "nV": int(n_v),
        "vRms": None,
        "vMad": None,
        "vRmsOverSpan": None,
        "modelSpanV": round_number(model_span, 4),
        "observedSpanV": None,
        "vRegularization": None,
        "vPriorSampleCounts": sample_counts,
        "vSource": MIRA_V_PRIOR_SOURCE,
    }


def fit_mira_v_multiperiodic_model(
    star: CatalogStar,
    photometry: np.ndarray,
    periods: list[float],
    prior: dict[str, object] | None = None,
    allow_prior_only: bool = False,
) -> dict[str, object] | None:
    component_count = len(periods)
    min_points = max(MIRA_PULSATION_MIN_V_POINTS, component_count * 4 + 2)
    if component_count == 0 or photometry.shape[0] < min_points:
        if allow_prior_only and component_count > 0 and prior is not None:
            return mira_v_prior_only_fit(periods, prior, int(photometry.shape[0]))
        return None

    times = np.asarray(photometry[:, 0], dtype=float)
    mags = np.asarray(photometry[:, 1], dtype=float)
    errs = np.clip(np.asarray(photometry[:, 2], dtype=float), 0.015, 0.5)
    design_columns = [np.ones_like(times)]
    for period in periods:
        angle = math.tau * times / period
        design_columns.append(np.sin(angle))
        design_columns.append(np.cos(angle))
    design = np.column_stack(design_columns)

    _, i_amplitudes = mira_component_arrays(star)
    observed_span = max(percentile_span(mags), 0.55 * peak_to_peak(mags), 0.12)
    if len(i_amplitudes) < component_count:
        i_amplitudes = [observed_span / max(component_count, 1)] * component_count
    primary_i_amplitude = max(float(i_amplitudes[0]), 0.1)
    v_to_i_prior = min(3.2, max(1.15, observed_span / primary_i_amplitude))
    coefficient_scales = np.ones(design.shape[1], dtype=float)
    coefficient_targets = np.zeros(design.shape[1], dtype=float)
    prior_arrays = mira_v_prior_arrays(prior, component_count)
    prior_span = 0.0
    prior_sample_counts: list[int] = []
    if prior_arrays is not None:
        prior_amplitudes, prior_phases, prior_scales, prior_sample_counts = prior_arrays
        dense_prior_times = np.linspace(float(np.min(times)), float(np.max(times)), 512)
        prior_span = peak_to_peak(mira_model_offsets(dense_prior_times, periods, prior_amplitudes, prior_phases))
        for component_index, (amplitude, phase, scale) in enumerate(zip(prior_amplitudes, prior_phases, prior_scales)):
            coefficient_targets[1 + component_index * 2] = 0.5 * amplitude * math.cos(phase)
            coefficient_targets[2 + component_index * 2] = 0.5 * amplitude * math.sin(phase)
            coefficient_scales[1 + component_index * 2] = max(0.08, scale)
            coefficient_scales[2 + component_index * 2] = max(0.08, scale)
    for component_index, i_amplitude in enumerate(i_amplitudes[:component_count]):
        if prior_arrays is None:
            prior_amplitude = min(observed_span * 1.15, max(0.18, float(i_amplitude) * v_to_i_prior))
            coefficient_scale = max(0.08, 0.5 * prior_amplitude)
            coefficient_scales[1 + component_index * 2] = coefficient_scale
            coefficient_scales[2 + component_index * 2] = coefficient_scale

    base_weights = 1.0 / np.square(errs)
    weights = base_weights.copy()
    coeffs = np.zeros(design.shape[1], dtype=float)

    def solve_coefficients(mask: np.ndarray, solve_weights: np.ndarray, ridge_strength: float) -> np.ndarray:
        sqrt_weights = np.sqrt(solve_weights[mask])
        weighted_design = design[mask] * sqrt_weights[:, None]
        weighted_mags = mags[mask] * sqrt_weights
        if ridge_strength > 0:
            weight_scale = max(float(np.median(base_weights[mask])), 1.0)
            penalty = math.sqrt(ridge_strength * weight_scale) / coefficient_scales[1:]
            regularization = np.zeros((design.shape[1] - 1, design.shape[1]), dtype=float)
            regularization[:, 1:] = np.diag(penalty)
            weighted_design = np.vstack([weighted_design, regularization])
            weighted_mags = np.concatenate([weighted_mags, penalty * coefficient_targets[1:]])
        return np.linalg.lstsq(weighted_design, weighted_mags, rcond=None)[0]

    def components_from_coefficients(candidate: np.ndarray) -> tuple[list[float], list[float]] | None:
        candidate_amplitudes: list[float] = []
        candidate_phases: list[float] = []
        for component_index in range(component_count):
            sin_coeff = float(candidate[1 + component_index * 2])
            cos_coeff = float(candidate[2 + component_index * 2])
            amplitude = 2.0 * math.hypot(sin_coeff, cos_coeff)
            phase = math.atan2(cos_coeff, sin_coeff)
            if not (math.isfinite(amplitude) and math.isfinite(phase)):
                return None
            candidate_amplitudes.append(amplitude)
            candidate_phases.append(float(((phase + math.pi) % math.tau) - math.pi))
        return candidate_amplitudes, candidate_phases

    for _ in range(6):
        try:
            coeffs = solve_coefficients(np.ones(times.shape, dtype=bool), weights, 0.55)
        except np.linalg.LinAlgError:
            return None
        residuals = mags - design @ coeffs
        center = float(np.median(residuals))
        sigma = max(1.4826 * float(np.median(np.abs(residuals - center))), 0.05)
        robust = np.minimum(1.0, (4.0 * sigma) / np.maximum(np.abs(residuals - center), 1e-6))
        weights = base_weights * robust

    components = components_from_coefficients(coeffs)
    if components is None:
        return None
    amplitudes, phases = components

    model_offsets = mira_model_offsets(times, periods, amplitudes, phases)
    model_offset = float(np.median(mags - model_offsets))
    residuals = mags - (model_offset + model_offsets)
    center = float(np.median(residuals))
    sigma = max(1.4826 * float(np.median(np.abs(residuals - center))), 0.06)
    mask = np.abs(residuals - center) <= max(4.0 * sigma, 0.25)
    if int(np.sum(mask)) >= max(min_points, int(0.55 * times.size)):
        fit_mask = mask
    else:
        fit_mask = np.ones(times.shape, dtype=bool)

    best_fit: tuple[float, float, float, list[float], list[float], np.ndarray, float] | None = None
    prior_span_safe = prior_span if math.isfinite(prior_span) and prior_span > 0 else 0.0
    allowed_span = max(observed_span * 1.45 + 0.2, prior_span_safe * 1.25 + 0.18)
    allowed_component = max(observed_span * 1.35 + 0.25, float(np.max(np.abs(coefficient_targets[1:]))) * 3.0 + 0.25)
    for ridge_strength in (0.15, 0.35, 0.75, 1.6, 3.5, 7.5, 16.0, 34.0):
        try:
            candidate_coeffs = solve_coefficients(fit_mask, base_weights, ridge_strength)
        except np.linalg.LinAlgError:
            continue
        components = components_from_coefficients(candidate_coeffs)
        if components is None:
            continue
        candidate_amplitudes, candidate_phases = components
        candidate_offsets = mira_model_offsets(times, periods, candidate_amplitudes, candidate_phases)
        candidate_offset = float(np.median(mags[fit_mask] - candidate_offsets[fit_mask]))
        candidate_residuals = mags - (candidate_offset + candidate_offsets)
        dense_times = np.linspace(float(np.min(times)), float(np.max(times)), 512)
        candidate_span = peak_to_peak(mira_model_offsets(dense_times, periods, candidate_amplitudes, candidate_phases))
        candidate_component = max(candidate_amplitudes)
        if not (math.isfinite(candidate_span) and math.isfinite(candidate_component)):
            continue
        candidate_rms = float(np.sqrt(np.mean(np.square(candidate_residuals))))
        span_excess = max(0.0, candidate_span - allowed_span)
        component_excess = max(0.0, candidate_component - allowed_component)
        prior_deviation = 0.0
        if prior_arrays is not None:
            normalized = (candidate_coeffs[1:] - coefficient_targets[1:]) / coefficient_scales[1:]
            prior_deviation = float(np.sqrt(np.mean(np.square(normalized))))
        score = (
            candidate_rms
            + 0.15 * span_excess
            + 0.08 * component_excess
            + (0.018 * prior_deviation if prior_arrays is not None else 0.0)
            + 0.0015 * ridge_strength
        )
        if best_fit is None or score < best_fit[0]:
            best_fit = (
                score,
                candidate_span,
                ridge_strength,
                candidate_amplitudes,
                candidate_phases,
                candidate_residuals,
                candidate_offset,
            )

    if best_fit is None:
        return None
    _, model_span, ridge_strength, amplitudes, phases, residuals, model_offset = best_fit
    span_ceiling = max(observed_span * 1.8 + 0.35, prior_span_safe * 1.65 + 0.3)
    component_ceiling = max(observed_span * 1.65 + 0.35, max((prior_arrays[0] if prior_arrays is not None else [0.0])) * 1.9 + 0.35)
    if model_span > span_ceiling or max(amplitudes) > component_ceiling:
        return None

    finite_amplitudes = np.asarray(amplitudes, dtype=float)
    if not np.isfinite(finite_amplitudes).all() or float(np.max(finite_amplitudes)) <= 0:
        return None
    if not math.isfinite(model_span) or model_span <= 0:
        return None

    rms = float(np.sqrt(np.mean(np.square(residuals))))
    mad = 1.4826 * float(np.median(np.abs(residuals - np.median(residuals))))
    rms_ratio = rms / max(model_span, 1e-6)
    quality = 1
    if photometry.shape[0] >= 36 and rms_ratio <= 0.25:
        quality = 3
    elif photometry.shape[0] >= min_points and rms_ratio <= 0.45:
        quality = 2

    result = {
        "amplitudesV": [round_number(value, 4) for value in amplitudes],
        "phasesV": [round_number(value, 6) for value in phases],
        "qualityV": quality,
        "nV": int(photometry.shape[0]),
        "vRms": round_number(rms, 4),
        "vMad": round_number(mad, 4),
        "vRmsOverSpan": round_number(rms_ratio, 4),
        "modelSpanV": round_number(model_span, 4),
        "observedSpanV": round_number(observed_span, 4),
        "vRegularization": round_number(ridge_strength, 4),
        "vSource": MIRA_V_PRIOR_ASSISTED_SOURCE if prior_arrays is not None else "ogle-lpv-v-multisine-v1",
    }
    if prior_arrays is not None:
        result["vPriorSampleCounts"] = prior_sample_counts
    return result


def fetch_and_fit_mira_pulsation(star: CatalogStar) -> dict[str, object]:
    try:
        request = urllib.request.Request(
            mira_photometry_url(star, "I"),
            headers={"User-Agent": MIRA_PULSATION_FIT_USER_AGENT},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            photometry = parse_photometry(response.read())
    except Exception as exc:  # noqa: BLE001 - record per-star remote failures in the cache summary.
        return {"id": star.obj_id, "status": "fetch_failed", "error": str(exc)[:160]}
    fit = fit_mira_multiperiodic_model(star, photometry)
    if fit.get("status") != "ok":
        return fit

    periods = [float(value) for value in fit.get("periods", [])] if isinstance(fit.get("periods"), list) else []
    try:
        request = urllib.request.Request(
            mira_photometry_url(star, "V"),
            headers={"User-Agent": MIRA_PULSATION_FIT_USER_AGENT},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            photometry_v = parse_photometry(response.read())
    except Exception:
        photometry_v = np.empty((0, 3), dtype=float)
    v_fit = fit_mira_v_multiperiodic_model(star, photometry_v, periods)
    if v_fit is not None:
        fit.update(v_fit)
    else:
        fit["nV"] = int(photometry_v.shape[0])
    return fit


def fit_float_list(fit: dict[str, object], key: str, count: int | None = None, positive: bool = False) -> list[float] | None:
    raw = fit.get(key)
    if not isinstance(raw, list):
        return None
    values: list[float] = []
    limit = len(raw) if count is None else min(count, len(raw))
    for value in raw[:limit]:
        parsed = finite_float(value)
        if parsed is None or (positive and parsed <= 0):
            return None
        values.append(parsed)
    if count is not None and len(values) != count:
        return None
    return values


def good_mira_v_prior_fit(fit: dict[str, object]) -> bool:
    if fit.get("status") != "ok":
        return False
    try:
        quality_i = int(fit.get("quality", 0))
        quality_v = int(fit.get("qualityV", 0))
        n_v = int(fit.get("nV", 0))
    except (TypeError, ValueError):
        return False
    rms_ratio = finite_float(fit.get("vRmsOverSpan"))
    model_span = finite_float(fit.get("modelSpanV"))
    observed_span = finite_float(fit.get("observedSpanV"))
    if quality_i < 3 or quality_v < 3 or n_v < 36 or rms_ratio is None or rms_ratio > 0.16:
        return False
    if model_span is None or observed_span is None or observed_span <= 0:
        return False
    span_ratio = model_span / observed_span
    return 0.65 <= span_ratio <= 1.55


def build_mira_v_prior_samples(
    miras: list[CatalogStar],
    fits: dict[str, dict[str, object]],
) -> dict[int, list[dict[str, float | str]]]:
    samples: dict[int, list[dict[str, float | str]]] = {}
    for star in miras:
        fit = fits.get(star.obj_id)
        if fit is None or not good_mira_v_prior_fit(fit):
            continue
        periods = fit_float_list(fit, "periods", positive=True)
        amplitudes_i = fit_float_list(fit, "amplitudesI", positive=True)
        phases_i = fit_float_list(fit, "phasesI")
        amplitudes_v = fit_float_list(fit, "amplitudesV", positive=True)
        phases_v = fit_float_list(fit, "phasesV")
        if not (periods and amplitudes_i and phases_i and amplitudes_v and phases_v):
            continue
        count = min(len(periods), len(amplitudes_i), len(phases_i), len(amplitudes_v), len(phases_v))
        if count == 0 or periods[0] <= 0:
            continue
        chemistry = mira_chemistry_key(star.mode) or "unknown"
        log_primary_period = math.log10(periods[0])
        for index in range(count):
            if amplitudes_i[index] <= 0:
                continue
            ratio = amplitudes_v[index] / amplitudes_i[index]
            if not math.isfinite(ratio) or ratio < 0.45 or ratio > 5.6:
                continue
            samples.setdefault(index, []).append(
                {
                    "chemistry": chemistry,
                    "logP": log_primary_period,
                    "ratio": ratio,
                    "phaseLag": phase_wrap(phases_v[index] - phases_i[index]),
                }
            )
    return samples


def mira_v_prior_for_component(
    samples: list[dict[str, float | str]],
    chemistry: str,
    log_primary_period: float,
    i_amplitude: float,
    i_phase: float,
) -> dict[str, float | int] | None:
    if not samples:
        return None
    chemistry_samples = [sample for sample in samples if sample.get("chemistry") == chemistry]
    active_samples = chemistry_samples if len(chemistry_samples) >= MIRA_V_PRIOR_MIN_SAMPLES else samples
    if len(active_samples) < 6:
        return None

    ratios: list[float] = []
    phase_lags: list[float] = []
    weights: list[float] = []
    for sample in active_samples:
        ratio = finite_float(sample.get("ratio"))
        phase_lag = finite_float(sample.get("phaseLag"))
        sample_logp = finite_float(sample.get("logP"))
        if ratio is None or phase_lag is None or sample_logp is None:
            continue
        period_weight = math.exp(-0.5 * ((log_primary_period - sample_logp) / MIRA_V_PRIOR_LOGP_SCALE) ** 2)
        if sample.get("chemistry") != chemistry:
            period_weight *= 0.45
        ratios.append(ratio)
        phase_lags.append(phase_lag)
        weights.append(max(period_weight, 0.025))
    if len(ratios) < 6 or sum(weights) <= 0:
        return None

    ratio_center = weighted_median(ratios, weights)
    ratio_mad = 1.4826 * weighted_median([abs(value - ratio_center) for value in ratios], weights)
    phase_lag_center = weighted_circular_mean(phase_lags, weights)
    phase_lag_mad = circular_mad(phase_lags, weights, phase_lag_center)
    effective_count = (sum(weights) ** 2) / max(sum(weight * weight for weight in weights), 1e-9)
    near_count = sum(1 for weight in weights if weight >= 0.25)

    ratio_center = min(5.0, max(0.7, ratio_center))
    amplitude = max(MIRA_PULSATION_MIN_AMPLITUDE, i_amplitude * ratio_center)
    phase = phase_wrap(i_phase + phase_lag_center)
    fractional_ratio_scatter = min(0.9, max(0.16, ratio_mad / max(ratio_center, 0.1)))
    phase_scatter = min(1.1, max(0.16, phase_lag_mad))
    loosen_for_sparse_prior = 1.0 + max(0.0, MIRA_V_PRIOR_MIN_SAMPLES - effective_count) * 0.025
    coefficient_scale = max(0.08, 0.5 * amplitude * max(fractional_ratio_scatter, 0.45 * phase_scatter) * loosen_for_sparse_prior)

    return {
        "amplitude": amplitude,
        "phase": phase,
        "coefficientScale": coefficient_scale,
        "sampleCount": int(round(max(near_count, effective_count))),
        "ratio": ratio_center,
        "phaseLag": phase_lag_center,
    }


def mira_v_prior_for_fit(
    star: CatalogStar,
    fit: dict[str, object],
    prior_samples: dict[int, list[dict[str, float | str]]],
) -> dict[str, object] | None:
    periods = fit_float_list(fit, "periods", positive=True)
    amplitudes_i = fit_float_list(fit, "amplitudesI", positive=True)
    phases_i = fit_float_list(fit, "phasesI")
    if not (periods and amplitudes_i and phases_i) or periods[0] <= 0:
        return None
    count = min(len(periods), len(amplitudes_i), len(phases_i))
    chemistry = mira_chemistry_key(star.mode) or "unknown"
    log_primary_period = math.log10(periods[0])
    amplitudes_v: list[float] = []
    phases_v: list[float] = []
    coefficient_scales: list[float] = []
    sample_counts: list[int] = []
    ratios: list[float] = []
    phase_lags: list[float] = []
    for index in range(count):
        component_prior = mira_v_prior_for_component(
            prior_samples.get(index, []),
            chemistry,
            log_primary_period,
            amplitudes_i[index],
            phases_i[index],
        )
        if component_prior is None:
            return None
        amplitudes_v.append(float(component_prior["amplitude"]))
        phases_v.append(float(component_prior["phase"]))
        coefficient_scales.append(float(component_prior["coefficientScale"]))
        sample_counts.append(int(component_prior["sampleCount"]))
        ratios.append(float(component_prior["ratio"]))
        phase_lags.append(float(component_prior["phaseLag"]))
    if not amplitudes_v:
        return None
    return {
        "amplitudesV": amplitudes_v,
        "phasesV": phases_v,
        "coefficientScales": coefficient_scales,
        "sampleCounts": sample_counts,
        "ratios": ratios,
        "phaseLags": phase_lags,
        "source": MIRA_V_PRIOR_SOURCE,
    }


def accept_mira_prior_v_fit(original: dict[str, object], candidate: dict[str, object]) -> bool:
    original_has_v = isinstance(original.get("amplitudesV"), list) and isinstance(original.get("phasesV"), list)
    if not original_has_v:
        return True
    try:
        original_quality = int(original.get("qualityV", 0))
        candidate_quality = int(candidate.get("qualityV", 0))
    except (TypeError, ValueError):
        return False
    if original_quality <= 1 or candidate_quality > original_quality:
        return True
    original_rms = finite_float(original.get("vRmsOverSpan"))
    candidate_rms = finite_float(candidate.get("vRmsOverSpan"))
    if original_rms is None or candidate_rms is None:
        return candidate.get("vSource") == MIRA_V_PRIOR_SOURCE
    return candidate_quality >= original_quality and candidate_rms <= original_rms * 1.15


def refit_mira_v_with_prior(
    star: CatalogStar,
    fit: dict[str, object],
    prior: dict[str, object],
) -> dict[str, object]:
    periods = fit_float_list(fit, "periods", positive=True) or []
    result = dict(fit)
    try:
        request = urllib.request.Request(
            mira_photometry_url(star, "V"),
            headers={"User-Agent": MIRA_PULSATION_FIT_USER_AGENT},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            photometry_v = parse_photometry(response.read())
    except Exception:
        photometry_v = np.empty((0, 3), dtype=float)
    v_fit = fit_mira_v_multiperiodic_model(star, photometry_v, periods, prior=prior, allow_prior_only=True)
    if v_fit is not None and accept_mira_prior_v_fit(fit, v_fit):
        result.update(v_fit)
    return result


def deterministic_mira_phases(star: CatalogStar, count: int) -> list[float]:
    return [
        round_number(stable_unit_interval(f"{star.obj_id}-mira-component-{index}") * math.tau - math.pi, 6)
        for index in range(count)
    ]


def cached_mira_fit_compatible(star: CatalogStar, fit: dict[str, object]) -> bool:
    periods, amplitudes = mira_component_arrays(star)
    fit_periods = fit.get("periods")
    fit_amplitudes = fit.get("amplitudesI")
    fit_phases = fit.get("phasesI")
    if not (isinstance(fit_periods, list) and isinstance(fit_amplitudes, list) and isinstance(fit_phases, list)):
        return False
    if len(periods) != len(fit_periods) or len(amplitudes) != len(fit_amplitudes) or len(periods) != len(fit_phases):
        return False
    for left, right in zip(periods, fit_periods):
        try:
            if abs(float(left) - float(right)) > 1e-4:
                return False
        except (TypeError, ValueError):
            return False
    for left, right in zip(amplitudes, fit_amplitudes):
        try:
            if abs(float(left) - float(right)) > 1e-4:
                return False
        except (TypeError, ValueError):
            return False
    return True


def load_mira_pulsation_fit_cache(miras: list[CatalogStar]) -> dict[str, dict[str, object]] | None:
    if not MIRA_PULSATION_FITS_CACHE.exists():
        return None
    try:
        payload = json.loads(MIRA_PULSATION_FITS_CACHE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if payload.get("version") != MIRA_PULSATION_FIT_VERSION:
        return None
    fits_raw = payload.get("fits")
    if not isinstance(fits_raw, dict):
        return None
    fits = {str(key): value for key, value in fits_raw.items() if isinstance(value, dict)}
    if any(star.obj_id not in fits or not cached_mira_fit_compatible(star, fits[star.obj_id]) for star in miras):
        return None
    return fits


def build_mira_pulsation_fit_cache(miras: list[CatalogStar]) -> dict[str, dict[str, object]]:
    fits: dict[str, dict[str, object]] = {}
    status_counts: dict[str, int] = {}
    PROCESSED.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=MIRA_PULSATION_FETCH_WORKERS) as executor:
        futures = [executor.submit(fetch_and_fit_mira_pulsation, star) for star in miras]
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            obj_id = str(result.get("id", ""))
            if obj_id:
                fits[obj_id] = result
            status = str(result.get("status", "unknown"))
            status_counts[status] = status_counts.get(status, 0) + 1
            if index % 100 == 0 or index == len(futures):
                print(f"Fitted Mira pulsation models {index}/{len(futures)}")

    prior_samples = build_mira_v_prior_samples(miras, fits)
    prior_candidates: list[tuple[CatalogStar, dict[str, object], dict[str, object]]] = []
    for star in miras:
        fit = fits.get(star.obj_id)
        if fit is None or fit.get("status") != "ok" or not cached_mira_fit_compatible(star, fit):
            continue
        try:
            quality_v = int(fit.get("qualityV", 0))
        except (TypeError, ValueError):
            quality_v = 0
        if quality_v >= 3:
            continue
        prior = mira_v_prior_for_fit(star, fit, prior_samples)
        if prior is not None:
            prior_candidates.append((star, fit, prior))

    prior_refit_count = 0
    if prior_candidates:
        with ThreadPoolExecutor(max_workers=MIRA_PULSATION_FETCH_WORKERS) as executor:
            futures = [executor.submit(refit_mira_v_with_prior, star, fit, prior) for star, fit, prior in prior_candidates]
            for index, future in enumerate(as_completed(futures), start=1):
                result = future.result()
                obj_id = str(result.get("id", ""))
                if obj_id:
                    old_source = str(fits.get(obj_id, {}).get("vSource", ""))
                    new_source = str(result.get("vSource", ""))
                    fits[obj_id] = result
                    if new_source in {MIRA_V_PRIOR_SOURCE, MIRA_V_PRIOR_ASSISTED_SOURCE} and new_source != old_source:
                        prior_refit_count += 1
                if index % 100 == 0 or index == len(futures):
                    print(f"Refitted weak Mira V models with learned priors {index}/{len(futures)}")

    quality_counts: dict[str, int] = {}
    v_quality_counts: dict[str, int] = {}
    v_source_counts: dict[str, int] = {}
    rms_ratios: list[float] = []
    v_rms_ratios: list[float] = []
    component_counts: list[int] = []
    for fit in fits.values():
        if fit.get("status") == "ok":
            quality = str(fit.get("quality", 0))
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
            if isinstance(fit.get("amplitudesV"), list) and isinstance(fit.get("phasesV"), list):
                v_quality = str(fit.get("qualityV", 0))
                v_quality_counts[v_quality] = v_quality_counts.get(v_quality, 0) + 1
                v_source = str(fit.get("vSource", "unknown"))
                v_source_counts[v_source] = v_source_counts.get(v_source, 0) + 1
                v_ratio = fit.get("vRmsOverSpan")
                if isinstance(v_ratio, (int, float)) and math.isfinite(float(v_ratio)):
                    v_rms_ratios.append(float(v_ratio))
            ratio = fit.get("rmsOverPrimaryAmplitude")
            if isinstance(ratio, (int, float)) and math.isfinite(float(ratio)):
                rms_ratios.append(float(ratio))
            periods = fit.get("periods")
            if isinstance(periods, list):
                component_counts.append(len(periods))

    summary = {
        "statusCounts": status_counts,
        "qualityCounts": quality_counts,
        "vQualityCounts": v_quality_counts,
        "vSourceCounts": v_source_counts,
        "medianRmsOverPrimaryAmplitude": round_number(float(np.median(rms_ratios)), 4) if rms_ratios else None,
        "medianVRmsOverSpan": round_number(float(np.median(v_rms_ratios)), 4) if v_rms_ratios else None,
        "medianComponentCount": round_number(float(np.median(component_counts)), 2) if component_counts else None,
        "vPriorTrainingSamples": {str(index): len(samples) for index, samples in sorted(prior_samples.items())},
        "vPriorCandidates": len(prior_candidates),
        "vPriorAcceptedRefits": prior_refit_count,
    }
    MIRA_PULSATION_FITS_CACHE.write_text(
        json.dumps(
            {
                "version": MIRA_PULSATION_FIT_VERSION,
                "summary": summary,
                "fits": fits,
            },
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    return fits


def apply_mira_pulsations(miras: list[CatalogStar]) -> dict[str, object]:
    fits = load_mira_pulsation_fit_cache(miras)
    if fits is None:
        fits = build_mira_pulsation_fit_cache(miras)

    quality_counts: dict[str, int] = {}
    v_quality_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}
    v_source_counts: dict[str, int] = {}
    component_counts: list[int] = []
    rms_ratios: list[float] = []
    v_rms_ratios: list[float] = []
    fitted = 0
    fitted_v = 0
    fitted_v_data = 0
    fitted_v_prior_assisted = 0
    fitted_v_prior_only = 0
    for star in miras:
        periods, amplitudes = mira_component_arrays(star)
        amplitudes_v: list[float] = []
        phases_v: list[float] = []
        quality_v = 0
        source_v: str | None = None
        fit = fits.get(star.obj_id)
        if fit is not None and fit.get("status") == "ok" and cached_mira_fit_compatible(star, fit):
            phases = [float(value) for value in fit.get("phasesI", [])]  # type: ignore[arg-type]
            quality = int(fit.get("quality", 1))
            source = str(fit.get("source", "ogle-lpv-multisine-v1"))
            fitted += 1
            ratio = fit.get("rmsOverPrimaryAmplitude")
            if isinstance(ratio, (int, float)) and math.isfinite(float(ratio)):
                rms_ratios.append(float(ratio))
            amplitudes_v_raw = fit.get("amplitudesV")
            phases_v_raw = fit.get("phasesV")
            if isinstance(amplitudes_v_raw, list) and isinstance(phases_v_raw, list):
                for amplitude_raw, phase_raw in zip(amplitudes_v_raw[: len(periods)], phases_v_raw[: len(periods)]):
                    amplitude_v = finite_float(amplitude_raw)
                    phase_v = finite_float(phase_raw)
                    if amplitude_v is None or phase_v is None or amplitude_v <= 0:
                        break
                    amplitudes_v.append(amplitude_v)
                    phases_v.append(phase_v)
                if len(amplitudes_v) != len(periods) or len(phases_v) != len(periods):
                    amplitudes_v = []
                    phases_v = []
                else:
                    fitted_v += 1
                    try:
                        quality_v = int(fit.get("qualityV", 1))
                    except (TypeError, ValueError):
                        quality_v = 1
                    source_v = str(fit.get("vSource", "ogle-lpv-v-multisine-v1"))
                    model_span_v = finite_float(fit.get("modelSpanV"))
                    if model_span_v is not None and model_span_v > 0:
                        star.v_amplitude = model_span_v
                    v_ratio = fit.get("vRmsOverSpan")
                    if isinstance(v_ratio, (int, float)) and math.isfinite(float(v_ratio)):
                        v_rms_ratios.append(float(v_ratio))
                    if source_v == MIRA_V_PRIOR_SOURCE:
                        fitted_v_prior_only += 1
                    elif source_v == MIRA_V_PRIOR_ASSISTED_SOURCE:
                        fitted_v_prior_assisted += 1
                    else:
                        fitted_v_data += 1
        else:
            phases = deterministic_mira_phases(star, len(periods))
            quality = 1 if periods else 0
            source = "catalog-multisine-random-phase" if periods else "none"

        mira_pulsation: dict[str, object] = {
            "periods": periods,
            "amplitudesI": amplitudes,
            "phasesI": phases,
            "quality": quality,
            "source": source,
        }
        if amplitudes_v and phases_v:
            mira_pulsation.update(
                {
                    "amplitudesV": amplitudes_v,
                    "phasesV": phases_v,
                    "qualityV": quality_v,
                    "sourceV": source_v,
                }
            )
        star.mira_pulsation = mira_pulsation
        if periods:
            component_counts.append(len(periods))
        quality_counts[str(quality)] = quality_counts.get(str(quality), 0) + 1
        source_counts[source] = source_counts.get(source, 0) + 1
        if amplitudes_v and source_v is not None:
            v_quality_counts[str(quality_v)] = v_quality_counts.get(str(quality_v), 0) + 1
            v_source_counts[source_v] = v_source_counts.get(source_v, 0) + 1

    return {
        "miraMultiperiodicModels": sum(1 for star in miras if star.mira_pulsation and star.mira_pulsation.get("periods")),
        "miraMultiperiodicPhaseFits": fitted,
        "miraVMultiperiodicPhaseFits": fitted_v,
        "miraVMultiperiodicDataFits": fitted_v_data,
        "miraVMultiperiodicPriorAssistedFits": fitted_v_prior_assisted,
        "miraVMultiperiodicPriorOnly": fitted_v_prior_only,
        "miraMultiperiodicQuality": quality_counts,
        "miraVMultiperiodicQuality": v_quality_counts,
        "miraMultiperiodicSources": source_counts,
        "miraVMultiperiodicSources": v_source_counts,
        "miraMultiperiodicMedianComponentCount": round_number(float(np.median(component_counts)), 2) if component_counts else None,
        "miraMultiperiodicMedianRmsOverPrimaryAmplitude": round_number(float(np.median(rms_ratios)), 4) if rms_ratios else None,
        "miraVMultiperiodicMedianRmsOverSpan": round_number(float(np.median(v_rms_ratios)), 4) if v_rms_ratios else None,
    }


def mira_chemistry_key(value: str | None) -> str | None:
    if not value:
        return None
    text = str(value).strip().upper()
    if text.startswith("C"):
        return "C"
    if text.startswith("O"):
        return "O"
    if "C-RICH" in text:
        return "C"
    if "O-RICH" in text:
        return "O"
    return None


def valid_mira_mid_ir_value(value: float | None) -> bool:
    return value is not None and math.isfinite(value) and -5.0 < value < 30.0


def mira_plr_coefficients(chemistry: str, period: float, band: str) -> dict[str, float] | None:
    if period <= 0:
        return None
    if chemistry == "C":
        return MIRA_PLR_COEFFICIENTS["C"].get(band)
    if chemistry == "O":
        group = "O_LINEAR" if math.log10(period) <= MIRA_PLR_O_RICH_LINEAR_LOGP_MAX else "O_QUADRATIC"
        return MIRA_PLR_COEFFICIENTS[group].get(band)
    return None


def mira_absolute_magnitude(period: float, chemistry: str, band: str) -> tuple[float, float, float] | None:
    coefficients = mira_plr_coefficients(chemistry, period, band)
    if coefficients is None:
        return None
    x = math.log10(period) - MIRA_PLR_LOGP_PIVOT
    absolute_mag = coefficients["a0"] + coefficients["a1"] * x + coefficients["a2"] * x * x
    coefficient_error = math.sqrt(
        coefficients["a0Err"] ** 2
        + (x * coefficients["a1Err"]) ** 2
        + (x * x * coefficients["a2Err"]) ** 2
    )
    return absolute_mag, coefficient_error, coefficients["scatter"]


def mira_mid_ir_extinction(star: CatalogStar, band: str, already_corrected: bool) -> float:
    if already_corrected:
        return 0.0
    if not math.isfinite(star.reddening_evi) or star.reddening_evi <= 0:
        return 0.0
    return MIRA_EXTINCTION_AV_PER_EVI * star.reddening_evi * MIRA_MIDIR_EXTINCTION_AV.get(band, 0.0)


def parse_iwanek2021_mira_table() -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    if not IWANEK2021_MIRA_TABLE.exists():
        return rows
    bands = ("W1", "W2", "W3", "W4", "S36", "S45", "S58", "S80")
    for line in IWANEK2021_MIRA_TABLE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("OGLE-"):
            continue
        parts = line.split()
        if len(parts) < 25:
            continue
        period = parse_float(parts[8])
        chemistry = mira_chemistry_key(parts[7])
        magnitudes: dict[str, float] = {}
        errors: dict[str, float] = {}
        value_index = 9
        for band in bands:
            mag = parse_float(parts[value_index])
            err = parse_float(parts[value_index + 1])
            value_index += 2
            if valid_mira_mid_ir_value(mag):
                magnitudes[band] = float(mag)
            if valid_mira_mid_ir_value(err):
                errors[band] = float(err)
        rows[parts[0]] = {
            "period": period,
            "chemistry": chemistry,
            "magnitudes": magnitudes,
            "errors": errors,
        }
    return rows


def download_mira_allwise_xmatch(stars: list[CatalogStar], path: Path) -> None:
    if path.exists() and path.stat().st_size > 1000:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    csv_lines = ["id,ra,dec"]
    for star in stars:
        csv_lines.append(f"{star.obj_id},{star.ra:.8f},{star.dec:.8f}")
    csv_payload = "\n".join(csv_lines) + "\n"

    boundary = "----mc-atlas-mira-xmatch-" + hashlib.sha256(csv_payload.encode("utf-8")).hexdigest()[:16]
    fields = {
        "request": "xmatch",
        "distMaxArcsec": "2",
        "RESPONSEFORMAT": "csv",
        "cat2": "vizier:II/328/allwise",
        "colRA1": "ra",
        "colDec1": "dec",
    }
    body = bytearray()
    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode("utf-8"))
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(b'Content-Disposition: form-data; name="cat1"; filename="miras.csv"\r\n')
    body.extend(b"Content-Type: text/csv\r\n\r\n")
    body.extend(csv_payload.encode("utf-8"))
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    request = urllib.request.Request(
        CDS_XMATCH_URL,
        data=bytes(body),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "mc-atlas-data-prep/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        path.write_bytes(response.read())


def parse_mira_allwise_xmatch(path: Path) -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            obj_id = row.get("id")
            if not obj_id:
                continue
            angular_distance = parse_float(row.get("angDist", ""))
            existing = rows.get(obj_id)
            if existing is not None and angular_distance is not None and angular_distance >= float(existing["angDist"]):
                continue
            magnitudes: dict[str, float] = {}
            errors: dict[str, float] = {}
            for band in ("W1", "W2", "W3"):
                mag = parse_float(row.get(f"{band}mag", ""))
                err = parse_float(row.get(f"e_{band}mag", ""))
                if valid_mira_mid_ir_value(mag):
                    magnitudes[band] = float(mag)
                if valid_mira_mid_ir_value(err):
                    errors[band] = float(err)
            rows[obj_id] = {
                "angDist": angular_distance if angular_distance is not None else 999.0,
                "magnitudes": magnitudes,
                "errors": errors,
            }
    return rows


def estimate_mira_distance(
    star: CatalogStar,
    period: float,
    chemistry: str | None,
    magnitudes: dict[str, float],
    errors: dict[str, float],
    source_prefix: str,
    already_corrected: bool,
    magnitude_error_floor: dict[str, float] | None = None,
) -> dict[str, float | str] | None:
    if chemistry is None or period <= 0:
        return None

    candidates: list[dict[str, float | str]] = []
    for band, mag in magnitudes.items():
        if band == "W4" or not valid_mira_mid_ir_value(mag):
            continue
        absolute = mira_absolute_magnitude(period, chemistry, band)
        if absolute is None:
            continue
        absolute_mag, coefficient_error, plr_scatter = absolute
        extinction = mira_mid_ir_extinction(star, band, already_corrected)
        distance_modulus = mag - extinction - absolute_mag
        distance = distance_modulus_to_kpc(distance_modulus)
        if not (MIRA_DISTANCE_VALID_RANGE_KPC[0] <= distance <= MIRA_DISTANCE_VALID_RANGE_KPC[1]):
            continue
        photometric_error = errors.get(band, 0.05)
        if magnitude_error_floor is not None:
            photometric_error = math.sqrt(photometric_error**2 + magnitude_error_floor.get(band, 0.0) ** 2)
        modulus_error = math.sqrt(photometric_error**2 + coefficient_error**2 + plr_scatter**2)
        candidates.append(
            {
                "distance": distance,
                "distanceModulus": distance_modulus,
                "distanceError": distance_error_from_modulus(distance, modulus_error),
                "modulusError": modulus_error,
                "source": f"{source_prefix} {band} PLR",
            }
        )

    if not candidates:
        return None
    candidates.sort(key=lambda item: float(item["modulusError"]))
    return candidates[0]


def estimate_mira_distance_from_neighbors(star: CatalogStar, estimated_stars: list[CatalogStar]) -> dict[str, float | str] | None:
    neighbors: list[tuple[float, CatalogStar]] = []
    for neighbor in estimated_stars:
        if neighbor.location != star.location or neighbor.distance_source is None or neighbor.distance_error is None:
            continue
        angular_distance = math.sqrt(angular_distance_sq_deg(star.ra, star.dec, neighbor.ra, neighbor.dec))
        if angular_distance <= MIRA_LOCAL_NEIGHBOR_MAX_ANGULAR_DEG:
            neighbors.append((angular_distance, neighbor))

    neighbors.sort(key=lambda item: item[0])
    selected = neighbors[:MIRA_LOCAL_NEIGHBOR_K]
    if len(selected) < MIRA_LOCAL_NEIGHBOR_MIN_NEIGHBORS:
        return None

    distances = [neighbor.distance for _, neighbor in selected]
    weights = [1.0 / max(angular_distance, 0.05) for angular_distance, _ in selected]
    distance = weighted_median(distances, weights)
    scatter = float(np.median([abs(value - distance) for value in distances])) * 1.4826 if len(distances) > 1 else 0.0
    propagated_error = math.sqrt(
        float(np.median([neighbor.distance_error or 0.0 for _, neighbor in selected])) ** 2
        + max(scatter, MIRA_LOCAL_NEIGHBOR_ERROR_FLOOR_KPC) ** 2
    )
    return {
        "distance": distance,
        "distanceModulus": kpc_to_distance_modulus(distance),
        "distanceError": propagated_error,
        "modulusError": 5.0 * propagated_error / (math.log(10) * distance),
        "source": f"same-cloud {MIRA_LOCAL_NEIGHBOR_K}-neighbor Mira distance estimate",
    }


def apply_mira_distances(miras: list[CatalogStar]) -> dict[str, object]:
    iwanek_rows = parse_iwanek2021_mira_table()
    lmc_miras = [star for star in miras if star.location == "LMC"]
    smc_miras = [star for star in miras if star.location == "SMC"]
    download_mira_allwise_xmatch(lmc_miras, LMC_MIRA_ALLWISE_XMATCH)
    download_mira_allwise_xmatch(smc_miras, SMC_MIRA_ALLWISE_XMATCH)
    lmc_allwise_rows = parse_mira_allwise_xmatch(LMC_MIRA_ALLWISE_XMATCH)
    smc_allwise_rows = parse_mira_allwise_xmatch(SMC_MIRA_ALLWISE_XMATCH)
    smc_allwise_estimates: dict[str, dict[str, float | str]] = {}
    smc_allwise_moduli: list[float] = []
    for star in smc_miras:
        row = smc_allwise_rows.get(star.obj_id)
        if row is None:
            continue
        estimate = estimate_mira_distance(
            star,
            star.period,
            mira_chemistry_key(star.mode),
            row["magnitudes"],  # type: ignore[arg-type]
            row["errors"],  # type: ignore[arg-type]
            "AllWISE xmatch + Iwanek+2021",
            already_corrected=False,
            magnitude_error_floor=MIRA_ALLWISE_MAG_ERROR_FLOOR,
        )
        if estimate is None:
            continue
        smc_allwise_estimates[star.obj_id] = estimate
        smc_allwise_moduli.append(float(estimate["distanceModulus"]))

    estimated = 0
    fallback = 0
    errors: list[float] = []
    relative_errors: list[float] = []
    source_counts: dict[str, int] = {}

    def assign_mira_estimate(star: CatalogStar, estimate: dict[str, float | str]) -> None:
        nonlocal estimated
        star.distance = float(estimate["distance"])
        star.distance_error = float(estimate["distanceError"])
        star.distance_source = str(estimate["source"])
        star.vector = equatorial_to_galactic_vector(star.ra, star.dec, star.distance)
        estimated += 1

    for star in miras:
        estimate: dict[str, float | str] | None = None
        if star.location == "LMC":
            row = iwanek_rows.get(star.obj_id)
            if row is not None:
                period = float(row["period"]) if row["period"] is not None else star.period
                chemistry = mira_chemistry_key(str(row["chemistry"])) or mira_chemistry_key(star.mode)
                estimate = estimate_mira_distance(
                    star,
                    period,
                    chemistry,
                    row["magnitudes"],  # type: ignore[arg-type]
                    row["errors"],  # type: ignore[arg-type]
                    "Iwanek+2021 published mean",
                    already_corrected=True,
                )
                if period > 0:
                    star.period = period
                    if star.light_curve is not None:
                        star.light_curve["period"] = period
                        star.light_curve["t0"] = stable_unit_interval(f"{star.obj_id}-mira-phase") * period
                    synchronize_mira_primary_period(star, period)
                if chemistry is not None:
                    star.mode = chemistry_label(chemistry)
                    if star.light_curve is not None:
                        star.light_curve["subtype"] = f"Mira {star.mode}"
            if estimate is None:
                row = lmc_allwise_rows.get(star.obj_id)
                if row is not None:
                    estimate = estimate_mira_distance(
                        star,
                        star.period,
                        mira_chemistry_key(star.mode),
                        row["magnitudes"],  # type: ignore[arg-type]
                        row["errors"],  # type: ignore[arg-type]
                        "AllWISE xmatch + Iwanek+2021",
                        already_corrected=False,
                        magnitude_error_floor=MIRA_ALLWISE_MAG_ERROR_FLOOR,
                    )
        elif star.location == "SMC":
            estimate = smc_allwise_estimates.get(star.obj_id)

        if estimate is not None:
            assign_mira_estimate(star, estimate)

    estimated_stars = [star for star in miras if star.distance_source is not None]
    for star in miras:
        if star.distance_source is not None:
            continue
        estimate = estimate_mira_distance_from_neighbors(star, estimated_stars)
        if estimate is not None:
            assign_mira_estimate(star, estimate)
            estimated_stars.append(star)

    for star in miras:
        if star.distance_source is None:
            fallback += 1
            star.distance_error = MIRA_CLOUD_DISTANCE_ERRORS_KPC.get(star.location)
            star.distance_source = f"{star.location} geometric mean fallback"
        if star.distance_error is not None:
            errors.append(star.distance_error)
            relative_errors.append(star.distance_error / star.distance)
        if star.distance_source:
            source_counts[star.distance_source] = source_counts.get(star.distance_source, 0) + 1

    return {
        "miraDistanceEstimates": estimated,
        "miraDistanceFallbacks": fallback,
        "miraDistanceSourceCounts": source_counts,
        "miraDistanceMedianErrorKpc": round_number(float(np.median(errors)), 3) if errors else None,
        "miraDistanceMedianRelativeError": round_number(float(np.median(relative_errors)), 4) if relative_errors else None,
        "miraSmcAllwiseMedianDistanceKpc": round_number(distance_modulus_to_kpc(float(np.median(smc_allwise_moduli))), 3) if smc_allwise_moduli else None,
    }


def parse_cepheids(path: Path) -> list[CatalogStar]:
    stars: list[CatalogStar] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 19:
            continue

        location, obj_id, mode = parts[0], parts[1], parts[2]
        if obj_id in RECLASSIFIED_CLASSICAL_CEPHEIDS:
            continue
        period = float(parts[3])
        i_mag = float(parts[4])
        v_mag = float(parts[5])
        ra = hms_to_degrees(parts[7])
        dec = dms_to_degrees(parts[8])
        distance = float(parts[9])
        age = float(parts[17])
        stars.append(
            CatalogStar(
                dataset="cepheids",
                location=location,
                obj_id=obj_id,
                period=period,
                i_mag=i_mag,
                v_mag=v_mag,
                ra=ra,
                dec=dec,
                distance=distance,
                vector=equatorial_to_galactic_vector(ra, dec, distance),
                age=age,
                mode=mode,
            )
        )
    return stars


def parse_rr_lyrae(path: Path) -> list[CatalogStar]:
    stars: list[CatalogStar] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 18:
            continue

        location, obj_id = parts[0], parts[1]
        period = float(parts[2])
        i_mag = float(parts[3])
        v_mag = float(parts[4])
        feh = float(parts[6])
        ra = hms_to_degrees(parts[8])
        dec = dms_to_degrees(parts[9])
        distance = float(parts[10])
        stars.append(
            CatalogStar(
                dataset="rrlyrae",
                location=location,
                obj_id=obj_id,
                period=period,
                i_mag=i_mag,
                v_mag=v_mag,
                ra=ra,
                dec=dec,
                distance=distance,
                vector=equatorial_to_galactic_vector(ra, dec, distance),
                feh=feh,
            )
        )
    return stars


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


def distance_modulus_to_kpc(mu0: float) -> float:
    return 10 ** ((mu0 - 10) / 5)


def smooth_unit(value: float) -> float:
    value = clamp_float(value, (0.0, 1.0))
    return value * value * (3 - 2 * value)


def cluster_mass_segregation_strength(log_age: float) -> float:
    age_gyr = 10 ** (log_age - 9)
    relaxed_unit = (math.log10(max(age_gyr, 0.01)) - math.log10(0.1)) / (math.log10(10.0) - math.log10(0.1))
    return round_number(0.7 * smooth_unit(relaxed_unit), 3)


_CLUSTER_PROFILE_CDF_CACHE: dict[tuple[str, float, float, float], tuple[np.ndarray, np.ndarray]] = {}


def plummer_scale_fraction_for_containment(containment: float) -> float:
    containment = clamp_float(containment, (0.01, 0.99))
    containment_q = containment ** (2 / 3)
    return math.sqrt((1 - containment_q) / containment_q)


def cluster_spatial_profile(cluster: ClusterParameters) -> tuple[str, float, float, float]:
    radius_pc = max(cluster.radius_pc, 0.5)
    core_fraction = (
        cluster.core_radius_pc / radius_pc
        if cluster.core_radius_pc is not None and cluster.core_radius_pc > 0
        else CLUSTER_DEFAULT_CORE_RADIUS_FRACTION
    )
    core_fraction = clamp_float(core_fraction, (CLUSTER_MIN_CORE_RADIUS_FRACTION, CLUSTER_MAX_CORE_RADIUS_FRACTION))

    if (
        cluster.log_age > CLUSTER_EFF_MAX_LOG_AGE
        and cluster.core_radius_pc is not None
        and cluster.tidal_radius_pc is not None
        and cluster.king_concentration is not None
        and cluster.tidal_radius_pc > cluster.core_radius_pc
        and (cluster.fc is None or cluster.fc < 4)
    ):
        outer_fraction = clamp_float(
            cluster.tidal_radius_pc / radius_pc,
            (1.05, CLUSTER_KING_MAX_TIDAL_RADIUS_MULTIPLIER),
        )
        return "king", core_fraction, outer_fraction, cluster.king_concentration

    if cluster.log_age <= CLUSTER_EFF_MAX_LOG_AGE:
        return "eff", core_fraction, CLUSTER_EFF_TRUNCATION_RADIUS_MULTIPLIER, CLUSTER_EFF_GAMMA

    scale_fraction = plummer_scale_fraction_for_containment(CLUSTER_SPATIAL_RADIUS_CONTAINMENT_FRACTION)
    return "plummer", scale_fraction, CLUSTER_SPATIAL_TRUNCATION_RADIUS_MULTIPLIER, 0.0


def cluster_profile_cdf(profile_type: str, core_fraction: float, outer_fraction: float, gamma: float) -> tuple[np.ndarray, np.ndarray]:
    safe_core = max(core_fraction, CLUSTER_MIN_CORE_RADIUS_FRACTION)
    safe_outer = max(outer_fraction, 1.01)
    key = (profile_type, round(safe_core, 4), round(safe_outer, 4), round(gamma, 3))
    cached = _CLUSTER_PROFILE_CDF_CACHE.get(key)
    if cached is not None:
        return cached

    radii = np.linspace(0, safe_outer, CLUSTER_SPATIAL_CDF_GRID_SIZE)
    scaled_radius_sq = (radii / safe_core) ** 2
    if profile_type == "king":
        tidal_term = 1 / math.sqrt(1 + (safe_outer / safe_core) ** 2)
        density = np.maximum(1 / np.sqrt(1 + scaled_radius_sq) - tidal_term, 0) ** 2
    elif profile_type == "eff":
        density = (1 + scaled_radius_sq) ** (-(max(gamma, 2.05) + 1) / 2)
    else:
        density = (1 + scaled_radius_sq) ** -2.5

    pdf = radii * radii * density
    increments = (pdf[:-1] + pdf[1:]) * 0.5 * np.diff(radii)
    cdf = np.concatenate(([0.0], np.cumsum(increments)))
    if cdf[-1] <= 0:
        cdf = (radii / safe_outer) ** 3
    else:
        cdf /= cdf[-1]
    _CLUSTER_PROFILE_CDF_CACHE[key] = (radii, cdf)
    return radii, cdf


def sample_cluster_radial_distances(
    rng: np.random.Generator,
    radius_kpc: float,
    mass_radius_scale: np.ndarray,
    profile: tuple[str, float, float, float],
) -> np.ndarray:
    if mass_radius_scale.size == 0:
        return mass_radius_scale.copy()

    radii, cdf = cluster_profile_cdf(*profile)
    unit_radius = np.interp(rng.random(mass_radius_scale.size), cdf, radii)
    return radius_kpc * mass_radius_scale * unit_radius


def load_asteca_cluster_flags(path: Path) -> dict[str, dict[str, object]]:
    flags: dict[str, dict[str, object]] = {}
    age_outlier_next = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            if line.startswith("#>>>"):
                delta_match = re.search(r",\s*([-+]?\d+(?:\.\d+)?)\s*$", line)
                age_outlier_next = bool(delta_match and abs(float(delta_match.group(1))) > 0.5)
            continue

        parts = line.split()
        if len(parts) < 45:
            age_outlier_next = False
            continue
        name = parts[0]
        flag_values = {
            "M1": int(parts[32]),
            "M2": int(parts[33]),
            **{f"f{index}": int(parts[33 + index]) for index in range(1, 11)},
        }
        active_flags = [label for label, value in flag_values.items() if value]
        flags[name] = {
            "r_cl": finite_float(parts[5]),
            "r_c": finite_float(parts[7]),
            "r_t": finite_float(parts[9]),
            "kcp": finite_float(parts[11]),
            "ci": finite_float(parts[12]),
            "prob_cl": finite_float(parts[18]),
            "fc": int(parts[44]),
            "quality_flags": ",".join(active_flags) if active_flags else "none",
            "age_outlier": age_outlier_next,
        }
        age_outlier_next = False
    return flags


def parse_perren_clusters(path: Path, asteca_path: Path) -> list[ClusterParameters]:
    asteca_flags = load_asteca_cluster_flags(asteca_path)
    clusters: list[ClusterParameters] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 15:
            continue
        flag_info = asteca_flags.get(parts[0], {})
        radius_pc = float(parts[4])
        asteca_radius = flag_info.get("r_cl")
        pixel_to_pc = radius_pc / asteca_radius if isinstance(asteca_radius, float) and asteca_radius > 0 else None
        asteca_core = flag_info.get("r_c")
        asteca_tidal = flag_info.get("r_t")
        clusters.append(
            ClusterParameters(
                name=parts[0],
                galaxy=parts[1],
                ra=float(parts[2]),
                dec=float(parts[3]),
                radius_pc=radius_pc,
                feh=float(parts[5]),
                e_feh=float(parts[6]),
                log_age=float(parts[7]),
                e_log_age=float(parts[8]),
                ebv=float(parts[9]),
                e_ebv=float(parts[10]),
                mu0=float(parts[11]),
                e_mu0=float(parts[12]),
                mass=float(parts[13]),
                e_mass=float(parts[14]),
                ci=flag_info.get("ci"),  # type: ignore[arg-type]
                prob_cl=flag_info.get("prob_cl"),  # type: ignore[arg-type]
                fc=flag_info.get("fc"),  # type: ignore[arg-type]
                core_radius_pc=asteca_core * pixel_to_pc if isinstance(asteca_core, float) and asteca_core > 0 and pixel_to_pc else None,
                tidal_radius_pc=asteca_tidal * pixel_to_pc if isinstance(asteca_tidal, float) and asteca_tidal > 0 and pixel_to_pc else None,
                king_concentration=flag_info.get("kcp") if isinstance(flag_info.get("kcp"), float) and flag_info.get("kcp") > 0 else None,
                quality_flags=str(flag_info.get("quality_flags", "none")),
                age_outlier=bool(flag_info.get("age_outlier", False)),
            )
        )
    return clusters


def mist_feh_from_filename(path: Path) -> float | None:
    match = re.search(r"feh_([mp])(\d+(?:\.\d+)?)_afe_p0(?:\.0)?_vvcrit\d+(?:\.\d+)?", path.name)
    if not match:
        return None
    raw_value = match.group(2)
    value = float(raw_value) if "." in raw_value else int(raw_value) / 100
    return value if match.group(1) == "p" else -value


def mist_file_label(path: Path) -> str:
    name = path.name
    for suffix in (".iso.UBVRIplus", ".iso.cmd", ".iso"):
        if name.lower().endswith(suffix.lower()):
            return name[: -len(suffix)]
    return path.stem


def is_mist_cmd_file(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".iso.cmd") or name.endswith(".iso.ubvriplus")


def available_mist_cmd_files() -> list[tuple[float, Path, str]]:
    files: list[tuple[float, Path, str]] = []
    for path in MIST_DIR.rglob("*"):
        if not path.is_file() or not is_mist_cmd_file(path):
            continue
        if "UBVRI" not in str(path).upper():
            continue
        feh = mist_feh_from_filename(path)
        if feh is not None:
            files.append((feh, path, mist_file_label(path)))
    non_rotating = [item for item in files if "vvcrit0.0" in item[1].name]
    return sorted(non_rotating or files, key=lambda item: item[0])


def available_mist_files() -> list[tuple[float, Path, str]]:
    files = available_mist_cmd_files()
    if files:
        return files

    for path in MIST_DIR.rglob("*_afe_p0_vvcrit0.0_full.iso"):
        feh = mist_feh_from_filename(path)
        if feh is not None:
            files.append((feh, path, mist_file_label(path)))
    return sorted(files, key=lambda item: item[0])


def mist_log_age_grid() -> tuple[float, ...]:
    return tuple(round(CLUSTER_ISOCHRONE_AGE_MIN + index * CLUSTER_ISOCHRONE_AGE_STEP, 2) for index in range(CLUSTER_ISOCHRONE_AGE_COUNT))


def nearest_by_value(values: list[float] | tuple[float, ...], target: float) -> float:
    return min(values, key=lambda value: abs(value - target))


def nearest_mist_file(files: list[tuple[float, Path, str]], target_feh: float) -> tuple[float, Path, str]:
    return min(files, key=lambda item: abs(item[0] - target_feh))


def bracketing_grid_values(values: list[float] | tuple[float, ...], target: float) -> tuple[float, float]:
    if target <= values[0]:
        return values[0], values[0]
    if target >= values[-1]:
        return values[-1], values[-1]
    right_index = bisect.bisect_left(values, target)
    if values[right_index] == target:
        return values[right_index], values[right_index]
    return values[right_index - 1], values[right_index]


def bracketing_mist_files(
    files: list[tuple[float, Path, str]],
    target_feh: float,
) -> tuple[tuple[float, Path, str], tuple[float, Path, str]]:
    if target_feh <= files[0][0]:
        return files[0], files[0]
    if target_feh >= files[-1][0]:
        return files[-1], files[-1]
    feh_values = [item[0] for item in files]
    right_index = bisect.bisect_left(feh_values, target_feh)
    if feh_values[right_index] == target_feh:
        return files[right_index], files[right_index]
    return files[right_index - 1], files[right_index]


def cluster_uncertainty_range(center: float, error: float, minimum: float, maximum: float) -> tuple[float, float]:
    sigma = max(float(error or 0), 0.0) * CLUSTER_ISOCHRONE_UNCERTAINTY_SIGMA
    low = center - sigma
    high = center + sigma
    if sigma <= 0:
        low = high = center
    low = clamp_float(low, (minimum, maximum))
    high = clamp_float(high, (minimum, maximum))
    if low > high:
        low, high = high, low
    return low, high


def support_grid_values(values: list[float] | tuple[float, ...], low: float, high: float) -> list[float]:
    left, _ = bracketing_grid_values(values, low)
    _, right = bracketing_grid_values(values, high)
    left_index = values.index(left)
    right_index = values.index(right)
    return list(values[left_index : right_index + 1])


def support_mist_files(
    files: list[tuple[float, Path, str]],
    low: float,
    high: float,
) -> list[tuple[float, Path, str]]:
    left, _ = bracketing_mist_files(files, low)
    _, right = bracketing_mist_files(files, high)
    left_index = files.index(left)
    right_index = files.index(right)
    return files[left_index : right_index + 1]


def choose_cluster_isochrone_specs(
    cluster: ClusterParameters,
    mist_files: list[tuple[float, Path, str]],
) -> list[tuple[float, float, str]]:
    age_grid = mist_log_age_grid()
    feh_low, feh_high = cluster_uncertainty_range(cluster.feh, cluster.e_feh, mist_files[0][0], mist_files[-1][0])
    age_low, age_high = cluster_uncertainty_range(cluster.log_age, cluster.e_log_age, age_grid[0], age_grid[-1])
    file_candidates = support_mist_files(mist_files, feh_low, feh_high)
    age_candidates = support_grid_values(age_grid, age_low, age_high)
    return [(feh, age, label) for feh, _path, label in file_candidates for age in age_candidates]


def mist_cache_key(label: str, log_age: float) -> str:
    return f"{label}__age_{log_age:.2f}"


def mist_file_signature(path: Path) -> dict[str, int]:
    stat = path.stat()
    return {"size": stat.st_size, "mtimeNs": stat.st_mtime_ns}


def mist_array_to_isochrone(array: np.ndarray, feh: float, log_age: float, label: str) -> MistIsochrone:
    return MistIsochrone(
        feh=feh,
        log_age=log_age,
        label=label,
        initial_mass=array[:, 0],
        star_mass=array[:, 1],
        i_luminosity=array[:, 2],
        radius=array[:, 3],
        v_minus_i=array[:, 4],
        temperature=array[:, 5],
        spectral=array[:, 6].astype(int),
    )


def parse_mist_isochrone_file(path: Path, ages: set[float]) -> dict[float, np.ndarray]:
    if is_mist_cmd_file(path):
        return parse_mist_cmd_isochrone_file(path, ages)

    wanted = {round(age, 2) for age in ages}
    selected: dict[float, list[list[float]]] = {age: [] for age in wanted}
    fallback: dict[float, list[list[float]]] = {age: [] for age in wanted}
    column_index: dict[str, int] | None = None

    with path.open("r", encoding="ascii", errors="ignore") as handle:
        for raw_line in handle:
            if raw_line.startswith("# EEP"):
                columns = raw_line[1:].split()
                column_index = {name: index for index, name in enumerate(columns)}
                continue
            if not raw_line.strip() or raw_line.startswith("#") or column_index is None:
                continue
            parts = raw_line.split()
            log_age = round(float(parts[column_index["log10_isochrone_age_yr"]]), 2)
            if log_age not in wanted:
                continue
            initial_mass = float(parts[column_index["initial_mass"]])
            star_mass = float(parts[column_index["star_mass"]])
            log_luminosity = float(parts[column_index["log_L"]])
            log_temperature = float(parts[column_index["log_Teff"]])
            log_radius = float(parts[column_index["log_R"]])
            phase = int(float(parts[column_index["phase"]]))
            if not all(math.isfinite(value) for value in (initial_mass, star_mass, log_luminosity, log_temperature, log_radius)):
                continue
            if initial_mass <= 0 or star_mass <= 0:
                continue
            temperature = 10 ** log_temperature
            radius = 10 ** log_radius
            i_luminosity = i_band_luminosity_from_radius_temperature(radius, temperature)
            if i_luminosity <= 0 or not math.isfinite(i_luminosity):
                continue
            v_minus_i = v_minus_i_from_temperature(temperature)
            row = [
                initial_mass,
                star_mass,
                i_luminosity,
                radius,
                v_minus_i,
                temperature,
                float(spectral_index(v_minus_i)),
            ]
            fallback[log_age].append(row)
            if phase <= CLUSTER_RENDER_PHASE_MAX:
                selected[log_age].append(row)

    parsed: dict[float, np.ndarray] = {}
    for age in wanted:
        rows = selected[age] or fallback[age]
        if not rows:
            continue
        array = np.array(rows, dtype=float)
        order = np.argsort(array[:, 0])
        array = array[order]
        unique_mass, unique_index = np.unique(array[:, 0], return_index=True)
        if unique_mass.size >= 2:
            parsed[age] = array[np.sort(unique_index)]
    return parsed


def parse_mist_cmd_isochrone_file(path: Path, ages: set[float]) -> dict[float, np.ndarray]:
    wanted = {round(age, 2) for age in ages}
    selected: dict[float, list[list[float]]] = {age: [] for age in wanted}
    fallback: dict[float, list[list[float]]] = {age: [] for age in wanted}
    column_index: dict[str, int] | None = None

    required_columns = {
        "log10_isochrone_age_yr",
        "initial_mass",
        "log_Teff",
        "log_g",
        "log_L",
        "Bessell_V",
        "Bessell_I",
        "phase",
    }

    with path.open("r", encoding="ascii", errors="ignore") as handle:
        for raw_line in handle:
            if raw_line.startswith("# EEP"):
                columns = raw_line[1:].split()
                column_index = {name: index for index, name in enumerate(columns)}
                if not required_columns.issubset(column_index):
                    missing = ", ".join(sorted(required_columns - set(column_index)))
                    raise ValueError(f"{path.name} is missing required MIST CMD columns: {missing}")
                continue
            if not raw_line.strip() or raw_line.startswith("#") or column_index is None:
                continue
            parts = raw_line.split()
            log_age = round(float(parts[column_index["log10_isochrone_age_yr"]]), 2)
            if log_age not in wanted:
                continue
            initial_mass = float(parts[column_index["initial_mass"]])
            log_temperature = float(parts[column_index["log_Teff"]])
            log_luminosity = float(parts[column_index["log_L"]])
            log_g = float(parts[column_index["log_g"]])
            v_mag = float(parts[column_index["Bessell_V"]])
            i_mag = float(parts[column_index["Bessell_I"]])
            phase = int(float(parts[column_index["phase"]]))
            if not all(
                math.isfinite(value)
                for value in (initial_mass, log_temperature, log_luminosity, log_g, v_mag, i_mag)
            ):
                continue
            if initial_mass <= 0 or abs(v_mag) > 90 or abs(i_mag) > 90:
                continue
            temperature = 10 ** log_temperature
            bolometric_luminosity = 10 ** log_luminosity
            radius = math.sqrt(max(bolometric_luminosity, 1e-12)) * (T_SUN / temperature) ** 2
            star_mass = max(0.0, 10 ** (log_g - LOG_G_SUN) * radius * radius)
            i_luminosity = 10 ** (-0.4 * (i_mag - M_SUN_I))
            v_minus_i = v_mag - i_mag
            if i_luminosity <= 0 or not math.isfinite(i_luminosity):
                continue
            row = [
                initial_mass,
                star_mass if star_mass > 0 else initial_mass,
                i_luminosity,
                radius,
                v_minus_i,
                temperature,
                float(spectral_index(v_minus_i)),
            ]
            fallback[log_age].append(row)
            if phase <= CLUSTER_RENDER_PHASE_MAX:
                selected[log_age].append(row)

    parsed: dict[float, np.ndarray] = {}
    for age in wanted:
        rows = selected[age] or fallback[age]
        if not rows:
            continue
        array = np.array(rows, dtype=float)
        order = np.argsort(array[:, 0])
        array = array[order]
        unique_mass, unique_index = np.unique(array[:, 0], return_index=True)
        if unique_mass.size >= 2:
            parsed[age] = array[np.sort(unique_index)]
    return parsed


def v_minus_i_temperature_anchor_dicts(anchors: tuple[tuple[float, float], ...]) -> list[dict[str, float]]:
    return [
        {
            "vMinusI": round_number(v_minus_i, 3),
            "temperature": round_number(temperature, 1),
        }
        for v_minus_i, temperature in anchors
    ]


def fallback_v_minus_i_temperature_calibration(reason: str) -> dict[str, object]:
    return {
        "source": "fallback-hand-anchors",
        "reason": reason,
        "interpolation": "log-temperature",
        "anchors": v_minus_i_temperature_anchor_dicts(V_MINUS_I_TEMPERATURE_ANCHORS),
        "fileCount": 0,
        "sampleCount": 0,
    }


def v_minus_i_temperature_anchors_from_calibration(calibration: dict[str, object]) -> tuple[tuple[float, float], ...]:
    anchors_raw = calibration.get("anchors")
    anchors: list[tuple[float, float]] = []
    if isinstance(anchors_raw, list):
        for item in anchors_raw:
            if not isinstance(item, dict):
                continue
            v_minus_i = finite_float(item.get("vMinusI"))
            temperature = finite_float(item.get("temperature"))
            if v_minus_i is not None and temperature is not None and temperature > 0:
                anchors.append((v_minus_i, temperature))
    return tuple(sorted(anchors, key=lambda item: item[0])) or V_MINUS_I_TEMPERATURE_ANCHORS


def mist_temperature_calibration_file_key(path: Path) -> str:
    try:
        return path.relative_to(MIST_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def mist_temperature_calibration_file_signatures(files: list[tuple[float, Path, str]]) -> dict[str, dict[str, int]]:
    return {mist_temperature_calibration_file_key(path): mist_file_signature(path) for _feh, path, _label in files}


def merge_mist_temperature_anchors(mist_anchors: list[tuple[float, float]]) -> tuple[tuple[float, float], ...]:
    if not mist_anchors:
        return V_MINUS_I_TEMPERATURE_ANCHORS
    mist_anchors = sorted(mist_anchors, key=lambda item: item[0])
    mist_min = mist_anchors[0][0]
    mist_max = mist_anchors[-1][0]
    margin = MIST_VI_TEMPERATURE_BIN_WIDTH * 2
    merged = [anchor for anchor in V_MINUS_I_TEMPERATURE_ANCHORS if anchor[0] < mist_min - margin]
    merged.extend(mist_anchors)
    merged.extend(anchor for anchor in V_MINUS_I_TEMPERATURE_ANCHORS if anchor[0] > mist_max + margin)
    clean: list[tuple[float, float]] = []
    last_color: float | None = None
    for v_minus_i, temperature in sorted(merged, key=lambda item: item[0]):
        if last_color is not None and abs(v_minus_i - last_color) < 1e-9:
            clean[-1] = (v_minus_i, temperature)
        else:
            clean.append((v_minus_i, temperature))
        last_color = v_minus_i
    return tuple(clean)


def parse_mist_cmd_vi_temperature_samples(path: Path, bins: list[list[tuple[float, float]]]) -> int:
    column_index: dict[str, int] | None = None
    required_columns = {"log_Teff", "Bessell_V", "Bessell_I", "phase"}
    sample_count = 0
    with path.open("r", encoding="ascii", errors="ignore") as handle:
        for raw_line in handle:
            if raw_line.startswith("# EEP"):
                columns = raw_line[1:].split()
                column_index = {name: index for index, name in enumerate(columns)}
                if not required_columns.issubset(column_index):
                    return sample_count
                continue
            if not raw_line.strip() or raw_line.startswith("#") or column_index is None:
                continue
            parts = raw_line.split()
            log_temperature = float(parts[column_index["log_Teff"]])
            v_mag = float(parts[column_index["Bessell_V"]])
            i_mag = float(parts[column_index["Bessell_I"]])
            phase = int(float(parts[column_index["phase"]]))
            if phase > MIST_VI_TEMPERATURE_PHASE_MAX:
                continue
            if not all(math.isfinite(value) for value in (log_temperature, v_mag, i_mag)):
                continue
            if abs(v_mag) > 90 or abs(i_mag) > 90:
                continue
            v_minus_i = v_mag - i_mag
            if not MIST_VI_TEMPERATURE_COLOR_MIN <= v_minus_i <= MIST_VI_TEMPERATURE_COLOR_MAX:
                continue
            bin_index = int((v_minus_i - MIST_VI_TEMPERATURE_COLOR_MIN) / MIST_VI_TEMPERATURE_BIN_WIDTH)
            if 0 <= bin_index < len(bins):
                bins[bin_index].append((v_minus_i, log_temperature))
                sample_count += 1
    return sample_count


def build_mist_v_minus_i_temperature_calibration() -> dict[str, object]:
    files = available_mist_cmd_files()
    if not files:
        return fallback_v_minus_i_temperature_calibration("UBVRIplus MIST CMD files not found under data/mist")

    file_signatures = mist_temperature_calibration_file_signatures(files)
    if MIST_VI_TEMPERATURE_CACHE.exists():
        try:
            cached = json.loads(MIST_VI_TEMPERATURE_CACHE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            cached = None
        if (
            isinstance(cached, dict)
            and cached.get("version") == MIST_VI_TEMPERATURE_CACHE_VERSION
            and cached.get("files") == file_signatures
        ):
            return cached

    bin_count = int((MIST_VI_TEMPERATURE_COLOR_MAX - MIST_VI_TEMPERATURE_COLOR_MIN) / MIST_VI_TEMPERATURE_BIN_WIDTH) + 1
    bins: list[list[tuple[float, float]]] = [[] for _ in range(bin_count)]
    sample_count = 0
    for _feh, path, _label in files:
        sample_count += parse_mist_cmd_vi_temperature_samples(path, bins)

    mist_anchors: list[tuple[float, float]] = []
    for samples in bins:
        if len(samples) < MIST_VI_TEMPERATURE_MIN_BIN_COUNT:
            continue
        color_values = np.array([sample[0] for sample in samples], dtype=float)
        log_temperature_values = np.array([sample[1] for sample in samples], dtype=float)
        color = float(np.median(color_values))
        temperature = float(10 ** np.median(log_temperature_values))
        mist_anchors.append((color, temperature))

    if len(mist_anchors) < 4:
        return fallback_v_minus_i_temperature_calibration("UBVRIplus files did not yield enough V-I/Teff samples")

    anchors = merge_mist_temperature_anchors(mist_anchors)
    calibration = {
        "version": MIST_VI_TEMPERATURE_CACHE_VERSION,
        "source": "MIST-UBVRIplus-Bessell-VI",
        "bands": ["Bessell_V", "Bessell_I"],
        "temperatureColumn": "log_Teff",
        "phaseMax": MIST_VI_TEMPERATURE_PHASE_MAX,
        "binWidth": MIST_VI_TEMPERATURE_BIN_WIDTH,
        "interpolation": "log-temperature",
        "anchors": v_minus_i_temperature_anchor_dicts(anchors),
        "fileCount": len(files),
        "sampleCount": sample_count,
        "files": file_signatures,
    }
    PROCESSED.mkdir(parents=True, exist_ok=True)
    MIST_VI_TEMPERATURE_CACHE.write_text(json.dumps(calibration, indent=2, sort_keys=True), encoding="utf-8")
    return calibration


def mist_temperature_anchor_signature(anchors: tuple[tuple[float, float], ...]) -> str:
    payload = json.dumps(v_minus_i_temperature_anchor_dicts(anchors), separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def fallback_vi_luminosity_temperature_calibration(
    reason: str,
    one_d_anchors: tuple[tuple[float, float], ...],
) -> dict[str, object]:
    return {
        "version": MIST_VI_LUMINOSITY_TEMPERATURE_CACHE_VERSION,
        "source": "fallback-one-dimensional-vi",
        "available": False,
        "reason": reason,
        "fallbackAnchorSignature": mist_temperature_anchor_signature(one_d_anchors),
        "fileCount": 0,
        "sampleCount": 0,
    }


def parse_mist_cmd_vi_luminosity_temperature_samples(
    path: Path,
    feh_index: int,
    sum_log_temperature: np.ndarray,
    counts: np.ndarray,
) -> int:
    column_index: dict[str, int] | None = None
    required_columns = {"log_Teff", "Bessell_V", "Bessell_I", "phase"}
    sample_count = 0
    with path.open("r", encoding="ascii", errors="ignore") as handle:
        for raw_line in handle:
            if raw_line.startswith("# EEP"):
                columns = raw_line[1:].split()
                column_index = {name: index for index, name in enumerate(columns)}
                if not required_columns.issubset(column_index):
                    return sample_count
                continue
            if not raw_line.strip() or raw_line.startswith("#") or column_index is None:
                continue
            parts = raw_line.split()
            try:
                log_temperature = float(parts[column_index["log_Teff"]])
                v_mag = float(parts[column_index["Bessell_V"]])
                i_mag = float(parts[column_index["Bessell_I"]])
                phase = int(float(parts[column_index["phase"]]))
            except (IndexError, ValueError):
                continue
            if phase > MIST_VI_TEMPERATURE_PHASE_MAX:
                continue
            if not all(math.isfinite(value) for value in (log_temperature, v_mag, i_mag)):
                continue
            if abs(v_mag) > 90 or abs(i_mag) > 90:
                continue

            v_minus_i = v_mag - i_mag
            log_i_luminosity = -0.4 * (i_mag - M_SUN_I)
            if not MIST_VI_TEMPERATURE_COLOR_MIN <= v_minus_i <= MIST_VI_TEMPERATURE_COLOR_MAX:
                continue
            if not (
                MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MIN
                <= log_i_luminosity
                <= MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MAX
            ):
                continue

            color_index = int(round((v_minus_i - MIST_VI_TEMPERATURE_COLOR_MIN) / MIST_VI_TEMPERATURE_BIN_WIDTH))
            lum_index = int(
                round(
                    (log_i_luminosity - MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MIN)
                    / MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_STEP
                )
            )
            if 0 <= color_index < sum_log_temperature.shape[1] and 0 <= lum_index < sum_log_temperature.shape[2]:
                sum_log_temperature[feh_index, color_index, lum_index] += log_temperature
                counts[feh_index, color_index, lum_index] += 1
                sample_count += 1
    return sample_count


def build_mist_vi_luminosity_temperature_calibration(
    one_d_calibration: dict[str, object],
) -> dict[str, object]:
    files = available_mist_cmd_files()
    one_d_anchors = v_minus_i_temperature_anchors_from_calibration(one_d_calibration)
    if not files:
        return fallback_vi_luminosity_temperature_calibration(
            "UBVRIplus MIST CMD files not found under data/mist",
            one_d_anchors,
        )

    file_signatures = mist_temperature_calibration_file_signatures(files)
    fallback_anchor_signature = mist_temperature_anchor_signature(one_d_anchors)
    if MIST_VI_LUMINOSITY_TEMPERATURE_CACHE.exists():
        try:
            cached = json.loads(MIST_VI_LUMINOSITY_TEMPERATURE_CACHE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            cached = None
        if (
            isinstance(cached, dict)
            and cached.get("version") == MIST_VI_LUMINOSITY_TEMPERATURE_CACHE_VERSION
            and cached.get("files") == file_signatures
            and cached.get("fallbackAnchorSignature") == fallback_anchor_signature
        ):
            return cached

    color_count = int(
        round((MIST_VI_TEMPERATURE_COLOR_MAX - MIST_VI_TEMPERATURE_COLOR_MIN) / MIST_VI_TEMPERATURE_BIN_WIDTH)
    ) + 1
    lum_count = int(
        round(
            (MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MAX - MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MIN)
            / MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_STEP
        )
    ) + 1
    feh_values = [round_number(feh, 3) for feh, _path, _label in files]
    sum_log_temperature = np.zeros((len(files), color_count, lum_count), dtype=np.float64)
    counts = np.zeros((len(files), color_count, lum_count), dtype=np.uint32)

    sample_count = 0
    for feh_index, (_feh, path, _label) in enumerate(files):
        sample_count += parse_mist_cmd_vi_luminosity_temperature_samples(
            path,
            feh_index,
            sum_log_temperature,
            counts,
        )

    fallback_log_temperature_by_color = np.array(
        [
            math.log10(
                temperature_from_v_minus_i_anchors(
                    MIST_VI_TEMPERATURE_COLOR_MIN + color_index * MIST_VI_TEMPERATURE_BIN_WIDTH,
                    one_d_anchors,
                )
            )
            for color_index in range(color_count)
        ],
        dtype=np.float64,
    )
    grid_log_temperature = np.empty((len(files), color_count, lum_count), dtype=np.float32)
    lum_indices = np.arange(lum_count, dtype=float)
    for feh_index in range(len(files)):
        for color_index in range(color_count):
            cell_counts = counts[feh_index, color_index]
            populated = np.flatnonzero(cell_counts > 0)
            if populated.size:
                mean_log_temperature = sum_log_temperature[feh_index, color_index, populated] / cell_counts[populated]
                grid_log_temperature[feh_index, color_index] = np.interp(
                    lum_indices,
                    populated.astype(float),
                    mean_log_temperature,
                )
            else:
                grid_log_temperature[feh_index, color_index] = fallback_log_temperature_by_color[color_index]

    encoded_values = np.clip(
        np.rint(grid_log_temperature * MIST_VI_LUMINOSITY_TEMPERATURE_VALUE_SCALE),
        1,
        np.iinfo(np.uint16).max,
    ).astype("<u2", copy=False)
    calibration = {
        "version": MIST_VI_LUMINOSITY_TEMPERATURE_CACHE_VERSION,
        "source": "MIST-UBVRIplus-Bessell-VI-logL-feh",
        "available": True,
        "bands": ["Bessell_V", "Bessell_I"],
        "temperatureColumn": "log_Teff",
        "luminosity": f"I-band luminosity using M_I(Sun)={M_SUN_I:.2f}",
        "phaseMax": MIST_VI_TEMPERATURE_PHASE_MAX,
        "interpolation": "trilinear-log-temperature",
        "missingCellFill": "interpolate along I-band log-luminosity, then fall back to one-dimensional V-I anchors",
        "axes": {
            "vMinusI": {
                "min": MIST_VI_TEMPERATURE_COLOR_MIN,
                "max": MIST_VI_TEMPERATURE_COLOR_MIN + (color_count - 1) * MIST_VI_TEMPERATURE_BIN_WIDTH,
                "step": MIST_VI_TEMPERATURE_BIN_WIDTH,
                "count": color_count,
            },
            "logLuminosity": {
                "min": MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MIN,
                "max": MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_MIN
                + (lum_count - 1) * MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_STEP,
                "step": MIST_VI_LUMINOSITY_TEMPERATURE_LOG_LUM_STEP,
                "count": lum_count,
            },
            "metallicityFeH": feh_values,
        },
        "valueEncoding": "uint16-base64-little-endian-log10K",
        "valueScale": MIST_VI_LUMINOSITY_TEMPERATURE_VALUE_SCALE,
        "values": base64.b64encode(encoded_values.tobytes(order="C")).decode("ascii"),
        "fileCount": len(files),
        "sampleCount": sample_count,
        "populatedCellCount": int(np.count_nonzero(counts)),
        "cellCount": int(counts.size),
        "fallbackAnchorSignature": fallback_anchor_signature,
        "files": file_signatures,
    }
    PROCESSED.mkdir(parents=True, exist_ok=True)
    MIST_VI_LUMINOSITY_TEMPERATURE_CACHE.write_text(
        json.dumps(calibration, separators=(",", ":"), sort_keys=True),
        encoding="utf-8",
    )
    return calibration


def load_mist_isochrones(
    requests: dict[Path, set[float]],
    mist_files: list[tuple[float, Path, str]],
) -> dict[tuple[str, float], MistIsochrone]:
    label_info = {label: (feh, path) for feh, path, label in mist_files}
    arrays: dict[str, np.ndarray] = {}
    meta: dict[str, object] = {"version": 1, "files": {}}
    requested_keys = {
        mist_cache_key(mist_file_label(path), round(age, 2))
        for path, ages in requests.items()
        for age in ages
    }

    if MIST_CLUSTER_ISOCHRONE_CACHE.exists():
        with np.load(MIST_CLUSTER_ISOCHRONE_CACHE, allow_pickle=False) as cached:
            try:
                meta = json.loads(str(cached["__meta__"].item()))
            except Exception:
                meta = {"version": 0, "files": {}}
            if meta.get("version") != MIST_CLUSTER_ISOCHRONE_CACHE_VERSION:
                meta = {"version": 0, "files": {}}
            meta_files = meta.get("files") if isinstance(meta.get("files"), dict) else {}
            for path, ages in requests.items():
                if meta_files.get(path.name) != mist_file_signature(path):
                    continue
                for age in ages:
                    key = mist_cache_key(mist_file_label(path), round(age, 2))
                    if key in cached:
                        arrays[key] = cached[key]

    missing: dict[Path, set[float]] = {}
    for path, ages in requests.items():
        for age in ages:
            key = mist_cache_key(mist_file_label(path), round(age, 2))
            if key not in arrays:
                missing.setdefault(path, set()).add(round(age, 2))

    if missing:
        for path, ages in sorted(missing.items(), key=lambda item: item[0].name):
            for age, array in parse_mist_isochrone_file(path, ages).items():
                arrays[mist_cache_key(mist_file_label(path), age)] = array
        PROCESSED.mkdir(parents=True, exist_ok=True)
        meta = {
            "version": MIST_CLUSTER_ISOCHRONE_CACHE_VERSION,
            "massCutoffSolar": CLUSTER_SYNTHETIC_MASS_CUTOFF,
            "renderPhaseMax": CLUSTER_RENDER_PHASE_MAX,
            "files": {path.name: mist_file_signature(path) for path in requests},
        }
        save_arrays = {key: value for key, value in arrays.items() if key in requested_keys}
        save_arrays["__meta__"] = np.array(json.dumps(meta, sort_keys=True))
        np.savez_compressed(MIST_CLUSTER_ISOCHRONE_CACHE, **save_arrays)

    isochrones: dict[tuple[str, float], MistIsochrone] = {}
    for key, array in arrays.items():
        if key not in requested_keys or array.ndim != 2 or array.shape[1] < 7:
            continue
        label, age_text = key.split("__age_")
        feh, _path = label_info[label]
        log_age = float(age_text)
        isochrones[(label, log_age)] = mist_array_to_isochrone(array, feh, log_age, label)
    return isochrones


_CLUSTER_IMF_GRID: tuple[np.ndarray, np.ndarray, float] | None = None


def cluster_imf_grid() -> tuple[np.ndarray, np.ndarray, float]:
    global _CLUSTER_IMF_GRID
    if _CLUSTER_IMF_GRID is not None:
        return _CLUSTER_IMF_GRID

    edges = np.logspace(math.log10(CLUSTER_IMF_MIN_MASS), math.log10(CLUSTER_IMF_MAX_MASS), CLUSTER_IMF_GRID_SIZE + 1)
    masses = np.sqrt(edges[:-1] * edges[1:])
    dm = np.diff(edges)
    log_mass = np.log10(masses)
    characteristic_mass = 0.22
    sigma = 0.57
    lognormal = np.exp(-((log_mass - math.log10(characteristic_mass)) ** 2) / (2 * sigma * sigma))
    low_mass_dndm = lognormal / (masses * math.log(10))
    dndm_at_one = math.exp(-((0.0 - math.log10(characteristic_mass)) ** 2) / (2 * sigma * sigma)) / math.log(10)
    dndm = np.where(masses <= 1.0, low_mass_dndm, dndm_at_one * masses ** -2.3)
    weights = dndm * dm
    weights = weights / np.sum(weights)
    mean_mass = float(np.sum(weights * masses))
    _CLUSTER_IMF_GRID = (masses, weights, mean_mass)
    return _CLUSTER_IMF_GRID


def visible_cluster_star_count_factor(max_initial_mass: float) -> float:
    masses, weights, mean_mass = cluster_imf_grid()
    mask = (masses >= CLUSTER_SYNTHETIC_MASS_CUTOFF) & (masses <= max_initial_mass)
    if not np.any(mask):
        return 0.0
    return float(np.sum(weights[mask]) / mean_mass)


def sample_cluster_initial_masses(rng: np.random.Generator, count: int, max_initial_mass: float) -> np.ndarray:
    if count <= 0:
        return np.array([], dtype=float)
    masses, weights, _mean_mass = cluster_imf_grid()
    mask = (masses >= CLUSTER_SYNTHETIC_MASS_CUTOFF) & (masses <= max_initial_mass)
    if not np.any(mask):
        return np.array([], dtype=float)
    selected_masses = masses[mask]
    selected_weights = weights[mask]
    cdf = np.cumsum(selected_weights)
    cdf /= cdf[-1]
    return np.interp(rng.random(count), cdf, selected_masses)


def sample_cluster_uncertainty_values(
    rng: np.random.Generator,
    center: float,
    error: float,
    count: int,
    low: float,
    high: float,
) -> np.ndarray:
    if count <= 0:
        return np.array([], dtype=float)
    sigma = max(float(error or 0), 0.0)
    center = clamp_float(center, (low, high))
    if sigma <= 0 or high <= low:
        return np.full(count, center, dtype=float)
    samples = np.empty(count, dtype=float)
    filled = 0
    while filled < count:
        draw_count = max(64, (count - filled) * 2)
        drawn = rng.normal(center, sigma, draw_count)
        accepted = drawn[(drawn >= low) & (drawn <= high)]
        take = min(count - filled, accepted.size)
        if take:
            samples[filled : filled + take] = accepted[:take]
            filled += take
    return samples


def interpolate_isochrone_values(isochrone: MistIsochrone, masses: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "star_mass": np.interp(masses, isochrone.initial_mass, isochrone.star_mass),
        "i_luminosity": np.interp(masses, isochrone.initial_mass, isochrone.i_luminosity),
        "radius": np.interp(masses, isochrone.initial_mass, isochrone.radius),
        "v_minus_i": np.interp(masses, isochrone.initial_mass, isochrone.v_minus_i),
        "temperature": np.interp(masses, isochrone.initial_mass, isochrone.temperature),
        "spectral": np.rint(np.interp(masses, isochrone.initial_mass, isochrone.spectral)).astype(int),
    }


def blend_isochrone_arrays(
    lower_feh_values: dict[str, np.ndarray],
    upper_feh_values: dict[str, np.ndarray],
    feh_weight: np.ndarray,
) -> dict[str, np.ndarray]:
    weight = feh_weight
    return {
        key: lower_feh_values[key] * (1 - weight) + upper_feh_values[key] * weight
        for key in lower_feh_values
    }


def blend_positive_arrays(values: list[np.ndarray], weights: list[np.ndarray]) -> np.ndarray:
    blended = np.zeros_like(values[0], dtype=float)
    for value, weight in zip(values, weights):
        blended += np.log(np.maximum(value, 1e-12)) * weight
    return np.exp(blended)


def interpolate_cluster_isochrone_values(
    isochrones: dict[tuple[str, float], MistIsochrone],
    low_feh_label: str,
    high_feh_label: str,
    low_age: float,
    high_age: float,
    sampled_feh: np.ndarray,
    sampled_log_age: np.ndarray,
    masses: np.ndarray,
) -> dict[str, np.ndarray] | None:
    corners = [
        isochrones.get((low_feh_label, low_age)),
        isochrones.get((high_feh_label, low_age)),
        isochrones.get((low_feh_label, high_age)),
        isochrones.get((high_feh_label, high_age)),
    ]
    if any(corner is None for corner in corners):
        return None
    low_feh_iso, high_feh_iso, low_feh_high_age_iso, high_feh_high_age_iso = corners  # type: ignore[misc]
    feh0 = low_feh_iso.feh
    feh1 = high_feh_iso.feh
    age0 = low_age
    age1 = high_age
    feh_weight = np.zeros_like(sampled_feh) if feh0 == feh1 else np.clip((sampled_feh - feh0) / (feh1 - feh0), 0, 1)
    age_weight = np.zeros_like(sampled_log_age) if age0 == age1 else np.clip((sampled_log_age - age0) / (age1 - age0), 0, 1)

    v00 = interpolate_isochrone_values(low_feh_iso, masses)
    v10 = interpolate_isochrone_values(high_feh_iso, masses)
    v01 = interpolate_isochrone_values(low_feh_high_age_iso, masses)
    v11 = interpolate_isochrone_values(high_feh_high_age_iso, masses)
    weights = [
        (1 - feh_weight) * (1 - age_weight),
        feh_weight * (1 - age_weight),
        (1 - feh_weight) * age_weight,
        feh_weight * age_weight,
    ]
    return {
        "star_mass": v00["star_mass"] * weights[0] + v10["star_mass"] * weights[1] + v01["star_mass"] * weights[2] + v11["star_mass"] * weights[3],
        "i_luminosity": blend_positive_arrays([v00["i_luminosity"], v10["i_luminosity"], v01["i_luminosity"], v11["i_luminosity"]], weights),
        "radius": blend_positive_arrays([v00["radius"], v10["radius"], v01["radius"], v11["radius"]], weights),
        "v_minus_i": v00["v_minus_i"] * weights[0] + v10["v_minus_i"] * weights[1] + v01["v_minus_i"] * weights[2] + v11["v_minus_i"] * weights[3],
        "temperature": blend_positive_arrays([v00["temperature"], v10["temperature"], v01["temperature"], v11["temperature"]], weights),
        "spectral": np.rint(v00["spectral"] * weights[0] + v10["spectral"] * weights[1] + v01["spectral"] * weights[2] + v11["spectral"] * weights[3]).astype(int),
    }


def round_luminosity(value: float) -> float:
    return round_number(value, 4 if value < 1 else 2)


def cluster_isochrone_summary(isochrones: list[MistIsochrone]) -> str:
    if not isochrones:
        return "none"
    feh_values = [iso.feh for iso in isochrones]
    age_values = [iso.log_age for iso in isochrones]
    return (
        f"interpolated MIST ({len(isochrones)} blocks); "
        f"[Fe/H] {min(feh_values):.2f}..{max(feh_values):.2f}; "
        f"log(age) {min(age_values):.2f}..{max(age_values):.2f}"
    )


def serialize_synthetic_clusters(
    clusters: list[ClusterParameters],
    origin: tuple[float, float, float],
    basis: dict[str, tuple[float, float, float]],
) -> tuple[
    list[list[float | int | str | bool | None]],
    list[list[float | int]],
    list[list[float | int]],
    list[list[float | int]],
    dict[str, int | float],
]:
    mist_files = available_mist_files()
    age_grid = mist_log_age_grid()
    mist_path_by_label = {label: path for _feh, path, label in mist_files}
    requests: dict[Path, set[float]] = {}
    for cluster in clusters:
        cluster.iso_specs = choose_cluster_isochrone_specs(cluster, mist_files)
        for _feh, log_age, label in cluster.iso_specs:
            requests.setdefault(mist_path_by_label[label], set()).add(log_age)

    isochrones = load_mist_isochrones(requests, mist_files)
    cluster_rows: list[list[float | int | str | bool | None]] = []
    star_rows: list[list[float | int]] = []
    glow_bin_rows: list[list[float | int]] = []
    hr_bin_rows: list[list[float | int]] = []
    total_expected = 0.0
    total_synthetic_stars = 0
    total_unresolved_stars = 0
    total_unresolved_luminosity = 0.0
    spatial_profile_counts: dict[str, int] = {}

    for cluster_index, cluster in enumerate(clusters):
        rng = np.random.default_rng(stable_seed_int(f"perren-cluster-{cluster.name}"))
        center_vector = equatorial_to_galactic_vector(cluster.ra, cluster.dec, distance_modulus_to_kpc(cluster.mu0))
        center_local = project_local(center_vector, origin, basis)
        gal_lon, gal_lat = vector_to_lon_lat(center_vector)
        distance = vector_length(center_vector)
        cluster_basis = make_basis(center_vector)
        segregation = cluster_mass_segregation_strength(cluster.log_age)
        cluster_isochrones = [
            isochrones[(label, log_age)]
            for _feh, log_age, label in (cluster.iso_specs or [])
            if (label, log_age) in isochrones
            and isochrones[(label, log_age)].initial_mass[-1] >= CLUSTER_SYNTHETIC_MASS_CUTOFF
        ]
        expected_count = cluster.mass * float(np.mean([visible_cluster_star_count_factor(iso.initial_mass[-1]) for iso in cluster_isochrones])) if cluster_isochrones else 0.0
        total_expected += expected_count
        star_count = int(math.floor(expected_count + rng.random())) if expected_count > 0 else 0
        total_synthetic_stars += star_count
        rendered_count = 0
        unresolved_count = 0
        unresolved_luminosity = 0.0
        unresolved_color_luminosity = 0.0
        glow_luminosity_bins = np.zeros(CLUSTER_GLOW_BIN_COUNT, dtype=float)
        glow_color_bins = np.zeros(CLUSTER_GLOW_BIN_COUNT, dtype=float)
        hr_count_bins = np.zeros(
            (CLUSTER_HR_COLOR_BIN_COUNT, CLUSTER_HR_LOG_LUMINOSITY_BIN_COUNT),
            dtype=np.int32,
        )
        hr_color_bins = np.zeros_like(hr_count_bins, dtype=float)
        hr_log_luminosity_bins = np.zeros_like(hr_count_bins, dtype=float)
        hr_luminosity_bins = np.zeros_like(hr_count_bins, dtype=float)
        hr_temperature_bins = np.zeros_like(hr_count_bins, dtype=float)
        hr_radius_bins = np.zeros_like(hr_count_bins, dtype=float)
        radius_kpc = max(cluster.radius_pc, 0.5) / 1000
        spatial_profile = cluster_spatial_profile(cluster)
        spatial_profile_counts[spatial_profile[0]] = spatial_profile_counts.get(spatial_profile[0], 0) + 1

        if star_count and cluster_isochrones:
            feh_low, feh_high = cluster_uncertainty_range(cluster.feh, cluster.e_feh, mist_files[0][0], mist_files[-1][0])
            age_low, age_high = cluster_uncertainty_range(cluster.log_age, cluster.e_log_age, age_grid[0], age_grid[-1])
            sampled_feh = sample_cluster_uncertainty_values(rng, cluster.feh, cluster.e_feh, star_count, feh_low, feh_high)
            sampled_log_age = sample_cluster_uncertainty_values(rng, cluster.log_age, cluster.e_log_age, star_count, age_low, age_high)
            interpolation_groups: dict[tuple[float, str, float, str, float, float], list[int]] = {}
            for sample_index, (sample_feh, sample_log_age) in enumerate(zip(sampled_feh, sampled_log_age)):
                low_file, high_file = bracketing_mist_files(mist_files, float(sample_feh))
                low_age, high_age = bracketing_grid_values(age_grid, float(sample_log_age))
                key = (low_file[0], low_file[2], high_file[0], high_file[2], low_age, high_age)
                interpolation_groups.setdefault(key, []).append(sample_index)

            for (_low_feh, low_label, _high_feh, high_label, low_age, high_age), group_indexes in interpolation_groups.items():
                group_indices = np.array(group_indexes, dtype=int)
                corner_isochrones = [
                    isochrones.get((low_label, low_age)),
                    isochrones.get((high_label, low_age)),
                    isochrones.get((low_label, high_age)),
                    isochrones.get((high_label, high_age)),
                ]
                if any(isochrone is None for isochrone in corner_isochrones):
                    continue
                max_initial_mass = min(float(isochrone.initial_mass[-1]) for isochrone in corner_isochrones if isochrone is not None)
                initial_masses = sample_cluster_initial_masses(rng, group_indices.size, max_initial_mass)
                if initial_masses.size == 0:
                    continue
                values = interpolate_cluster_isochrone_values(
                    isochrones,
                    low_label,
                    high_label,
                    low_age,
                    high_age,
                    sampled_feh[group_indices],
                    sampled_log_age[group_indices],
                    initial_masses,
                )
                if values is None:
                    continue
                mass_weight = np.clip(
                    np.log(np.maximum(initial_masses, CLUSTER_SYNTHETIC_MASS_CUTOFF) / CLUSTER_SYNTHETIC_MASS_CUTOFF)
                    / math.log(8.0 / CLUSTER_SYNTHETIC_MASS_CUTOFF),
                    0,
                    1,
                )
                mass_radius_scale = np.maximum(0.18, 1 - 0.58 * segregation * mass_weight)
                radial_distance = sample_cluster_radial_distances(rng, radius_kpc, mass_radius_scale, spatial_profile)
                cos_theta = rng.uniform(-1, 1, initial_masses.size)
                sin_theta = np.sqrt(np.maximum(0, 1 - cos_theta * cos_theta))
                phi = rng.random(initial_masses.size) * math.tau
                offsets = (
                    radial_distance * sin_theta * np.cos(phi),
                    radial_distance * sin_theta * np.sin(phi),
                    radial_distance * cos_theta,
                )

                east = cluster_basis["east"]
                north = cluster_basis["north"]
                radial = cluster_basis["radial"]
                for item_index, initial_mass in enumerate(initial_masses):
                    vector = (
                        center_vector[0] + offsets[0][item_index] * east[0] + offsets[1][item_index] * north[0] + offsets[2][item_index] * radial[0],
                        center_vector[1] + offsets[0][item_index] * east[1] + offsets[1][item_index] * north[1] + offsets[2][item_index] * radial[1],
                        center_vector[2] + offsets[0][item_index] * east[2] + offsets[1][item_index] * north[2] + offsets[2][item_index] * radial[2],
                    )
                    luminosity = float(values["i_luminosity"][item_index])
                    v_minus_i = float(values["v_minus_i"][item_index])
                    if luminosity < CLUSTER_POINT_LUMINOSITY_CUTOFF:
                        unresolved_count += 1
                        unresolved_luminosity += luminosity
                        unresolved_color_luminosity += luminosity * v_minus_i
                        radius_fraction = max(0.0, float(radial_distance[item_index] / radius_kpc))
                        glow_outer_fraction = max(spatial_profile[2], 1.0)
                        glow_bin = min(CLUSTER_GLOW_BIN_COUNT - 1, int((radius_fraction / glow_outer_fraction) * CLUSTER_GLOW_BIN_COUNT))
                        glow_luminosity_bins[glow_bin] += luminosity
                        glow_color_bins[glow_bin] += luminosity * v_minus_i
                        log_luminosity = math.log10(max(luminosity, 1e-9))
                        color_fraction = (v_minus_i - CLUSTER_HR_COLOR_MIN) / (CLUSTER_HR_COLOR_MAX - CLUSTER_HR_COLOR_MIN)
                        luminosity_fraction = (log_luminosity - CLUSTER_HR_LOG_LUMINOSITY_MIN) / (
                            CLUSTER_HR_LOG_LUMINOSITY_MAX - CLUSTER_HR_LOG_LUMINOSITY_MIN
                        )
                        color_bin = int(np.clip(color_fraction, 0, 0.999999) * CLUSTER_HR_COLOR_BIN_COUNT)
                        luminosity_bin = int(np.clip(luminosity_fraction, 0, 0.999999) * CLUSTER_HR_LOG_LUMINOSITY_BIN_COUNT)
                        hr_count_bins[color_bin, luminosity_bin] += 1
                        hr_color_bins[color_bin, luminosity_bin] += v_minus_i
                        hr_log_luminosity_bins[color_bin, luminosity_bin] += log_luminosity
                        hr_luminosity_bins[color_bin, luminosity_bin] += luminosity
                        hr_temperature_bins[color_bin, luminosity_bin] += float(values["temperature"][item_index])
                        hr_radius_bins[color_bin, luminosity_bin] += float(values["radius"][item_index])
                        continue

                    rendered_count += 1
                    local = project_local(vector, origin, basis)
                    star_lon, star_lat = vector_to_lon_lat(vector)
                    star_ra, star_dec = equatorial_vector_to_ra_dec(galactic_to_equatorial_vector(vector))
                    star_distance = vector_length(vector)
                    star_rows.append(
                        [
                            round_number(local[0], 6),
                            round_number(local[1], 6),
                            round_number(local[2], 6),
                            round_number(math.log10(max(luminosity, 1e-9)), 3),
                            round_luminosity(luminosity),
                            round_number(float(values["radius"][item_index]), 4),
                            int(values["spectral"][item_index]),
                            cluster_index,
                            round_number(float(initial_mass), 4),
                            round_number(float(values["star_mass"][item_index]), 4),
                            round_number(v_minus_i, 3),
                            int(round(float(values["temperature"][item_index]))),
                            round_number(star_ra, 5),
                            round_number(star_dec, 5),
                            round_number(star_lon, 5),
                            round_number(star_lat, 5),
                            round_number(star_distance, 5),
                        ]
                    )

        total_unresolved_stars += unresolved_count
        total_unresolved_luminosity += unresolved_luminosity
        unresolved_v_minus_i = unresolved_color_luminosity / unresolved_luminosity if unresolved_luminosity > 0 else None
        for bin_index, bin_luminosity in enumerate(glow_luminosity_bins):
            if bin_luminosity <= 0:
                continue
            glow_bin_rows.append(
                [
                    cluster_index,
                    round_number(((bin_index + 1) / CLUSTER_GLOW_BIN_COUNT) * max(spatial_profile[2], 1.0), 4),
                    round_luminosity(float(bin_luminosity)),
                    round_number(float(glow_color_bins[bin_index] / bin_luminosity), 3),
                ]
            )
        hr_bin_indexes = np.argwhere(hr_count_bins > 0)
        for color_bin, luminosity_bin in hr_bin_indexes:
            count = int(hr_count_bins[color_bin, luminosity_bin])
            hr_bin_rows.append(
                [
                    cluster_index,
                    round_number(float(hr_color_bins[color_bin, luminosity_bin] / count), 3),
                    round_number(float(hr_log_luminosity_bins[color_bin, luminosity_bin] / count), 3),
                    count,
                    round_luminosity(float(hr_luminosity_bins[color_bin, luminosity_bin])),
                    int(round(float(hr_temperature_bins[color_bin, luminosity_bin] / count))),
                    round_number(float(hr_radius_bins[color_bin, luminosity_bin] / count), 4),
                ]
            )

        cluster_rows.append(
            [
                round_number(center_local[0], 6),
                round_number(center_local[1], 6),
                round_number(center_local[2], 6),
                cluster.name,
                cluster.galaxy,
                round_number(cluster.ra, 6),
                round_number(cluster.dec, 6),
                round_number(gal_lon, 5),
                round_number(gal_lat, 5),
                round_number(distance, 4),
                round_number(cluster.radius_pc, 2),
                round_number(cluster.feh, 2),
                round_number(cluster.e_feh, 2),
                round_number(cluster.log_age, 2),
                round_number(cluster.e_log_age, 2),
                round_number(cluster.ebv, 3),
                round_number(cluster.e_ebv, 3),
                round_number(cluster.mu0, 2),
                round_number(cluster.e_mu0, 2),
                int(round(cluster.mass)),
                int(round(cluster.e_mass)),
                star_count,
                rendered_count,
                unresolved_count,
                round_luminosity(unresolved_luminosity),
                round_number(unresolved_v_minus_i, 3) if unresolved_v_minus_i is not None else None,
                cluster_isochrone_summary(cluster_isochrones),
                cluster.quality_flags,
                round_number(cluster.ci, 2) if cluster.ci is not None else None,
                round_number(cluster.prob_cl, 2) if cluster.prob_cl is not None else None,
                cluster.fc,
                segregation,
                cluster.age_outlier,
            ]
        )

    return cluster_rows, star_rows, glow_bin_rows, hr_bin_rows, {
        "clusters": len(clusters),
        "clusterSyntheticStars": total_synthetic_stars,
        "clusterRenderedStars": len(star_rows),
        "clusterUnresolvedStars": total_unresolved_stars,
        "clusterUnresolvedLuminositySolar": round_luminosity(total_unresolved_luminosity),
        "clusterGlowBins": len(glow_bin_rows),
        "clusterHrBins": len(hr_bin_rows),
        "clusterGlowBinCount": CLUSTER_GLOW_BIN_COUNT,
        "clusterSyntheticExpectedStars": round_number(total_expected, 1),
        "clusterSyntheticMassCutoffSolar": CLUSTER_SYNTHETIC_MASS_CUTOFF,
        "clusterPointLuminosityCutoffSolar": CLUSTER_POINT_LUMINOSITY_CUTOFF,
        "clusterSpatialProfile": "king-eff-plummer",
        "clusterSpatialRadiusContainmentFraction": CLUSTER_SPATIAL_RADIUS_CONTAINMENT_FRACTION,
        "clusterSpatialTruncationRadiusMultiplier": CLUSTER_SPATIAL_TRUNCATION_RADIUS_MULTIPLIER,
        "clusterSpatialProfileModel": "king-eff-plummer",
        "clusterSpatialProfileCounts": spatial_profile_counts,
        "clusterKingMaxTidalRadiusMultiplier": CLUSTER_KING_MAX_TIDAL_RADIUS_MULTIPLIER,
        "clusterEffMaxLogAge": CLUSTER_EFF_MAX_LOG_AGE,
        "clusterEffGamma": CLUSTER_EFF_GAMMA,
        "clusterSyntheticTotalMassSolar": int(round(sum(cluster.mass for cluster in clusters))),
        "clusterSyntheticAgeOutliers": sum(1 for cluster in clusters if cluster.age_outlier),
        "clusterMistIsochroneBlocks": len(isochrones),
    }


def parse_fits_distance_map(
    path: Path,
    origin: tuple[float, float, float],
    basis: dict[str, tuple[float, float, float]],
) -> list[list[float]]:
    raw = path.read_bytes()
    header_end = None
    cards: dict[str, str] = {}
    for offset in range(0, len(raw), 80):
        card = raw[offset : offset + 80].decode("ascii", errors="ignore")
        key = card[:8].strip()
        if key:
            cards[key] = card[10:30].strip()
        if key == "END":
            header_end = ((offset + 80 + 2879) // 2880) * 2880
            break

    if header_end is None:
        raise ValueError(f"No FITS END card found in {path}")

    n1 = int(cards["NAXIS1"])
    n2 = int(cards["NAXIS2"])
    crpix1 = float(cards["CRPIX1"])
    crpix2 = float(cards["CRPIX2"])
    cdelt1 = float(cards["CDELT1"])
    cdelt2 = float(cards["CDELT2"])
    crval1 = float(cards["CRVAL1"])
    crval2 = float(cards["CRVAL2"])

    cells: list[list[float]] = []
    for y in range(n2):
        for x in range(n1):
            offset = header_end + ((y * n1 + x) * 4)
            distance = struct.unpack(">f", raw[offset : offset + 4])[0]
            if not math.isfinite(distance) or distance <= 0 or distance > 200:
                continue

            lon = crval1 + ((x + 1) - crpix1) * cdelt1
            lat = crval2 + ((y + 1) - crpix2) * cdelt2
            local = project_local(galactic_to_vector(lon, lat, distance), origin, basis)
            cells.append(
                [
                    round_number(local[0]),
                    round_number(local[1]),
                    round_number(local[2]),
                    round_number(distance, 2),
                    round_number(lon, 3),
                    round_number(lat, 3),
                ]
            )
    return cells


def red_clump_density_key(lon: float, lat: float, bin_scale: int = 4) -> tuple[int, int]:
    return (round(lon * bin_scale), round(lat * bin_scale))


def density_smoothing_kernel(
    sigma_cells: float = XMC_DENSITY_SMOOTH_SIGMA_CELLS,
    radius_cells: int = XMC_DENSITY_SMOOTH_RADIUS_CELLS,
) -> list[tuple[int, int, float]]:
    kernel: list[tuple[int, int, float]] = []
    for dy in range(-radius_cells, radius_cells + 1):
        for dx in range(-radius_cells, radius_cells + 1):
            distance2 = dx * dx + dy * dy
            if distance2 > radius_cells * radius_cells:
                continue
            weight = math.exp(-0.5 * distance2 / (sigma_cells * sigma_cells))
            kernel.append((dx, dy, weight))
    return kernel


def smoothed_density_count(
    key: tuple[int, int],
    density_counts: dict[tuple[int, int], int],
    kernel: list[tuple[int, int, float]],
) -> float:
    total = 0.0
    total_weight = 0.0
    x, y = key
    for dx, dy, weight in kernel:
        total += density_counts.get((x + dx, y + dy), 0) * weight
        total_weight += weight
    return total / total_weight if total_weight > 0 else 0.0


def load_red_clump_density_counts(path: Path) -> tuple[dict[tuple[int, int], int], dict[str, object] | None]:
    if not path.exists():
        return {}, None

    payload = json.loads(path.read_text(encoding="utf-8"))
    meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
    bin_scale = int(meta.get("binScale", 4))
    density: dict[tuple[int, int], int] = {}
    for item in payload.get("bins", []):
        lon_bin = int(item["lonBin"])
        lat_bin = int(item["latBin"])
        count = int(item["count"])
        if bin_scale == 4:
            key = (lon_bin, lat_bin)
        else:
            key = red_clump_density_key(lon_bin / bin_scale, lat_bin / bin_scale)
        density[key] = density.get(key, 0) + count
    return density, meta


def attach_red_clump_density(
    cells: list[list[float]],
    density_counts: dict[tuple[int, int], int],
) -> dict[str, int | float]:
    if not density_counts:
        for cell in cells:
            cell.extend([0, 1.0])
        return {
            "redClumpDensityBins": 0,
            "redClumpDensityMatchedCells": 0,
            "redClumpDensityCountMax": 0,
            "redClumpDensityCountP98": 0,
        }

    kernel = density_smoothing_kernel()
    counts = []
    for cell in cells:
        key = red_clump_density_key(float(cell[4]), float(cell[5]))
        counts.append(smoothed_density_count(key, density_counts, kernel))
    positive_counts = np.array([count for count in counts if count > 0], dtype=float)
    reference = float(np.percentile(positive_counts, 98)) if positive_counts.size else 1.0
    reference = max(reference, 1.0)

    for cell, count in zip(cells, counts):
        density_unit = math.log1p(count) / math.log1p(reference) if count > 0 else 0.0
        cell.extend([int(round(count)), round_number(clamp_float(density_unit, (0.0, 1.0)), 3)])

    return {
        "redClumpDensityBins": len(density_counts),
        "redClumpDensityMatchedCells": sum(1 for count in counts if count > 0),
        "redClumpDensityCountMax": int(max(counts)) if counts else 0,
        "redClumpDensityCountP98": round_number(reference, 1),
        "redClumpDensitySmoothSigmaCells": XMC_DENSITY_SMOOTH_SIGMA_CELLS,
        "redClumpDensitySmoothRadiusCells": XMC_DENSITY_SMOOTH_RADIUS_CELLS,
    }


def location_to_index(location: str) -> int:
    return LOCATION_INDEX.get(location.upper(), 3)


def serialize_catalog(stars: list[CatalogStar], origin: tuple[float, float, float], basis: dict[str, tuple[float, float, float]]) -> list[list[float | int | str | None]]:
    rows: list[list[float | int | str | None]] = []
    for star in stars:
        local = project_local(star.vector, origin, basis)
        gal_lon, gal_lat = vector_to_lon_lat(star.vector)
        color_index = star.v_mag - star.i_mag
        intrinsic_color_index = color_index - star.reddening_evi
        lum = luminosity_from_i(star.i_mag, star.distance)
        radius = radius_from_luminosity_and_color(lum, intrinsic_color_index)
        mira_periods: list[float] = []
        mira_amplitudes: list[float] = []
        mira_phases: list[float] = []
        mira_amplitudes_v: list[float] = []
        mira_phases_v: list[float] = []
        mira_quality = 0
        mira_v_quality = 0
        mira_source: str | None = None
        mira_v_source: str | None = None
        if star.mira_pulsation:
            mira_periods, mira_amplitudes = mira_component_arrays(star)
            phases_raw = star.mira_pulsation.get("phasesI")
            if isinstance(phases_raw, list):
                for value in phases_raw[: len(mira_periods)]:
                    try:
                        phase = float(value)
                    except (TypeError, ValueError):
                        continue
                    if math.isfinite(phase):
                        mira_phases.append(phase)
            if len(mira_phases) != len(mira_periods):
                mira_periods = []
                mira_amplitudes = []
                mira_phases = []
            if mira_periods:
                try:
                    mira_quality = int(star.mira_pulsation.get("quality", 0))
                except (TypeError, ValueError):
                    mira_quality = 0
                source_raw = star.mira_pulsation.get("source")
                mira_source = str(source_raw) if source_raw else None
                amplitudes_v_raw = star.mira_pulsation.get("amplitudesV")
                phases_v_raw = star.mira_pulsation.get("phasesV")
                if isinstance(amplitudes_v_raw, list) and isinstance(phases_v_raw, list):
                    for amplitude_raw, phase_raw in zip(amplitudes_v_raw[: len(mira_periods)], phases_v_raw[: len(mira_periods)]):
                        amplitude_v = finite_float(amplitude_raw)
                        phase_v = finite_float(phase_raw)
                        if amplitude_v is None or phase_v is None or amplitude_v <= 0:
                            break
                        mira_amplitudes_v.append(amplitude_v)
                        mira_phases_v.append(phase_v)
                    if len(mira_amplitudes_v) != len(mira_periods) or len(mira_phases_v) != len(mira_periods):
                        mira_amplitudes_v = []
                        mira_phases_v = []
                    else:
                        try:
                            mira_v_quality = int(star.mira_pulsation.get("qualityV", 0))
                        except (TypeError, ValueError):
                            mira_v_quality = 0
                        source_v_raw = star.mira_pulsation.get("sourceV")
                        mira_v_source = str(source_v_raw) if source_v_raw else None
        rows.append(
            [
                round_number(local[0]),
                round_number(local[1]),
                round_number(local[2]),
                round_number(math.log10(lum), 3),
                round_number(lum, 2),
                round_number(radius, 2),
                spectral_index(intrinsic_color_index),
                DATASET_INDEX[star.dataset],
                location_to_index(star.location),
                round_number(float(star.light_curve["period"]) if star.light_curve else star.period, 7),
                round_number(star.distance, 2),
                round_number(color_index, 3),
                round_number(star.v_mag, 3),
                round_number(star.i_mag, 3),
                round_number(star.age, 1) if star.age is not None else None,
                round_number(star.feh, 2) if star.feh is not None else None,
                star.mode,
                star.obj_id,
                round_number(float(star.light_curve["amplitude"]), 3) if star.light_curve else None,
                round_number(star.v_amplitude, 3) if star.v_amplitude is not None else None,
                round_number(float(star.light_curve["t0"]), 5) if star.light_curve else None,
                round_number(float(star.light_curve["r21"]), 3) if star.light_curve else None,
                round_number(float(star.light_curve["phi21"]), 3) if star.light_curve else None,
                round_number(float(star.light_curve["r31"]), 3) if star.light_curve else None,
                round_number(float(star.light_curve["phi31"]), 3) if star.light_curve else None,
                str(star.light_curve["subtype"]) if star.light_curve else None,
                star.color_curve,
                star.color_curve_quality,
                star.brightness_curve,
                star.brightness_curve_quality,
                round_number(star.ra, 5),
                round_number(star.dec, 5),
                round_number(gal_lon, 5),
                round_number(gal_lat, 5),
                round_number(star.reddening_evi, 3),
                round_number(star.reddening_evi_error, 3) if star.reddening_evi_error is not None else None,
                star.reddening_source,
                star.reddening_partition_id,
                round_number(intrinsic_color_index, 3),
                round_number(star.distance_error, 3) if star.distance_error is not None else None,
                star.distance_source,
                [round_number(value, 6) for value in mira_periods] if mira_periods else None,
                [round_number(value, 4) for value in mira_amplitudes] if mira_amplitudes else None,
                [round_number(value, 6) for value in mira_phases] if mira_phases else None,
                mira_quality,
                mira_source,
                [round_number(value, 4) for value in mira_amplitudes_v] if mira_amplitudes_v else None,
                [round_number(value, 6) for value in mira_phases_v] if mira_phases_v else None,
                mira_v_quality,
                mira_v_source,
                star.mira_teff,
                star.mira_teff_source_index,
            ]
        )
    return rows


def bounds_for(
    rows: list[list[float | int | str | None]],
    cells: list[list[float]],
    extra_rows: list[list[float | int]] | None = None,
) -> dict[str, list[float]]:
    coordinates = [(float(row[0]), float(row[1]), float(row[2])) for row in rows]
    coordinates.extend((cell[0], cell[1], cell[2]) for cell in cells)
    if extra_rows:
        coordinates.extend((float(row[0]), float(row[1]), float(row[2])) for row in extra_rows)
    return {
        "x": [round_number(min(point[0] for point in coordinates)), round_number(max(point[0] for point in coordinates))],
        "y": [round_number(min(point[1] for point in coordinates)), round_number(max(point[1] for point in coordinates))],
        "z": [round_number(min(point[2] for point in coordinates)), round_number(max(point[2] for point in coordinates))],
    }


def mean_vector(stars: list[CatalogStar]) -> tuple[float, float, float]:
    return tuple(sum(star.vector[i] for star in stars) / len(stars) for i in range(3))  # type: ignore[return-value]


def rounded_vector(vector: tuple[float, float, float], digits: int = 6) -> list[float]:
    return [round_number(component, digits) for component in vector]

def compress_brotli(data: bytes) -> bytes | None:
    for module_name in ("brotli", "brotlicffi"):
        try:
            brotli_module = __import__(module_name)
        except ImportError:
            continue
        return brotli_module.compress(data, quality=11)
    return None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    download_catalog_source_files()
    cepheids = parse_cepheids(RAW / "ogle_cepheids_table3.dat")
    rr_lyrae = parse_rr_lyrae(RAW / "ogle_rrlyrae_table2.dat")
    anomalous_cepheids = parse_anomalous_cepheids()
    miras = parse_miras()
    catalog = cepheids + rr_lyrae + anomalous_cepheids + miras
    light_curve_parameters = load_light_curve_parameters()
    for star in catalog:
        if star.obj_id in light_curve_parameters:
            star.light_curve = light_curve_parameters[star.obj_id]
    color_curve_summary = apply_color_curves(catalog)
    reddening_summary = assign_reddening(catalog)
    mira_distance_summary = apply_mira_distances(miras)
    mira_temperature_summary = apply_mira_literature_temperatures(miras)
    reddening_summary = assign_reddening(catalog)
    mira_pulsation_summary = apply_mira_pulsations(miras)

    vi_temperature_calibration = build_mist_v_minus_i_temperature_calibration()
    set_v_minus_i_temperature_anchors(v_minus_i_temperature_anchors_from_calibration(vi_temperature_calibration))
    vi_luminosity_temperature_calibration = build_mist_vi_luminosity_temperature_calibration(
        vi_temperature_calibration
    )

    origin = mean_vector(catalog)
    lmc_origin = mean_vector([star for star in catalog if star.location == "LMC"])
    smc_origin = mean_vector([star for star in catalog if star.location == "SMC"])
    basis = make_basis(origin)
    rows = serialize_catalog(catalog, origin, basis)
    red_clump = parse_fits_distance_map(RAW / "MC_RC_Distance_Map_Oden25_galactic.fits", origin, basis)
    red_clump_density_counts, red_clump_density_meta = load_red_clump_density_counts(XMC_DENSITY_COUNTS)
    red_clump_density_summary = attach_red_clump_density(red_clump, red_clump_density_counts)
    clusters = parse_perren_clusters(PERREN_CLUSTER_TABLE, PERREN_ASTECA_TABLE)
    cluster_rows, cluster_stars, cluster_glow_bins, cluster_hr_bins, cluster_summary = serialize_synthetic_clusters(clusters, origin, basis)

    payload = {
        "meta": {
            "title": "Magellanic Cloud 3-D Atlas",
            "generatedFrom": [
                "OGLE Magellanic Cepheid and RR Lyrae distance tables",
                "OGLE-IV OCVS light-curve catalogs",
                "OGLE-IV anomalous Cepheids OCVS",
                "OGLE-III Magellanic LPV Mira catalogs",
                "Iwanek et al. 2021 Mira mid-IR mean magnitudes and PLRs",
                "AllWISE Mira cross-match for mid-IR PLR distances",
                "Riebel et al. 2012 GRAMS LMC evolved-star SED temperatures",
                "SAGE-Spec LMC/SMC evolved-star model temperatures",
                "XMC Red Clump Distance Map FITS",
                "Skowron et al. 2021 OGLE-IV Red Clump E(V-I) map",
                "He & Huang 2026 3-D RR Lyrae E(V-I) map",
                "Perren et al. 2017 ASteCA Magellanic Cloud cluster catalog",
                "MIST non-rotating alpha=0 isochrones",
            ],
            "coordinateFrame": "OGLE-aligned observed-sky tangent frame centered on the OGLE Magellanic sample; x/y are RA/Dec tangent axes rotated 15 degrees so the default OGLE-facing view starts level, z=away from Sun, units=kpc.",
            "spectralNote": "Spectral class is inferred from dereddened V-I color because most source tables do not publish literal spectral types; rendered color subtracts E(V-I), maps intrinsic V-I plus I-band luminosity and [Fe/H] to an effective-temperature calibration derived from MIST UBVRIplus Bessell V/I photometry when available, interpolates the full Mitchell Charity 2-degree sRGB D58 blackbody table, and applies display-only temperature/chroma contrast around the D58 whitepoint. Miras with literature or SED-model Teff values use those values as mean temperature priors for display color.",
            "reddeningNote": "E(V-I) defaults to the Skowron et al. 2021 OGLE-IV red-clump map. Where a star falls inside the He & Huang 2026 3-D RR Lyrae GeoJSON partitions, the distance-dependent He & Huang E(V-I) value overrides the Skowron map. Stars outside both maps use same-cloud k=32 nearest-neighbor imputation from directly matched stars, with same-cloud median only as a sparse-neighborhood fallback. Pulsation color curves keep their OGLE V-I offsets, but the mean color is dereddened before temperature conversion.",
            "luminosityNote": "Luminosity is derived from I-band magnitude and line-of-sight distance using M_I(Sun)=4.10.",
            "anomalousCepheidDistanceNote": "Anomalous Cepheid distances use the LMC OGLE-IV Wesenheit period-luminosity relations from Jacyszyn-Dobrzeniecka et al. 2019, anchored to the Pietrzynski et al. 2019 LMC distance of 49.59 kpc. The published Bridge anomalous Cepheids are marked as Bridge; the Galactic foreground reclassification OGLE-GAL-ACEP-028 is included as Outer at its published 28.18 kpc distance.",
            "miraDistanceNote": "OGLE Magellanic Mira positions and I/V means come from the published OGLE-III LPV catalogs because OGLE does not publish LMC/SMC Miras in the OGLE-IV OCVS. LMC Mira distances prefer the published Iwanek et al. 2021 extinction-corrected WISE/Spitzer mean magnitudes and their mid-IR PLRs, calibrated to the 49.59 kpc Pietrzynski et al. 2019 LMC distance; LMC stars missing those published mid-IR means fall back to a 2 arcsec AllWISE cross-match on the same PLRs. SMC Mira distances use a 2 arcsec AllWISE cross-match with the same published PLRs and a conservative single-catalog magnitude-error floor, without a geometric zero-point renormalization. Stars without reliable mid-IR estimates use a same-cloud 32-neighbor distance estimate where the local Mira field is dense enough, and only retain the published geometric cloud mean if that local estimate is unavailable.",
            "miraTemperatureNote": "Mira mean Teff priors prefer SAGE-Spec model temperatures where directly linked to OGLE IDs, then 2 arcsec Riebel et al. 2012 GRAMS LMC SED fits, then Iwanek et al. 2021 Tstar values for remaining golden-sample LMC Miras. These values are single-epoch or SED-model priors, not phase-resolved Rosseland temperatures; browser rendering constrains phase excursions around the prior so Miras remain cool late-type stars.",
            "radiusNote": "Radius is estimated from I-band luminosity and dereddened V-I color using the generated V-I effective-temperature calibration; it is intended for display scaling.",
            "colorCurveNote": "Pulsation color is driven by validated OGLE V- and I-band template fits; compact phase templates store V-I offsets around the catalog mean observed color before subtracting E(V-I). Rendering evaluates the temperature calibration at each phase using instantaneous intrinsic V-I and I-band luminosity.",
            "brightnessCurveNote": "Cepheid, anomalous Cepheid, and RR Lyrae brightness uses compact I-band templates fitted from OGLE epoch photometry, with validated convex dictionary templates promoted where they improve the unmodulated lightcurve. Miras use OGLE LPV primary, secondary, and tertiary periods and I-band amplitudes as a time-domain multi-sine model with phases fitted to OGLE I-band epoch photometry; V-band Mira components are fitted where possible, and sparse or missing V curves are regularized or filled from empirical V/I amplitude-ratio and phase-lag priors learned from the highest-quality Mira V/I fits.",
            "redClumpDensityNote": "Optional XMC surface opacity uses a smoothed Gaia DR3 broad red-clump count proxy binned on the same 0.25 degree galactic grid; it is for visual density only, not a reproduced Oden et al. RC catalog.",
            "clusterSynthesisNote": "Perren et al. cluster masses seed single-star samples from a Chabrier-style IMF above 0.5 solar masses. Each synthetic star samples [Fe/H] and log(age) from the cluster uncertainty distribution truncated to the reported one-sigma support, then bilinearly interpolates between neighboring MIST alpha=0, non-rotating isochrone blocks before mass interpolation. When UBVRIplus MIST CMD files are available, Bessell V and I magnitudes provide synthetic V-I colors and I-band luminosities; otherwise the build falls back to full MIST tracks with blackbody-derived display colors. Stars with I-band luminosity below 1 solar luminosity are aggregated into per-cluster radial glow bins and compact HR bins; brighter stars are rendered as points. Point radii come from MIST radii or from MIST luminosity plus Teff. Positions use the ASteCA structural fit where reliable: older clusters draw from a truncated King-like profile using the fitted core and tidal radii, young clusters draw from an EFF-like extended-halo profile, and sparse or unreliable fits fall back to a Plummer model. The reported cluster radius is treated as the main measured aperture rather than a hard edge, with an age-dependent mass-segregation bias.",
            "redClumpDensitySource": red_clump_density_meta,
            "viTemperatureCalibration": vi_temperature_calibration,
            "viLuminosityTemperatureCalibration": vi_luminosity_temperature_calibration,
            "meanMetallicityFeHByLocation": MEAN_METALLICITY_FEH_BY_LOCATION,
            "miraTemperatureSources": [dict(source) for source in MIRA_TEMPERATURE_SOURCES],
            "originDistanceKpc": round_number(vector_length(origin), 3),
            "coordinateCenters": {
                "sampleGalacticVectorKpc": rounded_vector(origin),
                "sampleEquatorialVectorKpc": rounded_vector(galactic_to_equatorial_vector(origin)),
                "lmcGalacticVectorKpc": rounded_vector(lmc_origin),
                "smcGalacticVectorKpc": rounded_vector(smc_origin),
            },
        },
        "fields": {
            "catalog": [
                "x",
                "y",
                "z",
                "logLuminosity",
                "luminositySolar",
                "radiusSolar",
                "spectralIndex",
                "datasetIndex",
                "locationIndex",
                "periodDays",
                "distanceKpc",
                "vMinusI",
                "vMag",
                "iMag",
                "ageMyr",
                "metallicityFeH",
                "mode",
                "id",
                "amplitudeI",
                "amplitudeV",
                "t0HjdMinus2450000",
                "r21",
                "phi21",
                "r31",
                "phi31",
                "lightCurveSubtype",
                "colorCurveVI",
                "colorCurveQuality",
                "brightnessCurveI",
                "brightnessCurveQuality",
                "raDeg",
                "decDeg",
                "galLonDeg",
                "galLatDeg",
                "reddeningEVI",
                "reddeningEVIError",
                "reddeningSource",
                "reddeningPartitionId",
                "vMinusI0",
                "distanceErrorKpc",
                "distanceSource",
                "miraPeriodsDays",
                "miraAmplitudesI",
                "miraPhasesI",
                "miraPulsationQuality",
                "miraPulsationSource",
                "miraAmplitudesV",
                "miraPhasesV",
                "miraVPulsationQuality",
                "miraVPulsationSource",
                "miraTeffK",
                "miraTeffSourceIndex",
            ],
            "redClump": ["x", "y", "z", "distanceKpc", "galLonDeg", "galLatDeg", "densityCount", "densityUnit"],
            "clusters": [
                "x",
                "y",
                "z",
                "name",
                "galaxy",
                "raDeg",
                "decDeg",
                "galLonDeg",
                "galLatDeg",
                "distanceKpc",
                "radiusPc",
                "metallicityFeH",
                "metallicityFeHError",
                "logAge",
                "logAgeError",
                "ebv",
                "ebvError",
                "distanceModulus",
                "distanceModulusError",
                "massSolar",
                "massSolarError",
                "syntheticStarCount",
                "renderedStarCount",
                "unresolvedStarCount",
                "unresolvedLuminositySolar",
                "unresolvedVMinusI0",
                "isochroneSummary",
                "qualityFlags",
                "contaminationIndex",
                "clusterProbability",
                "flagsCount",
                "massSegregationStrength",
                "ageOutlier",
            ],
            "clusterStars": [
                "x",
                "y",
                "z",
                "logLuminosity",
                "luminositySolar",
                "radiusSolar",
                "spectralIndex",
                "clusterIndex",
                "initialMassSolar",
                "currentMassSolar",
                "vMinusI0",
                "temperatureK",
                "raDeg",
                "decDeg",
                "galLonDeg",
                "galLatDeg",
                "distanceKpc",
            ],
            "clusterGlowBins": [
                "clusterIndex",
                "outerRadiusFraction",
                "luminositySolar",
                "vMinusI0",
            ],
            "clusterHrBins": [
                "clusterIndex",
                "vMinusI0",
                "logLuminosity",
                "starCount",
                "luminositySolar",
                "temperatureK",
                "radiusSolar",
            ],
        },
        "locations": ["LMC", "SMC", "Bridge", "Outer"],
        "spectralClasses": SPECTRAL_CLASSES,
        "datasets": {
            "catalog": rows,
            "redClump": red_clump,
            "clusters": cluster_rows,
            "clusterStars": cluster_stars,
            "clusterGlowBins": cluster_glow_bins,
            "clusterHrBins": cluster_hr_bins,
        },
        "counts": {
            "cepheids": len(cepheids),
            "rrLyrae": len(rr_lyrae),
            "anomalousCepheids": len(anomalous_cepheids),
            "miras": len(miras),
            "bridgeAnomalousCepheids": sum(1 for star in anomalous_cepheids if star.location == "BRIDGE"),
            "reclassifiedClassicalCepheidsRemoved": len(RECLASSIFIED_CLASSICAL_CEPHEIDS),
            "redClumpCells": len(red_clump),
            "lightCurveParameters": sum(1 for star in catalog if star.light_curve),
            **color_curve_summary,
            **reddening_summary,
            **mira_distance_summary,
            **mira_temperature_summary,
            **mira_pulsation_summary,
            **red_clump_density_summary,
            **cluster_summary,
        },
        "bounds": bounds_for(rows, red_clump, cluster_stars),
        "sources": [
            {
                "name": "XMC Red Clump Distance Map of the Magellanic Clouds",
                "url": "https://github.com/slateroden/XMC_DistanceMap",
            },
            {
                "name": "OGLE Classical Cepheid 3-D structure",
                "url": "https://ogle.astrouw.edu.pl/cont/4_main/str/3_dim_str/",
            },
            {
                "name": "OGLE RR Lyrae 3-D structure",
                "url": "https://ogle.astrouw.edu.pl/cont/4_main/str/3_dim_rrl/",
            },
            {
                "name": "OGLE-IV OCVS variable-star catalogs",
                "url": "https://www.astrouw.edu.pl/ogle/ogle4/OCVS/",
            },
            {
                "name": "Jacyszyn-Dobrzeniecka et al. 2019 Magellanic Bridge Cepheid distances",
                "url": "https://arxiv.org/abs/1904.08220",
            },
            {
                "name": "OGLE-III LPV and Mira catalogs",
                "url": "https://ftp.astrouw.edu.pl/ogle/ogle3/OIII-CVS/",
            },
            {
                "name": "Iwanek et al. 2021 Mira mid-IR photometry and PLRs",
                "url": "https://doi.org/10.3847/1538-4357/ac10c5",
            },
            {
                "name": "AllWISE Source Catalog",
                "url": "https://wise2.ipac.caltech.edu/docs/release/allwise/",
            },
            {
                "name": "Riebel et al. 2012 GRAMS LMC evolved-star SED fits",
                "url": "https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/ApJ/753/71?format=html&tex=true",
            },
            {
                "name": "Jones et al. 2017 SAGE-Spec LMC point-source classifications",
                "url": "https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J%2FMNRAS%2F470%2F3250",
            },
            {
                "name": "Ruffle et al. 2015 SAGE-Spec SMC point-source classifications",
                "url": "https://vizier.unistra.fr/cgi-bin/VizieR-3?-source=J%2FMNRAS%2F451%2F3504",
            },
            {
                "name": "Pietrzynski et al. 2019 LMC geometric distance",
                "url": "https://www.nature.com/articles/s41586-019-0999-4",
            },
            {
                "name": "Graczyk et al. 2020 SMC geometric distance",
                "url": "https://arxiv.org/abs/2010.08754",
            },
            {
                "name": "Perren et al. 2017 ASteCA Magellanic Cloud star-cluster catalog",
                "url": "https://ui.adsabs.harvard.edu/abs/2017A%26A...602A..89P/abstract",
            },
            {
                "name": "MIST stellar evolution isochrones",
                "url": "https://waps.cfa.harvard.edu/MIST/",
            },
            {
                "name": "Mitchell Charity blackbody sRGB D58 color table",
                "url": "http://www.vendian.org/mncharity/dir3/blackbody/UnstableURLs/bbr_color_D58.html",
            },
            {
                "name": "Skowron et al. 2021 OGLE-IV Red Clump E(V-I) reddening map",
                "url": "https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/252/23",
            },
            {
                "name": "He & Huang 2026 3-D RR Lyrae E(V-I) reddening map",
                "url": "https://doi.org/10.5281/zenodo.17717895",
            },
        ],
    }

    atlas_json = OUT / "magellanic-clouds.json"
    atlas_brotli = OUT / "magellanic-clouds.json.br"
    atlas_gzip = OUT / "magellanic-clouds.json.gz"
    atlas_json_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    atlas_json.write_bytes(atlas_json_bytes)
    brotli_bytes = compress_brotli(atlas_json_bytes)
    if brotli_bytes is not None:
        atlas_brotli.write_bytes(brotli_bytes)
    elif atlas_brotli.exists():
        atlas_brotli.unlink()
    atlas_gzip.write_bytes(gzip.compress(atlas_json_bytes, compresslevel=9, mtime=0))
    print(json.dumps(payload["counts"], indent=2))
    print(f"Wrote {atlas_json}")
    if brotli_bytes is not None:
        print(f"Wrote {atlas_brotli}")
    else:
        print("Skipped Brotli output; install brotli or brotlicffi to generate it.")
    print(f"Wrote {atlas_gzip}")


if __name__ == "__main__":
    main()
