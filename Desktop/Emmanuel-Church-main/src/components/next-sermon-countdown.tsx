"use client";

import { useEffect, useState } from "react";

const CHURCH_TIME_ZONE = "America/Chicago";
const SERVICE_START_WEEKDAY = 0; // Sunday
const SERVICE_START_HOUR = 11;
const SERVICE_START_MINUTE = 0;

function getTimeZoneOffsetMs(date: Date, timeZone: string) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    timeZoneName: "shortOffset",
    hour: "numeric",
  }).formatToParts(date);

  const offsetPart = parts.find((part) => part.type === "timeZoneName")?.value;
  const match = offsetPart?.match(/GMT([+-])(\d{1,2})(?::?(\d{2}))?/);

  if (!match) {
    return 0;
  }

  const sign = match[1] === "-" ? -1 : 1;
  const hours = Number(match[2] || 0);
  const minutes = Number(match[3] || 0);

  return sign * (hours * 60 + minutes) * 60 * 1000;
}

function getZonedParts(date: Date, timeZone: string) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
    hour12: false,
  }).formatToParts(date);

  const values = Object.fromEntries(parts.map((part) => [part.type, part.value]));

  return {
    year: Number(values.year),
    month: Number(values.month),
    day: Number(values.day),
    hour: Number(values.hour),
    minute: Number(values.minute),
    second: Number(values.second),
  };
}

function zonedLocalTimeToUtc({
  year,
  month,
  day,
  hour,
  minute,
  second,
  timeZone,
}: {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  second: number;
  timeZone: string;
}) {
  const utcGuess = Date.UTC(year, month - 1, day, hour, minute, second);
  let adjusted = utcGuess;

  for (let index = 0; index < 2; index += 1) {
    const offset = getTimeZoneOffsetMs(new Date(adjusted), timeZone);
    adjusted = utcGuess - offset;
  }

  return new Date(adjusted);
}

function getNextServiceStart(now: Date) {
  const parts = getZonedParts(now, CHURCH_TIME_ZONE);
  const zonedDate = new Date(Date.UTC(parts.year, parts.month - 1, parts.day));
  const weekday = zonedDate.getUTCDay();
  const currentMinutes = parts.hour * 60 + parts.minute + parts.second / 60;
  const serviceMinutes = SERVICE_START_HOUR * 60 + SERVICE_START_MINUTE;
  const daysUntilService =
    weekday === SERVICE_START_WEEKDAY
      ? currentMinutes < serviceMinutes
        ? 0
        : 7
      : (7 - weekday + SERVICE_START_WEEKDAY) % 7;

  return zonedLocalTimeToUtc({
    year: parts.year,
    month: parts.month,
    day: parts.day + daysUntilService,
    hour: SERVICE_START_HOUR,
    minute: SERVICE_START_MINUTE,
    second: 0,
    timeZone: CHURCH_TIME_ZONE,
  });
}

function formatCountdown(now: Date, target: Date, includeSeconds = false) {
  const totalSeconds = Math.max(0, Math.floor((target.getTime() - now.getTime()) / 1000));
  const days = Math.floor(totalSeconds / 86400);
  const hours = Math.floor((totalSeconds % 86400) / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  if (includeSeconds) {
    if (days > 0) {
      return `${days}d ${hours}h ${minutes}m ${seconds}s`;
    }

    if (hours > 0) {
      return `${hours}h ${minutes}m ${seconds}s`;
    }

    return `${minutes}m ${seconds}s`;
  }

  if (days > 0) {
    return `${days}d ${hours}h ${minutes}m`;
  }

  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }

  if (minutes > 0) {
    return includeSeconds ? `${minutes}m ${seconds}s` : `${minutes}m`;
  }

  return `${seconds}s`;
}

function getCountdownProgress(now: Date, target: Date) {
  const current = now.getTime();
  const due = target.getTime();
  const total = Math.max(1, due - current);
  const remaining = Math.max(0, due - current);

  return Math.min(100, Math.max(0, ((total - remaining) / total) * 100));
}

type NextSermonCountdownProps = {
  compact?: boolean;
  className?: string;
};

export function NextSermonCountdown({ compact = false, className }: NextSermonCountdownProps) {
  const [countdown, setCountdown] = useState("checking service time");
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const update = () => {
      const now = new Date();
      const nextService = getNextServiceStart(now);
      setCountdown(formatCountdown(now, nextService, compact));
      setProgress(getCountdownProgress(now, nextService));
    };

    update();
    const timer = window.setInterval(update, 1_000);

    return () => {
      window.clearInterval(timer);
    };
  }, []);

  return (
    <div
      className={`page-hero__countdown${compact ? " page-hero__countdown--compact" : ""}${className ? ` ${className}` : ""}`}
      aria-live="polite"
    >
      <span className="page-hero__countdown-label">Next live sermon</span>
      {compact ? (
        <strong>Starts in {countdown}</strong>
      ) : (
        <>
          <strong>Starts in {countdown}</strong>
          <span>Sundays at 11:00 AM Central</span>
          <div className="page-hero__countdown-bar" aria-hidden="true">
            <span className="page-hero__countdown-fill" style={{ width: `${progress}%` }} />
          </div>
        </>
      )}
    </div>
  );
}
