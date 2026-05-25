const canvas = document.querySelector("#clockCanvas");
const ctx = canvas.getContext("2d");
const digitalTime = document.querySelector("#digitalTime");
const statusEl = document.querySelector("#clockStatus");
const SUN_OUTSIDE_COLOR = "#540b0e";
const SUN_INSIDE_COLOR = "#fff3b0";
const MINUTE_INACTIVE_ALPHA = 0.15;

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
  const mobileLayout = rect.width < 720 || rect.height < 520;
  const diagramScale = size < 360 ? 0.34 : compact ? 0.36 : narrow ? 0.392 : 0.43;
  frame = {
    width: rect.width,
    height: rect.height,
    size,
    compact,
    narrow,
    mobileLayout,
    mobilePortrait: mobileLayout && rect.height >= rect.width,
    mobileLandscape: mobileLayout && rect.width > rect.height,
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

function overlayAlphaForTarget(targetAlpha, baseAlpha) {
  const clampedTarget = Math.min(1, Math.max(baseAlpha, targetAlpha));
  return (clampedTarget - baseAlpha) / (1 - baseAlpha);
}

function smoothStep(edge0, edge1, value) {
  const span = edge1 - edge0 || 1;
  const t = Math.min(1, Math.max(0, (value - edge0) / span));
  return t * t * (3 - 2 * t);
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

function drawPathRange(ray, startIndex, endIndex, color, lineWidth, alpha = 1, options = {}) {
  if (ray.points.length < 2 || endIndex <= startIndex) {
    return;
  }

  const start = Math.max(0, startIndex);
  const end = Math.min(ray.points.length - 1, endIndex);
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = color;
  ctx.lineWidth = scaleStroke(lineWidth);
  ctx.lineCap = options.lineCap || "round";
  ctx.lineJoin = options.lineJoin || "round";
  ctx.beginPath();
  const first = toScreen(ray.points[start]);
  ctx.moveTo(first.x, first.y);
  for (let index = start + 1; index <= end; index += 1) {
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

function drawFadedPath(ray, color, lineWidth, minAlpha = 0.08, maxAlpha = 0.56, fadePower = 1.65) {
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
    const fade = Math.pow((chunk + 1) / chunks, fadePower);
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

function drawMinuteAgeFadedPath(ray, marker, progress) {
  if (ray.points.length < 2) {
    return;
  }

  const currentProgress = ((progress % 1) + 1) % 1;
  const endIndex = Math.max(1, marker.index);
  const points = ray.points.slice(0, endIndex);
  const coordinates = ray.coordinate.slice(0, endIndex);
  points.push(marker.point);
  coordinates.push(currentProgress);

  const segmentCount = points.length - 1;
  if (segmentCount < 1) {
    return;
  }

  const chunks = Math.min(180, Math.max(1, segmentCount));
  const currentMinutes = currentProgress * 60;

  ctx.save();
  ctx.strokeStyle = ray.color;
  ctx.lineWidth = scaleStroke(ray.lineWidth + 0.7);
  ctx.lineCap = "butt";
  ctx.lineJoin = "round";

  for (let chunk = 0; chunk < chunks; chunk += 1) {
    const startIndex = Math.floor((chunk / chunks) * segmentCount);
    const end = Math.floor(((chunk + 1) / chunks) * segmentCount);
    const endChunkIndex = chunk === chunks - 1 ? segmentCount : Math.max(startIndex + 1, end);
    const midProgress = (coordinates[startIndex] + coordinates[endChunkIndex]) * 0.5;
    const ageMinutes = Math.max(0, (currentProgress - midProgress) * 60);
    let opacity = 0;
    if (ageMinutes <= 1.5) {
      opacity = 1;
    } else if (ageMinutes <= 3) {
      const transition = smoothStep(1.5, 3, ageMinutes);
      opacity = 1 - transition * 0.25;
    } else {
      const tailMinutes = Math.max(1, currentMinutes - 3);
      const tailProgress = smoothStep(0, 1, Math.min(1, (ageMinutes - 3) / tailMinutes));
      opacity = MINUTE_INACTIVE_ALPHA + (0.75 - MINUTE_INACTIVE_ALPHA) * (1 - tailProgress);
    }

    ctx.globalAlpha = overlayAlphaForTarget(opacity, MINUTE_INACTIVE_ALPHA);
    ctx.beginPath();
    const start = toScreen(points[startIndex]);
    ctx.moveTo(start.x, start.y);
    for (let index = startIndex + 1; index <= endChunkIndex; index += 1) {
      const point = toScreen(points[index]);
      ctx.lineTo(point.x, point.y);
    }
    ctx.stroke();
  }

  ctx.restore();
}

function drawYearProgressRange(ray, startIndex, endIndex, lineWidth, alpha = 1) {
  drawPathRange(ray, startIndex, endIndex, ray.color, lineWidth, alpha, {
    lineCap: "butt",
    lineJoin: "round",
  });
}

function drawYearSegments(ray, alpha, lineWidth) {
  if (!ray.segments?.length) {
    drawPath(ray, ray.color, lineWidth, alpha, ray.points.length - 1, {
      lineCap: "butt",
      lineJoin: "round",
    });
    return;
  }

  ray.segments.forEach((segment) => {
    drawPathRange(
      ray,
      segment.start,
      segment.end,
      ray.color,
      lineWidth,
      alpha,
      { lineCap: "butt", lineJoin: "round" },
    );
  });
}

function drawYearActivePath(ray, progress) {
  if (!ray.segments?.length) {
    const marker = pointAt(ray, progress);
    const activeRay = pathToMarker(ray, marker);
    drawPath(activeRay, ray.color, ray.lineWidth + 0.2, 0.38, activeRay.points.length - 1, {
      lineCap: "butt",
      lineJoin: "round",
    });
    return;
  }

  const target = ((progress % 1) + 1) % 1;
  ray.segments.forEach((segment) => {
    if (target <= segment.startTau) {
      return;
    }

    if (target >= segment.endTau) {
      drawYearProgressRange(ray, segment.start, segment.end, ray.lineWidth + 0.2, 0.38);
      return;
    }

    const marker = pointAt(ray, target);
    const activeRay = pathToMarker(ray, marker, segment.start);
    drawPath(activeRay, ray.color, ray.lineWidth + 0.2, 0.38, activeRay.points.length - 1, {
      lineCap: "butt",
      lineJoin: "round",
    });
  });
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

function centeredTextWidth(text, fontSize, weight = 760, haloWidth = 0) {
  ctx.save();
  ctx.font = `${weight} ${scaleFont(fontSize)}px Inter, sans-serif`;
  const width = ctx.measureText(text).width + scaleHalo(haloWidth);
  ctx.restore();
  return width;
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

function activeHourLabelSize() {
  return frame.compact ? 32 : frame.narrow ? 31 : 31;
}

function activeMinuteLabelSize() {
  return frame.compact ? 17 : frame.narrow ? 16 : 16;
}

function activeSecondLabelSize() {
  return frame.compact ? 16 : frame.narrow ? 15 : 15;
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
        activeHourLabelSize(),
        850,
        frame.compact ? 1.7 : frame.narrow ? 1.5 : 3.2,
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
      minuteRay.outerRadius + (frame.compact ? 0.086 : frame.narrow ? 0.082 : 0.048),
      angleForClockIndex(activeLabels.minute, 60),
      minuteRay.markerColor || minuteRay.color,
      activeMinuteLabelSize(),
      840,
      frame.compact ? 2.1 : frame.narrow ? 1.8 : 4.6,
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
      activeSecondLabelSize(),
      840,
      frame.compact ? 1.9 : frame.narrow ? 1.6 : 3.8,
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
  const dateText = formatDateText(now);
  const timeText = formatTimeText(now);

  if (frame.mobileLayout) {
    const dateSize = frame.compact ? 42 : 38;
    const timeSize = frame.compact ? 46 : 42;
    const dateHalo = frame.compact ? 5.2 : 4.8;
    const timeHalo = frame.compact ? 5.8 : 5.4;
    const clockRadius = frame.scale * (frame.compact ? 1.17 : 1.145);

    if (frame.mobilePortrait) {
      const topSpace = Math.max(0, frame.cy - clockRadius);
      const labelY = Math.max(
        scaleFont(timeSize) * 0.85,
        Math.min(frame.height * 0.095, topSpace * 0.4),
      );
      drawCenteredHaloText(
        dateText,
        frame.cx,
        labelY,
        SUN_INSIDE_COLOR,
        dateSize,
        840,
        dateHalo,
        SUN_OUTSIDE_COLOR,
      );
      drawCenteredHaloText(
        timeText,
        frame.cx,
        frame.height - labelY,
        SUN_INSIDE_COLOR,
        timeSize,
        850,
        timeHalo,
        SUN_OUTSIDE_COLOR,
      );
      return;
    }

    const sideSpace = Math.max(0, frame.cx - clockRadius);
    const labelX = Math.max(
      scaleFont(timeSize) * 2.8,
      Math.min(frame.width * 0.13, sideSpace * 0.48),
    );
    drawCenteredHaloText(
      dateText,
      labelX,
      frame.cy,
      SUN_INSIDE_COLOR,
      dateSize,
      840,
      dateHalo,
      SUN_OUTSIDE_COLOR,
    );
    drawCenteredHaloText(
      timeText,
      frame.width - labelX,
      frame.cy,
      SUN_INSIDE_COLOR,
      timeSize,
      850,
      timeHalo,
      SUN_OUTSIDE_COLOR,
    );
    return;
  }

  const sideDateSize = frame.narrow ? 35 : 38;
  const sideTimeSize = frame.narrow ? 38 : 42;
  const sideDateHalo = 5.6;
  const sideTimeHalo = 6.2;
  const sideClockRadius = frame.scale * 1.15;
  const sideSpace = Math.max(0, frame.cx - sideClockRadius);
  const labelGap = Math.max(24, frame.scale * 0.08);
  const dateWidth = centeredTextWidth(dateText, sideDateSize, 840, sideDateHalo);
  const timeWidth = centeredTextWidth(timeText, sideTimeSize, 850, sideTimeHalo);

  if (
    sideSpace >= dateWidth / 2 + labelGap
    && sideSpace >= timeWidth / 2 + labelGap
  ) {
    const leftLabelX = Math.max(dateWidth / 2 + 6, (frame.cx - sideClockRadius) / 2);
    const rightLabelX = Math.min(
      frame.width - timeWidth / 2 - 6,
      frame.width - (frame.cx - sideClockRadius) / 2,
    );

    drawCenteredHaloText(
      dateText,
      leftLabelX,
      frame.cy,
      SUN_INSIDE_COLOR,
      sideDateSize,
      840,
      sideDateHalo,
      SUN_OUTSIDE_COLOR,
    );
    drawCenteredHaloText(
      timeText,
      rightLabelX,
      frame.cy,
      SUN_INSIDE_COLOR,
      sideTimeSize,
      850,
      sideTimeHalo,
      SUN_OUTSIDE_COLOR,
    );
    return;
  }

  const dateOffset = frame.compact ? 0.78 : frame.narrow ? 0.73 : 0.69;
  const timeOffset = frame.compact ? 0.66 : frame.narrow ? 0.675 : 0.69;
  const dateSize = frame.compact ? 34 : frame.narrow ? 35 : 36;
  const timeSize = frame.compact ? 38 : frame.narrow ? 39 : 40;
  const dateHalo = frame.compact ? 4.4 : frame.narrow ? 5 : 5.6;
  const timeHalo = frame.compact ? 5 : frame.narrow ? 5.6 : 6.2;

  drawCenteredHaloText(
    dateText,
    frame.cx,
    frame.cy - frame.scale * dateOffset,
    SUN_OUTSIDE_COLOR,
    dateSize,
    840,
    dateHalo,
    SUN_INSIDE_COLOR,
  );
  drawCenteredHaloText(
    timeText,
    frame.cx,
    frame.cy + frame.scale * timeOffset,
    SUN_OUTSIDE_COLOR,
    timeSize,
    850,
    timeHalo,
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
  const yearRay = activeRays.find((ray) => ray.id === "year");
  const hourRay = activeRays.find((ray) => ray.id === "hours");
  const minuteRay = activeRays.find((ray) => ray.id === "minutes");
  const secondRay = activeRays.find((ray) => ray.id === "seconds");
  const nonYearRays = visibleRays.filter((ray) => ray.id !== "year");
  drawCircle(1, "rgba(84, 11, 14, 0.24)", 1.45);
  if (yearRay) {
    drawYearSegments(yearRay, frame.compact ? 0.07 : 0.052, yearRay.lineWidth + 0.05);
    drawYearActivePath(yearRay, progress.year);
  }
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

  nonYearRays.forEach((ray) => {
    const baseAlpha = ray.id === "hours" ? 0.2 : ray.id === "minutes" ? MINUTE_INACTIVE_ALPHA : 0.11;
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

  const markers = nonYearRays.map((ray) => {
    return {
      ray,
      renderRay: ray,
      marker: pointAt(ray, progress[ray.id]),
    };
  });

  markers.forEach(({ ray, renderRay, marker }) => {
    const activeRay = pathToMarker(renderRay, marker);
    if (ray.id === "minutes") {
      drawMinuteAgeFadedPath(ray, marker, progress.minutes);
    } else if (ray.id === "seconds") {
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
