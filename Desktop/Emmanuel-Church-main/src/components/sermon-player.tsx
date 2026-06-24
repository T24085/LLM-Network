"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowRightIcon } from "./icons";

export type SermonPlayerItem = {
  label: string;
  href: string;
  mediaId: number;
  embedSrc: string | null;
  audioUrl?: string | null;
  date?: string | null;
  speaker?: string | null;
  series?: string | null;
  thumbnail?: string | null;
  kind?: "video" | "audio";
};

type SermonPlayerProps = {
  sermons: SermonPlayerItem[];
};

export function SermonPlayer({ sermons }: SermonPlayerProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const active = sermons[activeIndex] ?? sermons[0];

  const hasAudio = Boolean(active?.audioUrl);
  const activeEmbedSrc = useMemo(() => active?.embedSrc || "", [active]);
  const getSermonKey = (sermon: SermonPlayerItem, index: number) =>
    `${sermon.mediaId || "media"}-${sermon.href || "href"}-${index}`;

  return (
    <div className="sermon-player">
      <div className="sermon-player__stage surface-card">
        <div className="sermon-player__media">
          {activeEmbedSrc ? (
            <iframe
              src={activeEmbedSrc}
              title={active?.label || "Sermon video"}
              allow="autoplay; fullscreen; picture-in-picture"
              allowFullScreen
            />
          ) : hasAudio ? (
            <div className="sermon-player__audio-wrap">
              <audio controls src={active?.audioUrl || undefined} />
              <p className="sermon-player__audio-note">Audio recording for this message.</p>
            </div>
          ) : (
            <div className="sermon-player__fallback">
              <p className="eyebrow eyebrow--small">Video unavailable</p>
              <h3>{active?.label}</h3>
              <p>The original sermon page is still available below.</p>
              <a className="button button--gold button--small" href={active?.href} target="_blank" rel="noreferrer">
                <span>Open sermon page</span>
                <ArrowRightIcon className="icon icon--xs" />
              </a>
            </div>
          )}
        </div>

        <div className="sermon-player__meta">
          <div>
            <p className="eyebrow eyebrow--small">Now playing</p>
            <h3>{active?.label}</h3>
            <p>{active?.series || "Emmanuel Church sermon archive"}</p>
          </div>
          <div className="sermon-player__detail">
            {active?.kind ? <span>{active.kind === "video" ? "Video sermon" : "Audio sermon"}</span> : null}
            {active?.date ? <span>{active.date}</span> : null}
            {active?.speaker ? <span>{active.speaker}</span> : null}
          </div>
          <div className="sermon-player__actions">
            <Link className="text-link text-link--secondary" href={active?.href || "#"} target="_blank" rel="noreferrer">
              <span>Open original page</span>
              <ArrowRightIcon className="icon icon--xs" />
            </Link>
          </div>
        </div>
      </div>

      <div className="sermon-player__playlist">
        {sermons.map((sermon, index) => {
          const selected = index === activeIndex;
          return (
            <button
              key={getSermonKey(sermon, index)}
              type="button"
              className={`sermon-player__item ${selected ? "sermon-player__item--active" : ""}`.trim()}
              onClick={() => setActiveIndex(index)}
              aria-pressed={selected}
            >
              <div className="sermon-player__thumb">
                {sermon.thumbnail ? <img src={sermon.thumbnail} alt="" /> : null}
              </div>
              <div className="sermon-player__copy">
                <span className="sermon-player__tag">
                  {sermon.kind === "video" ? "Video" : "Audio"}
                </span>
                <strong>{sermon.label}</strong>
                <span>{sermon.date || sermon.series || "Emmanuel Church"}</span>
              </div>
              <ArrowRightIcon className="icon icon--sm" />
            </button>
          );
        })}
      </div>
    </div>
  );
}
