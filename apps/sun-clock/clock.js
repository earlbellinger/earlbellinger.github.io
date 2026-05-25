const canvas = document.querySelector("#clockCanvas");
const ctx = canvas.getContext("2d");
const digitalTime = document.querySelector("#digitalTime");
const statusEl = document.querySelector("#clockStatus");
const SUN_OUTSIDE_COLOR = "#540b0e";
const SUN_INSIDE_COLOR = "#fff3b0";

let clockData = null;
let preparedRays = [];
let frame = null;

function setupCanvas() {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.round(rect.width * dpr));
  canvas.height = Math.max(1, Math.round(rect.height * dpr));
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  const size = Math.min(rect.width, rect.height);
  const compact = size < 440;
  const narrow = size < 560;
  const diagramScale = size < 360 ? 0.34 : compact ? 0.36 : narrow ? 0.392 : 0.43;
  frame = {
    width: rect.width,
    height: rect.height,
    size,
    compact,
    narrow,
    cx: rect.width / 2,
    cy: rect.height / 2,
    scale: size * diagramScale,
    textScale: Math.min(1, Math.max(0.52, size / 660)),
    strokeScale: Math.min(1, Math.max(0.72, size / 700)),
    markerScale: Math.min(1, Math.max(0.62, size / 680)),
  };
}

function toScreen(point) {
  return {
    x: frame.cx + point.x * frame.scale,
    y: frame.cy - point.y * frame.scale,
  };
}

function scaleFont(fontSize) {
  const minimum = fontSize >= 30 ? 18 : fontSize >= 20 ? 12 : 6.5;
  return Math.max(minimum, fontSize * frame.textScale);
}

function scaleStroke(width) {
  return Math.max(0.75, width * frame.strokeScale);
}

function scaleHalo(width) {
  if (width <= 0) {
    return 0;
  }
  return Math.max(1.2, width * frame.textScale);
}

function scaleMarker(size) {
  return Math.max(3.2, size * frame.markerScale);
}

function prepareRay(ray) {
  const points = ray.x.map((x, index) => ({ x, y: ray.y[index] }));
  let coordinate = ray.tau;
  if (!coordinate || coordinate.length !== points.length) {
    coordinate = [0];
    for (let index = 1; index < points.length; index += 1) {
      const dx = points[index].x - points[index - 1].x;
      const dy = points[index].y - points[index - 1].y;
      coordinate.push(coordinate[index - 1] + Math.hypot(dx, dy));
    }
    const totalLength = coordinate[coordinate.length - 1] || 1;
    coordinate = coordinate.map((value) => value / totalLength);
  }

  return {
    ...ray,
    points,
    coordinate,
  };
}

function pointAt(ray, progress) {
  const target = ((progress % 1) + 1) % 1;
  let lo = 0;
  let hi = ray.coordinate.length - 1;
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    if (ray.coordinate[mid] < target) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }

  const index = Math.max(1, lo);
  const prev = ray.points[index - 1];
  const next = ray.points[index];
  const span = ray.coordinate[index] - ray.coordinate[index - 1] || 1;
  const local = (target - ray.coordinate[index - 1]) / span;
  return {
    point: {
      x: prev.x + (next.x - prev.x) * local,
      y: prev.y + (next.y - prev.y) * local,
    },
    prev,
    next,
    index,
  };
}

function drawPath(ray, color, lineWidth, alpha = 1, limitIndex = ray.points.length - 1, options = {}) {
  if (ray.points.length < 2) {
    return;
  }

  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = color;
  ctx.lineWidth = scaleStroke(lineWidth);
  ctx.lineCap = options.lineCap || "round";
  ctx.lineJoin = options.lineJoin || "round";
  ctx.beginPath();
  const first = toScreen(ray.points[0]);
  ctx.moveTo(first.x, first.y);
  for (let index = 1; index <= limitIndex; index += 1) {
    const point = toScreen(ray.points[index]);
    ctx.lineTo(point.x, point.y);
  }
  ctx.stroke();
  ctx.restore();
}

function drawPathInsideRadius(
  ray,
  color,
  lineWidth,
  alpha,
  limitIndex,
  clipRadius,
  options = {},
) {
  ctx.save();
  ctx.beginPath();
  ctx.arc(frame.cx, frame.cy, clipRadius * frame.scale, 0, Math.PI * 2);
  ctx.clip();
  drawPath(ray, color, lineWidth, alpha, limitIndex, options);
  ctx.restore();
}

function pathToMarker(ray, marker, startIndex = 0) {
  const endIndex = Math.max(1, marker.index);
  const clampedStart = Math.min(Math.max(0, startIndex), endIndex - 1);
  const points = ray.points.slice(clampedStart, endIndex);
  if (!points.length) {
    points.push(marker.prev);
  }
  points.push(marker.point);
  return { ...ray, points };
}

function drawCurrentPoint(marker, color, size) {
  const point = toScreen(marker.point);
  ctx.save();
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(point.x, point.y, scaleMarker(size), 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function drawCircle(radius, color, width, alpha = 1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = color;
  ctx.lineWidth = scaleStroke(width);
  ctx.beginPath();
  ctx.arc(frame.cx, frame.cy, radius * frame.scale, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}

function fillCircle(radius, color) {
  ctx.save();
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(frame.cx, frame.cy, radius * frame.scale, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function drawCircumferenceTrace(
  ray,
  progress,
  width,
  color = ray.markerColor || ray.color,
  radius = ray.outerRadius,
) {
  if (progress <= 0) {
    return;
  }

  const start = -Math.PI / 2;
  const end = start + progress * Math.PI * 2;

  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = scaleStroke(width);
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.arc(frame.cx, frame.cy, radius * frame.scale, start, end);
  ctx.stroke();
  ctx.restore();
}

function drawFadedPath(ray, color, lineWidth, minAlpha = 0.08, maxAlpha = 0.56) {
  if (ray.points.length < 2) {
    return;
  }

  const chunks = Math.min(84, Math.max(3, ray.points.length - 1));
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = scaleStroke(lineWidth);
  ctx.lineCap = "butt";
  ctx.lineJoin = "round";

  for (let chunk = 0; chunk < chunks; chunk += 1) {
    const startIndex = Math.floor((chunk / chunks) * (ray.points.length - 1));
    const endIndex = Math.max(
      startIndex + 1,
      Math.floor(((chunk + 1) / chunks) * (ray.points.length - 1)),
    );
    const fade = Math.pow((chunk + 1) / chunks, 1.65);
    ctx.globalAlpha = minAlpha + (maxAlpha - minAlpha) * fade;
    ctx.beginPath();
    const start = toScreen(ray.points[startIndex]);
    ctx.moveTo(start.x, start.y);
    for (let index = startIndex + 1; index <= endIndex; index += 1) {
      const point = toScreen(ray.points[index]);
      ctx.lineTo(point.x, point.y);
    }
    ctx.stroke();
  }

  ctx.restore();
}

function drawRadialLabel(text, radius, theta, color, fontSize, weight = 700) {
  const x = frame.cx + radius * Math.cos(theta) * frame.scale;
  const y = frame.cy - radius * Math.sin(theta) * frame.scale;
  ctx.save();
  ctx.fillStyle = color;
  ctx.font = `${weight} ${scaleFont(fontSize)}px Inter, sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(text, x, y);
  ctx.restore();
}

function drawRadialLabelWithHalo(
  text,
  radius,
  theta,
  color,
  fontSize,
  weight = 700,
  haloWidth = 5,
  haloColor = SUN_INSIDE_COLOR,
) {
  const x = frame.cx + radius * Math.cos(theta) * frame.scale;
  const y = frame.cy - radius * Math.sin(theta) * frame.scale;
  ctx.save();
  ctx.font = `${weight} ${scaleFont(fontSize)}px Inter, sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.lineJoin = "round";
  const scaledHalo = scaleHalo(haloWidth);
  if (scaledHalo > 0) {
    ctx.lineWidth = scaledHalo;
    ctx.strokeStyle = haloColor;
    ctx.strokeText(text, x, y);
  }
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
  ctx.restore();
}

function drawCenteredHaloText(
  text,
  x,
  y,
  color,
  fontSize,
  weight = 760,
  haloWidth = 3,
  haloColor = SUN_INSIDE_COLOR,
) {
  ctx.save();
  ctx.font = `${weight} ${scaleFont(fontSize)}px Inter, sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.lineJoin = "round";
  const scaledHalo = scaleHalo(haloWidth);
  if (scaledHalo > 0) {
    ctx.lineWidth = scaledHalo;
    ctx.strokeStyle = haloColor;
    ctx.strokeText(text, x, y);
  }
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
  ctx.restore();
}

function drawTick(radius0, radius1, theta, color, width) {
  const a = {
    x: frame.cx + radius0 * Math.cos(theta) * frame.scale,
    y: frame.cy - radius0 * Math.sin(theta) * frame.scale,
  };
  const b = {
    x: frame.cx + radius1 * Math.cos(theta) * frame.scale,
    y: frame.cy - radius1 * Math.sin(theta) * frame.scale,
  };
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = scaleStroke(width);
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x, b.y);
  ctx.stroke();
  ctx.restore();
}

function angleForClockIndex(index, total) {
  return Math.PI / 2 - (index / total) * Math.PI * 2;
}

function activeLabelBuckets(now) {
  const hour = now.getHours() % 12 || 12;
  const minute = now.getMinutes();
  const second = now.getSeconds();
  return { hour, minute, second };
}

function isLeapYear(year) {
  return year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
}

function yearProgressInfo(now) {
  const year = now.getFullYear();
  const start = new Date(year, 0, 1);
  const end = new Date(year + 1, 0, 1);
  const days = isLeapYear(year) ? 366 : 365;
  const dayStart = Date.UTC(year, now.getMonth(), now.getDate());
  const yearStart = Date.UTC(year, 0, 1);
  const day = Math.min(days, Math.floor((dayStart - yearStart) / 86400000) + 1);

  return {
    day,
    days,
    fraction: Math.min(1, Math.max(0, (now - start) / (end - start))),
  };
}

function activeRaysForYear(yearDays) {
  return preparedRays.filter((ray) => !ray.yearDays || ray.yearDays === yearDays);
}

function hourLabelRadius(active) {
  if (active) {
    return frame.compact ? 1.125 : frame.narrow ? 1.115 : 1.095;
  }
  return frame.compact ? 1.095 : frame.narrow ? 1.085 : 1.075;
}

function drawClockNumbers(activeLabels, activeRays) {
  const hourRay = activeRays.find((ray) => ray.id === "hours");

  for (let hour = 1; hour <= 12; hour += 1) {
    const index = hour % 12;
    const theta = angleForClockIndex(index, 12);
    const active = hour === activeLabels.hour;
    if (active) {
      drawRadialLabelWithHalo(
        String(hour),
        hourLabelRadius(true),
        theta,
        SUN_INSIDE_COLOR,
        29,
        850,
        frame.narrow ? 1.2 : 3,
        hourRay?.markerColor || SUN_OUTSIDE_COLOR,
      );
    } else {
      drawRadialLabelWithHalo(
        String(hour),
        hourLabelRadius(false),
        theta,
        SUN_OUTSIDE_COLOR,
        25,
        780,
        frame.narrow ? 1.2 : 2.6,
        SUN_INSIDE_COLOR,
      );
    }
  }

  const minuteRay = activeRays.find((ray) => ray.id === "minutes");
  if (minuteRay) {
    for (let minute = 0; minute < 60; minute += 1) {
      const theta = angleForClockIndex(minute, 60);
      const major = minute % 5 === 0;
      const activeExact = minute === activeLabels.minute;
      if (major && !activeExact) {
        drawRadialLabelWithHalo(
          String(minute).padStart(2, "0"),
          minuteRay.outerRadius + (frame.narrow ? 0.062 : 0.03),
          theta,
          minuteRay.color,
          11,
          720,
          frame.narrow ? 0 : 5,
          SUN_INSIDE_COLOR,
        );
      }
    }
  }

}

function drawMovingMinuteSecondLabels(activeLabels, activeRays) {
  const minuteRay = activeRays.find((ray) => ray.id === "minutes");
  if (minuteRay) {
    drawRadialLabelWithHalo(
      String(activeLabels.minute).padStart(2, "0"),
      minuteRay.outerRadius + (frame.narrow ? 0.078 : 0.042),
      angleForClockIndex(activeLabels.minute, 60),
      minuteRay.markerColor || minuteRay.color,
      14,
      840,
      frame.narrow ? 1.6 : 4.2,
      SUN_INSIDE_COLOR,
    );
  }

  const secondRay = activeRays.find((ray) => ray.id === "seconds");
  if (secondRay) {
    drawRadialLabelWithHalo(
      String(activeLabels.second).padStart(2, "0"),
      secondRay.outerRadius - 0.048,
      angleForClockIndex(activeLabels.second, 60),
      secondRay.markerColor || secondRay.color,
      13,
      840,
      frame.narrow ? 1.4 : 3.4,
      SUN_INSIDE_COLOR,
    );
  }
}

function formatTimeText(now) {
  return new Intl.DateTimeFormat(undefined, {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
  }).format(now);
}

function formatDateText(now) {
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function drawDialDateTime(now) {
  drawCenteredHaloText(
    formatDateText(now),
    frame.cx,
    frame.cy - frame.scale * (frame.compact ? 0.66 : 0.69),
    "#540b0e",
    36,
    840,
    5.8,
    SUN_INSIDE_COLOR,
  );
  drawCenteredHaloText(
    formatTimeText(now),
    frame.cx,
    frame.cy + frame.scale * (frame.compact ? 0.66 : 0.69),
    "#540b0e",
    38,
    850,
    6,
    SUN_INSIDE_COLOR,
  );
}

function timeFractions(now, yearInfo) {
  const hours = now.getHours() % 12;
  const minutes = now.getMinutes();
  const seconds = now.getSeconds();
  const milliseconds = now.getMilliseconds();
  return {
    hours: (hours + minutes / 60 + seconds / 3600 + milliseconds / 3600000) / 12,
    minutes: (minutes + seconds / 60 + milliseconds / 60000) / 60,
    seconds: (seconds + milliseconds / 1000) / 60,
    year: yearInfo.fraction,
  };
}

function updateDigitalTime(now) {
  if (!digitalTime) {
    return;
  }

  const time = new Intl.DateTimeFormat(undefined, {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(now);
  digitalTime.textContent = time;
}

function draw(now) {
  if (!clockData || !frame) {
    return;
  }

  const yearInfo = yearProgressInfo(now);
  const activeRays = activeRaysForYear(yearInfo.days);
  const visibleRays = activeRays;
  const progress = timeFractions(now, yearInfo);
  const activeLabels = activeLabelBuckets(now);
  updateDigitalTime(now);
  ctx.clearRect(0, 0, frame.width, frame.height);
  ctx.fillStyle = SUN_OUTSIDE_COLOR;
  ctx.fillRect(0, 0, frame.width, frame.height);

  fillCircle(1, SUN_INSIDE_COLOR);
  const hourRay = activeRays.find((ray) => ray.id === "hours");
  const minuteRay = activeRays.find((ray) => ray.id === "minutes");
  const secondRay = activeRays.find((ray) => ray.id === "seconds");
  drawCircle(1, "rgba(84, 11, 14, 0.24)", 1.45);
  if (hourRay) {
    drawCircumferenceTrace(hourRay, progress.hours, 2.25, SUN_INSIDE_COLOR, frame.compact ? 1.008 : 1.014);
  }
  if (minuteRay) {
    drawCircumferenceTrace(minuteRay, progress.minutes, 1.55);
  }
  if (secondRay) {
    drawCircumferenceTrace(secondRay, progress.seconds, 1.35);
  }

  drawClockNumbers(activeLabels, activeRays);

  visibleRays.forEach((ray) => {
    if (ray.id === "year") {
      return;
    }
    const baseAlpha = ray.id === "hours" ? 0.2 : ray.id === "minutes" ? 0.15 : 0.11;
    drawPath(ray, ray.color, ray.lineWidth, baseAlpha);
  });

  ctx.save();
  ctx.fillStyle = SUN_INSIDE_COLOR;
  ctx.strokeStyle = "rgba(84, 11, 14, 0.15)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(frame.cx, frame.cy, frame.scale * 0.038, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();
  ctx.restore();

  const markers = visibleRays.map((ray) => ({
    ray,
    marker: pointAt(ray, progress[ray.id]),
  }));

  markers.forEach(({ ray, marker }) => {
    const activeRay = pathToMarker(ray, marker);
    if (ray.id === "year") {
      drawPathInsideRadius(
        activeRay,
        ray.color,
        ray.lineWidth + 0.12,
        0.24,
        activeRay.points.length - 1,
        0.984,
        { lineCap: "butt", lineJoin: "bevel" },
      );
    } else if (ray.id === "minutes" || ray.id === "seconds") {
      drawFadedPath(activeRay, ray.color, ray.lineWidth + 0.55);
    } else {
      drawPath(activeRay, ray.color, ray.lineWidth + 0.55, 0.7);
    }
  });

  markers.forEach(({ ray, marker }) => {
    if (ray.id === "year") {
      return;
    }
    const trailStart = Math.max(0, marker.index - Math.floor(ray.points.length * 0.04));
    const trailRay = pathToMarker(ray, marker, trailStart);
    drawPath(trailRay, ray.color, ray.lineWidth + 1.4, 0.28);
  });

  markers.forEach(({ ray, marker }) => {
    if (ray.id === "year") {
      return;
    }
    drawCurrentPoint(marker, ray.markerColor || ray.color, ray.markerSize || 8);
  });

  drawMovingMinuteSecondLabels(activeLabels, activeRays);
  drawDialDateTime(now);
}

function animate() {
  draw(new Date());
  requestAnimationFrame(animate);
}

async function loadClock() {
  setupCanvas();
  let dataSource = "embedded";
  if (window.CLOCK_RAY_DATA) {
    clockData = window.CLOCK_RAY_DATA;
  } else {
    dataSource = "api";
    const response = await fetch("/api/clock-rays");
    if (!response.ok) {
      throw new Error("Could not load clock rays.");
    }
    clockData = await response.json();
  }
  preparedRays = clockData.rays.map(prepareRay);
  canvas.dataset.clockDataSource = dataSource;
  if (statusEl) {
    statusEl.textContent = "Live local time";
  }
  animate();
}

let resizeFrame = null;
function scheduleResize() {
  if (resizeFrame !== null) {
    cancelAnimationFrame(resizeFrame);
  }
  resizeFrame = requestAnimationFrame(() => {
    resizeFrame = null;
    setupCanvas();
    draw(new Date());
  });
}

window.addEventListener("resize", scheduleResize);
if (window.visualViewport) {
  window.visualViewport.addEventListener("resize", scheduleResize);
}

window.addEventListener("orientationchange", () => {
  setupCanvas();
  draw(new Date());
});

loadClock().catch((error) => {
  if (statusEl) {
    statusEl.textContent = error.message;
  }
});
