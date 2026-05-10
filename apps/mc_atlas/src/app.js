const DATA_VERSION = "20260510-mira-literature-teff";
const DATA_URL = `./public/data/magellanic-clouds.json?v=${DATA_VERSION}`;
const DATA_DOWNLOAD_PROGRESS_MAX = 0.88;
const ZOOM_BASE_SCALE = 1.62;
const DEFAULT_ZOOM_SCALE = 1;
const ZOOM_SCALE_MIN = 0.5;
const ZOOM_SCALE_MAX = 1000;
const TARGET_ZOOM_SCALE_MAX = 100_000;
const TARGET_ZOOM_SCREEN_DIAMETER_FRACTION = 0.8;
const TARGET_SELECTION_RING_PADDING_PX = 7;
const TARGET_SELECTION_RING_MIN_RADIUS = 8;
const CLUSTER_TARGET_SELECTION_RADIUS_SCALE = 0.58;
const CLUSTER_TARGET_SELECTION_MIN_RADIUS = 10;
const CLUSTER_TARGET_PICK_MIN_RADIUS = 20;
const CLUSTER_TARGET_PICK_RADIUS_SCALE = 1.25;
const CATALOG_DIRECT_PICK_PADDING_PX = 2;
const CATALOG_DIRECT_PICK_MIN_RADIUS = 5;
const DEFAULT_UNCERTAINTY_SEED = 0;
const UNCERTAINTY_SEED_MAX = 100;
const UNCERTAINTY_TRUNCATION_SIGMA = 3;
const DESKTOP_SCENE_CENTER_OFFSET_X = -30;
const DATASET_EXPOSURE_MIN = 0.01;
const DATASET_EXPOSURE_MAX = 100;
const DATASET_EXPOSURE_DEFAULT = 1;
const PULSATOR_PRESET_CONTEXT_EXPOSURE = 0.1;
const RR_LYRAE_PRESET_CONTEXT_EXPOSURE = 0.02;
const CLUSTER_PRESET_CONTEXT_EXPOSURE = 0.12;
const CLUSTERS_PRESET_PULSATOR_CONTEXT_EXPOSURE = DATASET_EXPOSURE_MIN;
const CLUSTERS_PRESET_RED_CLUMP_CONTEXT_EXPOSURE = 0.5;
const RED_CLUMP_PRESET_HIGHLIGHT_EXPOSURE = 2;
const PULSATOR_PRESET_HIGHLIGHT_EXPOSURE = 1;
const PULSATOR_PRESET_HIGHLIGHT_EXPOSURES = {
  rrlyrae: 2,
};
const RADIUS_SCALE_MIN = 0.1;
const RADIUS_SCALE_MAX = 3;
const ORIGIN_PAN_DAMPING = 0.35;
const ORIGIN_PAN_MAX_GAIN = 1.6;
const PAN_DRAG_ZOOM_DAMPING = 0.24;
const PAN_DRAG_MIN_SENSITIVITY = 0.32;
const VIEWPORT_PAN_STEP_PX = 68;
const VIEWPORT_PAGE_STEP_PX = 220;
const VIEWPORT_ZOOM_STEP_GAIN = 1.16;
const VIEWPORT_YAW_STEP_DEGREES = 5;
const VIEWPORT_KEY_FAST_MULTIPLIER = 2.5;
const TARGET_NAVIGATION_HILBERT_BITS = 10;
const TARGET_NAVIGATION_VIEWPORT_MARGIN = 24;
const ORBIT_DRAG_ZOOM_DAMPING = 0.5;
const ORBIT_DRAG_MIN_SENSITIVITY = 0.18;
const PULSATOR_RADIUS_BASE_SCALE = 0.254016;
const INITIAL_PULSATION_SPEED = 18_000;
const PULSATION_SPEED_MIN = 1;
const PULSATION_SPEED_MAX = 25_000_000;
const PULSATION_FLICKER_FREQUENCY_HZ = 2;
const PULSATION_AMPLITUDE_MIN = 1;
const PULSATION_AMPLITUDE_MAX = 20;
const PULSATION_AMPLITUDE_DEFAULT = 7;
const PULSATION_SPEED_KEY_GAIN = 10 ** 0.125;
const PULSATION_SPEED_KEY_FAST_GAIN = 10;
const SECONDS_PER_DAY = 86400;
const INTRO_ROTATION_DURATION_MS = 3000;
const INTRO_CLOUD_LABEL_TRIGGER_YAW_DEGREES = -10;
const INTRO_CLOUD_LABEL_FADE_IN_MS = 360;
const INTRO_CLOUD_LABEL_HOLD_MS = 2000;
const INTRO_CLOUD_LABEL_FADE_OUT_MS = 1000;
const INTRO_CLOUD_LABEL_TOTAL_MS =
  INTRO_CLOUD_LABEL_FADE_IN_MS +
  INTRO_CLOUD_LABEL_HOLD_MS +
  INTRO_CLOUD_LABEL_FADE_OUT_MS;
const FACE_VIEW_ANGLES_DEGREES = { yaw: 0, pitch: 0, roll: 0 };
const EDGE_VIEW_ANGLES_DEGREES = { yaw: 88, pitch: 8, roll: 0 };
const AXIS_SPIN_DURATION_MS = 1800;
const PULSE_LOD_RADIUS_ON = 1.2;
const PULSE_LOD_RADIUS_OFF = 0.95;
const PULSE_LOD_ALPHA_ON = 1.01;
const PULSE_LOD_ALPHA_OFF = 0.98;
const PULSE_LOD_VISUAL_WEIGHT_ON = 0.9;
const PULSE_LOD_VISUAL_WEIGHT_OFF = 0.55;
const CATALOG_PULSE_ALL_STARS = true;
const NAVIGATION_ACTIVITY_SETTLE_MS = 400;
const NAVIGATION_SLOW_PULSE_REFRESH_FLOOR_DEFAULT_MS = 220;
const ADAPTIVE_PULSE_REFRESH_PERIOD_SECONDS = 2;
const SLOW_PULSE_REFRESH_FRAME_INTERVAL_MS = 1000 / 60;
const SLOW_PULSE_REFRESH_EASE_END_SECONDS = 8;
const SLOW_PULSE_REFRESH_SAMPLES_PER_CYCLE = 96;
const SLOW_PULSE_REFRESH_MAX_INTERVAL_MS = 1000;
const STAR_RADIUS_ZOOM_GAIN = 0.18;
const STAR_RADIUS_ZOOM_MAX_BOOST = 1.2;
const STAR_RADIUS_ZOOM_BASE_GAIN = 0.75;
const STAR_RADIUS_ZOOM_SIZE_MAX = 20;
const STAR_RADIUS_DEEP_ZOOM_FADE_START = 250;
const STAR_RADIUS_DEEP_ZOOM_FADE_END = 8000;
const STAR_RADIUS_DEEP_ZOOM_MIN_SCALE = 0.45;
const STAR_RADIUS_DEEP_ZOOM_TARGET_GROWTH_POWER = 0.72;
const STAR_RADIUS_BASE_MAX = 56;
const CATALOG_LIMB_DARKEN_ALL_STARS = true;
const LIMB_DARKENING_RADIUS_MIN = 1.35;
const LIMB_DARKENING_RADIUS_STEP = 0.25;
const LIMB_DARKENING_CACHE_MAX = 420;
const LIMB_DARKENING_COLOR_STEP = 8;
const LIMB_DARKENING_LINEAR_COEFFICIENT = 0.78;
const LIMB_DARKENING_FLUX_NORMALIZATION = 1 / (1 - LIMB_DARKENING_LINEAR_COEFFICIENT / 3);
const LIMB_DARKENING_ALPHA_MIN = 0.05;
const LIMB_DARKENING_VISUAL_WEIGHT_MIN = 0.12;
const LIMB_DARKENING_HIGH_RADIUS_SCALE = 2.1;
const LIMB_DARKENING_HIGH_RADIUS_VISUAL_WEIGHT_MIN = 0.55;
const CATALOG_GPU_VERTEX_FLOATS = 8;
const CATALOG_DYNAMIC_GPU_STATIC_VERTEX_FLOATS = 8;
const CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS = 5;
const CATALOG_WORLD_PULSE_DIRTY_RANGE_MERGE_GAP = 8;
const CATALOG_WORLD_PULSE_FULL_UPLOAD_DIRTY_FRACTION = 0.55;
const CATALOG_WORLD_PULSE_FULL_UPLOAD_RANGE_LIMIT = 160;
const CLUSTER_STAR_GPU_VERTEX_FLOATS = 9;
const RED_CLUMP_GPU_VERTEX_FLOATS = 6;
const RED_CLUMP_ZOOM_FADE_START = 75;
const RED_CLUMP_ZOOM_FADE_END = 350;
// User-facing yaw zero is the observer-side OGLE view.
const OBSERVED_VIEW_YAW_DEGREES = -180;
const OBSERVED_VIEW_ROLL_DEGREES = 0;
const DEFAULT_VIEW_AXIS_ROTATION_DEGREES = 15;
const INTRO_ROTATION_START_YAW_DEGREES = -143;
const INTRO_ROTATION_START_PITCH_DEGREES = 0;
const INTRO_ROTATION_START_ROLL_DEGREES = 0;
const AXIS_SPIN_AXES = new Set(["yaw", "pitch", "roll"]);
const GRID_SHORTCUT_SEQUENCE = ["none", "equatorial", "galactic", "both"];
const KEYBOARD_DATASET_PRESETS = {
  1: "cepheids",
  2: "rrlyrae",
  3: "miras",
  4: "clusters",
  5: "redclump",
};
const SHORTCUT_HELP_ITEMS = [
  { keys: ["/"], label: "Search targets" },
  { keys: ["Esc"], label: "Unlock or clear target" },
  { keys: ["Space"], label: "Pause or resume pulsation" },
  { keys: ["1", "2", "3", "4", "5"], label: "Activate dataset presets" },
  { keys: ["["], label: "Previous target" },
  { keys: ["]"], label: "Next target" },
  { keys: ["L"], label: "Lock camera to target" },
  { keys: ["H"], label: "Hide or show overlays" },
  { keys: ["V"], label: "Cycle face, edge, and custom view" },
  { keys: ["G"], label: "Cycle coordinate grids" },
  { keys: [","], label: "Slow pulsation" },
  { keys: ["."], label: "Speed pulsation" },
  { keys: ["?"], label: "Show this panel" },
];
const ORIENTATION_GRID_VISIBLE_MS = 1200;
const ORIENTATION_GRID_FADE_MS = 450;
const EQUATORIAL_GRID_RA_STEP_DEGREES = 30;
const EQUATORIAL_GRID_DEC_STEP_DEGREES = 5;
const GALACTIC_GRID_LON_STEP_DEGREES = 30;
const GALACTIC_GRID_LAT_STEP_DEGREES = 5;
const SKY_GRID_SAMPLE_STEP_DEGREES = 1;
const SKY_GRID_FRONT_HEMISPHERE_DOT_MIN = 0.02;
const SKY_GRID_LABEL_MARGIN = 18;
const SKY_GRID_BOUNDS_PADDING_DEGREES = 5;
const TARGET_SEARCH_RESULT_LIMIT = 80;
const SCALE_BAR_TARGET_WIDTH_PX = 128;
const SCALE_BAR_MIN_WIDTH_PX = 72;
const SCALE_BAR_MAX_WIDTH_PX = 168;
const SCALE_BAR_MAX_VIEWPORT_FRACTION = 0.22;
const SCALE_BAR_NICE_MULTIPLIERS = [1, 2, 5];

const IDX = {
  x: 0,
  y: 1,
  z: 2,
  logLum: 3,
  lum: 4,
  radius: 5,
  spectral: 6,
  dataset: 7,
  location: 8,
  period: 9,
  distance: 10,
  vMinusI: 11,
  vMag: 12,
  iMag: 13,
  age: 14,
  feh: 15,
  mode: 16,
  id: 17,
  amplitudeI: 18,
  amplitudeV: 19,
  t0: 20,
  r21: 21,
  phi21: 22,
  r31: 23,
  phi31: 24,
  lightCurveSubtype: 25,
  colorCurve: 26,
  colorCurveQuality: 27,
  brightnessCurve: 28,
  brightnessCurveQuality: 29,
  raDeg: 30,
  decDeg: 31,
  galLonDeg: 32,
  galLatDeg: 33,
  reddeningEVI: 34,
  reddeningEVIError: 35,
  reddeningSource: 36,
  reddeningPartitionId: 37,
  vMinusI0: 38,
  distanceError: 39,
  distanceSource: 40,
  miraPeriods: 41,
  miraAmplitudesI: 42,
  miraPhasesI: 43,
  miraPulsationQuality: 44,
  miraPulsationSource: 45,
  miraAmplitudesV: 46,
  miraPhasesV: 47,
  miraVPulsationQuality: 48,
  miraVPulsationSource: 49,
  miraTeff: 50,
  miraTeffSourceIndex: 51,
};

const RC = {
  x: 0,
  y: 1,
  z: 2,
  distance: 3,
  lon: 4,
  lat: 5,
  densityCount: 6,
  densityUnit: 7,
};

const CL = {
  x: 0,
  y: 1,
  z: 2,
  name: 3,
  galaxy: 4,
  raDeg: 5,
  decDeg: 6,
  galLonDeg: 7,
  galLatDeg: 8,
  distance: 9,
  radiusPc: 10,
  feh: 11,
  eFeh: 12,
  logAge: 13,
  eLogAge: 14,
  ebv: 15,
  eEbv: 16,
  mu0: 17,
  eMu0: 18,
  mass: 19,
  eMass: 20,
  syntheticStars: 21,
  renderedStars: 22,
  unresolvedStars: 23,
  unresolvedLum: 24,
  unresolvedVMinusI0: 25,
  isochroneSummary: 26,
  qualityFlags: 27,
  contaminationIndex: 28,
  clusterProbability: 29,
  flagsCount: 30,
  segregation: 31,
  ageOutlier: 32,
  source: 33,
};

const CS = {
  x: 0,
  y: 1,
  z: 2,
  logLum: 3,
  lum: 4,
  radius: 5,
  spectral: 6,
  cluster: 7,
  initialMass: 8,
  currentMass: 9,
  vMinusI0: 10,
  temperature: 11,
  raDeg: 12,
  decDeg: 13,
  galLonDeg: 14,
  galLatDeg: 15,
  distance: 16,
};

const CG = {
  cluster: 0,
  outerRadius: 1,
  lum: 2,
  vMinusI0: 3,
};

const CHR = {
  cluster: 0,
  vMinusI0: 1,
  logLum: 2,
  count: 3,
  lum: 4,
  temperature: 5,
  radius: 6,
};

const COORDINATE_FRAMES = [
  {
    id: "atlas",
    label: "3-D Space",
    detail: "OGLE view/depth",
    axes: [
      ["x", "east"],
      ["y", "north"],
      ["d", "distance from Sun"],
    ],
  },
  {
    id: "galactic",
    label: "Galactic",
    detail: "l,b sky map",
    axes: [
      ["x", "east"],
      ["y", "north"],
      ["d", "distance"],
    ],
  },
];

const COORDINATE_FRAME_BY_ID = new Map(COORDINATE_FRAMES.map((frame) => [frame.id, frame]));
const COORDINATE_CENTERS = [
  { id: "lmc", label: "LMC", locationIndex: 0 },
  { id: "bridge", label: "Bridge", locationIndex: 2 },
  { id: "smc", label: "SMC", locationIndex: 1 },
];
const COORDINATE_CENTER_BY_ID = new Map(COORDINATE_CENTERS.map((center) => [center.id, center]));
const INTRO_CLOUD_LABELS = [
  { id: "lmc", text: "LMC", textAlign: "right", offsetX: -160, offsetY: -48 },
  { id: "smc", text: "SMC", textAlign: "left", offsetX: 56, offsetY: -48 },
];
const DATASET_LABELS = ["Classical Cepheid", "RR Lyrae", "Anomalous Cepheid", "Mira"];
const DATASET_KEYS = ["cepheids", "rrlyrae", "anomalousCepheids", "miras"];
const CEPHEID_DATASET_KEYS = ["cepheids", "anomalousCepheids"];
const CLUSTER_PULSATOR_STRIP_DATASET_KEYS = ["cepheids", "rrlyrae", "anomalousCepheids"];
const CLUSTER_PULSATOR_STRIP_BIN_COUNT = 14;
const CLUSTER_PULSATOR_STRIP_MIN_BIN_STARS = 12;
const CLUSTER_PULSATOR_STRIP_COLOR_LOW_QUANTILE = 0.08;
const CLUSTER_PULSATOR_STRIP_COLOR_HIGH_QUANTILE = 0.92;
const CLUSTER_PULSATOR_STRIP_COLOR_MARGIN = 0.045;
const CLUSTER_PULSATOR_STRIP_LOG_LUM_MARGIN = 0.08;
const CLUSTER_PULSATOR_NEAREST_REFERENCE_COUNT = 160;
const PULSATOR_DEFAULT_PRESET = "default";
const PULSATOR_PRESETS = ["cepheids", "rrlyrae", "miras"];
const PULSATOR_PRESET_SEQUENCE = [...PULSATOR_PRESETS, PULSATOR_DEFAULT_PRESET];
const AUXILIARY_DATASET_PRESETS = ["clusters", "redclump"];
const DATASET_PRESETS = [...PULSATOR_PRESETS, ...AUXILIARY_DATASET_PRESETS];
const DATASET_PRESET_EXPOSURE_KEYS = [...DATASET_KEYS, "clusters", "redclump"];
const PULSATOR_PRESET_LABELS = {
  cepheids: "Cepheids",
  rrlyrae: "RR Lyrae",
  miras: "Miras",
};
const DATASET_PRESET_LABELS = {
  ...PULSATOR_PRESET_LABELS,
  clusters: "Clusters",
  redclump: "Red clump",
};
const PULSATOR_PRESET_DATASET_KEYS = {
  cepheids: CEPHEID_DATASET_KEYS,
  rrlyrae: ["rrlyrae"],
  miras: ["miras"],
};
const AUXILIARY_DATASET_PRESET_KEYS = {
  clusters: ["clusters", "redclump"],
  redclump: ["redclump"],
};
// Current catalog medians; matching speed values make each median period last 3 real seconds.
const PULSATOR_PRESET_MEDIAN_PERIOD_DAYS = {
  cepheids: 2.0506071,
  rrlyrae: 0.5907994,
  miras: 359.8,
};
const PULSATOR_PRESET_SPEEDS = {
  cepheids: 59_000,
  rrlyrae: 17_000,
  miras: 7_000_000,
};
// Baseline radii are calibrated so 1x matches the former 0.8x visual scale.
const PULSATOR_PRESET_RADIUS_SCALES = {
  default: 1,
  cepheids: 0.7,
  rrlyrae: 1.3333333333333333,
  miras: 1,
};
const PULSATOR_PRESET_AMPLITUDE_SCALES = {
  default: PULSATION_AMPLITUDE_DEFAULT,
  cepheids: 5,
  rrlyrae: 5,
  miras: 2,
};
const LOCATION_LABELS = ["LMC", "SMC", "Bridge", "Outer"];
const DEFAULT_MEAN_METALLICITY_FEH_BY_LOCATION = [-0.4, -0.7, -0.55, -0.8];
const OGLE_OCVS_OBJECT_URL = "https://ogledb.astrouw.edu.pl/~ogle/OCVS/getobj.php?s=";
const OGLE_III_CVS_OBJECT_URL = "https://ogledb.astrouw.edu.pl/~ogle/CVS/o.php?";
const SUN_ABSOLUTE_I_MAG = 4.1;
const SUN_EFFECTIVE_TEMPERATURE = 5772;
const RED_CLUMP_MI = -0.25;
const RED_CLUMP_LUMINOSITY = 10 ** (-0.4 * (RED_CLUMP_MI - SUN_ABSOLUTE_I_MAG));
const RED_CLUMP_TEMPERATURE = 4800;
const RED_CLUMP_RADIUS = Math.sqrt(RED_CLUMP_LUMINOSITY) * (5772 / RED_CLUMP_TEMPERATURE) ** 2;
const RED_CLUMP_GRID_QUANTIZATION = 4;
const RED_CLUMP_EDGE_FEATHER_CELLS = 10;
const RED_CLUMP_EDGE_ALPHA_FLOOR = 0.08;
// Keep the red clump map-like, but let the Gaia RC-like count proxy gently nudge brightness.
const RED_CLUMP_EXPOSURE_DEFAULT = 1;
const RED_CLUMP_EXPOSURE_RENDER_SCALE = 0.256;
const RED_CLUMP_SURFACE_ALPHA_SCALE = 0.46;
const RED_CLUMP_COUNT_TO_STAR_EQUIVALENT = 0.01;
const RED_CLUMP_DENSITY_SMOOTHING_BLEND = 0.45;
const RED_CLUMP_SURFACE_PHYSICAL_BLEND = 0.25;
const RED_CLUMP_SURFACE_PHYSICAL_MIN_RATIO = 0.55;
const RED_CLUMP_SURFACE_PHYSICAL_MAX_RATIO = 1.8;
const RED_CLUMP_SURFACE_ALPHA_MAX = 0.62;
const RED_CLUMP_SURFACE_POINT_FILL = 1;
const RED_CLUMP_SURFACE_VIEWPORT_MARGIN = 36;
const RED_CLUMP_DENSITY_ALPHA_FLOOR = 0.075;
const RED_CLUMP_DENSITY_ALPHA_POWER = 1.65;
const CLUSTER_GLOW_ALPHA_SCALE = 0.22;
const CLUSTER_GLOW_ALPHA_MAX = 0.16;
const CLUSTER_GLOW_RADIUS_SCALE = 1.15;
const CLUSTER_GLOW_EDGE_FEATHER = 0.7;
const CLUSTER_GLOW_PROFILE_STOPS = 14;
const CLUSTER_STAR_LOD_CORE_RADIUS_START = 6;
const CLUSTER_STAR_LOD_CORE_RADIUS_END = 13;
const CLUSTER_STAR_COLLAPSED_GLOW_ALPHA_SCALE = 0.16;
const CLUSTER_STAR_COLLAPSED_GLOW_ALPHA_MAX = 0.18;
const CLUSTER_STAR_RESOLVED_GLOW_FLOOR = 0.18;
const MAX_DISPLAY_LUMINOSITY_RATIO = 500;
const DISPLAY_LUMINOSITY_BASE_BOOST = 112;
const DISPLAY_ALPHA_MAX = 0.78;
const STAR_PULSE_ALPHA_MAX = 0.95;
const STAR_ALPHA_HEADROOM_EXPOSURE = 2.2;
const RAW_PULSE_FLUX_MIN = 1e-12;
const RAW_PULSE_FLUX_MAX = 1e12;
const PULSE_FLUX_RATIO_MIN = 1e-300;
const VISUAL_PULSE_LOG_FLOOR = PULSE_FLUX_RATIO_MIN;
const BASE_LUMINOSITY_FACTOR = 3.25;
const PULSATOR_BASE_RADIUS_FACTOR = 1.5;
const COLOR_CACHE_PRECISION = 200;
const MAX_COLOR_PULSE_OFFSET = 0.42;
const MAX_MIRA_COLOR_PULSE_OFFSET = 1.25;
const MAX_MIRA_PRIOR_ASSISTED_COLOR_PULSE_OFFSET = 1.0;
const MAX_MIRA_PRIOR_ONLY_COLOR_PULSE_OFFSET = 0.75;
const MIRA_MIN_INTRINSIC_V_MINUS_I = 1.15;
const MIRA_MAX_INTRINSIC_V_MINUS_I = 5.5;
const MIRA_TEMPERATURE_HALF_SPAN_K = 500;
const MIRA_TEMPERATURE_BOUNDS = {
  carbon: { min: 1400, max: 3600 },
  oxygen: { min: 2000, max: 4080 },
  fallback: { min: 1700, max: 4080 },
};
const LIGHT_CURVE_AREA_PULSE_SHARE = 0.78;
const CEPHEID_PRESET_AREA_PULSE_SHARE = 0.72;
const RR_LYRAE_AREA_PULSE_SHARE = 0.74;
const RR_LYRAE_PRESET_AREA_PULSE_SHARE = 0.68;
const MIRA_PRESET_AREA_PULSE_SHARE = 0.84;
const FITTED_COLOR_CURVE_SAMPLES = 96;
const FITTED_COLOR_CURVE_SCALE = 100;
const FITTED_COLOR_CURVE_ZERO = 64;
const FITTED_LIGHT_CURVE_SCALE = 200;
const FITTED_LIGHT_CURVE_ZERO = 128;
const FITTED_LIGHT_CURVE_INT16_SCALE = 1000;
const GALACTIC_TO_EQUATORIAL_J2000 = [
  [-0.0548755604, 0.4941094279, -0.867666149],
  [-0.8734370902, -0.44482963, -0.1980763734],
  [-0.4838350155, 0.7469822445, 0.4559837762],
];
const V_MINUS_I_TEMPERATURE_ANCHORS = [
  { vMinusI: -0.15, temperature: 12000 },
  { vMinusI: 0.05, temperature: 9500 },
  { vMinusI: 0.25, temperature: 7600 },
  { vMinusI: 0.45, temperature: 6500 },
  { vMinusI: 0.75, temperature: 5600 },
  { vMinusI: 1.15, temperature: 4500 },
  { vMinusI: 1.8, temperature: 3400 },
  { vMinusI: 2.4, temperature: 3000 },
  { vMinusI: 3.2, temperature: 2600 },
  { vMinusI: 4.2, temperature: 2200 },
];
const BLACKBODY_COLOR_STOPS = [
  [1000, "#ff3800"],
  [1100, "#ff4a00"],
  [1200, "#ff5800"],
  [1300, "#ff6300"],
  [1400, "#ff6d00"],
  [1500, "#ff7600"],
  [1600, "#ff7d00"],
  [1700, "#ff8400"],
  [1800, "#ff8a00"],
  [1900, "#ff8f00"],
  [2000, "#ff950d"],
  [2100, "#ff9b21"],
  [2200, "#ffa02e"],
  [2300, "#ffa639"],
  [2400, "#ffab43"],
  [2500, "#ffb04d"],
  [2600, "#ffb455"],
  [2700, "#ffb85e"],
  [2800, "#ffbc66"],
  [2900, "#ffc06d"],
  [3000, "#ffc475"],
  [3100, "#ffc77c"],
  [3200, "#ffcb83"],
  [3300, "#ffce89"],
  [3400, "#ffd190"],
  [3500, "#ffd496"],
  [3600, "#ffd79c"],
  [3700, "#ffd9a2"],
  [3800, "#ffdca8"],
  [3900, "#ffdead"],
  [4000, "#ffe1b3"],
  [4100, "#ffe3b8"],
  [4200, "#ffe5bd"],
  [4300, "#ffe7c2"],
  [4400, "#ffe9c7"],
  [4500, "#ffebcc"],
  [4600, "#ffedd0"],
  [4700, "#ffefd5"],
  [4800, "#fff1d9"],
  [4900, "#fff2dd"],
  [5000, "#fff4e1"],
  [5100, "#fff6e5"],
  [5200, "#fff7e9"],
  [5300, "#fff8ed"],
  [5400, "#fffaf1"],
  [5500, "#fffbf5"],
  [5600, "#fffdf8"],
  [5700, "#fffefc"],
  [5800, "#ffffff"],
  [5900, "#fcfdff"],
  [6000, "#f9fbff"],
  [6100, "#f6f9ff"],
  [6200, "#f3f7ff"],
  [6300, "#f0f5ff"],
  [6400, "#eef4ff"],
  [6500, "#ebf2ff"],
  [6600, "#e9f0ff"],
  [6700, "#e6efff"],
  [6800, "#e4edff"],
  [6900, "#e2ecff"],
  [7000, "#e0ebff"],
  [7100, "#dee9ff"],
  [7200, "#dce8ff"],
  [7300, "#dbe7ff"],
  [7400, "#d9e6ff"],
  [7500, "#d7e5ff"],
  [7600, "#d6e3ff"],
  [7700, "#d4e2ff"],
  [7800, "#d3e1ff"],
  [7900, "#d1e0ff"],
  [8000, "#d0dfff"],
  [8100, "#cfdeff"],
  [8200, "#cddeff"],
  [8300, "#ccddff"],
  [8400, "#cbdcff"],
  [8500, "#cadbff"],
  [8600, "#c8daff"],
  [8700, "#c7d9ff"],
  [8800, "#c6d9ff"],
  [8900, "#c5d8ff"],
  [9000, "#c4d7ff"],
  [9100, "#c3d6ff"],
  [9200, "#c2d6ff"],
  [9300, "#c1d5ff"],
  [9400, "#c1d4ff"],
  [9500, "#c0d4ff"],
  [9600, "#bfd3ff"],
  [9700, "#bed3ff"],
  [9800, "#bdd2ff"],
  [9900, "#bcd1ff"],
  [10000, "#bcd1ff"],
  [10100, "#bbd0ff"],
  [10200, "#bad0ff"],
  [10300, "#bacfff"],
  [10400, "#b9cfff"],
  [10500, "#b8ceff"],
  [10600, "#b8ceff"],
  [10700, "#b7cdff"],
  [10800, "#b6cdff"],
  [10900, "#b6ccff"],
  [11000, "#b5ccff"],
  [11100, "#b5ccff"],
  [11200, "#b4cbff"],
  [11300, "#b4cbff"],
  [11400, "#b3caff"],
  [11500, "#b2caff"],
  [11600, "#b2caff"],
  [11700, "#b1c9ff"],
  [11800, "#b1c9ff"],
  [11900, "#b1c8ff"],
  [12000, "#b0c8ff"],
  [12100, "#b0c8ff"],
  [12200, "#afc7ff"],
  [12300, "#afc7ff"],
  [12400, "#aec7ff"],
  [12500, "#aec6ff"],
  [12600, "#adc6ff"],
  [12700, "#adc6ff"],
  [12800, "#adc6ff"],
  [12900, "#acc5ff"],
  [13000, "#acc5ff"],
  [13100, "#acc5ff"],
  [13200, "#abc4ff"],
  [13300, "#abc4ff"],
  [13400, "#aac4ff"],
  [13500, "#aac4ff"],
  [13600, "#aac3ff"],
  [13700, "#a9c3ff"],
  [13800, "#a9c3ff"],
  [13900, "#a9c3ff"],
  [14000, "#a9c2ff"],
  [14100, "#a8c2ff"],
  [14200, "#a8c2ff"],
  [14300, "#a8c2ff"],
  [14400, "#a7c1ff"],
  [14500, "#a7c1ff"],
  [14600, "#a7c1ff"],
  [14700, "#a6c1ff"],
  [14800, "#a6c0ff"],
  [14900, "#a6c0ff"],
  [15000, "#a6c0ff"],
  [15100, "#a5c0ff"],
  [15200, "#a5c0ff"],
  [15300, "#a5bfff"],
  [15400, "#a5bfff"],
  [15500, "#a4bfff"],
  [15600, "#a4bfff"],
  [15700, "#a4bfff"],
  [15800, "#a4beff"],
  [15900, "#a4beff"],
  [16000, "#a3beff"],
  [16100, "#a3beff"],
  [16200, "#a3beff"],
  [16300, "#a3beff"],
  [16400, "#a2bdff"],
  [16500, "#a2bdff"],
  [16600, "#a2bdff"],
  [16700, "#a2bdff"],
  [16800, "#a2bdff"],
  [16900, "#a1bdff"],
  [17000, "#a1bcff"],
  [17100, "#a1bcff"],
  [17200, "#a1bcff"],
  [17300, "#a1bcff"],
  [17400, "#a1bcff"],
  [17500, "#a0bcff"],
  [17600, "#a0bcff"],
  [17700, "#a0bbff"],
  [17800, "#a0bbff"],
  [17900, "#a0bbff"],
  [18000, "#a0bbff"],
  [18100, "#9fbbff"],
  [18200, "#9fbbff"],
  [18300, "#9fbbff"],
  [18400, "#9fbbff"],
  [18500, "#9fbaff"],
  [18600, "#9fbaff"],
  [18700, "#9ebaff"],
  [18800, "#9ebaff"],
  [18900, "#9ebaff"],
  [19000, "#9ebaff"],
  [19100, "#9ebaff"],
  [19200, "#9ebaff"],
  [19300, "#9eb9ff"],
  [19400, "#9db9ff"],
  [19500, "#9db9ff"],
  [19600, "#9db9ff"],
  [19700, "#9db9ff"],
  [19800, "#9db9ff"],
  [19900, "#9db9ff"],
  [20000, "#9db9ff"],
  [20100, "#9db9ff"],
  [20200, "#9cb8ff"],
  [20300, "#9cb8ff"],
  [20400, "#9cb8ff"],
  [20500, "#9cb8ff"],
  [20600, "#9cb8ff"],
  [20700, "#9cb8ff"],
  [20800, "#9cb8ff"],
  [20900, "#9cb8ff"],
  [21000, "#9bb8ff"],
  [21100, "#9bb8ff"],
  [21200, "#9bb8ff"],
  [21300, "#9bb7ff"],
  [21400, "#9bb7ff"],
  [21500, "#9bb7ff"],
  [21600, "#9bb7ff"],
  [21700, "#9bb7ff"],
  [21800, "#9bb7ff"],
  [21900, "#9bb7ff"],
  [22000, "#9ab7ff"],
  [22100, "#9ab7ff"],
  [22200, "#9ab7ff"],
  [22300, "#9ab7ff"],
  [22400, "#9ab6ff"],
  [22500, "#9ab6ff"],
  [22600, "#9ab6ff"],
  [22700, "#9ab6ff"],
  [22800, "#9ab6ff"],
  [22900, "#9ab6ff"],
  [23000, "#99b6ff"],
  [23100, "#99b6ff"],
  [23200, "#99b6ff"],
  [23300, "#99b6ff"],
  [23400, "#99b6ff"],
  [23500, "#99b6ff"],
  [23600, "#99b6ff"],
  [23700, "#99b6ff"],
  [23800, "#99b5ff"],
  [23900, "#99b5ff"],
  [24000, "#99b5ff"],
  [24100, "#99b5ff"],
  [24200, "#98b5ff"],
  [24300, "#98b5ff"],
  [24400, "#98b5ff"],
  [24500, "#98b5ff"],
  [24600, "#98b5ff"],
  [24700, "#98b5ff"],
  [24800, "#98b5ff"],
  [24900, "#98b5ff"],
  [25000, "#98b5ff"],
  [25100, "#98b5ff"],
  [25200, "#98b5ff"],
  [25300, "#98b4ff"],
  [25400, "#98b4ff"],
  [25500, "#97b4ff"],
  [25600, "#97b4ff"],
  [25700, "#97b4ff"],
  [25800, "#97b4ff"],
  [25900, "#97b4ff"],
  [26000, "#97b4ff"],
  [26100, "#97b4ff"],
  [26200, "#97b4ff"],
  [26300, "#97b4ff"],
  [26400, "#97b4ff"],
  [26500, "#97b4ff"],
  [26600, "#97b4ff"],
  [26700, "#97b4ff"],
  [26800, "#97b4ff"],
  [26900, "#97b4ff"],
  [27000, "#96b4ff"],
  [27100, "#96b3ff"],
  [27200, "#96b3ff"],
  [27300, "#96b3ff"],
  [27400, "#96b3ff"],
  [27500, "#96b3ff"],
  [27600, "#96b3ff"],
  [27700, "#96b3ff"],
  [27800, "#96b3ff"],
  [27900, "#96b3ff"],
  [28000, "#96b3ff"],
  [28100, "#96b3ff"],
  [28200, "#96b3ff"],
  [28300, "#96b3ff"],
  [28400, "#96b3ff"],
  [28500, "#96b3ff"],
  [28600, "#96b3ff"],
  [28700, "#96b3ff"],
  [28800, "#95b3ff"],
  [28900, "#95b3ff"],
  [29000, "#95b3ff"],
  [29100, "#95b3ff"],
  [29200, "#95b2ff"],
  [29300, "#95b2ff"],
  [29400, "#95b2ff"],
  [29500, "#95b2ff"],
  [29600, "#95b2ff"],
  [29700, "#95b2ff"],
  [29800, "#95b2ff"],
  [29900, "#95b2ff"],
  [30000, "#95b2ff"],
  [30100, "#95b2ff"],
  [30200, "#95b2ff"],
  [30300, "#95b2ff"],
  [30400, "#95b2ff"],
  [30500, "#95b2ff"],
  [30600, "#95b2ff"],
  [30700, "#95b2ff"],
  [30800, "#95b2ff"],
  [30900, "#94b2ff"],
  [31000, "#94b2ff"],
  [31100, "#94b2ff"],
  [31200, "#94b2ff"],
  [31300, "#94b2ff"],
  [31400, "#94b2ff"],
  [31500, "#94b2ff"],
  [31600, "#94b2ff"],
  [31700, "#94b1ff"],
  [31800, "#94b1ff"],
  [31900, "#94b1ff"],
  [32000, "#94b1ff"],
  [32100, "#94b1ff"],
  [32200, "#94b1ff"],
  [32300, "#94b1ff"],
  [32400, "#94b1ff"],
  [32500, "#94b1ff"],
  [32600, "#94b1ff"],
  [32700, "#94b1ff"],
  [32800, "#94b1ff"],
  [32900, "#94b1ff"],
  [33000, "#94b1ff"],
  [33100, "#94b1ff"],
  [33200, "#94b1ff"],
  [33300, "#93b1ff"],
  [33400, "#93b1ff"],
  [33500, "#93b1ff"],
  [33600, "#93b1ff"],
  [33700, "#93b1ff"],
  [33800, "#93b1ff"],
  [33900, "#93b1ff"],
  [34000, "#93b1ff"],
  [34100, "#93b1ff"],
  [34200, "#93b1ff"],
  [34300, "#93b1ff"],
  [34400, "#93b1ff"],
  [34500, "#93b1ff"],
  [34600, "#93b1ff"],
  [34700, "#93b0ff"],
  [34800, "#93b0ff"],
  [34900, "#93b0ff"],
  [35000, "#93b0ff"],
  [35100, "#93b0ff"],
  [35200, "#93b0ff"],
  [35300, "#93b0ff"],
  [35400, "#93b0ff"],
  [35500, "#93b0ff"],
  [35600, "#93b0ff"],
  [35700, "#93b0ff"],
  [35800, "#93b0ff"],
  [35900, "#93b0ff"],
  [36000, "#93b0ff"],
  [36100, "#93b0ff"],
  [36200, "#92b0ff"],
  [36300, "#92b0ff"],
  [36400, "#92b0ff"],
  [36500, "#92b0ff"],
  [36600, "#92b0ff"],
  [36700, "#92b0ff"],
  [36800, "#92b0ff"],
  [36900, "#92b0ff"],
  [37000, "#92b0ff"],
  [37100, "#92b0ff"],
  [37200, "#92b0ff"],
  [37300, "#92b0ff"],
  [37400, "#92b0ff"],
  [37500, "#92b0ff"],
  [37600, "#92b0ff"],
  [37700, "#92b0ff"],
  [37800, "#92b0ff"],
  [37900, "#92b0ff"],
  [38000, "#92b0ff"],
  [38100, "#92b0ff"],
  [38200, "#92b0ff"],
  [38300, "#92b0ff"],
  [38400, "#92b0ff"],
  [38500, "#92afff"],
  [38600, "#92afff"],
  [38700, "#92afff"],
  [38800, "#92afff"],
  [38900, "#92afff"],
  [39000, "#92afff"],
  [39100, "#92afff"],
  [39200, "#92afff"],
  [39300, "#92afff"],
  [39400, "#92afff"],
  [39500, "#92afff"],
  [39600, "#92afff"],
  [39700, "#92afff"],
  [39800, "#91afff"],
  [39900, "#91afff"],
  [40000, "#91afff"],
];
const BLACKBODY_DISPLAY_WHITEPOINT_TEMPERATURE = 5800;
const BLACKBODY_DISPLAY_WHITEPOINT_RGB = [255, 255, 255];
const BLACKBODY_DISPLAY_CHROMA_BOOST = 1.2;
const COLOR_CONTRAST_MIN = 1;
const COLOR_CONTRAST_MAX = 5;
const COLOR_CONTRAST_DEFAULT = 2;
const SKY_GRID_CONFIGS = {
  equatorial: {
    id: "equatorial",
    longitudeStep: EQUATORIAL_GRID_RA_STEP_DEGREES,
    latitudeStep: EQUATORIAL_GRID_DEC_STEP_DEGREES,
    lineColor: "rgba(132, 166, 255, 0.46)",
    labelColor: "rgba(229, 229, 229, 0.94)",
    lineWidth: 1.25,
    lineDash: [],
    longitudeLabel: formatRaGridLabel,
    latitudeLabel: (value) => `Dec ${formatSignedGridDegrees(value)}`,
    vectorFor: vectorFromEquatorial,
  },
  galactic: {
    id: "galactic",
    longitudeStep: GALACTIC_GRID_LON_STEP_DEGREES,
    latitudeStep: GALACTIC_GRID_LAT_STEP_DEGREES,
    lineColor: "rgba(252, 174, 44, 0.52)",
    labelColor: "rgba(229, 229, 229, 0.94)",
    lineWidth: 1.3,
    lineDash: [6, 5],
    longitudeLabel: (value) => `l ${Math.round(value)}°`,
    latitudeLabel: (value) => `b ${formatSignedGridDegrees(value)}`,
    vectorFor: vectorFromLonLat,
  },
};

const canvas = document.querySelector("#scene");
const ctx = canvas.getContext("2d", { alpha: false });
const redClumpCanvas = document.querySelector("#redClumpScene");
const catalogCanvas = document.querySelector("#catalogScene");
const catalogDynamicCanvas = document.querySelector("#catalogDynamicScene");
const selectionCanvas = document.querySelector("#selectionScene");
const selectionCtx = selectionCanvas?.getContext("2d");
const URL_PARAMS = new URLSearchParams(window.location.search);
const PERF_HUD_ENABLED = URL_PARAMS.has("perf");
const PULSE_LOD_ENABLED = URL_PARAMS.get("pulseLod") !== "off";
const CATALOG_GPU_ENABLED = URL_PARAMS.get("catalogGpu") !== "off";
const NAVIGATION_SLOW_PULSE_REFRESH_FLOOR_MS = navigationSlowPulseRefreshFloorMsFromUrl();
const MOBILE_CONTROLS_MEDIA = window.matchMedia("(max-width: 860px)");
const MOBILE_TOUCH_MOVE_THRESHOLD = 7;
const MOBILE_PINCH_MOVE_THRESHOLD = 3;
const MOBILE_TARGET_PICK_RADIUS_SCALE = 2.25;
const MOBILE_DOUBLE_TAP_MAX_MS = 620;
const MOBILE_DOUBLE_TAP_MAX_DISTANCE = 28;
const MOBILE_ROTATE_ANGLE_THRESHOLD = 0.06;
const MOBILE_ROTATE_SENSITIVITY = 0.25;
const MOBILE_STAR_BASE_RADIUS_SCALE = 0.5;
const MOBILE_DRAWER_SWIPE_CLOSE_DISTANCE = 58;
let mobileControlsOpen = false;
let pendingUncertaintySeed = null;
let uncertaintySeedFrame = 0;

const controls = {
  yaw: document.querySelector("#yaw"),
  pitch: document.querySelector("#pitch"),
  roll: document.querySelector("#roll"),
  zoom: document.querySelector("#zoom"),
  radiusScale: document.querySelector("#radiusScale"),
  colorContrast: document.querySelector("#colorContrast"),
  uncertaintySeed: document.querySelector("#uncertaintySeed"),
  panLock: document.querySelector("#panLock"),
  pulsationSpeed: document.querySelector("#pulsationSpeed"),
  pulsationAmplitude: document.querySelector("#pulsationAmplitude"),
  datasetPresetToggle: document.querySelector("#datasetPresetToggle"),
  mobilePresetToggle: document.querySelector("#mobilePresetToggle"),
  targetSearch: document.querySelector("#targetSearch"),
};

const outputs = {
  yaw: document.querySelector("#yawValue"),
  pitch: document.querySelector("#pitchValue"),
  roll: document.querySelector("#rollValue"),
  zoom: document.querySelector("#zoomValue"),
  radiusScale: document.querySelector("#radiusValue"),
  colorContrast: document.querySelector("#colorContrastValue"),
  uncertaintySeed: document.querySelector("#uncertaintySeedValue"),
  pulsationSpeed: document.querySelector("#pulsationSpeedValue"),
  pulsationAmplitude: document.querySelector("#pulsationAmplitudeValue"),
  visibleTotal: document.querySelector("#visibleTotal"),
  depthSpan: document.querySelector("#depthSpan"),
  cepheidCount: document.querySelector("#cepheidCount"),
  rrCount: document.querySelector("#rrCount"),
  miraCount: document.querySelector("#miraCount"),
  rcCount: document.querySelector("#rcCount"),
  clusterCount: document.querySelector("#clusterCount"),
  pulsationDaySeconds: document.querySelector("#pulsationDaySeconds"),
};

const elements = {
  atlas: document.querySelector(".atlas"),
  masthead: document.querySelector(".masthead"),
  panel: document.querySelector("#atlasControls"),
  loading: document.querySelector("#loading"),
  legend: document.querySelector("#spectralLegend"),
  target: document.querySelector("#target"),
  sources: document.querySelector("#sourceLinks"),
  coordinateFrames: document.querySelector("#coordinateFrameControls"),
  coordinateCenters: document.querySelector("#coordinateCenterControls"),
  coordinateHud: document.querySelector(".coordinateHud"),
  coordinateReadout: document.querySelector("#coordinateReadout"),
  faceView: document.querySelector("#faceView"),
  edgeView: document.querySelector("#edgeView"),
  pulsationClockHourHand: document.querySelector("#pulsationClockHourHand"),
  perfHud: document.querySelector("#perfHud"),
  scaleBar: document.querySelector("#scaleBar"),
  scaleBarValue: document.querySelector("#scaleBarValue"),
  overlayToggle: document.querySelector("#overlayToggle"),
  mobileControlsToggle: document.querySelector("#mobileControlsToggle"),
  mobileControlsBackdrop: document.querySelector("#mobileControlsBackdrop"),
  mobileControlsClose: document.querySelector("#mobileControlsClose"),
  mobileTargetPreview: document.querySelector("#mobileTargetPreview"),
  mobileTargetPreviewName: document.querySelector("#mobileTargetPreviewName"),
  mobileTargetPreviewPlot: document.querySelector("#mobileTargetPreviewPlot"),
  mobilePanelHeader: document.querySelector(".mobilePanelHeader"),
  shortcutHelp: document.querySelector("#shortcutHelp"),
  shortcutHelpList: document.querySelector("#shortcutHelpList"),
  shortcutHelpClose: document.querySelector("#shortcutHelpClose"),
};

const state = {
  yaw: 0,
  pitch: 0,
  roll: 0,
  zoom: DEFAULT_ZOOM_SCALE,
  panX: 0,
  panY: 0,
  radiusScale: defaultRadiusScaleForPreset(PULSATOR_DEFAULT_PRESET),
  colorContrast: COLOR_CONTRAST_DEFAULT,
  datasetExposure: {
    cepheids: DATASET_EXPOSURE_DEFAULT,
    rrlyrae: DATASET_EXPOSURE_DEFAULT,
    anomalousCepheids: DATASET_EXPOSURE_DEFAULT,
    miras: DATASET_EXPOSURE_DEFAULT,
    redclump: RED_CLUMP_EXPOSURE_DEFAULT,
    clusters: DATASET_EXPOSURE_DEFAULT,
  },
  depthScale: 1,
  density: 100,
  pulsationSpeedLog: Math.log10(INITIAL_PULSATION_SPEED),
  pulsationSpeed: INITIAL_PULSATION_SPEED,
  pulsationAmplitudeScale: defaultPulsationAmplitudeScaleForPreset(PULSATOR_DEFAULT_PRESET),
  uncertaintySeed: DEFAULT_UNCERTAINTY_SEED,
  datasetPreset: null,
  pulsatorPreset: null,
  datasets: {
    cepheids: true,
    rrlyrae: true,
    anomalousCepheids: true,
    miras: true,
    redclump: true,
    clusters: true,
  },
  spectral: new Set([0, 1, 2, 3, 4, 5]),
  coordinateFrame: "atlas",
  coordinateCenter: "bridge",
  centerSelection: "bridge",
  customCoordinateContext: null,
  panLock: true,
  equatorialGrid: false,
  galacticGrid: false,
  cursorClientX: null,
  cursorClientY: null,
  targetSearchQuery: "",
  hovered: null,
  locked: null,
  cameraLocked: false,
  cameraFollowsLockedTarget: false,
  overlaysHidden: false,
  pulsationPaused: false,
};

const editableMultiplierConfigs = {
  yaw: {
    label: "yaw",
    digits: 0,
    inputMode: "decimal",
    unit: "°",
    min: () => Number(controls.yaw.min),
    max: () => Number(controls.yaw.max),
    get: () => radiansToDegrees(state.yaw),
    set: (value) => setOrbitAngle("yaw", value),
  },
  pitch: {
    label: "pitch",
    digits: 0,
    inputMode: "decimal",
    unit: "°",
    min: () => Number(controls.pitch.min),
    max: () => Number(controls.pitch.max),
    get: () => radiansToDegrees(state.pitch),
    set: (value) => setOrbitAngle("pitch", value),
  },
  roll: {
    label: "roll",
    digits: 0,
    inputMode: "decimal",
    unit: "°",
    min: () => Number(controls.roll.min),
    max: () => Number(controls.roll.max),
    get: () => radiansToDegrees(state.roll),
    set: (value) => setOrbitAngle("roll", value),
  },
  zoom: {
    label: "zoom",
    digits: 2,
    inputMode: "decimal",
    min: () => ZOOM_SCALE_MIN,
    max: () => ZOOM_SCALE_MAX,
    get: () => state.zoom,
    set: (value) => setZoom(value),
  },
  radiusScale: {
    label: "radius",
    digits: 2,
    inputMode: "decimal",
    min: () => RADIUS_SCALE_MIN,
    max: () => RADIUS_SCALE_MAX,
    get: () => state.radiusScale,
    set: (value) => {
      state.radiusScale = clampRadiusScale(value);
      markRedClumpLayerDirty();
      queueRender();
    },
  },
  colorContrast: {
    label: "color",
    digits: 2,
    inputMode: "decimal",
    min: () => COLOR_CONTRAST_MIN,
    max: () => COLOR_CONTRAST_MAX,
    get: () => state.colorContrast,
    set: (value) => setColorContrast(value),
  },
  uncertaintySeed: {
    label: "seed",
    digits: 0,
    inputMode: "numeric",
    unit: "",
    min: () => DEFAULT_UNCERTAINTY_SEED,
    max: () => UNCERTAINTY_SEED_MAX,
    get: () => state.uncertaintySeed,
    set: (value) => setUncertaintySeed(value),
  },
  pulsationSpeed: {
    label: "speed",
    digits: 0,
    inputMode: "numeric",
    min: () => 10 ** Number(controls.pulsationSpeed.min),
    max: () => 10 ** Number(controls.pulsationSpeed.max),
    get: () => state.pulsationSpeed,
    set: (value) => {
      setPulsationSpeed(value);
      markCatalogStaticDirty();
      queueRender();
    },
  },
  pulsationAmplitude: {
    label: "amplitude",
    digits: 1,
    inputMode: "decimal",
    min: () => PULSATION_AMPLITUDE_MIN,
    max: () => PULSATION_AMPLITUDE_MAX,
    get: () => state.pulsationAmplitudeScale,
    set: (value) => {
      state.pulsationAmplitudeScale = clampPulsationAmplitudeScale(value);
      queueRender();
    },
  },
};

const scene = {
  width: 0,
  height: 0,
  dpr: 1,
  centerX: 0,
  centerY: 0,
  scale: 1,
  temperatureAnchors: V_MINUS_I_TEMPERATURE_ANCHORS,
  temperatureGrid: null,
  meanMetallicityFeHByLocation: DEFAULT_MEAN_METALLICITY_FEH_BY_LOCATION,
  miraTemperatureSources: [],
  payload: null,
  catalog: [],
  redClump: [],
  redClumpSurface: [],
  clusters: [],
  clusterStars: [],
  clusterStarsByCluster: new Map(),
  activeCatalog: [],
  activeRedClump: [],
  activeClusters: [],
  activeClusterStars: [],
  activeClusterPulsatorStars: [],
  activeClusterStarsByCluster: [],
  activeClusterStarCountsByCluster: [],
  activeClusterStarRenderCount: 0,
  clusterStarLodAlphaByCluster: [],
  clusterPulsatorStats: null,
  catalogDrawList: [],
  catalogDrawListScreenProjected: true,
  catalogProjectionFastPending: false,
  catalogAnimatedDrawList: [],
  catalogWorldStaticDrawList: [],
  redClumpDrawList: [],
  redClumpSurfaceDrawList: [],
  clusterTargetDrawList: [],
  catalogStaticCanvas: document.createElement("canvas"),
  catalogStaticCtx: null,
  catalogStaticDirty: true,
  catalogStaticCounts: { animated: 0, static: 0 },
  catalogStaticRadiusScale: null,
  catalogStaticExposureSignature: null,
  catalogStaticPulsationSpeed: null,
  catalogStaticPulsationAmplitudeScale: null,
  catalogStaticPulsatorPreset: null,
  catalogStaticPulseLodActive: null,
  catalogStaticProjectionMode: null,
  catalogStaticCacheVersion: 0,
  catalogStaticRenderer: null,
  catalogRenderer: null,
  redClumpRenderer: null,
  redClumpGpuDirty: true,
  clusterStarGpuDirty: true,
  redClumpStaticCanvas: redClumpCanvas || document.createElement("canvas"),
  redClumpStaticCtx: null,
  redClumpStaticDirty: true,
  redClumpStaticSignature: null,
  gpuLayerFrameActive: false,
  limbSpriteCache: new Map(),
  colorBuckets: new Map(),
  staticColorBuckets: new Map(),
  cachedStats: {
    catalog: { count: 0, minDepth: Infinity, maxDepth: -Infinity },
    redClump: { count: 0, minDepth: Infinity, maxDepth: -Infinity },
  },
  coordinateContext: null,
  coordinateCacheKey: null,
  skyGridBounds: null,
  activePointsDirty: true,
  spectralClasses: [],
  bounds: null,
};
scene.catalogStaticCtx = scene.catalogStaticCanvas.getContext("2d");
scene.catalogStaticRenderer = createCatalogRenderer(catalogCanvas, { preserveDrawingBuffer: true });
scene.catalogRenderer = scene.catalogStaticRenderer ? createCatalogRenderer(catalogDynamicCanvas) : null;
if (!scene.catalogRenderer) scene.catalogStaticRenderer = null;
scene.redClumpRenderer = createRedClumpLayerRenderer(redClumpCanvas);
scene.redClumpStaticCtx = scene.redClumpRenderer ? null : scene.redClumpStaticCanvas.getContext("2d");

let renderQueued = false;
let projectionDirty = true;
let dragging = false;
let dragStart = null;
let movedDuringDrag = false;
let touchGesture = null;
let drawerSwipeGesture = null;
const activeTouchPointers = new Map();
let hoverTimer = 0;
let hoverSuppressedUntil = 0;
let pointerMode = "orbit";
let loadingProgress = 0;
let activeLightcurveInsets = [];
let lastRightClick = { time: 0, x: 0, y: 0 };
let lastMobileTap = { time: 0, x: 0, y: 0, target: null };
let introRotation = null;
let introCloudLabelAnimation = null;
let axisSpinAnimation = null;
let datasetPresetPreview = null;
const animationEpoch = 6000;
const animationStartMs = performance.now();
let simulationTimeOffsetDays = 0;
let pausedSimulationDay = null;
let previousCustomView = null;
let lastTargetNavigationStep = null;
let orientationGridLastActivityMs = animationStartMs;
let navigationActivityUntilMs = 0;
const WAVEFORM_SAMPLES = 96;
const LIGHTCURVE_INSET_CYCLES = 2;
const MIRA_LIGHTCURVE_INSET_CYCLES = 10;
const MIRA_AMPLITUDE_STATS_CYCLES = 30;
const SVG_NS = "http://www.w3.org/2000/svg";
const colorCache = new Map();
const catalogTemperatureColorCache = new Map();
const CATALOG_TEMPERATURE_COLOR_CACHE_MAX = 500_000;
const TEMPERATURE_GRID_METALLICITY_CACHE_PRECISION = 20;
const catalogRenderColorCache = new Map();
const perfState = {
  catalogMs: 0,
  projectionMs: 0,
  redClumpMs: 0,
  lastHudMs: 0,
  animatedCatalog: 0,
  staticCatalog: 0,
};

function degreesToRadians(value) {
  return (value * Math.PI) / 180;
}

function radiansToRawDegrees(value) {
  return (value * 180) / Math.PI;
}

function radiansToDegrees(value) {
  return Math.round(radiansToRawDegrees(value));
}

function normalizeRadians(value) {
  let angle = (value + Math.PI) % (Math.PI * 2);
  if (angle < 0) angle += Math.PI * 2;
  return angle - Math.PI;
}

function orbitAnglesMatchPreset(preset) {
  return Object.entries(preset).every(([axis, degrees]) => {
    const delta = normalizeRadians(state[axis] - degreesToRadians(degrees));
    return Math.abs(delta) < 1e-9;
  });
}

function observedViewYaw() {
  return normalizeRadians(state.yaw + degreesToRadians(OBSERVED_VIEW_YAW_DEGREES));
}

function observedViewRoll() {
  return normalizeRadians(state.roll + degreesToRadians(OBSERVED_VIEW_ROLL_DEGREES));
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function easeOutSine(value) {
  return Math.sin(clamp(value, 0, 1) * Math.PI * 0.5);
}

function markOrientationGridActive(now = performance.now()) {
  orientationGridLastActivityMs = now;
}

function orientationGridAlpha(now = performance.now()) {
  const elapsed = now - orientationGridLastActivityMs;
  if (elapsed <= ORIENTATION_GRID_VISIBLE_MS) return 1;
  return 1 - smoothStep((elapsed - ORIENTATION_GRID_VISIBLE_MS) / ORIENTATION_GRID_FADE_MS);
}

function navigationSlowPulseRefreshFloorMsFromUrl() {
  const rawValue = URL_PARAMS.get("navPulseFloorMs") ?? URL_PARAMS.get("navPulseMs");
  if (rawValue === null) return NAVIGATION_SLOW_PULSE_REFRESH_FLOOR_DEFAULT_MS;
  if (["off", "false"].includes(rawValue.toLowerCase())) return 0;
  const value = Number(rawValue);
  if (!Number.isFinite(value)) return NAVIGATION_SLOW_PULSE_REFRESH_FLOOR_DEFAULT_MS;
  return clamp(value, 0, 1000);
}

function navigationActivityActive(now = performance.now()) {
  return now < navigationActivityUntilMs;
}

function navigationPulseRefreshFloorActive(now = performance.now()) {
  return (
    PULSE_LOD_ENABLED &&
    CATALOG_PULSE_ALL_STARS &&
    NAVIGATION_SLOW_PULSE_REFRESH_FLOOR_MS > SLOW_PULSE_REFRESH_FRAME_INTERVAL_MS + 1 &&
    navigationActivityActive(now)
  );
}

function shouldUseCatalogPulseLod(now = performance.now()) {
  void now;
  return PULSE_LOD_ENABLED && !CATALOG_PULSE_ALL_STARS;
}

function catalogPulseModeLabel(now = performance.now()) {
  if (!PULSE_LOD_ENABLED) return "all";
  if (!CATALOG_PULSE_ALL_STARS) return "lod";
  if (navigationPulseRefreshFloorActive(now)) {
    return `nav pulse floor ${Math.round(NAVIGATION_SLOW_PULSE_REFRESH_FLOOR_MS)} ms`;
  }
  return navigationActivityActive(now) ? "nav projection" : "all";
}

function markNavigationActivityActive(now = performance.now()) {
  navigationActivityUntilMs = Math.max(
    navigationActivityUntilMs,
    now + NAVIGATION_ACTIVITY_SETTLE_MS,
  );
}

function slowPulseAdaptiveRefreshIntervalMsForPeriod(periodSeconds) {
  if (
    !Number.isFinite(periodSeconds) ||
    periodSeconds <= ADAPTIVE_PULSE_REFRESH_PERIOD_SECONDS
  ) {
    return 0;
  }

  const ease = smoothStep(
    (periodSeconds - ADAPTIVE_PULSE_REFRESH_PERIOD_SECONDS) /
      Math.max(
        0.001,
        SLOW_PULSE_REFRESH_EASE_END_SECONDS - ADAPTIVE_PULSE_REFRESH_PERIOD_SECONDS,
      ),
  );
  const targetIntervalMs = clamp(
    (periodSeconds * 1000) / SLOW_PULSE_REFRESH_SAMPLES_PER_CYCLE,
    SLOW_PULSE_REFRESH_FRAME_INTERVAL_MS,
    SLOW_PULSE_REFRESH_MAX_INTERVAL_MS,
  );
  return (
    SLOW_PULSE_REFRESH_FRAME_INTERVAL_MS +
    (targetIntervalMs - SLOW_PULSE_REFRESH_FRAME_INTERVAL_MS) * ease
  );
}

function updateSlowPulseRefreshSchedule(item) {
  const point = item?.point;
  if (!item) return;
  if (!point?.lightCurve) {
    item.slowPulseScheduleSpeed = state.pulsationSpeed;
    item.slowPulseScheduleLightCurve = null;
    item.slowPulseRenderedPeriodSeconds = Infinity;
    item.slowPulseAdaptiveRefreshIntervalMs = 0;
    item.slowPulseRefreshPhase = 0;
    return;
  }
  if (
    item.slowPulseScheduleSpeed === state.pulsationSpeed &&
    item.slowPulseScheduleLightCurve === point.lightCurve
  ) {
    return;
  }

  const periodSeconds = renderedPulsationPeriodSeconds(point);
  item.slowPulseScheduleSpeed = state.pulsationSpeed;
  item.slowPulseScheduleLightCurve = point.lightCurve;
  item.slowPulseRenderedPeriodSeconds = periodSeconds;
  item.slowPulseAdaptiveRefreshIntervalMs =
    slowPulseAdaptiveRefreshIntervalMsForPeriod(periodSeconds);
  item.slowPulseRefreshPhase = (point.sample || 0) / 100;
}

function slowPulseRefreshIntervalMs(item, useNavigationPulseFloor = false) {
  if (!item) return 0;
  updateSlowPulseRefreshSchedule(item);
  const adaptiveIntervalMs = item.slowPulseAdaptiveRefreshIntervalMs || 0;
  if (!useNavigationPulseFloor) return adaptiveIntervalMs;
  return Math.max(adaptiveIntervalMs, NAVIGATION_SLOW_PULSE_REFRESH_FLOOR_MS);
}

function clampDatasetExposure(value) {
  return clamp(value, DATASET_EXPOSURE_MIN, DATASET_EXPOSURE_MAX);
}

function clampPulsationSpeed(value) {
  return clamp(value, PULSATION_SPEED_MIN, PULSATION_SPEED_MAX);
}

function clampPulsationAmplitudeScale(value) {
  return clamp(value, PULSATION_AMPLITUDE_MIN, PULSATION_AMPLITUDE_MAX);
}

function clampRadiusScale(value) {
  return clamp(value, RADIUS_SCALE_MIN, RADIUS_SCALE_MAX);
}

function clampColorContrast(value) {
  const numeric = Number(value);
  return clamp(Number.isFinite(numeric) ? numeric : COLOR_CONTRAST_DEFAULT, COLOR_CONTRAST_MIN, COLOR_CONTRAST_MAX);
}

function clampUncertaintySeed(value) {
  const seed = Number(value);
  if (!Number.isFinite(seed)) return DEFAULT_UNCERTAINTY_SEED;
  return Math.trunc(clamp(seed, DEFAULT_UNCERTAINTY_SEED, UNCERTAINTY_SEED_MAX));
}

function selectedTargetForDeepZoom() {
  return state.locked || null;
}

function targetZoomUsableViewportSize() {
  const width = scene.width || window.innerWidth || 0;
  const height = scene.height || window.innerHeight || 0;
  let usableWidth = width;
  let usableHeight = height;
  const panelRect = elements.panel?.getBoundingClientRect?.();
  if (
    !state.overlaysHidden &&
    panelRect &&
    panelRect.width > 0 &&
    panelRect.height > 0 &&
    panelRect.right > 0 &&
    panelRect.bottom > 0 &&
    panelRect.left < width &&
    panelRect.top < height
  ) {
    if (panelRect.left > width * 0.5) usableWidth = Math.min(usableWidth, panelRect.left);
    if (panelRect.top > height * 0.5) usableHeight = Math.min(usableHeight, panelRect.top);
  }
  return { width: usableWidth, height: usableHeight };
}

function targetZoomLimitRadius() {
  const { width, height } = targetZoomUsableViewportSize();
  const viewportSize = Math.min(width, height);
  return Math.max(48, viewportSize * TARGET_ZOOM_SCREEN_DIAMETER_FRACTION * 0.5);
}

function targetZoomForRadiusLimit(target, low, high, limitRadius) {
  if (targetSelectionRadiusAtZoom(target, low) >= limitRadius) return low;
  if (targetSelectionRadiusAtZoom(target, high) < limitRadius) return high;

  for (let index = 0; index < 28; index += 1) {
    const mid = Math.sqrt(low * high);
    if (targetSelectionRadiusAtZoom(target, mid) < limitRadius) low = mid;
    else high = mid;
  }
  return high;
}

function targetZoomScaleMax(target = selectedTargetForDeepZoom()) {
  if (!target || scene.width <= 0 || scene.height <= 0) return ZOOM_SCALE_MAX;

  const limitRadius = targetZoomLimitRadius();
  const radiusAtSliderMax = targetSelectionRadiusAtZoom(target, ZOOM_SCALE_MAX);
  if (!Number.isFinite(radiusAtSliderMax)) return ZOOM_SCALE_MAX;
  if (radiusAtSliderMax >= limitRadius) {
    return targetZoomForRadiusLimit(target, ZOOM_SCALE_MIN, ZOOM_SCALE_MAX, limitRadius);
  }
  return targetZoomForRadiusLimit(target, ZOOM_SCALE_MAX, TARGET_ZOOM_SCALE_MAX, limitRadius);
}

function clampZoomScale(value, { allowTargetZoom = false, target = selectedTargetForDeepZoom() } = {}) {
  const targetMaxZoom = target ? targetZoomScaleMax(target) : ZOOM_SCALE_MAX;
  const maxZoom = allowTargetZoom ? targetMaxZoom : Math.min(ZOOM_SCALE_MAX, targetMaxZoom);
  return clamp(value, ZOOM_SCALE_MIN, maxZoom);
}

function effectiveZoomScale(value = state.zoom) {
  const zoom = Number.isFinite(value) ? value : DEFAULT_ZOOM_SCALE;
  return Math.max(ZOOM_SCALE_MIN, zoom) * ZOOM_BASE_SCALE;
}

function logarithmicZoomFade(value, start, end) {
  const zoom = Math.max(ZOOM_SCALE_MIN, Number.isFinite(value) ? value : DEFAULT_ZOOM_SCALE);
  if (end <= start) return zoom >= end ? 1 : 0;
  const logZoom = Math.log10(zoom);
  return smoothStep((logZoom - Math.log10(start)) / (Math.log10(end) - Math.log10(start)));
}

function redClumpZoomFade(value = state.zoom) {
  return 1 - logarithmicZoomFade(value, RED_CLUMP_ZOOM_FADE_START, RED_CLUMP_ZOOM_FADE_END);
}

function starRadiusDeepZoomScale(value = state.zoom) {
  const fade = logarithmicZoomFade(value, STAR_RADIUS_DEEP_ZOOM_FADE_START, STAR_RADIUS_DEEP_ZOOM_FADE_END);
  return 1 - (1 - STAR_RADIUS_DEEP_ZOOM_MIN_SCALE) * fade;
}

function panDragSensitivity(value = state.zoom) {
  const zoom = Number.isFinite(value) ? value : DEFAULT_ZOOM_SCALE;
  const zoomSteps = Math.max(0, Math.log2(Math.max(1, zoom)));
  return Math.max(PAN_DRAG_MIN_SENSITIVITY, 1 / (1 + zoomSteps * PAN_DRAG_ZOOM_DAMPING));
}

function orbitDragSensitivity(value = state.zoom) {
  const zoom = Number.isFinite(value) ? value : DEFAULT_ZOOM_SCALE;
  const zoomSteps = Math.max(0, Math.log2(Math.max(1, zoom)));
  return Math.max(ORBIT_DRAG_MIN_SENSITIVITY, 1 / (1 + zoomSteps * ORBIT_DRAG_ZOOM_DAMPING));
}

function wrapDegrees(value) {
  let angle = (value + 180) % 360;
  if (angle < 0) angle += 360;
  return angle - 180;
}

function normalizeDegrees360(value) {
  return positiveModulo(value, 360);
}

function vectorLength(vector) {
  return Math.hypot(vector[0], vector[1], vector[2]);
}

function vectorFromLonLat(lonDeg, latDeg, distance) {
  const lon = degreesToRadians(lonDeg);
  const lat = degreesToRadians(latDeg);
  return [
    distance * Math.cos(lat) * Math.cos(lon),
    distance * Math.cos(lat) * Math.sin(lon),
    distance * Math.sin(lat),
  ];
}

function lonLatFromVector(vector) {
  const radius = vectorLength(vector);
  if (radius === 0) return { lon: 0, lat: 0, distance: 0 };
  return {
    lon: (radiansToRawDegrees(Math.atan2(vector[1], vector[0])) + 360) % 360,
    lat: radiansToRawDegrees(Math.asin(vector[2] / radius)),
    distance: radius,
  };
}

function equatorialFromGalacticVector(vector) {
  const radius = vectorLength(vector);
  if (radius === 0) return { ra: 0, dec: 0 };
  const unit = vector.map((component) => component / radius);
  const equatorial = GALACTIC_TO_EQUATORIAL_J2000.map((row) =>
    row[0] * unit[0] + row[1] * unit[1] + row[2] * unit[2],
  );
  return {
    ra: (radiansToRawDegrees(Math.atan2(equatorial[1], equatorial[0])) + 360) % 360,
    dec: radiansToRawDegrees(Math.asin(clamp(equatorial[2], -1, 1))),
  };
}

function galacticFromEquatorialVector(equatorial) {
  return [
    GALACTIC_TO_EQUATORIAL_J2000[0][0] * equatorial[0] +
      GALACTIC_TO_EQUATORIAL_J2000[1][0] * equatorial[1] +
      GALACTIC_TO_EQUATORIAL_J2000[2][0] * equatorial[2],
    GALACTIC_TO_EQUATORIAL_J2000[0][1] * equatorial[0] +
      GALACTIC_TO_EQUATORIAL_J2000[1][1] * equatorial[1] +
      GALACTIC_TO_EQUATORIAL_J2000[2][1] * equatorial[2],
    GALACTIC_TO_EQUATORIAL_J2000[0][2] * equatorial[0] +
      GALACTIC_TO_EQUATORIAL_J2000[1][2] * equatorial[1] +
      GALACTIC_TO_EQUATORIAL_J2000[2][2] * equatorial[2],
  ];
}

function vectorFromEquatorial(raDeg, decDeg, distance) {
  const ra = degreesToRadians(raDeg);
  const dec = degreesToRadians(decDeg);
  const equatorial = [
    Math.cos(dec) * Math.cos(ra),
    Math.cos(dec) * Math.sin(ra),
    Math.sin(dec),
  ];
  return galacticFromEquatorialVector(equatorial).map((component) => component * distance);
}

function subtractVectors(left, right) {
  return [left[0] - right[0], left[1] - right[1], left[2] - right[2]];
}

function rotateTangentBasis(east, north, angleDegrees) {
  const angle = degreesToRadians(angleDegrees);
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  return {
    east: [
      east[0] * cos - north[0] * sin,
      east[1] * cos - north[1] * sin,
      east[2] * cos - north[2] * sin,
    ],
    north: [
      east[0] * sin + north[0] * cos,
      east[1] * sin + north[1] * cos,
      east[2] * sin + north[2] * cos,
    ],
  };
}

function makeEquatorialBasis(origin) {
  const center = equatorialFromGalacticVector(origin);
  const ra = degreesToRadians(center.ra);
  const dec = degreesToRadians(center.dec);
  const radialLength = vectorLength(origin);
  const radial =
    radialLength > 0
      ? origin.map((component) => component / radialLength)
      : galacticFromEquatorialVector([Math.cos(dec) * Math.cos(ra), Math.cos(dec) * Math.sin(ra), Math.sin(dec)]);

  const tangent = rotateTangentBasis(
    galacticFromEquatorialVector([-Math.sin(ra), Math.cos(ra), 0]),
    galacticFromEquatorialVector([-Math.sin(dec) * Math.cos(ra), -Math.sin(dec) * Math.sin(ra), Math.cos(dec)]),
    DEFAULT_VIEW_AXIS_ROTATION_DEGREES,
  );

  return {
    east: tangent.east,
    north: tangent.north,
    radial,
  };
}

function projectLocalVector(vector, origin, basis) {
  const delta = subtractVectors(vector, origin);
  return ["east", "north", "radial"].map((axis) => {
    const basisVector = basis[axis];
    return delta[0] * basisVector[0] + delta[1] * basisVector[1] + delta[2] * basisVector[2];
  });
}

function angularCoordinate(lonDeg, latDeg, distance, center) {
  const centerLat = degreesToRadians(center.lat);
  const distanceScale = center.distance;
  return [
    degreesToRadians(wrapDegrees(lonDeg - center.lon)) * Math.cos(centerLat) * distanceScale,
    degreesToRadians(latDeg - center.lat) * distanceScale,
    distance - center.distance,
  ];
}

function formatNumber(value, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "n/a";
  }
  return Number(value).toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function formatKpcValue(value, digits = 1) {
  return Number.isFinite(value) ? `${formatNumber(value, digits)} kpc` : "";
}

function scaleBarKpcCandidates(targetKpc) {
  if (!Number.isFinite(targetKpc) || targetKpc <= 0) return [1];
  const exponent = Math.floor(Math.log10(targetKpc));
  const candidates = [];
  for (let power = exponent - 3; power <= exponent + 3; power += 1) {
    const magnitude = 10 ** power;
    for (const multiplier of SCALE_BAR_NICE_MULTIPLIERS) {
      candidates.push(multiplier * magnitude);
    }
  }
  return candidates;
}

function scaleBarLengthKpc(scale, targetWidth, maxWidth) {
  const targetKpc = targetWidth / scale;
  let best = null;
  for (const kpc of scaleBarKpcCandidates(targetKpc)) {
    const width = kpc * scale;
    const inRange = width >= SCALE_BAR_MIN_WIDTH_PX && width <= maxWidth;
    const score = Math.abs(Math.log(width / targetWidth)) + (inRange ? 0 : 10);
    if (!best || score < best.score) {
      best = { kpc, score };
    }
  }
  return best?.kpc || targetKpc;
}

function formatScaleBarLabel(kpc) {
  const value = Math.abs(kpc);
  if (value < 0.1) {
    const pc = kpc * 1000;
    const pcValue = Math.abs(pc);
    const pcDigits = pcValue >= 10 ? 0 : pcValue >= 1 ? 1 : 2;
    return `${formatNumberCompact(pc, pcDigits)} pc`;
  }
  const digits = value >= 20 ? 0 : value >= 2 ? 1 : value >= 0.2 ? 2 : value >= 0.02 ? 3 : 4;
  return `${formatNumberCompact(kpc, digits)} kpc`;
}

function updateScaleBar() {
  if (!elements.scaleBar || !elements.scaleBarValue) return;
  const scale = Number(scene.scale);
  if (!Number.isFinite(scale) || scale <= 0) return;

  const viewportMaxWidth =
    scene.width > 0 ? scene.width * SCALE_BAR_MAX_VIEWPORT_FRACTION : SCALE_BAR_MAX_WIDTH_PX;
  const maxWidth = Math.max(SCALE_BAR_MIN_WIDTH_PX, Math.min(SCALE_BAR_MAX_WIDTH_PX, viewportMaxWidth));
  const targetWidth = clamp(SCALE_BAR_TARGET_WIDTH_PX, SCALE_BAR_MIN_WIDTH_PX, maxWidth);
  const kpc = scaleBarLengthKpc(scale, targetWidth, maxWidth);
  const label = formatScaleBarLabel(kpc);

  elements.scaleBar.style.setProperty("--scale-bar-width", `${Math.max(1, kpc * scale).toFixed(1)}px`);
  elements.scaleBarValue.textContent = label;
  elements.scaleBar.setAttribute("aria-label", `${label} scale bar`);
}

function formatNumberCompact(value, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "n/a";
  }
  return Number(value).toLocaleString(undefined, {
    maximumFractionDigits: digits,
  });
}

function formatPeriodDays(row) {
  const period = row[IDX.period];
  if (DATASET_KEYS[row[IDX.dataset]] === "miras") {
    const periodDigits = period >= 1000 ? 0 : 1;
    return `${formatNumberCompact(period, periodDigits)} d`;
  }
  return `${formatNumber(period, 4)} d`;
}

function formatPulsationDuration(seconds) {
  if (!Number.isFinite(seconds) || seconds <= 0) return "n/a";
  if (seconds >= 10) return `${formatNumberCompact(seconds, 0)} s`;
  if (seconds >= 1) return `${formatNumber(seconds, 1)} s`;
  if (seconds >= 0.1) return `${formatNumberCompact(seconds, 2)} s`;
  if (seconds >= 0.001) return `${formatNumberCompact(seconds * 1000, 1)} ms`;
  return `${formatNumberCompact(seconds * 1000000, 1)} us`;
}

function formatSignedGridDegrees(value) {
  const rounded = Math.round(value);
  return `${rounded > 0 ? "+" : ""}${rounded}°`;
}

function formatRaGridLabel(value) {
  const hours = Math.round(value / 15) % 24;
  return `RA ${String(hours).padStart(2, "0")}h`;
}

function formatInteger(value) {
  return Number(value).toLocaleString();
}

function nextFrame() {
  return new Promise((resolve) => {
    requestAnimationFrame(resolve);
  });
}

function setLoadingProgress(progress) {
  if (!elements.loading) return;
  loadingProgress = Math.max(loadingProgress, clamp(progress, 0, 1));
  const progressPercent = Math.round(loadingProgress * 100);
  elements.loading.classList.remove("indeterminate");
  elements.loading.style.setProperty("--loading-progress", loadingProgress.toFixed(4));
  elements.loading.setAttribute("aria-valuenow", `${progressPercent}`);
}

function setIndeterminateLoadingProgress() {
  if (!elements.loading) return;
  elements.loading.classList.add("indeterminate");
  elements.loading.removeAttribute("aria-valuenow");
}

function progressTrackedStream(stream, contentLength, progressMax) {
  if (!Number.isFinite(contentLength) || contentLength <= 0 || typeof TransformStream === "undefined") {
    setIndeterminateLoadingProgress();
    return stream;
  }

  let receivedLength = 0;
  return stream.pipeThrough(
    new TransformStream({
      transform(chunk, controller) {
        receivedLength += chunk.byteLength;
        setLoadingProgress((receivedLength / contentLength) * progressMax);
        controller.enqueue(chunk);
      },
    }),
  );
}

async function responseTextWithProgress(response) {
  if (!response.body) {
    setIndeterminateLoadingProgress();
    return response.text();
  }

  const contentEncoding = response.headers.get("content-encoding")?.toLowerCase() ?? "";
  const decodedContentLength = Number(response.headers.get("x-uncompressed-content-length"));
  const encodedContentLength = Number(response.headers.get("content-length"));
  const contentLength = Number.isFinite(decodedContentLength) && decodedContentLength > 0
    ? decodedContentLength
    : contentEncoding
      ? NaN
      : encodedContentLength;
  let stream = progressTrackedStream(response.body, contentLength, DATA_DOWNLOAD_PROGRESS_MAX);

  return new Response(stream).text();
}

async function fetchAtlasPayload() {
  const response = await fetch(DATA_URL);
  if (!response.ok) throw new Error(`Data request failed with ${response.status}`);

  const jsonText = await responseTextWithProgress(response);
  setLoadingProgress(0.9);
  await nextFrame();
  const payload = JSON.parse(jsonText);
  setLoadingProgress(0.92);
  return payload;
}

function updatePerfHud({ catalogMs, redClumpMs, animatedCatalog, staticCatalog }) {
  if (!PERF_HUD_ENABLED || !elements.perfHud) return;

  if (Number.isFinite(catalogMs)) {
    perfState.catalogMs = perfState.catalogMs
      ? perfState.catalogMs * 0.88 + catalogMs * 0.12
      : catalogMs;
  }
  if (Number.isFinite(redClumpMs)) {
    perfState.redClumpMs = perfState.redClumpMs
      ? perfState.redClumpMs * 0.88 + redClumpMs * 0.12
      : redClumpMs;
  }
  if (Number.isFinite(animatedCatalog)) perfState.animatedCatalog = animatedCatalog;
  if (Number.isFinite(staticCatalog)) perfState.staticCatalog = staticCatalog;

  const now = performance.now();
  if (now - perfState.lastHudMs < 250) return;
  perfState.lastHudMs = now;

  const totalCatalog = perfState.animatedCatalog + perfState.staticCatalog;
  const animatedPercent = totalCatalog > 0 ? (perfState.animatedCatalog / totalCatalog) * 100 : 0;
  elements.perfHud.classList.remove("hidden");
  elements.perfHud.replaceChildren(
    `project ${perfState.projectionMs.toFixed(2)} ms`,
    document.createElement("br"),
    `red clump ${perfState.redClumpMs.toFixed(2)} ms`,
    document.createElement("br"),
    `catalog ${perfState.catalogMs.toFixed(2)} ms`,
    document.createElement("br"),
    `renderer ${scene.catalogRenderer && scene.catalogStaticRenderer ? "gpu" : "canvas"}`,
    document.createElement("br"),
    `pulse mode ${catalogPulseModeLabel(now)}`,
    document.createElement("br"),
    `pulse ${formatInteger(perfState.animatedCatalog)} / ${formatInteger(totalCatalog)} (${animatedPercent.toFixed(1)}%)`,
    document.createElement("br"),
    `static ${formatInteger(perfState.staticCatalog)}`,
  );
}

function formatMultiplierValue(value, digits) {
  return digits === 0 ? formatInteger(Math.round(value)) : formatNumber(value, digits);
}

function parseMultiplierInput(value) {
  const normalized = value.trim().replace(/,/g, "").replace(/\s*(x|°|deg|degrees)$/i, "");
  if (!normalized) return null;
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : null;
}

function resolveEditableBound(bound) {
  const value = typeof bound === "function" ? bound() : bound;
  return Number.isFinite(value) ? value : null;
}

function clampEditableMultiplierValue(value, config) {
  const min = resolveEditableBound(config.min);
  const max = resolveEditableBound(config.max);
  let nextValue = value;
  if (min !== null) nextValue = Math.max(min, nextValue);
  if (max !== null) nextValue = Math.min(max, nextValue);
  return nextValue;
}

function syncEditableMultiplierOutput(key, value) {
  const output = outputs[key];
  const config = editableMultiplierConfigs[key];
  if (!output || !config || output.dataset.editing === "true") return;

  let button = output.querySelector(".editableMultiplierValue");
  let unit = output.querySelector(".editableMultiplierUnit");

  if (!button) {
    button = document.createElement("button");
    button.type = "button";
    button.className = "editableMultiplierValue";
  }

  if (button.dataset.editBound !== "true") {
    button.addEventListener("click", () => beginEditableMultiplierEdit(key));
    button.dataset.editBound = "true";
  }

  if (!unit) {
    unit = document.createElement("span");
    unit.className = "editableMultiplierUnit";
  }

  button.textContent = formatMultiplierValue(value, config.digits);
  button.setAttribute("aria-label", `Edit ${config.label} value`);
  button.title = `Edit ${config.label} value`;
  unit.textContent = config.unit ?? "x";
  if (output.firstElementChild !== button || output.lastElementChild !== unit || output.children.length !== 2) {
    output.replaceChildren(button, unit);
  }
}

function finishEditableMultiplierEdit(key, input, shouldCommit) {
  const output = outputs[key];
  const config = editableMultiplierConfigs[key];
  if (!output || !config) return;

  output.dataset.editing = "false";
  delete output.dataset.editing;

  if (shouldCommit) {
    const parsed = parseMultiplierInput(input.value);
    if (parsed !== null) {
      config.set(clampEditableMultiplierValue(parsed, config));
    }
  }

  syncRangeOutputs();
}

function beginEditableMultiplierEdit(key) {
  const output = outputs[key];
  const config = editableMultiplierConfigs[key];
  if (!output || !config || output.dataset.editing === "true") return;

  output.dataset.editing = "true";
  const input = document.createElement("input");
  const unit = document.createElement("span");
  let finished = false;

  input.type = "text";
  input.className = "editableMultiplierInput";
  input.inputMode = config.inputMode;
  input.value = formatMultiplierValue(config.get(), config.digits);
  input.setAttribute("aria-label", `Edit ${config.label} value`);

  unit.className = "editableMultiplierUnit";
  unit.textContent = config.unit ?? "x";

  const finish = (shouldCommit) => {
    if (finished) return;
    finished = true;
    finishEditableMultiplierEdit(key, input, shouldCommit);
  };

  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      finish(true);
    } else if (event.key === "Escape") {
      event.preventDefault();
      finish(false);
    }
  });
  input.addEventListener("blur", () => finish(true));
  input.addEventListener("click", (event) => event.stopPropagation());

  output.replaceChildren(input, unit);
  window.requestAnimationFrame(() => {
    input.focus();
    input.select();
  });
}

function activeCoordinateFrame() {
  return COORDINATE_FRAME_BY_ID.get(state.coordinateFrame) || COORDINATE_FRAMES[0];
}

function activeCoordinateCenter() {
  return (
    COORDINATE_CENTER_BY_ID.get(state.coordinateCenter) ||
    COORDINATE_CENTER_BY_ID.get("bridge") ||
    COORDINATE_CENTERS[0]
  );
}

function activeCoordinateReference() {
  if (state.cameraLocked && state.locked?.kind === "catalog") {
    return {
      label: "Target",
      context: centerContext(state.locked.coordinates.galacticVector),
    };
  }

  if (state.customCoordinateContext) {
    return {
      label: "View",
      context: state.customCoordinateContext,
    };
  }

  const center = activeCoordinateCenter();
  return {
    label: center.label,
    context: scene.coordinateContext?.centers[center.id] || scene.coordinateContext?.centers.bridge,
  };
}

function formatCoordinateTriplet(coordinates) {
  return `${formatNumber(coordinates[0], 1)}, ${formatNumber(coordinates[1], 1)}, ${formatNumber(coordinates[2], 1)} kpc`;
}

function distanceForPoint(point) {
  if (!point) {
    const reference = activeCoordinateReference().context;
    return reference ? reference.galacticCenter.distance : 0;
  }
  return point.coordinates.distance;
}

function displayCoordinatesForPoint(point) {
  if (!point) return [0, 0, distanceForPoint(null)];
  const coordinates = coordinatesForPoint(point);
  return [coordinates[0], coordinates[1], distanceForPoint(point)];
}

function readoutSampleForVector(localCoordinates, galacticVector) {
  const galactic = lonLatFromVector(galacticVector);
  const equatorial = equatorialFromGalacticVector(galacticVector);
  return {
    local: localCoordinates,
    sky: {
      ra: equatorial.ra,
      dec: equatorial.dec,
      lon: galactic.lon,
      lat: galactic.lat,
    },
  };
}

function readoutSampleForPoint(point) {
  if (!point) {
    const reference = activeCoordinateReference().context;
    const distance = reference ? reference.galacticCenter.distance : 0;
    return readoutSampleForVector([0, 0, null], reference?.galacticVector || [0, 0, distance]);
  }

  const coordinates = coordinatesForPoint(point);
  return readoutSampleForVector(
    [coordinates[0], coordinates[1], distanceForPoint(point)],
    point.coordinates.galacticVector,
  );
}

function localVectorFromPlaneCoordinates(x, y, reference) {
  const origin = reference.galacticVector;
  const basis = reference.basis;
  return [
    origin[0] + x * basis.east[0] + y * basis.north[0],
    origin[1] + x * basis.east[1] + y * basis.north[1],
    origin[2] + x * basis.east[2] + y * basis.north[2],
  ];
}

function cursorCoordinatesForClient(clientX, clientY) {
  const reference = activeCoordinateReference().context;
  if (!reference) return null;
  const coordinates = localPlaneCoordinatesFromScreen(clientX, clientY);
  const vector = localVectorFromPlaneCoordinates(coordinates[0], coordinates[1], reference);
  return readoutSampleForVector([coordinates[0], coordinates[1], null], vector);
}

function coordinateReadoutSample() {
  const activeTarget = state.locked || state.hovered;
  if (activeTarget) return readoutSampleForPoint(activeTarget);

  if (state.cursorClientX !== null && state.cursorClientY !== null) {
    const cursorCoordinates = cursorCoordinatesForClient(state.cursorClientX, state.cursorClientY);
    if (cursorCoordinates) return cursorCoordinates;
  }
  return readoutSampleForPoint(null);
}

function meanVector(vectors, fallback) {
  if (!vectors.length) return fallback;
  const total = vectors.reduce((sum, vector) => [sum[0] + vector[0], sum[1] + vector[1], sum[2] + vector[2]], [0, 0, 0]);
  return total.map((component) => component / vectors.length);
}

function centerContext(vector) {
  return {
    galacticVector: vector,
    galacticCenter: lonLatFromVector(vector),
    basis: makeEquatorialBasis(vector),
  };
}

function coordinateContextFromPayload(payload) {
  const metaCenters = payload.meta?.coordinateCenters || {};
  const sampleGalactic = metaCenters.sampleGalacticVectorKpc || [0, 0, payload.meta?.originDistanceKpc || 0];
  const regionVectors = new Map(COORDINATE_CENTERS.map((center) => [center.id, []]));

  for (const row of payload.datasets.catalog) {
    const center = COORDINATE_CENTERS.find((item) => item.locationIndex === row[IDX.location]);
    if (!center) continue;
    regionVectors.get(center.id).push(vectorFromLonLat(row[IDX.galLonDeg], row[IDX.galLatDeg], row[IDX.distance]));
  }

  const lmcGalactic = metaCenters.lmcGalacticVectorKpc || meanVector(regionVectors.get("lmc"), sampleGalactic);
  const smcGalactic = metaCenters.smcGalacticVectorKpc || meanVector(regionVectors.get("smc"), sampleGalactic);
  const bridgeDirection = meanVector(regionVectors.get("bridge"), meanVector([lmcGalactic, smcGalactic], sampleGalactic));
  const bridgeDistance = (vectorLength(lmcGalactic) + vectorLength(smcGalactic)) / 2;
  const bridgeLength = vectorLength(bridgeDirection);
  const bridgeGalactic =
    bridgeLength > 0
      ? bridgeDirection.map((component) => (component / bridgeLength) * bridgeDistance)
      : meanVector([lmcGalactic, smcGalactic], sampleGalactic);

  return {
    centers: {
      bridge: centerContext(bridgeGalactic),
      lmc: centerContext(lmcGalactic),
      smc: centerContext(smcGalactic),
    },
  };
}

function catalogCoordinates(row) {
  const distance = row[IDX.distance];
  const galacticVector = vectorFromLonLat(row[IDX.galLonDeg], row[IDX.galLatDeg], distance);
  return {
    galacticVector,
    distance,
    lonDeg: row[IDX.galLonDeg],
    latDeg: row[IDX.galLatDeg],
  };
}

function redClumpCoordinates(row) {
  const distance = row[RC.distance];
  const galacticVector = vectorFromLonLat(row[RC.lon], row[RC.lat], distance);
  return {
    galacticVector,
    distance,
    lonDeg: row[RC.lon],
    latDeg: row[RC.lat],
  };
}

function clusterCoordinates(row) {
  const distance = row[CL.distance];
  const galacticVector = vectorFromLonLat(row[CL.galLonDeg], row[CL.galLatDeg], distance);
  return {
    galacticVector,
    distance,
    lonDeg: row[CL.galLonDeg],
    latDeg: row[CL.galLatDeg],
  };
}

function clusterStarCoordinates(row) {
  const distance = row[CS.distance];
  const galacticVector = vectorFromLonLat(row[CS.galLonDeg], row[CS.galLatDeg], distance);
  return {
    galacticVector,
    distance,
    lonDeg: row[CS.galLonDeg],
    latDeg: row[CS.galLatDeg],
  };
}

function coordinatesFromGalacticVector(galacticVector) {
  const center = lonLatFromVector(galacticVector);
  return {
    galacticVector,
    distance: center.distance,
    lonDeg: center.lon,
    latDeg: center.lat,
  };
}

function catalogCoordinatesForDistance(row, distance) {
  const galacticVector = vectorFromLonLat(row[IDX.galLonDeg], row[IDX.galLatDeg], distance);
  return {
    galacticVector,
    distance,
    lonDeg: row[IDX.galLonDeg],
    latDeg: row[IDX.galLatDeg],
  };
}

function clusterCoordinatesForDistance(row, distance) {
  const galacticVector = vectorFromLonLat(row[CL.galLonDeg], row[CL.galLatDeg], distance);
  return {
    galacticVector,
    distance,
    lonDeg: row[CL.galLonDeg],
    latDeg: row[CL.galLatDeg],
  };
}

function kpcToDistanceModulus(distanceKpc) {
  return 5 * Math.log10(distanceKpc) + 10;
}

function distanceModulusToKpc(distanceModulus) {
  return 10 ** ((distanceModulus - 10) / 5);
}

function distanceErrorToModulusError(distanceKpc, distanceErrorKpc) {
  if (!Number.isFinite(distanceKpc) || !Number.isFinite(distanceErrorKpc) || distanceKpc <= 0 || distanceErrorKpc <= 0) {
    return null;
  }
  return (5 * distanceErrorKpc) / (Math.log(10) * distanceKpc);
}

function truncatedSeededStandardNormal(seed, key) {
  let fallback = 0;
  for (let attempt = 0; attempt < 12; attempt += 1) {
    const u1 = Math.max(Number.EPSILON, seededUnit32(`${seed}:${key}:${attempt}:a`));
    const u2 = seededUnit32(`${seed}:${key}:${attempt}:b`);
    const normal = Math.sqrt(-2 * Math.log(u1)) * Math.cos(Math.PI * 2 * u2);
    if (Number.isFinite(normal)) {
      fallback = normal;
      if (Math.abs(normal) <= UNCERTAINTY_TRUNCATION_SIGMA) return normal;
    }
  }
  return clamp(fallback, -UNCERTAINTY_TRUNCATION_SIGMA, UNCERTAINTY_TRUNCATION_SIGMA);
}

function sampledDistanceFromModulusError(distanceKpc, modulusError, seed, key) {
  if (
    seed === DEFAULT_UNCERTAINTY_SEED ||
    !Number.isFinite(distanceKpc) ||
    !Number.isFinite(modulusError) ||
    distanceKpc <= 0 ||
    modulusError <= 0
  ) {
    return distanceKpc;
  }
  const sampledModulus = kpcToDistanceModulus(distanceKpc) + truncatedSeededStandardNormal(seed, key) * modulusError;
  const sampledDistance = distanceModulusToKpc(sampledModulus);
  return Number.isFinite(sampledDistance) && sampledDistance > 0 ? sampledDistance : distanceKpc;
}

function sampledDistanceFromKpcError(distanceKpc, distanceErrorKpc, seed, key) {
  return sampledDistanceFromModulusError(
    distanceKpc,
    distanceErrorToModulusError(distanceKpc, distanceErrorKpc),
    seed,
    key,
  );
}

function luminosityFromIMagnitude(iMagnitude, distanceKpc) {
  if (!Number.isFinite(iMagnitude) || !Number.isFinite(distanceKpc) || distanceKpc <= 0) return null;
  const absoluteI = iMagnitude - kpcToDistanceModulus(distanceKpc);
  const luminosity = 10 ** (-0.4 * (absoluteI - SUN_ABSOLUTE_I_MAG));
  return Number.isFinite(luminosity) && luminosity > 0 ? luminosity : null;
}

function stellarRadiusFromLuminosityAndColor(row, luminosity, vMinusI) {
  if (!Number.isFinite(luminosity) || luminosity <= 0 || !Number.isFinite(vMinusI)) return null;
  const logLuminosity = Math.log10(luminosity);
  const temperature = effectiveTemperatureForCatalogState(row, vMinusI, logLuminosity);
  if (!Number.isFinite(temperature) || temperature <= 0) return null;
  return Math.sqrt(luminosity) * (SUN_EFFECTIVE_TEMPERATURE / temperature) ** 2;
}

function longitudeBoundsForValues(values, padding = SKY_GRID_BOUNDS_PADDING_DEGREES) {
  const longitudes = values.filter(Number.isFinite).map(normalizeDegrees360).sort((a, b) => a - b);
  if (longitudes.length === 0) return { start: 0, span: 0 };
  if (longitudes.length === 1) {
    return {
      start: normalizeDegrees360(longitudes[0] - padding),
      span: Math.min(360, padding * 2),
    };
  }

  let largestGap = -Infinity;
  let largestGapIndex = 0;
  for (let index = 0; index < longitudes.length; index += 1) {
    const current = longitudes[index];
    const next = index === longitudes.length - 1 ? longitudes[0] + 360 : longitudes[index + 1];
    const gap = next - current;
    if (gap > largestGap) {
      largestGap = gap;
      largestGapIndex = index;
    }
  }

  const rawStart = longitudes[(largestGapIndex + 1) % longitudes.length];
  const rawSpan = 360 - largestGap;
  const paddedSpan = rawSpan + padding * 2;
  if (paddedSpan >= 360) return { start: 0, span: 360 };
  return {
    start: normalizeDegrees360(rawStart - padding),
    span: paddedSpan,
  };
}

function latitudeBoundsForValues(values, padding = SKY_GRID_BOUNDS_PADDING_DEGREES) {
  const latitudes = values.filter(Number.isFinite);
  if (latitudes.length === 0) return { min: -5, max: 5 };
  return {
    min: clamp(Math.min(...latitudes) - padding, -90, 90),
    max: clamp(Math.max(...latitudes) + padding, -90, 90),
  };
}

function skyGridBoundsFromValues(longitudes, latitudes) {
  return {
    longitude: longitudeBoundsForValues(longitudes),
    latitude: latitudeBoundsForValues(latitudes),
  };
}

function skyGridBoundsFromPayload(payload) {
  const equatorialLongitudes = [];
  const equatorialLatitudes = [];
  const galacticLongitudes = [];
  const galacticLatitudes = [];
  const redClumpEquatorialLongitudes = [];
  const redClumpEquatorialLatitudes = [];

  for (const row of payload.datasets.catalog) {
    equatorialLongitudes.push(row[IDX.raDeg]);
    equatorialLatitudes.push(row[IDX.decDeg]);
    galacticLongitudes.push(row[IDX.galLonDeg]);
    galacticLatitudes.push(row[IDX.galLatDeg]);
  }

  for (const row of payload.datasets.clusters || []) {
    equatorialLongitudes.push(row[CL.raDeg]);
    equatorialLatitudes.push(row[CL.decDeg]);
    galacticLongitudes.push(row[CL.galLonDeg]);
    galacticLatitudes.push(row[CL.galLatDeg]);
  }

  for (const row of payload.datasets.redClump) {
    const vector = vectorFromLonLat(row[RC.lon], row[RC.lat], 1);
    const equatorial = equatorialFromGalacticVector(vector);
    redClumpEquatorialLongitudes.push(equatorial.ra);
    redClumpEquatorialLatitudes.push(equatorial.dec);
    galacticLongitudes.push(row[RC.lon]);
    galacticLatitudes.push(row[RC.lat]);
  }

  if (equatorialLongitudes.length === 0) {
    equatorialLongitudes.push(...redClumpEquatorialLongitudes);
    equatorialLatitudes.push(...redClumpEquatorialLatitudes);
  }

  return {
    equatorial: skyGridBoundsFromValues(equatorialLongitudes, equatorialLatitudes),
    galactic: skyGridBoundsFromValues(galacticLongitudes, galacticLatitudes),
  };
}

function activeCoordinateCacheKey(reference = activeCoordinateReference()) {
  const center = reference.context;
  if (!center) return `${state.coordinateFrame}:none`;
  const vector = center.galacticVector || [0, 0, 0];
  return `${state.coordinateFrame}:${vector[0].toFixed(6)},${vector[1].toFixed(6)},${vector[2].toFixed(6)}`;
}

function coordinatesForReference(point, reference) {
  const center = reference.context;
  if (!center) return [0, 0, 0];
  if (state.coordinateFrame === "galactic") {
    return angularCoordinate(point.coordinates.lonDeg, point.coordinates.latDeg, point.coordinates.distance, center.galacticCenter);
  }
  return projectLocalVector(point.coordinates.galacticVector, center.galacticVector, center.basis);
}

function rebuildCoordinateCache(reference = activeCoordinateReference()) {
  const cacheKey = activeCoordinateCacheKey(reference);
  if (scene.coordinateCacheKey === cacheKey) return;

  for (const point of scene.catalog) {
    point.activeCoordinates = coordinatesForReference(point, reference);
  }
  for (const point of scene.clusterStars) {
    point.activeCoordinates = coordinatesForReference(point, reference);
  }
  for (const point of scene.clusters) {
    point.activeCoordinates = coordinatesForReference(point, reference);
  }
  for (const point of scene.redClump) {
    point.activeCoordinates = coordinatesForReference(point, reference);
  }
  scene.coordinateCacheKey = cacheKey;
}

function invalidateCoordinateCache() {
  scene.coordinateCacheKey = null;
  scene.clusterStarGpuDirty = true;
}

function coordinatesForPoint(point) {
  rebuildCoordinateCache();
  return point.activeCoordinates || [0, 0, 0];
}

function hexToRgb(hex) {
  const clean = hex.replace("#", "");
  return [
    parseInt(clean.slice(0, 2), 16),
    parseInt(clean.slice(2, 4), 16),
    parseInt(clean.slice(4, 6), 16),
  ];
}

function cssColorToRgb(color) {
  if (color.startsWith("#")) return hexToRgb(color);
  const match = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/i);
  if (!match) return [255, 255, 255];
  return [Number(match[1]), Number(match[2]), Number(match[3])];
}

function normalizedRgbFromCssColor(color) {
  const cached = catalogRenderColorCache.get(color);
  if (cached) return cached;
  const rgbValue = cssColorToRgb(color).map((value) => value / 255);
  catalogRenderColorCache.set(color, rgbValue);
  return rgbValue;
}

function normalizedRgbForCatalogColor(color) {
  if (color && typeof color !== "string" && color.length >= 3) return color;
  return normalizedRgbFromCssColor(color || "#ffffff");
}

function rgbaFromRgb(values, alpha) {
  return `rgba(${values[0]}, ${values[1]}, ${values[2]}, ${alpha})`;
}

function rgb(values) {
  return `rgb(${values[0]}, ${values[1]}, ${values[2]})`;
}

function mixRgb(left, right, amount) {
  return [
    Math.round(left[0] + (right[0] - left[0]) * amount),
    Math.round(left[1] + (right[1] - left[1]) * amount),
    Math.round(left[2] + (right[2] - left[2]) * amount),
  ];
}

function quantizeRgb(values, step) {
  return values.map((value) => clamp(Math.round(value / step) * step, 0, 255));
}

function smoothStep(value) {
  const t = clamp(value, 0, 1);
  return t * t * (3 - 2 * t);
}

function normalizedTemperatureAnchors(anchors) {
  if (!Array.isArray(anchors)) return V_MINUS_I_TEMPERATURE_ANCHORS;
  const clean = anchors
    .map((anchor) => ({
      vMinusI: Number(anchor?.vMinusI),
      temperature: Number(anchor?.temperature),
    }))
    .filter((anchor) => Number.isFinite(anchor.vMinusI) && Number.isFinite(anchor.temperature) && anchor.temperature > 0)
    .sort((left, right) => left.vMinusI - right.vMinusI);
  return clean.length >= 2 ? clean : V_MINUS_I_TEMPERATURE_ANCHORS;
}

function activeVMinusITemperatureAnchors() {
  return scene.temperatureAnchors?.length >= 2 ? scene.temperatureAnchors : V_MINUS_I_TEMPERATURE_ANCHORS;
}

function effectiveTemperatureFromVMinusI(vMinusI) {
  const anchors = activeVMinusITemperatureAnchors();
  if (vMinusI <= anchors[0].vMinusI) return anchors[0].temperature;

  for (let index = 1; index < anchors.length; index += 1) {
    const left = anchors[index - 1];
    const right = anchors[index];
    if (vMinusI <= right.vMinusI) {
      const amount = (vMinusI - left.vMinusI) / (right.vMinusI - left.vMinusI);
      const logLeft = Math.log(left.temperature);
      const logRight = Math.log(right.temperature);
      return Math.exp(logLeft + (logRight - logLeft) * amount);
    }
  }

  return anchors[anchors.length - 1].temperature;
}

function normalizedMeanMetallicityFeHByLocation(raw) {
  const values = DEFAULT_MEAN_METALLICITY_FEH_BY_LOCATION.slice();
  if (!raw || typeof raw !== "object") return values;
  LOCATION_LABELS.forEach((label, index) => {
    const value = Number(raw[label]);
    if (Number.isFinite(value)) values[index] = value;
  });
  return values;
}

function decodeBase64Uint16(encoded) {
  if (typeof encoded !== "string" || !encoded) return null;
  try {
    const binary = window.atob(encoded);
    if (binary.length % 2 !== 0) return null;
    const values = new Uint16Array(binary.length / 2);
    for (let index = 0, byteIndex = 0; index < values.length; index += 1, byteIndex += 2) {
      values[index] = binary.charCodeAt(byteIndex) | (binary.charCodeAt(byteIndex + 1) << 8);
    }
    return values;
  } catch {
    return null;
  }
}

function normalizedGridAxis(raw) {
  const min = Number(raw?.min);
  const step = Number(raw?.step);
  const count = Math.trunc(Number(raw?.count));
  if (!Number.isFinite(min) || !Number.isFinite(step) || step <= 0 || !Number.isInteger(count) || count < 2) {
    return null;
  }
  return {
    min,
    step,
    count,
    max: min + step * (count - 1),
  };
}

function normalizedTemperatureGrid(raw) {
  if (!raw?.available || raw.valueEncoding !== "uint16-base64-little-endian-log10K") return null;
  const colorAxis = normalizedGridAxis(raw.axes?.vMinusI);
  const logLuminosityAxis = normalizedGridAxis(raw.axes?.logLuminosity);
  const metallicityFeH = Array.isArray(raw.axes?.metallicityFeH)
    ? raw.axes.metallicityFeH.map(Number).filter(Number.isFinite)
    : [];
  const valueScale = Number(raw.valueScale);
  const values = decodeBase64Uint16(raw.values);
  const expectedLength = colorAxis?.count * logLuminosityAxis?.count * metallicityFeH.length;
  if (
    !colorAxis ||
    !logLuminosityAxis ||
    metallicityFeH.length < 2 ||
    !Number.isFinite(valueScale) ||
    valueScale <= 0 ||
    !values ||
    values.length !== expectedLength
  ) {
    return null;
  }
  return {
    colorAxis,
    logLuminosityAxis,
    metallicityFeH,
    valueScale,
    values,
  };
}

function axisBracket(axis, value) {
  const rawIndex = clamp((value - axis.min) / axis.step, 0, axis.count - 1);
  const lower = Math.floor(rawIndex);
  const upper = Math.min(axis.count - 1, lower + 1);
  return {
    lower,
    upper,
    amount: upper === lower ? 0 : rawIndex - lower,
  };
}

function metallicityBracket(values, feh) {
  if (feh <= values[0]) return { lower: 0, upper: 0, amount: 0 };
  const lastIndex = values.length - 1;
  if (feh >= values[lastIndex]) return { lower: lastIndex, upper: lastIndex, amount: 0 };
  for (let index = 1; index < values.length; index += 1) {
    if (feh <= values[index]) {
      const left = values[index - 1];
      const right = values[index];
      return {
        lower: index - 1,
        upper: index,
        amount: (feh - left) / (right - left),
      };
    }
  }
  return { lower: lastIndex, upper: lastIndex, amount: 0 };
}

function temperatureGridValue(grid, fehIndex, colorIndex, lumIndex) {
  const index =
    (fehIndex * grid.colorAxis.count + colorIndex) * grid.logLuminosityAxis.count + lumIndex;
  return grid.values[index] / grid.valueScale;
}

function temperatureFromGrid(vMinusI, logLuminosity, metallicityFeH) {
  const grid = scene.temperatureGrid;
  if (
    !grid ||
    !Number.isFinite(vMinusI) ||
    !Number.isFinite(logLuminosity) ||
    !Number.isFinite(metallicityFeH)
  ) {
    return null;
  }

  const color = axisBracket(grid.colorAxis, vMinusI);
  const luminosity = axisBracket(grid.logLuminosityAxis, logLuminosity);
  const metallicity = metallicityBracket(grid.metallicityFeH, metallicityFeH);
  let weightedLogTemperature = 0;
  let totalWeight = 0;

  for (const [fehIndex, fehWeight] of [
    [metallicity.lower, 1 - metallicity.amount],
    [metallicity.upper, metallicity.amount],
  ]) {
    if (fehWeight <= 0) continue;
    for (const [colorIndex, colorWeight] of [
      [color.lower, 1 - color.amount],
      [color.upper, color.amount],
    ]) {
      if (colorWeight <= 0) continue;
      for (const [lumIndex, lumWeight] of [
        [luminosity.lower, 1 - luminosity.amount],
        [luminosity.upper, luminosity.amount],
      ]) {
        const weight = fehWeight * colorWeight * lumWeight;
        if (weight <= 0) continue;
        weightedLogTemperature += temperatureGridValue(grid, fehIndex, colorIndex, lumIndex) * weight;
        totalWeight += weight;
      }
    }
  }

  if (totalWeight <= 0) return null;
  return 10 ** (weightedLogTemperature / totalWeight);
}

function metallicityForCatalogRow(row) {
  if (Number.isFinite(row?.[IDX.feh])) return row[IDX.feh];
  const location = Math.trunc(Number(row?.[IDX.location]));
  const value = scene.meanMetallicityFeHByLocation?.[location];
  if (Number.isFinite(value)) return value;
  return DEFAULT_MEAN_METALLICITY_FEH_BY_LOCATION[0];
}

function isMiraRow(row) {
  return DATASET_KEYS[row?.[IDX.dataset]] === "miras";
}

function temperatureFromColorLuminosity(row, vMinusI, logLuminosity) {
  const gridTemperature = temperatureFromGrid(vMinusI, logLuminosity, metallicityForCatalogRow(row));
  return Number.isFinite(gridTemperature) ? gridTemperature : effectiveTemperatureFromVMinusI(vMinusI);
}

function miraLiteratureTemperature(row) {
  const temperature = Number(row?.[IDX.miraTeff]);
  return Number.isFinite(temperature) && temperature > 0 ? temperature : null;
}

function miraTemperatureSourceLabel(row) {
  const sourceIndex = Math.trunc(Number(row?.[IDX.miraTeffSourceIndex]));
  if (!Number.isInteger(sourceIndex) || sourceIndex < 0) return null;
  const source = scene.miraTemperatureSources?.[sourceIndex];
  return source?.label || source?.id || null;
}

function miraTemperatureAbsoluteBounds(row) {
  const mode = String(row?.[IDX.mode] || "").toLowerCase();
  if (mode.startsWith("c") || mode.includes("c-rich")) return MIRA_TEMPERATURE_BOUNDS.carbon;
  if (mode.startsWith("o") || mode.includes("o-rich")) return MIRA_TEMPERATURE_BOUNDS.oxygen;
  return MIRA_TEMPERATURE_BOUNDS.fallback;
}

function miraMeanTemperature(row) {
  const bounds = miraTemperatureAbsoluteBounds(row);
  const literatureTemperature = miraLiteratureTemperature(row);
  if (Number.isFinite(literatureTemperature)) {
    return clamp(literatureTemperature, bounds.min, bounds.max);
  }
  const meanVMinusI = intrinsicVMinusIForRow(row);
  const colorTemperature = temperatureFromColorLuminosity(row, meanVMinusI, row?.[IDX.logLum]);
  if (Number.isFinite(colorTemperature)) {
    return clamp(colorTemperature, bounds.min, bounds.max);
  }
  return (bounds.min + bounds.max) * 0.5;
}

function miraTemperatureBoundsForRow(row) {
  const bounds = miraTemperatureAbsoluteBounds(row);
  const meanTemperature = miraMeanTemperature(row);
  return {
    min: Math.max(bounds.min, meanTemperature - MIRA_TEMPERATURE_HALF_SPAN_K),
    max: Math.min(bounds.max, meanTemperature + MIRA_TEMPERATURE_HALF_SPAN_K),
    mean: meanTemperature,
  };
}

function miraTemperatureForCatalogState(row, vMinusI, logLuminosity) {
  const bounds = miraTemperatureBoundsForRow(row);
  const colorTemperature = temperatureFromColorLuminosity(row, vMinusI, logLuminosity);
  const temperature = Number.isFinite(colorTemperature) ? colorTemperature : bounds.mean;
  return clamp(temperature, bounds.min, bounds.max);
}

function effectiveTemperatureForCatalogState(row, vMinusI, logLuminosity) {
  if (isMiraRow(row)) return miraTemperatureForCatalogState(row, vMinusI, logLuminosity);
  return temperatureFromColorLuminosity(row, vMinusI, logLuminosity);
}

function quantizedGridAxisValue(axis, value) {
  const index = clamp(Math.round((value - axis.min) / axis.step), 0, axis.count - 1);
  return {
    key: index,
    value: axis.min + index * axis.step,
  };
}

function rgbForTemperature(temperature) {
  const stops = BLACKBODY_COLOR_STOPS;
  if (temperature <= stops[0][0]) return hexToRgb(stops[0][1]);

  for (let index = 1; index < stops.length; index += 1) {
    const [rightTemperature, rightColor] = stops[index];
    if (temperature <= rightTemperature) {
      const [leftTemperature, leftColor] = stops[index - 1];
      const amount = (temperature - leftTemperature) / (rightTemperature - leftTemperature);
      return mixRgb(hexToRgb(leftColor), hexToRgb(rightColor), amount);
    }
  }

  return hexToRgb(stops[stops.length - 1][1]);
}

function displayTemperatureFromPhysicalTemperature(temperature) {
  const minTemperature = BLACKBODY_COLOR_STOPS[0][0];
  const maxTemperature = BLACKBODY_COLOR_STOPS[BLACKBODY_COLOR_STOPS.length - 1][0];
  const boundedTemperature = clamp(temperature, minTemperature, maxTemperature);
  const logRatio = Math.log(boundedTemperature / BLACKBODY_DISPLAY_WHITEPOINT_TEMPERATURE);
  const colorContrast = clampColorContrast(state?.colorContrast ?? COLOR_CONTRAST_DEFAULT);

  return clamp(
    BLACKBODY_DISPLAY_WHITEPOINT_TEMPERATURE * Math.exp(logRatio * colorContrast),
    minTemperature,
    maxTemperature,
  );
}

function displayRgbFromBlackbodyRgb(values) {
  return values.map((value, index) =>
    clamp(
      Math.round(
        BLACKBODY_DISPLAY_WHITEPOINT_RGB[index] +
          (value - BLACKBODY_DISPLAY_WHITEPOINT_RGB[index]) * BLACKBODY_DISPLAY_CHROMA_BOOST,
      ),
      0,
      255,
    ),
  );
}

function colorForTemperature(temperature) {
  return rgb(displayRgbFromBlackbodyRgb(rgbForTemperature(displayTemperatureFromPhysicalTemperature(temperature))));
}

function colorForVMinusI(vMinusI, spectralIndex) {
  if (!Number.isFinite(vMinusI)) {
    return scene.spectralClasses[spectralIndex]?.color || "#dfeaff";
  }

  const anchors = activeVMinusITemperatureAnchors();
  const cacheKey = clamp(
    Math.round(vMinusI * COLOR_CACHE_PRECISION),
    Math.round(anchors[0].vMinusI * COLOR_CACHE_PRECISION),
    Math.round(anchors[anchors.length - 1].vMinusI * COLOR_CACHE_PRECISION),
  );
  const cached = colorCache.get(cacheKey);
  if (cached) return cached;

  const cachedVMinusI = cacheKey / COLOR_CACHE_PRECISION;
  const color = colorForTemperature(effectiveTemperatureFromVMinusI(cachedVMinusI));
  colorCache.set(cacheKey, color);
  return color;
}

function colorForCatalogState(row, vMinusI, logLuminosity) {
  if (!Number.isFinite(vMinusI)) {
    return scene.spectralClasses[row?.[IDX.spectral]]?.color || "#dfeaff";
  }
  if (isMiraRow(row)) {
    return colorForTemperature(effectiveTemperatureForCatalogState(row, vMinusI, logLuminosity));
  }
  const grid = scene.temperatureGrid;
  if (!grid || !Number.isFinite(logLuminosity)) {
    return colorForVMinusI(vMinusI, row?.[IDX.spectral]);
  }

  const colorSample = quantizedGridAxisValue(grid.colorAxis, vMinusI);
  const luminositySample = quantizedGridAxisValue(grid.logLuminosityAxis, logLuminosity);
  const metallicityKey = Math.round(metallicityForCatalogRow(row) * TEMPERATURE_GRID_METALLICITY_CACHE_PRECISION);
  const metallicitySample = metallicityKey / TEMPERATURE_GRID_METALLICITY_CACHE_PRECISION;
  const cacheKey = `${colorSample.key}/${luminositySample.key}/${metallicityKey}`;
  const cached = catalogTemperatureColorCache.get(cacheKey);
  if (cached) return cached;

  const temperature =
    temperatureFromGrid(colorSample.value, luminositySample.value, metallicitySample) ||
    effectiveTemperatureFromVMinusI(colorSample.value);
  const color = colorForTemperature(temperature);
  if (catalogTemperatureColorCache.size > CATALOG_TEMPERATURE_COLOR_CACHE_MAX) {
    catalogTemperatureColorCache.clear();
  }
  catalogTemperatureColorCache.set(cacheKey, color);
  return color;
}

function reddeningEVIForRow(row) {
  return Number.isFinite(row[IDX.reddeningEVI]) ? row[IDX.reddeningEVI] : 0;
}

function intrinsicVMinusIForRow(row) {
  if (Number.isFinite(row[IDX.vMinusI0])) {
    return row[IDX.vMinusI0];
  }
  if (!Number.isFinite(row[IDX.vMinusI])) {
    return null;
  }
  return row[IDX.vMinusI] - reddeningEVIForRow(row);
}

function recolorCatalogLightCurve(lightCurve, row, baseVMinusI, baseLogLuminosity) {
  if (!lightCurve || !Number.isFinite(baseVMinusI)) return;
  if (lightCurve.colors && lightCurve.colorOffsets && lightCurve.logLuminosities) {
    for (let index = 0; index < lightCurve.colors.length; index += 1) {
      lightCurve.colors[index] = colorForCatalogState(
        row,
        baseVMinusI + lightCurve.colorOffsets[index],
        lightCurve.logLuminosities[index],
      );
    }
  }
  const meanColorOffset = Number.isFinite(lightCurve.meanColorOffset) ? lightCurve.meanColorOffset : 0;
  const meanLogLuminosity = Number.isFinite(baseLogLuminosity) ? baseLogLuminosity : row?.[IDX.logLum];
  lightCurve.meanColor = colorForCatalogState(row, baseVMinusI + meanColorOffset, meanLogLuminosity);
}

function updateLightCurveLuminosityColors(point) {
  const lightCurve = point.lightCurve;
  if (!lightCurve || !Number.isFinite(point.currentLogLum)) return;

  const previousBase = Number.isFinite(lightCurve.currentBaseLogLuminosity)
    ? lightCurve.currentBaseLogLuminosity
    : point.row[IDX.logLum];
  const shift = point.currentLogLum - previousBase;
  if (Number.isFinite(shift) && Math.abs(shift) > 1e-10 && lightCurve.logLuminosities) {
    for (let index = 0; index < lightCurve.logLuminosities.length; index += 1) {
      lightCurve.logLuminosities[index] += shift;
    }
  }
  lightCurve.currentBaseLogLuminosity = point.currentLogLum;

  recolorCatalogLightCurve(lightCurve, point.row, point.vMinusI0, point.currentLogLum);
}

function updateCatalogPointForDistance(point, distance) {
  const row = point.row;
  const catalogDistance = row[IDX.distance];
  const hasSampledDistance =
    state.uncertaintySeed !== DEFAULT_UNCERTAINTY_SEED &&
    Number.isFinite(distance) &&
    Number.isFinite(catalogDistance) &&
    Math.abs(distance - catalogDistance) > 1e-8;

  point.coordinates = hasSampledDistance ? catalogCoordinatesForDistance(row, distance) : point.baseCoordinates;
  point.currentDistance = point.coordinates.distance;

  let luminosity = row[IDX.lum];
  if (hasSampledDistance) {
    luminosity = luminosityFromIMagnitude(row[IDX.iMag], distance) || row[IDX.lum];
  }
  const logLuminosity = Number.isFinite(luminosity) && luminosity > 0 ? Math.log10(luminosity) : row[IDX.logLum];
  const radius =
    hasSampledDistance
      ? stellarRadiusFromLuminosityAndColor(row, luminosity, point.vMinusI0) || row[IDX.radius]
      : row[IDX.radius];

  point.currentLum = luminosity;
  point.currentLogLum = logLuminosity;
  point.currentRadius = radius;
  point.radiusUnit = pointRadiusUnitFromStellarRadius(radius);
  point.alphaBaseUnit = pointAlphaUnitBaseFromLuminosity(luminosity) * BASE_LUMINOSITY_FACTOR;
  point.color = colorForCatalogState(row, point.vMinusI0, logLuminosity);
  updateLightCurveLuminosityColors(point);
}

function updateClusterPointForDistance(point, distance) {
  const row = point.row;
  const catalogDistance = row[CL.distance];
  const hasSampledDistance =
    state.uncertaintySeed !== DEFAULT_UNCERTAINTY_SEED &&
    Number.isFinite(distance) &&
    Number.isFinite(catalogDistance) &&
    Math.abs(distance - catalogDistance) > 1e-8;
  point.coordinates = hasSampledDistance ? clusterCoordinatesForDistance(row, distance) : point.baseCoordinates;
  point.currentDistance = point.coordinates.distance;
}

function refreshTemperatureDrivenColors() {
  colorCache.clear();
  catalogTemperatureColorCache.clear();

  for (const point of scene.catalog) {
    if (!point?.row) continue;
    const logLuminosity = currentCatalogLogLuminosity(point);
    point.color = colorForCatalogState(point.row, point.vMinusI0, logLuminosity);
    updateLightCurveLuminosityColors(point);
    if (point.drawItem) point.drawItem.currentColor = null;
  }

  const clusterRenderedLuminosity = new Array(scene.clusters.length).fill(0);
  const clusterRenderedColorSums = scene.clusters.map(() => [0, 0, 0]);
  for (const point of scene.clusterStars) {
    const row = point.row;
    point.color = Number.isFinite(row?.[CS.temperature])
      ? colorForTemperature(row[CS.temperature])
      : colorForVMinusI(row?.[CS.vMinusI0], row?.[CS.spectral]);
    const syntheticRow = point.lightCurve?.syntheticRow;
    if (syntheticRow) {
      recolorCatalogLightCurve(point.lightCurve, syntheticRow, syntheticRow[IDX.vMinusI0], syntheticRow[IDX.logLum]);
    }
    if (point.drawItem) point.drawItem.currentColor = null;

    const clusterIndex = point.clusterIndex;
    const starLuminosity = Number.isFinite(row?.[CS.lum]) ? Math.max(0, row[CS.lum]) : 0;
    const renderedColorSums = clusterRenderedColorSums[clusterIndex];
    if (starLuminosity > 0 && renderedColorSums) {
      const rgbValue = cssColorToRgb(point.color);
      clusterRenderedLuminosity[clusterIndex] += starLuminosity;
      renderedColorSums[0] += rgbValue[0] * starLuminosity;
      renderedColorSums[1] += rgbValue[1] * starLuminosity;
      renderedColorSums[2] += rgbValue[2] * starLuminosity;
    }
  }

  for (const cluster of scene.clusters) {
    const renderedLuminosity = clusterRenderedLuminosity[cluster.index] || 0;
    const renderedColorSums = clusterRenderedColorSums[cluster.index];
    cluster.renderedStarGlowRgb =
      renderedLuminosity > 0 && renderedColorSums
        ? renderedColorSums.map((value) => Math.round(value / renderedLuminosity))
        : cssColorToRgb(colorForVMinusI(cluster.row?.[CL.unresolvedVMinusI0], 4));
    for (const bin of cluster.hrBins || []) {
      bin.color = Number.isFinite(bin.temperature)
        ? colorForTemperature(bin.temperature)
        : colorForVMinusI(bin.vMinusI0, 5);
    }
  }

  markCatalogStaticDirty();
  markClusterStarGpuDirty();
  setTarget(state.locked || state.hovered);
  queueRender();
}

function setColorContrast(value) {
  const next = clampColorContrast(value);
  if (Math.abs(state.colorContrast - next) < 1e-6) return;
  state.colorContrast = next;
  refreshTemperatureDrivenColors();
}

function applyUncertaintyRealization({ updateTarget = true } = {}) {
  const seed = clampUncertaintySeed(state.uncertaintySeed);
  state.uncertaintySeed = seed;

  for (const point of scene.catalog) {
    const sampledDistance = sampledDistanceFromKpcError(
      point.row[IDX.distance],
      point.row[IDX.distanceError],
      seed,
      `catalog:${point.row[IDX.id]}`,
    );
    updateCatalogPointForDistance(point, sampledDistance);
  }

  for (const point of scene.clusters) {
    const sampledDistance = sampledDistanceFromModulusError(
      point.row[CL.distance],
      point.row[CL.eMu0],
      seed,
      `cluster:${point.row[CL.name]}:${point.index}`,
    );
    updateClusterPointForDistance(point, sampledDistance);
  }

  for (const point of scene.clusterStars) {
    const cluster = scene.clusters[point.clusterIndex];
    if (seed === DEFAULT_UNCERTAINTY_SEED || !cluster || cluster.coordinates === cluster.baseCoordinates) {
      point.coordinates = point.baseCoordinates;
    } else {
      point.coordinates = coordinatesFromGalacticVector([
        cluster.coordinates.galacticVector[0] + point.clusterOffsetVector[0],
        cluster.coordinates.galacticVector[1] + point.clusterOffsetVector[1],
        cluster.coordinates.galacticVector[2] + point.clusterOffsetVector[2],
      ]);
    }
    point.currentDistance = point.coordinates.distance;
  }

  invalidateCoordinateCache();
  if (state.cameraLocked && state.locked && (state.locked.kind === "catalog" || state.locked.kind === "cluster")) {
    state.customCoordinateContext = centerContext(state.locked.coordinates.galacticVector);
  }
  if (updateTarget && (state.locked || state.hovered)) setTarget(state.locked || state.hovered);
  markCatalogStaticDirty();
}

function setUncertaintySeed(value) {
  const seed = clampUncertaintySeed(value);
  if (state.uncertaintySeed === seed) return;
  state.uncertaintySeed = seed;
  applyUncertaintyRealization();
  syncRangeOutputs();
  markProjectionDirty();
}

function requestUncertaintySeed(value) {
  pendingUncertaintySeed = clampUncertaintySeed(value);
  if (uncertaintySeedFrame) return;
  uncertaintySeedFrame = window.requestAnimationFrame(() => {
    uncertaintySeedFrame = 0;
    const seed = pendingUncertaintySeed;
    pendingUncertaintySeed = null;
    setUncertaintySeed(seed);
  });
}

function decodeColorCurve(encoded) {
  if (!encoded) return null;
  try {
    const binary = window.atob(encoded);
    if (binary.length < 8) return null;
    const offsets = new Float32Array(binary.length);
    for (let index = 0; index < binary.length; index += 1) {
      offsets[index] = (binary.charCodeAt(index) - FITTED_COLOR_CURVE_ZERO) / FITTED_COLOR_CURVE_SCALE;
    }
    return offsets;
  } catch {
    return null;
  }
}

function decodeLightCurve(encoded) {
  if (!encoded) return null;
  try {
    const binary = window.atob(encoded);
    if (binary.length < 8) return null;

    if (binary.length === WAVEFORM_SAMPLES * 2) {
      const offsets = new Float32Array(WAVEFORM_SAMPLES);
      for (let index = 0; index < WAVEFORM_SAMPLES; index += 1) {
        const low = binary.charCodeAt(index * 2);
        const high = binary.charCodeAt(index * 2 + 1);
        let value = low | (high << 8);
        if (value >= 0x8000) value -= 0x10000;
        offsets[index] = value / FITTED_LIGHT_CURVE_INT16_SCALE;
      }
      return offsets;
    }

    const offsets = new Float32Array(binary.length);
    for (let index = 0; index < binary.length; index += 1) {
      offsets[index] = (binary.charCodeAt(index) - FITTED_LIGHT_CURVE_ZERO) / FITTED_LIGHT_CURVE_SCALE;
    }
    return offsets;
  } catch {
    return null;
  }
}

function samplePeriodic(samples, phase) {
  const scaled = positiveModulo(phase, 1) * samples.length;
  const index = Math.floor(scaled) % samples.length;
  const next = (index + 1) % samples.length;
  const fraction = scaled - Math.floor(scaled);
  return samples[index] * (1 - fraction) + samples[next] * fraction;
}

function numericArray(value) {
  if (!Array.isArray(value)) return null;
  const values = value.map((item) => Number(item)).filter((item) => Number.isFinite(item));
  return values.length ? values : null;
}

function miraComponentsForRow(row, band = "I") {
  if (DATASET_KEYS[row[IDX.dataset]] !== "miras") return null;
  const periods = numericArray(row[IDX.miraPeriods]);
  const amplitudes = numericArray(band === "V" ? row[IDX.miraAmplitudesV] : row[IDX.miraAmplitudesI]);
  const phases = numericArray(band === "V" ? row[IDX.miraPhasesV] : row[IDX.miraPhasesI]);
  if (!periods || !amplitudes || !phases) return null;
  const count = Math.min(periods.length, amplitudes.length, phases.length);
  const components = [];
  for (let index = 0; index < count; index += 1) {
    const period = periods[index];
    const amplitude = amplitudes[index];
    const phase = phases[index];
    if (period > 0 && amplitude > 0 && Number.isFinite(phase)) {
      components.push({ period, amplitude, phase });
    }
  }
  return components.length ? components : null;
}

function miraMagnitudeOffsetAtDay(components, simulationDay) {
  let offset = 0;
  for (const component of components) {
    offset +=
      0.5 *
      component.amplitude *
      Math.sin((Math.PI * 2 * simulationDay) / component.period + component.phase);
  }
  return offset;
}

function hashString(value) {
  let hash = 2166136261;
  for (let index = 0; index < value.length; index += 1) {
    hash ^= value.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return Math.abs(hash >>> 0);
}

function seededUnit32(value) {
  return (hashString(value) + 0.5) / 4294967296;
}

function seededUnit(value) {
  return (hashString(value) % 100000) / 100000;
}

function positiveModulo(value, divisor) {
  return ((value % divisor) + divisor) % divisor;
}

function sortedQuantile(sortedValues, quantile) {
  if (!sortedValues.length) return null;
  if (sortedValues.length === 1) return sortedValues[0];
  const bounded = clamp(quantile, 0, 1);
  const position = bounded * (sortedValues.length - 1);
  const lowIndex = Math.floor(position);
  const highIndex = Math.ceil(position);
  const fraction = position - lowIndex;
  return sortedValues[lowIndex] * (1 - fraction) + sortedValues[highIndex] * fraction;
}

function lowerBoundByLogLum(samples, logLuminosity) {
  let low = 0;
  let high = samples.length;
  while (low < high) {
    const mid = (low + high) >> 1;
    if (samples[mid].logLum < logLuminosity) low = mid + 1;
    else high = mid;
  }
  return low;
}

function simulationDayForSpeed(speed = state.pulsationSpeed, now = performance.now()) {
  const elapsedMs = now - animationStartMs;
  return animationEpoch + simulationTimeOffsetDays + (elapsedMs / 86400000) * speed;
}

function setSimulationOffsetForDay(day, speed = state.pulsationSpeed, now = performance.now()) {
  simulationTimeOffsetDays = day - animationEpoch - ((now - animationStartMs) / 86400000) * speed;
}

function currentSimulationDay(now = performance.now()) {
  if (state.pulsationPaused && Number.isFinite(pausedSimulationDay)) return pausedSimulationDay;
  return simulationDayForSpeed(state.pulsationSpeed, now);
}

function setPulsationSpeed(value, { preserveDay = true } = {}) {
  const now = performance.now();
  const day = preserveDay ? currentSimulationDay(now) : null;
  const speed = clampPulsationSpeed(value);
  state.pulsationSpeed = speed;
  state.pulsationSpeedLog = Math.log10(speed);
  if (preserveDay && Number.isFinite(day)) {
    if (state.pulsationPaused) pausedSimulationDay = day;
    else setSimulationOffsetForDay(day, speed, now);
  }
}

function resetSimulationClock() {
  simulationTimeOffsetDays = 0;
  pausedSimulationDay = null;
  state.pulsationPaused = false;
}

function setPulsationPaused(paused) {
  const shouldPause = Boolean(paused);
  if (state.pulsationPaused === shouldPause) return;
  const now = performance.now();
  if (shouldPause) {
    pausedSimulationDay = currentSimulationDay(now);
    state.pulsationPaused = true;
  } else {
    if (Number.isFinite(pausedSimulationDay)) setSimulationOffsetForDay(pausedSimulationDay, state.pulsationSpeed, now);
    pausedSimulationDay = null;
    state.pulsationPaused = false;
  }
  markCatalogStaticDirty();
  queueRender();
}

function togglePulsationPaused() {
  setPulsationPaused(!state.pulsationPaused);
}

function adjustPulsationSpeed(direction, fast = false) {
  if (!direction) return;
  const gain = fast ? PULSATION_SPEED_KEY_FAST_GAIN : PULSATION_SPEED_KEY_GAIN;
  const factor = direction > 0 ? gain : 1 / gain;
  setPulsationSpeed(state.pulsationSpeed * factor);
  markCatalogStaticDirty();
  syncRangeOutputs();
  queueRender();
}

function updatePulsationClock() {
  if (!elements.pulsationClockHourHand) return;
  const dayFraction = positiveModulo(currentSimulationDay(), 1);
  elements.pulsationClockHourHand.style.transform = `rotate(${dayFraction * 360}deg)`;
}

function lightCurveParams(row) {
  const measuredAmplitudeI = Number(row[IDX.amplitudeI]);
  if (Number.isFinite(measuredAmplitudeI) && measuredAmplitudeI > 0) {
    const measuredT0 = Number.isFinite(row[IDX.t0])
      ? row[IDX.t0]
      : animationEpoch + seededUnit(`${row[IDX.id]}-phase`) * row[IDX.period];
    return {
      amplitude: measuredAmplitudeI,
      t0: measuredT0,
      r21: row[IDX.r21] || 0,
      phi21: row[IDX.phi21] || 0,
      r31: row[IDX.r31] || 0,
      phi31: row[IDX.phi31] || 0,
      subtype: row[IDX.lightCurveSubtype] || row[IDX.mode] || DATASET_LABELS[row[IDX.dataset]],
      measured: true,
    };
  }

  const dataset = row[IDX.dataset];
  const datasetKey = DATASET_KEYS[dataset];
  const subtype =
    row[IDX.mode] || (datasetKey === "rrlyrae" ? "RRab" : datasetKey === "miras" ? "Mira" : "F");
  const overtone = String(subtype).includes("1O") || String(subtype).includes("RRc");
  let defaults;
  if (datasetKey === "cepheids" || datasetKey === "anomalousCepheids") {
    defaults = {
      amplitude: overtone ? 0.34 : 0.58,
      r21: overtone ? 0.16 : 0.42,
      phi21: overtone ? 3.9 : 4.7,
      r31: overtone ? 0.06 : 0.2,
      phi31: overtone ? 2.5 : 3.1,
    };
  } else if (datasetKey === "miras") {
    defaults = {
      amplitude: 1.2,
      r21: 0,
      phi21: 0,
      r31: 0,
      phi31: 0,
    };
  } else {
    defaults = {
      amplitude: 0.48,
      r21: 0.48,
      phi21: 4.45,
      r31: 0.3,
      phi31: 2.75,
    };
  }

  return {
    ...defaults,
    t0: animationEpoch + seededUnit(`${row[IDX.id]}-phase`) * row[IDX.period],
    subtype,
    measured: false,
  };
}

function vToIAmplitudeRatio(row, subtype) {
  const mode = String(subtype || row[IDX.mode] || "");
  const firstOvertone = mode.includes("1O") || mode.includes("RRc");
  const datasetKey = DATASET_KEYS[row[IDX.dataset]];

  if (datasetKey === "cepheids" || datasetKey === "anomalousCepheids") {
    return firstOvertone ? 1.42 : 1.55;
  }
  if (datasetKey === "miras") {
    return 1.85;
  }

  return firstOvertone ? 1.48 : 1.62;
}

function magnitudeOffsetSpan(samples, mean = 0) {
  let min = Infinity;
  let max = -Infinity;
  for (let index = 0; index < samples.length; index += 1) {
    const value = samples[index] - mean;
    if (!Number.isFinite(value)) continue;
    min = Math.min(min, value);
    max = Math.max(max, value);
  }
  if (!Number.isFinite(min) || !Number.isFinite(max)) return 0;
  return max - min;
}

function fluxFromMagnitudeOffset(magnitudeOffset) {
  if (!Number.isFinite(magnitudeOffset)) return 1;
  return clamp(10 ** (-0.4 * magnitudeOffset), RAW_PULSE_FLUX_MIN, RAW_PULSE_FLUX_MAX);
}

function maxColorPulseOffsetForRow(row, source = "") {
  if (DATASET_KEYS[row?.[IDX.dataset]] !== "miras") return MAX_COLOR_PULSE_OFFSET;
  if (String(source).startsWith("learned-mira-v-prior")) return MAX_MIRA_PRIOR_ONLY_COLOR_PULSE_OFFSET;
  if (String(source).includes("prior")) return MAX_MIRA_PRIOR_ASSISTED_COLOR_PULSE_OFFSET;
  return MAX_MIRA_COLOR_PULSE_OFFSET;
}

function colorPulseOffsetBoundsForRow(row, meanVMinusI0, source = "") {
  const maxOffset = maxColorPulseOffsetForRow(row, source);
  let min = -maxOffset;
  let max = maxOffset;
  if (isMiraRow(row) && Number.isFinite(meanVMinusI0)) {
    min = Math.max(min, MIRA_MIN_INTRINSIC_V_MINUS_I - meanVMinusI0);
    max = Math.min(max, MIRA_MAX_INTRINSIC_V_MINUS_I - meanVMinusI0);
  }
  return { min, max };
}

function makeWaveform(row) {
  const params = lightCurveParams(row);
  const colorAmplitudeRatio = vToIAmplitudeRatio(row, params.subtype);
  const fittedColorOffsets = decodeColorCurve(row[IDX.colorCurve]);
  const fittedIMagnitudeOffsets = decodeLightCurve(row[IDX.brightnessCurve]);
  const miraComponents = miraComponentsForRow(row, "I");
  const miraVComponents = miraComponentsForRow(row, "V");
  const miraVSource = miraVComponents ? String(row[IDX.miraVPulsationSource] || "") : "";
  const miraVUsesPrior = miraVSource.includes("prior");
  const miraVIsPriorOnly = miraVSource.startsWith("learned-mira-v-prior");
  const iMagnitudeOffsets = new Float32Array(WAVEFORM_SAMPLES);
  const vMagnitudeOffsets = new Float32Array(WAVEFORM_SAMPLES);
  let miraPrimaryPeriod = params.period || row[IDX.period] || 1;
  let meanIMagnitudeOffset = 0;
  let meanVMagnitudeOffset = 0;

  if (miraComponents) {
    miraPrimaryPeriod = miraComponents[0].period || miraPrimaryPeriod;
    for (let index = 0; index < WAVEFORM_SAMPLES; index += 1) {
      const simulationDay = animationEpoch + (index / WAVEFORM_SAMPLES) * miraPrimaryPeriod;
      const magnitudeOffset = miraMagnitudeOffsetAtDay(miraComponents, simulationDay);
      iMagnitudeOffsets[index] = magnitudeOffset;
      meanIMagnitudeOffset += magnitudeOffset;
      if (miraVComponents) {
        const vMagnitudeOffset = miraMagnitudeOffsetAtDay(miraVComponents, simulationDay);
        vMagnitudeOffsets[index] = vMagnitudeOffset;
        meanVMagnitudeOffset += vMagnitudeOffset;
      }
    }
  } else if (fittedIMagnitudeOffsets) {
    for (let index = 0; index < WAVEFORM_SAMPLES; index += 1) {
      const magnitudeOffset = samplePeriodic(fittedIMagnitudeOffsets, index / WAVEFORM_SAMPLES);
      iMagnitudeOffsets[index] = magnitudeOffset;
      meanIMagnitudeOffset += magnitudeOffset;
    }
  } else {
    const shape = [];
    for (let index = 0; index < WAVEFORM_SAMPLES; index += 1) {
      const angle = (index / WAVEFORM_SAMPLES) * Math.PI * 2;
      shape.push(
        Math.cos(angle) +
          params.r21 * Math.cos(2 * angle + params.phi21) +
          params.r31 * Math.cos(3 * angle + params.phi31),
      );
    }

    let min = Infinity;
    let max = -Infinity;
    let brightestIndex = 0;
    for (let index = 0; index < shape.length; index += 1) {
      if (shape[index] < min) {
        min = shape[index];
        brightestIndex = index;
      }
      max = Math.max(max, shape[index]);
    }

    const range = Math.max(0.001, max - min);
    const midpoint = (max + min) / 2;
    for (let index = 0; index < WAVEFORM_SAMPLES; index += 1) {
      const shifted = shape[(index + brightestIndex) % WAVEFORM_SAMPLES];
      const magnitudeOffset = ((shifted - midpoint) / range) * params.amplitude;
      iMagnitudeOffsets[index] = magnitudeOffset;
      meanIMagnitudeOffset += magnitudeOffset;
    }
  }
  meanIMagnitudeOffset /= WAVEFORM_SAMPLES;
  if (miraVComponents) {
    meanVMagnitudeOffset /= WAVEFORM_SAMPLES;
  }

  const waveform = new Float32Array(WAVEFORM_SAMPLES);
  const rawColorOffsets = new Float32Array(WAVEFORM_SAMPLES);
  const colorOffsets = new Float32Array(WAVEFORM_SAMPLES);
  const logLuminosities = new Float32Array(WAVEFORM_SAMPLES);
  const temperatures = new Float32Array(WAVEFORM_SAMPLES);
  const colors = new Array(WAVEFORM_SAMPLES);
  const rgbColors = new Float32Array(WAVEFORM_SAMPLES * 3);
  const meanVMinusI0 = intrinsicVMinusIForRow(row);
  const iAmplitude = magnitudeOffsetSpan(iMagnitudeOffsets, meanIMagnitudeOffset);
  const fallbackVAmplitude = iAmplitude * colorAmplitudeRatio;
  const measuredMiraVAmplitude = miraVComponents ? magnitudeOffsetSpan(vMagnitudeOffsets, meanVMagnitudeOffset) : 0;
  let minFittedVMagnitudeOffset = Infinity;
  let maxFittedVMagnitudeOffset = -Infinity;
  let minFlux = Infinity;
  let maxFlux = -Infinity;
  let maxFluxIndex = 0;
  let meanFlux = 0;
  let meanColorOffset = 0;
  const maxColorPulseOffset = maxColorPulseOffsetForRow(row, miraVSource);
  const colorOffsetBounds = colorPulseOffsetBoundsForRow(row, meanVMinusI0, miraVSource);

  for (let index = 0; index < WAVEFORM_SAMPLES; index += 1) {
    const iMagnitudeOffset = iMagnitudeOffsets[index];
    const rawColorOffset = fittedColorOffsets
      ? samplePeriodic(fittedColorOffsets, index / WAVEFORM_SAMPLES)
      : miraVComponents
        ? vMagnitudeOffsets[index] - meanVMagnitudeOffset - (iMagnitudeOffset - meanIMagnitudeOffset)
        : (colorAmplitudeRatio - 1) * (iMagnitudeOffset - meanIMagnitudeOffset);
    rawColorOffsets[index] = rawColorOffset;
    if (fittedColorOffsets || miraVComponents) {
      const fittedVMagnitudeOffset = miraVComponents
        ? vMagnitudeOffsets[index] - meanVMagnitudeOffset
        : iMagnitudeOffset + rawColorOffset;
      minFittedVMagnitudeOffset = Math.min(minFittedVMagnitudeOffset, fittedVMagnitudeOffset);
      maxFittedVMagnitudeOffset = Math.max(maxFittedVMagnitudeOffset, fittedVMagnitudeOffset);
    }
  }

  const iAmplitudeSafe = Math.max(0.001, iAmplitude);
  const fittedVAmplitude =
    Number.isFinite(minFittedVMagnitudeOffset) && Number.isFinite(maxFittedVMagnitudeOffset)
      ? maxFittedVMagnitudeOffset - minFittedVMagnitudeOffset
      : 0;
  const catalogVAmplitude = Number(row[IDX.amplitudeV]);
  let vAmplitude = fallbackVAmplitude;
  let vAmplitudeSource = "template ratio";
  if (miraVComponents && measuredMiraVAmplitude > 0) {
    vAmplitude = measuredMiraVAmplitude;
    vAmplitudeSource = miraVIsPriorOnly ? "learned Mira V prior" : miraVUsesPrior ? "OGLE V + prior" : "OGLE V multisine";
  } else if (Number.isFinite(catalogVAmplitude) && catalogVAmplitude > 0) {
    vAmplitude = catalogVAmplitude;
    vAmplitudeSource = "catalog V";
  } else if (fittedColorOffsets && fittedVAmplitude > 0 && fittedVAmplitude <= iAmplitudeSafe * 3.2) {
    vAmplitude = fittedVAmplitude;
    vAmplitudeSource = "OGLE V/I fit";
  }
  const vAmplitudeSafe = Math.max(0.001, vAmplitude);
  const brightnessAmplitudeScale = vAmplitudeSafe / iAmplitudeSafe;
  let amplitudeSourceFluxes = null;

  for (let index = 0; index < WAVEFORM_SAMPLES; index += 1) {
    const iMagnitudeOffset = iMagnitudeOffsets[index];
    const centeredIMagnitudeOffset = iMagnitudeOffset - meanIMagnitudeOffset;
    const brightnessMagnitudeOffset = miraVComponents
      ? vMagnitudeOffsets[index] - meanVMagnitudeOffset
      : centeredIMagnitudeOffset * brightnessAmplitudeScale;
    const rawColorOffset = rawColorOffsets[index];
    const colorOffset = clamp(rawColorOffset, colorOffsetBounds.min, colorOffsetBounds.max);
    const logLuminosity = Number.isFinite(row[IDX.logLum])
      ? row[IDX.logLum] - 0.4 * centeredIMagnitudeOffset
      : NaN;
    const temperature = effectiveTemperatureForCatalogState(row, meanVMinusI0 + colorOffset, logLuminosity);
    waveform[index] = fluxFromMagnitudeOffset(brightnessMagnitudeOffset);
    colorOffsets[index] = colorOffset;
    logLuminosities[index] = logLuminosity;
    temperatures[index] = Number.isFinite(temperature) ? temperature : NaN;
    const color = Number.isFinite(meanVMinusI0)
      ? Number.isFinite(temperature)
        ? colorForTemperature(temperature)
        : colorForCatalogState(row, meanVMinusI0, logLuminosity)
      : colorForCatalogState(row, meanVMinusI0, logLuminosity);
    const rgbColor = cssColorToRgb(color);
    colors[index] = color;
    rgbColors[index * 3] = rgbColor[0] / 255;
    rgbColors[index * 3 + 1] = rgbColor[1] / 255;
    rgbColors[index * 3 + 2] = rgbColor[2] / 255;
    meanFlux += waveform[index];
    meanColorOffset += colorOffset;
    minFlux = Math.min(minFlux, waveform[index]);
    if (waveform[index] > maxFlux) {
      maxFlux = waveform[index];
      maxFluxIndex = index;
    }
  }
  meanFlux /= WAVEFORM_SAMPLES;
  meanColorOffset /= WAVEFORM_SAMPLES;
  if (miraComponents) {
    const sampleCount = Math.max(WAVEFORM_SAMPLES * MIRA_AMPLITUDE_STATS_CYCLES, 320);
    amplitudeSourceFluxes = new Float32Array(sampleCount);
    for (let index = 0; index < sampleCount; index += 1) {
      const simulationDay = animationEpoch + (index / sampleCount) * MIRA_AMPLITUDE_STATS_CYCLES * miraPrimaryPeriod;
      const iMagnitudeOffset =
        miraMagnitudeOffsetAtDay(miraComponents, simulationDay) - (meanIMagnitudeOffset || 0);
      let brightnessMagnitudeOffset = iMagnitudeOffset * brightnessAmplitudeScale;
      if (miraVComponents) {
        brightnessMagnitudeOffset =
          miraMagnitudeOffsetAtDay(miraVComponents, simulationDay) - (meanVMagnitudeOffset || 0);
      }
      amplitudeSourceFluxes[index] = fluxFromMagnitudeOffset(brightnessMagnitudeOffset);
    }
  }
  const meanColor = Number.isFinite(meanVMinusI0)
    ? colorForCatalogState(row, meanVMinusI0 + meanColorOffset, row[IDX.logLum])
    : colors[0];

  return {
    waveform,
    colorOffsets,
    logLuminosities,
    temperatures,
    colors,
    rgbColors,
    params,
    minFlux,
    maxFlux,
    meanFlux,
    amplitudeSourceFluxes,
    meanColor,
    meanColorOffset,
    currentBaseLogLuminosity: row[IDX.logLum],
    maxFluxPhase: maxFluxIndex / WAVEFORM_SAMPLES,
    source: miraComponents ? "mira-multisine" : fittedIMagnitudeOffsets ? "ogle-fit" : params.measured ? "fourier" : "template",
    sourceQuality: miraComponents ? row[IDX.miraPulsationQuality] || 0 : row[IDX.brightnessCurveQuality] || 0,
    brightnessBand: "V",
    shapeBand: "I",
    iAmplitude,
    vAmplitude: vAmplitudeSafe,
    brightnessAmplitudeScale,
    vAmplitudeSource,
    meanIMagnitudeOffset,
    meanVMagnitudeOffset,
    colorAmplitudeRatio,
    colorSource: miraVComponents
      ? miraVIsPriorOnly
        ? "mira-v-prior"
        : miraVUsesPrior
          ? "ogle-v-prior"
          : "ogle-v-multisine"
      : fittedColorOffsets
        ? "ogle-fit"
        : "template",
    colorQuality: miraVComponents ? row[IDX.miraVPulsationQuality] || 0 : row[IDX.colorCurveQuality] || 0,
    miraVSource,
    maxColorPulseOffset,
    colorOffsetBounds,
    timeDomain: Boolean(miraComponents),
    components: miraComponents,
    vComponents: miraVComponents,
  };
}

function observedInstabilityStripSample(row) {
  const datasetIndex = Math.trunc(Number(row?.[IDX.dataset]));
  const datasetKey = DATASET_KEYS[datasetIndex];
  if (!CLUSTER_PULSATOR_STRIP_DATASET_KEYS.includes(datasetKey)) return null;

  const logLum = Number(row[IDX.logLum]);
  const color = intrinsicVMinusIForRow(row);
  const period = Number(row[IDX.period]);
  if (!Number.isFinite(logLum) || !Number.isFinite(color) || !Number.isFinite(period) || period <= 0) {
    return null;
  }

  return {
    row,
    datasetIndex,
    datasetKey,
    logLum,
    color,
    period,
  };
}

function buildObservedInstabilityStripModel(catalogRows) {
  const grouped = new Map();
  for (const row of catalogRows || []) {
    const sample = observedInstabilityStripSample(row);
    if (!sample) continue;
    if (!grouped.has(sample.datasetKey)) grouped.set(sample.datasetKey, []);
    grouped.get(sample.datasetKey).push(sample);
  }

  const strips = [];
  for (const datasetKey of CLUSTER_PULSATOR_STRIP_DATASET_KEYS) {
    const samples = grouped.get(datasetKey) || [];
    if (samples.length < CLUSTER_PULSATOR_STRIP_MIN_BIN_STARS) continue;

    samples.sort((left, right) => left.logLum - right.logLum);
    const logLumValues = samples.map((sample) => sample.logLum);
    const colorValues = samples.map((sample) => sample.color).sort((left, right) => left - right);
    const logLumLow = sortedQuantile(logLumValues, 0.01);
    const logLumHigh = sortedQuantile(logLumValues, 0.99);
    const binStart = Number.isFinite(logLumLow) ? logLumLow : logLumValues[0];
    const binEnd = Number.isFinite(logLumHigh) ? logLumHigh : logLumValues[logLumValues.length - 1];
    const binWidth = Math.max(0.001, (binEnd - binStart) / CLUSTER_PULSATOR_STRIP_BIN_COUNT);
    const bins = [];

    for (let binIndex = 0; binIndex < CLUSTER_PULSATOR_STRIP_BIN_COUNT; binIndex += 1) {
      const low = binStart + binIndex * binWidth;
      const high = binIndex === CLUSTER_PULSATOR_STRIP_BIN_COUNT - 1 ? binEnd + 1e-9 : low + binWidth;
      const binColors = samples
        .filter((sample) => sample.logLum >= low && sample.logLum < high)
        .map((sample) => sample.color)
        .sort((left, right) => left - right);
      if (binColors.length < CLUSTER_PULSATOR_STRIP_MIN_BIN_STARS) continue;

      bins.push({
        center: (low + high) * 0.5,
        lower: sortedQuantile(binColors, CLUSTER_PULSATOR_STRIP_COLOR_LOW_QUANTILE),
        upper: sortedQuantile(binColors, CLUSTER_PULSATOR_STRIP_COLOR_HIGH_QUANTILE),
        count: binColors.length,
      });
    }

    if (!bins.length) {
      bins.push({
        center: (binStart + binEnd) * 0.5,
        lower: sortedQuantile(colorValues, CLUSTER_PULSATOR_STRIP_COLOR_LOW_QUANTILE),
        upper: sortedQuantile(colorValues, CLUSTER_PULSATOR_STRIP_COLOR_HIGH_QUANTILE),
        count: samples.length,
      });
    }

    const colorP16 = sortedQuantile(colorValues, 0.16);
    const colorP84 = sortedQuantile(colorValues, 0.84);
    strips.push({
      datasetKey,
      datasetIndex: DATASET_KEYS.indexOf(datasetKey),
      samples,
      bins,
      logLumMin: binStart - CLUSTER_PULSATOR_STRIP_LOG_LUM_MARGIN,
      logLumMax: binEnd + CLUSTER_PULSATOR_STRIP_LOG_LUM_MARGIN,
      logLumScale: Math.max(0.12, (binEnd - binStart) * 0.5),
      colorScale: Math.max(0.05, (colorP84 || 0) - (colorP16 || 0)),
    });
  }

  return { strips };
}

function interpolatedInstabilityStripBounds(strip, logLuminosity) {
  const bins = strip?.bins || [];
  if (!bins.length) return null;
  if (bins.length === 1 || logLuminosity <= bins[0].center) {
    return {
      lower: bins[0].lower - CLUSTER_PULSATOR_STRIP_COLOR_MARGIN,
      upper: bins[0].upper + CLUSTER_PULSATOR_STRIP_COLOR_MARGIN,
    };
  }
  const last = bins[bins.length - 1];
  if (logLuminosity >= last.center) {
    return {
      lower: last.lower - CLUSTER_PULSATOR_STRIP_COLOR_MARGIN,
      upper: last.upper + CLUSTER_PULSATOR_STRIP_COLOR_MARGIN,
    };
  }

  for (let index = 0; index < bins.length - 1; index += 1) {
    const left = bins[index];
    const right = bins[index + 1];
    if (logLuminosity < left.center || logLuminosity > right.center) continue;
    const fraction = (logLuminosity - left.center) / Math.max(0.000001, right.center - left.center);
    return {
      lower:
        left.lower * (1 - fraction) +
        right.lower * fraction -
        CLUSTER_PULSATOR_STRIP_COLOR_MARGIN,
      upper:
        left.upper * (1 - fraction) +
        right.upper * fraction +
        CLUSTER_PULSATOR_STRIP_COLOR_MARGIN,
    };
  }

  return null;
}

function nearestObservedPulsatorReference(strip, logLuminosity, color) {
  const samples = strip?.samples || [];
  if (!samples.length) return null;

  let left = lowerBoundByLogLum(samples, logLuminosity) - 1;
  let right = left + 1;
  let checked = 0;
  let best = null;

  while (
    checked < CLUSTER_PULSATOR_NEAREST_REFERENCE_COUNT &&
    (left >= 0 || right < samples.length)
  ) {
    const useLeft =
      right >= samples.length ||
      (left >= 0 &&
        Math.abs(samples[left].logLum - logLuminosity) <=
          Math.abs(samples[right].logLum - logLuminosity));
    const sample = useLeft ? samples[left] : samples[right];
    if (useLeft) left -= 1;
    else right += 1;

    const logLumScore = (sample.logLum - logLuminosity) / strip.logLumScale;
    const colorScore = (sample.color - color) / strip.colorScale;
    const distance = logLumScore * logLumScore + colorScore * colorScore;
    if (!best || distance < best.distance) best = { sample, distance };
    checked += 1;
  }

  return best;
}

function clusterStarInstabilityStripMatch(row, stripModel) {
  const logLum = Number(row?.[CS.logLum]);
  const color = Number(row?.[CS.vMinusI0]);
  if (!Number.isFinite(logLum) || !Number.isFinite(color)) return null;

  let best = null;
  for (const strip of stripModel?.strips || []) {
    if (logLum < strip.logLumMin || logLum > strip.logLumMax) continue;
    const bounds = interpolatedInstabilityStripBounds(strip, logLum);
    if (!bounds || color < bounds.lower || color > bounds.upper) continue;

    const reference = nearestObservedPulsatorReference(strip, logLum, color);
    if (!reference) continue;
    const center = (bounds.lower + bounds.upper) * 0.5;
    const halfWidth = Math.max(0.02, (bounds.upper - bounds.lower) * 0.5);
    const stripScore = reference.distance + (Math.abs(color - center) / halfWidth) * 0.05;
    if (!best || stripScore < best.score) {
      best = { strip, reference: reference.sample, score: stripScore };
    }
  }

  return best;
}

function clusterLocationIndexForRow(clusterRow) {
  const galaxy = String(clusterRow?.[CL.galaxy] || "").toUpperCase();
  if (galaxy === "LMC") return 0;
  if (galaxy === "SMC") return 1;
  return 3;
}

function syntheticCatalogRowForClusterPulsator(clusterStarRow, clusterStarIndex, clusterRow, match) {
  const referenceRow = match.reference.row;
  const syntheticRow = referenceRow.slice();
  const clusterName = String(clusterRow?.[CL.name] || `cluster-${clusterStarRow?.[CS.cluster] ?? "unknown"}`);
  const period = Math.max(
    0.05,
    Number(referenceRow[IDX.period]) || PULSATOR_PRESET_MEDIAN_PERIOD_DAYS[match.strip.datasetKey] || 1,
  );
  const logAge = Number(clusterRow?.[CL.logAge]);

  syntheticRow[IDX.x] = clusterStarRow[CS.x];
  syntheticRow[IDX.y] = clusterStarRow[CS.y];
  syntheticRow[IDX.z] = clusterStarRow[CS.z];
  syntheticRow[IDX.logLum] = clusterStarRow[CS.logLum];
  syntheticRow[IDX.lum] = clusterStarRow[CS.lum];
  syntheticRow[IDX.radius] = clusterStarRow[CS.radius];
  syntheticRow[IDX.spectral] = clusterStarRow[CS.spectral];
  syntheticRow[IDX.dataset] = match.strip.datasetIndex;
  syntheticRow[IDX.location] = clusterLocationIndexForRow(clusterRow);
  syntheticRow[IDX.period] = period;
  syntheticRow[IDX.distance] = clusterStarRow[CS.distance];
  syntheticRow[IDX.vMinusI] = clusterStarRow[CS.vMinusI0];
  syntheticRow[IDX.vMinusI0] = clusterStarRow[CS.vMinusI0];
  syntheticRow[IDX.age] = Number.isFinite(logAge) ? 10 ** (logAge - 6) : syntheticRow[IDX.age];
  syntheticRow[IDX.feh] = Number.isFinite(clusterRow?.[CL.feh]) ? clusterRow[CL.feh] : syntheticRow[IDX.feh];
  syntheticRow[IDX.mode] = referenceRow[IDX.mode] || referenceRow[IDX.lightCurveSubtype] || DATASET_LABELS[match.strip.datasetIndex];
  syntheticRow[IDX.id] = `MIST-${clusterName}-${clusterStarIndex}`;
  syntheticRow[IDX.t0] = animationEpoch + seededUnit(`${syntheticRow[IDX.id]}-phase`) * period;
  syntheticRow[IDX.raDeg] = clusterStarRow[CS.raDeg];
  syntheticRow[IDX.decDeg] = clusterStarRow[CS.decDeg];
  syntheticRow[IDX.galLonDeg] = clusterStarRow[CS.galLonDeg];
  syntheticRow[IDX.galLatDeg] = clusterStarRow[CS.galLatDeg];
  syntheticRow[IDX.reddeningEVI] = 0;
  syntheticRow[IDX.reddeningEVIError] = 0;
  syntheticRow[IDX.distanceError] = 0;
  syntheticRow[IDX.distanceSource] = "cluster";
  syntheticRow[IDX.miraPeriods] = null;
  syntheticRow[IDX.miraAmplitudesI] = null;
  syntheticRow[IDX.miraPhasesI] = null;
  syntheticRow[IDX.miraAmplitudesV] = null;
  syntheticRow[IDX.miraPhasesV] = null;
  syntheticRow[IDX.miraTeff] = null;
  syntheticRow[IDX.miraTeffSourceIndex] = null;
  return syntheticRow;
}

function makeClusterStarWaveform(clusterStarRow, clusterStarIndex, clusterRow, match) {
  if (!match) return null;
  const syntheticRow = syntheticCatalogRowForClusterPulsator(clusterStarRow, clusterStarIndex, clusterRow, match);
  const lightCurve = makeWaveform(syntheticRow);
  lightCurve.params.period = syntheticRow[IDX.period];
  lightCurve.syntheticClusterPulsator = true;
  lightCurve.referenceId = match.reference.row[IDX.id];
  lightCurve.referenceDatasetKey = match.strip.datasetKey;
  lightCurve.syntheticRow = syntheticRow;
  return lightCurve;
}

function pulsationPeriodDays(point) {
  return Math.max(0.05, Number(point?.lightCurve?.params?.period || point?.row?.[IDX.period] || 1));
}

function renderedPulsationFrequencyHz(point) {
  if (!point?.lightCurve) return 0;
  return state.pulsationSpeed / (pulsationPeriodDays(point) * SECONDS_PER_DAY);
}

function renderedPulsationPeriodSeconds(point) {
  const frequencyHz = renderedPulsationFrequencyHz(point);
  return frequencyHz > 0 ? 1 / frequencyHz : Infinity;
}

function shouldSlowPulseThrottleCatalogItem(item) {
  const point = item?.point;
  if (!point?.lightCurve) return false;
  updateSlowPulseRefreshSchedule(item);
  return item.slowPulseAdaptiveRefreshIntervalMs > SLOW_PULSE_REFRESH_FRAME_INTERVAL_MS + 1;
}

function pulsationTooFastForAnimation(point) {
  return renderedPulsationFrequencyHz(point) > PULSATION_FLICKER_FREQUENCY_HZ;
}

function waveformSample(point, simulationDay) {
  const period = pulsationPeriodDays(point);
  const phase = positiveModulo((simulationDay - point.lightCurve.params.t0) / period, 1);
  const sample = phase * WAVEFORM_SAMPLES;
  const index = Math.floor(sample) % WAVEFORM_SAMPLES;
  const next = (index + 1) % WAVEFORM_SAMPLES;
  const fraction = sample - Math.floor(sample);
  return { phase, index, next, fraction };
}

function frozenLightCurveSampleDay(point) {
  const lightCurve = point?.lightCurve;
  const period = pulsationPeriodDays(point);
  if (!lightCurve?.waveform?.length) return lightCurve?.params?.t0 || animationEpoch;

  let bestIndex = 0;
  let bestDistance = Infinity;
  const meanFlux = lightCurve.meanFlux || 1;
  for (let index = 0; index < lightCurve.waveform.length; index += 1) {
    const flux = lightCurve.waveform[index];
    const distance = Math.abs(flux - meanFlux);
    if (distance < bestDistance) {
      bestDistance = distance;
      bestIndex = index;
    }
  }
  return (lightCurve.params?.t0 || animationEpoch) + (bestIndex / lightCurve.waveform.length) * period;
}

function lightCurveInsetSampleDay(point) {
  return pulsationTooFastForAnimation(point) ? frozenLightCurveSampleDay(point) : currentSimulationDay();
}

function interpolateSamples(samples, sample) {
  return samples[sample.index] * (1 - sample.fraction) + samples[sample.next] * sample.fraction;
}

function amplitudeFluxRatio(flux, meanFlux) {
  return Math.max(PULSE_FLUX_RATIO_MIN, Number(flux) / Math.max(PULSE_FLUX_RATIO_MIN, meanFlux));
}

function lightCurveAmplitudeScaleStats(lightCurve, scale = clampPulsationAmplitudeScale(state.pulsationAmplitudeScale)) {
  const meanFlux = Math.max(0.001, lightCurve?.meanFlux || 1);
  if (!lightCurve) {
    return { scale, meanFlux, normalization: 1, minFlux: meanFlux, maxFlux: meanFlux };
  }

  const cached = lightCurve.amplitudeScaleStats;
  if (cached?.scale === scale) return cached;

  const samples = lightCurve.amplitudeSourceFluxes || lightCurve.waveform;
  let normalization = 1;
  let minFlux = Infinity;
  let maxFlux = -Infinity;
  if (samples?.length) {
    let sumScaledRatio = 0;
    for (const sampleFlux of samples) {
      sumScaledRatio += amplitudeFluxRatio(sampleFlux, meanFlux) ** scale;
    }
    normalization = Math.max(0.000001, sumScaledRatio / samples.length);

    for (const sampleFlux of samples) {
      const scaledFlux = (meanFlux * amplitudeFluxRatio(sampleFlux, meanFlux) ** scale) / normalization;
      minFlux = Math.min(minFlux, scaledFlux);
      maxFlux = Math.max(maxFlux, scaledFlux);
    }
  }

  if (!Number.isFinite(minFlux) || !Number.isFinite(maxFlux)) {
    minFlux = meanFlux;
    maxFlux = meanFlux;
  }

  const stats = { scale, meanFlux, normalization, minFlux, maxFlux };
  lightCurve.amplitudeScaleStats = stats;
  return stats;
}

function pulsationAmplitudeScaledFlux(lightCurve, flux) {
  if (!Number.isFinite(flux)) return lightCurve?.meanFlux || 1;
  const scale = clampPulsationAmplitudeScale(state.pulsationAmplitudeScale);
  const stats = lightCurveAmplitudeScaleStats(lightCurve, scale);
  return (stats.meanFlux * amplitudeFluxRatio(flux, stats.meanFlux) ** scale) / stats.normalization;
}

function pulsationAmplitudeScaledMaxFlux(lightCurve) {
  return lightCurveAmplitudeScaleStats(lightCurve).maxFlux;
}

function softVisualPulse(pulse) {
  const value = Math.max(VISUAL_PULSE_LOG_FLOOR, Number.isFinite(pulse) ? pulse : 1);
  if (value >= 1) {
    return 1 + Math.log(value);
  }

  return 1 / (1 + Math.log(1 / value));
}

function lightCurveInsetDisplayValue(flux) {
  return softVisualPulse(flux);
}

function currentCatalogLogLuminosity(point) {
  if (Number.isFinite(point?.currentLogLum)) return point.currentLogLum;
  return Number.isFinite(point?.row?.[IDX.logLum]) ? point.row[IDX.logLum] : NaN;
}

function timeDomainPulseSample(point, simulationDay) {
  const lightCurve = point?.lightCurve;
  if (!lightCurve?.timeDomain || !lightCurve.components?.length) return null;
  const iMagnitudeOffset =
    miraMagnitudeOffsetAtDay(lightCurve.components, simulationDay) - (lightCurve.meanIMagnitudeOffset || 0);
  let brightnessMagnitudeOffset = iMagnitudeOffset * (lightCurve.brightnessAmplitudeScale || 1);
  let rawColorOffset = ((lightCurve.colorAmplitudeRatio || 1) - 1) * iMagnitudeOffset;
  if (lightCurve.vComponents?.length) {
    const vMagnitudeOffset =
      miraMagnitudeOffsetAtDay(lightCurve.vComponents, simulationDay) - (lightCurve.meanVMagnitudeOffset || 0);
    brightnessMagnitudeOffset = vMagnitudeOffset;
    rawColorOffset = vMagnitudeOffset - iMagnitudeOffset;
  }
  const maxColorPulseOffset =
    lightCurve.maxColorPulseOffset || maxColorPulseOffsetForRow(point?.row, lightCurve.miraVSource);
  const pulse = fluxFromMagnitudeOffset(brightnessMagnitudeOffset);
  const meanVMinusI0 = point?.vMinusI0;
  const colorOffsetBounds =
    lightCurve.colorOffsetBounds || colorPulseOffsetBoundsForRow(point?.row, meanVMinusI0, lightCurve.miraVSource);
  const colorOffset = clamp(
    rawColorOffset,
    Number.isFinite(colorOffsetBounds.min) ? colorOffsetBounds.min : -maxColorPulseOffset,
    Number.isFinite(colorOffsetBounds.max) ? colorOffsetBounds.max : maxColorPulseOffset,
  );
  const baseLogLuminosity = currentCatalogLogLuminosity(point);
  const logLuminosity = Number.isFinite(baseLogLuminosity)
    ? baseLogLuminosity - 0.4 * iMagnitudeOffset
    : NaN;
  const temperature = effectiveTemperatureForCatalogState(point.row, meanVMinusI0 + colorOffset, logLuminosity);
  const color = Number.isFinite(meanVMinusI0)
    ? Number.isFinite(temperature)
      ? colorForTemperature(temperature)
      : colorForCatalogState(point.row, meanVMinusI0, logLuminosity)
    : point?.lightCurve?.meanColor || point?.color || "#ffffff";
  return {
    pulse,
    color,
    rgb: normalizedRgbFromCssColor(color),
    colorOffset,
    logLuminosity,
    temperature,
  };
}

function pulseFactor(point, simulationDay) {
  if (pulsationTooFastForAnimation(point)) return point.lightCurve.meanFlux || 1;
  if (point?.lightCurve?.timeDomain) {
    const pulse = timeDomainPulseSample(point, simulationDay)?.pulse || point.lightCurve.meanFlux || 1;
    return pulsationAmplitudeScaledFlux(point.lightCurve, pulse);
  }
  const sample = waveformSample(point, simulationDay);
  return pulsationAmplitudeScaledFlux(point.lightCurve, interpolateSamples(point.lightCurve.waveform, sample));
}

function lightCurveAreaPulseShare(point) {
  if (point?.kind !== "catalog") return LIGHT_CURVE_AREA_PULSE_SHARE;

  const dataset = point.row?.[IDX.dataset];
  const preset = currentPulsatorPreset();
  if (dataset === 1) {
    return preset === "rrlyrae" ? RR_LYRAE_PRESET_AREA_PULSE_SHARE : RR_LYRAE_AREA_PULSE_SHARE;
  }
  if (CEPHEID_DATASET_KEYS.includes(DATASET_KEYS[dataset]) && preset === "cepheids") {
    return CEPHEID_PRESET_AREA_PULSE_SHARE;
  }
  if (DATASET_KEYS[dataset] === "miras" && preset === "miras") {
    return MIRA_PRESET_AREA_PULSE_SHARE;
  }
  return LIGHT_CURVE_AREA_PULSE_SHARE;
}

function lightCurvePulseShares(point) {
  const areaShare = clamp(lightCurveAreaPulseShare(point), 0, 1);
  return {
    areaShare,
    opacityShare: 1 - areaShare,
  };
}

function lightCurveVisualPulses(fluxPulse, point = null) {
  const pulse = softVisualPulse(fluxPulse);
  const { areaShare, opacityShare } = lightCurvePulseShares(point);
  return {
    areaPulse: pulse ** areaShare,
    opacityPulse: pulse ** opacityShare,
  };
}

function meanPulseState(point) {
  const pulse = point?.lightCurve?.meanFlux || 1;
  const visualPulses = lightCurveVisualPulses(pulse, point);
  const color = point?.lightCurve?.meanColor || point?.color || "#ffffff";
  return {
    pulse,
    areaPulse: visualPulses.areaPulse,
    opacityPulse: visualPulses.opacityPulse,
    color,
    rgb: normalizedRgbFromCssColor(color),
  };
}

function pulseState(point, simulationDay) {
  if (pulsationTooFastForAnimation(point)) return meanPulseState(point);
  if (point?.lightCurve?.timeDomain) {
    const current = timeDomainPulseSample(point, simulationDay);
    if (current) {
      const pulse = pulsationAmplitudeScaledFlux(point.lightCurve, current.pulse);
      const visualPulses = lightCurveVisualPulses(pulse, point);
      return {
        pulse,
        areaPulse: visualPulses.areaPulse,
        opacityPulse: visualPulses.opacityPulse,
        color: current.color,
        rgb: current.rgb,
      };
    }
  }
  const sample = waveformSample(point, simulationDay);
  const colorIndex = sample.fraction < 0.5 ? sample.index : sample.next;
  const pulse = pulsationAmplitudeScaledFlux(point.lightCurve, interpolateSamples(point.lightCurve.waveform, sample));
  const visualPulses = lightCurveVisualPulses(pulse, point);
  return {
    pulse,
    areaPulse: visualPulses.areaPulse,
    opacityPulse: visualPulses.opacityPulse,
    color: point.lightCurve.colors[colorIndex],
    rgbArray: point.lightCurve.rgbColors,
    rgbOffset: colorIndex * 3,
  };
}

function vMinusIPulseRangeForTarget(target) {
  if (!target?.lightCurve?.colorOffsets || !Number.isFinite(target.vMinusI0)) return null;

  let minOffset = Infinity;
  let maxOffset = -Infinity;
  for (const offset of target.lightCurve.colorOffsets) {
    if (!Number.isFinite(offset)) continue;
    minOffset = Math.min(minOffset, offset);
    maxOffset = Math.max(maxOffset, offset);
  }
  if (!Number.isFinite(minOffset) || !Number.isFinite(maxOffset)) return null;

  return {
    min: target.vMinusI0 + minOffset,
    max: target.vMinusI0 + maxOffset,
  };
}

function temperaturePulseRangeForTarget(target) {
  if (!target?.lightCurve?.colorOffsets || !Number.isFinite(target.vMinusI0)) return null;

  let minTemperature = Infinity;
  let maxTemperature = -Infinity;
  const temperatures = target.lightCurve.temperatures;
  if (temperatures?.length) {
    for (const temperature of temperatures) {
      if (!Number.isFinite(temperature)) continue;
      minTemperature = Math.min(minTemperature, temperature);
      maxTemperature = Math.max(maxTemperature, temperature);
    }
    if (Number.isFinite(minTemperature) && Number.isFinite(maxTemperature)) {
      return {
        min: minTemperature,
        max: maxTemperature,
      };
    }
  }

  const logLuminosities = target.lightCurve.logLuminosities;
  for (let index = 0; index < target.lightCurve.colorOffsets.length; index += 1) {
    const offset = target.lightCurve.colorOffsets[index];
    if (!Number.isFinite(offset)) continue;
    const logLuminosity = Number.isFinite(logLuminosities?.[index])
      ? logLuminosities[index]
      : currentCatalogLogLuminosity(target);
    const temperature = effectiveTemperatureForCatalogState(
      target.row,
      target.vMinusI0 + offset,
      logLuminosity,
    );
    if (!Number.isFinite(temperature)) continue;
    minTemperature = Math.min(minTemperature, temperature);
    maxTemperature = Math.max(maxTemperature, temperature);
  }
  if (!Number.isFinite(minTemperature) || !Number.isFinite(maxTemperature)) return null;

  return {
    min: minTemperature,
    max: maxTemperature,
  };
}

function createSvgElement(name) {
  return document.createElementNS(SVG_NS, name);
}

function lightCurveInsetCycles(point) {
  return point?.lightCurve?.timeDomain ? MIRA_LIGHTCURVE_INSET_CYCLES : LIGHTCURVE_INSET_CYCLES;
}

function lightCurveInsetFluxRange(lightCurve, values = null) {
  let minFlux = Infinity;
  let maxFlux = -Infinity;
  if (values) {
    for (const value of values) {
      if (!Number.isFinite(value)) continue;
      const displayValue = lightCurveInsetDisplayValue(value);
      minFlux = Math.min(minFlux, displayValue);
      maxFlux = Math.max(maxFlux, displayValue);
    }
  } else {
    minFlux = lightCurveInsetDisplayValue(lightCurve.minFlux);
    maxFlux = lightCurveInsetDisplayValue(lightCurve.maxFlux);
  }
  if (!Number.isFinite(minFlux) || !Number.isFinite(maxFlux)) {
    minFlux = 0.8;
    maxFlux = 1.2;
  }
  const range = Math.max(0.001, maxFlux - minFlux);
  const padding = Math.max(range * 0.12, 0.035);
  return {
    minFlux: Math.max(0.001, minFlux - padding),
    maxFlux: maxFlux + padding,
  };
}

function lightCurveY(lightCurve, flux, height, padY, fluxRange = null) {
  const rangeValues = fluxRange || lightCurveInsetFluxRange(lightCurve);
  const minFlux = rangeValues.minFlux;
  const maxFlux = rangeValues.maxFlux;
  const range = Math.max(0.001, maxFlux - minFlux);
  const normalized = (lightCurveInsetDisplayValue(flux) - minFlux) / range;
  return padY + (1 - normalized) * (height - padY * 2);
}

function timeDomainInsetWindow(point, simulationDay) {
  const cycles = lightCurveInsetCycles(point);
  const period = pulsationPeriodDays(point);
  const startDay = simulationDay - (cycles * period) / 2;
  const sampleCount = Math.max(WAVEFORM_SAMPLES * cycles, 160);
  const fluxes = new Float32Array(sampleCount + 1);
  for (let index = 0; index <= sampleCount; index += 1) {
    const fraction = index / sampleCount;
    const day = startDay + fraction * cycles * period;
    const rawFlux = timeDomainPulseSample(point, day)?.pulse || point.lightCurve.meanFlux || 1;
    fluxes[index] = rawFlux;
  }
  const currentFlux = timeDomainPulseSample(point, simulationDay)?.pulse || point.lightCurve.meanFlux || 1;
  return {
    cycles,
    startDay,
    fluxes,
    currentFraction: 0.5,
    currentFlux,
    fluxRange: lightCurveInsetFluxRange(point.lightCurve, fluxes),
  };
}

function lightCurvePath(point, width, height, padX, padY, window = null) {
  const samples = point.lightCurve.waveform;
  const plotWidth = width - padX * 2;
  const commands = [];
  if (point.lightCurve?.timeDomain) {
    const insetWindow = window || timeDomainInsetWindow(point, currentSimulationDay());
    const totalSamples = insetWindow.fluxes.length - 1;
    for (let index = 0; index <= totalSamples; index += 1) {
      const fraction = index / totalSamples;
      const x = padX + fraction * plotWidth;
      const y = lightCurveY(point.lightCurve, insetWindow.fluxes[index], height, padY, insetWindow.fluxRange);
      commands.push(`${index === 0 ? "M" : "L"}${x.toFixed(2)} ${y.toFixed(2)}`);
    }
    return commands.join(" ");
  }
  const cycles = lightCurveInsetCycles(point);
  const totalSamples = samples.length * cycles;
  for (let index = 0; index <= totalSamples; index += 1) {
    const phase = index / totalSamples;
    const x = padX + phase * plotWidth;
    const y = lightCurveY(
      point.lightCurve,
      samples[index % samples.length],
      height,
      padY,
    );
    commands.push(`${index === 0 ? "M" : "L"}${x.toFixed(2)} ${y.toFixed(2)}`);
  }
  return commands.join(" ");
}

function createLightCurveInset(target) {
  const isTimeDomain = Boolean(target.lightCurve?.timeDomain);
  const width = isTimeDomain ? 220 : 164;
  const height = isTimeDomain ? 58 : 52;
  const padX = 8;
  const padY = 7;
  const inset = document.createElement("div");
  inset.className = "lightcurveInset";
  if (isTimeDomain) {
    inset.classList.add("miraLightcurveInset");
  }
  inset.title = isTimeDomain
    ? "V-band flux from the fitted Mira multi-period model over ten primary cycles"
    : "V-band flux from I-band light-curve shape over one pulsation period";

  const svg = createSvgElement("svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Target V-band lightcurve");

  const midLine = createSvgElement("line");
  midLine.classList.add("lightcurveGrid");
  midLine.setAttribute("x1", String(padX));
  midLine.setAttribute("x2", String(width - padX));
  midLine.setAttribute("y1", String(height / 2));
  midLine.setAttribute("y2", String(height / 2));

  const cycleLine = createSvgElement("line");
  cycleLine.classList.add("lightcurveGrid");
  cycleLine.setAttribute("x1", String(width / 2));
  cycleLine.setAttribute("x2", String(width / 2));
  cycleLine.setAttribute("y1", String(padY - 1));
  cycleLine.setAttribute("y2", String(height - padY + 1));

  const trace = createSvgElement("path");
  trace.classList.add("lightcurveTrace");
  trace.setAttribute("d", lightCurvePath(target, width, height, padX, padY));
  trace.style.stroke = target.color;

  const phaseMarkers = [];
  const phaseDots = [];
  const markerCount = isTimeDomain ? 1 : lightCurveInsetCycles(target);
  for (let cycle = 0; cycle < markerCount; cycle += 1) {
    const phaseMarker = createSvgElement("line");
    phaseMarker.classList.add("lightcurvePhase");
    phaseMarker.setAttribute("y1", String(padY - 1));
    phaseMarker.setAttribute("y2", String(height - padY + 1));

    const phaseDot = createSvgElement("circle");
    phaseDot.classList.add("lightcurveDot");
    phaseDot.setAttribute("r", "2.5");

    phaseMarkers.push(phaseMarker);
    phaseDots.push(phaseDot);
  }

  if (isTimeDomain) {
    svg.append(midLine, trace, ...phaseMarkers, ...phaseDots);
  } else {
    svg.append(midLine, cycleLine, trace, ...phaseMarkers, ...phaseDots);
  }
  inset.append(svg);

  activeLightcurveInsets.push({
    target,
    trace,
    phaseMarkers,
    phaseDots,
    width,
    height,
    padX,
    padY,
  });
  updateLightcurveInset();
  return inset;
}

function clearActiveLightcurveInsets() {
  activeLightcurveInsets = [];
}

function updateLightcurveInset() {
  if (!activeLightcurveInsets.length) return;

  for (const activeLightcurveInset of activeLightcurveInsets) {
    const { target, trace, phaseMarkers, phaseDots, width, height, padX, padY } = activeLightcurveInset;
    const simulationDay = lightCurveInsetSampleDay(target);
    const sample = waveformSample(target, simulationDay);
    const currentPulse = pulseState(target, simulationDay);
    const flux = interpolateSamples(target.lightCurve.waveform, sample);
    if (target.lightCurve?.timeDomain) {
      const insetWindow = timeDomainInsetWindow(target, simulationDay);
      trace.setAttribute("d", lightCurvePath(target, width, height, padX, padY, insetWindow));
      const x = padX + insetWindow.currentFraction * (width - padX * 2);
      const y = lightCurveY(target.lightCurve, insetWindow.currentFlux, height, padY, insetWindow.fluxRange);
      phaseMarkers[0].setAttribute("x1", x.toFixed(2));
      phaseMarkers[0].setAttribute("x2", x.toFixed(2));
      phaseDots[0].setAttribute("cx", x.toFixed(2));
      phaseDots[0].setAttribute("cy", y.toFixed(2));
      phaseDots[0].style.fill = currentPulse.color;
      continue;
    } else {
      trace.setAttribute("d", lightCurvePath(target, width, height, padX, padY));
    }

    const cycleWidth = (width - padX * 2) / lightCurveInsetCycles(target);
    const y = lightCurveY(target.lightCurve, flux, height, padY);
    for (let cycle = 0; cycle < lightCurveInsetCycles(target); cycle += 1) {
      const x = padX + (cycle + sample.phase) * cycleWidth;
      phaseMarkers[cycle].setAttribute("x1", x.toFixed(2));
      phaseMarkers[cycle].setAttribute("x2", x.toFixed(2));
      phaseDots[cycle].setAttribute("cx", x.toFixed(2));
      phaseDots[cycle].setAttribute("cy", y.toFixed(2));
      phaseDots[cycle].style.fill = currentPulse.color;
    }
  }
}

function clusterHrExpandedRange(min, max, minSpan, hardMin, hardMax) {
  if (!Number.isFinite(min) || !Number.isFinite(max)) {
    return [hardMin, hardMax];
  }
  let low = Math.min(min, max);
  let high = Math.max(min, max);
  const span = Math.max(high - low, minSpan);
  low -= span * 0.08;
  high += span * 0.08;
  if (high - low < minSpan) {
    const center = (low + high) / 2;
    low = center - minSpan / 2;
    high = center + minSpan / 2;
  }
  if (low < hardMin) {
    high += hardMin - low;
    low = hardMin;
  }
  if (high > hardMax) {
    low -= high - hardMax;
    high = hardMax;
  }
  return [Math.max(hardMin, low), Math.min(hardMax, high)];
}

function clusterHrTicks(min, max, count) {
  if (!Number.isFinite(min) || !Number.isFinite(max) || count <= 1) return [];
  const ticks = [];
  for (let index = 0; index < count; index += 1) {
    ticks.push(min + ((max - min) * index) / (count - 1));
  }
  return ticks;
}

function clusterHrTickLabel(value) {
  const rounded = Math.round(value * 10) / 10;
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1);
}

function clusterHrTemperatureTickLabel(value) {
  if (!Number.isFinite(value)) return "";
  const rounded = value >= 10000 ? Math.round(value / 1000) * 1000 : Math.round(value / 100) * 100;
  return formatInteger(rounded);
}

function clusterHrStarsForTarget(target) {
  if (!target) return [];
  if (Array.isArray(target.clusterStars)) return target.clusterStars;
  const stars = scene.clusterStarsByCluster.get(target.index) || [];
  target.clusterStars = stars;
  return stars;
}

function sampledClusterHrStars(stars, limit = 1600) {
  if (stars.length <= limit) return stars;
  const brightLimit = Math.min(320, Math.floor(limit * 0.25));
  const selected = new Set(
    [...stars]
      .sort((left, right) => (right.row[CS.logLum] || 0) - (left.row[CS.logLum] || 0))
      .slice(0, brightLimit),
  );
  const remaining = Math.max(1, limit - selected.size);
  const stride = Math.max(1, Math.ceil(stars.length / remaining));
  for (let index = 0; index < stars.length && selected.size < limit; index += stride) {
    selected.add(stars[index]);
  }
  return [...selected];
}

function clusterHrPointRadius(radiusSolar, radiusMin, radiusMax, { faint = false } = {}) {
  const safeRadius = Math.max(0.02, Number.isFinite(radiusSolar) ? radiusSolar : radiusMin);
  const safeMin = Math.max(0.02, Number.isFinite(radiusMin) ? radiusMin : 0.1);
  const safeMax = Math.max(safeMin * 1.05, Number.isFinite(radiusMax) ? radiusMax : safeMin * 8);
  const low = Math.log10(safeMin);
  const high = Math.log10(safeMax);
  const level = high > low ? clamp((Math.log10(safeRadius) - low) / (high - low), 0, 1) : 0.5;
  return faint ? 0.42 + level * 1.15 : 0.72 + level * 2.55;
}

function clusterHrJitterUnit(seed) {
  const raw = Math.sin(seed * 12.9898) * 43758.5453;
  return raw - Math.floor(raw);
}

function clusterHrBinSampleCount(bin, totalCount, budget) {
  const count = Math.max(0, Math.floor(bin.count || 0));
  if (!count) return 0;
  if (totalCount <= budget) return count;
  return Math.min(count, Math.max(1, Math.round((count / totalCount) * budget)));
}

function createClusterHrDiagram(target) {
  const stars = clusterHrStarsForTarget(target);
  const hrBins = target.hrBins || [];
  let temperatureMin = Infinity;
  let temperatureMax = -Infinity;
  let logLumMin = Infinity;
  let logLumMax = -Infinity;
  let radiusMin = Infinity;
  let radiusMax = -Infinity;

  for (const star of stars) {
    const temperature = star.row[CS.temperature];
    const logLum = star.row[CS.logLum];
    const radius = star.row[CS.radius];
    if (!Number.isFinite(temperature) || !Number.isFinite(logLum)) continue;
    temperatureMin = Math.min(temperatureMin, temperature);
    temperatureMax = Math.max(temperatureMax, temperature);
    logLumMin = Math.min(logLumMin, logLum);
    logLumMax = Math.max(logLumMax, logLum);
    if (Number.isFinite(radius)) {
      radiusMin = Math.min(radiusMin, radius);
      radiusMax = Math.max(radiusMax, radius);
    }
  }
  for (const bin of hrBins) {
    if (!Number.isFinite(bin.temperature) || !Number.isFinite(bin.logLum)) continue;
    temperatureMin = Math.min(temperatureMin, bin.temperature);
    temperatureMax = Math.max(temperatureMax, bin.temperature);
    logLumMin = Math.min(logLumMin, bin.logLum);
    logLumMax = Math.max(logLumMax, bin.logLum);
    if (Number.isFinite(bin.radius)) {
      radiusMin = Math.min(radiusMin, bin.radius);
      radiusMax = Math.max(radiusMax, bin.radius);
    }
  }

  if (!Number.isFinite(temperatureMin) || !Number.isFinite(logLumMin)) return null;

  const width = 278;
  const height = 184;
  const padLeft = 38;
  const padRight = 11;
  const padTop = 12;
  const padBottom = 30;
  const plotWidth = width - padLeft - padRight;
  const plotHeight = height - padTop - padBottom;
  const [xMin, xMax] = clusterHrExpandedRange(temperatureMin, temperatureMax, 2200, 2500, 40000);
  const [yMin, yMax] = clusterHrExpandedRange(logLumMin, logLumMax, 1.6, -2.1, 6.2);
  const xForTemperature = (temperature) => padLeft + (1 - (temperature - xMin) / (xMax - xMin)) * plotWidth;
  const yForLogLum = (logLum) => padTop + (1 - (logLum - yMin) / (yMax - yMin)) * plotHeight;

  const diagram = document.createElement("div");
  diagram.className = "clusterHrDiagram";

  const svg = createSvgElement("svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Synthetic cluster HR diagram");

  const plot = createSvgElement("rect");
  plot.classList.add("clusterHrPlot");
  plot.setAttribute("x", String(padLeft));
  plot.setAttribute("y", String(padTop));
  plot.setAttribute("width", String(plotWidth));
  plot.setAttribute("height", String(plotHeight));

  const gridGroup = createSvgElement("g");
  const axisGroup = createSvgElement("g");
  const xTicks = clusterHrTicks(xMin, xMax, 4);
  const yTicks = clusterHrTicks(yMin, yMax, 4);
  for (const tick of xTicks) {
    const x = xForTemperature(tick);
    const line = createSvgElement("line");
    line.classList.add("clusterHrGrid");
    line.setAttribute("x1", x.toFixed(2));
    line.setAttribute("x2", x.toFixed(2));
    line.setAttribute("y1", String(padTop));
    line.setAttribute("y2", String(padTop + plotHeight));
    gridGroup.append(line);

    const label = createSvgElement("text");
    label.classList.add("clusterHrTick");
    label.setAttribute("x", x.toFixed(2));
    label.setAttribute("y", String(height - 13));
    label.setAttribute("text-anchor", "middle");
    label.textContent = clusterHrTemperatureTickLabel(tick);
    axisGroup.append(label);
  }
  for (const tick of yTicks) {
    const y = yForLogLum(tick);
    const line = createSvgElement("line");
    line.classList.add("clusterHrGrid");
    line.setAttribute("x1", String(padLeft));
    line.setAttribute("x2", String(padLeft + plotWidth));
    line.setAttribute("y1", y.toFixed(2));
    line.setAttribute("y2", y.toFixed(2));
    gridGroup.append(line);

    const label = createSvgElement("text");
    label.classList.add("clusterHrTick");
    label.setAttribute("x", String(padLeft - 6));
    label.setAttribute("y", (y + 3).toFixed(2));
    label.setAttribute("text-anchor", "end");
    label.textContent = clusterHrTickLabel(tick);
    axisGroup.append(label);
  }

  const xLabel = createSvgElement("text");
  xLabel.classList.add("clusterHrLabel");
  xLabel.setAttribute("x", String(padLeft + plotWidth / 2));
  xLabel.setAttribute("y", String(height - 2));
  xLabel.setAttribute("text-anchor", "middle");
  xLabel.textContent = "Teff [K]";

  const yLabel = createSvgElement("text");
  yLabel.classList.add("clusterHrLabel");
  yLabel.setAttribute("x", "9");
  yLabel.setAttribute("y", String(padTop + plotHeight / 2));
  yLabel.setAttribute("text-anchor", "middle");
  yLabel.setAttribute("transform", `rotate(-90 9 ${padTop + plotHeight / 2})`);
  yLabel.textContent = "log L_I [Lsun]";
  axisGroup.append(xLabel, yLabel);

  const binGroup = createSvgElement("g");
  const totalBinCount = hrBins.reduce((total, bin) => total + Math.max(0, Math.floor(bin.count || 0)), 0);
  const binBudget = 1200;
  for (let binIndex = 0; binIndex < hrBins.length; binIndex += 1) {
    const bin = hrBins[binIndex];
    if (!Number.isFinite(bin.temperature) || !Number.isFinite(bin.logLum)) continue;
    const sampleCount = clusterHrBinSampleCount(bin, totalBinCount, binBudget);
    const opacity = totalBinCount > binBudget ? 0.34 : 0.42;
    for (let sample = 0; sample < sampleCount; sample += 1) {
      const seed = (target.index + 1) * 104729 + (binIndex + 1) * 577 + (sample + 1) * 37;
      const temperatureJitter = (clusterHrJitterUnit(seed) - 0.5) * 0.038;
      const logLumJitter = (clusterHrJitterUnit(seed + 17) - 0.5) * 0.11;
      const radiusJitter = 1 + (clusterHrJitterUnit(seed + 31) - 0.5) * 0.18;
      const temperature = clamp(bin.temperature * (1 + temperatureJitter), xMin, xMax);
      const logLum = clamp(bin.logLum + logLumJitter, yMin, yMax);
      const radius = Number.isFinite(bin.radius) ? bin.radius * radiusJitter : radiusMin;
      const circle = createSvgElement("circle");
      circle.classList.add("clusterHrBin");
      circle.setAttribute("cx", xForTemperature(temperature).toFixed(2));
      circle.setAttribute("cy", yForLogLum(logLum).toFixed(2));
      circle.setAttribute("r", clusterHrPointRadius(radius, radiusMin, radiusMax, { faint: true }).toFixed(2));
      circle.style.fill = bin.color;
      circle.style.opacity = String(opacity);
      binGroup.append(circle);
    }
  }

  const starGroup = createSvgElement("g");
  const displayStars = sampledClusterHrStars(stars);
  const starOpacity = displayStars.length > 900 ? 0.62 : 0.78;
  for (const star of displayStars) {
    const temperature = star.row[CS.temperature];
    const logLum = star.row[CS.logLum];
    const radius = star.row[CS.radius];
    if (!Number.isFinite(temperature) || !Number.isFinite(logLum)) continue;
    const circle = createSvgElement("circle");
    circle.classList.add("clusterHrStar");
    circle.setAttribute("cx", xForTemperature(temperature).toFixed(2));
    circle.setAttribute("cy", yForLogLum(logLum).toFixed(2));
    circle.setAttribute("r", clusterHrPointRadius(radius, radiusMin, radiusMax).toFixed(2));
    circle.style.fill = star.color;
    circle.style.opacity = String(starOpacity);
    starGroup.append(circle);
  }

  svg.append(plot, gridGroup, binGroup, starGroup, axisGroup);
  diagram.append(svg);
  return diagram;
}

function luminosityDisplayLevel(luminositySolar) {
  const ratio = Math.max(0, luminositySolar / RED_CLUMP_LUMINOSITY);
  return clamp(Math.log10(1 + ratio) / Math.log10(1 + MAX_DISPLAY_LUMINOSITY_RATIO), 0, 1.35);
}

function pointRadiusFromLuminosity(luminositySolar, projected) {
  const level = luminosityDisplayLevel(luminositySolar);
  const zoomSize = 0.78 + Math.log2(Math.max(1, effectiveZoomScale())) * 0.15;
  return clamp((0.2 + level ** 0.72 * 1.55) * zoomSize * projected.perspective, 0.22, 2.55);
}

function pointRadiusFromStellarRadius(radiusSolar, projected) {
  return pointRadiusFromStellarRadiusAtPerspective(radiusSolar, projected.perspective);
}

function pointRadiusUnitFromStellarRadius(radiusSolar) {
  const redClumpRatio = Math.max(0.03, radiusSolar / RED_CLUMP_RADIUS);
  const radiusLevel = Math.log10(1 + redClumpRatio) / Math.log10(1 + 20);
  return 0.35 + radiusLevel ** 0.75 * 3.0;
}

function pointRadiusZoomSize() {
  return 0.8 + Math.log2(Math.max(1, effectiveZoomScale())) * 0.16;
}

function pointRadiusZoomSizeForZoom(zoom = state.zoom) {
  return 0.8 + Math.log2(Math.max(1, effectiveZoomScale(zoom))) * 0.16;
}

function starRadiusZoomSizeForZoom(zoom = state.zoom) {
  const zoomSize = 0.8 + Math.log2(Math.max(1, effectiveZoomScale(zoom))) * STAR_RADIUS_ZOOM_BASE_GAIN;
  const boost = 1 + Math.min(STAR_RADIUS_ZOOM_MAX_BOOST, Math.log2(Math.max(1, zoom)) * STAR_RADIUS_ZOOM_GAIN);
  return Math.min(zoomSize * boost, STAR_RADIUS_ZOOM_SIZE_MAX) * starRadiusDeepZoomScale(zoom);
}

function starRadiusZoomSize() {
  return starRadiusZoomSizeForZoom(state.zoom);
}

function pointRadiusBaseFromStellarRadius(radiusSolar) {
  return pointRadiusUnitFromStellarRadius(radiusSolar) * starRadiusZoomSize();
}

function starBaseRadiusViewportScale() {
  return MOBILE_CONTROLS_MEDIA.matches ? MOBILE_STAR_BASE_RADIUS_SCALE : 1;
}

function pointRadiusFromUnitAtPerspective(radiusUnit, perspective, zoomSize = pointRadiusZoomSize()) {
  return clamp(radiusUnit * zoomSize * perspective, 0.35, 5.2);
}

function starRadiusFromUnitAtPerspective(radiusUnit, perspective, zoomSize = starRadiusZoomSize()) {
  return clamp(radiusUnit * zoomSize * perspective, 0.35, STAR_RADIUS_BASE_MAX) * starBaseRadiusViewportScale();
}

function starRadiusFromUnitAtPerspectiveForZoom(radiusUnit, perspective, zoom = state.zoom) {
  return starRadiusFromUnitAtPerspective(radiusUnit, perspective, starRadiusZoomSizeForZoom(zoom));
}

function pointRadiusFromStellarRadiusAtPerspective(radiusSolar, perspective, zoomSize = starRadiusZoomSize()) {
  return starRadiusFromUnitAtPerspective(pointRadiusUnitFromStellarRadius(radiusSolar), perspective, zoomSize);
}

function pointAlphaFromLuminosity(luminositySolar, projected, gain) {
  return pointAlphaFromUnit(pointAlphaUnitFromLuminosity(luminositySolar, projected), gain);
}

function pointAlphaUnitFromLuminosity(luminositySolar, projected) {
  return pointAlphaUnitFromLuminosityAtPerspective(luminositySolar, projected.perspective);
}

function pointAlphaUnitBaseFromLuminosity(luminositySolar) {
  const level = luminosityDisplayLevel(luminositySolar);
  return 0.01 + level ** 1.08 * 0.42;
}

function pointAlphaUnitFromBaseAtPerspective(alphaBaseUnit, perspective) {
  return alphaBaseUnit * (0.64 + perspective * 0.24);
}

function pointAlphaUnitFromLuminosityAtPerspective(luminositySolar, perspective) {
  return pointAlphaUnitFromBaseAtPerspective(pointAlphaUnitBaseFromLuminosity(luminositySolar), perspective);
}

function pointAlphaFromUnit(alphaUnit, gain) {
  const exposure = (gain / 10) * DISPLAY_LUMINOSITY_BASE_BOOST * alphaUnit;
  return clamp(DISPLAY_ALPHA_MAX * (1 - Math.exp(-exposure / DISPLAY_ALPHA_MAX)), 0.001, DISPLAY_ALPHA_MAX);
}

function polygonArea(points) {
  if (!Array.isArray(points) || points.length < 3) return 0;
  let area = 0;
  for (let index = 0; index < points.length; index += 1) {
    const current = points[index];
    const next = points[(index + 1) % points.length];
    area += current.x * next.y - next.x * current.y;
  }
  return Math.abs(area) * 0.5;
}

function redClumpDensityCountForPoint(point) {
  const smoothedCount = Number(point?.smoothedDensityCount);
  const count = Number.isFinite(smoothedCount) ? smoothedCount : Number(point?.row?.[RC.densityCount]);
  return Number.isFinite(count) ? Math.max(0, count) : 0;
}

function redClumpDensityAlpha(unit) {
  if (!Number.isFinite(unit)) return 1;
  return RED_CLUMP_DENSITY_ALPHA_FLOOR + (1 - RED_CLUMP_DENSITY_ALPHA_FLOOR) * clamp(unit, 0, 1) ** RED_CLUMP_DENSITY_ALPHA_POWER;
}

function smoothRedClumpField(pointByCell, point, fieldIndex) {
  const rawValue = Number(point?.row?.[fieldIndex]);
  let weightedSum = 0;
  let totalWeight = 0;
  for (let dy = -1; dy <= 1; dy += 1) {
    for (let dx = -1; dx <= 1; dx += 1) {
      const neighbor = pointByCell.get(redClumpGridKey(point.grid.x + dx, point.grid.y + dy));
      const value = Number(neighbor?.row?.[fieldIndex]);
      if (!Number.isFinite(value)) continue;
      const weight = dx === 0 && dy === 0 ? 4 : dx === 0 || dy === 0 ? 2 : 1;
      weightedSum += value * weight;
      totalWeight += weight;
    }
  }
  if (totalWeight <= 0) return rawValue;
  const smoothedValue = weightedSum / totalWeight;
  return Number.isFinite(rawValue)
    ? rawValue * (1 - RED_CLUMP_DENSITY_SMOOTHING_BLEND) +
        smoothedValue * RED_CLUMP_DENSITY_SMOOTHING_BLEND
    : smoothedValue;
}

function smoothRedClumpDensities(points) {
  const pointByCell = new Map(points.map((point) => [point.gridKey, point]));
  const smoothed = points.map((point) => ({
    count: smoothRedClumpField(pointByCell, point, RC.densityCount),
    unit: smoothRedClumpField(pointByCell, point, RC.densityUnit),
  }));

  points.forEach((point, index) => {
    const { count, unit } = smoothed[index];
    point.smoothedDensityCount = Number.isFinite(count) ? Math.max(0, count) : 0;
    point.smoothedDensityUnit = Number.isFinite(unit) ? clamp(unit, 0, 1) : 1;
    point.densityAlpha = redClumpDensityAlpha(point.smoothedDensityUnit);
  });
}

function drawDisc(x, y, radius) {
  drawDiscOnContext(ctx, x, y, radius);
}

function drawDiscOnContext(context, x, y, radius) {
  context.beginPath();
  context.arc(x, y, Math.max(0.18, radius), 0, Math.PI * 2);
  context.fill();
}

function limbDarkeningRadiusBucket(radius) {
  return Math.max(
    LIMB_DARKENING_RADIUS_MIN,
    Math.round(radius / LIMB_DARKENING_RADIUS_STEP) * LIMB_DARKENING_RADIUS_STEP,
  );
}

function limbDarkeningVisualWeight(item) {
  return item.currentRadius * item.currentRadius * item.currentAlpha;
}

function linearLimbDarkeningIntensity(radiusFraction) {
  const radius = clamp(radiusFraction, 0, 1);
  const mu = Math.sqrt(Math.max(0, 1 - radius * radius));
  return 1 - LIMB_DARKENING_LINEAR_COEFFICIENT * (1 - mu);
}

function shouldUseLimbDarkening(item) {
  if (CATALOG_LIMB_DARKEN_ALL_STARS) return true;

  if (item.currentRadius < LIMB_DARKENING_RADIUS_MIN || item.currentAlpha < LIMB_DARKENING_ALPHA_MIN) {
    return false;
  }

  const visualWeight = limbDarkeningVisualWeight(item);
  if (state.radiusScale >= LIMB_DARKENING_HIGH_RADIUS_SCALE) {
    return visualWeight >= LIMB_DARKENING_HIGH_RADIUS_VISUAL_WEIGHT_MIN;
  }
  return visualWeight >= LIMB_DARKENING_VISUAL_WEIGHT_MIN;
}

function shouldUseCanvasLimbDarkening(item) {
  return shouldUseLimbDarkening(item) && item.currentRadius >= LIMB_DARKENING_RADIUS_MIN;
}

function limbDarkenedSprite(color, radius) {
  const bucketRadius = limbDarkeningRadiusBucket(radius);
  const dpr = scene.dpr || 1;
  const rgbValue = quantizeRgb(cssColorToRgb(color), LIMB_DARKENING_COLOR_STEP);
  const key = `${rgbValue.join(",")}|${bucketRadius.toFixed(2)}|${dpr.toFixed(2)}|u${LIMB_DARKENING_LINEAR_COEFFICIENT}`;
  const cached = scene.limbSpriteCache.get(key);
  if (cached) return cached;

  if (scene.limbSpriteCache.size >= LIMB_DARKENING_CACHE_MAX) {
    const oldestKey = scene.limbSpriteCache.keys().next().value;
    if (oldestKey) {
      scene.limbSpriteCache.delete(oldestKey);
    }
  }

  const padding = Math.max(1, bucketRadius * 0.18);
  const displaySize = Math.ceil((bucketRadius + padding) * 2);
  const canvasSize = Math.max(2, Math.ceil(displaySize * dpr));
  const spriteCanvas = document.createElement("canvas");
  spriteCanvas.width = canvasSize;
  spriteCanvas.height = canvasSize;

  const spriteCtx = spriteCanvas.getContext("2d");
  spriteCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const center = displaySize / 2;
  const gradient = spriteCtx.createRadialGradient(
    center,
    center,
    0,
    center,
    center,
    bucketRadius,
  );
  for (const radiusFraction of [0, 0.42, 0.62, 0.78, 0.9, 0.97, 1]) {
    gradient.addColorStop(radiusFraction, rgbaFromRgb(rgbValue, linearLimbDarkeningIntensity(radiusFraction)));
  }

  spriteCtx.fillStyle = gradient;
  spriteCtx.beginPath();
  spriteCtx.arc(center, center, bucketRadius, 0, Math.PI * 2);
  spriteCtx.fill();

  const sprite = { canvas: spriteCanvas, size: displaySize };
  scene.limbSpriteCache.set(key, sprite);
  return sprite;
}

function drawStarOnContext(context, color, item) {
  if (!shouldUseCanvasLimbDarkening(item)) {
    drawDiscOnContext(context, item.projected.x, item.projected.y, item.currentRadius);
    return;
  }

  const sprite = limbDarkenedSprite(color, item.currentRadius);
  const halfSize = sprite.size / 2;
  context.drawImage(sprite.canvas, item.projected.x - halfSize, item.projected.y - halfSize, sprite.size, sprite.size);
}

function compileCatalogShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (gl.getShaderParameter(shader, gl.COMPILE_STATUS)) return shader;

  console.warn("Catalog WebGL shader compile failed", gl.getShaderInfoLog(shader));
  gl.deleteShader(shader);
  return null;
}

function createCatalogProgram(gl) {
  const vertexShader = compileCatalogShader(
    gl,
    gl.VERTEX_SHADER,
    `
      attribute vec2 a_position;
      attribute float a_radius;
      attribute vec3 a_color;
      attribute float a_alpha;
      attribute float a_limb;

      uniform vec2 u_resolution;
      uniform float u_dpr;

      varying vec3 v_color;
      varying float v_alpha;
      varying float v_limb;

      void main() {
        vec2 clip = (a_position / u_resolution) * 2.0 - 1.0;
        gl_Position = vec4(clip.x, -clip.y, 0.0, 1.0);
        gl_PointSize = max(1.0, a_radius * 2.0 * u_dpr);
        v_color = a_color;
        v_alpha = a_alpha;
        v_limb = a_limb;
      }
    `,
  );
  const fragmentShader = compileCatalogShader(
    gl,
    gl.FRAGMENT_SHADER,
    `
      precision mediump float;

      uniform float u_limbCoefficient;
      uniform float u_limbFluxNormalization;

      varying vec3 v_color;
      varying float v_alpha;
      varying float v_limb;

      void main() {
        vec2 uv = gl_PointCoord * 2.0 - 1.0;
        float radiusSquared = dot(uv, uv);
        if (radiusSquared > 1.0) discard;

        float edgeAlpha = 1.0 - smoothstep(0.94, 1.0, radiusSquared);
        float intensity = 1.0;
        if (v_limb > 0.5) {
          float mu = sqrt(max(0.0, 1.0 - radiusSquared));
          intensity = (1.0 - u_limbCoefficient * (1.0 - mu)) * u_limbFluxNormalization;
        }

        float alpha = clamp(v_alpha * edgeAlpha * intensity, 0.0, 1.0);
        gl_FragColor = vec4(v_color * alpha, alpha);
      }
    `,
  );
  if (!vertexShader || !fragmentShader) return null;

  const program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  gl.deleteShader(vertexShader);
  gl.deleteShader(fragmentShader);
  if (gl.getProgramParameter(program, gl.LINK_STATUS)) return program;

  console.warn("Catalog WebGL program link failed", gl.getProgramInfoLog(program));
  gl.deleteProgram(program);
  return null;
}

function createCatalogDynamicProgram(gl) {
  const vertexShader = compileCatalogShader(
    gl,
    gl.VERTEX_SHADER,
    `
      precision highp float;

      attribute vec3 a_position;
      attribute vec4 a_static0;
      attribute float a_lodAlpha;
      attribute vec2 a_pulse;
      attribute vec3 a_color;

      uniform vec2 u_resolution;
      uniform vec2 u_center;
      uniform vec4 u_yawPitch;
      uniform vec2 u_roll;
      uniform float u_scale;
      uniform float u_depthScale;
      uniform float u_dpr;
      uniform float u_radiusZoomSize;
      uniform float u_radiusScale;
      uniform float u_starBaseRadiusViewportScale;
      uniform float u_displayLuminosityBaseBoost;
      uniform float u_starAlphaHeadroomExposure;
      uniform float u_starPulseAlphaMax;
      uniform float u_starRadiusBaseMax;

      varying vec3 v_color;
      varying float v_alpha;
      varying float v_limb;

      void main() {
        float cosy = u_yawPitch.x;
        float siny = u_yawPitch.y;
        float cosp = u_yawPitch.z;
        float sinp = u_yawPitch.w;
        float cosr = u_roll.x;
        float sinr = u_roll.y;
        float depthZ = a_position.z * u_depthScale;

        float x1 = a_position.x * cosy - depthZ * siny;
        float z1 = a_position.x * siny + depthZ * cosy;
        float y1 = a_position.y * cosp - z1 * sinp;
        float z2 = a_position.y * sinp + z1 * cosp;
        float x2 = x1 * cosr - y1 * sinr;
        float y2 = x1 * sinr + y1 * cosr;
        float perspective = clamp(140.0 / (140.0 - z2), 0.45, 2.2);
        vec2 screen = u_center + vec2(x2, -y2) * u_scale * perspective;
        vec2 clip = (screen / u_resolution) * 2.0 - 1.0;
        float radiusUnit = a_static0.x;
        float alphaBaseUnit = a_static0.y;
        float pulseSafeAlpha = a_static0.z;
        float exposureGain = a_static0.w;
        float areaPulse = a_pulse.x;
        float opacityPulse = a_pulse.y;

        float baseRadius = clamp(
          radiusUnit * u_radiusZoomSize * perspective,
          0.35,
          u_starRadiusBaseMax
        ) * u_starBaseRadiusViewportScale;
        float radius = clamp(
          baseRadius *
            ${PULSATOR_RADIUS_BASE_SCALE.toFixed(6)} *
            ${PULSATOR_BASE_RADIUS_FACTOR.toFixed(2)} *
            u_radiusScale *
            sqrt(max(0.000001, areaPulse)),
          0.18,
          28.0
        );
        float alphaUnit = alphaBaseUnit * (0.64 + perspective * 0.24);
        float exposure = (exposureGain / 10.0) * u_displayLuminosityBaseBoost * alphaUnit;
        float baseAlphaWithPulseHeadroom =
          pulseSafeAlpha * (1.0 - exp(-exposure / u_starAlphaHeadroomExposure));
        float alpha = clamp(
          baseAlphaWithPulseHeadroom * opacityPulse,
          0.0005,
          u_starPulseAlphaMax
        ) * a_lodAlpha;
        float highRadiusScale = step(${LIMB_DARKENING_HIGH_RADIUS_SCALE.toFixed(4)}, u_radiusScale);
        float limbVisualWeightMin = mix(
          ${LIMB_DARKENING_VISUAL_WEIGHT_MIN.toFixed(4)},
          ${LIMB_DARKENING_HIGH_RADIUS_VISUAL_WEIGHT_MIN.toFixed(4)},
          highRadiusScale
        );
        float visualWeight = radius * radius * alpha;
        float limb =
          ${CATALOG_LIMB_DARKEN_ALL_STARS ? "1.0" : "0.0"} *
          step(${LIMB_DARKENING_RADIUS_MIN.toFixed(4)}, radius) *
          step(${LIMB_DARKENING_ALPHA_MIN.toFixed(4)}, alpha) *
          step(limbVisualWeightMin, visualWeight);

        gl_Position = vec4(clip.x, -clip.y, 0.0, 1.0);
        gl_PointSize = max(1.0, radius * 2.0 * u_dpr);
        v_color = a_color;
        v_alpha = alpha;
        v_limb = limb;
      }
    `,
  );
  const fragmentShader = compileCatalogShader(
    gl,
    gl.FRAGMENT_SHADER,
    `
      precision mediump float;

      uniform float u_limbCoefficient;
      uniform float u_limbFluxNormalization;

      varying vec3 v_color;
      varying float v_alpha;
      varying float v_limb;

      void main() {
        vec2 uv = gl_PointCoord * 2.0 - 1.0;
        float radiusSquared = dot(uv, uv);
        if (radiusSquared > 1.0) discard;

        float edgeAlpha = 1.0 - smoothstep(0.94, 1.0, radiusSquared);
        float intensity = 1.0;
        if (v_limb > 0.5) {
          float mu = sqrt(max(0.0, 1.0 - radiusSquared));
          intensity = (1.0 - u_limbCoefficient * (1.0 - mu)) * u_limbFluxNormalization;
        }

        float alpha = clamp(v_alpha * edgeAlpha * intensity, 0.0, 1.0);
        gl_FragColor = vec4(v_color * alpha, alpha);
      }
    `,
  );
  if (!vertexShader || !fragmentShader) return null;

  const program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  gl.deleteShader(vertexShader);
  gl.deleteShader(fragmentShader);
  if (gl.getProgramParameter(program, gl.LINK_STATUS)) return program;

  console.warn("Dynamic catalog WebGL program link failed", gl.getProgramInfoLog(program));
  gl.deleteProgram(program);
  return null;
}

function createClusterStarProgram(gl) {
  const vertexShader = compileCatalogShader(
    gl,
    gl.VERTEX_SHADER,
    `
      precision highp float;

      attribute vec3 a_position;
      attribute float a_radiusUnit;
      attribute float a_alphaBaseUnit;
      attribute float a_lodAlpha;
      attribute vec3 a_color;

      uniform vec2 u_resolution;
      uniform vec2 u_center;
      uniform vec4 u_yawPitch;
      uniform vec2 u_roll;
      uniform float u_scale;
      uniform float u_depthScale;
      uniform float u_dpr;
      uniform float u_radiusZoomSize;
      uniform float u_radiusScale;
      uniform float u_starBaseRadiusViewportScale;
      uniform float u_exposure;
      uniform float u_displayLuminosityBaseBoost;
      uniform float u_starAlphaHeadroomExposure;
      uniform float u_starPulseAlphaMax;
      uniform float u_starRadiusBaseMax;

      varying vec3 v_color;
      varying float v_alpha;

      void main() {
        float cosy = u_yawPitch.x;
        float siny = u_yawPitch.y;
        float cosp = u_yawPitch.z;
        float sinp = u_yawPitch.w;
        float cosr = u_roll.x;
        float sinr = u_roll.y;
        float depthZ = a_position.z * u_depthScale;

        float x1 = a_position.x * cosy - depthZ * siny;
        float z1 = a_position.x * siny + depthZ * cosy;
        float y1 = a_position.y * cosp - z1 * sinp;
        float z2 = a_position.y * sinp + z1 * cosp;
        float x2 = x1 * cosr - y1 * sinr;
        float y2 = x1 * sinr + y1 * cosr;
        float perspective = clamp(140.0 / (140.0 - z2), 0.45, 2.2);
        vec2 screen = u_center + vec2(x2, -y2) * u_scale * perspective;
        vec2 clip = (screen / u_resolution) * 2.0 - 1.0;

        float baseRadius = clamp(
          a_radiusUnit * u_radiusZoomSize * perspective,
          0.35,
          u_starRadiusBaseMax
        ) * u_starBaseRadiusViewportScale;
        float radius = clamp(
          baseRadius * ${PULSATOR_RADIUS_BASE_SCALE.toFixed(6)} * ${PULSATOR_BASE_RADIUS_FACTOR.toFixed(2)} * u_radiusScale,
          0.18,
          28.0
        );
        float alphaUnit = a_alphaBaseUnit * (0.64 + perspective * 0.24);
        float exposure = (u_exposure / 10.0) * u_displayLuminosityBaseBoost * alphaUnit;
        float alpha = clamp(
          u_starPulseAlphaMax * (1.0 - exp(-exposure / u_starAlphaHeadroomExposure)),
          0.0005,
          u_starPulseAlphaMax
        ) * a_lodAlpha;

        gl_Position = vec4(clip.x, -clip.y, 0.0, 1.0);
        gl_PointSize = max(1.0, radius * 2.0 * u_dpr);
        v_color = a_color;
        v_alpha = alpha;
      }
    `,
  );
  const fragmentShader = compileCatalogShader(
    gl,
    gl.FRAGMENT_SHADER,
    `
      precision mediump float;

      varying vec3 v_color;
      varying float v_alpha;

      void main() {
        vec2 uv = gl_PointCoord * 2.0 - 1.0;
        float radiusSquared = dot(uv, uv);
        if (radiusSquared > 1.0) discard;

        float edgeAlpha = 1.0 - smoothstep(0.94, 1.0, radiusSquared);
        float alpha = clamp(v_alpha * edgeAlpha, 0.0, 1.0);
        gl_FragColor = vec4(v_color * alpha, alpha);
      }
    `,
  );
  if (!vertexShader || !fragmentShader) return null;

  const program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  gl.deleteShader(vertexShader);
  gl.deleteShader(fragmentShader);
  if (gl.getProgramParameter(program, gl.LINK_STATUS)) return program;

  console.warn("Cluster star WebGL program link failed", gl.getProgramInfoLog(program));
  gl.deleteProgram(program);
  return null;
}

function createRedClumpProgram(gl) {
  const vertexShader = compileCatalogShader(
    gl,
    gl.VERTEX_SHADER,
    `
      precision highp float;

      attribute vec3 a_position;
      attribute vec3 a_alphaFactors;

      uniform vec2 u_resolution;
      uniform vec2 u_center;
      uniform vec3 u_color;
      uniform vec4 u_yawPitch;
      uniform vec2 u_roll;
      uniform float u_scale;
      uniform float u_depthScale;
      uniform float u_density;
      uniform float u_exposure;
      uniform float u_alphaBaseUnit;
      uniform float u_displayLuminosityBaseBoost;
      uniform float u_displayAlphaMax;
      uniform float u_surfaceAlphaScale;
      uniform float u_surfaceAlphaMax;

      varying vec4 v_color;

      void main() {
        float cosy = u_yawPitch.x;
        float siny = u_yawPitch.y;
        float cosp = u_yawPitch.z;
        float sinp = u_yawPitch.w;
        float cosr = u_roll.x;
        float sinr = u_roll.y;
        float depthZ = a_position.z * u_depthScale;

        float x1 = a_position.x * cosy - depthZ * siny;
        float z1 = a_position.x * siny + depthZ * cosy;
        float y1 = a_position.y * cosp - z1 * sinp;
        float z2 = a_position.y * sinp + z1 * cosp;
        float x2 = x1 * cosr - y1 * sinr;
        float y2 = x1 * sinr + y1 * cosr;
        float perspective = clamp(140.0 / (140.0 - z2), 0.45, 2.2);
        vec2 screen = u_center + vec2(x2, -y2) * u_scale * perspective;
        vec2 clip = (screen / u_resolution) * 2.0 - 1.0;
        float alphaUnit = u_alphaBaseUnit * (0.64 + perspective * 0.24);
        float exposure = (u_exposure / 10.0) * u_displayLuminosityBaseBoost * alphaUnit;
        float pointAlpha = clamp(
          u_displayAlphaMax * (1.0 - exp(-exposure / u_displayAlphaMax)),
          0.001,
          u_displayAlphaMax
        );
        float visible = step(a_alphaFactors.z, u_density);
        float alpha = clamp(
          pointAlpha * a_alphaFactors.x * a_alphaFactors.y * u_surfaceAlphaScale,
          0.0,
          u_surfaceAlphaMax
        ) * visible;

        gl_Position = vec4(clip.x, -clip.y, 0.0, 1.0);
        v_color = vec4(u_color * alpha, alpha);
      }
    `,
  );
  const fragmentShader = compileCatalogShader(
    gl,
    gl.FRAGMENT_SHADER,
    `
      precision mediump float;

      varying vec4 v_color;

      void main() {
        gl_FragColor = v_color;
      }
    `,
  );
  if (!vertexShader || !fragmentShader) return null;

  const program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  gl.deleteShader(vertexShader);
  gl.deleteShader(fragmentShader);
  if (gl.getProgramParameter(program, gl.LINK_STATUS)) return program;

  console.warn("Red clump WebGL program link failed", gl.getProgramInfoLog(program));
  gl.deleteProgram(program);
  return null;
}

function createCatalogRenderer(canvasElement, options = {}) {
  if (!CATALOG_GPU_ENABLED || !canvasElement) return null;

  const gl = canvasElement.getContext("webgl", {
    alpha: true,
    antialias: false,
    depth: false,
    stencil: false,
    premultipliedAlpha: true,
    preserveDrawingBuffer: Boolean(options.preserveDrawingBuffer),
  });
  if (!gl) return null;

  const catalogProgram = createCatalogProgram(gl);
  if (!catalogProgram) return null;
  const catalogDynamicProgram = createCatalogDynamicProgram(gl);

  const catalogDynamicBuffer = gl.createBuffer();
  const catalogWorldStaticBuffer = catalogDynamicProgram ? gl.createBuffer() : null;
  const catalogWorldPulseBuffer = catalogDynamicProgram ? gl.createBuffer() : null;
  const catalogStaticBuffer = gl.createBuffer();
  const catalogStride = CATALOG_GPU_VERTEX_FLOATS * Float32Array.BYTES_PER_ELEMENT;
  const catalogWorldStaticStride = CATALOG_DYNAMIC_GPU_STATIC_VERTEX_FLOATS * Float32Array.BYTES_PER_ELEMENT;
  const catalogWorldPulseStride = CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS * Float32Array.BYTES_PER_ELEMENT;
  const catalogAttributes = {
    position: gl.getAttribLocation(catalogProgram, "a_position"),
    radius: gl.getAttribLocation(catalogProgram, "a_radius"),
    color: gl.getAttribLocation(catalogProgram, "a_color"),
    alpha: gl.getAttribLocation(catalogProgram, "a_alpha"),
    limb: gl.getAttribLocation(catalogProgram, "a_limb"),
  };
  const catalogUniforms = {
    resolution: gl.getUniformLocation(catalogProgram, "u_resolution"),
    dpr: gl.getUniformLocation(catalogProgram, "u_dpr"),
    limbCoefficient: gl.getUniformLocation(catalogProgram, "u_limbCoefficient"),
    limbFluxNormalization: gl.getUniformLocation(catalogProgram, "u_limbFluxNormalization"),
  };
  const catalogDynamicAttributes = catalogDynamicProgram
    ? {
        position: gl.getAttribLocation(catalogDynamicProgram, "a_position"),
        static0: gl.getAttribLocation(catalogDynamicProgram, "a_static0"),
        lodAlpha: gl.getAttribLocation(catalogDynamicProgram, "a_lodAlpha"),
        pulse: gl.getAttribLocation(catalogDynamicProgram, "a_pulse"),
        color: gl.getAttribLocation(catalogDynamicProgram, "a_color"),
      }
    : null;
  const catalogDynamicUniforms = catalogDynamicProgram
    ? {
        resolution: gl.getUniformLocation(catalogDynamicProgram, "u_resolution"),
        center: gl.getUniformLocation(catalogDynamicProgram, "u_center"),
        yawPitch: gl.getUniformLocation(catalogDynamicProgram, "u_yawPitch"),
        roll: gl.getUniformLocation(catalogDynamicProgram, "u_roll"),
        scale: gl.getUniformLocation(catalogDynamicProgram, "u_scale"),
        depthScale: gl.getUniformLocation(catalogDynamicProgram, "u_depthScale"),
        dpr: gl.getUniformLocation(catalogDynamicProgram, "u_dpr"),
        radiusZoomSize: gl.getUniformLocation(catalogDynamicProgram, "u_radiusZoomSize"),
        radiusScale: gl.getUniformLocation(catalogDynamicProgram, "u_radiusScale"),
        starBaseRadiusViewportScale: gl.getUniformLocation(
          catalogDynamicProgram,
          "u_starBaseRadiusViewportScale",
        ),
        displayLuminosityBaseBoost: gl.getUniformLocation(catalogDynamicProgram, "u_displayLuminosityBaseBoost"),
        starAlphaHeadroomExposure: gl.getUniformLocation(catalogDynamicProgram, "u_starAlphaHeadroomExposure"),
        starPulseAlphaMax: gl.getUniformLocation(catalogDynamicProgram, "u_starPulseAlphaMax"),
        starRadiusBaseMax: gl.getUniformLocation(catalogDynamicProgram, "u_starRadiusBaseMax"),
        limbCoefficient: gl.getUniformLocation(catalogDynamicProgram, "u_limbCoefficient"),
        limbFluxNormalization: gl.getUniformLocation(catalogDynamicProgram, "u_limbFluxNormalization"),
      }
    : null;
  const clusterStarProgram = createClusterStarProgram(gl);
  const clusterStarBuffer = clusterStarProgram ? gl.createBuffer() : null;
  const clusterStarStride = CLUSTER_STAR_GPU_VERTEX_FLOATS * Float32Array.BYTES_PER_ELEMENT;
  const clusterStarAttributes = clusterStarProgram
    ? {
        position: gl.getAttribLocation(clusterStarProgram, "a_position"),
        radiusUnit: gl.getAttribLocation(clusterStarProgram, "a_radiusUnit"),
        alphaBaseUnit: gl.getAttribLocation(clusterStarProgram, "a_alphaBaseUnit"),
        lodAlpha: gl.getAttribLocation(clusterStarProgram, "a_lodAlpha"),
        color: gl.getAttribLocation(clusterStarProgram, "a_color"),
      }
    : null;
  const clusterStarUniforms = clusterStarProgram
    ? {
        resolution: gl.getUniformLocation(clusterStarProgram, "u_resolution"),
        center: gl.getUniformLocation(clusterStarProgram, "u_center"),
        yawPitch: gl.getUniformLocation(clusterStarProgram, "u_yawPitch"),
        roll: gl.getUniformLocation(clusterStarProgram, "u_roll"),
        scale: gl.getUniformLocation(clusterStarProgram, "u_scale"),
        depthScale: gl.getUniformLocation(clusterStarProgram, "u_depthScale"),
        dpr: gl.getUniformLocation(clusterStarProgram, "u_dpr"),
        radiusZoomSize: gl.getUniformLocation(clusterStarProgram, "u_radiusZoomSize"),
        radiusScale: gl.getUniformLocation(clusterStarProgram, "u_radiusScale"),
        starBaseRadiusViewportScale: gl.getUniformLocation(clusterStarProgram, "u_starBaseRadiusViewportScale"),
        exposure: gl.getUniformLocation(clusterStarProgram, "u_exposure"),
        displayLuminosityBaseBoost: gl.getUniformLocation(clusterStarProgram, "u_displayLuminosityBaseBoost"),
        starAlphaHeadroomExposure: gl.getUniformLocation(clusterStarProgram, "u_starAlphaHeadroomExposure"),
        starPulseAlphaMax: gl.getUniformLocation(clusterStarProgram, "u_starPulseAlphaMax"),
        starRadiusBaseMax: gl.getUniformLocation(clusterStarProgram, "u_starRadiusBaseMax"),
      }
    : null;

  gl.disable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);

  canvasElement.addEventListener("webglcontextlost", (event) => {
    event.preventDefault();
    scene.catalogStaticRenderer = null;
    scene.catalogRenderer = null;
    markCatalogStaticDirty();
    markClusterStarGpuDirty();
  });

  return {
    mode: "gpu",
    gl,
    canvas: canvasElement,
    catalogProgram,
    catalogDynamicProgram,
    catalogDynamicBuffer,
    catalogWorldStaticBuffer,
    catalogWorldPulseBuffer,
    catalogStaticBuffer,
    catalogAttributes,
    catalogUniforms,
    catalogDynamicAttributes,
    catalogDynamicUniforms,
    clusterStarProgram,
    clusterStarBuffer,
    clusterStarAttributes,
    clusterStarUniforms,
    projectsCatalogDynamicInShader: Boolean(catalogDynamicProgram),
    projectsClusterStarsInShader: Boolean(clusterStarProgram),
    catalogDynamicCapacity: 0,
    catalogDynamicData: new Float32Array(0),
    catalogWorldStaticCapacity: 0,
    catalogWorldStaticData: new Float32Array(0),
    catalogWorldStaticCount: 0,
    catalogWorldStaticCacheVersion: -1,
    catalogWorldPulseCapacity: 0,
    catalogWorldPulseData: new Float32Array(0),
    catalogWorldPulseUploadedCount: 0,
    catalogWorldPulseCacheVersion: -1,
    catalogStaticCapacity: 0,
    catalogStaticData: new Float32Array(0),
    catalogStaticCount: 0,
    clusterStarCapacity: 0,
    clusterStarData: new Float32Array(0),
    clusterStarCount: 0,
    clusterStarSourceCount: 0,
    clusterStarCoordinateCacheKey: null,
    ensureCatalogCapacity(count) {
      if (this.catalogDynamicCapacity >= count) return this.catalogDynamicData;
      this.catalogDynamicCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, count)));
      this.catalogDynamicData = new Float32Array(this.catalogDynamicCapacity * CATALOG_GPU_VERTEX_FLOATS);
      return this.catalogDynamicData;
    },
    ensureCatalogWorldStaticCapacity(count) {
      if (this.catalogWorldStaticCapacity >= count) return this.catalogWorldStaticData;
      this.catalogWorldStaticCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, count)));
      this.catalogWorldStaticData = new Float32Array(
        this.catalogWorldStaticCapacity * CATALOG_DYNAMIC_GPU_STATIC_VERTEX_FLOATS,
      );
      return this.catalogWorldStaticData;
    },
    ensureCatalogWorldPulseCapacity(count) {
      if (this.catalogWorldPulseCapacity >= count) return this.catalogWorldPulseData;
      this.catalogWorldPulseCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, count)));
      this.catalogWorldPulseData = new Float32Array(
        this.catalogWorldPulseCapacity * CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS,
      );
      this.catalogWorldPulseUploadedCount = 0;
      this.catalogWorldPulseCacheVersion = -1;
      return this.catalogWorldPulseData;
    },
    ensureCatalogStaticCapacity(count) {
      if (this.catalogStaticCapacity >= count) return this.catalogStaticData;
      this.catalogStaticCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, count)));
      this.catalogStaticData = new Float32Array(this.catalogStaticCapacity * CATALOG_GPU_VERTEX_FLOATS);
      return this.catalogStaticData;
    },
    ensureClusterStarCapacity(count) {
      if (this.clusterStarCapacity >= count) return this.clusterStarData;
      this.clusterStarCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, count)));
      this.clusterStarData = new Float32Array(this.clusterStarCapacity * CLUSTER_STAR_GPU_VERTEX_FLOATS);
      return this.clusterStarData;
    },
    resize() {
      const width = Math.round(scene.width * scene.dpr);
      const height = Math.round(scene.height * scene.dpr);
      if (this.canvas.width !== width) this.canvas.width = width;
      if (this.canvas.height !== height) this.canvas.height = height;
      this.canvas.style.width = `${scene.width}px`;
      this.canvas.style.height = `${scene.height}px`;
      this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    },
    disableUnusedAttributes(keepLocations) {
      const keep = new Set(keepLocations.filter((location) => location >= 0));
      for (const attributes of [this.catalogAttributes, this.catalogDynamicAttributes, this.clusterStarAttributes]) {
        if (!attributes) continue;
        for (const location of Object.values(attributes)) {
          if (location >= 0 && !keep.has(location)) this.gl.disableVertexAttribArray(location);
        }
      }
    },
    clear() {
      this.gl.clearColor(0, 0, 0, 0);
      this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    },
    bindCatalogAttributes(buffer = this.catalogDynamicBuffer) {
      this.disableUnusedAttributes(Object.values(this.catalogAttributes));
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, buffer);
      this.gl.enableVertexAttribArray(this.catalogAttributes.position);
      this.gl.vertexAttribPointer(this.catalogAttributes.position, 2, this.gl.FLOAT, false, catalogStride, 0);
      this.gl.enableVertexAttribArray(this.catalogAttributes.radius);
      this.gl.vertexAttribPointer(
        this.catalogAttributes.radius,
        1,
        this.gl.FLOAT,
        false,
        catalogStride,
        2 * Float32Array.BYTES_PER_ELEMENT,
      );
      this.gl.enableVertexAttribArray(this.catalogAttributes.color);
      this.gl.vertexAttribPointer(
        this.catalogAttributes.color,
        3,
        this.gl.FLOAT,
        false,
        catalogStride,
        3 * Float32Array.BYTES_PER_ELEMENT,
      );
      this.gl.enableVertexAttribArray(this.catalogAttributes.alpha);
      this.gl.vertexAttribPointer(
        this.catalogAttributes.alpha,
        1,
        this.gl.FLOAT,
        false,
        catalogStride,
        6 * Float32Array.BYTES_PER_ELEMENT,
      );
      this.gl.enableVertexAttribArray(this.catalogAttributes.limb);
      this.gl.vertexAttribPointer(
        this.catalogAttributes.limb,
        1,
        this.gl.FLOAT,
        false,
        catalogStride,
        7 * Float32Array.BYTES_PER_ELEMENT,
      );
    },
    bindCatalogWorldAttributes() {
      if (!this.projectsCatalogDynamicInShader) return false;
      this.disableUnusedAttributes(Object.values(this.catalogDynamicAttributes));
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.catalogWorldStaticBuffer);
      this.gl.enableVertexAttribArray(this.catalogDynamicAttributes.position);
      this.gl.vertexAttribPointer(
        this.catalogDynamicAttributes.position,
        3,
        this.gl.FLOAT,
        false,
        catalogWorldStaticStride,
        0,
      );
      this.gl.enableVertexAttribArray(this.catalogDynamicAttributes.static0);
      this.gl.vertexAttribPointer(
        this.catalogDynamicAttributes.static0,
        4,
        this.gl.FLOAT,
        false,
        catalogWorldStaticStride,
        3 * Float32Array.BYTES_PER_ELEMENT,
      );
      this.gl.enableVertexAttribArray(this.catalogDynamicAttributes.lodAlpha);
      this.gl.vertexAttribPointer(
        this.catalogDynamicAttributes.lodAlpha,
        1,
        this.gl.FLOAT,
        false,
        catalogWorldStaticStride,
        7 * Float32Array.BYTES_PER_ELEMENT,
      );
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.catalogWorldPulseBuffer);
      this.gl.enableVertexAttribArray(this.catalogDynamicAttributes.pulse);
      this.gl.vertexAttribPointer(
        this.catalogDynamicAttributes.pulse,
        2,
        this.gl.FLOAT,
        false,
        catalogWorldPulseStride,
        0,
      );
      this.gl.enableVertexAttribArray(this.catalogDynamicAttributes.color);
      this.gl.vertexAttribPointer(
        this.catalogDynamicAttributes.color,
        3,
        this.gl.FLOAT,
        false,
        catalogWorldPulseStride,
        2 * Float32Array.BYTES_PER_ELEMENT,
      );
      return true;
    },
    bindClusterStarAttributes() {
      if (!this.projectsClusterStarsInShader) return false;
      this.disableUnusedAttributes(Object.values(this.clusterStarAttributes));
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.clusterStarBuffer);
      this.gl.enableVertexAttribArray(this.clusterStarAttributes.position);
      this.gl.vertexAttribPointer(this.clusterStarAttributes.position, 3, this.gl.FLOAT, false, clusterStarStride, 0);
      this.gl.enableVertexAttribArray(this.clusterStarAttributes.radiusUnit);
      this.gl.vertexAttribPointer(
        this.clusterStarAttributes.radiusUnit,
        1,
        this.gl.FLOAT,
        false,
        clusterStarStride,
        3 * Float32Array.BYTES_PER_ELEMENT,
      );
      this.gl.enableVertexAttribArray(this.clusterStarAttributes.alphaBaseUnit);
      this.gl.vertexAttribPointer(
        this.clusterStarAttributes.alphaBaseUnit,
        1,
        this.gl.FLOAT,
        false,
        clusterStarStride,
        4 * Float32Array.BYTES_PER_ELEMENT,
      );
      this.gl.enableVertexAttribArray(this.clusterStarAttributes.lodAlpha);
      this.gl.vertexAttribPointer(
        this.clusterStarAttributes.lodAlpha,
        1,
        this.gl.FLOAT,
        false,
        clusterStarStride,
        5 * Float32Array.BYTES_PER_ELEMENT,
      );
      this.gl.enableVertexAttribArray(this.clusterStarAttributes.color);
      this.gl.vertexAttribPointer(
        this.clusterStarAttributes.color,
        3,
        this.gl.FLOAT,
        false,
        clusterStarStride,
        6 * Float32Array.BYTES_PER_ELEMENT,
      );
      return true;
    },
    updateClusterStarBuffer() {
      if (!this.projectsClusterStarsInShader) return false;
      const data = this.ensureClusterStarCapacity(scene.activeClusterStarRenderCount);
      const buckets = scene.activeClusterStarsByCluster;
      const lodAlphaByCluster = scene.clusterStarLodAlphaByCluster;
      let offset = 0;
      let count = 0;
      for (let clusterIndex = 0; clusterIndex < buckets.length; clusterIndex += 1) {
        const lodAlpha = lodAlphaByCluster[clusterIndex] || 0;
        if (lodAlpha <= 0.001) continue;
        const stars = buckets[clusterIndex];
        if (!stars || stars.length === 0) continue;
        for (const point of stars) {
          const coordinates = point.activeCoordinates || coordinatesForPoint(point);
          const rgbValue = normalizedRgbFromCssColor(point.color);
          data[offset] = coordinates[0];
          data[offset + 1] = coordinates[1];
          data[offset + 2] = coordinates[2];
          data[offset + 3] = point.radiusUnit;
          data[offset + 4] = point.alphaBaseUnit;
          data[offset + 5] = lodAlpha;
          data[offset + 6] = rgbValue[0];
          data[offset + 7] = rgbValue[1];
          data[offset + 8] = rgbValue[2];
          offset += CLUSTER_STAR_GPU_VERTEX_FLOATS;
          count += 1;
        }
      }
      this.clusterStarCount = count;
      this.clusterStarSourceCount = scene.activeClusterStarRenderCount;
      this.clusterStarCoordinateCacheKey = scene.coordinateCacheKey;
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.clusterStarBuffer);
      this.gl.bufferData(
        this.gl.ARRAY_BUFFER,
        data.subarray(0, count * CLUSTER_STAR_GPU_VERTEX_FLOATS),
        this.gl.STATIC_DRAW,
      );
      scene.clusterStarGpuDirty = false;
      return true;
    },
    drawClusterStars() {
      if (!this.projectsClusterStarsInShader) return false;
      this.resize();
      rebuildActivePointLists();
      rebuildCoordinateCache();
      if (
        scene.clusterStarGpuDirty ||
        this.clusterStarSourceCount !== scene.activeClusterStarRenderCount ||
        this.clusterStarCoordinateCacheKey !== scene.coordinateCacheKey
      ) {
        this.updateClusterStarBuffer();
      }
      if (this.clusterStarCount <= 0) return true;

      const transform = makeProjectionTransform();
      this.gl.useProgram(this.clusterStarProgram);
      this.bindClusterStarAttributes();
      this.gl.uniform2f(this.clusterStarUniforms.resolution, scene.width, scene.height);
      this.gl.uniform2f(this.clusterStarUniforms.center, scene.centerX, scene.centerY);
      this.gl.uniform4f(this.clusterStarUniforms.yawPitch, transform.cosy, transform.siny, transform.cosp, transform.sinp);
      this.gl.uniform2f(this.clusterStarUniforms.roll, transform.cosr, transform.sinr);
      this.gl.uniform1f(this.clusterStarUniforms.scale, transform.scale);
      this.gl.uniform1f(this.clusterStarUniforms.depthScale, transform.depthScale);
      this.gl.uniform1f(this.clusterStarUniforms.dpr, scene.dpr);
      this.gl.uniform1f(this.clusterStarUniforms.radiusZoomSize, starRadiusZoomSize());
      this.gl.uniform1f(this.clusterStarUniforms.radiusScale, state.radiusScale);
      this.gl.uniform1f(this.clusterStarUniforms.starBaseRadiusViewportScale, starBaseRadiusViewportScale());
      this.gl.uniform1f(this.clusterStarUniforms.exposure, datasetExposureValue("clusters"));
      this.gl.uniform1f(this.clusterStarUniforms.displayLuminosityBaseBoost, DISPLAY_LUMINOSITY_BASE_BOOST);
      this.gl.uniform1f(this.clusterStarUniforms.starAlphaHeadroomExposure, STAR_ALPHA_HEADROOM_EXPOSURE);
      this.gl.uniform1f(this.clusterStarUniforms.starPulseAlphaMax, STAR_PULSE_ALPHA_MAX);
      this.gl.uniform1f(this.clusterStarUniforms.starRadiusBaseMax, STAR_RADIUS_BASE_MAX);
      this.gl.blendFunc(this.gl.ONE, this.gl.ONE);
      this.gl.drawArrays(this.gl.POINTS, 0, this.clusterStarCount);
      return true;
    },
    prepareCatalogDraw(buffer) {
      this.resize();
      this.gl.useProgram(this.catalogProgram);
      this.bindCatalogAttributes(buffer);
      this.gl.uniform2f(this.catalogUniforms.resolution, scene.width, scene.height);
      this.gl.uniform1f(this.catalogUniforms.dpr, scene.dpr);
      this.gl.uniform1f(this.catalogUniforms.limbCoefficient, LIMB_DARKENING_LINEAR_COEFFICIENT);
      this.gl.uniform1f(this.catalogUniforms.limbFluxNormalization, LIMB_DARKENING_FLUX_NORMALIZATION);
      this.gl.blendFunc(this.gl.ONE, this.gl.ONE);
    },
    prepareCatalogWorldDraw() {
      if (!this.projectsCatalogDynamicInShader) return false;
      this.resize();
      const transform = makeProjectionTransform();
      this.gl.useProgram(this.catalogDynamicProgram);
      this.bindCatalogWorldAttributes();
      this.gl.uniform2f(this.catalogDynamicUniforms.resolution, scene.width, scene.height);
      this.gl.uniform2f(this.catalogDynamicUniforms.center, scene.centerX, scene.centerY);
      this.gl.uniform4f(
        this.catalogDynamicUniforms.yawPitch,
        transform.cosy,
        transform.siny,
        transform.cosp,
        transform.sinp,
      );
      this.gl.uniform2f(this.catalogDynamicUniforms.roll, transform.cosr, transform.sinr);
      this.gl.uniform1f(this.catalogDynamicUniforms.scale, transform.scale);
      this.gl.uniform1f(this.catalogDynamicUniforms.depthScale, transform.depthScale);
      this.gl.uniform1f(this.catalogDynamicUniforms.dpr, scene.dpr);
      this.gl.uniform1f(this.catalogDynamicUniforms.radiusZoomSize, starRadiusZoomSize());
      this.gl.uniform1f(this.catalogDynamicUniforms.radiusScale, state.radiusScale);
      this.gl.uniform1f(this.catalogDynamicUniforms.starBaseRadiusViewportScale, starBaseRadiusViewportScale());
      this.gl.uniform1f(this.catalogDynamicUniforms.displayLuminosityBaseBoost, DISPLAY_LUMINOSITY_BASE_BOOST);
      this.gl.uniform1f(this.catalogDynamicUniforms.starAlphaHeadroomExposure, STAR_ALPHA_HEADROOM_EXPOSURE);
      this.gl.uniform1f(this.catalogDynamicUniforms.starPulseAlphaMax, STAR_PULSE_ALPHA_MAX);
      this.gl.uniform1f(this.catalogDynamicUniforms.starRadiusBaseMax, STAR_RADIUS_BASE_MAX);
      this.gl.uniform1f(this.catalogDynamicUniforms.limbCoefficient, LIMB_DARKENING_LINEAR_COEFFICIENT);
      this.gl.uniform1f(this.catalogDynamicUniforms.limbFluxNormalization, LIMB_DARKENING_FLUX_NORMALIZATION);
      this.gl.blendFunc(this.gl.ONE, this.gl.ONE);
      return true;
    },
    drawCatalogBuffer(buffer, count) {
      if (count <= 0) return;
      this.prepareCatalogDraw(buffer);
      this.gl.drawArrays(this.gl.POINTS, 0, count);
    },
    uploadCatalogStatic(count) {
      this.catalogStaticCount = count;
      const vertexCount = count * CATALOG_GPU_VERTEX_FLOATS;
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.catalogStaticBuffer);
      this.gl.bufferData(this.gl.ARRAY_BUFFER, this.catalogStaticData.subarray(0, vertexCount), this.gl.STATIC_DRAW);
    },
    uploadCatalogWorldStatic(items) {
      if (!this.projectsCatalogDynamicInShader) return 0;
      const data = this.ensureCatalogWorldStaticCapacity(items.length);
      let offset = 0;
      let count = 0;
      for (const item of items) {
        if (scene.catalogDrawListScreenProjected && catalogDynamicItemNeedsScreenProjection(item)) {
          item.catalogWorldPulseIndex = -1;
          continue;
        }
        item.catalogWorldPulseIndex = count;
        offset = writeCatalogGpuWorldStaticItem(data, offset, item);
        count += 1;
      }
      this.catalogWorldStaticCount = count;
      this.catalogWorldStaticCacheVersion = scene.catalogStaticCacheVersion;
      this.catalogWorldPulseUploadedCount = 0;
      this.catalogWorldPulseCacheVersion = -1;
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.catalogWorldStaticBuffer);
      this.gl.bufferData(
        this.gl.ARRAY_BUFFER,
        data.subarray(0, count * CATALOG_DYNAMIC_GPU_STATIC_VERTEX_FLOATS),
        this.gl.STATIC_DRAW,
      );
      return count;
    },
    ensureCatalogWorldStatic(items) {
      if (!this.projectsCatalogDynamicInShader) return 0;
      if (this.catalogWorldStaticCacheVersion !== scene.catalogStaticCacheVersion) {
        return this.uploadCatalogWorldStatic(items);
      }
      return this.catalogWorldStaticCount;
    },
    drawCatalogStatic() {
      this.drawCatalogBuffer(this.catalogStaticBuffer, this.catalogStaticCount);
    },
    uploadCatalogWorldPulse(count, dirtyRanges = [], forceFullUpload = false) {
      if (!this.projectsCatalogDynamicInShader || count <= 0) return false;
      const vertexCount = count * CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS;
      const needsFullUpload =
        forceFullUpload ||
        this.catalogWorldPulseUploadedCount !== count ||
        this.catalogWorldPulseCacheVersion !== scene.catalogStaticCacheVersion;
      let uploadFull = needsFullUpload;
      let dirtyVertexCount = 0;
      if (!uploadFull) {
        for (const range of dirtyRanges) {
          dirtyVertexCount += (range.end - range.start) * CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS;
        }
        uploadFull =
          dirtyRanges.length > CATALOG_WORLD_PULSE_FULL_UPLOAD_RANGE_LIMIT ||
          dirtyVertexCount / Math.max(1, vertexCount) >= CATALOG_WORLD_PULSE_FULL_UPLOAD_DIRTY_FRACTION;
      }

      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.catalogWorldPulseBuffer);
      if (uploadFull) {
        this.gl.bufferData(
          this.gl.ARRAY_BUFFER,
          this.catalogWorldPulseData.subarray(0, vertexCount),
          this.gl.STREAM_DRAW,
        );
      } else {
        for (const range of dirtyRanges) {
          const start = range.start * CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS;
          const end = range.end * CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS;
          this.gl.bufferSubData(
            this.gl.ARRAY_BUFFER,
            start * Float32Array.BYTES_PER_ELEMENT,
            this.catalogWorldPulseData.subarray(start, end),
          );
        }
      }
      this.catalogWorldPulseUploadedCount = count;
      this.catalogWorldPulseCacheVersion = scene.catalogStaticCacheVersion;
      return true;
    },
    drawCatalogDynamicWorld(count, dirtyRanges = [], forceFullUpload = false) {
      if (!this.projectsCatalogDynamicInShader || count <= 0) return false;
      this.uploadCatalogWorldPulse(count, dirtyRanges, forceFullUpload);
      this.prepareCatalogWorldDraw();
      this.gl.drawArrays(this.gl.POINTS, 0, count);
      return true;
    },
    drawCatalogDynamic(count) {
      if (count <= 0) return;
      const vertexCount = count * CATALOG_GPU_VERTEX_FLOATS;
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.catalogDynamicBuffer);
      this.gl.bufferData(this.gl.ARRAY_BUFFER, this.catalogDynamicData.subarray(0, vertexCount), this.gl.STREAM_DRAW);
      this.drawCatalogBuffer(this.catalogDynamicBuffer, count);
    },
    drawCatalog(count) {
      this.drawCatalogDynamic(count);
    },
  };
}

function createRedClumpLayerRenderer(canvasElement) {
  if (!CATALOG_GPU_ENABLED || !canvasElement) return null;

  const gl = canvasElement.getContext("webgl", {
    alpha: true,
    antialias: false,
    depth: false,
    stencil: false,
    premultipliedAlpha: true,
    preserveDrawingBuffer: true,
  });
  if (!gl) return null;

  const redClumpProgram = createRedClumpProgram(gl);
  if (!redClumpProgram) return null;

  const redClumpBuffer = gl.createBuffer();
  const redClumpIndexBuffer = gl.createBuffer();
  const uintIndexExtension = gl.getExtension("OES_element_index_uint");
  const redClumpIndexArrayType = uintIndexExtension ? Uint32Array : Uint16Array;
  const redClumpIndexType = uintIndexExtension ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT;
  const redClumpStride = RED_CLUMP_GPU_VERTEX_FLOATS * Float32Array.BYTES_PER_ELEMENT;
  const redClumpAttributes = {
    position: gl.getAttribLocation(redClumpProgram, "a_position"),
    alphaFactors: gl.getAttribLocation(redClumpProgram, "a_alphaFactors"),
  };
  const redClumpUniforms = {
    resolution: gl.getUniformLocation(redClumpProgram, "u_resolution"),
    center: gl.getUniformLocation(redClumpProgram, "u_center"),
    color: gl.getUniformLocation(redClumpProgram, "u_color"),
    yawPitch: gl.getUniformLocation(redClumpProgram, "u_yawPitch"),
    roll: gl.getUniformLocation(redClumpProgram, "u_roll"),
    scale: gl.getUniformLocation(redClumpProgram, "u_scale"),
    depthScale: gl.getUniformLocation(redClumpProgram, "u_depthScale"),
    density: gl.getUniformLocation(redClumpProgram, "u_density"),
    exposure: gl.getUniformLocation(redClumpProgram, "u_exposure"),
    alphaBaseUnit: gl.getUniformLocation(redClumpProgram, "u_alphaBaseUnit"),
    displayLuminosityBaseBoost: gl.getUniformLocation(redClumpProgram, "u_displayLuminosityBaseBoost"),
    displayAlphaMax: gl.getUniformLocation(redClumpProgram, "u_displayAlphaMax"),
    surfaceAlphaScale: gl.getUniformLocation(redClumpProgram, "u_surfaceAlphaScale"),
    surfaceAlphaMax: gl.getUniformLocation(redClumpProgram, "u_surfaceAlphaMax"),
  };

  gl.disable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);

  canvasElement.addEventListener("webglcontextlost", (event) => {
    event.preventDefault();
    scene.redClumpRenderer = null;
    markRedClumpLayerDirty();
  });

  return {
    mode: "gpu",
    projectsInShader: true,
    gl,
    canvas: canvasElement,
    redClumpProgram,
    redClumpBuffer,
    redClumpIndexBuffer,
    redClumpAttributes,
    redClumpUniforms,
    redClumpCapacity: 0,
    redClumpData: new Float32Array(0),
    redClumpIndexCapacity: 0,
    redClumpIndexData: new redClumpIndexArrayType(0),
    redClumpIndexCount: 0,
    redClumpIndexType,
    redClumpUsesIndexedDraw: true,
    redClumpCount: 0,
    redClumpSourceCount: -1,
    redClumpCoordinateCacheKey: null,
    ensureRedClumpCapacity(vertexCount) {
      if (this.redClumpCapacity >= vertexCount) return this.redClumpData;
      this.redClumpCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, vertexCount)));
      this.redClumpData = new Float32Array(this.redClumpCapacity * RED_CLUMP_GPU_VERTEX_FLOATS);
      return this.redClumpData;
    },
    ensureRedClumpIndexCapacity(indexCount) {
      if (this.redClumpIndexCapacity >= indexCount) return this.redClumpIndexData;
      this.redClumpIndexCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, indexCount)));
      this.redClumpIndexData = new redClumpIndexArrayType(this.redClumpIndexCapacity);
      return this.redClumpIndexData;
    },
    resize() {
      const width = Math.round(scene.width * scene.dpr);
      const height = Math.round(scene.height * scene.dpr);
      if (this.canvas.width !== width) this.canvas.width = width;
      if (this.canvas.height !== height) this.canvas.height = height;
      this.canvas.style.width = `${scene.width}px`;
      this.canvas.style.height = `${scene.height}px`;
      this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    },
    clear() {
      this.gl.clearColor(0, 0, 0, 0);
      this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    },
    bindRedClumpAttributes() {
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.redClumpBuffer);
      this.gl.enableVertexAttribArray(this.redClumpAttributes.position);
      this.gl.vertexAttribPointer(this.redClumpAttributes.position, 3, this.gl.FLOAT, false, redClumpStride, 0);
      this.gl.enableVertexAttribArray(this.redClumpAttributes.alphaFactors);
      this.gl.vertexAttribPointer(
        this.redClumpAttributes.alphaFactors,
        3,
        this.gl.FLOAT,
        false,
        redClumpStride,
        3 * Float32Array.BYTES_PER_ELEMENT,
      );
    },
    updateRedClumpBuffer() {
      const cells = scene.redClumpSurface;
      const maxIndexedVertexCount = uintIndexExtension ? Infinity : 65535;
      const canUseIndexedDraw = cells.length * 4 <= maxIndexedVertexCount;
      const data = this.ensureRedClumpCapacity(cells.length * (canUseIndexedDraw ? 4 : 6));
      const indexData = canUseIndexedDraw ? this.ensureRedClumpIndexCapacity(cells.length * 6) : null;
      const triangleIndexes = [0, 1, 2, 0, 2, 3];
      let offset = 0;
      let vertexCount = 0;
      let indexCount = 0;
      for (const cell of cells) {
        const points = cell.points;
        const coordinates = points.map((point) => point.activeCoordinates);
        if (coordinates.some((pointCoordinates) => !pointCoordinates)) continue;
        const sampleMax = Math.max(
          points[0].sample || 0,
          points[1].sample || 0,
          points[2].sample || 0,
          points[3].sample || 0,
        );

        if (canUseIndexedDraw) {
          const baseIndex = vertexCount;
          for (let pointIndex = 0; pointIndex < 4; pointIndex += 1) {
            const point = points[pointIndex];
            const pointCoordinates = coordinates[pointIndex];
            data[offset] = pointCoordinates[0];
            data[offset + 1] = pointCoordinates[1];
            data[offset + 2] = pointCoordinates[2];
            data[offset + 3] = point.edgeAlpha;
            data[offset + 4] = point.densityAlpha;
            data[offset + 5] = sampleMax;
            offset += RED_CLUMP_GPU_VERTEX_FLOATS;
            vertexCount += 1;
          }
          indexData[indexCount] = baseIndex;
          indexData[indexCount + 1] = baseIndex + 1;
          indexData[indexCount + 2] = baseIndex + 2;
          indexData[indexCount + 3] = baseIndex;
          indexData[indexCount + 4] = baseIndex + 2;
          indexData[indexCount + 5] = baseIndex + 3;
          indexCount += 6;
        } else {
          for (const pointIndex of triangleIndexes) {
            const point = points[pointIndex];
            const pointCoordinates = coordinates[pointIndex];
            data[offset] = pointCoordinates[0];
            data[offset + 1] = pointCoordinates[1];
            data[offset + 2] = pointCoordinates[2];
            data[offset + 3] = point.edgeAlpha;
            data[offset + 4] = point.densityAlpha;
            data[offset + 5] = sampleMax;
            offset += RED_CLUMP_GPU_VERTEX_FLOATS;
            vertexCount += 1;
          }
        }
      }

      this.redClumpCount = vertexCount;
      this.redClumpIndexCount = indexCount;
      this.redClumpUsesIndexedDraw = canUseIndexedDraw;
      this.redClumpSourceCount = cells.length;
      this.redClumpCoordinateCacheKey = scene.coordinateCacheKey;
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.redClumpBuffer);
      this.gl.bufferData(this.gl.ARRAY_BUFFER, data.subarray(0, offset), this.gl.DYNAMIC_DRAW);
      if (canUseIndexedDraw) {
        this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, this.redClumpIndexBuffer);
        this.gl.bufferData(this.gl.ELEMENT_ARRAY_BUFFER, indexData.subarray(0, indexCount), this.gl.DYNAMIC_DRAW);
      }
      scene.redClumpGpuDirty = false;
    },
    drawRedClump(rgbValue) {
      this.resize();
      rebuildCoordinateCache();
      if (
        scene.redClumpGpuDirty ||
        this.redClumpSourceCount !== scene.redClumpSurface.length ||
        this.redClumpCoordinateCacheKey !== scene.coordinateCacheKey
      ) {
        this.updateRedClumpBuffer();
      }
      if (this.redClumpCount <= 0) return;

      const transform = makeProjectionTransform();
      this.gl.useProgram(this.redClumpProgram);
      this.bindRedClumpAttributes();
      this.gl.uniform2f(this.redClumpUniforms.resolution, scene.width, scene.height);
      this.gl.uniform2f(this.redClumpUniforms.center, scene.centerX, scene.centerY);
      this.gl.uniform3f(this.redClumpUniforms.color, rgbValue[0], rgbValue[1], rgbValue[2]);
      this.gl.uniform4f(
        this.redClumpUniforms.yawPitch,
        transform.cosy,
        transform.siny,
        transform.cosp,
        transform.sinp,
      );
      this.gl.uniform2f(this.redClumpUniforms.roll, transform.cosr, transform.sinr);
      this.gl.uniform1f(this.redClumpUniforms.scale, transform.scale);
      this.gl.uniform1f(this.redClumpUniforms.depthScale, transform.depthScale);
      this.gl.uniform1f(this.redClumpUniforms.density, state.density);
      this.gl.uniform1f(this.redClumpUniforms.exposure, redClumpRenderExposureValue());
      this.gl.uniform1f(
        this.redClumpUniforms.alphaBaseUnit,
        pointAlphaUnitBaseFromLuminosity(RED_CLUMP_LUMINOSITY) * BASE_LUMINOSITY_FACTOR,
      );
      this.gl.uniform1f(this.redClumpUniforms.displayLuminosityBaseBoost, DISPLAY_LUMINOSITY_BASE_BOOST);
      this.gl.uniform1f(this.redClumpUniforms.displayAlphaMax, DISPLAY_ALPHA_MAX);
      this.gl.uniform1f(this.redClumpUniforms.surfaceAlphaScale, RED_CLUMP_SURFACE_ALPHA_SCALE);
      this.gl.uniform1f(this.redClumpUniforms.surfaceAlphaMax, RED_CLUMP_SURFACE_ALPHA_MAX);
      this.gl.blendFunc(this.gl.ONE, this.gl.ONE_MINUS_SRC_ALPHA);
      if (this.redClumpUsesIndexedDraw) {
        this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, this.redClumpIndexBuffer);
        this.gl.drawElements(this.gl.TRIANGLES, this.redClumpIndexCount, this.redClumpIndexType, 0);
      } else {
        this.gl.drawArrays(this.gl.TRIANGLES, 0, this.redClumpCount);
      }
    },
  };
}

function clearCatalogRenderer() {
  if (scene.catalogStaticRenderer) scene.catalogStaticRenderer.clear();
  if (scene.catalogRenderer) scene.catalogRenderer.clear();
}

function beginGpuSceneLayer() {
  if (!scene.catalogRenderer) return;
  scene.catalogRenderer.resize();
  scene.catalogRenderer.clear();
  scene.gpuLayerFrameActive = true;
}

function endGpuSceneLayer() {
  scene.gpuLayerFrameActive = false;
}

function prepareGpuSceneLayer() {
  const renderer = scene.catalogRenderer;
  if (!renderer || !scene.catalogStaticRenderer) return null;
  if (!scene.gpuLayerFrameActive) {
    renderer.resize();
    renderer.clear();
  }
  return renderer;
}

function markCatalogStaticDirty() {
  scene.catalogStaticDirty = true;
}

function markClusterStarGpuDirty() {
  scene.clusterStarGpuDirty = true;
}

function markRedClumpLayerDirty() {
  scene.redClumpGpuDirty = true;
  scene.redClumpStaticDirty = true;
  scene.redClumpStaticSignature = null;
}

function resizeCatalogStaticCanvas() {
  if (
    scene.catalogStaticCanvas.width !== canvas.width ||
    scene.catalogStaticCanvas.height !== canvas.height
  ) {
    scene.catalogStaticCanvas.width = canvas.width;
    scene.catalogStaticCanvas.height = canvas.height;
    markCatalogStaticDirty();
  }
  scene.catalogStaticCtx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
}

function resizeRedClumpStaticCanvas() {
  if (
    scene.redClumpStaticCanvas.width !== canvas.width ||
    scene.redClumpStaticCanvas.height !== canvas.height
  ) {
    scene.redClumpStaticCanvas.width = canvas.width;
    scene.redClumpStaticCanvas.height = canvas.height;
    markRedClumpLayerDirty();
  }
  scene.redClumpStaticCanvas.style.width = `${scene.width}px`;
  scene.redClumpStaticCanvas.style.height = `${scene.height}px`;
  if (scene.redClumpRenderer) {
    scene.redClumpRenderer.resize();
    return;
  }
  if (!scene.redClumpStaticCtx) return;
  scene.redClumpStaticCtx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
}

function clearCatalogStaticCanvas() {
  scene.catalogStaticCtx.setTransform(1, 0, 0, 1, 0, 0);
  scene.catalogStaticCtx.clearRect(0, 0, scene.catalogStaticCanvas.width, scene.catalogStaticCanvas.height);
  scene.catalogStaticCtx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
}

function clearRedClumpStaticCanvas() {
  if (scene.redClumpRenderer) {
    scene.redClumpRenderer.resize();
    scene.redClumpRenderer.clear();
    return;
  }
  if (!scene.redClumpStaticCtx) return;
  scene.redClumpStaticCtx.setTransform(1, 0, 0, 1, 0, 0);
  scene.redClumpStaticCtx.clearRect(0, 0, scene.redClumpStaticCanvas.width, scene.redClumpStaticCanvas.height);
  scene.redClumpStaticCtx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
}

function resizeSelectionCanvas() {
  if (!selectionCanvas || !selectionCtx) return;
  selectionCanvas.width = canvas.width;
  selectionCanvas.height = canvas.height;
  selectionCanvas.style.width = `${scene.width}px`;
  selectionCanvas.style.height = `${scene.height}px`;
  selectionCtx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
}

function clearSelectionOverlay() {
  if (!selectionCanvas || !selectionCtx) return;
  selectionCtx.setTransform(1, 0, 0, 1, 0, 0);
  selectionCtx.clearRect(0, 0, selectionCanvas.width, selectionCanvas.height);
  selectionCtx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
}

function resizeCanvas() {
  scene.width = window.innerWidth;
  scene.height = window.innerHeight;
  scene.dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(scene.width * scene.dpr);
  canvas.height = Math.round(scene.height * scene.dpr);
  canvas.style.width = `${scene.width}px`;
  canvas.style.height = `${scene.height}px`;
  ctx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
  resizeCatalogStaticCanvas();
  resizeRedClumpStaticCanvas();
  resizeSelectionCanvas();
  if (scene.catalogStaticRenderer) {
    scene.catalogStaticRenderer.resize();
    markCatalogStaticDirty();
  }
  if (scene.catalogRenderer) scene.catalogRenderer.resize();
  updateSceneLayout();
  markProjectionDirty();
}

function baseSceneScaleForZoom(zoom = state.zoom) {
  const centerOffsetX = scene.width > 860 ? DESKTOP_SCENE_CENTER_OFFSET_X : 0;
  const availableWidth = Math.max(320, scene.width - Math.abs(centerOffsetX) * 2);
  return (Math.min(availableWidth, scene.height) / 64) * effectiveZoomScale(zoom);
}

function getBaseSceneLayout() {
  const centerOffsetX = scene.width > 860 ? DESKTOP_SCENE_CENTER_OFFSET_X : 0;
  return {
    centerX: scene.width / 2 + centerOffsetX,
    centerY: scene.height * (scene.width > 860 ? 0.53 : 0.42),
    scale: baseSceneScaleForZoom(),
  };
}

function updateSceneLayout() {
  const base = getBaseSceneLayout();
  scene.scale = base.scale;
  const panScale = Math.max(1, effectiveZoomScale());
  const maxPanX = scene.width * 2.5 * panScale;
  const maxPanY = scene.height * 2.5 * panScale;

  if (state.cameraLocked && state.cameraFollowsLockedTarget && state.locked) {
    const target = targetCoordinates(state.locked);
    const offset = projectedOffsetFor(target.x, target.y, target.z, base.scale);
    state.panX = -offset.x;
    state.panY = -offset.y;
  }

  state.panX = clamp(state.panX, -maxPanX, maxPanX);
  state.panY = clamp(state.panY, -maxPanY, maxPanY);
  scene.centerX = base.centerX + state.panX;
  scene.centerY = base.centerY + state.panY;
  scene.scale = base.scale;
  updateScaleBar();
}

function recenterViewport() {
  state.panX = 0;
  state.panY = 0;
  updateSceneLayout();
}

function nudgeViewportByScreenDelta(dx, dy) {
  if (!dx && !dy) return;

  cancelIntroRotation();
  cancelAxisSpinAnimation();
  markOrientationGridActive();
  if (state.locked || state.cameraLocked) clearTargetSelection();

  if (state.panLock) {
    const sensitivity = panDragSensitivity();
    state.panX += dx * sensitivity;
    state.panY += dy * sensitivity;
  } else {
    const scale = scene.scale || getBaseSceneLayout().scale;
    const nextContext = coordinateContextAfterScreenPan(activeCoordinateReference().context, dx, dy, scale);
    if (!nextContext) return;
    state.customCoordinateContext = nextContext;
    state.panX = 0;
    state.panY = 0;
    clearCoordinateCenterSelection();
  }

  updateSceneLayout();
  markProjectionDirty();
}

function moveViewportByScreenDelta(dx, dy) {
  if (!dx && !dy) return;

  cancelIntroRotation();
  cancelAxisSpinAnimation();
  markOrientationGridActive();
  if (state.locked || state.cameraLocked) clearTargetSelection();

  const sensitivity = panDragSensitivity();
  state.panX += dx * sensitivity;
  state.panY += dy * sensitivity;
  updateSceneLayout();
  markProjectionDirty();
}

function zoomViewportByStep(direction, multiplier = 1) {
  if (!direction) return;
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  const zoomGain = Math.exp(Math.log(VIEWPORT_ZOOM_STEP_GAIN) * direction * multiplier);
  setZoom(state.zoom * zoomGain, scene.centerX, scene.centerY, { allowTargetZoom: true, focusTarget: true });
  syncRangeOutputs();
}

function yawViewportByDegrees(deltaDegrees) {
  if (!deltaDegrees) return;
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  markOrientationGridActive();
  state.yaw = normalizeRadians(state.yaw + degreesToRadians(deltaDegrees));
  syncRangeOutputs();
  markProjectionDirty();
}

function screenPanToLocalDelta(dx, dy, scale = scene.scale) {
  const yaw = observedViewYaw();
  const roll = observedViewRoll();
  const cosy = Math.cos(yaw);
  const siny = Math.sin(yaw);
  const cosp = Math.cos(state.pitch);
  const sinp = Math.sin(state.pitch);
  const cosr = Math.cos(roll);
  const sinr = Math.sin(roll);

  const a = cosy * cosr + siny * sinp * sinr;
  const b = -cosp * sinr;
  const c = cosy * sinr - siny * sinp * cosr;
  const d = cosp * cosr;
  const screenX = dx / Math.max(1, scale);
  const screenY = -dy / Math.max(1, scale);
  const screenDistance = Math.hypot(screenX, screenY);

  // Use a damped inverse so origin-panning stays stable when the view is nearly edge-on.
  const dampingSquared = ORIGIN_PAN_DAMPING * ORIGIN_PAN_DAMPING;
  const m00 = a * a + c * c + dampingSquared;
  const m01 = a * b + c * d;
  const m11 = b * b + d * d + dampingSquared;
  const rhs0 = a * screenX + c * screenY;
  const rhs1 = b * screenX + d * screenY;
  const dampedDeterminant = m00 * m11 - m01 * m01;
  if (Math.abs(dampedDeterminant) < 0.000001) {
    return [screenX, screenY];
  }

  let localX = (rhs0 * m11 - m01 * rhs1) / dampedDeterminant;
  let localY = (m00 * rhs1 - m01 * rhs0) / dampedDeterminant;
  const localDistance = Math.hypot(localX, localY);
  const maxDistance = screenDistance * ORIGIN_PAN_MAX_GAIN;
  if (localDistance > maxDistance && maxDistance > 0) {
    const gain = maxDistance / localDistance;
    localX *= gain;
    localY *= gain;
  }

  return [localX, localY];
}

function coordinateContextAfterScreenPan(reference, dx, dy, scale) {
  if (!reference) return null;
  const [localX, localY] = screenPanToLocalDelta(dx, dy, scale);
  const origin = reference.galacticVector;
  const basis = reference.basis;
  const distance = vectorLength(origin);
  const shifted = [
    origin[0] - localX * basis.east[0] - localY * basis.north[0],
    origin[1] - localX * basis.east[1] - localY * basis.north[1],
    origin[2] - localX * basis.east[2] - localY * basis.north[2],
  ];
  const shiftedDistance = vectorLength(shifted);
  const vector =
    shiftedDistance > 0 && distance > 0
      ? shifted.map((component) => (component / shiftedDistance) * distance)
      : shifted;
  return centerContext(vector);
}

function localPlaneCoordinatesFromScreen(clientX, clientY) {
  const scale = Math.max(1, scene.scale || 1);
  const screenX = (clientX - scene.centerX) / scale;
  const screenY = -(clientY - scene.centerY) / scale;
  const transform = makeProjectionTransform(scale);

  const a = transform.cosy * transform.cosr + transform.siny * transform.sinp * transform.sinr;
  const b = -transform.cosp * transform.sinr;
  const c = transform.cosy * transform.sinr - transform.siny * transform.sinp * transform.cosr;
  const d = transform.cosp * transform.cosr;
  const e = transform.siny * transform.cosp;
  const f = transform.sinp;
  const m11 = 140 * a + screenX * e;
  const m12 = 140 * b + screenX * f;
  const m21 = 140 * c + screenY * e;
  const m22 = 140 * d + screenY * f;
  const rhsX = 140 * screenX;
  const rhsY = 140 * screenY;
  const determinant = m11 * m22 - m12 * m21;

  if (Math.abs(determinant) < 0.000001) {
    return screenPanToLocalDelta(clientX - scene.centerX, clientY - scene.centerY, scale);
  }

  return [
    (rhsX * m22 - m12 * rhsY) / determinant,
    (m11 * rhsY - rhsX * m21) / determinant,
  ];
}

function setOrbitAngle(axis, value) {
  if (!AXIS_SPIN_AXES.has(axis)) return;
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  markOrientationGridActive();
  state[axis] = degreesToRadians(Math.round(value));
  syncRangeOutputs();
  markProjectionDirty();
}

function zoomFocusPointForTarget(target) {
  if (!target) return null;
  const coordinates = coordinatesForPoint(target);
  const projected = projectPoint(coordinates[0], coordinates[1], coordinates[2]);
  return Number.isFinite(projected.x) && Number.isFinite(projected.y) ? projected : null;
}

function setZoom(
  nextZoom,
  focusX = scene.centerX,
  focusY = scene.centerY,
  { allowTargetZoom = false, focusTarget = false } = {},
) {
  markOrientationGridActive();
  const target = selectedTargetForDeepZoom();
  const targetFocus = focusTarget ? zoomFocusPointForTarget(target) : null;
  const anchorX = targetFocus?.x ?? focusX;
  const anchorY = targetFocus?.y ?? focusY;
  const oldScale = scene.scale || 1;
  const oldCenterX = scene.centerX;
  const oldCenterY = scene.centerY;
  state.zoom = clampZoomScale(nextZoom, { allowTargetZoom, target });
  updateSceneLayout();

  const ratio = scene.scale / oldScale;
  const targetCenterX = anchorX - (anchorX - oldCenterX) * ratio;
  const targetCenterY = anchorY - (anchorY - oldCenterY) * ratio;
  const base = getBaseSceneLayout();
  state.panX = targetCenterX - base.centerX;
  state.panY = targetCenterY - base.centerY;
  updateSceneLayout();
  markProjectionDirty();
}

function primeIntroRotation() {
  if (introRotation) return;
  const targetYaw = state.yaw;
  const targetPitch = state.pitch;
  const targetRoll = state.roll;
  state.yaw = degreesToRadians(INTRO_ROTATION_START_YAW_DEGREES);
  state.pitch = degreesToRadians(INTRO_ROTATION_START_PITCH_DEGREES);
  state.roll = degreesToRadians(INTRO_ROTATION_START_ROLL_DEGREES);
  introRotation = {
    startMs: null,
    startYaw: state.yaw,
    targetYaw,
    startPitch: state.pitch,
    targetPitch,
    startRoll: state.roll,
    targetRoll,
  };
  projectionDirty = true;
  syncIntroRotationOutput();
}

function startIntroRotation() {
  const now = performance.now();
  markOrientationGridActive(now);
  primeIntroRotation();
  markNavigationActivityActive(now);
  introRotation.startMs = now;
  introCloudLabelAnimation = { startMs: null };
  projectionDirty = true;
  syncIntroRotationOutput();
}

function syncIntroRotationOutput() {
  syncEditableMultiplierOutput("yaw", radiansToDegrees(state.yaw));
  syncEditableMultiplierOutput("pitch", radiansToDegrees(state.pitch));
  syncEditableMultiplierOutput("roll", radiansToDegrees(state.roll));
  controls.yaw.value = String(radiansToDegrees(state.yaw));
  controls.pitch.value = String(radiansToDegrees(state.pitch));
  controls.roll.value = String(radiansToDegrees(state.roll));
  syncOrientationPresetButtons();
}

function updateIntroRotation(now = performance.now()) {
  if (!introRotation?.startMs) return;
  markOrientationGridActive(now);
  const elapsed = now - introRotation.startMs;
  const progress = clamp(elapsed / INTRO_ROTATION_DURATION_MS, 0, 1);
  const easedProgress = easeOutSine(progress);
  const yawDelta = introRotation.targetYaw - introRotation.startYaw;
  const pitchDelta = introRotation.targetPitch - introRotation.startPitch;
  const rollDelta = introRotation.targetRoll - introRotation.startRoll;
  state.yaw = normalizeRadians(introRotation.startYaw + easedProgress * yawDelta);
  state.pitch = normalizeRadians(introRotation.startPitch + easedProgress * pitchDelta);
  state.roll = normalizeRadians(introRotation.startRoll + easedProgress * rollDelta);
  projectionDirty = true;
  syncIntroRotationOutput();
  maybeStartIntroCloudLabels(now);

  if (progress >= 1) {
    state.yaw = introRotation.targetYaw;
    state.pitch = introRotation.targetPitch;
    state.roll = introRotation.targetRoll;
    introRotation = null;
    updateCoordinateReadout();
    syncRangeOutputs();
  }
}

function cancelIntroRotation() {
  introRotation = null;
  introCloudLabelAnimation = null;
}

function cancelAxisSpinAnimation() {
  axisSpinAnimation = null;
}

function startAxisSpin(axis) {
  if (!AXIS_SPIN_AXES.has(axis)) return;
  const now = performance.now();
  markOrientationGridActive(now);
  cancelIntroRotation();
  axisSpinAnimation = {
    axis,
    startMs: now,
    startValue: state[axis],
  };
  queueRender();
}

function updateAxisSpinAnimation(now = performance.now()) {
  if (!axisSpinAnimation) return;
  markOrientationGridActive(now);

  const elapsed = now - axisSpinAnimation.startMs;
  const progress = clamp(elapsed / AXIS_SPIN_DURATION_MS, 0, 1);
  const easedProgress = smoothStep(progress);
  const axis = axisSpinAnimation.axis;

  state[axis] =
    progress >= 1
      ? axisSpinAnimation.startValue
      : normalizeRadians(axisSpinAnimation.startValue + easedProgress * Math.PI * 2);

  if (progress >= 1) axisSpinAnimation = null;
  projectionDirty = true;
  updateCoordinateReadout();
  syncRangeOutputs();
}

function makeProjectionTransform(scale = scene.scale) {
  const yaw = observedViewYaw();
  const roll = observedViewRoll();
  return {
    cosy: Math.cos(yaw),
    siny: Math.sin(yaw),
    cosp: Math.cos(state.pitch),
    sinp: Math.sin(state.pitch),
    cosr: Math.cos(roll),
    sinr: Math.sin(roll),
    depthScale: state.depthScale,
    scale,
  };
}

function projectOffsetWithTransformInto(target, x, y, z, transform) {
  const depthZ = z * transform.depthScale;

  const x1 = x * transform.cosy - depthZ * transform.siny;
  const z1 = x * transform.siny + depthZ * transform.cosy;
  const y1 = y * transform.cosp - z1 * transform.sinp;
  const z2 = y * transform.sinp + z1 * transform.cosp;
  const x2 = x1 * transform.cosr - y1 * transform.sinr;
  const y2 = x1 * transform.sinr + y1 * transform.cosr;
  const perspective = clamp(140 / (140 - z2), 0.45, 2.2);

  target.x = x2 * transform.scale * perspective;
  target.y = -y2 * transform.scale * perspective;
  target.z = z2;
  target.perspective = perspective;
  return target;
}

function projectOffsetWithTransform(x, y, z, transform) {
  return projectOffsetWithTransformInto({}, x, y, z, transform);
}

function projectedOffsetFor(x, y, z, scale = scene.scale) {
  return projectOffsetWithTransform(x, y, z, makeProjectionTransform(scale));
}

function makeProjector() {
  const transform = makeProjectionTransform();
  const centerX = scene.centerX;
  const centerY = scene.centerY;

  return (x, y, z) => {
    const projected = projectOffsetWithTransform(x, y, z, transform);

    return {
      x: centerX + projected.x,
      y: centerY + projected.y,
      z: projected.z,
      perspective: projected.perspective,
    };
  };
}

function makeProjectorInto() {
  const transform = makeProjectionTransform();
  const centerX = scene.centerX;
  const centerY = scene.centerY;

  return (target, x, y, z) => {
    projectOffsetWithTransformInto(target, x, y, z, transform);
    target.x += centerX;
    target.y += centerY;
    return target;
  };
}

function projectPoint(x, y, z) {
  return makeProjector()(x, y, z);
}

function withinViewport(point, margin = Math.max(28, effectiveZoomScale() * 0.35)) {
  return (
    point.x > -margin &&
    point.x < scene.width + margin &&
    point.y > -margin &&
    point.y < scene.height + margin
  );
}

function projectCatalogItemsForCache(points, catalogDrawList, catalogStats, transform, centerX, centerY, zoomSize, margin) {
  const minX = -margin;
  const maxX = scene.width + margin;
  const minY = -margin;
  const maxY = scene.height + margin;
  const {
    cosy,
    siny,
    cosp,
    sinp,
    cosr,
    sinr,
    depthScale,
    scale,
  } = transform;

  for (let index = 0; index < points.length; index += 1) {
    const point = points[index];
    const coordinates = point.activeCoordinates;
    if (!coordinates) continue;
    const clusterStarLodAlpha =
      point.kind === "clusterStar" ? scene.clusterStarLodAlphaByCluster[point.clusterIndex] || 0 : 1;
    if (clusterStarLodAlpha <= 0.001) continue;

    const x = coordinates[0];
    const y = coordinates[1];
    const depthZ = coordinates[2] * depthScale;
    const x1 = x * cosy - depthZ * siny;
    const z1 = x * siny + depthZ * cosy;
    const y1 = y * cosp - z1 * sinp;
    const z2 = y * sinp + z1 * cosp;
    const x2 = x1 * cosr - y1 * sinr;
    const y2 = x1 * sinr + y1 * cosr;
    const perspective = clamp(140 / (140 - z2), 0.45, 2.2);
    const projected = point.projected;
    projected.x = centerX + x2 * scale * perspective;
    projected.y = centerY - y2 * scale * perspective;
    projected.z = z2;
    projected.perspective = perspective;

    if (projected.x <= minX || projected.x >= maxX || projected.y <= minY || projected.y >= maxY) continue;

    const item = point.drawItem;
    item.baseRadius = starRadiusFromUnitAtPerspective(point.radiusUnit, perspective, zoomSize);
    item.alphaUnit = point.alphaBaseUnit * (0.64 + perspective * 0.24);
    item.clusterStarLodAlpha = clusterStarLodAlpha;
    catalogDrawList.push(item);
    catalogStats.count += 1;
    catalogStats.minDepth = Math.min(catalogStats.minDepth, z2);
    catalogStats.maxDepth = Math.max(catalogStats.maxDepth, z2);
  }
}

function selectedCatalogProjectionTarget() {
  const target = state.locked || state.hovered;
  if (!target) return null;
  return target.kind === "catalog" || target.kind === "clusterStar" ? target : null;
}

function catalogCanUseFastProjectionCache(now = performance.now()) {
  return Boolean(
    scene.catalogRenderer?.projectsCatalogDynamicInShader &&
      scene.catalogStaticRenderer?.projectsCatalogDynamicInShader &&
      CATALOG_PULSE_ALL_STARS &&
      !shouldUseCatalogPulseLod(now) &&
      navigationActivityActive(now) &&
      !selectedCatalogProjectionTarget()
  );
}

function appendCatalogItemsForGpuProjection(
  points,
  catalogDrawList,
  catalogStats,
  { clusterStarLodAlphaByCluster = null } = {},
) {
  for (let index = 0; index < points.length; index += 1) {
    const point = points[index];
    const coordinates = point.activeCoordinates;
    if (!coordinates) continue;

    const item = point.drawItem;
    if (point.kind === "clusterStar") {
      const clusterStarLodAlpha = clusterStarLodAlphaByCluster?.[point.clusterIndex] || 0;
      if (clusterStarLodAlpha <= 0.001) continue;
      item.clusterStarLodAlpha = clusterStarLodAlpha;
    } else {
      item.clusterStarLodAlpha = 1;
    }

    catalogDrawList.push(item);
    catalogStats.count += 1;
    const depth = Number.isFinite(coordinates[2]) ? coordinates[2] * state.depthScale : 0;
    catalogStats.minDepth = Math.min(catalogStats.minDepth, depth);
    catalogStats.maxDepth = Math.max(catalogStats.maxDepth, depth);
  }
}

function ensureProjectionCacheForInteraction() {
  if (projectionDirty || scene.catalogProjectionFastPending) {
    rebuildProjectionCache({ forceCatalogProjection: true });
  }
}

function isCatalogVisible(point) {
  const datasetKey = DATASET_KEYS[point.row[IDX.dataset]];
  return (
    state.datasets[datasetKey] &&
    state.spectral.has(point.row[IDX.spectral]) &&
    point.sample <= state.density
  );
}

function isRedClumpVisible(point) {
  return state.datasets.redclump && point.sample <= state.density;
}

function isClusterStarVisible(point) {
  return state.datasets.clusters && state.spectral.has(point.row[CS.spectral]) && point.sample <= state.density;
}

function isClusterVisible() {
  return state.datasets.clusters;
}

function clusterStarLodAlphaForCoreRadius(coreRadiusPx) {
  return smoothStep(
    (coreRadiusPx - CLUSTER_STAR_LOD_CORE_RADIUS_START) /
      (CLUSTER_STAR_LOD_CORE_RADIUS_END - CLUSTER_STAR_LOD_CORE_RADIUS_START),
  );
}

function rebuildActivePointLists() {
  if (!scene.activePointsDirty) return;

  scene.activeCatalog.length = 0;
  scene.activeRedClump.length = 0;
  scene.activeClusterStars.length = 0;
  scene.activeClusterPulsatorStars.length = 0;
  scene.activeClusters.length = 0;
  scene.activeClusterStarsByCluster.length = scene.clusters.length;
  scene.activeClusterStarCountsByCluster.length = scene.clusters.length;
  for (let index = 0; index < scene.clusters.length; index += 1) {
    if (!scene.activeClusterStarsByCluster[index]) scene.activeClusterStarsByCluster[index] = [];
    else scene.activeClusterStarsByCluster[index].length = 0;
    scene.activeClusterStarCountsByCluster[index] = 0;
  }

  for (const point of scene.catalog) {
    if (isCatalogVisible(point)) scene.activeCatalog.push(point);
  }

  for (const point of scene.clusterStars) {
    if (!isClusterStarVisible(point)) continue;
    scene.activeClusterStars.push(point);
    if (point.lightCurve) {
      scene.activeClusterPulsatorStars.push(point);
      continue;
    }
    const bucket = scene.activeClusterStarsByCluster[point.clusterIndex];
    if (bucket) bucket.push(point);
    scene.activeClusterStarCountsByCluster[point.clusterIndex] =
      (scene.activeClusterStarCountsByCluster[point.clusterIndex] || 0) + 1;
  }

  if (isClusterVisible()) {
    for (const point of scene.clusters) {
      point.activeProjected = null;
      scene.activeClusters.push(point);
    }
  }

  for (const point of scene.redClump) {
    point.activeProjected = null;
    if (!isRedClumpVisible(point)) continue;
    scene.activeRedClump.push(point);
  }

  scene.activePointsDirty = false;
}

function invalidateActivePointLists() {
  scene.activePointsDirty = true;
  markClusterStarGpuDirty();
}

function targetCoordinates(target) {
  const coordinates = coordinatesForPoint(target);
  return { x: coordinates[0], y: coordinates[1], z: coordinates[2] };
}

function queueRender() {
  if (renderQueued) return;
  renderQueued = true;
  window.requestAnimationFrame((timestamp) => {
    renderQueued = false;
    render(timestamp);
  });
}

function resetStats(stats) {
  stats.count = 0;
  stats.minDepth = Infinity;
  stats.maxDepth = -Infinity;
  return stats;
}

function updateStats(stats, depth) {
  stats.count += 1;
  stats.minDepth = Math.min(stats.minDepth, depth);
  stats.maxDepth = Math.max(stats.maxDepth, depth);
}

function markProjectionDirty() {
  if (state.cameraLocked && state.cameraFollowsLockedTarget && state.locked) {
    updateSceneLayout();
  }
  updateCoordinateReadout();
  projectionDirty = true;
  queueRender();
}

function rebuildProjectionCache({ forceCatalogProjection = false } = {}) {
  const projectionStartMs = PERF_HUD_ENABLED ? performance.now() : 0;
  const redStats = resetStats(scene.cachedStats.redClump);
  const catalogStats = resetStats(scene.cachedStats.catalog);
  const redClumpDrawList = scene.redClumpDrawList;
  const redClumpSurfaceDrawList = scene.redClumpSurfaceDrawList;
  const catalogDrawList = scene.catalogDrawList;
  const clusterTargetDrawList = scene.clusterTargetDrawList;
  const projectionTransform = makeProjectionTransform();
  const redClumpProjectsInShader = Boolean(scene.redClumpRenderer?.projectsInShader);
  const clusterStarsProjectInShader = Boolean(scene.catalogStaticRenderer?.projectsClusterStarsInShader);
  const fastCatalogProjection = !forceCatalogProjection && catalogCanUseFastProjectionCache();
  const project = (target, x, y, z) => {
    projectOffsetWithTransformInto(target, x, y, z, projectionTransform);
    target.x += scene.centerX;
    target.y += scene.centerY;
    return target;
  };
  const redClumpRadiusZoomSize = pointRadiusZoomSize();
  const catalogRadiusZoomSize = starRadiusZoomSize();
  const redClumpRadiusUnit = pointRadiusUnitFromStellarRadius(RED_CLUMP_RADIUS);
  const redClumpAlphaBaseUnit = pointAlphaUnitBaseFromLuminosity(RED_CLUMP_LUMINOSITY) * BASE_LUMINOSITY_FACTOR;
  const redClumpAlphaSignature = redClumpAlphaCacheSignature();
  redClumpDrawList.length = 0;
  redClumpSurfaceDrawList.length = 0;
  catalogDrawList.length = 0;
  scene.catalogDrawListScreenProjected = !fastCatalogProjection;
  scene.catalogProjectionFastPending = fastCatalogProjection;
  clusterTargetDrawList.length = 0;
  scene.activeClusterStarRenderCount = 0;
  scene.clusterStarLodAlphaByCluster.length = scene.clusters.length;
  scene.clusterStarLodAlphaByCluster.fill(0);
  rebuildActivePointLists();
  rebuildCoordinateCache();

  if (state.datasets.redclump) {
    for (const point of scene.activeRedClump) {
      const coordinates = point.activeCoordinates || coordinatesForPoint(point);
      const projected = project(point.projected, coordinates[0], coordinates[1], coordinates[2]);
      point.activeProjected = projected;
      if (!withinViewport(projected, 10)) continue;
      const item = point.drawItem;
      item.radius = pointRadiusFromUnitAtPerspective(redClumpRadiusUnit, projected.perspective, redClumpRadiusZoomSize);
      item.alphaUnit = pointAlphaUnitFromBaseAtPerspective(redClumpAlphaBaseUnit, projected.perspective);
      redClumpDrawList.push(item);
      updateStats(redStats, projected.z);
    }

    if (!redClumpProjectsInShader) {
      const surfaceMargin = RED_CLUMP_SURFACE_VIEWPORT_MARGIN;
      for (const cell of scene.redClumpSurface) {
        const projected = cell.projected;
        const p0 = cell.points[0].activeProjected;
        const p1 = cell.points[1].activeProjected;
        const p2 = cell.points[2].activeProjected;
        const p3 = cell.points[3].activeProjected;
        if (!p0 || !p1 || !p2 || !p3) continue;
        projected[0] = p0;
        projected[1] = p1;
        projected[2] = p2;
        projected[3] = p3;

        const minX = Math.min(p0.x, p1.x, p2.x, p3.x);
        const maxX = Math.max(p0.x, p1.x, p2.x, p3.x);
        const minY = Math.min(p0.y, p1.y, p2.y, p3.y);
        const maxY = Math.max(p0.y, p1.y, p2.y, p3.y);
        if (
          maxX <= -surfaceMargin ||
          minX >= scene.width + surfaceMargin ||
          maxY <= -surfaceMargin ||
          minY >= scene.height + surfaceMargin
        ) {
          continue;
        }

        const item = cell.drawItem;
        item.z = (p0.z + p1.z + p2.z + p3.z) * 0.25;
        const alpha0 = pointAlphaUnitFromBaseAtPerspective(redClumpAlphaBaseUnit, p0.perspective);
        const alpha1 = pointAlphaUnitFromBaseAtPerspective(redClumpAlphaBaseUnit, p1.perspective);
        const alpha2 = pointAlphaUnitFromBaseAtPerspective(redClumpAlphaBaseUnit, p2.perspective);
        const alpha3 = pointAlphaUnitFromBaseAtPerspective(redClumpAlphaBaseUnit, p3.perspective);
        item.vertexAlphaUnits[0] = alpha0;
        item.vertexAlphaUnits[1] = alpha1;
        item.vertexAlphaUnits[2] = alpha2;
        item.vertexAlphaUnits[3] = alpha3;
        item.alphaUnit = (alpha0 + alpha1 + alpha2 + alpha3) * 0.25;
        item.starRadius =
          (starRadiusFromBase(
            starRadiusFromUnitAtPerspective(redClumpRadiusUnit, p0.perspective, catalogRadiusZoomSize),
            1,
            PULSATOR_BASE_RADIUS_FACTOR,
          ) +
            starRadiusFromBase(
              starRadiusFromUnitAtPerspective(redClumpRadiusUnit, p1.perspective, catalogRadiusZoomSize),
              1,
              PULSATOR_BASE_RADIUS_FACTOR,
            ) +
            starRadiusFromBase(
              starRadiusFromUnitAtPerspective(redClumpRadiusUnit, p2.perspective, catalogRadiusZoomSize),
              1,
              PULSATOR_BASE_RADIUS_FACTOR,
            ) +
            starRadiusFromBase(
              starRadiusFromUnitAtPerspective(redClumpRadiusUnit, p3.perspective, catalogRadiusZoomSize),
              1,
              PULSATOR_BASE_RADIUS_FACTOR,
            )) *
          0.25;
        updateRedClumpSurfaceAlphaCache(item, true, redClumpAlphaSignature);
        redClumpSurfaceDrawList.push(item);
      }
    }
  }

  const catalogViewportMargin = Math.max(28, effectiveZoomScale() * 0.35);
  if (fastCatalogProjection) {
    appendCatalogItemsForGpuProjection(scene.activeCatalog, catalogDrawList, catalogStats);
  } else {
    projectCatalogItemsForCache(
      scene.activeCatalog,
      catalogDrawList,
      catalogStats,
      projectionTransform,
      scene.centerX,
      scene.centerY,
      catalogRadiusZoomSize,
      catalogViewportMargin,
    );
  }

  for (const point of scene.activeClusters) {
    const coordinates = point.activeCoordinates || coordinatesForPoint(point);
    const projected = project(point.projected, coordinates[0], coordinates[1], coordinates[2]);
    point.activeProjected = projected;
    const item = point.drawItem;
    const physicalRadius = (point.radiusPc / 1000) * scene.scale * projected.perspective;
    const clusterStarLodAlpha = clusterStarLodAlphaForCoreRadius(physicalRadius);
    item.screenRadius = clamp(physicalRadius, 8, 260);
    item.glowAlphaUnit = pointAlphaUnitFromBaseAtPerspective(point.glowAlphaBaseUnit, projected.perspective);
    item.renderedStarGlowAlphaUnit = pointAlphaUnitFromBaseAtPerspective(
      point.renderedStarGlowAlphaBaseUnit,
      projected.perspective,
    );
    item.clusterStarLodAlpha = clusterStarLodAlpha;
    if (!withinViewport(projected, item.screenRadius + 24)) continue;
    scene.clusterStarLodAlphaByCluster[point.index] = clusterStarLodAlpha;
    if (clusterStarLodAlpha > 0.001) {
      scene.activeClusterStarRenderCount += scene.activeClusterStarCountsByCluster[point.index] || 0;
    }
    clusterTargetDrawList.push(item);
  }

  if (clusterStarsProjectInShader) {
    catalogStats.count += scene.activeClusterStarRenderCount;
    markClusterStarGpuDirty();
    if (fastCatalogProjection) {
      appendCatalogItemsForGpuProjection(scene.activeClusterPulsatorStars, catalogDrawList, catalogStats, {
        clusterStarLodAlphaByCluster: scene.clusterStarLodAlphaByCluster,
      });
    } else {
      projectCatalogItemsForCache(
        scene.activeClusterPulsatorStars,
        catalogDrawList,
        catalogStats,
        projectionTransform,
        scene.centerX,
        scene.centerY,
        catalogRadiusZoomSize,
        catalogViewportMargin,
      );
    }
  } else {
    projectCatalogItemsForCache(
      scene.activeClusterStars,
      catalogDrawList,
      catalogStats,
      projectionTransform,
      scene.centerX,
      scene.centerY,
      catalogRadiusZoomSize,
      catalogViewportMargin,
    );
  }

  if (!redClumpProjectsInShader) markRedClumpLayerDirty();
  markCatalogStaticDirty();
  if (PERF_HUD_ENABLED) {
    const projectionMs = performance.now() - projectionStartMs;
    perfState.projectionMs = perfState.projectionMs
      ? perfState.projectionMs * 0.82 + projectionMs * 0.18
      : projectionMs;
  }
  projectionDirty = false;
}

function drawGrid(timestamp = performance.now()) {
  const overlayAlpha = orientationGridAlpha(timestamp);
  if (overlayAlpha <= 0.001) return;

  ctx.save();
  ctx.lineWidth = 1;
  ctx.globalAlpha = 0.36 * overlayAlpha;
  const project = makeProjector();

  for (const radius of [10, 20, 30]) {
    ctx.beginPath();
    for (let index = 0; index <= 96; index += 1) {
      const angle = (index / 96) * Math.PI * 2;
      const point = project(Math.cos(angle) * radius, Math.sin(angle) * radius, 0);
      if (index === 0) ctx.moveTo(point.x, point.y);
      else ctx.lineTo(point.x, point.y);
    }
    ctx.strokeStyle = "rgba(20, 33, 61, 0.24)";
    ctx.stroke();
  }

  const frame = activeCoordinateFrame();
  const axes = [
    { from: [-32, 0, 0], to: [32, 0, 0], color: "rgba(20, 33, 61, 0.78)", label: frame.axes[0][0] },
    { from: [0, -32, 0], to: [0, 32, 0], color: "rgba(252, 163, 17, 0.58)", label: frame.axes[1][0] },
    { from: [0, 0, -24], to: [0, 0, 34], color: "rgba(229, 229, 229, 0.5)", label: frame.axes[2][0] },
  ];

  ctx.font = "12px Inter, system-ui, sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  for (const axis of axes) {
    const from = project(axis.from[0], axis.from[1], axis.from[2]);
    const to = project(axis.to[0], axis.to[1], axis.to[2]);
    ctx.beginPath();
    ctx.moveTo(from.x, from.y);
    ctx.lineTo(to.x, to.y);
    ctx.strokeStyle = axis.color;
    ctx.stroke();
    ctx.fillStyle = axis.color;
    ctx.fillText(axis.label, to.x, to.y);
  }

  ctx.restore();
}

function coordinatesForSkyGridVector(vector, reference) {
  const distance = vectorLength(vector);
  if (state.coordinateFrame === "galactic") {
    const galactic = lonLatFromVector(vector);
    return angularCoordinate(galactic.lon, galactic.lat, distance, reference.galacticCenter);
  }
  return projectLocalVector(vector, reference.galacticVector, reference.basis);
}

function skyGridPointIsDrawable(vector, reference) {
  const referenceDistance = vectorLength(reference.galacticVector);
  const distance = vectorLength(vector);
  if (referenceDistance === 0 || distance === 0) return false;

  const dot =
    (vector[0] * reference.galacticVector[0] +
      vector[1] * reference.galacticVector[1] +
      vector[2] * reference.galacticVector[2]) /
    (referenceDistance * distance);
  return dot > SKY_GRID_FRONT_HEMISPHERE_DOT_MIN;
}

function skyGridLabelCandidate(current, point) {
  if (
    point.x < SKY_GRID_LABEL_MARGIN ||
    point.x > scene.width - SKY_GRID_LABEL_MARGIN ||
    point.y < SKY_GRID_LABEL_MARGIN ||
    point.y > scene.height - SKY_GRID_LABEL_MARGIN
  ) {
    return current;
  }

  const edgeDistance = Math.min(point.x, scene.width - point.x, point.y, scene.height - point.y);
  const centerDistance = Math.hypot(point.x - scene.width * 0.5, point.y - scene.height * 0.5);
  const score = edgeDistance - centerDistance * 0.015;
  return !current || score < current.score ? { x: point.x, y: point.y, score } : current;
}

function labelBoxesOverlap(left, right) {
  return (
    left.x < right.x + right.width &&
    left.x + left.width > right.x &&
    left.y < right.y + right.height &&
    left.y + left.height > right.y
  );
}

function drawSkyGridLabel(label, point, config, placedLabels, context) {
  const labelWidth = context.measureText(label).width;
  const labelHeight = 14;
  const x = clamp(point.x, SKY_GRID_LABEL_MARGIN + labelWidth * 0.5, scene.width - SKY_GRID_LABEL_MARGIN - labelWidth * 0.5);
  const y = clamp(point.y - 8, SKY_GRID_LABEL_MARGIN + labelHeight * 0.5, scene.height - SKY_GRID_LABEL_MARGIN - labelHeight * 0.5);
  const box = {
    x: x - labelWidth * 0.5 - 4,
    y: y - labelHeight * 0.5 - 2,
    width: labelWidth + 8,
    height: labelHeight + 4,
  };

  if (placedLabels.some((placed) => labelBoxesOverlap(placed, box))) return;

  context.save();
  context.globalAlpha = 0.96;
  context.lineWidth = 3;
  context.strokeStyle = "rgba(0, 0, 0, 0.86)";
  context.fillStyle = config.labelColor;
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.strokeText(label, x, y);
  context.fillText(label, x, y);
  context.restore();
  placedLabels.push(box);
}

function longitudeWithinBounds(value, bounds) {
  if (!bounds || bounds.span >= 360) return true;
  return positiveModulo(normalizeDegrees360(value) - bounds.start, 360) <= bounds.span + 0.0001;
}

function gridLongitudeValues(bounds, step) {
  const values = [];
  for (let value = 0; value < 360; value += step) {
    if (longitudeWithinBounds(value, bounds)) values.push(value);
  }
  return values;
}

function gridLatitudeValues(bounds, step) {
  const values = [];
  const start = Math.ceil(bounds.min / step) * step;
  for (let value = start; value <= bounds.max + 0.0001; value += step) {
    values.push(value);
  }
  return values;
}

function drawSkyGridLine(config, fixedAxis, fixedValue, label, bounds, reference, project, distance, placedLabels, context) {
  const isLongitude = fixedAxis === "longitude";
  const sampleSpan = isLongitude ? bounds.latitude.max - bounds.latitude.min : bounds.longitude.span;
  const sampleCount = Math.max(1, Math.ceil(sampleSpan / SKY_GRID_SAMPLE_STEP_DEGREES));
  const jumpLimit = Math.max(scene.width, scene.height) * 0.72;
  let previous = null;
  let segmentStarted = false;
  let labelCandidate = null;
  let hasPath = false;

  context.beginPath();
  for (let index = 0; index <= sampleCount; index += 1) {
    const fraction = sampleCount === 0 ? 0 : index / sampleCount;
    const lon = isLongitude
      ? fixedValue
      : normalizeDegrees360(bounds.longitude.start + bounds.longitude.span * fraction);
    const lat = isLongitude
      ? bounds.latitude.min + (bounds.latitude.max - bounds.latitude.min) * fraction
      : fixedValue;
    const vector = config.vectorFor(lon, lat, distance);
    if (!skyGridPointIsDrawable(vector, reference)) {
      previous = null;
      segmentStarted = false;
      continue;
    }

    const coordinates = coordinatesForSkyGridVector(vector, reference);
    const point = project(coordinates[0], coordinates[1], coordinates[2]);
    if (!Number.isFinite(point.x) || !Number.isFinite(point.y)) {
      previous = null;
      segmentStarted = false;
      continue;
    }

    const jump = previous ? Math.hypot(point.x - previous.x, point.y - previous.y) > jumpLimit : false;
    if (!segmentStarted || jump) {
      context.moveTo(point.x, point.y);
      segmentStarted = true;
    } else {
      context.lineTo(point.x, point.y);
    }
    previous = point;
    hasPath = true;
    labelCandidate = skyGridLabelCandidate(labelCandidate, point);
  }

  if (!hasPath) return;

  context.lineWidth = config.lineWidth ?? 0.85;
  context.strokeStyle = config.lineColor;
  context.setLineDash(config.lineDash);
  context.stroke();
  context.setLineDash([]);

  if (labelCandidate) drawSkyGridLabel(label, labelCandidate, config, placedLabels, context);
}

function drawSkyCoordinateGrid(config, placedLabels, context) {
  const reference = activeCoordinateReference().context;
  const bounds = scene.skyGridBounds?.[config.id];
  if (!reference) return;
  if (!bounds || bounds.longitude.span <= 0 || bounds.latitude.max <= bounds.latitude.min) return;

  const distance = Math.max(1, reference.galacticCenter.distance || 50);
  const project = makeProjector();

  context.save();
  context.font = "11px Inter, system-ui, sans-serif";
  for (const lon of gridLongitudeValues(bounds.longitude, config.longitudeStep)) {
    drawSkyGridLine(config, "longitude", lon, config.longitudeLabel(lon), bounds, reference, project, distance, placedLabels, context);
  }
  for (const lat of gridLatitudeValues(bounds.latitude, config.latitudeStep)) {
    drawSkyGridLine(config, "latitude", lat, config.latitudeLabel(lat), bounds, reference, project, distance, placedLabels, context);
  }
  context.restore();
}

function drawSkyCoordinateGrids() {
  if (!state.equatorialGrid && !state.galacticGrid) return;
  const context = selectionCtx || ctx;
  const placedLabels = [];
  if (state.equatorialGrid) drawSkyCoordinateGrid(SKY_GRID_CONFIGS.equatorial, placedLabels, context);
  if (state.galacticGrid) drawSkyCoordinateGrid(SKY_GRID_CONFIGS.galactic, placedLabels, context);
}

function clusterGlowHalfLightFraction(bins) {
  const totalLuminosity = bins.reduce((sum, bin) => sum + bin.luminosity, 0);
  if (totalLuminosity <= 0) return 0.45;

  const targetLuminosity = totalLuminosity * 0.5;
  let cumulativeLuminosity = 0;
  let previousOuter = 0;

  for (const bin of bins) {
    const outer = Math.max(previousOuter + 0.001, Number.isFinite(bin.outerRadius) ? bin.outerRadius : previousOuter);
    const nextLuminosity = cumulativeLuminosity + bin.luminosity;
    if (nextLuminosity >= targetLuminosity) {
      const fraction = clamp((targetLuminosity - cumulativeLuminosity) / Math.max(bin.luminosity, 0.0001), 0, 1);
      const radiusSquared = previousOuter * previousOuter + fraction * (outer * outer - previousOuter * previousOuter);
      return clamp(Math.sqrt(Math.max(0, radiusSquared)), 0.08, outer);
    }
    cumulativeLuminosity = nextLuminosity;
    previousOuter = outer;
  }

  return Math.max(0.95, previousOuter * 0.5);
}

function cachedClusterGlowHalfLightFraction(item, bins) {
  if (!bins || bins.length === 0) return 0.45;
  if (item.clusterGlowHalfLightBins === bins && Number.isFinite(item.clusterGlowHalfLightFraction)) {
    return item.clusterGlowHalfLightFraction;
  }
  item.clusterGlowHalfLightBins = bins;
  item.clusterGlowHalfLightFraction = clusterGlowHalfLightFraction(bins);
  return item.clusterGlowHalfLightFraction;
}

function clusterGlowOuterRadiusFraction(point) {
  return Math.max(1, point.glowOuterRadiusFraction || 1);
}

function cachedClusterUnresolvedGlowRgb(item, row) {
  const colorKey = `${row[CL.unresolvedVMinusI0]}|${state.colorContrast}`;
  if (item.clusterGlowUnresolvedColorKey === colorKey && item.clusterGlowUnresolvedRgb) {
    return item.clusterGlowUnresolvedRgb;
  }
  item.clusterGlowUnresolvedColorKey = colorKey;
  item.clusterGlowUnresolvedRgb = cssColorToRgb(colorForVMinusI(row[CL.unresolvedVMinusI0], 4));
  return item.clusterGlowUnresolvedRgb;
}

function cachedClusterGlowStopColors(item, radius, profileRadius, scaleRadius, alpha, glowColor) {
  if (
    item.clusterGlowStopRadius === radius &&
    item.clusterGlowStopProfileRadius === profileRadius &&
    item.clusterGlowStopScaleRadius === scaleRadius &&
    item.clusterGlowStopAlpha === alpha &&
    item.clusterGlowStopRed === glowColor[0] &&
    item.clusterGlowStopGreen === glowColor[1] &&
    item.clusterGlowStopBlue === glowColor[2] &&
    item.clusterGlowStopColors
  ) {
    return item.clusterGlowStopColors;
  }

  const stopColors = [];
  for (let index = 0; index <= CLUSTER_GLOW_PROFILE_STOPS; index += 1) {
    const stop = index / CLUSTER_GLOW_PROFILE_STOPS;
    const projectedRadius = stop * radius;
    const plummerSurface = 1 / (1 + (projectedRadius / scaleRadius) ** 2) ** 2;
    const edgeUnit = projectedRadius <= profileRadius ? 0 : (projectedRadius - profileRadius) / (radius - profileRadius);
    const edgeFade = 1 - smoothStep(edgeUnit);
    stopColors.push(rgbaFromRgb(glowColor, alpha * plummerSurface * edgeFade));
  }

  item.clusterGlowStopRadius = radius;
  item.clusterGlowStopProfileRadius = profileRadius;
  item.clusterGlowStopScaleRadius = scaleRadius;
  item.clusterGlowStopAlpha = alpha;
  item.clusterGlowStopRed = glowColor[0];
  item.clusterGlowStopGreen = glowColor[1];
  item.clusterGlowStopBlue = glowColor[2];
  item.clusterGlowStopColors = stopColors;
  return stopColors;
}

function drawClusterGlows() {
  if (!state.datasets.clusters || scene.clusterTargetDrawList.length === 0) return;

  ctx.save();
  ctx.globalCompositeOperation = "source-over";

  for (const item of scene.clusterTargetDrawList) {
    const row = item.point.row;
    const luminosity = row[CL.unresolvedLum];
    const hasUnresolvedGlow = Number.isFinite(luminosity) && luminosity > 0;
    const hasCollapsedStarGlow = (item.renderedStarGlowAlphaUnit || 0) > 0;
    if (!hasUnresolvedGlow && !hasCollapsedStarGlow) continue;
    const bins = item.point.glowBins;

    const unresolvedAlpha = hasUnresolvedGlow
      ? Math.min(
          CLUSTER_GLOW_ALPHA_MAX,
          pointAlphaFromUnit(item.glowAlphaUnit, datasetExposureValue("clusters")) * CLUSTER_GLOW_ALPHA_SCALE,
        )
      : 0;
    const clusterStarLodAlpha = item.clusterStarLodAlpha || 0;
    const collapsedStarFraction =
      CLUSTER_STAR_RESOLVED_GLOW_FLOOR + (1 - CLUSTER_STAR_RESOLVED_GLOW_FLOOR) * (1 - clusterStarLodAlpha);
    const collapsedStarAlpha = hasCollapsedStarGlow
      ? Math.min(
          CLUSTER_STAR_COLLAPSED_GLOW_ALPHA_MAX,
          pointAlphaFromUnit(item.renderedStarGlowAlphaUnit || 0, datasetExposureValue("clusters")) *
            CLUSTER_STAR_COLLAPSED_GLOW_ALPHA_SCALE *
            collapsedStarFraction,
        )
      : 0;
    const alpha = Math.min(CLUSTER_GLOW_ALPHA_MAX + CLUSTER_STAR_COLLAPSED_GLOW_ALPHA_MAX, unresolvedAlpha + collapsedStarAlpha);
    if (alpha <= 0.001) continue;

    const glowOuterRadiusFraction = clusterGlowOuterRadiusFraction(item.point);
    const profileRadius = Math.max(7, item.screenRadius * CLUSTER_GLOW_RADIUS_SCALE * glowOuterRadiusFraction);
    const radius = clusterGlowOuterRadiusFromCoreRadius(item.screenRadius, glowOuterRadiusFraction);
    const halfLightFraction = cachedClusterGlowHalfLightFraction(item, bins);
    const scaleRadius = Math.max(0.08, halfLightFraction) * item.screenRadius * CLUSTER_GLOW_RADIUS_SCALE;
    const unresolvedColor = cachedClusterUnresolvedGlowRgb(item, row);
    const renderedColor = item.point.renderedStarGlowRgb || unresolvedColor;
    const collapsedMix = alpha > 0 ? collapsedStarAlpha / alpha : 0;
    const glowColor = mixRgb(unresolvedColor, renderedColor, collapsedMix);
    const gradient = ctx.createRadialGradient(
      item.projected.x,
      item.projected.y,
      0,
      item.projected.x,
      item.projected.y,
      radius,
    );

    const stopColors = cachedClusterGlowStopColors(item, radius, profileRadius, scaleRadius, alpha, glowColor);
    for (let index = 0; index <= CLUSTER_GLOW_PROFILE_STOPS; index += 1) {
      gradient.addColorStop(index / CLUSTER_GLOW_PROFILE_STOPS, stopColors[index]);
    }

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(item.projected.x, item.projected.y, radius, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.restore();
}

function drawRedClumpGpu() {
  const renderer = scene.redClumpRenderer;
  if (!renderer) return false;

  renderer.drawRedClump(normalizedRgbFromCssColor(scene.spectralClasses[4].color));
  return true;
}

function redClumpStaticSignature() {
  const surfaceCount = scene.redClumpRenderer?.projectsInShader
    ? scene.redClumpSurface.length
    : scene.redClumpSurfaceDrawList.length;
  return [
    scene.width,
    scene.height,
    scene.dpr,
    surfaceCount,
    state.density,
    redClumpRenderExposureValue().toFixed(6),
  ].join("|");
}

function redClumpSurfaceRenderCount() {
  return scene.redClumpRenderer?.projectsInShader
    ? scene.redClumpSurface.length
    : scene.redClumpSurfaceDrawList.length;
}

function drawRedClumpSurfaceToContext(context) {
  context.save();
  context.globalCompositeOperation = "source-over";
  const color = hexToRgb(scene.spectralClasses[4].color);

  for (const item of scene.redClumpSurfaceDrawList) {
    const alpha = updateRedClumpSurfaceAlphaCache(item);
    if (alpha <= 0.001) continue;
    context.fillStyle = rgbaFromRgb(color, alpha);
    context.beginPath();
    context.moveTo(item.projected[0].x, item.projected[0].y);
    for (let index = 1; index < item.projected.length; index += 1) {
      context.lineTo(item.projected[index].x, item.projected[index].y);
    }
    context.closePath();
    context.fill();
  }

  context.restore();
}

function rebuildRedClumpStaticLayerGpu() {
  const renderer = scene.redClumpRenderer;
  if (!renderer) return false;

  renderer.drawRedClump(normalizedRgbFromCssColor(scene.spectralClasses[4].color));
  return true;
}

function rebuildRedClumpStaticLayer() {
  resizeRedClumpStaticCanvas();
  clearRedClumpStaticCanvas();

  const signature = redClumpStaticSignature();
  if (!state.datasets.redclump || redClumpSurfaceRenderCount() === 0) {
    scene.redClumpStaticDirty = false;
    scene.redClumpStaticSignature = signature;
    return;
  }

  if (!rebuildRedClumpStaticLayerGpu() && scene.redClumpStaticCtx) {
    drawRedClumpSurfaceToContext(scene.redClumpStaticCtx);
  }

  scene.redClumpStaticDirty = false;
  scene.redClumpStaticSignature = signature;
}

function setRedClumpLayerOpacity(opacity) {
  if (!redClumpCanvas) return;
  redClumpCanvas.style.opacity = String(clamp(opacity, 0, 1));
}

function drawRedClumpStaticLayer(opacity = 1) {
  if (scene.redClumpStaticCanvas === redClumpCanvas) return;
  if (scene.redClumpStaticCanvas.width <= 0 || scene.redClumpStaticCanvas.height <= 0) return;
  ctx.save();
  ctx.globalAlpha *= clamp(opacity, 0, 1);
  ctx.drawImage(scene.redClumpStaticCanvas, 0, 0, scene.width, scene.height);
  ctx.restore();
}

function drawRedClump(forceDirect = false) {
  const redClumpStartMs = PERF_HUD_ENABLED ? performance.now() : 0;
  const zoomFade = redClumpZoomFade();
  setRedClumpLayerOpacity(zoomFade);
  if (!state.datasets.redclump) {
    if (scene.redClumpStaticSignature !== "disabled") {
      clearRedClumpStaticCanvas();
      scene.redClumpStaticSignature = "disabled";
      scene.redClumpStaticDirty = true;
    }
    return scene.cachedStats.redClump;
  }

  const signature = redClumpStaticSignature();
  if (forceDirect) {
    clearRedClumpStaticCanvas();
    if (!drawRedClumpGpu()) {
      drawRedClumpSurfaceToContext(scene.redClumpStaticCtx || ctx);
    }
  } else {
    if (scene.redClumpStaticDirty || scene.redClumpStaticSignature !== signature) {
      rebuildRedClumpStaticLayer();
    }
    drawRedClumpStaticLayer(zoomFade);
  }

  if (PERF_HUD_ENABLED) {
    updatePerfHud({ redClumpMs: performance.now() - redClumpStartMs });
  }
  return scene.cachedStats.redClump;
}

function starRadiusFactorForPoint(point) {
  return point.kind === "catalog" || point.kind === "clusterStar" ? PULSATOR_BASE_RADIUS_FACTOR : 1;
}

function rawStarRadiusBaseFromBase(baseRadius, radiusFactor = 1) {
  return (
    baseRadius *
      PULSATOR_RADIUS_BASE_SCALE *
      state.radiusScale *
      radiusFactor
  );
}

function rawStarRadiusFromBase(baseRadius, areaPulse = 1, radiusFactor = 1) {
  return rawStarRadiusBaseFromBase(baseRadius, radiusFactor) * Math.sqrt(Math.max(0.000001, areaPulse));
}

function starRadiusFromRawBase(rawBaseRadius, areaPulse = 1, maxRadius = 28) {
  return clamp(rawBaseRadius * Math.sqrt(Math.max(0.000001, areaPulse)), 0.18, maxRadius);
}

function starRadiusFromBase(baseRadius, areaPulse = 1, radiusFactor = 1, maxRadius = 28) {
  return starRadiusFromRawBase(rawStarRadiusBaseFromBase(baseRadius, radiusFactor), areaPulse, maxRadius);
}

function starRadius(point, projected, areaPulse = 1) {
  return starRadiusFromBase(
    starRadiusFromUnitAtPerspective(point.radiusUnit, projected.perspective),
    areaPulse,
    starRadiusFactorForPoint(point),
  );
}

function catalogTargetStarMaxRadius() {
  return Math.max(28, targetZoomLimitRadius() - TARGET_SELECTION_RING_PADDING_PX);
}

function catalogMaxAreaPulse(point) {
  const maxFluxPulse = Math.max(1, pulsationAmplitudeScaledMaxFlux(point?.lightCurve));
  return Math.max(1, lightCurveVisualPulses(maxFluxPulse, point).areaPulse);
}

function catalogNormalVisualRadiusAtZoom(point, projected, zoom = state.zoom, areaPulse = 1) {
  const baseRadius = starRadiusFromUnitAtPerspectiveForZoom(point.radiusUnit, projected.perspective, zoom);
  return starRadiusFromBase(baseRadius, areaPulse, starRadiusFactorForPoint(point));
}

function catalogDeepZoomVisualRadiusAtZoom(point, projected, zoom = state.zoom, areaPulse = 1) {
  const normalRadius = catalogNormalVisualRadiusAtZoom(point, projected, zoom, areaPulse);
  if (zoom <= ZOOM_SCALE_MAX) return normalRadius;

  const maxAreaPulse = Math.max(areaPulse, catalogMaxAreaPulse(point));
  const sliderProjected = targetProjectedAtZoom(point, ZOOM_SCALE_MAX);
  const sliderMaxRadius = catalogNormalVisualRadiusAtZoom(point, sliderProjected, ZOOM_SCALE_MAX, maxAreaPulse);
  const deepZoomGrowth = (zoom / ZOOM_SCALE_MAX) ** STAR_RADIUS_DEEP_ZOOM_TARGET_GROWTH_POWER;
  const grownMaxRadius = Math.min(
    catalogTargetStarMaxRadius(),
    sliderMaxRadius * deepZoomGrowth * starRadiusDeepZoomScale(zoom),
  );
  const pulseScale = Math.sqrt(Math.max(0.000001, areaPulse) / Math.max(0.000001, maxAreaPulse));
  return Math.max(normalRadius, grownMaxRadius * Math.min(1, pulseScale));
}

function catalogRenderVisualRadius(item, areaPulse = 1) {
  if (item.point === state.locked) {
    return catalogDeepZoomVisualRadiusAtZoom(item.point, item.projected, state.zoom, areaPulse);
  }
  return starRadiusFromBase(item.baseRadius, areaPulse, starRadiusFactorForPoint(item.point));
}

function pulseSafeAlphaForPoint(point, lightCurve = null) {
  const scale = clampPulsationAmplitudeScale(state.pulsationAmplitudeScale);
  const preset = currentPulsatorPreset();
  const cacheKey = `${scale}|${preset}`;
  if (point?.pulseSafeAlphaKey === cacheKey && Number.isFinite(point.pulseSafeAlpha)) {
    return point.pulseSafeAlpha;
  }

  const maxFluxPulse = Math.max(1, pulsationAmplitudeScaledMaxFlux(lightCurve));
  const maxOpacityPulse = Math.max(1, lightCurveVisualPulses(maxFluxPulse, point).opacityPulse);
  const pulseSafeAlpha = STAR_PULSE_ALPHA_MAX / maxOpacityPulse;
  if (point) {
    point.pulseSafeAlphaKey = cacheKey;
    point.pulseSafeAlpha = pulseSafeAlpha;
  }
  return pulseSafeAlpha;
}

function starBaseAlphaWithPulseHeadroomFromUnit(
  alphaUnit,
  lightCurve = null,
  point = null,
  exposureGain = datasetExposureForPoint(point),
) {
  const pulseSafeAlpha = pulseSafeAlphaForPoint(point, lightCurve);
  const exposure = (exposureGain / 10) * DISPLAY_LUMINOSITY_BASE_BOOST * alphaUnit;
  return pulseSafeAlpha * (1 - Math.exp(-exposure / STAR_ALPHA_HEADROOM_EXPOSURE));
}

function starAlphaFromBaseAlphaWithPulseHeadroom(baseAlphaWithPulseHeadroom, opacityPulse) {
  return clamp(baseAlphaWithPulseHeadroom * opacityPulse, 0.0005, STAR_PULSE_ALPHA_MAX);
}

function starAlphaFromUnit(alphaUnit, opacityPulse, lightCurve = null, point = null, exposureGain = datasetExposureForPoint(point)) {
  return starAlphaFromBaseAlphaWithPulseHeadroom(
    starBaseAlphaWithPulseHeadroomFromUnit(alphaUnit, lightCurve, point, exposureGain),
    opacityPulse,
  );
}

function redClumpSurfacePhysicalAlpha(item) {
  const count = Math.max(0, item.effectiveCount || 0) * RED_CLUMP_COUNT_TO_STAR_EQUIVALENT;
  if (count <= 0) return 0;
  const area = Math.max(1, polygonArea(item.projected));
  const starAlpha = starAlphaFromUnit(item.alphaUnit, 1, null, item);
  const starArea = Math.PI * item.starRadius * item.starRadius * RED_CLUMP_SURFACE_POINT_FILL;
  const expectedBrightness = (count * starArea * starAlpha) / area;
  const alpha = 1 - Math.exp(-Math.max(0, expectedBrightness));
  return clamp(alpha * item.edgeAlpha, 0, RED_CLUMP_SURFACE_ALPHA_MAX);
}

function redClumpSurfaceVisualAlpha(item, pointIndex = -1) {
  const point = pointIndex >= 0 ? item.points?.[pointIndex] : null;
  const alphaUnit =
    pointIndex >= 0 ? item.vertexAlphaUnits?.[pointIndex] ?? item.alphaUnit : item.alphaUnit;
  return clamp(
    pointAlphaFromUnit(alphaUnit, redClumpRenderExposureValue()) *
      (point?.edgeAlpha ?? item.edgeAlpha) *
      (point?.densityAlpha ?? item.densityAlpha) *
      RED_CLUMP_SURFACE_ALPHA_SCALE,
    0,
    RED_CLUMP_SURFACE_ALPHA_MAX,
  );
}

function redClumpAlphaCacheSignature() {
  return redClumpRenderExposureValue();
}

function updateRedClumpSurfaceAlphaCache(item, force = false, signature = redClumpAlphaCacheSignature()) {
  if (!force && item.surfaceAlphaSignature === signature) return item.surfaceAlpha || 0;

  const referenceVisualAlpha = redClumpSurfaceVisualAlpha(item);
  const physicalAlpha = redClumpSurfacePhysicalAlpha(item);
  let alphaScale = 1;
  if (referenceVisualAlpha > 0 && physicalAlpha > 0) {
    const physicalRatio = clamp(
      physicalAlpha / Math.max(referenceVisualAlpha, 0.000001),
      RED_CLUMP_SURFACE_PHYSICAL_MIN_RATIO,
      RED_CLUMP_SURFACE_PHYSICAL_MAX_RATIO,
    );
    alphaScale = 1 + (physicalRatio - 1) * RED_CLUMP_SURFACE_PHYSICAL_BLEND;
  }

  const vertexAlphas = item.surfaceVertexAlphas || [0, 0, 0, 0];
  item.surfaceAlpha = clamp(referenceVisualAlpha * alphaScale, 0, RED_CLUMP_SURFACE_ALPHA_MAX);
  for (let index = 0; index < 4; index += 1) {
    vertexAlphas[index] = clamp(redClumpSurfaceVisualAlpha(item, index) * alphaScale, 0, RED_CLUMP_SURFACE_ALPHA_MAX);
  }
  item.surfaceVertexAlphas = vertexAlphas;
  item.surfaceAlphaSignature = signature;
  return item.surfaceAlpha;
}

function redClumpSurfaceAlpha(item, pointIndex = -1) {
  const signature = redClumpAlphaCacheSignature();
  if (item.surfaceAlphaSignature === signature) {
    if (pointIndex >= 0) return item.surfaceVertexAlphas?.[pointIndex] ?? 0;
    if (Number.isFinite(item.surfaceAlpha)) return item.surfaceAlpha;
  }

  const visualAlpha = redClumpSurfaceVisualAlpha(item, pointIndex);
  const referenceVisualAlpha = redClumpSurfaceVisualAlpha(item);
  const physicalAlpha = redClumpSurfacePhysicalAlpha(item);
  if (referenceVisualAlpha <= 0 || physicalAlpha <= 0) return visualAlpha;

  const physicalRatio = clamp(
    physicalAlpha / Math.max(referenceVisualAlpha, 0.000001),
    RED_CLUMP_SURFACE_PHYSICAL_MIN_RATIO,
    RED_CLUMP_SURFACE_PHYSICAL_MAX_RATIO,
  );
  return clamp(
    visualAlpha * (1 + (physicalRatio - 1) * RED_CLUMP_SURFACE_PHYSICAL_BLEND),
    0,
    RED_CLUMP_SURFACE_ALPHA_MAX,
  );
}

function catalogItemLodAlpha(item) {
  return item.point.kind === "clusterStar" ? item.clusterStarLodAlpha || 0 : 1;
}

function updateCatalogStaticStyle(item) {
  const radiusFactor = starRadiusFactorForPoint(item.point);
  const lodAlpha = catalogItemLodAlpha(item);
  const pulsatorPreset = currentPulsatorPreset();
  if (
    item.staticBaseRadius !== item.baseRadius ||
    item.staticAlphaUnit !== item.alphaUnit ||
    item.staticLodAlpha !== lodAlpha ||
    item.staticRadiusFactor !== radiusFactor ||
    item.staticRadiusScale !== state.radiusScale ||
    item.staticExposure !== datasetExposureForPoint(item.point) ||
    item.staticLightCurve !== item.point.lightCurve ||
    item.staticPulsationAmplitudeScale !== state.pulsationAmplitudeScale ||
    item.staticPulsatorPreset !== pulsatorPreset
  ) {
    item.staticBaseRadius = item.baseRadius;
    item.staticAlphaUnit = item.alphaUnit;
    item.staticLodAlpha = lodAlpha;
    item.staticRadiusFactor = radiusFactor;
    item.staticRadiusScale = state.radiusScale;
    item.staticExposure = datasetExposureForPoint(item.point);
    item.staticLightCurve = item.point.lightCurve;
    item.staticPulsationAmplitudeScale = state.pulsationAmplitudeScale;
    item.staticPulsatorPreset = pulsatorPreset;
    item.staticRadiusRawBase = rawStarRadiusBaseFromBase(item.baseRadius, radiusFactor);
    item.staticRadius = starRadiusFromRawBase(item.staticRadiusRawBase);
    item.staticBaseAlphaWithPulseHeadroom = starBaseAlphaWithPulseHeadroomFromUnit(
      item.alphaUnit,
      item.point.lightCurve,
      item.point,
      item.staticExposure,
    );
    item.staticAlpha =
      starAlphaFromBaseAlphaWithPulseHeadroom(item.staticBaseAlphaWithPulseHeadroom, 1) * lodAlpha;
  }
  item.slowPulseThrottle = shouldSlowPulseThrottleCatalogItem(item);
}

function shouldAnimateCatalogItem(item, baseRadius, baseAlpha, usePulseLod = shouldUseCatalogPulseLod()) {
  if (item.point.kind === "clusterStar" && !item.point.lightCurve) return false;
  if (item.point === state.locked || item.point === state.hovered) {
    item.point.animatePulse = true;
    return true;
  }

  if (pulsationTooFastForAnimation(item.point)) {
    item.point.animatePulse = false;
    return false;
  }

  if (!usePulseLod) {
    item.point.animatePulse = true;
    return true;
  }

  const lodRadius = baseRadius / Math.max(1, state.radiusScale);
  const visualWeight = lodRadius * lodRadius * baseAlpha;
  const wasAnimating = item.point.animatePulse === true;
  const radiusThreshold = wasAnimating ? PULSE_LOD_RADIUS_OFF : PULSE_LOD_RADIUS_ON;
  const alphaThreshold = wasAnimating ? PULSE_LOD_ALPHA_OFF : PULSE_LOD_ALPHA_ON;
  const visualWeightThreshold = wasAnimating ? PULSE_LOD_VISUAL_WEIGHT_OFF : PULSE_LOD_VISUAL_WEIGHT_ON;
  const shouldAnimate =
    lodRadius >= radiusThreshold || baseAlpha >= alphaThreshold || visualWeight >= visualWeightThreshold;

  item.point.animatePulse = shouldAnimate;
  return shouldAnimate;
}

function clearColorBuckets(colorBuckets) {
  for (const bucket of colorBuckets.values()) {
    bucket.length = 0;
  }
}

function pushColorBucket(colorBuckets, color, item) {
  let bucket = colorBuckets.get(color);
  if (!bucket) {
    bucket = [];
    colorBuckets.set(color, bucket);
  }
  bucket.push(item);
}

function drawCatalogBuckets(context, colorBuckets) {
  context.save();
  context.globalCompositeOperation = "lighter";

  for (const [color, bucket] of colorBuckets) {
    if (bucket.length === 0) continue;
    context.fillStyle = color;
    for (const item of bucket) {
      context.globalAlpha = item.currentAlpha;
      drawStarOnContext(context, color, item);
    }
  }

  context.restore();
}

function catalogStaticVisualBaseMatches(item) {
  return (
    item.staticBaseRadius === item.baseRadius &&
    item.staticAlphaUnit === item.alphaUnit &&
    item.staticRadiusFactor === starRadiusFactorForPoint(item.point) &&
    item.staticRadiusScale === state.radiusScale &&
    item.staticExposure === datasetExposureForPoint(item.point) &&
    item.staticLightCurve === item.point.lightCurve &&
    item.staticPulsationAmplitudeScale === state.pulsationAmplitudeScale &&
    item.staticPulsatorPreset === currentPulsatorPreset() &&
    Number.isFinite(item.staticRadiusRawBase) &&
    Number.isFinite(item.staticBaseAlphaWithPulseHeadroom)
  );
}

function animatedCatalogVisualStyleMatches(item) {
  const locked = item.point === state.locked;
  return (
    Number.isFinite(item.currentAlpha) &&
    Number.isFinite(item.currentRadius) &&
    item.currentVisualStyleBaseRadius === item.baseRadius &&
    item.currentVisualStyleAlphaUnit === item.alphaUnit &&
    item.currentVisualStyleExposure === item.staticExposure &&
    item.currentVisualStyleAreaPulse === item.currentAreaPulse &&
    item.currentVisualStyleOpacityPulse === item.currentOpacityPulse &&
    item.currentVisualStyleRadiusScale === state.radiusScale &&
    item.currentVisualStyleLightCurve === item.point.lightCurve &&
    item.currentVisualStylePulsatorPreset === currentPulsatorPreset() &&
    item.currentVisualStyleLocked === locked &&
    (!locked || item.currentVisualStyleZoom === state.zoom)
  );
}

function stampAnimatedCatalogVisualStyle(item) {
  item.currentVisualStyleBaseRadius = item.baseRadius;
  item.currentVisualStyleAlphaUnit = item.alphaUnit;
  item.currentVisualStyleExposure = item.staticExposure;
  item.currentVisualStyleAreaPulse = item.currentAreaPulse;
  item.currentVisualStyleOpacityPulse = item.currentOpacityPulse;
  item.currentVisualStyleRadiusScale = state.radiusScale;
  item.currentVisualStyleLightCurve = item.point.lightCurve;
  item.currentVisualStylePulsatorPreset = currentPulsatorPreset();
  item.currentVisualStyleLocked = item.point === state.locked;
  item.currentVisualStyleZoom = state.zoom;
}

function updateAnimatedCatalogVisualStyle(item) {
  if (catalogStaticVisualBaseMatches(item)) {
    item.currentAlpha = starAlphaFromBaseAlphaWithPulseHeadroom(
      item.staticBaseAlphaWithPulseHeadroom,
      item.currentOpacityPulse,
    );
    item.currentRadius =
      item.point === state.locked
        ? catalogRenderVisualRadius(item, item.currentAreaPulse)
        : starRadiusFromRawBase(item.staticRadiusRawBase, item.currentAreaPulse);
  } else {
    item.currentAlpha = starAlphaFromUnit(
      item.alphaUnit,
      item.currentOpacityPulse,
      item.point.lightCurve,
      item.point,
      item.staticExposure,
    );
    item.currentRadius = catalogRenderVisualRadius(item, item.currentAreaPulse);
  }
  stampAnimatedCatalogVisualStyle(item);
}

function animatedCatalogPulseStateValid(item) {
  return (
    item.currentColor &&
    Number.isFinite(item.currentAreaPulse) &&
    item.currentAreaPulse > 0 &&
    Number.isFinite(item.currentOpacityPulse) &&
    item.currentOpacityPulse > 0
  );
}

function updateAnimatedCatalogPulseState(item, simulationDay) {
  const pulseSample = pulseState(item.point, simulationDay);
  item.currentPulse = pulseSample.pulse;
  item.currentAreaPulse = pulseSample.areaPulse;
  item.currentOpacityPulse = pulseSample.opacityPulse;
  item.currentColor = pulseSample.color;
  item.currentRgb = pulseSample.rgb || null;
  item.currentRgbArray = pulseSample.rgbArray || null;
  item.currentRgbOffset = pulseSample.rgbOffset || 0;
  return item.currentColor;
}

function updateAnimatedCatalogItem(item, simulationDay) {
  updateAnimatedCatalogPulseState(item, simulationDay);
  updateAnimatedCatalogVisualStyle(item);
  return item.currentColor;
}

function cachedAnimatedCatalogItemColor(item, simulationDay) {
  if (!animatedCatalogPulseStateValid(item)) {
    return updateAnimatedCatalogItem(item, simulationDay);
  }
  if (!animatedCatalogVisualStyleMatches(item)) updateAnimatedCatalogVisualStyle(item);
  return item.currentColor;
}

function shouldRefreshAnimatedCatalogItem(item, now, useNavigationPulseFloor = false) {
  if (!PULSE_LOD_ENABLED || !CATALOG_PULSE_ALL_STARS) return true;
  if (!item.slowPulseThrottle) return true;
  if (item.point === state.locked || item.point === state.hovered) return true;

  const intervalMs = slowPulseRefreshIntervalMs(item, useNavigationPulseFloor);
  if (intervalMs <= SLOW_PULSE_REFRESH_FRAME_INTERVAL_MS + 1) return true;

  const refreshBucket = Math.floor((now + intervalMs * item.slowPulseRefreshPhase) / intervalMs);
  const pulsatorPreset = currentPulsatorPreset();
  if (
    item.pulseRefreshBucket === refreshBucket &&
    item.pulseRefreshSpeed === state.pulsationSpeed &&
    item.pulseRefreshAmplitudeScale === state.pulsationAmplitudeScale &&
    item.pulseRefreshPulsatorPreset === pulsatorPreset &&
    item.currentColor
  ) {
    return false;
  }
  item.pulseRefreshBucket = refreshBucket;
  item.pulseRefreshSpeed = state.pulsationSpeed;
  item.pulseRefreshAmplitudeScale = state.pulsationAmplitudeScale;
  item.pulseRefreshPulsatorPreset = pulsatorPreset;
  return true;
}

function updateAnimatedCatalogPulseStateIfNeeded(
  item,
  simulationDay,
  pulseNow,
  useNavigationPulseFloor = false,
) {
  if (!shouldRefreshAnimatedCatalogItem(item, pulseNow, useNavigationPulseFloor)) {
    if (!animatedCatalogPulseStateValid(item)) {
      updateAnimatedCatalogPulseState(item, simulationDay);
      return true;
    }
    return false;
  }
  updateAnimatedCatalogPulseState(item, simulationDay);
  return true;
}

function animatedCatalogItemColor(item, simulationDay, pulseNow, useNavigationPulseFloor = false) {
  if (!shouldRefreshAnimatedCatalogItem(item, pulseNow, useNavigationPulseFloor)) {
    return cachedAnimatedCatalogItemColor(item, simulationDay);
  }
  return updateAnimatedCatalogItem(item, simulationDay);
}

function updateStaticCatalogItem(item) {
  if (pulsationTooFastForAnimation(item.point)) {
    const pulseSample = meanPulseState(item.point);
    item.currentPulse = pulseSample.pulse;
    item.currentAreaPulse = pulseSample.areaPulse;
    item.currentOpacityPulse = pulseSample.opacityPulse;
    item.currentAlpha = starAlphaFromUnit(
      item.alphaUnit,
      item.currentOpacityPulse,
      item.point.lightCurve,
      item.point,
      item.staticExposure,
    );
    item.currentRadius = catalogRenderVisualRadius(item, item.currentAreaPulse);
    item.currentColor = pulseSample.color;
    item.currentRgb = pulseSample.rgb || normalizedRgbForCatalogColor(item.currentColor);
    item.currentRgbArray = null;
    item.currentRgbOffset = 0;
    return item.currentColor;
  }

  item.currentPulse = 1;
  item.currentAreaPulse = 1;
  item.currentOpacityPulse = 1;
  item.currentAlpha = item.staticAlpha;
  item.currentRadius = item.staticRadius;
  item.currentColor = item.point.color;
  item.currentRgb = normalizedRgbForCatalogColor(item.currentColor);
  item.currentRgbArray = null;
  item.currentRgbOffset = 0;
  return item.currentColor;
}

function writeCatalogGpuRgb(data, offset, item, color) {
  const rgbArray = item.currentRgbArray;
  if (rgbArray) {
    const rgbOffset = item.currentRgbOffset || 0;
    data[offset] = rgbArray[rgbOffset];
    data[offset + 1] = rgbArray[rgbOffset + 1];
    data[offset + 2] = rgbArray[rgbOffset + 2];
    return;
  }

  const rgbValue = item.currentRgb || normalizedRgbForCatalogColor(color);
  data[offset] = rgbValue[0];
  data[offset + 1] = rgbValue[1];
  data[offset + 2] = rgbValue[2];
}

function writeCatalogGpuItem(data, offset, item, color) {
  data[offset] = item.projected.x;
  data[offset + 1] = item.projected.y;
  data[offset + 2] = item.currentRadius;
  writeCatalogGpuRgb(data, offset + 3, item, color);
  data[offset + 6] = item.currentAlpha;
  data[offset + 7] = shouldUseLimbDarkening(item) ? 1 : 0;
  return offset + CATALOG_GPU_VERTEX_FLOATS;
}

function catalogDynamicItemNeedsScreenProjection(item) {
  return item.point === state.locked || item.point === state.hovered;
}

function writeCatalogGpuWorldStaticItem(data, offset, item) {
  const coordinates = item.point.activeCoordinates || coordinatesForPoint(item.point);
  const exposure = Number.isFinite(item.staticExposure) ? item.staticExposure : datasetExposureForPoint(item.point);
  data[offset] = coordinates[0];
  data[offset + 1] = coordinates[1];
  data[offset + 2] = coordinates[2];
  data[offset + 3] = item.point.radiusUnit;
  data[offset + 4] = item.point.alphaBaseUnit;
  data[offset + 5] = pulseSafeAlphaForPoint(item.point, item.point.lightCurve);
  data[offset + 6] = exposure;
  data[offset + 7] = catalogItemLodAlpha(item);
  return offset + CATALOG_DYNAMIC_GPU_STATIC_VERTEX_FLOATS;
}

function writeCatalogGpuWorldPulseItem(data, offset, item, color) {
  data[offset] = item.currentAreaPulse;
  data[offset + 1] = item.currentOpacityPulse;
  writeCatalogGpuRgb(data, offset + 2, item, color);
  return offset + CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS;
}

function writeCatalogGpuWorldPulseItemAt(data, index, item, color) {
  return writeCatalogGpuWorldPulseItem(
    data,
    index * CATALOG_DYNAMIC_GPU_PULSE_VERTEX_FLOATS,
    item,
    color,
  );
}

function appendCatalogWorldPulseDirtyRange(ranges, index) {
  const lastRange = ranges[ranges.length - 1];
  if (lastRange && index - lastRange.end <= CATALOG_WORLD_PULSE_DIRTY_RANGE_MERGE_GAP) {
    lastRange.end = index + 1;
    return;
  }
  ranges.push({ start: index, end: index + 1 });
}

function catalogStaticCacheMatches() {
  const pulseLodActive = shouldUseCatalogPulseLod();
  const projectionMode = scene.catalogDrawListScreenProjected ? "screen" : "world";
  return (
    !scene.catalogStaticDirty &&
    (!scene.catalogStaticRenderer?.projectsClusterStarsInShader || !scene.clusterStarGpuDirty) &&
    scene.catalogStaticRadiusScale === state.radiusScale &&
    scene.catalogStaticExposureSignature === catalogExposureSignature() &&
    scene.catalogStaticPulsationSpeed === state.pulsationSpeed &&
    scene.catalogStaticPulsationAmplitudeScale === state.pulsationAmplitudeScale &&
    scene.catalogStaticPulsatorPreset === currentPulsatorPreset() &&
    scene.catalogStaticPulseLodActive === pulseLodActive &&
    scene.catalogStaticProjectionMode === projectionMode
  );
}

function stampCatalogStaticCache(animatedCatalog, staticCatalog, pulseLodActive = shouldUseCatalogPulseLod()) {
  scene.catalogStaticCounts.animated = animatedCatalog;
  scene.catalogStaticCounts.static = staticCatalog;
  scene.catalogStaticRadiusScale = state.radiusScale;
  scene.catalogStaticExposureSignature = catalogExposureSignature();
  scene.catalogStaticPulsationSpeed = state.pulsationSpeed;
  scene.catalogStaticPulsationAmplitudeScale = state.pulsationAmplitudeScale;
  scene.catalogStaticPulsatorPreset = currentPulsatorPreset();
  scene.catalogStaticPulseLodActive = pulseLodActive;
  scene.catalogStaticProjectionMode = scene.catalogDrawListScreenProjected ? "screen" : "world";
  scene.catalogStaticDirty = false;
  scene.catalogStaticCacheVersion += 1;
}

function drawAnimatedCatalogItems(
  items,
  simulationDay,
  pulseNow = performance.now(),
  useNavigationPulseFloor = false,
) {
  const colorBuckets = scene.colorBuckets;
  clearColorBuckets(colorBuckets);

  for (const item of items) {
    const color = animatedCatalogItemColor(item, simulationDay, pulseNow, useNavigationPulseFloor);
    pushColorBucket(colorBuckets, color, item);
  }

  drawCatalogBuckets(ctx, colorBuckets);
}

function rebuildCatalogGpuStaticLayer(renderer) {
  scene.catalogAnimatedDrawList.length = 0;
  scene.catalogWorldStaticDrawList.length = 0;
  const now = performance.now();
  const usePulseLod = shouldUseCatalogPulseLod(now);
  const useWorldProjectionCache =
    !scene.catalogDrawListScreenProjected &&
    renderer.projectsCatalogDynamicInShader &&
    CATALOG_PULSE_ALL_STARS &&
    !usePulseLod;

  if (useWorldProjectionCache) {
    let animatedCatalog = 0;
    let staticCatalog = 0;
    for (const item of scene.catalogDrawList) {
      updateCatalogStaticStyle(item);
      const animates = shouldAnimateCatalogItem(item, item.staticRadius, item.staticAlpha, usePulseLod);
      item.catalogWorldStaticPulseState = !animates;
      if (animates) {
        animatedCatalog += 1;
        scene.catalogAnimatedDrawList.push(item);
      } else {
        updateStaticCatalogItem(item);
        staticCatalog += 1;
        scene.catalogWorldStaticDrawList.push(item);
      }
    }

    renderer.resize();
    renderer.clear();
    renderer.uploadCatalogStatic(0);
    renderer.drawCatalogStatic();
    const staticWorldCount = renderer.ensureCatalogWorldStatic(scene.catalogWorldStaticDrawList);
    const staticWorldData = renderer.ensureCatalogWorldPulseCapacity(staticWorldCount);
    for (const item of scene.catalogWorldStaticDrawList) {
      const worldIndex = item.catalogWorldPulseIndex;
      if (worldIndex < 0 || worldIndex >= staticWorldCount) continue;
      writeCatalogGpuWorldPulseItemAt(staticWorldData, worldIndex, item, item.currentColor);
    }
    renderer.drawCatalogDynamicWorld(staticWorldCount, [], true);
    if (renderer.projectsClusterStarsInShader) {
      renderer.drawClusterStars();
      staticCatalog += renderer.clusterStarCount;
    }
    stampCatalogStaticCache(animatedCatalog, staticCatalog, usePulseLod);
    renderer.catalogWorldStaticCacheVersion = scene.catalogStaticCacheVersion;
    renderer.catalogWorldPulseCacheVersion = scene.catalogStaticCacheVersion;
    return;
  }

  const data = renderer.ensureCatalogStaticCapacity(scene.catalogDrawList.length);

  let offset = 0;
  let staticCount = 0;
  let animatedCatalog = 0;
  let staticCatalog = 0;

  for (const item of scene.catalogDrawList) {
    updateCatalogStaticStyle(item);
    const animates = shouldAnimateCatalogItem(item, item.staticRadius, item.staticAlpha, usePulseLod);
    if (animates) {
      item.catalogWorldStaticPulseState = false;
      scene.catalogAnimatedDrawList.push(item);
      animatedCatalog += 1;
    } else {
      item.catalogWorldStaticPulseState = true;
      offset = writeCatalogGpuItem(
        data,
        offset,
        item,
        updateStaticCatalogItem(item),
      );
      staticCount += 1;
      staticCatalog += 1;
    }
  }

  renderer.resize();
  renderer.clear();
  renderer.uploadCatalogStatic(staticCount);
  renderer.drawCatalogStatic();
  if (renderer.projectsClusterStarsInShader) {
    renderer.drawClusterStars();
    staticCatalog += renderer.clusterStarCount;
  }
  stampCatalogStaticCache(animatedCatalog, staticCatalog, usePulseLod);
}

function rebuildCatalogStaticLayer() {
  resizeCatalogStaticCanvas();
  clearCatalogStaticCanvas();
  clearColorBuckets(scene.staticColorBuckets);
  scene.catalogAnimatedDrawList.length = 0;
  const now = performance.now();
  const usePulseLod = shouldUseCatalogPulseLod(now);

  let animatedCatalog = 0;
  let staticCatalog = 0;

  for (const item of scene.catalogDrawList) {
    updateCatalogStaticStyle(item);
    const animates = shouldAnimateCatalogItem(item, item.staticRadius, item.staticAlpha, usePulseLod);
    if (animates) {
      item.catalogWorldStaticPulseState = false;
      scene.catalogAnimatedDrawList.push(item);
      animatedCatalog += 1;
    } else {
      item.catalogWorldStaticPulseState = true;
      pushColorBucket(
        scene.staticColorBuckets,
        updateStaticCatalogItem(item),
        item,
      );
      staticCatalog += 1;
    }
  }

  drawCatalogBuckets(scene.catalogStaticCtx, scene.staticColorBuckets);
  stampCatalogStaticCache(animatedCatalog, staticCatalog, usePulseLod);
}

function drawCatalogDirect(
  simulationDay,
  pulseNow = performance.now(),
  useNavigationPulseFloor = false,
) {
  const colorBuckets = scene.colorBuckets;
  clearColorBuckets(colorBuckets);
  const now = pulseNow;
  const usePulseLod = shouldUseCatalogPulseLod(now);
  let animatedCatalog = 0;
  let staticCatalog = 0;

  for (const item of scene.catalogDrawList) {
    updateCatalogStaticStyle(item);
    const animates = shouldAnimateCatalogItem(item, item.staticRadius, item.staticAlpha, usePulseLod);
    let color = item.point.color;
    if (animates) {
      item.catalogWorldStaticPulseState = false;
      color = animatedCatalogItemColor(item, simulationDay, now, useNavigationPulseFloor);
      animatedCatalog += 1;
    } else {
      item.catalogWorldStaticPulseState = true;
      color = updateStaticCatalogItem(item);
      staticCatalog += 1;
    }
    pushColorBucket(colorBuckets, color, item);
  }

  drawCatalogBuckets(ctx, colorBuckets);
  return { animatedCatalog, staticCatalog };
}

function drawCatalogGpu(
  simulationDay,
  pulseNow = performance.now(),
  useNavigationPulseFloor = false,
) {
  const renderer = prepareGpuSceneLayer();
  if (!renderer) return null;
  const staticRenderer = scene.catalogStaticRenderer;
  if (!staticRenderer) return null;

  if (!catalogStaticCacheMatches()) {
    rebuildCatalogGpuStaticLayer(staticRenderer);
  }

  const useWorldProjection = renderer.projectsCatalogDynamicInShader;
  const expectedWorldCount = useWorldProjection
    ? renderer.ensureCatalogWorldStatic(scene.catalogAnimatedDrawList)
    : 0;
  const data = renderer.ensureCatalogCapacity(scene.catalogAnimatedDrawList.length);
  const worldData = useWorldProjection
    ? renderer.ensureCatalogWorldPulseCapacity(expectedWorldCount)
    : null;
  const forceWorldPulseFullUpload =
    useWorldProjection &&
    (renderer.catalogWorldPulseUploadedCount !== expectedWorldCount ||
      renderer.catalogWorldPulseCacheVersion !== scene.catalogStaticCacheVersion);
  const worldDirtyRanges = [];
  let offset = 0;
  let count = 0;

  for (const item of scene.catalogAnimatedDrawList) {
    const needsScreenProjection =
      scene.catalogDrawListScreenProjected && catalogDynamicItemNeedsScreenProjection(item);
    if (useWorldProjection && !needsScreenProjection) {
      const worldIndex = item.catalogWorldPulseIndex;
      if (worldIndex < 0 || worldIndex >= expectedWorldCount) continue;
      const refreshed = item.catalogWorldStaticPulseState
        ? Boolean(forceWorldPulseFullUpload || !animatedCatalogPulseStateValid(item))
        : updateAnimatedCatalogPulseStateIfNeeded(
            item,
            simulationDay,
            pulseNow,
            useNavigationPulseFloor,
          );
      if (item.catalogWorldStaticPulseState && refreshed) updateStaticCatalogItem(item);
      if (forceWorldPulseFullUpload || refreshed) {
        writeCatalogGpuWorldPulseItemAt(worldData, worldIndex, item, item.currentColor);
        if (!forceWorldPulseFullUpload) appendCatalogWorldPulseDirtyRange(worldDirtyRanges, worldIndex);
      }
    } else {
      const color = animatedCatalogItemColor(item, simulationDay, pulseNow, useNavigationPulseFloor);
      offset = writeCatalogGpuItem(data, offset, item, color);
      count += 1;
    }
  }

  renderer.drawCatalogDynamicWorld(expectedWorldCount, worldDirtyRanges, forceWorldPulseFullUpload);
  renderer.drawCatalogDynamic(count);
  return {
    animatedCatalog: scene.catalogStaticCounts.animated,
    staticCatalog: scene.catalogStaticCounts.static,
  };
}

function drawCatalog(useStaticCache = true) {
  const catalogStartMs = PERF_HUD_ENABLED ? performance.now() : 0;
  const simulationDay = currentSimulationDay();
  const pulseNow = performance.now();
  const useNavigationPulseFloor = navigationPulseRefreshFloorActive(pulseNow);
  let animatedCatalog = 0;
  let staticCatalog = 0;

  const gpuResult = drawCatalogGpu(simulationDay, pulseNow, useNavigationPulseFloor);
  if (gpuResult) {
    ({ animatedCatalog, staticCatalog } = gpuResult);
  } else {
    if (!scene.catalogDrawListScreenProjected) rebuildProjectionCache({ forceCatalogProjection: true });
    if (useStaticCache && PULSE_LOD_ENABLED && catalogStaticCacheMatches()) {
      if (scene.catalogStaticDirty) rebuildCatalogStaticLayer();
      ctx.drawImage(scene.catalogStaticCanvas, 0, 0, scene.width, scene.height);
      animatedCatalog = scene.catalogStaticCounts.animated;
      staticCatalog = scene.catalogStaticCounts.static;
      drawAnimatedCatalogItems(
        scene.catalogAnimatedDrawList,
        simulationDay,
        pulseNow,
        useNavigationPulseFloor,
      );
    } else if (useStaticCache && PULSE_LOD_ENABLED) {
      rebuildCatalogStaticLayer();
      ctx.drawImage(scene.catalogStaticCanvas, 0, 0, scene.width, scene.height);
      animatedCatalog = scene.catalogStaticCounts.animated;
      staticCatalog = scene.catalogStaticCounts.static;
      drawAnimatedCatalogItems(
        scene.catalogAnimatedDrawList,
        simulationDay,
        pulseNow,
        useNavigationPulseFloor,
      );
    } else {
      ({ animatedCatalog, staticCatalog } = drawCatalogDirect(
        simulationDay,
        pulseNow,
        useNavigationPulseFloor,
      ));
    }
  }

  if (PERF_HUD_ENABLED) {
    updatePerfHud({
      catalogMs: performance.now() - catalogStartMs,
      animatedCatalog,
      staticCatalog,
    });
  }
  return scene.cachedStats.catalog;
}

function targetProjectedAtZoom(target, zoom = state.zoom) {
  const coordinates = coordinatesForPoint(target);
  const transform = makeProjectionTransform(baseSceneScaleForZoom(zoom));
  return projectOffsetWithTransform(coordinates[0], coordinates[1], coordinates[2], transform);
}

function clusterGlowOuterRadiusFromCoreRadius(coreRadius, outerRadiusFraction = 1) {
  const profileRadius = Math.max(7, coreRadius * CLUSTER_GLOW_RADIUS_SCALE * Math.max(1, outerRadiusFraction));
  return profileRadius * (1 + CLUSTER_GLOW_EDGE_FEATHER);
}

function clusterCoreRadiusAtZoom(target, projected, zoom = state.zoom, { bounded = false } = {}) {
  const physicalRadius = (target.radiusPc / 1000) * baseSceneScaleForZoom(zoom) * projected.perspective;
  return bounded ? clamp(physicalRadius, 8, 260) : Math.max(8, physicalRadius);
}

function catalogTargetVisualRadiusAtZoom(target, projected, zoom = state.zoom) {
  return catalogDeepZoomVisualRadiusAtZoom(target, projected, zoom, catalogMaxAreaPulse(target));
}

function clusterTargetVisualRadiusAtZoom(target, projected, zoom = state.zoom) {
  const physicalRadius = clusterCoreRadiusAtZoom(target, projected, zoom);
  return Math.max(CLUSTER_TARGET_SELECTION_MIN_RADIUS, physicalRadius * CLUSTER_TARGET_SELECTION_RADIUS_SCALE);
}

function redClumpTargetVisualRadiusAtZoom(projected, zoom = state.zoom) {
  const radiusUnit = pointRadiusUnitFromStellarRadius(RED_CLUMP_RADIUS);
  return pointRadiusFromUnitAtPerspective(radiusUnit, projected.perspective, pointRadiusZoomSizeForZoom(zoom));
}

function targetVisualRadiusAtZoom(target, zoom = state.zoom) {
  if (!target) return 0;
  const projected = targetProjectedAtZoom(target, zoom);
  if (target.kind === "catalog") return catalogTargetVisualRadiusAtZoom(target, projected, zoom);
  if (target.kind === "cluster") return clusterTargetVisualRadiusAtZoom(target, projected, zoom);
  if (target.kind === "redclump") return redClumpTargetVisualRadiusAtZoom(projected, zoom);
  return TARGET_SELECTION_RING_MIN_RADIUS;
}

function targetSelectionRadiusAtZoom(target, zoom = state.zoom) {
  return Math.max(
    TARGET_SELECTION_RING_MIN_RADIUS,
    targetVisualRadiusAtZoom(target, zoom) + TARGET_SELECTION_RING_PADDING_PX,
  );
}

function drawSelection(target) {
  if (!target) return;
  const coordinates = coordinatesForPoint(target);
  const projected = projectPoint(coordinates[0], coordinates[1], coordinates[2]);
  const radius = targetSelectionRadiusAtZoom(target, state.zoom);
  if (!withinViewport(projected, radius + 8)) return;

  const context = selectionCtx || ctx;
  context.save();
  context.lineWidth = 1.5;
  context.strokeStyle = state.locked === target ? "rgba(252, 163, 17, 0.95)" : "rgba(255, 255, 255, 0.9)";
  context.beginPath();
  context.arc(projected.x, projected.y, radius, 0, Math.PI * 2);
  context.stroke();
  context.restore();
}

function maybeStartIntroCloudLabels(now = performance.now()) {
  if (!introCloudLabelAnimation || introCloudLabelAnimation.startMs !== null) return;
  if (radiansToRawDegrees(state.yaw) < INTRO_CLOUD_LABEL_TRIGGER_YAW_DEGREES) return;
  introCloudLabelAnimation.startMs = now;
}

function introCloudLabelAlpha(now = performance.now()) {
  if (!introCloudLabelAnimation || introCloudLabelAnimation.startMs === null) return 0;

  const elapsed = now - introCloudLabelAnimation.startMs;
  if (elapsed >= INTRO_CLOUD_LABEL_TOTAL_MS) {
    introCloudLabelAnimation = null;
    return 0;
  }

  if (elapsed < INTRO_CLOUD_LABEL_FADE_IN_MS) {
    return smoothStep(elapsed / INTRO_CLOUD_LABEL_FADE_IN_MS);
  }

  const fadeOutStart = INTRO_CLOUD_LABEL_FADE_IN_MS + INTRO_CLOUD_LABEL_HOLD_MS;
  if (elapsed < fadeOutStart) return 1;

  const fadeOutElapsed = elapsed - fadeOutStart;
  return 1 - smoothStep(fadeOutElapsed / INTRO_CLOUD_LABEL_FADE_OUT_MS);
}

function introCloudLabelPoint(projected, spec, labelWidth) {
  const margin = 22;
  const x = projected.x + spec.offsetX;
  const y = projected.y + spec.offsetY;
  const minX = spec.textAlign === "right" ? margin + labelWidth : margin;
  const maxX = spec.textAlign === "right" ? scene.width - margin : scene.width - margin - labelWidth;

  return {
    x: clamp(x, minX, maxX),
    y: clamp(y, margin + 18, scene.height - margin),
  };
}

function drawIntroCloudLabels(timestamp = performance.now()) {
  const alpha = introCloudLabelAlpha(timestamp);
  if (alpha <= 0.001) return;

  const centers = scene.coordinateContext?.centers;
  const reference = activeCoordinateReference().context;
  if (!centers || !reference) return;

  const context = selectionCtx || ctx;
  context.save();
  context.globalAlpha = alpha;
  context.font = "800 28px Inter, system-ui, sans-serif";
  context.textBaseline = "bottom";
  context.fillStyle = "rgba(255, 255, 255, 0.96)";
  context.shadowColor = "rgba(252, 163, 17, 0.5)";
  context.shadowBlur = 14;

  for (const spec of INTRO_CLOUD_LABELS) {
    const center = centers[spec.id];
    if (!center) continue;
    const coordinates = coordinatesForSkyGridVector(center.galacticVector, reference);
    const projected = projectPoint(coordinates[0], coordinates[1], coordinates[2]);
    if (!withinViewport(projected, 160)) continue;

    context.textAlign = spec.textAlign;
    const labelWidth = context.measureText(spec.text).width;
    const point = introCloudLabelPoint(projected, spec, labelWidth);
    context.fillText(spec.text, point.x, point.y);
  }

  context.restore();
}

function render(timestamp) {
  updatePulsationClock();
  if (!scene.payload) return;
  updateIntroRotation(timestamp);
  updateAxisSpinAnimation(timestamp);

  ctx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
  ctx.clearRect(0, 0, scene.width, scene.height);
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, scene.width, scene.height);
  drawBackgroundStars();
  drawGrid(timestamp);

  let forceExactProjectionRebuild = false;
  if (!projectionDirty && scene.catalogProjectionFastPending && !navigationActivityActive(timestamp)) {
    projectionDirty = true;
    forceExactProjectionRebuild = true;
  }

  let rebuiltProjection = false;
  if (projectionDirty) {
    if (!forceExactProjectionRebuild) markNavigationActivityActive(timestamp);
    rebuildProjectionCache({ forceCatalogProjection: forceExactProjectionRebuild });
    rebuiltProjection = true;
  }
  drawClusterGlows();
  beginGpuSceneLayer();
  const redStats = drawRedClump(rebuiltProjection);
  const catalogStats = drawCatalog(!rebuiltProjection);
  endGpuSceneLayer();
  clearSelectionOverlay();
  drawSkyCoordinateGrids();
  drawSelection(state.locked || state.hovered);
  drawIntroCloudLabels(timestamp);

  const visibleTotal = redStats.count + catalogStats.count;
  const minDepth = Math.min(redStats.minDepth, catalogStats.minDepth);
  const maxDepth = Math.max(redStats.maxDepth, catalogStats.maxDepth);
  outputs.visibleTotal.textContent = formatInteger(visibleTotal);
  outputs.depthSpan.textContent = Number.isFinite(minDepth) ? formatNumber(Math.abs(maxDepth - minDepth), 0) : "0";
  updateLightcurveInset();
  queueRender();
}

async function prewarmIntroFrame() {
  if (!scene.payload) return;
  updatePulsationClock();
  rebuildProjectionCache();
  drawClusterGlows();
  beginGpuSceneLayer();
  drawRedClump(true);
  drawCatalog(false);
  endGpuSceneLayer();
  await nextFrame();
}

function drawBackgroundStars() {
  ctx.save();
  ctx.globalAlpha = 0.4;
  ctx.fillStyle = "#e5e5e5";
  const count = Math.floor((scene.width * scene.height) / 26000);
  for (let index = 0; index < count; index += 1) {
    const x = (hashString(`x${index}`) % 10000) / 10000;
    const y = (hashString(`y${index}`) % 10000) / 10000;
    const brightness = ((hashString(`b${index}`) % 100) / 100) * 0.55 + 0.15;
    ctx.globalAlpha = brightness * 0.28;
    ctx.fillRect(x * scene.width, y * scene.height, 1, 1);
  }
  ctx.restore();
}

function syncRangeProgress(input) {
  if (!input || input.type !== "range") return;
  const min = Number(input.min || 0);
  const max = Number(input.max || 100);
  const value = Number(input.value);
  const progress = Number.isFinite(min) && Number.isFinite(max) && Number.isFinite(value) && max !== min
    ? clamp(((value - min) / (max - min)) * 100, 0, 100)
    : 50;
  input.style.setProperty("--range-progress", `${progress}%`);
}

function syncOrientationPresetButtons() {
  const faceActive = orbitAnglesMatchPreset(FACE_VIEW_ANGLES_DEGREES);
  const edgeActive = orbitAnglesMatchPreset(EDGE_VIEW_ANGLES_DEGREES);
  if (elements.faceView) {
    elements.faceView.classList.toggle("active", faceActive);
    elements.faceView.setAttribute("aria-pressed", String(faceActive));
  }
  if (elements.edgeView) {
    elements.edgeView.classList.toggle("active", edgeActive);
    elements.edgeView.setAttribute("aria-pressed", String(edgeActive));
  }
}

function syncRangeOutputs() {
  state.zoom = clampZoomScale(state.zoom, { allowTargetZoom: Boolean(selectedTargetForDeepZoom()) });
  state.radiusScale = clampRadiusScale(state.radiusScale);
  state.colorContrast = clampColorContrast(state.colorContrast);
  setPulsationSpeed(state.pulsationSpeed);
  state.pulsationAmplitudeScale = clampPulsationAmplitudeScale(state.pulsationAmplitudeScale);
  syncEditableMultiplierOutput("yaw", radiansToDegrees(state.yaw));
  syncEditableMultiplierOutput("pitch", radiansToDegrees(state.pitch));
  syncEditableMultiplierOutput("roll", radiansToDegrees(state.roll));
  syncEditableMultiplierOutput("zoom", state.zoom);
  syncEditableMultiplierOutput("radiusScale", state.radiusScale);
  syncEditableMultiplierOutput("colorContrast", state.colorContrast);
  syncEditableMultiplierOutput("uncertaintySeed", state.uncertaintySeed);
  syncEditableMultiplierOutput("pulsationSpeed", state.pulsationSpeed);
  syncEditableMultiplierOutput("pulsationAmplitude", state.pulsationAmplitudeScale);
  outputs.pulsationDaySeconds.textContent = `1 d = ${formatPulsationDuration(
    SECONDS_PER_DAY / state.pulsationSpeed,
  )}`;

  controls.yaw.value = String(radiansToDegrees(state.yaw));
  controls.pitch.value = String(radiansToDegrees(state.pitch));
  controls.roll.value = String(radiansToDegrees(state.roll));
  controls.zoom.value = String(Math.log10(clampZoomScale(state.zoom)));
  controls.radiusScale.value = String(Math.log10(state.radiusScale));
  controls.colorContrast.value = String(state.colorContrast);
  controls.uncertaintySeed.value = String(state.uncertaintySeed);
  controls.pulsationSpeed.value = String(state.pulsationSpeedLog);
  controls.pulsationAmplitude.value = String(Math.log10(state.pulsationAmplitudeScale));
  [
    controls.yaw,
    controls.pitch,
    controls.roll,
    controls.zoom,
    controls.radiusScale,
    controls.colorContrast,
    controls.uncertaintySeed,
    controls.pulsationSpeed,
    controls.pulsationAmplitude,
  ].forEach(syncRangeProgress);
  syncDatasetExposureSliders();
  controls.panLock.checked = state.panLock;
  const equatorialGrid = document.querySelector("#equatorialGrid");
  const galacticGrid = document.querySelector("#galacticGrid");
  if (equatorialGrid) equatorialGrid.checked = state.equatorialGrid;
  if (galacticGrid) galacticGrid.checked = state.galacticGrid;
  syncOrientationPresetButtons();
  syncDatasetPresetButtons();
  syncDatasetPresetToggle();
}

function syncDatasetCheckboxes() {
  document.querySelectorAll("[data-dataset]").forEach((input) => {
    const datasetKey = input.dataset.dataset;
    if (datasetKey === "cepheids") {
      const visibleCepheidKeys = CEPHEID_DATASET_KEYS.filter((key) => state.datasets[key]);
      input.checked = visibleCepheidKeys.length > 0;
      input.indeterminate = visibleCepheidKeys.length > 0 && visibleCepheidKeys.length < CEPHEID_DATASET_KEYS.length;
      return;
    }
    input.checked = Boolean(state.datasets[datasetKey]);
    input.indeterminate = false;
  });
}

function defaultDatasetExposureValue(datasetKey) {
  return datasetKey === "redclump" ? RED_CLUMP_EXPOSURE_DEFAULT : DATASET_EXPOSURE_DEFAULT;
}

function datasetExposureValue(datasetKey) {
  return clampDatasetExposure(state.datasetExposure[datasetKey] ?? defaultDatasetExposureValue(datasetKey));
}

function redClumpRenderExposureValue() {
  return datasetExposureValue("redclump") * RED_CLUMP_EXPOSURE_RENDER_SCALE;
}

function syncDatasetExposureSliders() {
  document.querySelectorAll("[data-exposure]").forEach((input) => {
    input.value = String(Math.log10(datasetExposureValue(input.dataset.exposure)));
    syncRangeProgress(input);
  });
}

function setDatasetExposure(datasetKey, value) {
  const exposure = clampDatasetExposure(value);
  if (datasetKey === "cepheids") {
    CEPHEID_DATASET_KEYS.forEach((key) => {
      state.datasetExposure[key] = exposure;
    });
  } else {
    state.datasetExposure[datasetKey] = exposure;
  }

  if (datasetKey === "redclump") {
    markRedClumpLayerDirty();
  } else {
    markCatalogStaticDirty();
  }
  syncDatasetExposureSliders();
  queueRender();
}

function datasetExposureForPoint(point) {
  if (point?.kind === "catalog") return datasetExposureValue(DATASET_KEYS[point.row[IDX.dataset]]);
  if (point?.kind === "cluster" || point?.kind === "clusterStar") return datasetExposureValue("clusters");
  if (point?.kind === "redclump") return redClumpRenderExposureValue();
  return DATASET_EXPOSURE_DEFAULT;
}

function catalogExposureSignature() {
  return ["cepheids", "rrlyrae", "anomalousCepheids", "miras", "clusters"]
    .map((key) => `${key}:${datasetExposureValue(key).toFixed(4)}`)
    .join("|");
}

function cepheidDatasetsVisible() {
  return CEPHEID_DATASET_KEYS.some((key) => state.datasets[key]);
}

function setDatasetVisibility(datasetKey, visible) {
  if (datasetKey === "cepheids") {
    CEPHEID_DATASET_KEYS.forEach((key) => {
      state.datasets[key] = visible;
    });
    return;
  }
  state.datasets[datasetKey] = visible;
}

function activeDatasetPreset() {
  return DATASET_PRESETS.includes(state.datasetPreset) ? state.datasetPreset : null;
}

function committedDatasetPresetForPicking() {
  if (!datasetPresetPreview) return activeDatasetPreset();
  const preset = datasetPresetPreview.snapshot.datasetPreset;
  return DATASET_PRESETS.includes(preset) ? preset : null;
}

function syncDatasetPresetButtons() {
  const activePreset = datasetPresetPreview
    ? DATASET_PRESETS.includes(datasetPresetPreview.snapshot.datasetPreset)
      ? datasetPresetPreview.snapshot.datasetPreset
      : null
    : activeDatasetPreset();
  document.querySelectorAll("[data-dataset-preset]").forEach((button) => {
    const preset = button.dataset.datasetPreset;
    const active = preset === activePreset;
    const label = DATASET_PRESET_LABELS[preset] || button.textContent.trim();
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
    button.setAttribute("aria-label", active ? `${label} preset active` : `Preview or activate ${label} preset`);
    const shortcutKey = Object.entries(KEYBOARD_DATASET_PRESETS).find(([, presetKey]) => presetKey === preset)?.[0];
    if (shortcutKey) button.setAttribute("aria-keyshortcuts", shortcutKey);
    button.title = active ? `${label} preset active` : `Preview or activate ${label} preset`;
  });
}

function syncDatasetPresetToggle() {
  const buttons = [controls.datasetPresetToggle, controls.mobilePresetToggle].filter(Boolean);
  if (!buttons.length) return;

  const preset = currentPulsatorPreset();
  const nextPreset = nextPulsatorPreset();
  const currentLabel = PULSATOR_PRESETS.includes(preset) ? PULSATOR_PRESET_LABELS[preset] : null;
  const nextLabel =
    nextPreset === PULSATOR_DEFAULT_PRESET ? "default" : PULSATOR_PRESET_LABELS[nextPreset] || "Cepheids";
  const label = currentLabel
    ? `${currentLabel} preset active. Switch to ${nextLabel} preset`
    : `Switch to ${nextLabel} preset`;
  for (const button of buttons) {
    button.classList.toggle("active", PULSATOR_PRESETS.includes(preset));
    button.setAttribute("aria-pressed", String(PULSATOR_PRESETS.includes(preset)));
    button.setAttribute("aria-label", label);
    button.title = label;
  }
}

function updateCoordinateReadout() {
  if (!elements.coordinateReadout) return;
  const frame = activeCoordinateFrame();
  const sample = coordinateReadoutSample();
  elements.coordinateReadout.replaceChildren();

  const buildGridToggle = (label, gridToggle) => {
    const toggle = document.createElement("label");
    toggle.className = "coordinateGridToggle";
    toggle.title = gridToggle.title;

    const input = document.createElement("input");
    input.id = gridToggle.id;
    input.type = "checkbox";
    input.dataset.skyGrid = gridToggle.gridKey;
    input.checked = gridToggle.checked;
    input.setAttribute("aria-label", gridToggle.title);
    input.setAttribute("aria-keyshortcuts", "G");

    const text = document.createElement("span");
    text.textContent = label;

    toggle.append(input, text);
    return toggle;
  };

  const buildSkyCoordinate = (label, valueText) => {
    const item = document.createElement("span");
    item.className = "skyCoordinate";
    const symbol = document.createElement("b");
    symbol.textContent = label;
    const value = document.createElement("strong");
    value.textContent = valueText;
    item.append(symbol, value);
    return item;
  };

  const buildReadoutGroup = (...children) => {
    const group = document.createElement("div");
    group.className = "coordinateReadoutGroup";
    group.append(...children);
    return group;
  };

  const skyRow = document.createElement("div");
  skyRow.className = "coordinateSkyRow";
  skyRow.append(
    buildReadoutGroup(
      buildGridToggle("ECS", {
        id: "equatorialGrid",
        gridKey: "equatorial",
        checked: state.equatorialGrid,
        title: "Show RA/Dec grid lines",
      }),
      buildSkyCoordinate("RA", `${formatNumber(sample.sky.ra, 3)}°`),
      buildSkyCoordinate("Dec", `${formatNumber(sample.sky.dec, 3)}°`),
    ),
    buildReadoutGroup(
      buildGridToggle("GCS", {
        id: "galacticGrid",
        gridKey: "galactic",
        checked: state.galacticGrid,
        title: "Show Galactic coordinate grid lines",
      }),
      buildSkyCoordinate("l", `${formatNumber(sample.sky.lon, 3)}°`),
      buildSkyCoordinate("b", `${formatNumber(sample.sky.lat, 3)}°`),
    ),
  );
  elements.coordinateReadout.append(skyRow);

  const localRow = document.createElement("div");
  localRow.className = "coordinateLocalRow";
  frame.axes.forEach((axis, index) => {
    const item = document.createElement("span");
    item.className = "localCoordinate";
    const symbol = document.createElement("b");
    symbol.textContent = axis[0];

    const value = document.createElement("strong");
    value.textContent = formatKpcValue(sample.local[index], 1);

    item.append(symbol, ` ${axis[1]} `, value);
    localRow.append(item);
  });
  elements.coordinateReadout.append(localRow);
}

function syncCoordinateFrameControls() {
  if (elements.coordinateFrames) {
    elements.coordinateFrames.querySelectorAll("input[type='radio']").forEach((input) => {
      input.checked = input.value === state.coordinateFrame;
    });
  }
  if (elements.coordinateCenters) {
    elements.coordinateCenters.querySelectorAll("input[type='radio']").forEach((input) => {
      input.checked = input.value === state.centerSelection;
    });
  }
  updateCoordinateReadout();
}

function setCoordinateFrame(frameId) {
  if (!COORDINATE_FRAME_BY_ID.has(frameId) || state.coordinateFrame === frameId) return;
  state.coordinateFrame = frameId;
  applyCoordinateChange();
}

function setCoordinateCenter(centerId) {
  if (!COORDINATE_CENTER_BY_ID.has(centerId)) return;
  if (state.coordinateCenter === centerId && state.centerSelection === centerId) return;
  state.coordinateCenter = centerId;
  state.centerSelection = centerId;
  state.customCoordinateContext = null;
  lastTargetNavigationStep = null;
  state.locked = null;
  state.hovered = null;
  state.cameraLocked = false;
  state.cameraFollowsLockedTarget = false;
  clearActiveLightcurveInsets();
  applyCoordinateChange();
}

function clearCoordinateCenterSelection() {
  if (state.centerSelection === null) return;
  state.centerSelection = null;
  syncCoordinateFrameControls();
}

function clearCenterSelectionForTarget(target, { preserveScreenPosition = false, previousReference = null } = {}) {
  if (!state.cameraLocked || !target?.coordinates?.galacticVector) return;

  const base = getBaseSceneLayout();
  const transform = makeProjectionTransform(base.scale);
  const referenceBeforeChange = previousReference || activeCoordinateReference();
  const previousCoordinates = preserveScreenPosition ? coordinatesForReference(target, referenceBeforeChange) : null;
  const previousProjected = previousCoordinates
    ? projectOffsetWithTransform(previousCoordinates[0], previousCoordinates[1], previousCoordinates[2], transform)
    : null;

  state.customCoordinateContext = centerContext(target.coordinates.galacticVector);
  clearCoordinateCenterSelection();

  if (previousProjected) {
    const nextCoordinates = coordinatesForReference(target, { context: state.customCoordinateContext });
    const nextProjected = projectOffsetWithTransform(nextCoordinates[0], nextCoordinates[1], nextCoordinates[2], transform);
    state.panX += previousProjected.x - nextProjected.x;
    state.panY += previousProjected.y - nextProjected.y;
  }
}

function applyCoordinateChange() {
  markOrientationGridActive();
  state.panX = 0;
  state.panY = 0;
  updateSceneLayout();
  syncCoordinateFrameControls();
  setTarget(state.locked || state.hovered);
  markProjectionDirty();
}

function buildCoordinateControls() {
  const buildRadio = (item, name, checkedValue, clickHandler) => {
    const label = document.createElement("label");
    label.className = "coordinateOption";

    const input = document.createElement("input");
    input.type = "radio";
    input.name = name;
    input.value = item.id;
    input.checked = item.id === checkedValue;
    input.addEventListener("change", () => {
      if (input.checked) clickHandler(item.id);
    });

    const text = document.createElement("span");
    text.textContent = item.label;

    label.append(input, text);
    return label;
  };

  if (elements.coordinateFrames) {
    elements.coordinateFrames.replaceChildren();
    elements.coordinateFrames.setAttribute("role", "radiogroup");
    elements.coordinateFrames.setAttribute("aria-label", "Coordinate frame");
    for (const frame of COORDINATE_FRAMES) {
      elements.coordinateFrames.append(buildRadio(frame, "coordinate-frame", state.coordinateFrame, setCoordinateFrame));
    }
  }

  if (elements.coordinateCenters) {
    elements.coordinateCenters.replaceChildren();
    elements.coordinateCenters.setAttribute("role", "radiogroup");
    elements.coordinateCenters.setAttribute("aria-label", "Coordinate center");
    for (const center of COORDINATE_CENTERS) {
      elements.coordinateCenters.append(buildRadio(center, "coordinate-center", state.centerSelection, setCoordinateCenter));
    }
  }
  syncCoordinateFrameControls();
}

function targetDatasetIsVisible(target) {
  if (!target) return true;
  if (target.kind === "redclump") return state.datasets.redclump;
  if (target.kind === "cluster" || target.kind === "clusterStar") return state.datasets.clusters;
  return state.datasets[DATASET_KEYS[target.row[IDX.dataset]]];
}

function targetMatchesActiveDatasetPreset(target) {
  const preset = committedDatasetPresetForPicking();
  if (!preset || !target) return true;

  if (preset === "clusters") return target.kind === "cluster" || target.kind === "clusterStar";
  if (preset === "redclump") return target.kind === "redclump";
  if (target.kind !== "catalog") return false;

  return (PULSATOR_PRESET_DATASET_KEYS[preset] || []).includes(DATASET_KEYS[target.row[IDX.dataset]]);
}

function targetIsPickable(target) {
  if (target?.kind === "redclump") return false;
  return targetDatasetIsVisible(target) && targetMatchesActiveDatasetPreset(target);
}

function clearHiddenTargetSelection() {
  if (state.locked && !targetIsPickable(state.locked)) {
    clearTargetSelection();
    return;
  }

  if (!state.locked && state.hovered && !targetIsPickable(state.hovered)) {
    state.hovered = null;
    setTarget(null);
  }
}

function pulsationSpeedForPreset(preset) {
  return clampPulsationSpeed(PULSATOR_PRESET_SPEEDS[preset] || INITIAL_PULSATION_SPEED);
}

function currentPulsatorPreset() {
  if (PULSATOR_PRESETS.includes(state.pulsatorPreset)) return state.pulsatorPreset;
  return PULSATOR_DEFAULT_PRESET;
}

function nextPulsatorPreset() {
  const index = PULSATOR_PRESET_SEQUENCE.indexOf(currentPulsatorPreset());
  return PULSATOR_PRESET_SEQUENCE[(index + 1) % PULSATOR_PRESET_SEQUENCE.length];
}

function defaultRadiusScaleForPreset(preset = currentPulsatorPreset()) {
  return clampRadiusScale(PULSATOR_PRESET_RADIUS_SCALES[preset] || PULSATOR_PRESET_RADIUS_SCALES.default);
}

function defaultPulsationAmplitudeScaleForPreset(preset = currentPulsatorPreset()) {
  return clampPulsationAmplitudeScale(
    PULSATOR_PRESET_AMPLITUDE_SCALES[preset] || PULSATION_AMPLITUDE_DEFAULT,
  );
}

function defaultPulsationSpeedForPreset(preset = currentPulsatorPreset()) {
  if (PULSATOR_PRESETS.includes(preset)) return pulsationSpeedForPreset(preset);
  return INITIAL_PULSATION_SPEED;
}

function highlightExposureForPulsatorPreset(preset) {
  return clampDatasetExposure(
    PULSATOR_PRESET_HIGHLIGHT_EXPOSURES[preset] || PULSATOR_PRESET_HIGHLIGHT_EXPOSURE,
  );
}

function contextExposureForPulsatorPreset(preset) {
  return clampDatasetExposure(
    preset === "rrlyrae" ? RR_LYRAE_PRESET_CONTEXT_EXPOSURE : PULSATOR_PRESET_CONTEXT_EXPOSURE,
  );
}

function contextExposureForDatasetPreset(datasetKey, preset = null) {
  if (preset === "redclump") {
    return DATASET_EXPOSURE_MIN;
  }
  if (preset === "clusters" && datasetKey === "redclump") {
    return CLUSTERS_PRESET_RED_CLUMP_CONTEXT_EXPOSURE;
  }
  if (preset === "clusters" && DATASET_KEYS.includes(datasetKey)) {
    return clampDatasetExposure(CLUSTERS_PRESET_PULSATOR_CONTEXT_EXPOSURE);
  }
  return clampDatasetExposure(
    datasetKey === "clusters" ? CLUSTER_PRESET_CONTEXT_EXPOSURE : PULSATOR_PRESET_CONTEXT_EXPOSURE,
  );
}

function highlightExposureForDatasetPreset(datasetKey, preset = null) {
  if (preset === "clusters" && datasetKey === "clusters") {
    return DATASET_EXPOSURE_MAX;
  }
  if (preset === "clusters" && datasetKey === "redclump") {
    return CLUSTERS_PRESET_RED_CLUMP_CONTEXT_EXPOSURE;
  }
  return preset === "redclump" && datasetKey === "redclump"
    ? RED_CLUMP_PRESET_HIGHLIGHT_EXPOSURE
    : DATASET_EXPOSURE_DEFAULT;
}

function syncDatasetPresetStateChange() {
  syncDatasetCheckboxes();
  syncRangeOutputs();
  invalidateActivePointLists();
  clearHiddenTargetSelection();
  markCatalogStaticDirty();
  markRedClumpLayerDirty();
  markProjectionDirty();
}

function applyPulsatorPreset(preset) {
  if (!PULSATOR_PRESET_SEQUENCE.includes(preset)) return;
  if (preset === PULSATOR_DEFAULT_PRESET) {
    state.datasetPreset = null;
    state.pulsatorPreset = null;
    DATASET_PRESET_EXPOSURE_KEYS.forEach((datasetKey) => {
      state.datasets[datasetKey] = true;
      state.datasetExposure[datasetKey] = defaultDatasetExposureValue(datasetKey);
    });
    state.radiusScale = defaultRadiusScaleForPreset(preset);
    state.pulsationAmplitudeScale = defaultPulsationAmplitudeScaleForPreset(preset);
    setPulsationSpeed(defaultPulsationSpeedForPreset(preset));
    syncDatasetPresetStateChange();
    return;
  }

  state.datasetPreset = PULSATOR_PRESETS.includes(preset) ? preset : null;
  state.pulsatorPreset = PULSATOR_PRESETS.includes(preset) ? preset : null;
  PULSATOR_PRESETS.forEach((presetKey) => {
    const exposure =
      preset === PULSATOR_DEFAULT_PRESET
        ? DATASET_EXPOSURE_DEFAULT
        : presetKey === preset
          ? highlightExposureForPulsatorPreset(presetKey)
          : contextExposureForPulsatorPreset(preset);
    for (const datasetKey of PULSATOR_PRESET_DATASET_KEYS[presetKey]) {
      state.datasets[datasetKey] = true;
      state.datasetExposure[datasetKey] = exposure;
    }
  });
  state.datasets.clusters = true;
  state.datasetExposure.clusters =
    preset === PULSATOR_DEFAULT_PRESET ? DATASET_EXPOSURE_DEFAULT : CLUSTER_PRESET_CONTEXT_EXPOSURE;
  state.radiusScale = defaultRadiusScaleForPreset(preset);
  state.pulsationAmplitudeScale = defaultPulsationAmplitudeScaleForPreset(preset);
  setPulsationSpeed(defaultPulsationSpeedForPreset(preset));

  syncDatasetPresetStateChange();
}

function applyAuxiliaryDatasetPreset(preset) {
  if (!AUXILIARY_DATASET_PRESETS.includes(preset)) return;

  const highlightedKeys = new Set(AUXILIARY_DATASET_PRESET_KEYS[preset] || []);
  state.datasetPreset = preset;
  state.pulsatorPreset = null;
  DATASET_PRESET_EXPOSURE_KEYS.forEach((datasetKey) => {
    state.datasets[datasetKey] = true;
    state.datasetExposure[datasetKey] = highlightedKeys.has(datasetKey)
      ? highlightExposureForDatasetPreset(datasetKey, preset)
      : contextExposureForDatasetPreset(datasetKey, preset);
  });

  state.radiusScale = defaultRadiusScaleForPreset(PULSATOR_DEFAULT_PRESET);
  state.pulsationAmplitudeScale = defaultPulsationAmplitudeScaleForPreset(PULSATOR_DEFAULT_PRESET);
  setPulsationSpeed(defaultPulsationSpeedForPreset(PULSATOR_DEFAULT_PRESET));

  syncDatasetPresetStateChange();
}

function applyDatasetPreset(preset) {
  if (PULSATOR_PRESET_SEQUENCE.includes(preset)) {
    applyPulsatorPreset(preset);
  } else if (AUXILIARY_DATASET_PRESETS.includes(preset)) {
    applyAuxiliaryDatasetPreset(preset);
  }
}

function snapshotDatasetPresetState() {
  return {
    datasetPreset: state.datasetPreset,
    pulsatorPreset: state.pulsatorPreset,
    datasets: { ...state.datasets },
    datasetExposure: { ...state.datasetExposure },
    radiusScale: state.radiusScale,
    pulsationAmplitudeScale: state.pulsationAmplitudeScale,
    pulsationSpeed: state.pulsationSpeed,
    pulsationSpeedLog: state.pulsationSpeedLog,
  };
}

function restoreDatasetPresetState(snapshot) {
  state.datasetPreset = snapshot.datasetPreset;
  state.pulsatorPreset = snapshot.pulsatorPreset;
  state.datasets = { ...snapshot.datasets };
  state.datasetExposure = { ...snapshot.datasetExposure };
  state.radiusScale = snapshot.radiusScale;
  state.pulsationAmplitudeScale = snapshot.pulsationAmplitudeScale;
  setPulsationSpeed(snapshot.pulsationSpeed);
  syncDatasetPresetStateChange();
}

function beginDatasetPresetPreview(preset) {
  if (!DATASET_PRESETS.includes(preset)) return;
  if (datasetPresetPreview?.preset === preset) return;
  endDatasetPresetPreview(null, { restore: true });
  datasetPresetPreview = {
    preset,
    snapshot: snapshotDatasetPresetState(),
  };
  applyDatasetPreset(preset);
}

function endDatasetPresetPreview(preset, { restore = true } = {}) {
  if (!datasetPresetPreview) return;
  if (preset && datasetPresetPreview.preset !== preset) return;

  const snapshot = datasetPresetPreview.snapshot;
  datasetPresetPreview = null;
  if (restore) restoreDatasetPresetState(snapshot);
}

function commitDatasetPreset(preset) {
  const committedPreset = committedDatasetPresetForPicking();
  endDatasetPresetPreview(preset, { restore: false });
  applyDatasetPreset(committedPreset === preset ? PULSATOR_DEFAULT_PRESET : preset);
}

function ogleObjectUrl(row) {
  const objectId = String(row[IDX.id]);
  const datasetKey = DATASET_KEYS[row[IDX.dataset]];
  const lacksOgleIvCatalogRow =
    (datasetKey === "cepheids" || datasetKey === "rrlyrae") && !row[IDX.lightCurveSubtype];
  if (datasetKey === "miras" || lacksOgleIvCatalogRow) {
    return `${OGLE_III_CVS_OBJECT_URL}${encodeURIComponent(objectId)}`;
  }
  return `${OGLE_OCVS_OBJECT_URL}${encodeURIComponent(objectId)}`;
}

function pointerModeForEvent(event) {
  const leftButton = (event.buttons & 1) === 1;
  const rightButton = (event.buttons & 2) === 2;
  if (leftButton && rightButton) return "roll";
  if (rightButton || event.button === 2 || event.shiftKey) return "pan";
  return "orbit";
}

function setDragStart(event) {
  dragStart = {
    x: event.clientX,
    y: event.clientY,
    yaw: state.yaw,
    pitch: state.pitch,
    roll: state.roll,
    panX: state.panX,
    panY: state.panY,
    zoom: state.zoom,
    scale: scene.scale || getBaseSceneLayout().scale,
    coordinateContext: activeCoordinateReference().context,
  };
}

function setCursorClientPosition(clientX, clientY) {
  state.cursorClientX = clientX;
  state.cursorClientY = clientY;
  updateCoordinateReadout();
}

function setCursorPosition(event) {
  setCursorClientPosition(event.clientX, event.clientY);
}

function clearCursorPosition() {
  state.cursorClientX = null;
  state.cursorClientY = null;
  updateCoordinateReadout();
}

function setPanLock(enabled) {
  state.panLock = Boolean(enabled);
  syncRangeOutputs();
}

function togglePanLock() {
  setPanLock(!state.panLock);
}

function consumeRightDoubleClick(event) {
  const now = performance.now();
  const dx = event.clientX - lastRightClick.x;
  const dy = event.clientY - lastRightClick.y;
  const isDoubleClick = now - lastRightClick.time < 380 && dx * dx + dy * dy < 64;
  lastRightClick = { time: isDoubleClick ? 0 : now, x: event.clientX, y: event.clientY };
  if (!isDoubleClick) return false;
  togglePanLock();
  return true;
}

function isMobileTouchPointer(event) {
  return event.pointerType === "touch" && MOBILE_CONTROLS_MEDIA.matches;
}

function activeFullscreenElement() {
  return document.fullscreenElement || document.webkitFullscreenElement || null;
}

function requestMobileFullscreen() {
  if (!MOBILE_CONTROLS_MEDIA.matches || activeFullscreenElement()) return;
  const target = elements.atlas || document.documentElement;
  const requestFullscreen =
    target.requestFullscreen || target.webkitRequestFullscreen || target.msRequestFullscreen;
  if (!requestFullscreen) return;
  try {
    const result = requestFullscreen.call(target, { navigationUI: "hide" });
    if (result?.catch) result.catch(() => {});
  } catch {
    // Some mobile browsers only support fullscreen for installed web apps or media elements.
  }
}

function exitMobileFullscreen() {
  if (!activeFullscreenElement()) return;
  const exitFullscreen = document.exitFullscreen || document.webkitExitFullscreen || document.msExitFullscreen;
  if (!exitFullscreen) return;
  try {
    const result = exitFullscreen.call(document);
    if (result?.catch) result.catch(() => {});
  } catch {
    // Ignore browser-specific fullscreen exit failures.
  }
}

function touchPointFromEvent(event) {
  return {
    pointerId: event.pointerId,
    clientX: event.clientX,
    clientY: event.clientY,
  };
}

function currentTouchPoints() {
  return Array.from(activeTouchPointers.values());
}

function touchPairMetrics(points = currentTouchPoints()) {
  if (points.length < 2) return null;
  const first = points[0];
  const second = points[1];
  const dx = second.clientX - first.clientX;
  const dy = second.clientY - first.clientY;
  return {
    centerX: (first.clientX + second.clientX) / 2,
    centerY: (first.clientY + second.clientY) / 2,
    distance: Math.max(1, Math.hypot(dx, dy)),
    angle: Math.atan2(dy, dx),
  };
}

function captureCanvasPointer(event) {
  try {
    canvas.setPointerCapture(event.pointerId);
  } catch {
    // Ignore capture races from interrupted mobile gestures.
  }
}

function releaseCanvasPointer(event) {
  try {
    if (canvas.hasPointerCapture(event.pointerId)) canvas.releasePointerCapture(event.pointerId);
  } catch {
    // Ignore release races from interrupted mobile gestures.
  }
}

function beginSingleTouchGesture(point, { suppressTap = false } = {}) {
  touchGesture = {
    mode: "single",
    pointerId: point.pointerId,
    x: point.clientX,
    y: point.clientY,
    yaw: state.yaw,
    pitch: state.pitch,
    roll: state.roll,
    zoom: state.zoom,
    moved: false,
    suppressTap,
  };
  setCursorClientPosition(point.clientX, point.clientY);
  canvas.classList.add("is-dragging");
}

function beginMultiTouchGesture() {
  const metrics = touchPairMetrics();
  if (!metrics) return;
  touchGesture = {
    mode: "multi",
    centerX: metrics.centerX,
    centerY: metrics.centerY,
    distance: metrics.distance,
    angle: metrics.angle,
    roll: state.roll,
    zoom: state.zoom,
    scale: scene.scale || getBaseSceneLayout().scale,
    sceneCenterX: scene.centerX,
    sceneCenterY: scene.centerY,
    moved: false,
    suppressTap: true,
  };
  dragging = false;
  dragStart = null;
  movedDuringDrag = true;
  setCursorClientPosition(metrics.centerX, metrics.centerY);
  canvas.classList.add("is-dragging");
}

function finishMobileTouchGesture() {
  touchGesture = null;
  dragging = false;
  dragStart = null;
  movedDuringDrag = false;
  canvas.classList.remove("is-dragging");
  window.clearTimeout(hoverTimer);
  hoverSuppressedUntil = performance.now() + 350;
}

function applySingleTouchGesture(point) {
  if (!touchGesture || touchGesture.mode !== "single" || touchGesture.pointerId !== point.pointerId) return;
  const dx = point.clientX - touchGesture.x;
  const dy = point.clientY - touchGesture.y;
  if (Math.hypot(dx, dy) > MOBILE_TOUCH_MOVE_THRESHOLD) {
    touchGesture.moved = true;
  }

  if (touchGesture.moved) {
    cancelIntroRotation();
    cancelAxisSpinAnimation();
    markOrientationGridActive();
    const orbitSensitivity = orbitDragSensitivity(touchGesture.zoom);
    state.yaw = normalizeRadians(touchGesture.yaw + dx * 0.004 * orbitSensitivity);
    state.pitch = normalizeRadians(touchGesture.pitch + dy * 0.0032 * orbitSensitivity);
    syncRangeOutputs();
    markProjectionDirty();
  }

  setCursorClientPosition(point.clientX, point.clientY);
}

function applyMultiTouchGesture() {
  if (!touchGesture || touchGesture.mode !== "multi") return;
  const metrics = touchPairMetrics();
  if (!metrics) return;
  const dx = metrics.centerX - touchGesture.centerX;
  const dy = metrics.centerY - touchGesture.centerY;
  const distanceDelta = Math.abs(metrics.distance - touchGesture.distance);
  const angleDelta = normalizeRadians(metrics.angle - touchGesture.angle);
  const moved =
    Math.hypot(dx, dy) > MOBILE_TOUCH_MOVE_THRESHOLD ||
    distanceDelta > MOBILE_PINCH_MOVE_THRESHOLD ||
    Math.abs(angleDelta) > MOBILE_ROTATE_ANGLE_THRESHOLD;

  if (moved) {
    touchGesture.moved = true;
    cancelIntroRotation();
    cancelAxisSpinAnimation();
    markOrientationGridActive();
    if (state.locked || state.cameraLocked) clearTargetSelection();

    const nextZoom = clampZoomScale(touchGesture.zoom * (metrics.distance / Math.max(1, touchGesture.distance)));
    state.roll = normalizeRadians(touchGesture.roll - angleDelta * MOBILE_ROTATE_SENSITIVITY);
    state.zoom = nextZoom;
    updateSceneLayout();

    const scaleRatio = scene.scale / Math.max(1, touchGesture.scale);
    const targetCenterX = metrics.centerX - (touchGesture.centerX - touchGesture.sceneCenterX) * scaleRatio;
    const targetCenterY = metrics.centerY - (touchGesture.centerY - touchGesture.sceneCenterY) * scaleRatio;
    const base = getBaseSceneLayout();
    state.panX = targetCenterX - base.centerX;
    state.panY = targetCenterY - base.centerY;
    updateSceneLayout();
    syncRangeOutputs();
    markProjectionDirty();
  }

  setCursorClientPosition(metrics.centerX, metrics.centerY);
}

function resetMobileViewportToDefault() {
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  markOrientationGridActive();
  state.yaw = 0;
  state.pitch = 0;
  state.roll = 0;
  state.zoom = DEFAULT_ZOOM_SCALE;
  state.panX = 0;
  state.panY = 0;
  state.coordinateFrame = "atlas";
  state.coordinateCenter = "bridge";
  state.centerSelection = "bridge";
  state.customCoordinateContext = null;
  state.hovered = null;
  state.locked = null;
  state.cameraLocked = false;
  state.cameraFollowsLockedTarget = false;
  previousCustomView = null;
  lastTargetNavigationStep = null;
  updateSceneLayout();
  syncRangeOutputs();
  syncCoordinateFrameControls();
  setTarget(null);
  markProjectionDirty();
  exitMobileFullscreen();
}

function selectMobileTapTarget(point) {
  const now = performance.now();
  const isDoubleTap =
    now - lastMobileTap.time <= MOBILE_DOUBLE_TAP_MAX_MS &&
    Math.hypot(point.clientX - lastMobileTap.x, point.clientY - lastMobileTap.y) <= MOBILE_DOUBLE_TAP_MAX_DISTANCE;

  if (isDoubleTap) {
    resetMobileViewportToDefault();
    lastMobileTap = { time: 0, x: 0, y: 0, target: null };
    return;
  }

  const target = nearestTarget(point.clientX, point.clientY, {
    pickRadiusScale: MOBILE_TARGET_PICK_RADIUS_SCALE,
  });
  if (target) {
    lastTargetNavigationStep = null;
    state.locked = target;
    state.hovered = null;
    state.cameraLocked = false;
    state.cameraFollowsLockedTarget = false;
    setTarget(target);
    updateCoordinateReadout();
    queueRender();
  } else {
    clearTargetSelection();
  }

  lastMobileTap = { time: now, x: point.clientX, y: point.clientY, target };
}

function handleCanvasTouchPointerDown(event) {
  if (!isMobileTouchPointer(event)) return false;
  event.preventDefault();
  requestMobileFullscreen();
  window.clearTimeout(hoverTimer);
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  activeTouchPointers.set(event.pointerId, touchPointFromEvent(event));
  captureCanvasPointer(event);

  if (activeTouchPointers.size >= 2) {
    beginMultiTouchGesture();
  } else {
    beginSingleTouchGesture(touchPointFromEvent(event));
  }
  return true;
}

function handleCanvasTouchPointerMove(event) {
  if (!activeTouchPointers.has(event.pointerId)) return false;
  event.preventDefault();
  const point = touchPointFromEvent(event);
  activeTouchPointers.set(event.pointerId, point);
  if (activeTouchPointers.size >= 2) {
    if (!touchGesture || touchGesture.mode !== "multi") beginMultiTouchGesture();
    applyMultiTouchGesture();
  } else {
    applySingleTouchGesture(point);
  }
  return true;
}

function handleCanvasTouchPointerUp(event) {
  if (!activeTouchPointers.has(event.pointerId)) return false;
  event.preventDefault();
  const point = activeTouchPointers.get(event.pointerId) || touchPointFromEvent(event);
  const wasTap =
    touchGesture?.mode === "single" &&
    touchGesture.pointerId === event.pointerId &&
    !touchGesture.moved &&
    !touchGesture.suppressTap &&
    activeTouchPointers.size === 1;

  setCursorClientPosition(point.clientX, point.clientY);
  activeTouchPointers.delete(event.pointerId);
  releaseCanvasPointer(event);

  if (wasTap) {
    selectMobileTapTarget(point);
  }

  if (activeTouchPointers.size >= 2) {
    beginMultiTouchGesture();
  } else if (activeTouchPointers.size === 1) {
    beginSingleTouchGesture(currentTouchPoints()[0], { suppressTap: true });
  } else {
    finishMobileTouchGesture();
  }

  return true;
}

function handleCanvasTouchPointerCancel(event) {
  if (!activeTouchPointers.has(event.pointerId)) return false;
  event.preventDefault();
  activeTouchPointers.delete(event.pointerId);
  releaseCanvasPointer(event);
  if (activeTouchPointers.size >= 2) {
    beginMultiTouchGesture();
  } else if (activeTouchPointers.size === 1) {
    beginSingleTouchGesture(currentTouchPoints()[0], { suppressTap: true });
  } else {
    finishMobileTouchGesture();
  }
  return true;
}

function isEditableKeyboardTarget(target) {
  if (!(target instanceof Element)) return false;
  if (target.isContentEditable) return true;
  if (target.tagName === "INPUT") {
    return !["checkbox", "radio", "button", "submit", "reset"].includes(target.type);
  }
  return ["SELECT", "TEXTAREA"].includes(target.tagName);
}

function viewportKeyboardMultiplier(event) {
  return event.shiftKey ? VIEWPORT_KEY_FAST_MULTIPLIER : 1;
}

function bindPointerRangeFocusRelease(input) {
  let pointerIsDown = false;
  const releaseFocus = () => {
    if (!pointerIsDown) return;
    pointerIsDown = false;
    window.setTimeout(() => {
      if (document.activeElement === input) input.blur();
    }, 0);
  };

  input.addEventListener("pointerdown", () => {
    pointerIsDown = true;
    window.addEventListener("pointerup", releaseFocus, { once: true });
    window.addEventListener("pointercancel", releaseFocus, { once: true });
  });
  input.addEventListener("change", releaseFocus);
}

function resetAppState() {
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  introCloudLabelAnimation = null;
  datasetPresetPreview = null;
  window.clearTimeout(hoverTimer);
  markOrientationGridActive();

  state.yaw = 0;
  state.pitch = 0;
  state.roll = 0;
  state.zoom = DEFAULT_ZOOM_SCALE;
  state.panX = 0;
  state.panY = 0;
  state.radiusScale = defaultRadiusScaleForPreset(PULSATOR_DEFAULT_PRESET);
  state.datasetExposure = {
    cepheids: DATASET_EXPOSURE_DEFAULT,
    rrlyrae: DATASET_EXPOSURE_DEFAULT,
    anomalousCepheids: DATASET_EXPOSURE_DEFAULT,
    miras: DATASET_EXPOSURE_DEFAULT,
    redclump: RED_CLUMP_EXPOSURE_DEFAULT,
    clusters: DATASET_EXPOSURE_DEFAULT,
  };
  state.depthScale = 1;
  state.density = 100;
  state.colorContrast = COLOR_CONTRAST_DEFAULT;
  resetSimulationClock();
  setPulsationSpeed(INITIAL_PULSATION_SPEED, { preserveDay: false });
  state.pulsationAmplitudeScale = defaultPulsationAmplitudeScaleForPreset(PULSATOR_DEFAULT_PRESET);
  state.uncertaintySeed = DEFAULT_UNCERTAINTY_SEED;
  state.datasetPreset = null;
  state.pulsatorPreset = null;
  state.datasets = {
    cepheids: true,
    rrlyrae: true,
    anomalousCepheids: true,
    miras: true,
    redclump: true,
    clusters: true,
  };
  state.spectral = new Set(
    scene.spectralClasses.length ? scene.spectralClasses.map((_, index) => index) : [0, 1, 2, 3, 4, 5],
  );
  state.coordinateFrame = "atlas";
  state.coordinateCenter = "bridge";
  state.centerSelection = "bridge";
  state.customCoordinateContext = null;
  state.panLock = true;
  state.equatorialGrid = false;
  state.galacticGrid = false;
  state.cursorClientX = null;
  state.cursorClientY = null;
  state.targetSearchQuery = "";
  state.hovered = null;
  state.locked = null;
  state.cameraLocked = false;
  state.cameraFollowsLockedTarget = false;
  previousCustomView = null;
  lastTargetNavigationStep = null;
  clearActiveLightcurveInsets();
  applyUncertaintyRealization({ updateTarget: false });
  refreshTemperatureDrivenColors();

  updateSceneLayout();
  syncTargetSearchInput();
  syncDatasetCheckboxes();
  syncSpectralControls();
  syncCoordinateFrameControls();
  syncRangeOutputs();
  setTarget(null);
  invalidateActivePointLists();
  markCatalogStaticDirty();
  markRedClumpLayerDirty();
  markProjectionDirty();
}

function shortcutHelpIsOpen() {
  return Boolean(elements.shortcutHelp && !elements.shortcutHelp.hidden);
}

function setShortcutHelpOpen(open, { focusClose = false } = {}) {
  if (!elements.shortcutHelp) return false;
  const nextOpen = Boolean(open);
  elements.shortcutHelp.hidden = !nextOpen;
  elements.shortcutHelp.classList.toggle("open", nextOpen);
  elements.shortcutHelp.setAttribute("aria-hidden", String(!nextOpen));
  if (nextOpen && focusClose) {
    window.requestAnimationFrame(() => {
      elements.shortcutHelpClose?.focus({ preventScroll: true });
    });
  }
  return true;
}

function toggleShortcutHelp() {
  return setShortcutHelpOpen(!shortcutHelpIsOpen(), { focusClose: true });
}

function buildShortcutHelp() {
  if (!elements.shortcutHelpList || elements.shortcutHelpList.dataset.built === "true") return;
  const fragment = document.createDocumentFragment();
  for (const item of SHORTCUT_HELP_ITEMS) {
    const row = document.createElement("div");
    row.className = "shortcutHelpRow";

    const keys = document.createElement("span");
    keys.className = "shortcutHelpKeys";
    item.keys.forEach((key, index) => {
      if (index > 0) keys.append(" ");
      const keyElement = document.createElement("kbd");
      keyElement.textContent = key;
      keys.append(keyElement);
    });

    const label = document.createElement("span");
    label.className = "shortcutHelpLabel";
    label.textContent = item.label;

    row.append(keys, label);
    fragment.append(row);
  }
  elements.shortcutHelpList.append(fragment);
  elements.shortcutHelpList.dataset.built = "true";
}

function focusTargetSearch() {
  if (!controls.targetSearch) return false;
  if (state.overlaysHidden) setOverlaysHidden(false);
  if (MOBILE_CONTROLS_MEDIA.matches) {
    setMobileControlsOpen(true, { focusClose: false });
  }
  window.requestAnimationFrame(() => {
    controls.targetSearch.focus({ preventScroll: true });
    controls.targetSearch.select();
  });
  return true;
}

function clearActiveTargetOrCamera() {
  if (state.cameraLocked) {
    setCameraLock(false);
    return true;
  }
  if (state.locked || state.hovered) {
    clearTargetSelection();
    return true;
  }
  return false;
}

function toggleCameraLockShortcut() {
  const target = state.locked || state.hovered;
  if (!target) return false;
  setCameraLock(!(state.cameraLocked && state.locked === target), target);
  return true;
}

function activateKeyboardDatasetPreset(key) {
  const preset = KEYBOARD_DATASET_PRESETS[key];
  if (!preset) return false;
  commitDatasetPreset(preset);
  return true;
}

function cycleCoordinateGrids() {
  const current =
    state.equatorialGrid && state.galacticGrid
      ? "both"
      : state.equatorialGrid
        ? "equatorial"
        : state.galacticGrid
          ? "galactic"
          : "none";
  const next = GRID_SHORTCUT_SEQUENCE[
    (GRID_SHORTCUT_SEQUENCE.indexOf(current) + 1) % GRID_SHORTCUT_SEQUENCE.length
  ];
  state.equatorialGrid = next === "equatorial" || next === "both";
  state.galacticGrid = next === "galactic" || next === "both";
  syncCoordinateFrameControls();
  queueRender();
}

function orientationSnapshot() {
  return {
    yaw: state.yaw,
    pitch: state.pitch,
    roll: state.roll,
  };
}

function applyOrientationSnapshot(snapshot, { recenter = true } = {}) {
  if (!snapshot) return;
  markOrientationGridActive();
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  state.yaw = normalizeRadians(snapshot.yaw);
  state.pitch = normalizeRadians(snapshot.pitch);
  state.roll = normalizeRadians(snapshot.roll);
  if (recenter) recenterViewport();
  syncRangeOutputs();
  markProjectionDirty();
}

function applyViewOrientation(angles) {
  applyOrientationSnapshot(
    {
      yaw: degreesToRadians(angles.yaw),
      pitch: degreesToRadians(angles.pitch),
      roll: degreesToRadians(angles.roll),
    },
    { recenter: true },
  );
}

function cycleViewOrientation() {
  const faceActive = orbitAnglesMatchPreset(FACE_VIEW_ANGLES_DEGREES);
  const edgeActive = orbitAnglesMatchPreset(EDGE_VIEW_ANGLES_DEGREES);
  if (!faceActive && !edgeActive) {
    previousCustomView = orientationSnapshot();
    applyViewOrientation(FACE_VIEW_ANGLES_DEGREES);
  } else if (faceActive) {
    applyViewOrientation(EDGE_VIEW_ANGLES_DEGREES);
  } else if (previousCustomView) {
    applyOrientationSnapshot(previousCustomView, { recenter: true });
  } else {
    applyViewOrientation(FACE_VIEW_ANGLES_DEGREES);
  }
}

function isActivatableKeyboardTarget(target) {
  if (!(target instanceof Element)) return false;
  return Boolean(target.closest("button, a[href], input, select, textarea, [role='button']"));
}

function handleViewportKeydown(event) {
  if (
    event.defaultPrevented ||
    event.ctrlKey ||
    event.metaKey ||
    event.altKey ||
    isEditableKeyboardTarget(event.target)
  ) {
    return;
  }

  const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
  if (shortcutHelpIsOpen() && key !== "Escape" && key !== "?") return;

  const multiplier = viewportKeyboardMultiplier(event);
  const panStep = VIEWPORT_PAN_STEP_PX * multiplier;
  const pageStep = VIEWPORT_PAGE_STEP_PX * multiplier;
  const yawStep = VIEWPORT_YAW_STEP_DEGREES * multiplier;
  let handled = true;

  switch (key) {
    case "/":
      handled = focusTargetSearch();
      break;
    case "?":
      handled = toggleShortcutHelp();
      break;
    case "Escape":
      if (shortcutHelpIsOpen()) {
        handled = setShortcutHelpOpen(false);
      } else {
        handled = clearActiveTargetOrCamera();
      }
      break;
    case " ":
    case "Spacebar":
      if (isActivatableKeyboardTarget(event.target)) {
        handled = false;
      } else {
        togglePulsationPaused();
      }
      break;
    case "w":
      zoomViewportByStep(1, multiplier);
      break;
    case "+":
    case "=":
      zoomViewportByStep(1);
      break;
    case "ArrowUp":
      moveViewportByScreenDelta(0, -panStep);
      break;
    case "a":
      nudgeViewportByScreenDelta(-panStep, 0);
      break;
    case "ArrowLeft":
      moveViewportByScreenDelta(-panStep, 0);
      break;
    case "s":
      zoomViewportByStep(-1, multiplier);
      break;
    case "-":
    case "_":
      zoomViewportByStep(-1);
      break;
    case "ArrowDown":
      moveViewportByScreenDelta(0, panStep);
      break;
    case "d":
      nudgeViewportByScreenDelta(panStep, 0);
      break;
    case "ArrowRight":
      moveViewportByScreenDelta(panStep, 0);
      break;
    case "PageUp":
      moveViewportByScreenDelta(0, -pageStep);
      break;
    case "PageDown":
      moveViewportByScreenDelta(0, pageStep);
      break;
    case "[":
    case "{":
      stepTargetNavigation(-1);
      break;
    case "]":
    case "}":
      stepTargetNavigation(1);
      break;
    case "q":
      yawViewportByDegrees(-yawStep);
      break;
    case "e":
      yawViewportByDegrees(yawStep);
      break;
    case "1":
    case "2":
    case "3":
    case "4":
    case "5":
      handled = activateKeyboardDatasetPreset(key);
      break;
    case "l":
      handled = toggleCameraLockShortcut();
      break;
    case "h":
      setOverlaysHidden(!state.overlaysHidden);
      break;
    case "v":
      cycleViewOrientation();
      break;
    case "g":
      cycleCoordinateGrids();
      break;
    case ",":
    case "<":
      adjustPulsationSpeed(-1, event.shiftKey);
      break;
    case ".":
    case ">":
      adjustPulsationSpeed(1, event.shiftKey);
      break;
    case "0":
      resetAppState();
      break;
    default:
      handled = false;
      break;
  }

  if (handled) {
    event.preventDefault();
  }
}

function syncTargetSearchInput() {
  if (controls.targetSearch && controls.targetSearch.value !== state.targetSearchQuery) {
    controls.targetSearch.value = state.targetSearchQuery;
  }
}

function clearTargetSearch() {
  state.targetSearchQuery = "";
  syncTargetSearchInput();
}

function catalogSearchTextForRow(row) {
  const spectralClass = scene.spectralClasses[row[IDX.spectral]]?.id || "";
  return [
    row[IDX.id],
    DATASET_LABELS[row[IDX.dataset]],
    DATASET_KEYS[row[IDX.dataset]],
    LOCATION_LABELS[row[IDX.location]],
    spectralClass,
    row[IDX.mode],
    row[IDX.period],
    row[IDX.raDeg],
    row[IDX.decDeg],
    row[IDX.galLonDeg],
    row[IDX.galLatDeg],
  ]
    .filter((value) => value !== null && value !== undefined && value !== "")
    .join(" ")
    .toLowerCase();
}

function clusterSearchTextForRow(row) {
  return [
    row[CL.name],
    row[CL.galaxy],
    "cluster",
    "mist",
    row[CL.source],
    row[CL.feh],
    row[CL.logAge],
    row[CL.raDeg],
    row[CL.decDeg],
    row[CL.galLonDeg],
    row[CL.galLatDeg],
    row[CL.qualityFlags],
  ]
    .filter((value) => value !== null && value !== undefined && value !== "")
    .join(" ")
    .toLowerCase();
}

function catalogSearchTerms(query = state.targetSearchQuery) {
  return query.trim().toLowerCase().split(/\s+/).filter(Boolean);
}

function catalogSearchMatches(query = state.targetSearchQuery) {
  const normalizedQuery = query.trim().toLowerCase();
  const terms = catalogSearchTerms(query);
  const matches = [];
  let exactMatch = null;
  let total = 0;
  if (!terms.length) return { matches, total, exactMatch };

  for (const point of scene.catalog) {
    if (!targetIsPickable(point)) continue;
    const searchText = point.searchText || catalogSearchTextForRow(point.row);
    if (!terms.every((term) => searchText.includes(term))) continue;
    total += 1;
    if (!exactMatch && String(point.row[IDX.id]).toLowerCase() === normalizedQuery) {
      exactMatch = point;
    }
    if (matches.length < TARGET_SEARCH_RESULT_LIMIT) matches.push(point);
  }

  for (const point of scene.clusters) {
    if (!targetIsPickable(point)) continue;
    const searchText = point.searchText || clusterSearchTextForRow(point.row);
    if (!terms.every((term) => searchText.includes(term))) continue;
    total += 1;
    if (!exactMatch && String(point.row[CL.name]).toLowerCase() === normalizedQuery) {
      exactMatch = point;
    }
    if (matches.length < TARGET_SEARCH_RESULT_LIMIT) matches.push(point);
  }

  return { matches, total, exactMatch };
}

function catalogMatchMeta(point) {
  if (point.kind === "cluster") {
    const row = point.row;
    return [
      `Star cluster, ${row[CL.galaxy]}`,
      row[CL.source] || "Perren+2017",
      `log age ${formatNumber(row[CL.logAge], 2)}`,
      `${formatInteger(row[CL.renderedStars])} points`,
    ].join(" | ");
  }

  const row = point.row;
  const spectralClass = scene.spectralClasses[row[IDX.spectral]]?.id || "n/a";
  return [
    DATASET_LABELS[row[IDX.dataset]],
    LOCATION_LABELS[row[IDX.location]],
    spectralClass,
    formatPeriodDays(row),
  ].join(" | ");
}

function clampZoomToTarget(target = selectedTargetForDeepZoom()) {
  const previousZoom = state.zoom;
  state.zoom = clampZoomScale(state.zoom, { allowTargetZoom: Boolean(target), target });
  if (state.zoom === previousZoom) return false;
  updateSceneLayout();
  return true;
}

function selectCatalogSearchTarget(target) {
  if (!targetIsPickable(target)) return;
  lastTargetNavigationStep = null;
  state.locked = target;
  state.hovered = null;
  state.cameraLocked = false;
  state.cameraFollowsLockedTarget = false;
  const zoomChanged = clampZoomToTarget(target);
  setTarget(state.locked);
  if (zoomChanged) syncRangeOutputs();
  markProjectionDirty();
}

function renderTargetSearchMatches() {
  const { matches, total } = catalogSearchMatches();
  elements.target.classList.add("hasMatches");

  if (!total) {
    const strong = document.createElement("strong");
    strong.textContent = "No target matches";
    elements.target.append(strong);
    return;
  }

  const summary = document.createElement("strong");
  summary.textContent = total === 1 ? "1 target match" : `${formatInteger(total)} target matches`;

  const list = document.createElement("div");
  list.className = "targetMatchList";

  for (const point of matches) {
    const row = point.row;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "targetMatch";
    button.addEventListener("click", () => selectCatalogSearchTarget(point));

    const id = document.createElement("span");
    id.className = "targetMatchId";
    id.textContent = point.kind === "cluster" ? String(row[CL.name]) : String(row[IDX.id]);

    const meta = document.createElement("span");
    meta.className = "targetMatchMeta";
    meta.textContent = catalogMatchMeta(point);

    button.append(id, meta);
    list.append(button);
  }

  elements.target.append(summary, list);

  if (total > matches.length) {
    const overflow = document.createElement("span");
    overflow.className = "targetMatchOverflow";
    overflow.textContent = `Showing ${formatInteger(matches.length)} of ${formatInteger(total)}`;
    elements.target.append(overflow);
  }
}

function renderNoTargetState() {
  elements.target.classList.remove("hasMatches");
  if (state.targetSearchQuery.trim()) {
    renderTargetSearchMatches();
    return;
  }

  const strong = document.createElement("strong");
  strong.textContent = "No target selected";
  elements.target.append(strong);
}

function mobileTargetPreviewName(target) {
  if (target?.kind === "catalog") return String(target.row[IDX.id]);
  if (target?.kind === "cluster") return String(target.row[CL.name]);
  if (target?.kind === "clusterStar") {
    const cluster = scene.clusters[target.clusterIndex] || scene.clusters[target.row?.[CS.cluster]];
    return cluster ? `${cluster.row[CL.name]} star` : "Synthetic cluster star";
  }
  return "XMC surface cell";
}

function createMobileTargetPreviewPlot(target) {
  if (target?.kind === "cluster") return createClusterHrDiagram(target);
  if (target?.lightCurve?.waveform?.length) {
    const plot = createLightCurveInset(target);
    if (target.kind !== "catalog") return plot;
    const link = document.createElement("a");
    link.className = "mobileTargetPreviewLink";
    link.href = ogleObjectUrl(target.row);
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.setAttribute("aria-label", `Open ${mobileTargetPreviewName(target)} in OGLE`);
    link.append(plot);
    return link;
  }
  return null;
}

function renderMobileTargetPreview(target) {
  if (!elements.mobileTargetPreview || !elements.mobileTargetPreviewName || !elements.mobileTargetPreviewPlot) return;

  elements.mobileTargetPreview.hidden = true;
  elements.mobileTargetPreviewName.textContent = "";
  elements.mobileTargetPreviewPlot.replaceChildren();

  if (!MOBILE_CONTROLS_MEDIA.matches || !target || target !== state.locked) return;

  const plot = createMobileTargetPreviewPlot(target);
  if (!plot) return;

  const name = mobileTargetPreviewName(target);
  elements.mobileTargetPreviewName.textContent = name;
  elements.mobileTargetPreview.setAttribute("aria-label", `${name} target preview`);
  elements.mobileTargetPreviewPlot.append(plot);
  elements.mobileTargetPreview.hidden = false;
}

function handleTargetSearchInput() {
  state.targetSearchQuery = controls.targetSearch.value;
  const { matches, total, exactMatch } = catalogSearchMatches();
  const autoTarget = exactMatch || (total === 1 ? matches[0] : null);
  if (autoTarget) {
    selectCatalogSearchTarget(autoTarget);
    return;
  }

  if (state.locked || state.hovered || state.cameraLocked) {
    lastTargetNavigationStep = null;
    state.locked = null;
    state.hovered = null;
    state.cameraLocked = false;
    state.cameraFollowsLockedTarget = false;
    clearActiveLightcurveInsets();
    if (clampZoomToTarget(null)) syncRangeOutputs();
  }

  setTarget(null);
  markProjectionDirty();
}

function handleTargetSearchKeydown(event) {
  if (event.key === "Escape") {
    clearTargetSearch();
    setTarget(null);
    return;
  }

  if (event.key !== "Enter") return;
  const { matches } = catalogSearchMatches();
  if (!matches.length) return;
  event.preventDefault();
  selectCatalogSearchTarget(matches[0]);
}

function clearTargetSelection() {
  lastTargetNavigationStep = null;
  state.locked = null;
  state.hovered = null;
  state.cameraLocked = false;
  state.cameraFollowsLockedTarget = false;
  const zoomChanged = clampZoomToTarget(null);
  setTarget(null);
  if (zoomChanged) {
    syncRangeOutputs();
    markProjectionDirty();
  }
}

function setCameraLock(enabled, target = state.locked, { followViewport = !MOBILE_CONTROLS_MEDIA.matches } = {}) {
  markOrientationGridActive();
  let zoomChanged = false;
  if (enabled && target) {
    const previousReference = activeCoordinateReference();
    state.locked = target;
    state.hovered = null;
    state.cameraLocked = true;
    state.cameraFollowsLockedTarget = Boolean(followViewport);
    clearCenterSelectionForTarget(target, {
      preserveScreenPosition: !state.cameraFollowsLockedTarget,
      previousReference,
    });
    if (state.cameraFollowsLockedTarget) zoomChanged = clampZoomToTarget(target);
  } else {
    state.cameraLocked = false;
    state.cameraFollowsLockedTarget = false;
  }

  updateSceneLayout();
  setTarget(state.locked || state.hovered);
  if (zoomChanged) syncRangeOutputs();
  markProjectionDirty();
}

function setTarget(target) {
  const current = target || state.locked || state.hovered;
  clearActiveLightcurveInsets();
  markCatalogStaticDirty();
  elements.target.classList.remove("hasMatches");
  elements.target.replaceChildren();

  if (!current) {
    renderMobileTargetPreview(null);
    renderNoTargetState();
    updateCoordinateReadout();
    return;
  }

  clearTargetSearch();

  const header = document.createElement("div");
  header.className = "targetHeader";

  const strong = document.createElement("strong");
  if (current.kind === "catalog") {
    const link = document.createElement("a");
    const objectId = String(current.row[IDX.id]);
    link.href = ogleObjectUrl(current.row);
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = objectId;
    strong.append(link);
  } else if (current.kind === "cluster") {
    strong.textContent = String(current.row[CL.name]);
  } else {
    strong.textContent = "XMC surface cell";
  }
  header.append(strong);

  const lockLabel = document.createElement("label");
  lockLabel.className = "targetLock";
  lockLabel.title = "Lock camera to target";

  const lockInput = document.createElement("input");
  lockInput.type = "checkbox";
  lockInput.checked = state.cameraLocked && state.locked === current;
  lockInput.setAttribute("aria-label", "Lock camera to target");
  lockInput.setAttribute("aria-keyshortcuts", "L");
  lockInput.addEventListener("change", () => {
    setCameraLock(lockInput.checked, current);
  });

  const lockIcon = document.createElement("span");
  lockIcon.className = "lockIcon";
  lockIcon.setAttribute("aria-hidden", "true");
  lockIcon.innerHTML =
    '<svg viewBox="0 0 24 24"><rect x="5" y="10" width="14" height="10" rx="2"></rect><path d="M8 10V7a4 4 0 0 1 8 0v3"></path></svg>';

  lockLabel.append(lockInput, lockIcon);
  header.append(lockLabel);
  elements.target.append(header);
  if (current.kind === "cluster") {
    const hrDiagram = createClusterHrDiagram(current);
    if (hrDiagram) elements.target.append(hrDiagram);
  }

  const dl = document.createElement("dl");
  const rows =
    current.kind === "catalog"
      ? targetRowsForCatalog(current)
      : current.kind === "cluster"
        ? targetRowsForCluster(current)
        : targetRowsForRedClump(current);
  for (const [label, value] of rows) {
    const dt = document.createElement("dt");
    const dd = document.createElement("dd");
    dt.textContent = label;
    if (current.kind === "catalog" && label === "Period") {
      const periodValue = document.createElement("span");
      periodValue.textContent = value;
      dd.className = "withLightcurve";
      dd.append(periodValue, createLightCurveInset(current));
    } else {
      dd.textContent = value;
    }
    dl.append(dt, dd);
  }
  elements.target.append(dl);
  renderMobileTargetPreview(current);
  updateCoordinateReadout();
}

function targetRowsForCatalog(target) {
  const row = target.row;
  const spec = scene.spectralClasses[row[IDX.spectral]].id;
  const dataset = DATASET_LABELS[row[IDX.dataset]];
  const location = LOCATION_LABELS[row[IDX.location]];
  const lightCurve = target.lightCurve;
  const params = lightCurve?.params || lightCurveParams(row);
  const frame = activeCoordinateFrame();
  const reference = activeCoordinateReference();
  const activeCoordinates = displayCoordinatesForPoint(target);
  const reddeningEVI = reddeningEVIForRow(row);
  const intrinsicVMinusI = intrinsicVMinusIForRow(row);
  const reddeningSource =
    row[IDX.reddeningSource] && row[IDX.reddeningSource] !== "none"
      ? row[IDX.reddeningSource]
      : "none";
  const reddeningPartition = row[IDX.reddeningPartitionId];
  const reddeningLabel =
    reddeningSource === "He&Huang2026" && Number.isFinite(reddeningPartition)
      ? `${reddeningSource} #${reddeningPartition}`
      : reddeningSource;
  const colorPulseRange = vMinusIPulseRangeForTarget(target);
  const temperaturePulseRange = temperaturePulseRangeForTarget(target);
  const colorPulseSource =
    target.lightCurve.colorSource === "mira-v-prior"
      ? "learned Mira V/I prior"
      : target.lightCurve.colorSource === "ogle-v-prior"
        ? "OGLE V/I + prior"
        : target.lightCurve.colorSource === "ogle-v-multisine"
      ? "OGLE V/I multisine"
      : target.lightCurve.colorSource === "ogle-fit"
        ? "OGLE V/I"
        : "template";
  const colorFitLabel =
    lightCurve?.colorSource === "mira-v-prior"
      ? `learned Mira V prior Q${lightCurve.colorQuality}`
      : lightCurve?.colorSource === "ogle-v-prior"
        ? `OGLE V + prior Q${lightCurve.colorQuality}`
        : lightCurve?.colorSource === "ogle-v-multisine"
      ? `OGLE V multisine Q${lightCurve.colorQuality}`
      : row[IDX.colorCurve]
        ? `OGLE V/I Q${row[IDX.colorCurveQuality]}`
        : "template";
  const distanceError = Number.isFinite(row[IDX.distanceError]) ? row[IDX.distanceError] : null;
  const sampledDistance =
    state.uncertaintySeed !== DEFAULT_UNCERTAINTY_SEED && Number.isFinite(target.currentDistance)
      ? target.currentDistance
      : null;
  const distanceLabel =
    sampledDistance !== null && distanceError !== null && Math.abs(sampledDistance - row[IDX.distance]) > 0.005
      ? `${formatNumber(sampledDistance, 2)} sampled (${formatNumber(row[IDX.distance], 2)} +/- ${formatNumber(distanceError, 2)} kpc)`
      : distanceError !== null
      ? `${formatNumber(row[IDX.distance], 2)} +/- ${formatNumber(distanceError, 2)} kpc`
      : `${formatNumber(row[IDX.distance], 2)} kpc`;
  const datasetKey = DATASET_KEYS[row[IDX.dataset]];
  const metallicityFeH = metallicityForCatalogRow(row);
  const metallicitySource = Number.isFinite(row[IDX.feh]) ? "catalog" : "mean";
  const miraTeffSource = datasetKey === "miras" ? miraTemperatureSourceLabel(row) : null;
  const luminosity = Number.isFinite(target.currentLum) ? target.currentLum : row[IDX.lum];
  const logLuminosity = Number.isFinite(target.currentLogLum) ? target.currentLogLum : row[IDX.logLum];
  const radius = Number.isFinite(target.currentRadius) ? target.currentRadius : row[IDX.radius];
  const details = [
    ["Type", `${dataset}, ${location}, ${spec}`],
    ["Period", formatPeriodDays(row)],
    ["Lum", `${formatNumber(luminosity, 0)} Lsun`],
    ["Radius", `${formatNumber(radius, 1)} Rsun`],
    ["vs RC", `${formatNumber(luminosity / RED_CLUMP_LUMINOSITY, 1)}x`],
    ["Dist", distanceLabel],
    ["V-I obs", formatNumber(row[IDX.vMinusI], 3)],
    ["E(V-I)", `${formatNumber(reddeningEVI, 3)} ${reddeningLabel}`],
    ["V-I 0", Number.isFinite(intrinsicVMinusI) ? formatNumber(intrinsicVMinusI, 3) : "n/a"],
    [
      "Teff",
      Number.isFinite(intrinsicVMinusI)
        ? `${formatNumber(effectiveTemperatureForCatalogState(row, intrinsicVMinusI, logLuminosity), 0)} K`
        : "n/a",
    ],
    ["Fe/H used", `${formatNumber(metallicityFeH, 2)} ${metallicitySource}`],
    [
      "Amp",
      `${formatNumber(lightCurve?.vAmplitude, 3)} mag V (${formatNumber(lightCurve?.iAmplitude, 3)} I)`,
    ],
    [
      "Brightness",
      lightCurve?.source === "mira-multisine"
        ? lightCurve?.vComponents?.length
          ? lightCurve?.colorSource === "mira-v-prior"
            ? `I multi-period + V prior Q${lightCurve.sourceQuality}/${lightCurve.colorQuality}`
            : lightCurve?.colorSource === "ogle-v-prior"
              ? `V/I multi-period + prior Q${lightCurve.sourceQuality}/${lightCurve.colorQuality}`
              : `V/I multi-period OGLE Q${lightCurve.sourceQuality}/${lightCurve.colorQuality}`
          : `I multi-period OGLE Q${lightCurve.sourceQuality}`
        : lightCurve?.source === "ogle-fit"
        ? `V from OGLE I shape Q${lightCurve.sourceQuality}`
        : "V-scaled Fourier template",
    ],
    ["V amp src", lightCurve?.vAmplitudeSource || "template ratio"],
    ["Color fit", colorFitLabel],
    [
      "V-I pulse",
      colorPulseRange
        ? `${formatNumber(colorPulseRange.min, 3)}-${formatNumber(colorPulseRange.max, 3)} ${colorPulseSource}`
        : "n/a",
    ],
    [
      "Teff pulse",
      temperaturePulseRange
        ? `${formatNumber(temperaturePulseRange.min, 0)}-${formatNumber(temperaturePulseRange.max, 0)} K`
        : "n/a",
    ],
  ];

  if (datasetKey === "cepheids") {
    details.push(["Age", `${formatNumber(row[IDX.age], 0)} Myr`], ["Mode", row[IDX.mode] || "n/a"]);
  } else if (datasetKey === "rrlyrae") {
    details.push(["[Fe/H]", formatNumber(row[IDX.feh], 2)]);
  } else if (datasetKey === "anomalousCepheids") {
    details.push(["Mode", row[IDX.mode] || "n/a"]);
  } else if (datasetKey === "miras") {
    details.push(["Chemistry", row[IDX.mode] || "n/a"]);
    details.push([
      "Teff src",
      miraTeffSource && Number.isFinite(row[IDX.miraTeff])
        ? `${formatNumber(row[IDX.miraTeff], 0)} K ${miraTeffSource}`
        : "MIST V-I prior",
    ]);
    if (Array.isArray(row[IDX.miraPeriods]) && row[IDX.miraPeriods].length) {
      details.push([
        "Components",
        row[IDX.miraPeriods]
          .map((period) => `${formatNumberCompact(period, period >= 1000 ? 0 : 1)} d`)
          .join(", "),
      ]);
    }
    if (row[IDX.distanceSource]) {
      details.push(["Dist src", row[IDX.distanceSource]]);
    }
  }

  const t0Label =
    datasetKey === "miras"
      ? lightCurve?.source === "mira-multisine"
        ? "OGLE fitted phases"
        : "catalog phase"
      : params.measured
        ? `${formatNumber(params.t0, 5)} HJD-2450000`
        : "template phase";
  details.push(["T0", t0Label], ["Fourier", `R21 ${formatNumber(params.r21, 3)}, R31 ${formatNumber(params.r31, 3)}`]);
  details.push(
    [`${reference.label} ${frame.label}`, formatCoordinateTriplet(activeCoordinates)],
    ["RA, Dec", `${formatNumber(row[IDX.raDeg], 4)}°, ${formatNumber(row[IDX.decDeg], 4)}°`],
    ["Gal l,b", `${formatNumber(row[IDX.galLonDeg], 4)}°, ${formatNumber(row[IDX.galLatDeg], 4)}°`],
  );
  return details;
}

function targetRowsForRedClump(target) {
  const row = target.row;
  const frame = activeCoordinateFrame();
  const reference = activeCoordinateReference();
  const activeCoordinates = displayCoordinatesForPoint(target);
  const details = [
    ["Type", "Red clump distance surface, K"],
    ["Lum ref", `${formatNumber(RED_CLUMP_LUMINOSITY, 0)} Lsun`],
    ["Radius ref", `${formatNumber(RED_CLUMP_RADIUS, 1)} Rsun`],
    ["Dist", `${formatNumber(row[RC.distance], 2)} kpc`],
    ["Gal l,b", `${formatNumber(row[RC.lon], 2)}°, ${formatNumber(row[RC.lat], 2)}°`],
    [`${reference.label} ${frame.label}`, formatCoordinateTriplet(activeCoordinates)],
  ];
  if (Number.isFinite(row[RC.densityCount])) {
    details.splice(4, 0, ["RC-like count", formatInteger(row[RC.densityCount])]);
  }
  return details;
}

function targetRowsForCluster(target) {
  const row = target.row;
  const frame = activeCoordinateFrame();
  const reference = activeCoordinateReference();
  const activeCoordinates = displayCoordinatesForPoint(target);
  const source = row[CL.source] || "Perren+2017";
  const ageMyr = 10 ** (row[CL.logAge] - 6);
  const ageUnit = ageMyr >= 1000 ? "Gyr" : "Myr";
  const ageScale = ageMyr >= 1000 ? 1000 : 1;
  const ageValue = ageMyr / ageScale;
  const agePlus = Number.isFinite(row[CL.eLogAge]) ? (10 ** (row[CL.logAge] + row[CL.eLogAge] - 6) - ageMyr) / ageScale : null;
  const ageMinus = Number.isFinite(row[CL.eLogAge]) ? (ageMyr - 10 ** (row[CL.logAge] - row[CL.eLogAge] - 6)) / ageScale : null;
  const ageDigits = ageUnit === "Gyr" ? 2 : 0;
  const distanceError = Number.isFinite(row[CL.eMu0]) ? (Math.log(10) / 5) * row[CL.distance] * row[CL.eMu0] : null;
  const sampledDistance =
    state.uncertaintySeed !== DEFAULT_UNCERTAINTY_SEED && Number.isFinite(target.currentDistance)
      ? target.currentDistance
      : null;
  const distanceLabel =
    sampledDistance !== null && Number.isFinite(distanceError) && Math.abs(sampledDistance - row[CL.distance]) > 0.005
      ? `${formatNumber(sampledDistance, 2)} sampled (${formatNumber(row[CL.distance], 2)} +/- ${formatNumber(distanceError, 2)})`
      : Number.isFinite(distanceError)
        ? `${formatNumber(row[CL.distance], 2)} +/- ${formatNumber(distanceError, 2)}`
        : formatNumber(row[CL.distance], 2);
  const ageLabel =
    Number.isFinite(agePlus) && Number.isFinite(ageMinus)
      ? `${formatNumber(ageValue, ageDigits)} +${formatNumber(agePlus, ageDigits)}/-${formatNumber(ageMinus, ageDigits)}`
      : formatNumber(ageValue, ageDigits);
  const details = [
    ["Type", `MIST synthetic cluster, ${row[CL.galaxy]}`],
    ["Source", source],
    ["Stars [N]", `${formatInteger(row[CL.renderedStars])} rendered, ${formatInteger(row[CL.unresolvedStars])} glow`],
    ["Mass [Msun]", `${formatInteger(row[CL.mass])} +/- ${formatInteger(row[CL.eMass])}`],
    ["Radius [pc]", formatNumber(row[CL.radiusPc], 1)],
    ["[Fe/H] [dex]", `${formatNumber(row[CL.feh], 2)} +/- ${formatNumber(row[CL.eFeh], 2)}`],
    ["log age [dex]", `${formatNumber(row[CL.logAge], 2)} +/- ${formatNumber(row[CL.eLogAge], 2)}`],
    [`Age [${ageUnit}]`, ageLabel],
    ["E(B-V) [mag]", `${formatNumber(row[CL.ebv], 3)} +/- ${formatNumber(row[CL.eEbv], 3)}`],
    ["Dist [kpc]", distanceLabel],
    ["Isochrones", row[CL.isochroneSummary]],
    [
      "Glow [Lsun]",
      `${formatNumber(row[CL.unresolvedLum], 1)} in ${formatInteger(target.glowBins?.length || 0)} bins, V-I0 [mag] ${formatNumber(row[CL.unresolvedVMinusI0], 2)}`,
    ],
    ["Segregation", formatNumber(row[CL.segregation], 2)],
    [
      "Quality",
      row[CL.qualityFlags] === "none"
        ? Number.isFinite(row[CL.flagsCount])
          ? `FC ${row[CL.flagsCount]}`
          : "none"
        : Number.isFinite(row[CL.flagsCount])
          ? `${row[CL.qualityFlags]} (FC ${row[CL.flagsCount]})`
          : row[CL.qualityFlags],
    ],
    [`${reference.label} ${frame.label} [kpc]`, formatCoordinateTriplet(activeCoordinates)],
    ["RA, Dec [deg]", `${formatNumber(row[CL.raDeg], 4)}°, ${formatNumber(row[CL.decDeg], 4)}°`],
    ["Gal l,b [deg]", `${formatNumber(row[CL.galLonDeg], 4)}°, ${formatNumber(row[CL.galLatDeg], 4)}°`],
  ];
  if (row[CL.ageOutlier]) {
    details.splice(12, 0, ["ASteCA note", "large published age rerun delta"]);
  }
  if (Number.isFinite(row[CL.contaminationIndex]) || Number.isFinite(row[CL.clusterProbability])) {
    details.splice(
      12,
      0,
      ["CI / Pcl", `${formatNumber(row[CL.contaminationIndex], 2)} / ${formatNumber(row[CL.clusterProbability], 2)}`],
    );
  }
  return details;
}

function targetNavigationIncludesRedClump() {
  const current = state.locked || state.hovered;
  return committedDatasetPresetForPicking() === "redclump" || current?.kind === "redclump";
}

function targetNavigationSortLabel(target) {
  if (target.kind === "catalog") return String(target.row[IDX.id]);
  if (target.kind === "cluster") return String(target.row[CL.name]);
  if (target.kind === "redclump") {
    const row = target.row;
    return `${formatNumber(row[RC.lon], 4)},${formatNumber(row[RC.lat], 4)},${formatNumber(row[RC.distance], 3)}`;
  }
  return "";
}

function targetNavigationHilbertIndex(x, y) {
  let xi = x;
  let yi = y;
  let index = 0;
  const side = 1 << TARGET_NAVIGATION_HILBERT_BITS;
  const last = side - 1;

  for (let step = side >> 1; step > 0; step >>= 1) {
    const rx = (xi & step) > 0 ? 1 : 0;
    const ry = (yi & step) > 0 ? 1 : 0;
    index += step * step * ((3 * rx) ^ ry);
    if (ry === 0) {
      if (rx === 1) {
        xi = last - xi;
        yi = last - yi;
      }
      const nextX = xi;
      xi = yi;
      yi = nextX;
    }
  }

  return index;
}

function targetNavigationKindWeight(target) {
  if (target?.kind === "catalog") return 0;
  if (target?.kind === "cluster") return 1;
  if (target?.kind === "redclump") return 2;
  return Infinity;
}

function targetNavigationTargetIsAllowed(target, includeRedClump) {
  if (!target || !targetIsPickable(target)) return false;
  if (target.kind === "redclump") return includeRedClump;
  return target.kind === "catalog" || target.kind === "cluster";
}

function buildTargetNavigationCandidates() {
  ensureProjectionCacheForInteraction();
  if (scene.width <= 0 || scene.height <= 0) return [];

  const candidates = [];
  const seen = new Set();
  const includeRedClump = targetNavigationIncludesRedClump();
  const maxHilbertCoordinate = (1 << TARGET_NAVIGATION_HILBERT_BITS) - 1;
  const centerX = scene.width * 0.5;
  const centerY = scene.height * 0.5;
  const minX = -TARGET_NAVIGATION_VIEWPORT_MARGIN;
  const maxX = scene.width + TARGET_NAVIGATION_VIEWPORT_MARGIN;
  const minY = -TARGET_NAVIGATION_VIEWPORT_MARGIN;
  const maxY = scene.height + TARGET_NAVIGATION_VIEWPORT_MARGIN;

  const append = (item, kindWeight) => {
    const target = item?.point;
    if (!target || seen.has(target) || !targetIsPickable(target)) return;
    if (target.kind === "redclump" && !includeRedClump) return;
    if (target.kind !== "catalog" && target.kind !== "cluster" && target.kind !== "redclump") return;

    const projected = item.projected || target.activeProjected || target.projected;
    if (!projected || !Number.isFinite(projected.x) || !Number.isFinite(projected.y)) return;
    if (projected.x < minX || projected.x > maxX || projected.y < minY || projected.y > maxY) return;

    const hilbertX = Math.round((clamp(projected.x, 0, scene.width) / scene.width) * maxHilbertCoordinate);
    const hilbertY = Math.round((clamp(projected.y, 0, scene.height) / scene.height) * maxHilbertCoordinate);
    const dx = projected.x - centerX;
    const dy = projected.y - centerY;
    seen.add(target);
    candidates.push({
      target,
      key: targetNavigationHilbertIndex(hilbertX, hilbertY),
      kindWeight,
      centerDistance2: dx * dx + dy * dy,
      depth: Number.isFinite(projected.z) ? projected.z : 0,
      label: targetNavigationSortLabel(target),
    });
  };

  for (const item of scene.catalogDrawList) {
    if (item.point?.kind === "catalog") append(item, 0);
  }
  for (const item of scene.clusterTargetDrawList) append(item, 1);
  if (includeRedClump) {
    for (const item of scene.redClumpDrawList) append(item, 2);
  }

  candidates.sort(
    (left, right) =>
      left.key - right.key ||
      left.kindWeight - right.kindWeight ||
      left.depth - right.depth ||
      left.label.localeCompare(right.label),
  );
  return candidates;
}

function buildFullTargetNavigationCandidates() {
  if (projectionDirty || scene.catalogProjectionFastPending) {
    rebuildProjectionCache({ forceCatalogProjection: true });
  } else {
    rebuildActivePointLists();
    rebuildCoordinateCache();
  }

  const includeRedClump = targetNavigationIncludesRedClump();
  const entries = [];
  const transform = makeProjectionTransform(1);
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;

  const append = (target) => {
    if (!targetNavigationTargetIsAllowed(target, includeRedClump)) return;
    const coordinates = coordinatesForPoint(target);
    if (!coordinates) return;
    const navigationProjected = projectOffsetWithTransform(coordinates[0], coordinates[1], coordinates[2], transform);
    if (!Number.isFinite(navigationProjected.x) || !Number.isFinite(navigationProjected.y)) return;

    const screenProjected = target.activeProjected || target.projected || navigationProjected;
    const dx = (screenProjected.x || 0) - scene.width * 0.5;
    const dy = (screenProjected.y || 0) - scene.height * 0.5;
    entries.push({
      target,
      navigationProjected,
      centerDistance2: dx * dx + dy * dy,
      depth: Number.isFinite(navigationProjected.z) ? navigationProjected.z : 0,
      kindWeight: targetNavigationKindWeight(target),
      label: targetNavigationSortLabel(target),
    });
    minX = Math.min(minX, navigationProjected.x);
    maxX = Math.max(maxX, navigationProjected.x);
    minY = Math.min(minY, navigationProjected.y);
    maxY = Math.max(maxY, navigationProjected.y);
  };

  for (const target of scene.activeCatalog) append(target);
  for (const target of scene.activeClusters) append(target);
  if (includeRedClump) {
    for (const target of scene.activeRedClump) append(target);
  }

  if (!entries.length) return [];

  const maxHilbertCoordinate = (1 << TARGET_NAVIGATION_HILBERT_BITS) - 1;
  const spanX = Math.max(0.000001, maxX - minX);
  const spanY = Math.max(0.000001, maxY - minY);
  const candidates = entries.map((entry) => {
    const hilbertX = Math.round(((entry.navigationProjected.x - minX) / spanX) * maxHilbertCoordinate);
    const hilbertY = Math.round(((entry.navigationProjected.y - minY) / spanY) * maxHilbertCoordinate);
    return {
      ...entry,
      key: targetNavigationHilbertIndex(hilbertX, hilbertY),
    };
  });

  candidates.sort(
    (left, right) =>
      left.key - right.key ||
      left.kindWeight - right.kindWeight ||
      left.depth - right.depth ||
      left.label.localeCompare(right.label),
  );
  return candidates;
}

function nearestTargetNavigationCandidateIndex(candidates) {
  let bestIndex = -1;
  let bestDistance = Infinity;
  for (let index = 0; index < candidates.length; index += 1) {
    const distance = candidates[index].centerDistance2;
    if (distance < bestDistance) {
      bestDistance = distance;
      bestIndex = index;
    }
  }
  return bestIndex;
}

function targetNavigationStepDirection(direction) {
  if (direction < 0) return -1;
  if (direction > 0) return 1;
  return 0;
}

function targetNavigationCandidateIndex(candidates, current, direction) {
  if (!candidates.length) return -1;
  const currentIndex = current ? candidates.findIndex((candidate) => candidate.target === current) : -1;
  if (currentIndex >= 0) return positiveModulo(currentIndex + direction, candidates.length);
  return nearestTargetNavigationCandidateIndex(candidates);
}

function targetNavigationWouldBacktrack(target, current, direction) {
  return Boolean(
    target &&
      current &&
      lastTargetNavigationStep &&
      lastTargetNavigationStep.direction === direction &&
      lastTargetNavigationStep.from === target &&
      lastTargetNavigationStep.to === current,
  );
}

function steppedTargetNavigationTarget(candidates, current, direction, { avoidBacktrack = false } = {}) {
  const startIndex = targetNavigationCandidateIndex(candidates, current, direction);
  if (startIndex < 0) return null;
  const startTarget = candidates[startIndex]?.target || null;
  if (!avoidBacktrack || !targetNavigationWouldBacktrack(startTarget, current, direction)) {
    return startTarget;
  }

  for (let offset = 1; offset < candidates.length; offset += 1) {
    const target = candidates[positiveModulo(startIndex + offset * direction, candidates.length)]?.target || null;
    if (!target || target === current) continue;
    if (!targetNavigationWouldBacktrack(target, current, direction)) return target;
  }

  return startTarget;
}

function centerViewportOnTarget(target) {
  const base = getBaseSceneLayout();
  const coordinates = targetCoordinates(target);
  const offset = projectedOffsetFor(coordinates.x, coordinates.y, coordinates.z, base.scale);
  state.panX = -offset.x;
  state.panY = -offset.y;
  updateSceneLayout();
}

function selectNavigationTarget(target, { centerViewport = false } = {}) {
  if (!target) return;
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  markOrientationGridActive();

  if (state.cameraLocked) {
    setCameraLock(true, target);
    return;
  }

  state.locked = target;
  state.hovered = null;
  const zoomChanged = clampZoomToTarget(target);
  if (centerViewport) centerViewportOnTarget(target);
  setTarget(target);
  if (zoomChanged) syncRangeOutputs();
  if (centerViewport || zoomChanged) markProjectionDirty();
  else {
    updateCoordinateReadout();
    queueRender();
  }
}

function selectSteppedNavigationTarget(target, current, direction, options = {}) {
  if (!target) return false;
  lastTargetNavigationStep = {
    from: current || null,
    to: target,
    direction,
  };
  selectNavigationTarget(target, options);
  return true;
}

function stepTargetNavigation(direction) {
  const stepDirection = targetNavigationStepDirection(direction);
  if (!stepDirection) return;

  const visibleCandidates = buildTargetNavigationCandidates();
  const current = state.locked || state.hovered;
  const visibleCurrentIndex = current
    ? visibleCandidates.findIndex((candidate) => candidate.target === current)
    : -1;

  if (visibleCandidates.length && (visibleCurrentIndex < 0 || visibleCandidates.length > 1)) {
    const visibleTarget = steppedTargetNavigationTarget(visibleCandidates, current, stepDirection, {
      avoidBacktrack: true,
    });
    if (!targetNavigationWouldBacktrack(visibleTarget, current, stepDirection)) {
      selectSteppedNavigationTarget(visibleTarget, current, stepDirection);
      return;
    }
  }

  const fullCandidates = buildFullTargetNavigationCandidates();
  if (!fullCandidates.length) return;
  const fullTarget = steppedTargetNavigationTarget(fullCandidates, current, stepDirection, {
    avoidBacktrack: true,
  });

  selectSteppedNavigationTarget(fullTarget, current, stepDirection, { centerViewport: true });
}

function projectionCacheReadyForHoverPicking() {
  return !projectionDirty && !scene.catalogProjectionFastPending && scene.catalogDrawListScreenProjected;
}

function catalogPickVisualRadius(item, { useCachedVisuals = false, simulationDay = null } = {}) {
  if (useCachedVisuals && Number.isFinite(item.currentRadius) && item.currentRadius > 0) return item.currentRadius;
  let areaPulse = 1;
  if (useCachedVisuals) {
    if (Number.isFinite(item.currentAreaPulse) && item.currentAreaPulse > 0) areaPulse = item.currentAreaPulse;
  } else if (item.point.animatePulse || item.point === state.locked) {
    areaPulse = lightCurveVisualPulses(pulseFactor(item.point, simulationDay ?? currentSimulationDay()), item.point)
      .areaPulse;
  }
  return catalogRenderVisualRadius(item, areaPulse);
}

function nearestTarget(clientX, clientY, { pickRadiusScale = 1, refreshProjection = true } = {}) {
  if (refreshProjection) {
    ensureProjectionCacheForInteraction();
  } else if (!projectionCacheReadyForHoverPicking()) {
    return null;
  }

  const radiusScale = Math.max(1, pickRadiusScale);
  const maxCatalogPickDistance = 144 * radiusScale * radiusScale;
  const useCachedVisuals = !refreshProjection;
  const simulationDay = useCachedVisuals ? null : currentSimulationDay();
  let bestCatalog = null;
  let bestCatalogDistance = maxCatalogPickDistance;
  let bestCatalogFallback = null;
  let bestCatalogFallbackDistance = maxCatalogPickDistance;

  for (const item of scene.catalogDrawList) {
    if (item.point.kind !== "catalog") continue;
    if (!targetIsPickable(item.point)) continue;
    const visualRadius = catalogPickVisualRadius(item, { useCachedVisuals, simulationDay });
    const radius =
      Math.max(CATALOG_DIRECT_PICK_MIN_RADIUS, visualRadius + CATALOG_DIRECT_PICK_PADDING_PX) *
      radiusScale;
    const dx = item.projected.x - clientX;
    const dy = item.projected.y - clientY;
    const distance = dx * dx + dy * dy;
    if (distance <= radius * radius && distance < bestCatalogDistance) {
      bestCatalog = item.point;
      bestCatalogDistance = distance;
    }
    if (distance < bestCatalogFallbackDistance) {
      bestCatalogFallback = item.point;
      bestCatalogFallbackDistance = distance;
    }
  }

  if (bestCatalog) return bestCatalog;

  let best = null;
  let bestClusterScore = Infinity;
  for (const item of scene.clusterTargetDrawList) {
    if (!targetIsPickable(item.point)) continue;
    const dx = item.projected.x - clientX;
    const dy = item.projected.y - clientY;
    const distance = dx * dx + dy * dy;
    const radius =
      Math.max(CLUSTER_TARGET_PICK_MIN_RADIUS, item.screenRadius * CLUSTER_TARGET_PICK_RADIUS_SCALE) * radiusScale;
    const radius2 = radius * radius;
    if (distance <= radius2) {
      const score = distance / radius2;
      if (score < bestClusterScore) {
        best = item.point;
        bestClusterScore = score;
      }
    }
  }

  if (best) return best;
  return bestCatalogFallback;
}

function selectTargetAt(clientX, clientY, { pickRadiusScale = 1, focusSelectedOnRepeat = false, lockCamera = false } = {}) {
  const target = nearestTarget(clientX, clientY, { pickRadiusScale });
  if (lockCamera) {
    if (target) setCameraLock(true, target);
    return target;
  }

  if (focusSelectedOnRepeat && target && target === state.locked) {
    setCameraLock(true, target);
    return target;
  }

  const wasCameraLocked = state.cameraLocked;
  lastTargetNavigationStep = null;
  state.locked = target;
  state.hovered = null;
  clearCenterSelectionForTarget(state.locked);
  if (!state.locked) {
    state.cameraLocked = false;
    state.cameraFollowsLockedTarget = false;
  }
  const zoomChanged = clampZoomToTarget(state.locked);
  setTarget(state.locked);
  if (zoomChanged) syncRangeOutputs();
  if (wasCameraLocked || zoomChanged) {
    markProjectionDirty();
  } else {
    updateCoordinateReadout();
    queueRender();
  }
  return target;
}

function resetRangeControl(controlId) {
  const preset = currentPulsatorPreset();
  cancelIntroRotation();
  cancelAxisSpinAnimation();
  if (["yaw", "pitch", "roll", "zoom"].includes(controlId)) {
    markOrientationGridActive();
  }

  switch (controlId) {
    case "yaw":
      state.yaw = 0;
      syncRangeOutputs();
      markProjectionDirty();
      break;
    case "pitch":
      state.pitch = 0;
      syncRangeOutputs();
      markProjectionDirty();
      break;
    case "roll":
      state.roll = 0;
      syncRangeOutputs();
      markProjectionDirty();
      break;
    case "zoom":
      setZoom(DEFAULT_ZOOM_SCALE);
      syncRangeOutputs();
      break;
    case "radiusScale":
      state.radiusScale = defaultRadiusScaleForPreset(preset);
      markRedClumpLayerDirty();
      syncRangeOutputs();
      queueRender();
      break;
    case "colorContrast":
      setColorContrast(COLOR_CONTRAST_DEFAULT);
      syncRangeOutputs();
      break;
    case "uncertaintySeed":
      setUncertaintySeed(DEFAULT_UNCERTAINTY_SEED);
      break;
    case "pulsationSpeed":
      setPulsationSpeed(defaultPulsationSpeedForPreset(preset));
      markCatalogStaticDirty();
      syncRangeOutputs();
      queueRender();
      break;
    case "pulsationAmplitude":
      state.pulsationAmplitudeScale = defaultPulsationAmplitudeScaleForPreset(preset);
      syncRangeOutputs();
      queueRender();
      break;
    default:
      break;
  }
}

function handleRangeReset(event) {
  if (event.type === "keydown" && event.key !== "Enter" && event.key !== " ") return;
  event.preventDefault();
  event.stopPropagation();
  resetRangeControl(event.currentTarget.dataset.resetControl);
}

function setMobileElementHidden(element, hidden) {
  if (!element) return;
  if (hidden) element.setAttribute("aria-hidden", "true");
  else element.removeAttribute("aria-hidden");
  element.inert = hidden;
}

function syncOverlayVisibility() {
  const overlaysHidden = Boolean(state.overlaysHidden);
  elements.atlas?.classList.toggle("overlays-hidden", overlaysHidden);

  if (elements.overlayToggle) {
    const label = overlaysHidden ? "Show overlays" : "Hide overlays";
    const labelElement = elements.overlayToggle.querySelector(".overlayToggleLabel");
    if (labelElement) labelElement.textContent = label;
    elements.overlayToggle.classList.toggle("active", overlaysHidden);
    elements.overlayToggle.setAttribute("aria-pressed", String(overlaysHidden));
    elements.overlayToggle.setAttribute("aria-label", label);
    elements.overlayToggle.title = label;
  }

  if (overlaysHidden) {
    mobileControlsOpen = false;
    if (elements.mobileControlsBackdrop) elements.mobileControlsBackdrop.hidden = true;
  }

  setMobileElementHidden(elements.mobileControlsToggle, overlaysHidden);
  setMobileElementHidden(controls.mobilePresetToggle, overlaysHidden);
  syncMobileControlsVisibility();
}

function setOverlaysHidden(hidden) {
  const nextHidden = Boolean(hidden);
  if (state.overlaysHidden === nextHidden) return;
  state.overlaysHidden = nextHidden;
  syncOverlayVisibility();
}

function syncMobileControlsVisibility() {
  const overlaysHidden = Boolean(state.overlaysHidden);
  const isMobile = MOBILE_CONTROLS_MEDIA.matches;
  if (overlaysHidden) mobileControlsOpen = false;
  if (!isMobile) mobileControlsOpen = false;
  const isOpen = isMobile && mobileControlsOpen;
  elements.atlas?.classList.toggle("mobile-controls-open", isOpen);
  elements.mobileControlsToggle?.setAttribute("aria-expanded", String(isOpen));
  if (elements.mobileControlsBackdrop) elements.mobileControlsBackdrop.hidden = !isOpen;
  setMobileElementHidden(elements.masthead, overlaysHidden || (isMobile && isOpen));
  setMobileElementHidden(elements.panel, isMobile && !isOpen && !overlaysHidden);
  setMobileElementHidden(elements.coordinateHud, overlaysHidden || (isMobile && !isOpen));
}

function handleMobileControlsMediaChange() {
  syncMobileControlsVisibility();
  renderMobileTargetPreview(state.locked || state.hovered);
}

function setMobileControlsOpen(open, { restoreFocus = false, focusClose = true } = {}) {
  const isMobile = MOBILE_CONTROLS_MEDIA.matches;
  const nextOpen = isMobile && Boolean(open);
  if (!nextOpen && restoreFocus && isMobile) {
    elements.mobileControlsToggle?.focus({ preventScroll: true });
  }
  mobileControlsOpen = nextOpen;
  syncMobileControlsVisibility();
  if (nextOpen && focusClose) {
    window.requestAnimationFrame(() => {
      elements.mobileControlsClose?.focus({ preventScroll: true });
    });
  }
}

function beginMobileDrawerSwipe(event) {
  if (event.pointerType !== "touch" || !MOBILE_CONTROLS_MEDIA.matches || !mobileControlsOpen) return;
  drawerSwipeGesture = {
    pointerId: event.pointerId,
    x: event.clientX,
    y: event.clientY,
  };
  try {
    elements.mobilePanelHeader?.setPointerCapture?.(event.pointerId);
  } catch {
    // Ignore capture races from interrupted mobile gestures.
  }
}

function updateMobileDrawerSwipe(event) {
  if (!drawerSwipeGesture || drawerSwipeGesture.pointerId !== event.pointerId) return;
  const dx = event.clientX - drawerSwipeGesture.x;
  const dy = event.clientY - drawerSwipeGesture.y;
  if (dy < MOBILE_DRAWER_SWIPE_CLOSE_DISTANCE || Math.abs(dx) > dy * 1.25) return;
  drawerSwipeGesture = null;
  setMobileControlsOpen(false, { restoreFocus: true });
}

function endMobileDrawerSwipe(event) {
  if (!drawerSwipeGesture || drawerSwipeGesture.pointerId !== event.pointerId) return;
  drawerSwipeGesture = null;
}

function bindMobileControls() {
  elements.mobileControlsToggle?.addEventListener("click", () => {
    requestMobileFullscreen();
    setMobileControlsOpen(true);
  });
  elements.mobileControlsClose?.addEventListener("click", () => {
    setMobileControlsOpen(false, { restoreFocus: true });
  });
  elements.mobileControlsBackdrop?.addEventListener("click", () => {
    setMobileControlsOpen(false, { restoreFocus: true });
  });
  window.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !MOBILE_CONTROLS_MEDIA.matches || !mobileControlsOpen) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    setMobileControlsOpen(false, { restoreFocus: true });
  });
  if (MOBILE_CONTROLS_MEDIA.addEventListener) {
    MOBILE_CONTROLS_MEDIA.addEventListener("change", handleMobileControlsMediaChange);
  } else {
    MOBILE_CONTROLS_MEDIA.addListener(handleMobileControlsMediaChange);
  }
  elements.mobilePanelHeader?.addEventListener("pointerdown", beginMobileDrawerSwipe);
  elements.mobilePanelHeader?.addEventListener("pointermove", updateMobileDrawerSwipe);
  elements.mobilePanelHeader?.addEventListener("pointerup", endMobileDrawerSwipe);
  elements.mobilePanelHeader?.addEventListener("pointercancel", endMobileDrawerSwipe);
  syncMobileControlsVisibility();
}

function bindControls() {
  bindMobileControls();
  buildShortcutHelp();
  elements.shortcutHelpClose?.addEventListener("click", () => setShortcutHelpOpen(false));
  elements.shortcutHelp?.addEventListener("click", (event) => {
    if (event.target === elements.shortcutHelp) setShortcutHelpOpen(false);
  });
  controls.targetSearch?.setAttribute("aria-keyshortcuts", "/");
  elements.overlayToggle?.setAttribute("aria-keyshortcuts", "H");

  elements.overlayToggle?.addEventListener("click", () => {
    setOverlaysHidden(!state.overlaysHidden);
  });

  document.querySelectorAll('input[type="range"]').forEach(bindPointerRangeFocusRelease);

  controls.yaw.addEventListener("input", () => {
    markOrientationGridActive();
    cancelAxisSpinAnimation();
    state.yaw = degreesToRadians(Number(controls.yaw.value));
    syncRangeOutputs();
    markProjectionDirty();
  });
  controls.pitch.addEventListener("input", () => {
    markOrientationGridActive();
    cancelAxisSpinAnimation();
    state.pitch = degreesToRadians(Number(controls.pitch.value));
    syncRangeOutputs();
    markProjectionDirty();
  });
  controls.roll.addEventListener("input", () => {
    markOrientationGridActive();
    cancelAxisSpinAnimation();
    state.roll = degreesToRadians(Number(controls.roll.value));
    syncRangeOutputs();
    markProjectionDirty();
  });
  document.querySelectorAll("[data-spin-axis]").forEach((button) => {
    button.addEventListener("click", () => {
      startAxisSpin(button.dataset.spinAxis);
    });
  });
  document.querySelectorAll("[data-reset-control]").forEach((label) => {
    label.addEventListener("click", handleRangeReset);
    label.addEventListener("keydown", handleRangeReset);
  });
  controls.zoom.addEventListener("input", () => {
    setZoom(10 ** Number(controls.zoom.value));
    syncRangeOutputs();
  });
  controls.radiusScale.addEventListener("input", () => {
    state.radiusScale = clampRadiusScale(10 ** Number(controls.radiusScale.value));
    markRedClumpLayerDirty();
    syncRangeOutputs();
    queueRender();
  });
  const updateColorContrast = () => {
    setColorContrast(controls.colorContrast.value);
    syncRangeOutputs();
  };
  controls.colorContrast.addEventListener("input", updateColorContrast);
  controls.colorContrast.addEventListener("change", updateColorContrast);
  controls.uncertaintySeed.addEventListener("input", () => {
    requestUncertaintySeed(controls.uncertaintySeed.value);
  });
  controls.uncertaintySeed.addEventListener("change", () => {
    setUncertaintySeed(controls.uncertaintySeed.value);
  });
  document.querySelectorAll("[data-exposure]").forEach((input) => {
    input.addEventListener("input", () => {
      setDatasetExposure(input.dataset.exposure, 10 ** Number(input.value));
    });
  });

  const updatePulsationSpeed = () => {
    setPulsationSpeed(10 ** Number(controls.pulsationSpeed.value));
    markCatalogStaticDirty();
    syncRangeOutputs();
    queueRender();
  };
  controls.pulsationSpeed.addEventListener("input", updatePulsationSpeed);
  controls.pulsationSpeed.addEventListener("change", updatePulsationSpeed);

  const updatePulsationAmplitude = () => {
    state.pulsationAmplitudeScale = clampPulsationAmplitudeScale(10 ** Number(controls.pulsationAmplitude.value));
    syncRangeOutputs();
    queueRender();
  };
  controls.pulsationAmplitude.addEventListener("input", updatePulsationAmplitude);
  controls.pulsationAmplitude.addEventListener("change", updatePulsationAmplitude);

  [controls.datasetPresetToggle, controls.mobilePresetToggle].filter(Boolean).forEach((button) => {
    button.addEventListener("click", () => {
      if (button === controls.mobilePresetToggle) requestMobileFullscreen();
      applyPulsatorPreset(nextPulsatorPreset());
    });
  });

  document.querySelectorAll("[data-dataset-preset]").forEach((button) => {
    const preset = button.dataset.datasetPreset;
    button.addEventListener("pointerenter", () => beginDatasetPresetPreview(preset));
    button.addEventListener("pointerleave", () => endDatasetPresetPreview(preset));
    button.addEventListener("focus", () => beginDatasetPresetPreview(preset));
    button.addEventListener("blur", () => endDatasetPresetPreview(preset));
    button.addEventListener("click", () => commitDatasetPreset(preset));
  });

  controls.targetSearch.addEventListener("input", handleTargetSearchInput);
  controls.targetSearch.addEventListener("keydown", handleTargetSearchKeydown);

  document.querySelectorAll("[data-dataset]").forEach((input) => {
    input.addEventListener("change", () => {
      setDatasetVisibility(input.dataset.dataset, input.checked);
      syncDatasetCheckboxes();
      syncDatasetPresetToggle();
      invalidateActivePointLists();
      clearHiddenTargetSelection();
      markProjectionDirty();
    });
  });

  controls.panLock.addEventListener("change", () => {
    state.panLock = controls.panLock.checked;
    syncRangeOutputs();
  });

  elements.coordinateReadout.addEventListener("change", (event) => {
    const input = event.target.closest("[data-sky-grid]");
    if (!input) return;
    if (input.dataset.skyGrid === "equatorial") {
      state.equatorialGrid = input.checked;
    } else if (input.dataset.skyGrid === "galactic") {
      state.galacticGrid = input.checked;
    }
    syncRangeOutputs();
    queueRender();
  });

  elements.faceView?.setAttribute("aria-keyshortcuts", "V");
  elements.edgeView?.setAttribute("aria-keyshortcuts", "V");
  elements.faceView?.addEventListener("click", () => applyViewOrientation(FACE_VIEW_ANGLES_DEGREES));
  elements.edgeView?.addEventListener("click", () => applyViewOrientation(EDGE_VIEW_ANGLES_DEGREES));

  canvas.addEventListener("pointerdown", (event) => {
    if (handleCanvasTouchPointerDown(event)) return;
    event.preventDefault();
    canvas.focus({ preventScroll: true });
    cancelIntroRotation();
    cancelAxisSpinAnimation();
    setCursorPosition(event);
    dragging = true;
    movedDuringDrag = false;
    pointerMode = pointerModeForEvent(event);
    setDragStart(event);
    canvas.classList.add("is-dragging");
    canvas.setPointerCapture(event.pointerId);
  });

  canvas.addEventListener("pointermove", (event) => {
    if (handleCanvasTouchPointerMove(event)) return;
    if (dragging && dragStart) {
      const nextMode = pointerModeForEvent(event);
      if (nextMode !== pointerMode) {
        pointerMode = nextMode;
        setDragStart(event);
      }

      const dx = event.clientX - dragStart.x;
      const dy = event.clientY - dragStart.y;
      if (Math.abs(dx) + Math.abs(dy) > 3) movedDuringDrag = true;

      if (pointerMode === "pan") {
        if (movedDuringDrag) {
          const panSensitivity = panDragSensitivity(dragStart.zoom);
          const panX = dragStart.panX + dx * panSensitivity;
          const panY = dragStart.panY + dy * panSensitivity;
          if (state.panLock) {
            state.panX = panX;
            state.panY = panY;
          } else {
            state.customCoordinateContext = coordinateContextAfterScreenPan(
              dragStart.coordinateContext,
              panX,
              panY,
              dragStart.scale,
            );
            state.panX = 0;
            state.panY = 0;
            clearCoordinateCenterSelection();
          }
          if (state.locked || state.cameraLocked) clearTargetSelection();
          updateSceneLayout();
        }
      } else if (pointerMode === "roll") {
        state.roll = normalizeRadians(dragStart.roll + dx * 0.006);
      } else {
        const orbitSensitivity = orbitDragSensitivity(dragStart.zoom);
        state.yaw = normalizeRadians(dragStart.yaw + dx * 0.004 * orbitSensitivity);
        state.pitch = normalizeRadians(dragStart.pitch + dy * 0.0032 * orbitSensitivity);
      }

      if (movedDuringDrag) markOrientationGridActive();
      setCursorPosition(event);
      syncRangeOutputs();
      markProjectionDirty();
      return;
    }

    setCursorPosition(event);
    window.clearTimeout(hoverTimer);
    if (performance.now() < hoverSuppressedUntil) return;
    const hoverX = event.clientX;
    const hoverY = event.clientY;
    hoverTimer = window.setTimeout(() => {
      if (!projectionCacheReadyForHoverPicking()) return;
      const nextHovered = nearestTarget(hoverX, hoverY, { refreshProjection: false });
      if (nextHovered === state.hovered) return;
      state.hovered = nextHovered;
      markCatalogStaticDirty();
      if (!state.locked) setTarget(state.hovered);
      queueRender();
    }, 20);
  });

  canvas.addEventListener("pointerup", (event) => {
    if (handleCanvasTouchPointerUp(event)) return;
    setCursorPosition(event);
    dragging = false;
    dragStart = null;
    canvas.classList.remove("is-dragging");
    if (movedDuringDrag && pointerMode === "pan") {
      window.clearTimeout(hoverTimer);
      hoverSuppressedUntil = performance.now() + 350;
      clearTargetSelection();
      markProjectionDirty();
      return;
    }

    if (!movedDuringDrag && pointerMode === "orbit" && event.button === 0) {
      if (MOBILE_CONTROLS_MEDIA.matches) {
        selectMobileTapTarget(touchPointFromEvent(event));
      } else {
        selectTargetAt(event.clientX, event.clientY);
      }
    } else if (!movedDuringDrag && pointerMode === "pan" && event.button === 2) {
      if (consumeRightDoubleClick(event)) {
        queueRender();
        return;
      }
      clearTargetSelection();
      queueRender();
    }
  });

  canvas.addEventListener("pointerleave", (event) => {
    if (activeTouchPointers.has(event.pointerId)) return;
    if (!dragging) clearCursorPosition();
  });

  canvas.addEventListener("dblclick", (event) => {
    event.preventDefault();
    if (MOBILE_CONTROLS_MEDIA.matches) return;
    setCursorPosition(event);
    selectTargetAt(event.clientX, event.clientY, { lockCamera: true });
  });

  canvas.addEventListener("pointercancel", (event) => {
    if (handleCanvasTouchPointerCancel(event)) return;
    dragging = false;
    dragStart = null;
    canvas.classList.remove("is-dragging");
  });

  canvas.addEventListener("contextmenu", (event) => {
    event.preventDefault();
  });

  canvas.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
      setCursorPosition(event);
      const next = state.zoom * Math.exp(-event.deltaY * 0.0012);
      setZoom(next, event.clientX, event.clientY, { allowTargetZoom: true, focusTarget: true });
      syncRangeOutputs();
    },
    { passive: false },
  );

  window.addEventListener("keydown", handleViewportKeydown);
  window.addEventListener("resize", resizeCanvas);
}

function buildLegend() {
  elements.legend.replaceChildren();
  scene.spectralClasses.forEach((spec, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "active";
    button.dataset.spectral = String(index);
    button.title = spec.range;

    const swatch = document.createElement("span");
    swatch.className = "swatch";
    swatch.style.background = spec.color;
    swatch.style.color = spec.color;

    const label = document.createElement("span");
    label.textContent = spec.id;

    button.append(swatch, label);
    button.addEventListener("click", () => {
      if (state.spectral.has(index)) state.spectral.delete(index);
      else state.spectral.add(index);
      syncSpectralControls();
      invalidateActivePointLists();
      markProjectionDirty();
    });
    button.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      const isSoloed = state.spectral.size === 1 && state.spectral.has(index);
      state.spectral = isSoloed
        ? new Set(scene.spectralClasses.map((_, classIndex) => classIndex))
        : new Set([index]);
      syncSpectralControls();
      invalidateActivePointLists();
      markProjectionDirty();
    });
    elements.legend.append(button);
  });
  syncSpectralControls();
}

function buildSources() {
  elements.sources.replaceChildren();
  for (const source of scene.payload.sources) {
    const link = document.createElement("a");
    link.href = source.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = source.name;
    elements.sources.append(link);
  }
}

function syncSpectralControls() {
  elements.legend.querySelectorAll("[data-spectral]").forEach((button) => {
    button.classList.toggle("active", state.spectral.has(Number(button.dataset.spectral)));
  });
}

function redClumpGridPosition(row) {
  return {
    x: Math.round(row[RC.lon] * RED_CLUMP_GRID_QUANTIZATION),
    y: Math.round(row[RC.lat] * RED_CLUMP_GRID_QUANTIZATION),
  };
}

function redClumpGridKey(x, y) {
  return `${x}:${y}`;
}

function hasOpenRedClumpNeighbor(cellSet, x, y, radius) {
  for (let dx = -radius; dx <= radius; dx += 1) {
    if (!cellSet.has(redClumpGridKey(x + dx, y - radius))) return true;
    if (!cellSet.has(redClumpGridKey(x + dx, y + radius))) return true;
  }

  for (let dy = -radius + 1; dy <= radius - 1; dy += 1) {
    if (!cellSet.has(redClumpGridKey(x - radius, y + dy))) return true;
    if (!cellSet.has(redClumpGridKey(x + radius, y + dy))) return true;
  }

  return false;
}

function redClumpEdgeAlpha(edgeDistance) {
  const edgeFade = smoothStep((edgeDistance + 0.5) / RED_CLUMP_EDGE_FEATHER_CELLS);
  return RED_CLUMP_EDGE_ALPHA_FLOOR + (1 - RED_CLUMP_EDGE_ALPHA_FLOOR) * edgeFade;
}

function redClumpEdgeWeights(rows) {
  const positions = rows.map(redClumpGridPosition);
  const cellSet = new Set(positions.map((cell) => redClumpGridKey(cell.x, cell.y)));

  return positions.map((cell) => {
    let edgeDistance = RED_CLUMP_EDGE_FEATHER_CELLS;
    for (let radius = 1; radius <= RED_CLUMP_EDGE_FEATHER_CELLS; radius += 1) {
      if (hasOpenRedClumpNeighbor(cellSet, cell.x, cell.y, radius)) {
        edgeDistance = radius - 1;
        break;
      }
    }
    return redClumpEdgeAlpha(edgeDistance);
  });
}

function buildRedClumpSurface(points) {
  const pointByCell = new Map(points.map((point) => [point.gridKey, point]));
  const cells = [];

  for (const point of points) {
    const { x, y } = point.grid;
    const east = pointByCell.get(redClumpGridKey(x + 1, y));
    const north = pointByCell.get(redClumpGridKey(x, y + 1));
    const northeast = pointByCell.get(redClumpGridKey(x + 1, y + 1));
    if (!east || !north || !northeast) continue;
    const projected = [null, null, null, null];
    const edgeAlpha = (point.edgeAlpha + east.edgeAlpha + northeast.edgeAlpha + north.edgeAlpha) / 4;
    const densityAlpha = (point.densityAlpha + east.densityAlpha + northeast.densityAlpha + north.densityAlpha) / 4;
    const effectiveCount =
      (redClumpDensityCountForPoint(point) +
        redClumpDensityCountForPoint(east) +
        redClumpDensityCountForPoint(northeast) +
        redClumpDensityCountForPoint(north)) *
      0.25;

    cells.push({
      points: [point, east, northeast, north],
      projected,
      drawItem: {
        kind: "redclump",
        points: [point, east, northeast, north],
        projected,
        z: 0,
        alphaUnit: 0,
        vertexAlphaUnits: [0, 0, 0, 0],
        surfaceAlpha: 0,
        surfaceAlphaSignature: null,
        surfaceVertexAlphas: [0, 0, 0, 0],
        starRadius: 0,
        effectiveCount,
        edgeAlpha,
        densityAlpha,
      },
      edgeAlpha,
      densityAlpha,
      effectiveCount,
    });
  }

  return cells;
}

function preparePoints(payload) {
  scene.payload = payload;
  scene.spectralClasses = payload.spectralClasses;
  scene.temperatureAnchors = normalizedTemperatureAnchors(payload.meta?.viTemperatureCalibration?.anchors);
  scene.temperatureGrid = normalizedTemperatureGrid(payload.meta?.viLuminosityTemperatureCalibration);
  scene.meanMetallicityFeHByLocation = normalizedMeanMetallicityFeHByLocation(payload.meta?.meanMetallicityFeHByLocation);
  scene.miraTemperatureSources = Array.isArray(payload.meta?.miraTemperatureSources)
    ? payload.meta.miraTemperatureSources
    : [];
  colorCache.clear();
  catalogTemperatureColorCache.clear();
  scene.bounds = payload.bounds;
  scene.coordinateContext = coordinateContextFromPayload(payload);
  scene.skyGridBounds = skyGridBoundsFromPayload(payload);
  scene.catalog = payload.datasets.catalog.map((row) => {
    const projected = { x: 0, y: 0, z: 0, perspective: 1 };
    const intrinsicVMinusI = intrinsicVMinusIForRow(row);
    const baseCoordinates = catalogCoordinates(row);
    const point = {
      kind: "catalog",
      row,
      baseCoordinates,
      coordinates: baseCoordinates,
      activeCoordinates: null,
      projected,
      currentDistance: row[IDX.distance],
      currentLum: row[IDX.lum],
      currentLogLum: row[IDX.logLum],
      currentRadius: row[IDX.radius],
      radiusUnit: pointRadiusUnitFromStellarRadius(row[IDX.radius]),
      alphaBaseUnit: pointAlphaUnitBaseFromLuminosity(row[IDX.lum]) * BASE_LUMINOSITY_FACTOR,
      vMinusI: Number.isFinite(row[IDX.vMinusI]) ? row[IDX.vMinusI] : null,
      vMinusI0: Number.isFinite(intrinsicVMinusI) ? intrinsicVMinusI : null,
      color: colorForCatalogState(row, intrinsicVMinusI, row[IDX.logLum]),
      sample: hashString(String(row[IDX.id])) % 100,
      searchText: catalogSearchTextForRow(row),
      lightCurve: makeWaveform(row),
    };
    point.drawItem = {
      point,
      projected,
      baseRadius: 0,
      alphaUnit: 0,
      currentPulse: 1,
      currentAreaPulse: 1,
      currentOpacityPulse: 1,
      currentAlpha: 0,
      currentRadius: 0,
      currentColor: null,
      currentRgb: null,
      currentRgbArray: null,
      currentRgbOffset: 0,
      slowPulseThrottle: false,
      catalogWorldPulseIndex: -1,
      staticBaseRadius: -1,
      staticAlphaUnit: -1,
      staticLodAlpha: -1,
      staticRadiusFactor: -1,
      staticRadiusScale: -1,
      staticExposure: -1,
      staticRadius: 0,
      staticAlpha: 0,
    };
    return point;
  });
  const clusterGlowBinsByIndex = new Map();
  for (const row of payload.datasets.clusterGlowBins || []) {
    const clusterIndex = row[CG.cluster];
    let bins = clusterGlowBinsByIndex.get(clusterIndex);
    if (!bins) {
      bins = [];
      clusterGlowBinsByIndex.set(clusterIndex, bins);
    }
    bins.push({
      outerRadius: row[CG.outerRadius],
      luminosity: row[CG.lum],
      vMinusI0: row[CG.vMinusI0],
      color: colorForVMinusI(row[CG.vMinusI0], 4),
    });
  }
  for (const bins of clusterGlowBinsByIndex.values()) {
    bins.sort((left, right) => left.outerRadius - right.outerRadius);
  }
  const clusterHrBinsByIndex = new Map();
  for (const row of payload.datasets.clusterHrBins || []) {
    const clusterIndex = row[CHR.cluster];
    let bins = clusterHrBinsByIndex.get(clusterIndex);
    if (!bins) {
      bins = [];
      clusterHrBinsByIndex.set(clusterIndex, bins);
    }
    bins.push({
      vMinusI0: row[CHR.vMinusI0],
      logLum: row[CHR.logLum],
      count: row[CHR.count],
      luminosity: row[CHR.lum],
      temperature: row[CHR.temperature],
      radius: row[CHR.radius],
      color: colorForVMinusI(row[CHR.vMinusI0], 5),
    });
  }
  for (const bins of clusterHrBinsByIndex.values()) {
    bins.sort((left, right) => left.logLum - right.logLum);
  }
  const clusterRows = payload.datasets.clusters || [];
  const clusterBaseCoordinatesByIndex = clusterRows.map((row) => clusterCoordinates(row));
  const clusterRenderedLuminosityByIndex = new Array(clusterBaseCoordinatesByIndex.length).fill(0);
  const clusterRenderedColorSumsByIndex = clusterBaseCoordinatesByIndex.map(() => [0, 0, 0]);
  const clusterPulsatorStripModel = buildObservedInstabilityStripModel(payload.datasets.catalog || []);
  const clusterPulsatorStats = {
    total: 0,
    byDataset: Object.fromEntries(CLUSTER_PULSATOR_STRIP_DATASET_KEYS.map((key) => [key, 0])),
    referenceModelStars: Object.fromEntries(
      clusterPulsatorStripModel.strips.map((strip) => [strip.datasetKey, strip.samples.length]),
    ),
  };
  scene.clusterStarsByCluster = new Map();
  scene.clusterStars = (payload.datasets.clusterStars || []).map((row, index) => {
    const clusterIndex = row[CS.cluster];
    const clusterRow = clusterRows[clusterIndex];
    const projected = { x: 0, y: 0, z: 0, perspective: 1 };
    const baseCoordinates = clusterStarCoordinates(row);
    const clusterBaseCoordinates = clusterBaseCoordinatesByIndex[clusterIndex];
    const clusterOffsetVector = clusterBaseCoordinates
      ? [
          baseCoordinates.galacticVector[0] - clusterBaseCoordinates.galacticVector[0],
          baseCoordinates.galacticVector[1] - clusterBaseCoordinates.galacticVector[1],
          baseCoordinates.galacticVector[2] - clusterBaseCoordinates.galacticVector[2],
        ]
      : [0, 0, 0];
    const pulsatorMatch = clusterStarInstabilityStripMatch(row, clusterPulsatorStripModel);
    const lightCurve = makeClusterStarWaveform(row, index, clusterRow, pulsatorMatch);
    if (lightCurve) {
      clusterPulsatorStats.total += 1;
      clusterPulsatorStats.byDataset[lightCurve.referenceDatasetKey] =
        (clusterPulsatorStats.byDataset[lightCurve.referenceDatasetKey] || 0) + 1;
    }
    const point = {
      kind: "clusterStar",
      row,
      clusterIndex,
      clusterPulsatorMatch: lightCurve
        ? {
            datasetKey: lightCurve.referenceDatasetKey,
            referenceId: lightCurve.referenceId,
            score: pulsatorMatch.score,
          }
        : null,
      baseCoordinates,
      coordinates: baseCoordinates,
      clusterOffsetVector,
      activeCoordinates: null,
      projected,
      currentDistance: row[CS.distance],
      currentLum: row[CS.lum],
      currentLogLum: row[CS.logLum],
      radiusUnit: pointRadiusUnitFromStellarRadius(row[CS.radius]),
      alphaBaseUnit: pointAlphaUnitBaseFromLuminosity(row[CS.lum]) * BASE_LUMINOSITY_FACTOR,
      vMinusI0: Number.isFinite(row[CS.vMinusI0]) ? row[CS.vMinusI0] : null,
      color: Number.isFinite(row[CS.temperature])
        ? colorForTemperature(row[CS.temperature])
        : colorForVMinusI(row[CS.vMinusI0], row[CS.spectral]),
      sample: hashString(`cs-${row[CS.cluster]}-${index}`) % 100,
      lightCurve,
    };
    const starLuminosity = Number.isFinite(row[CS.lum]) ? Math.max(0, row[CS.lum]) : 0;
    const renderedColorSums = clusterRenderedColorSumsByIndex[clusterIndex];
    if (starLuminosity > 0 && renderedColorSums) {
      const rgbValue = cssColorToRgb(point.color);
      clusterRenderedLuminosityByIndex[clusterIndex] += starLuminosity;
      renderedColorSums[0] += rgbValue[0] * starLuminosity;
      renderedColorSums[1] += rgbValue[1] * starLuminosity;
      renderedColorSums[2] += rgbValue[2] * starLuminosity;
    }
    let clusterStars = scene.clusterStarsByCluster.get(clusterIndex);
    if (!clusterStars) {
      clusterStars = [];
      scene.clusterStarsByCluster.set(clusterIndex, clusterStars);
    }
    clusterStars.push(point);
    point.drawItem = {
      point,
      projected,
      baseRadius: 0,
      alphaUnit: 0,
      currentPulse: 1,
      currentAreaPulse: 1,
      currentOpacityPulse: 1,
      currentAlpha: 0,
      currentRadius: 0,
      currentColor: null,
      currentRgb: null,
      currentRgbArray: null,
      currentRgbOffset: 0,
      slowPulseThrottle: false,
      catalogWorldPulseIndex: -1,
      staticBaseRadius: -1,
      staticAlphaUnit: -1,
      staticLodAlpha: -1,
      staticRadiusFactor: -1,
      staticRadiusScale: -1,
      staticExposure: -1,
      staticRadius: 0,
      staticAlpha: 0,
    };
    return point;
  });
  scene.clusterPulsatorStats = clusterPulsatorStats;
  scene.clusters = clusterRows.map((row, index) => {
    const projected = { x: 0, y: 0, z: 0, perspective: 1 };
    const baseCoordinates = clusterBaseCoordinatesByIndex[index] || clusterCoordinates(row);
    const renderedLuminosity = clusterRenderedLuminosityByIndex[index] || 0;
    const renderedColorSums = clusterRenderedColorSumsByIndex[index];
    const renderedStarGlowRgb =
      renderedLuminosity > 0 && renderedColorSums
        ? renderedColorSums.map((value) => Math.round(value / renderedLuminosity))
        : cssColorToRgb(colorForVMinusI(row[CL.unresolvedVMinusI0], 4));
    const glowBins = clusterGlowBinsByIndex.get(index) || [];
    const glowOuterRadiusFraction = glowBins.reduce((outer, bin) => Math.max(outer, bin.outerRadius || 0), 1);
    const point = {
      kind: "cluster",
      index,
      row,
      baseCoordinates,
      coordinates: baseCoordinates,
      activeCoordinates: null,
      projected,
      activeProjected: null,
      currentDistance: row[CL.distance],
      radiusPc: row[CL.radiusPc],
      glowAlphaBaseUnit: pointAlphaUnitBaseFromLuminosity(row[CL.unresolvedLum] || 0),
      renderedStarGlowAlphaBaseUnit: pointAlphaUnitBaseFromLuminosity(renderedLuminosity) * BASE_LUMINOSITY_FACTOR,
      renderedStarGlowRgb,
      glowOuterRadiusFraction,
      glowBins,
      hrBins: clusterHrBinsByIndex.get(index) || [],
      sample: hashString(`cluster-${row[CL.name]}-${index}`) % 100,
      searchText: clusterSearchTextForRow(row),
    };
    point.drawItem = {
      point,
      projected,
      screenRadius: 10,
      glowAlphaUnit: 0,
      renderedStarGlowAlphaUnit: 0,
      clusterStarLodAlpha: 0,
    };
    return point;
  });
  const redClumpEdgeFactors = redClumpEdgeWeights(payload.datasets.redClump);
  scene.redClump = payload.datasets.redClump.map((row, index) => {
    const grid = redClumpGridPosition(row);
    const projected = { x: 0, y: 0, z: 0, perspective: 1 };
    const point = {
      kind: "redclump",
      row,
      grid,
      gridKey: redClumpGridKey(grid.x, grid.y),
      coordinates: redClumpCoordinates(row),
      activeCoordinates: null,
      projected,
      activeProjected: null,
      sample: hashString(`rc-${index}`) % 100,
      edgeAlpha: redClumpEdgeFactors[index],
      densityAlpha: redClumpDensityAlpha(row[RC.densityUnit]),
    };
    point.drawItem = {
      point,
      projected,
      radius: 0,
      alphaUnit: 0,
      edgeAlpha: point.edgeAlpha,
    };
    return point;
  });
  smoothRedClumpDensities(scene.redClump);
  scene.redClumpSurface = buildRedClumpSurface(scene.redClump);
  if (state.uncertaintySeed !== DEFAULT_UNCERTAINTY_SEED) {
    applyUncertaintyRealization({ updateTarget: false });
  }
  invalidateCoordinateCache();
  invalidateActivePointLists();

  outputs.cepheidCount.textContent = formatInteger(
    (payload.counts.cepheids || 0) + (payload.counts.anomalousCepheids || 0),
  );
  outputs.rrCount.textContent = formatInteger(payload.counts.rrLyrae);
  if (outputs.miraCount) {
    outputs.miraCount.textContent = formatInteger(payload.counts.miras || 0);
  }
  if (outputs.rcCount) {
    outputs.rcCount.textContent = formatInteger(payload.counts.redClumpCells);
  }
  if (outputs.clusterCount) {
    outputs.clusterCount.textContent = formatInteger(payload.counts.clusters || 0);
  }
  markProjectionDirty();
}

async function init() {
  try {
    bindControls();
    buildCoordinateControls();
    syncRangeOutputs();
    resizeCanvas();
    const payload = await fetchAtlasPayload();
    primeIntroRotation();
    setLoadingProgress(0.94);
    await nextFrame();
    preparePoints(payload);
    setLoadingProgress(0.98);
    buildLegend();
    buildSources();
    setTarget(null);
    setLoadingProgress(1);
    await prewarmIntroFrame();
    elements.loading.classList.add("hidden");
    startIntroRotation();
    queueRender();
  } catch (error) {
    elements.loading.classList.add("error");
    elements.loading.textContent = `Could not load atlas data: ${error.message}`;
    console.error(error);
  }
}

if (PERF_HUD_ENABLED) {
  window.__mcAtlasPerf = {
    drawCatalog,
    invalidateActivePointLists,
    invalidateCoordinateCache,
    rebuildProjectionCache,
    setView({ yaw = state.yaw, pitch = state.pitch, roll = state.roll, zoom = state.zoom }) {
      introRotation = null;
      introCloudLabelAnimation = null;
      axisSpinAnimation = null;
      state.yaw = yaw;
      state.pitch = pitch;
      state.roll = roll;
      state.zoom = clampZoomScale(zoom);
      state.panX = 0;
      state.panY = 0;
      updateSceneLayout();
    },
    ready() {
      return Boolean(scene.payload);
    },
  };
}

init();
