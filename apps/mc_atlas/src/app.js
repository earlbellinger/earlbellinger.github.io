const DATA_VERSION = "20260509-cluster-hr-diagram-mist-teff";
const DATA_URL = `./public/data/magellanic-clouds.json?v=${DATA_VERSION}`;
const DATA_DOWNLOAD_PROGRESS_MAX = 0.88;
const ZOOM_BASE_SCALE = 1.62;
const DEFAULT_ZOOM_SCALE = 1;
const ZOOM_SCALE_MIN = 0.5;
const ZOOM_SCALE_MAX = 1000;
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
const PULSATOR_RADIUS_BASE_SCALE = 0.31752;
const INITIAL_PULSATION_SPEED = 18_000;
const PULSATION_SPEED_MIN = 1;
const PULSATION_SPEED_MAX = 25_000_000;
const PULSATION_FLICKER_FREQUENCY_HZ = 2;
const PULSATION_AMPLITUDE_MIN = 1;
const PULSATION_AMPLITUDE_MAX = 20;
const PULSATION_AMPLITUDE_DEFAULT = 10;
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
const STAR_RADIUS_ZOOM_GAIN = 0.18;
const STAR_RADIUS_ZOOM_MAX_BOOST = 1.2;
const STAR_RADIUS_ZOOM_BASE_GAIN = 0.75;
const STAR_RADIUS_ZOOM_SIZE_MAX = 20;
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
const RED_CLUMP_GPU_VERTEX_FLOATS = 6;
// User-facing yaw zero is the observer-side OGLE view.
const OBSERVED_VIEW_YAW_DEGREES = -180;
const OBSERVED_VIEW_ROLL_DEGREES = 0;
const DEFAULT_VIEW_AXIS_ROTATION_DEGREES = 15;
const INTRO_ROTATION_START_YAW_DEGREES = -180;
const INTRO_ROTATION_START_PITCH_DEGREES = 0;
const INTRO_ROTATION_START_ROLL_DEGREES = 0;
const AXIS_SPIN_AXES = new Set(["yaw", "pitch", "roll"]);
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
// Baseline radii are 0.75x the previous calibration; class presets compensate to preserve tuned visual sizes.
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
const OGLE_OCVS_OBJECT_URL = "https://ogledb.astrouw.edu.pl/~ogle/OCVS/getobj.php?s=";
const OGLE_III_CVS_OBJECT_URL = "https://ogledb.astrouw.edu.pl/~ogle/CVS/o.php?";
const SUN_ABSOLUTE_I_MAG = 4.1;
const RED_CLUMP_MI = -0.25;
const RED_CLUMP_LUMINOSITY = 10 ** (-0.4 * (RED_CLUMP_MI - SUN_ABSOLUTE_I_MAG));
const RED_CLUMP_TEMPERATURE = 4800;
const RED_CLUMP_RADIUS = Math.sqrt(RED_CLUMP_LUMINOSITY) * (5772 / RED_CLUMP_TEMPERATURE) ** 2;
const RED_CLUMP_GRID_QUANTIZATION = 4;
const RED_CLUMP_EDGE_FEATHER_CELLS = 10;
const RED_CLUMP_EDGE_ALPHA_FLOOR = 0.08;
// Keep the red clump map-like, but let the Gaia RC-like count proxy gently nudge brightness.
const RED_CLUMP_EXPOSURE_DEFAULT = 1;
const RED_CLUMP_EXPOSURE_RENDER_SCALE = 0.4;
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
const MAX_MIRA_COLOR_PULSE_OFFSET = 2.2;
const MAX_MIRA_PRIOR_ASSISTED_COLOR_PULSE_OFFSET = 2.0;
const MAX_MIRA_PRIOR_ONLY_COLOR_PULSE_OFFSET = 1.6;
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
const BLACKBODY_DISPLAY_TEMPERATURE_CONTRAST = 3.6;
const BLACKBODY_DISPLAY_WHITEPOINT_RGB = [255, 255, 255];
const BLACKBODY_DISPLAY_CHROMA_BOOST = 2.0;
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
const MOBILE_CONTROLS_MEDIA = window.matchMedia("(max-width: 860px)");
const MOBILE_TOUCH_MOVE_THRESHOLD = 7;
const MOBILE_PINCH_MOVE_THRESHOLD = 3;
const MOBILE_TARGET_PICK_RADIUS_SCALE = 2.25;
const MOBILE_STAR_BASE_RADIUS_SCALE = 0.5;
const MOBILE_DRAWER_SWIPE_CLOSE_DISTANCE = 58;
let mobileControlsOpen = false;

const controls = {
  yaw: document.querySelector("#yaw"),
  pitch: document.querySelector("#pitch"),
  roll: document.querySelector("#roll"),
  zoom: document.querySelector("#zoom"),
  radiusScale: document.querySelector("#radiusScale"),
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
  mobilePanelHeader: document.querySelector(".mobilePanelHeader"),
};

const state = {
  yaw: 0,
  pitch: 0,
  roll: 0,
  zoom: DEFAULT_ZOOM_SCALE,
  panX: 0,
  panY: 0,
  radiusScale: defaultRadiusScaleForPreset(PULSATOR_DEFAULT_PRESET),
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
  overlaysHidden: false,
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
  pulsationSpeed: {
    label: "speed",
    digits: 0,
    inputMode: "numeric",
    min: () => 10 ** Number(controls.pulsationSpeed.min),
    max: () => 10 ** Number(controls.pulsationSpeed.max),
    get: () => state.pulsationSpeed,
    set: (value) => {
      const speed = clampPulsationSpeed(value);
      state.pulsationSpeed = speed;
      state.pulsationSpeedLog = Math.log10(speed);
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
  catalogDrawList: [],
  catalogAnimatedDrawList: [],
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
  catalogStaticRenderer: null,
  catalogRenderer: null,
  redClumpRenderer: null,
  redClumpGpuDirty: true,
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
let activeLightcurveInset = null;
let lastRightClick = { time: 0, x: 0, y: 0 };
let introRotation = null;
let introCloudLabelAnimation = null;
let axisSpinAnimation = null;
let datasetPresetPreview = null;
const animationStartMs = performance.now();
let orientationGridLastActivityMs = animationStartMs;
const animationEpoch = 6000;
const WAVEFORM_SAMPLES = 96;
const LIGHTCURVE_INSET_CYCLES = 2;
const MIRA_LIGHTCURVE_INSET_CYCLES = 10;
const MIRA_AMPLITUDE_STATS_CYCLES = 30;
const SVG_NS = "http://www.w3.org/2000/svg";
const colorCache = new Map();
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

function clampZoomScale(value) {
  return clamp(value, ZOOM_SCALE_MIN, ZOOM_SCALE_MAX);
}

function effectiveZoomScale(value = state.zoom) {
  return clampZoomScale(value) * ZOOM_BASE_SCALE;
}

function panDragSensitivity(value = state.zoom) {
  const zoomSteps = Math.max(0, Math.log2(Math.max(1, clampZoomScale(value))));
  return Math.max(PAN_DRAG_MIN_SENSITIVITY, 1 / (1 + zoomSteps * PAN_DRAG_ZOOM_DAMPING));
}

function orbitDragSensitivity(value = state.zoom) {
  const zoomSteps = Math.max(0, Math.log2(Math.max(1, clampZoomScale(value))));
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
    `pulse mode ${CATALOG_PULSE_ALL_STARS || !PULSE_LOD_ENABLED ? "all" : "lod"}`,
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
  unit.textContent = config.unit || "x";
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
  unit.textContent = config.unit || "x";

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

function effectiveTemperatureFromVMinusI(vMinusI) {
  const anchors = V_MINUS_I_TEMPERATURE_ANCHORS;
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

  return clamp(
    BLACKBODY_DISPLAY_WHITEPOINT_TEMPERATURE * Math.exp(logRatio * BLACKBODY_DISPLAY_TEMPERATURE_CONTRAST),
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

  const cacheKey = clamp(
    Math.round(vMinusI * COLOR_CACHE_PRECISION),
    Math.round(V_MINUS_I_TEMPERATURE_ANCHORS[0].vMinusI * COLOR_CACHE_PRECISION),
    Math.round(V_MINUS_I_TEMPERATURE_ANCHORS[V_MINUS_I_TEMPERATURE_ANCHORS.length - 1].vMinusI * COLOR_CACHE_PRECISION),
  );
  const cached = colorCache.get(cacheKey);
  if (cached) return cached;

  const cachedVMinusI = cacheKey / COLOR_CACHE_PRECISION;
  const color = colorForTemperature(effectiveTemperatureFromVMinusI(cachedVMinusI));
  colorCache.set(cacheKey, color);
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

function seededUnit(value) {
  return (hashString(value) % 100000) / 100000;
}

function positiveModulo(value, divisor) {
  return ((value % divisor) + divisor) % divisor;
}

function currentSimulationDay() {
  const elapsedMs = performance.now() - animationStartMs;
  return animationEpoch + (elapsedMs / 86400000) * state.pulsationSpeed;
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
  const colors = new Array(WAVEFORM_SAMPLES);
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
    const brightnessMagnitudeOffset = miraVComponents
      ? vMagnitudeOffsets[index] - meanVMagnitudeOffset
      : (iMagnitudeOffset - meanIMagnitudeOffset) * brightnessAmplitudeScale;
    const rawColorOffset = rawColorOffsets[index];
    const colorOffset = clamp(rawColorOffset, -maxColorPulseOffset, maxColorPulseOffset);
    waveform[index] = fluxFromMagnitudeOffset(brightnessMagnitudeOffset);
    colorOffsets[index] = colorOffset;
    colors[index] = Number.isFinite(meanVMinusI0)
      ? colorForVMinusI(meanVMinusI0 + colorOffset, row[IDX.spectral])
      : colorForVMinusI(meanVMinusI0, row[IDX.spectral]);
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
    ? colorForVMinusI(meanVMinusI0 + meanColorOffset, row[IDX.spectral])
    : colors[0];

  return {
    waveform,
    colorOffsets,
    colors,
    params,
    minFlux,
    maxFlux,
    meanFlux,
    amplitudeSourceFluxes,
    meanColor,
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
    timeDomain: Boolean(miraComponents),
    components: miraComponents,
    vComponents: miraVComponents,
  };
}

function pulsationPeriodDays(point) {
  return Math.max(0.05, Number(point?.row?.[IDX.period] || point?.lightCurve?.params?.period || 1));
}

function renderedPulsationFrequencyHz(point) {
  if (point?.kind !== "catalog" || !point.lightCurve) return 0;
  return state.pulsationSpeed / (pulsationPeriodDays(point) * SECONDS_PER_DAY);
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
  const colorOffset = clamp(rawColorOffset, -maxColorPulseOffset, maxColorPulseOffset);
  const pulse = fluxFromMagnitudeOffset(brightnessMagnitudeOffset);
  const meanVMinusI0 = point?.vMinusI0;
  const color = Number.isFinite(meanVMinusI0)
    ? colorForVMinusI(meanVMinusI0 + colorOffset, point.row?.[IDX.spectral])
    : point?.lightCurve?.meanColor || point?.color || "#ffffff";
  return {
    pulse,
    color,
    colorOffset,
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
  return {
    pulse,
    areaPulse: visualPulses.areaPulse,
    opacityPulse: visualPulses.opacityPulse,
    color: point?.lightCurve?.meanColor || point?.color || "#ffffff",
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

  activeLightcurveInset = {
    target,
    trace,
    phaseMarkers,
    phaseDots,
    width,
    height,
    padX,
    padY,
  };
  updateLightcurveInset();
  return inset;
}

function updateLightcurveInset() {
  if (!activeLightcurveInset) return;

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
    return;
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

function createClusterHrDiagram(target) {
  const stars = clusterHrStarsForTarget(target);
  const hrBins = target.hrBins || [];
  let colorMin = Infinity;
  let colorMax = -Infinity;
  let logLumMin = Infinity;
  let logLumMax = -Infinity;

  for (const star of stars) {
    const color = star.row[CS.vMinusI0];
    const logLum = star.row[CS.logLum];
    if (!Number.isFinite(color) || !Number.isFinite(logLum)) continue;
    colorMin = Math.min(colorMin, color);
    colorMax = Math.max(colorMax, color);
    logLumMin = Math.min(logLumMin, logLum);
    logLumMax = Math.max(logLumMax, logLum);
  }
  for (const bin of hrBins) {
    if (!Number.isFinite(bin.vMinusI0) || !Number.isFinite(bin.logLum)) continue;
    colorMin = Math.min(colorMin, bin.vMinusI0);
    colorMax = Math.max(colorMax, bin.vMinusI0);
    logLumMin = Math.min(logLumMin, bin.logLum);
    logLumMax = Math.max(logLumMax, bin.logLum);
  }

  if (!Number.isFinite(colorMin) || !Number.isFinite(logLumMin)) return null;

  const width = 278;
  const height = 184;
  const padLeft = 34;
  const padRight = 10;
  const padTop = 12;
  const padBottom = 28;
  const plotWidth = width - padLeft - padRight;
  const plotHeight = height - padTop - padBottom;
  const [xMin, xMax] = clusterHrExpandedRange(colorMin, colorMax, 0.9, -0.6, 3.25);
  const [yMin, yMax] = clusterHrExpandedRange(logLumMin, logLumMax, 1.6, -2.1, 6.2);
  const xForColor = (color) => padLeft + ((color - xMin) / (xMax - xMin)) * plotWidth;
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
    const x = xForColor(tick);
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
    label.textContent = clusterHrTickLabel(tick);
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
  xLabel.textContent = "V-I0";

  const yLabel = createSvgElement("text");
  yLabel.classList.add("clusterHrLabel");
  yLabel.setAttribute("x", "9");
  yLabel.setAttribute("y", String(padTop + plotHeight / 2));
  yLabel.setAttribute("text-anchor", "middle");
  yLabel.setAttribute("transform", `rotate(-90 9 ${padTop + plotHeight / 2})`);
  yLabel.textContent = "log L";
  axisGroup.append(xLabel, yLabel);

  const binGroup = createSvgElement("g");
  const maxBinCount = Math.max(1, ...hrBins.map((bin) => bin.count || 0));
  for (const bin of hrBins) {
    if (!Number.isFinite(bin.vMinusI0) || !Number.isFinite(bin.logLum)) continue;
    const x = xForColor(bin.vMinusI0);
    const y = yForLogLum(bin.logLum);
    const countLevel = Math.log1p(bin.count || 1) / Math.log1p(maxBinCount);
    const circle = createSvgElement("circle");
    circle.classList.add("clusterHrBin");
    circle.setAttribute("cx", x.toFixed(2));
    circle.setAttribute("cy", y.toFixed(2));
    circle.setAttribute("r", (1.2 + countLevel * 5.3).toFixed(2));
    circle.style.fill = bin.color;
    circle.style.opacity = String(0.16 + countLevel * 0.36);
    binGroup.append(circle);
  }

  const starGroup = createSvgElement("g");
  const displayStars = sampledClusterHrStars(stars);
  const starOpacity = displayStars.length > 900 ? 0.62 : 0.78;
  for (const star of displayStars) {
    const color = star.row[CS.vMinusI0];
    const logLum = star.row[CS.logLum];
    if (!Number.isFinite(color) || !Number.isFinite(logLum)) continue;
    const lumLevel = clamp((logLum - yMin) / (yMax - yMin), 0, 1);
    const circle = createSvgElement("circle");
    circle.classList.add("clusterHrStar");
    circle.setAttribute("cx", xForColor(color).toFixed(2));
    circle.setAttribute("cy", yForLogLum(logLum).toFixed(2));
    circle.setAttribute("r", (0.85 + lumLevel * 1.8).toFixed(2));
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

function starRadiusZoomSize() {
  const zoomSize = 0.8 + Math.log2(Math.max(1, effectiveZoomScale())) * STAR_RADIUS_ZOOM_BASE_GAIN;
  const boost = 1 + Math.min(STAR_RADIUS_ZOOM_MAX_BOOST, Math.log2(Math.max(1, state.zoom)) * STAR_RADIUS_ZOOM_GAIN);
  return Math.min(zoomSize * boost, STAR_RADIUS_ZOOM_SIZE_MAX);
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

function createRedClumpProgram(gl) {
  const vertexShader = compileCatalogShader(
    gl,
    gl.VERTEX_SHADER,
    `
      attribute vec2 a_position;
      attribute vec4 a_color;

      uniform vec2 u_resolution;

      varying vec4 v_color;

      void main() {
        vec2 clip = (a_position / u_resolution) * 2.0 - 1.0;
        gl_Position = vec4(clip.x, -clip.y, 0.0, 1.0);
        v_color = a_color;
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

  const catalogDynamicBuffer = gl.createBuffer();
  const catalogStaticBuffer = gl.createBuffer();
  const catalogStride = CATALOG_GPU_VERTEX_FLOATS * Float32Array.BYTES_PER_ELEMENT;
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

  gl.disable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);

  canvasElement.addEventListener("webglcontextlost", (event) => {
    event.preventDefault();
    scene.catalogStaticRenderer = null;
    scene.catalogRenderer = null;
    markCatalogStaticDirty();
  });

  return {
    mode: "gpu",
    gl,
    canvas: canvasElement,
    catalogProgram,
    catalogDynamicBuffer,
    catalogStaticBuffer,
    catalogAttributes,
    catalogUniforms,
    catalogDynamicCapacity: 0,
    catalogDynamicData: new Float32Array(0),
    catalogStaticCapacity: 0,
    catalogStaticData: new Float32Array(0),
    catalogStaticCount: 0,
    ensureCatalogCapacity(count) {
      if (this.catalogDynamicCapacity >= count) return this.catalogDynamicData;
      this.catalogDynamicCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, count)));
      this.catalogDynamicData = new Float32Array(this.catalogDynamicCapacity * CATALOG_GPU_VERTEX_FLOATS);
      return this.catalogDynamicData;
    },
    ensureCatalogStaticCapacity(count) {
      if (this.catalogStaticCapacity >= count) return this.catalogStaticData;
      this.catalogStaticCapacity = 2 ** Math.ceil(Math.log2(Math.max(1, count)));
      this.catalogStaticData = new Float32Array(this.catalogStaticCapacity * CATALOG_GPU_VERTEX_FLOATS);
      return this.catalogStaticData;
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
    bindCatalogAttributes(buffer = this.catalogDynamicBuffer) {
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
    drawCatalogStatic() {
      this.drawCatalogBuffer(this.catalogStaticBuffer, this.catalogStaticCount);
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
    color: gl.getAttribLocation(redClumpProgram, "a_color"),
  };
  const redClumpUniforms = {
    resolution: gl.getUniformLocation(redClumpProgram, "u_resolution"),
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
    redClumpExposure: null,
    redClumpSourceCount: -1,
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
      this.gl.vertexAttribPointer(this.redClumpAttributes.position, 2, this.gl.FLOAT, false, redClumpStride, 0);
      this.gl.enableVertexAttribArray(this.redClumpAttributes.color);
      this.gl.vertexAttribPointer(
        this.redClumpAttributes.color,
        4,
        this.gl.FLOAT,
        false,
        redClumpStride,
        2 * Float32Array.BYTES_PER_ELEMENT,
      );
    },
    updateRedClumpBuffer(items, rgbValue) {
      const maxIndexedVertexCount = uintIndexExtension ? Infinity : 65535;
      const canUseIndexedDraw = items.length * 4 <= maxIndexedVertexCount;
      const alphaSignature = redClumpAlphaCacheSignature();
      const data = this.ensureRedClumpCapacity(items.length * (canUseIndexedDraw ? 4 : 6));
      const indexData = canUseIndexedDraw ? this.ensureRedClumpIndexCapacity(items.length * 6) : null;
      const triangleIndexes = [0, 1, 2, 0, 2, 3];
      let offset = 0;
      let vertexCount = 0;
      let indexCount = 0;
      for (const item of items) {
        if (updateRedClumpSurfaceAlphaCache(item, false, alphaSignature) <= 0.001) continue;

        if (canUseIndexedDraw) {
          const baseIndex = vertexCount;
          for (let pointIndex = 0; pointIndex < 4; pointIndex += 1) {
            const point = item.projected[pointIndex];
            const alpha = item.surfaceVertexAlphas[pointIndex];
            data[offset] = point.x;
            data[offset + 1] = point.y;
            data[offset + 2] = rgbValue[0] * alpha;
            data[offset + 3] = rgbValue[1] * alpha;
            data[offset + 4] = rgbValue[2] * alpha;
            data[offset + 5] = alpha;
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
            const point = item.projected[pointIndex];
            const alpha = item.surfaceVertexAlphas[pointIndex];
            data[offset] = point.x;
            data[offset + 1] = point.y;
            data[offset + 2] = rgbValue[0] * alpha;
            data[offset + 3] = rgbValue[1] * alpha;
            data[offset + 4] = rgbValue[2] * alpha;
            data[offset + 5] = alpha;
            offset += RED_CLUMP_GPU_VERTEX_FLOATS;
            vertexCount += 1;
          }
        }
      }

      this.redClumpCount = vertexCount;
      this.redClumpIndexCount = indexCount;
      this.redClumpUsesIndexedDraw = canUseIndexedDraw;
      this.redClumpExposure = redClumpRenderExposureValue();
      this.redClumpSourceCount = items.length;
      this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.redClumpBuffer);
      this.gl.bufferData(this.gl.ARRAY_BUFFER, data.subarray(0, offset), this.gl.DYNAMIC_DRAW);
      if (canUseIndexedDraw) {
        this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, this.redClumpIndexBuffer);
        this.gl.bufferData(this.gl.ELEMENT_ARRAY_BUFFER, indexData.subarray(0, indexCount), this.gl.DYNAMIC_DRAW);
      }
      scene.redClumpGpuDirty = false;
    },
    drawRedClump(items, rgbValue) {
      this.resize();
      if (
        scene.redClumpGpuDirty ||
        this.redClumpExposure !== redClumpRenderExposureValue() ||
        this.redClumpSourceCount !== items.length
      ) {
        this.updateRedClumpBuffer(items, rgbValue);
      }
      if (this.redClumpCount <= 0) return;

      this.gl.useProgram(this.redClumpProgram);
      this.bindRedClumpAttributes();
      this.gl.uniform2f(this.redClumpUniforms.resolution, scene.width, scene.height);
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

function getBaseSceneLayout() {
  const centerOffsetX = scene.width > 860 ? DESKTOP_SCENE_CENTER_OFFSET_X : 0;
  const availableWidth = Math.max(320, scene.width - Math.abs(centerOffsetX) * 2);
  return {
    centerX: scene.width / 2 + centerOffsetX,
    centerY: scene.height * (scene.width > 860 ? 0.53 : 0.42),
    scale: (Math.min(availableWidth, scene.height) / 64) * effectiveZoomScale(),
  };
}

function updateSceneLayout() {
  const base = getBaseSceneLayout();
  scene.scale = base.scale;
  const panScale = Math.max(1, effectiveZoomScale());
  const maxPanX = scene.width * 2.5 * panScale;
  const maxPanY = scene.height * 2.5 * panScale;

  if (state.cameraLocked && state.locked) {
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
  setZoom(state.zoom * zoomGain);
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

function setZoom(nextZoom, focusX = scene.centerX, focusY = scene.centerY) {
  markOrientationGridActive();
  const oldScale = scene.scale || 1;
  const oldCenterX = scene.centerX;
  const oldCenterY = scene.centerY;
  state.zoom = clampZoomScale(nextZoom);
  updateSceneLayout();

  const ratio = scene.scale / oldScale;
  const targetCenterX = focusX - (focusX - oldCenterX) * ratio;
  const targetCenterY = focusY - (focusY - oldCenterY) * ratio;
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
    catalogDrawList.push(item);
    catalogStats.count += 1;
    catalogStats.minDepth = Math.min(catalogStats.minDepth, z2);
    catalogStats.maxDepth = Math.max(catalogStats.maxDepth, z2);
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

function rebuildActivePointLists() {
  if (!scene.activePointsDirty) return;

  scene.activeCatalog.length = 0;
  scene.activeRedClump.length = 0;
  scene.activeClusterStars.length = 0;
  scene.activeClusters.length = 0;

  for (const point of scene.catalog) {
    if (isCatalogVisible(point)) scene.activeCatalog.push(point);
  }

  for (const point of scene.clusterStars) {
    if (isClusterStarVisible(point)) scene.activeClusterStars.push(point);
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
  if (state.cameraLocked && state.locked) {
    updateSceneLayout();
  }
  updateCoordinateReadout();
  projectionDirty = true;
  queueRender();
}

function rebuildProjectionCache() {
  const projectionStartMs = PERF_HUD_ENABLED ? performance.now() : 0;
  const redStats = resetStats(scene.cachedStats.redClump);
  const catalogStats = resetStats(scene.cachedStats.catalog);
  const redClumpDrawList = scene.redClumpDrawList;
  const redClumpSurfaceDrawList = scene.redClumpSurfaceDrawList;
  const catalogDrawList = scene.catalogDrawList;
  const clusterTargetDrawList = scene.clusterTargetDrawList;
  const projectionTransform = makeProjectionTransform();
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
  clusterTargetDrawList.length = 0;
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

  const catalogViewportMargin = Math.max(28, effectiveZoomScale() * 0.35);
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

  for (const point of scene.activeClusters) {
    const coordinates = point.activeCoordinates || coordinatesForPoint(point);
    const projected = project(point.projected, coordinates[0], coordinates[1], coordinates[2]);
    point.activeProjected = projected;
    const item = point.drawItem;
    const physicalRadius = (point.radiusPc / 1000) * scene.scale * projected.perspective;
    item.screenRadius = clamp(physicalRadius, 8, 260);
    item.glowAlphaUnit = pointAlphaUnitFromBaseAtPerspective(point.glowAlphaBaseUnit, projected.perspective);
    if (!withinViewport(projected, item.screenRadius + 24)) continue;
    clusterTargetDrawList.push(item);
  }

  markRedClumpLayerDirty();
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
    const outer = clamp(bin.outerRadius, previousOuter + 0.001, 1);
    const nextLuminosity = cumulativeLuminosity + bin.luminosity;
    if (nextLuminosity >= targetLuminosity) {
      const fraction = clamp((targetLuminosity - cumulativeLuminosity) / Math.max(bin.luminosity, 0.0001), 0, 1);
      const radiusSquared = previousOuter * previousOuter + fraction * (outer * outer - previousOuter * previousOuter);
      return clamp(Math.sqrt(Math.max(0, radiusSquared)), 0.08, 0.95);
    }
    cumulativeLuminosity = nextLuminosity;
    previousOuter = outer;
  }

  return 0.95;
}

function drawClusterGlows() {
  if (!state.datasets.clusters || scene.clusterTargetDrawList.length === 0) return;

  ctx.save();
  ctx.globalCompositeOperation = "source-over";

  for (const item of scene.clusterTargetDrawList) {
    const row = item.point.row;
    const luminosity = row[CL.unresolvedLum];
    if (!Number.isFinite(luminosity) || luminosity <= 0) continue;
    const bins = item.point.glowBins;
    if (!bins || bins.length === 0) continue;

    const alpha = Math.min(
      CLUSTER_GLOW_ALPHA_MAX,
      pointAlphaFromUnit(item.glowAlphaUnit, datasetExposureValue("clusters")) * CLUSTER_GLOW_ALPHA_SCALE,
    );
    if (alpha <= 0.001) continue;

    const profileRadius = Math.max(7, item.screenRadius * CLUSTER_GLOW_RADIUS_SCALE);
    const radius = profileRadius * (1 + CLUSTER_GLOW_EDGE_FEATHER);
    const halfLightFraction = clusterGlowHalfLightFraction(bins);
    const scaleRadius = Math.max(0.08, halfLightFraction) * profileRadius;
    const glowColor = cssColorToRgb(colorForVMinusI(row[CL.unresolvedVMinusI0], 4));
    const gradient = ctx.createRadialGradient(
      item.projected.x,
      item.projected.y,
      0,
      item.projected.x,
      item.projected.y,
      radius,
    );

    for (let index = 0; index <= CLUSTER_GLOW_PROFILE_STOPS; index += 1) {
      const stop = index / CLUSTER_GLOW_PROFILE_STOPS;
      const projectedRadius = stop * radius;
      const plummerSurface = 1 / (1 + (projectedRadius / scaleRadius) ** 2) ** 2;
      const edgeUnit = projectedRadius <= profileRadius ? 0 : (projectedRadius - profileRadius) / (radius - profileRadius);
      const edgeFade = 1 - smoothStep(edgeUnit);
      gradient.addColorStop(stop, rgbaFromRgb(glowColor, alpha * plummerSurface * edgeFade));
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

  renderer.drawRedClump(scene.redClumpSurfaceDrawList, normalizedRgbFromCssColor(scene.spectralClasses[4].color));
  return true;
}

function redClumpStaticSignature() {
  return [
    scene.width,
    scene.height,
    scene.dpr,
    scene.redClumpSurfaceDrawList.length,
    redClumpRenderExposureValue().toFixed(6),
  ].join("|");
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

  renderer.drawRedClump(scene.redClumpSurfaceDrawList, normalizedRgbFromCssColor(scene.spectralClasses[4].color));
  return true;
}

function rebuildRedClumpStaticLayer() {
  resizeRedClumpStaticCanvas();
  clearRedClumpStaticCanvas();

  const signature = redClumpStaticSignature();
  if (!state.datasets.redclump || scene.redClumpSurfaceDrawList.length === 0) {
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

function drawRedClumpStaticLayer() {
  if (scene.redClumpStaticCanvas === redClumpCanvas) return;
  if (scene.redClumpStaticCanvas.width <= 0 || scene.redClumpStaticCanvas.height <= 0) return;
  ctx.drawImage(scene.redClumpStaticCanvas, 0, 0, scene.width, scene.height);
}

function drawRedClump(forceDirect = false) {
  const redClumpStartMs = PERF_HUD_ENABLED ? performance.now() : 0;
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
    drawRedClumpStaticLayer();
  }

  if (PERF_HUD_ENABLED) {
    updatePerfHud({ redClumpMs: performance.now() - redClumpStartMs });
  }
  return scene.cachedStats.redClump;
}

function starRadiusFactorForPoint(point) {
  return point.kind === "catalog" ? PULSATOR_BASE_RADIUS_FACTOR : 1;
}

function starRadiusFromBase(baseRadius, areaPulse = 1, radiusFactor = 1) {
  return clamp(
    baseRadius *
      PULSATOR_RADIUS_BASE_SCALE *
      state.radiusScale *
      radiusFactor *
      Math.sqrt(Math.max(0.000001, areaPulse)),
    0.18,
    28,
  );
}

function starRadius(point, projected, areaPulse = 1) {
  return starRadiusFromBase(
    starRadiusFromUnitAtPerspective(point.radiusUnit, projected.perspective),
    areaPulse,
    starRadiusFactorForPoint(point),
  );
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

function starAlphaFromUnit(alphaUnit, opacityPulse, lightCurve = null, point = null, exposureGain = datasetExposureForPoint(point)) {
  const pulseSafeAlpha = pulseSafeAlphaForPoint(point, lightCurve);
  const exposure = (exposureGain / 10) * DISPLAY_LUMINOSITY_BASE_BOOST * alphaUnit;
  const baseAlphaWithPulseHeadroom = pulseSafeAlpha * (1 - Math.exp(-exposure / STAR_ALPHA_HEADROOM_EXPOSURE));
  return clamp(baseAlphaWithPulseHeadroom * opacityPulse, 0.0005, STAR_PULSE_ALPHA_MAX);
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

function updateCatalogStaticStyle(item) {
  const radiusFactor = starRadiusFactorForPoint(item.point);
  if (
    item.staticBaseRadius !== item.baseRadius ||
    item.staticAlphaUnit !== item.alphaUnit ||
    item.staticRadiusFactor !== radiusFactor ||
    item.staticRadiusScale !== state.radiusScale ||
    item.staticExposure !== datasetExposureForPoint(item.point)
  ) {
    item.staticBaseRadius = item.baseRadius;
    item.staticAlphaUnit = item.alphaUnit;
    item.staticRadiusFactor = radiusFactor;
    item.staticRadiusScale = state.radiusScale;
    item.staticExposure = datasetExposureForPoint(item.point);
    item.staticRadius = starRadiusFromBase(item.baseRadius, 1, radiusFactor);
    item.staticAlpha = starAlphaFromUnit(item.alphaUnit, 1, item.point.lightCurve, item.point, item.staticExposure);
  }
}

function shouldAnimateCatalogItem(item, baseRadius, baseAlpha) {
  if (item.point.kind === "clusterStar") return false;
  if (pulsationTooFastForAnimation(item.point)) {
    item.point.animatePulse = false;
    return false;
  }

  if (CATALOG_PULSE_ALL_STARS || !PULSE_LOD_ENABLED) {
    item.point.animatePulse = true;
    return true;
  }

  if (item.point === state.locked || item.point === state.hovered) return true;

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

function updateAnimatedCatalogItem(item, simulationDay) {
  const pulseSample = pulseState(item.point, simulationDay);
  item.currentPulse = pulseSample.pulse;
  item.currentAlpha = starAlphaFromUnit(
    item.alphaUnit,
    pulseSample.opacityPulse,
    item.point.lightCurve,
    item.point,
    item.staticExposure,
  );
  item.currentRadius = starRadiusFromBase(
    item.baseRadius,
    pulseSample.areaPulse,
    starRadiusFactorForPoint(item.point),
  );
  return pulseSample.color;
}

function updateStaticCatalogItem(item) {
  if (pulsationTooFastForAnimation(item.point)) {
    const pulseSample = meanPulseState(item.point);
    item.currentPulse = pulseSample.pulse;
    item.currentAlpha = starAlphaFromUnit(
      item.alphaUnit,
      pulseSample.opacityPulse,
      item.point.lightCurve,
      item.point,
      item.staticExposure,
    );
    item.currentRadius = starRadiusFromBase(
      item.baseRadius,
      pulseSample.areaPulse,
      starRadiusFactorForPoint(item.point),
    );
    return pulseSample.color;
  }

  item.currentPulse = 1;
  item.currentAlpha = item.staticAlpha;
  item.currentRadius = item.staticRadius;
  return item.point.color;
}

function writeCatalogGpuItem(data, offset, item, color) {
  const rgbValue = normalizedRgbFromCssColor(color);
  data[offset] = item.projected.x;
  data[offset + 1] = item.projected.y;
  data[offset + 2] = item.currentRadius;
  data[offset + 3] = rgbValue[0];
  data[offset + 4] = rgbValue[1];
  data[offset + 5] = rgbValue[2];
  data[offset + 6] = item.currentAlpha;
  data[offset + 7] = shouldUseLimbDarkening(item) ? 1 : 0;
  return offset + CATALOG_GPU_VERTEX_FLOATS;
}

function catalogStaticCacheMatches() {
  return (
    !scene.catalogStaticDirty &&
    scene.catalogStaticRadiusScale === state.radiusScale &&
    scene.catalogStaticExposureSignature === catalogExposureSignature() &&
    scene.catalogStaticPulsationSpeed === state.pulsationSpeed
  );
}

function stampCatalogStaticCache(animatedCatalog, staticCatalog) {
  scene.catalogStaticCounts.animated = animatedCatalog;
  scene.catalogStaticCounts.static = staticCatalog;
  scene.catalogStaticRadiusScale = state.radiusScale;
  scene.catalogStaticExposureSignature = catalogExposureSignature();
  scene.catalogStaticPulsationSpeed = state.pulsationSpeed;
  scene.catalogStaticDirty = false;
}

function drawAnimatedCatalogItems(items, simulationDay) {
  const colorBuckets = scene.colorBuckets;
  clearColorBuckets(colorBuckets);

  for (const item of items) {
    pushColorBucket(colorBuckets, updateAnimatedCatalogItem(item, simulationDay), item);
  }

  drawCatalogBuckets(ctx, colorBuckets);
}

function rebuildCatalogGpuStaticLayer(renderer) {
  const data = renderer.ensureCatalogStaticCapacity(scene.catalogDrawList.length);
  scene.catalogAnimatedDrawList.length = 0;

  let offset = 0;
  let staticCount = 0;
  let animatedCatalog = 0;
  let staticCatalog = 0;

  for (const item of scene.catalogDrawList) {
    updateCatalogStaticStyle(item);
    const animates = shouldAnimateCatalogItem(item, item.staticRadius, item.staticAlpha);
    if (animates) {
      scene.catalogAnimatedDrawList.push(item);
      animatedCatalog += 1;
    } else {
      offset = writeCatalogGpuItem(data, offset, item, updateStaticCatalogItem(item));
      staticCount += 1;
      staticCatalog += 1;
    }
  }

  renderer.resize();
  renderer.clear();
  renderer.uploadCatalogStatic(staticCount);
  renderer.drawCatalogStatic();
  stampCatalogStaticCache(animatedCatalog, staticCatalog);
}

function rebuildCatalogStaticLayer() {
  resizeCatalogStaticCanvas();
  clearCatalogStaticCanvas();
  clearColorBuckets(scene.staticColorBuckets);
  scene.catalogAnimatedDrawList.length = 0;

  let animatedCatalog = 0;
  let staticCatalog = 0;

  for (const item of scene.catalogDrawList) {
    updateCatalogStaticStyle(item);
    const animates = shouldAnimateCatalogItem(item, item.staticRadius, item.staticAlpha);
    if (animates) {
      scene.catalogAnimatedDrawList.push(item);
      animatedCatalog += 1;
    } else {
      pushColorBucket(scene.staticColorBuckets, updateStaticCatalogItem(item), item);
      staticCatalog += 1;
    }
  }

  drawCatalogBuckets(scene.catalogStaticCtx, scene.staticColorBuckets);
  stampCatalogStaticCache(animatedCatalog, staticCatalog);
}

function drawCatalogDirect(simulationDay) {
  const colorBuckets = scene.colorBuckets;
  clearColorBuckets(colorBuckets);
  let animatedCatalog = 0;
  let staticCatalog = 0;

  for (const item of scene.catalogDrawList) {
    updateCatalogStaticStyle(item);
    const animates = shouldAnimateCatalogItem(item, item.staticRadius, item.staticAlpha);
    let color = item.point.color;
    if (animates) {
      color = updateAnimatedCatalogItem(item, simulationDay);
      animatedCatalog += 1;
    } else {
      color = updateStaticCatalogItem(item);
      staticCatalog += 1;
    }
    pushColorBucket(colorBuckets, color, item);
  }

  drawCatalogBuckets(ctx, colorBuckets);
  return { animatedCatalog, staticCatalog };
}

function drawCatalogGpu(simulationDay) {
  const renderer = prepareGpuSceneLayer();
  if (!renderer) return null;
  const staticRenderer = scene.catalogStaticRenderer;
  if (!staticRenderer) return null;

  if (!catalogStaticCacheMatches()) {
    rebuildCatalogGpuStaticLayer(staticRenderer);
  }

  const data = renderer.ensureCatalogCapacity(scene.catalogAnimatedDrawList.length);
  let offset = 0;
  let count = 0;

  for (const item of scene.catalogAnimatedDrawList) {
    offset = writeCatalogGpuItem(data, offset, item, updateAnimatedCatalogItem(item, simulationDay));
    count += 1;
  }

  renderer.drawCatalogDynamic(count);
  return {
    animatedCatalog: scene.catalogStaticCounts.animated,
    staticCatalog: scene.catalogStaticCounts.static,
  };
}

function drawCatalog(useStaticCache = true) {
  const catalogStartMs = PERF_HUD_ENABLED ? performance.now() : 0;
  const simulationDay = currentSimulationDay();
  let animatedCatalog = 0;
  let staticCatalog = 0;

  const gpuResult = drawCatalogGpu(simulationDay);
  if (gpuResult) {
    ({ animatedCatalog, staticCatalog } = gpuResult);
  } else if (useStaticCache && PULSE_LOD_ENABLED && catalogStaticCacheMatches()) {
    if (scene.catalogStaticDirty) rebuildCatalogStaticLayer();
    ctx.drawImage(scene.catalogStaticCanvas, 0, 0, scene.width, scene.height);
    animatedCatalog = scene.catalogStaticCounts.animated;
    staticCatalog = scene.catalogStaticCounts.static;
    drawAnimatedCatalogItems(scene.catalogAnimatedDrawList, simulationDay);
  } else if (useStaticCache && PULSE_LOD_ENABLED) {
    rebuildCatalogStaticLayer();
    ctx.drawImage(scene.catalogStaticCanvas, 0, 0, scene.width, scene.height);
    animatedCatalog = scene.catalogStaticCounts.animated;
    staticCatalog = scene.catalogStaticCounts.static;
    drawAnimatedCatalogItems(scene.catalogAnimatedDrawList, simulationDay);
  } else {
    ({ animatedCatalog, staticCatalog } = drawCatalogDirect(simulationDay));
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

function drawSelection(target) {
  if (!target) return;
  const coordinates = coordinatesForPoint(target);
  const projected = projectPoint(coordinates[0], coordinates[1], coordinates[2]);
  if (!withinViewport(projected, 60)) return;

  const radius =
    target.kind === "catalog"
      ? starRadius(target, projected, 1) + 7
      : target.kind === "cluster"
        ? Math.max(10, target.drawItem?.screenRadius || 10)
        : 8;
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

  const rebuiltProjection = projectionDirty;
  if (projectionDirty) rebuildProjectionCache();
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
  state.zoom = clampZoomScale(state.zoom);
  state.radiusScale = clampRadiusScale(state.radiusScale);
  state.pulsationSpeed = clampPulsationSpeed(state.pulsationSpeed);
  state.pulsationSpeedLog = Math.log10(state.pulsationSpeed);
  state.pulsationAmplitudeScale = clampPulsationAmplitudeScale(state.pulsationAmplitudeScale);
  syncEditableMultiplierOutput("yaw", radiansToDegrees(state.yaw));
  syncEditableMultiplierOutput("pitch", radiansToDegrees(state.pitch));
  syncEditableMultiplierOutput("roll", radiansToDegrees(state.roll));
  syncEditableMultiplierOutput("zoom", state.zoom);
  syncEditableMultiplierOutput("radiusScale", state.radiusScale);
  syncEditableMultiplierOutput("pulsationSpeed", state.pulsationSpeed);
  syncEditableMultiplierOutput("pulsationAmplitude", state.pulsationAmplitudeScale);
  outputs.pulsationDaySeconds.textContent = `1 d = ${formatPulsationDuration(
    SECONDS_PER_DAY / state.pulsationSpeed,
  )}`;

  controls.yaw.value = String(radiansToDegrees(state.yaw));
  controls.pitch.value = String(radiansToDegrees(state.pitch));
  controls.roll.value = String(radiansToDegrees(state.roll));
  controls.zoom.value = String(Math.log10(state.zoom));
  controls.radiusScale.value = String(Math.log10(state.radiusScale));
  controls.pulsationSpeed.value = String(state.pulsationSpeedLog);
  controls.pulsationAmplitude.value = String(Math.log10(state.pulsationAmplitudeScale));
  [
    controls.yaw,
    controls.pitch,
    controls.roll,
    controls.zoom,
    controls.radiusScale,
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

function datasetExposureValue(datasetKey) {
  return clampDatasetExposure(state.datasetExposure[datasetKey] ?? DATASET_EXPOSURE_DEFAULT);
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
  state.locked = null;
  state.hovered = null;
  state.cameraLocked = false;
  activeLightcurveInset = null;
  applyCoordinateChange();
}

function clearCoordinateCenterSelection() {
  if (state.centerSelection === null) return;
  state.centerSelection = null;
  syncCoordinateFrameControls();
}

function clearCenterSelectionForTarget(target) {
  if (state.cameraLocked && (target?.kind === "catalog" || target?.kind === "cluster")) {
    state.customCoordinateContext = centerContext(target.coordinates.galacticVector);
    clearCoordinateCenterSelection();
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
      state.datasetExposure[datasetKey] = DATASET_EXPOSURE_DEFAULT;
    });
    state.radiusScale = defaultRadiusScaleForPreset(preset);
    state.pulsationAmplitudeScale = defaultPulsationAmplitudeScaleForPreset(preset);
    state.pulsationSpeed = defaultPulsationSpeedForPreset(preset);
    state.pulsationSpeedLog = Math.log10(state.pulsationSpeed);
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
  state.pulsationSpeed = defaultPulsationSpeedForPreset(preset);
  state.pulsationSpeedLog = Math.log10(state.pulsationSpeed);

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
  state.pulsationSpeed = defaultPulsationSpeedForPreset(PULSATOR_DEFAULT_PRESET);
  state.pulsationSpeedLog = Math.log10(state.pulsationSpeed);

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
  state.pulsationSpeed = snapshot.pulsationSpeed;
  state.pulsationSpeedLog = snapshot.pulsationSpeedLog;
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
  const moved = Math.hypot(dx, dy) > MOBILE_TOUCH_MOVE_THRESHOLD || distanceDelta > MOBILE_PINCH_MOVE_THRESHOLD;

  if (moved) {
    touchGesture.moved = true;
    cancelIntroRotation();
    cancelAxisSpinAnimation();
    markOrientationGridActive();
    if (state.locked || state.cameraLocked) clearTargetSelection();

    const nextZoom = clampZoomScale(touchGesture.zoom * (metrics.distance / Math.max(1, touchGesture.distance)));
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

function handleCanvasTouchPointerDown(event) {
  if (!isMobileTouchPointer(event)) return false;
  event.preventDefault();
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
    selectTargetAt(point.clientX, point.clientY, {
      pickRadiusScale: MOBILE_TARGET_PICK_RADIUS_SCALE,
      focusSelectedOnRepeat: true,
    });
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
  return ["INPUT", "SELECT", "TEXTAREA"].includes(target.tagName);
}

function viewportKeyboardMultiplier(event) {
  return event.shiftKey ? VIEWPORT_KEY_FAST_MULTIPLIER : 1;
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
  state.pulsationSpeed = INITIAL_PULSATION_SPEED;
  state.pulsationSpeedLog = Math.log10(INITIAL_PULSATION_SPEED);
  state.pulsationAmplitudeScale = defaultPulsationAmplitudeScaleForPreset(PULSATOR_DEFAULT_PRESET);
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
  activeLightcurveInset = null;

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
  const multiplier = viewportKeyboardMultiplier(event);
  const panStep = VIEWPORT_PAN_STEP_PX * multiplier;
  const pageStep = VIEWPORT_PAGE_STEP_PX * multiplier;
  const yawStep = VIEWPORT_YAW_STEP_DEGREES * multiplier;
  let handled = true;

  switch (key) {
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
    "perren",
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

function selectCatalogSearchTarget(target) {
  if (!targetIsPickable(target)) return;
  state.locked = target;
  state.hovered = null;
  state.cameraLocked = false;
  setTarget(state.locked);
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

function handleTargetSearchInput() {
  state.targetSearchQuery = controls.targetSearch.value;
  const { matches, total, exactMatch } = catalogSearchMatches();
  const autoTarget = exactMatch || (total === 1 ? matches[0] : null);
  if (autoTarget) {
    selectCatalogSearchTarget(autoTarget);
    return;
  }

  if (state.locked || state.hovered || state.cameraLocked) {
    state.locked = null;
    state.hovered = null;
    state.cameraLocked = false;
    activeLightcurveInset = null;
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
  state.locked = null;
  state.hovered = null;
  state.cameraLocked = false;
  setTarget(null);
}

function setCameraLock(enabled, target = state.locked) {
  markOrientationGridActive();
  if (enabled && target) {
    state.locked = target;
    state.hovered = null;
    state.cameraLocked = true;
    clearCenterSelectionForTarget(target);
  } else {
    state.cameraLocked = false;
  }

  updateSceneLayout();
  setTarget(state.locked || state.hovered);
  markProjectionDirty();
}

function setTarget(target) {
  const current = target || state.locked || state.hovered;
  activeLightcurveInset = null;
  markCatalogStaticDirty();
  elements.target.classList.remove("hasMatches");
  elements.target.replaceChildren();

  if (!current) {
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
  if (current.kind === "cluster") {
    const hrDiagram = createClusterHrDiagram(current);
    if (hrDiagram) elements.target.append(hrDiagram);
  }
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
  const distanceLabel =
    distanceError !== null
      ? `${formatNumber(row[IDX.distance], 2)} +/- ${formatNumber(distanceError, 2)} kpc`
      : `${formatNumber(row[IDX.distance], 2)} kpc`;
  const details = [
    ["Type", `${dataset}, ${location}, ${spec}`],
    ["Period", formatPeriodDays(row)],
    ["Lum", `${formatNumber(row[IDX.lum], 0)} Lsun`],
    ["Radius", `${formatNumber(row[IDX.radius], 1)} Rsun`],
    ["vs RC", `${formatNumber(row[IDX.lum] / RED_CLUMP_LUMINOSITY, 1)}x`],
    ["Dist", distanceLabel],
    ["V-I obs", formatNumber(row[IDX.vMinusI], 3)],
    ["E(V-I)", `${formatNumber(reddeningEVI, 3)} ${reddeningLabel}`],
    ["V-I 0", Number.isFinite(intrinsicVMinusI) ? formatNumber(intrinsicVMinusI, 3) : "n/a"],
    [
      "Teff",
      Number.isFinite(intrinsicVMinusI)
        ? `${formatNumber(effectiveTemperatureFromVMinusI(intrinsicVMinusI), 0)} K`
        : "n/a",
    ],
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
  ];

  const datasetKey = DATASET_KEYS[row[IDX.dataset]];
  if (datasetKey === "cepheids") {
    details.push(["Age", `${formatNumber(row[IDX.age], 0)} Myr`], ["Mode", row[IDX.mode] || "n/a"]);
  } else if (datasetKey === "rrlyrae") {
    details.push(["[Fe/H]", formatNumber(row[IDX.feh], 2)]);
  } else if (datasetKey === "anomalousCepheids") {
    details.push(["Mode", row[IDX.mode] || "n/a"]);
  } else if (datasetKey === "miras") {
    details.push(["Chemistry", row[IDX.mode] || "n/a"]);
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
  const ageMyr = 10 ** (row[CL.logAge] - 6);
  const details = [
    ["Type", `MIST synthetic cluster, ${row[CL.galaxy]}`],
    ["Stars", `${formatInteger(row[CL.renderedStars])} points, ${formatInteger(row[CL.unresolvedStars])} in glow`],
    ["Mass", `${formatInteger(row[CL.mass])} +/- ${formatInteger(row[CL.eMass])} Msun`],
    ["Radius", `${formatNumber(row[CL.radiusPc], 1)} pc`],
    ["[Fe/H]", `${formatNumber(row[CL.feh], 2)} +/- ${formatNumber(row[CL.eFeh], 2)}`],
    ["log age", `${formatNumber(row[CL.logAge], 2)} +/- ${formatNumber(row[CL.eLogAge], 2)}`],
    ["Age", ageMyr >= 1000 ? `${formatNumber(ageMyr / 1000, 2)} Gyr` : `${formatNumber(ageMyr, 0)} Myr`],
    ["E(B-V)", `${formatNumber(row[CL.ebv], 3)} +/- ${formatNumber(row[CL.eEbv], 3)}`],
    ["Dist", `${formatNumber(row[CL.distance], 2)} kpc`],
    ["Isochrones", row[CL.isochroneSummary]],
    [
      "Glow",
      `${formatNumber(row[CL.unresolvedLum], 1)} Lsun in ${formatInteger(target.glowBins?.length || 0)} bins, V-I ${formatNumber(row[CL.unresolvedVMinusI0], 2)}`,
    ],
    ["Segregation", formatNumber(row[CL.segregation], 2)],
    ["Quality", row[CL.qualityFlags] === "none" ? `FC ${row[CL.flagsCount]}` : `${row[CL.qualityFlags]} (FC ${row[CL.flagsCount]})`],
    [`${reference.label} ${frame.label}`, formatCoordinateTriplet(activeCoordinates)],
    ["RA, Dec", `${formatNumber(row[CL.raDeg], 4)}°, ${formatNumber(row[CL.decDeg], 4)}°`],
    ["Gal l,b", `${formatNumber(row[CL.galLonDeg], 4)}°, ${formatNumber(row[CL.galLatDeg], 4)}°`],
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

function buildTargetNavigationCandidates() {
  if (projectionDirty) rebuildProjectionCache();
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

function selectNavigationTarget(target) {
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
  setTarget(target);
  updateCoordinateReadout();
  queueRender();
}

function stepTargetNavigation(direction) {
  const candidates = buildTargetNavigationCandidates();
  if (!candidates.length) return;

  const current = state.locked || state.hovered;
  const currentIndex = current ? candidates.findIndex((candidate) => candidate.target === current) : -1;
  const nextIndex =
    currentIndex >= 0
      ? positiveModulo(currentIndex + direction, candidates.length)
      : nearestTargetNavigationCandidateIndex(candidates);

  selectNavigationTarget(candidates[nextIndex]?.target);
}

function nearestTarget(clientX, clientY, { pickRadiusScale = 1 } = {}) {
  if (projectionDirty) rebuildProjectionCache();

  let best = null;
  const radiusScale = Math.max(1, pickRadiusScale);
  let bestDistance = 144 * radiusScale * radiusScale;
  const simulationDay = currentSimulationDay();

  for (const item of scene.catalogDrawList) {
    if (item.point.kind !== "catalog") continue;
    if (!targetIsPickable(item.point)) continue;
    const areaPulse =
      item.point.animatePulse || item.point === state.locked
        ? lightCurveVisualPulses(pulseFactor(item.point, simulationDay), item.point).areaPulse
        : 1;
    const radius = (starRadiusFromBase(item.baseRadius, areaPulse, starRadiusFactorForPoint(item.point)) + 5) * radiusScale;
    const dx = item.projected.x - clientX;
    const dy = item.projected.y - clientY;
    const distance = dx * dx + dy * dy;
    const threshold = Math.max(bestDistance, radius * radius);
    if (distance < threshold && distance < bestDistance) {
      best = item.point;
      bestDistance = distance;
    }
  }

  if (best) return best;

  let bestClusterScore = Infinity;
  for (const item of scene.clusterTargetDrawList) {
    if (!targetIsPickable(item.point)) continue;
    const dx = item.projected.x - clientX;
    const dy = item.projected.y - clientY;
    const distance = dx * dx + dy * dy;
    const radius = Math.max(10, item.screenRadius) * radiusScale;
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

  for (const item of scene.redClumpDrawList) {
    if (!targetIsPickable(item.point)) continue;
    const dx = item.projected.x - clientX;
    const dy = item.projected.y - clientY;
    const distance = dx * dx + dy * dy;
    if (distance < bestDistance) {
      best = item.point;
      bestDistance = distance;
    }
  }

  return best;
}

function selectTargetAt(clientX, clientY, { pickRadiusScale = 1, focusSelectedOnRepeat = false, lockCamera = false } = {}) {
  const target = nearestTarget(clientX, clientY, { pickRadiusScale });
  if (lockCamera) {
    if (target) setCameraLock(true, target);
    return;
  }

  if (focusSelectedOnRepeat && target && target === state.locked) {
    setCameraLock(true, target);
    return;
  }

  const wasCameraLocked = state.cameraLocked;
  state.locked = target;
  state.hovered = null;
  clearCenterSelectionForTarget(state.locked);
  if (!state.locked) state.cameraLocked = false;
  setTarget(state.locked);
  if (wasCameraLocked) {
    markProjectionDirty();
  } else {
    updateCoordinateReadout();
    queueRender();
  }
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
    case "pulsationSpeed":
      state.pulsationSpeed = defaultPulsationSpeedForPreset(preset);
      state.pulsationSpeedLog = Math.log10(state.pulsationSpeed);
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
  elements.mobileControlsToggle?.addEventListener("click", () => setMobileControlsOpen(true));
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
    MOBILE_CONTROLS_MEDIA.addEventListener("change", syncMobileControlsVisibility);
  } else {
    MOBILE_CONTROLS_MEDIA.addListener(syncMobileControlsVisibility);
  }
  elements.mobilePanelHeader?.addEventListener("pointerdown", beginMobileDrawerSwipe);
  elements.mobilePanelHeader?.addEventListener("pointermove", updateMobileDrawerSwipe);
  elements.mobilePanelHeader?.addEventListener("pointerup", endMobileDrawerSwipe);
  elements.mobilePanelHeader?.addEventListener("pointercancel", endMobileDrawerSwipe);
  syncMobileControlsVisibility();
}

function bindControls() {
  bindMobileControls();

  elements.overlayToggle?.addEventListener("click", () => {
    setOverlaysHidden(!state.overlaysHidden);
  });

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
  document.querySelectorAll("[data-exposure]").forEach((input) => {
    input.addEventListener("input", () => {
      setDatasetExposure(input.dataset.exposure, 10 ** Number(input.value));
    });
  });

  const updatePulsationSpeed = () => {
    state.pulsationSpeed = clampPulsationSpeed(10 ** Number(controls.pulsationSpeed.value));
    state.pulsationSpeedLog = Math.log10(state.pulsationSpeed);
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

  elements.faceView?.addEventListener("click", () => {
    markOrientationGridActive();
    cancelIntroRotation();
    cancelAxisSpinAnimation();
    state.yaw = degreesToRadians(FACE_VIEW_ANGLES_DEGREES.yaw);
    state.pitch = degreesToRadians(FACE_VIEW_ANGLES_DEGREES.pitch);
    state.roll = degreesToRadians(FACE_VIEW_ANGLES_DEGREES.roll);
    recenterViewport();
    syncRangeOutputs();
    markProjectionDirty();
  });

  elements.edgeView?.addEventListener("click", () => {
    markOrientationGridActive();
    cancelIntroRotation();
    cancelAxisSpinAnimation();
    state.yaw = degreesToRadians(EDGE_VIEW_ANGLES_DEGREES.yaw);
    state.pitch = degreesToRadians(EDGE_VIEW_ANGLES_DEGREES.pitch);
    state.roll = degreesToRadians(EDGE_VIEW_ANGLES_DEGREES.roll);
    recenterViewport();
    syncRangeOutputs();
    markProjectionDirty();
  });

  canvas.addEventListener("pointerdown", (event) => {
    if (handleCanvasTouchPointerDown(event)) return;
    event.preventDefault();
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
    hoverTimer = window.setTimeout(() => {
      state.hovered = nearestTarget(event.clientX, event.clientY);
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
      selectTargetAt(event.clientX, event.clientY);
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
      setZoom(next, event.clientX, event.clientY);
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
  scene.bounds = payload.bounds;
  scene.coordinateContext = coordinateContextFromPayload(payload);
  scene.skyGridBounds = skyGridBoundsFromPayload(payload);
  scene.catalog = payload.datasets.catalog.map((row) => {
    const projected = { x: 0, y: 0, z: 0, perspective: 1 };
    const intrinsicVMinusI = intrinsicVMinusIForRow(row);
    const point = {
      kind: "catalog",
      row,
      coordinates: catalogCoordinates(row),
      activeCoordinates: null,
      projected,
      radiusUnit: pointRadiusUnitFromStellarRadius(row[IDX.radius]),
      alphaBaseUnit: pointAlphaUnitBaseFromLuminosity(row[IDX.lum]) * BASE_LUMINOSITY_FACTOR,
      vMinusI: Number.isFinite(row[IDX.vMinusI]) ? row[IDX.vMinusI] : null,
      vMinusI0: Number.isFinite(intrinsicVMinusI) ? intrinsicVMinusI : null,
      color: colorForVMinusI(intrinsicVMinusI, row[IDX.spectral]),
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
      currentAlpha: 0,
      currentRadius: 0,
      staticBaseRadius: -1,
      staticAlphaUnit: -1,
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
      color: colorForVMinusI(row[CHR.vMinusI0], 5),
    });
  }
  for (const bins of clusterHrBinsByIndex.values()) {
    bins.sort((left, right) => left.logLum - right.logLum);
  }
  scene.clusterStarsByCluster = new Map();
  scene.clusterStars = (payload.datasets.clusterStars || []).map((row, index) => {
    const clusterIndex = row[CS.cluster];
    const projected = { x: 0, y: 0, z: 0, perspective: 1 };
    const point = {
      kind: "clusterStar",
      row,
      clusterIndex,
      coordinates: clusterStarCoordinates(row),
      activeCoordinates: null,
      projected,
      radiusUnit: pointRadiusUnitFromStellarRadius(row[CS.radius]),
      alphaBaseUnit: pointAlphaUnitBaseFromLuminosity(row[CS.lum]),
      vMinusI0: Number.isFinite(row[CS.vMinusI0]) ? row[CS.vMinusI0] : null,
      color: Number.isFinite(row[CS.temperature])
        ? colorForTemperature(row[CS.temperature])
        : colorForVMinusI(row[CS.vMinusI0], row[CS.spectral]),
      sample: hashString(`cs-${row[CS.cluster]}-${index}`) % 100,
      lightCurve: null,
    };
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
      currentAlpha: 0,
      currentRadius: 0,
      staticBaseRadius: -1,
      staticAlphaUnit: -1,
      staticRadiusFactor: -1,
      staticRadiusScale: -1,
      staticExposure: -1,
      staticRadius: 0,
      staticAlpha: 0,
    };
    return point;
  });
  scene.clusters = (payload.datasets.clusters || []).map((row, index) => {
    const projected = { x: 0, y: 0, z: 0, perspective: 1 };
    const point = {
      kind: "cluster",
      index,
      row,
      coordinates: clusterCoordinates(row),
      activeCoordinates: null,
      projected,
      activeProjected: null,
      radiusPc: row[CL.radiusPc],
      glowAlphaBaseUnit: pointAlphaUnitBaseFromLuminosity(row[CL.unresolvedLum] || 0),
      glowBins: clusterGlowBinsByIndex.get(index) || [],
      hrBins: clusterHrBinsByIndex.get(index) || [],
      sample: hashString(`cluster-${row[CL.name]}-${index}`) % 100,
      searchText: clusterSearchTextForRow(row),
    };
    point.drawItem = {
      point,
      projected,
      screenRadius: 10,
      glowAlphaUnit: 0,
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
