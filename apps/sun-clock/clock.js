const canvas = document.querySelector("#clockCanvas");
const ctx = canvas.getContext("2d");
const digitalTime = document.querySelector("#digitalTime");
const statusEl = document.querySelector("#clockStatus");
const SUN_OUTSIDE_COLOR = "#264653";
const SUN_INSIDE_COLOR = "#e9c46a";

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
  const diagramScale = size < 360 ? 0.35 : compact ? 0.372 : size < 560 ? 0.41 : 0.43;
  frame = {
    width: rect.width,
    height: rect.height,
    size,
    compact,
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

function drawPath(ray, color, lineWidth, alpha = 1, limitIndex = ray.points.length - 1) {
  if (ray.points.length < 2) {
    return;
  }

  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = color;
  ctx.lineWidth = scaleStroke(lineWidth);
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
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
  ctx.lineCap = "round";
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
  ctx.lineWidth = scaleHalo(haloWidth);
  ctx.strokeStyle = haloColor;
  ctx.strokeText(text, x, y);
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
  ctx.lineWidth = scaleHalo(haloWidth);
  ctx.strokeStyle = haloColor;
  ctx.strokeText(text, x, y);
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

function drawClockNumbers(activeLabels) {
  const hourRay = preparedRays.find((ray) => ray.id === "hours");

  for (let hour = 1; hour <= 12; hour += 1) {
    const index = hour % 12;
    const theta = angleForClockIndex(index, 12);
    const active = hour === activeLabels.hour;
    if (active) {
      drawRadialLabelWithHalo(
        String(hour),
        frame.compact ? 1.062 : 1.085,
        theta,
        hourRay?.markerColor || "#e76f51",
        29,
        850,
        2.4,
        "#111111",
      );
    } else {
      drawRadialLabel(String(hour), frame.compact ? 1.045 : 1.065, theta, SUN_INSIDE_COLOR, 25, 780);
    }
  }

  const minuteRay = preparedRays.find((ray) => ray.id === "minutes");
  if (minuteRay) {
    for (let minute = 0; minute < 60; minute += 1) {
      const theta = angleForClockIndex(minute, 60);
      const major = minute % 5 === 0;
      const activeExact = minute === activeLabels.minute;
      if (major && !activeExact) {
        drawRadialLabelWithHalo(
          String(minute).padStart(2, "0"),
          minuteRay.outerRadius + (frame.compact ? 0.018 : 0.03),
          theta,
          minuteRay.color,
          11,
          720,
          5,
          SUN_INSIDE_COLOR,
        );
      }
    }
  }

}

function drawMovingMinuteSecondLabels(activeLabels) {
  const minuteRay = preparedRays.find((ray) => ray.id === "minutes");
  if (minuteRay) {
    drawRadialLabelWithHalo(
      String(activeLabels.minute).padStart(2, "0"),
      minuteRay.outerRadius + (frame.compact ? 0.03 : 0.042),
      angleForClockIndex(activeLabels.minute, 60),
      minuteRay.markerColor || minuteRay.color,
      14,
      840,
      4.2,
      SUN_INSIDE_COLOR,
    );
  }

  const secondRay = preparedRays.find((ray) => ray.id === "seconds");
  if (secondRay) {
    drawRadialLabelWithHalo(
      String(activeLabels.second).padStart(2, "0"),
      secondRay.outerRadius - 0.048,
      angleForClockIndex(activeLabels.second, 60),
      secondRay.markerColor || secondRay.color,
      13,
      840,
      3.4,
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
    "#264653",
    36,
    840,
    5.8,
    SUN_INSIDE_COLOR,
  );
  drawCenteredHaloText(
    formatTimeText(now),
    frame.cx,
    frame.cy + frame.scale * (frame.compact ? 0.66 : 0.69),
    "#264653",
    38,
    850,
    6,
    SUN_INSIDE_COLOR,
  );
}

function timeFractions(now) {
  const hours = now.getHours() % 12;
  const minutes = now.getMinutes();
  const seconds = now.getSeconds();
  const milliseconds = now.getMilliseconds();
  return {
    hours: (hours + minutes / 60 + seconds / 3600 + milliseconds / 3600000) / 12,
    minutes: (minutes + seconds / 60 + milliseconds / 60000) / 60,
    seconds: (seconds + milliseconds / 1000) / 60,
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

  const progress = timeFractions(now);
  const activeLabels = activeLabelBuckets(now);
  updateDigitalTime(now);
  ctx.clearRect(0, 0, frame.width, frame.height);
  ctx.fillStyle = SUN_OUTSIDE_COLOR;
  ctx.fillRect(0, 0, frame.width, frame.height);

  fillCircle(1, SUN_INSIDE_COLOR);
  const hourRay = preparedRays.find((ray) => ray.id === "hours");
  const minuteRay = preparedRays.find((ray) => ray.id === "minutes");
  const secondRay = preparedRays.find((ray) => ray.id === "seconds");
  drawCircle(1, "rgba(38, 70, 83, 0.24)", 1.45);
  if (hourRay) {
    drawCircumferenceTrace(hourRay, progress.hours, 2.25, SUN_INSIDE_COLOR, frame.compact ? 1.008 : 1.014);
  }
  if (minuteRay) {
    drawCircumferenceTrace(minuteRay, progress.minutes, 1.55);
  }
  if (secondRay) {
    drawCircumferenceTrace(secondRay, progress.seconds, 1.35);
  }

  drawClockNumbers(activeLabels);

  preparedRays.forEach((ray) => {
    const baseAlpha = ray.id === "hours" ? 0.2 : ray.id === "minutes" ? 0.15 : 0.11;
    drawPath(ray, ray.color, ray.lineWidth, baseAlpha);
  });

  ctx.save();
  ctx.fillStyle = SUN_INSIDE_COLOR;
  ctx.strokeStyle = "rgba(15, 23, 42, 0.12)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(frame.cx, frame.cy, frame.scale * 0.038, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();
  ctx.restore();

  const markers = preparedRays.map((ray) => ({
    ray,
    marker: pointAt(ray, progress[ray.id]),
  }));

  markers.forEach(({ ray, marker }) => {
    const activeRay = pathToMarker(ray, marker);
    if (ray.id === "minutes" || ray.id === "seconds") {
      drawFadedPath(activeRay, ray.color, ray.lineWidth + 0.55);
    } else {
      drawPath(activeRay, ray.color, ray.lineWidth + 0.55, 0.7);
    }
  });

  markers.forEach(({ ray, marker }) => {
    const trailStart = Math.max(0, marker.index - Math.floor(ray.points.length * 0.04));
    const trailRay = pathToMarker(ray, marker, trailStart);
    drawPath(trailRay, ray.color, ray.lineWidth + 1.4, 0.28);
  });

  markers.forEach(({ ray, marker }) => {
    drawCurrentPoint(marker, ray.markerColor || ray.color, ray.markerSize || 8);
  });

  drawMovingMinuteSecondLabels(activeLabels);
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
