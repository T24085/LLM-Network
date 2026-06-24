"use client";

import Image, { type StaticImageData } from "next/image";
import { useState } from "react";
import { withBasePath } from "@/lib/site-path";

type ValueFlipCardProps = {
  title: string;
  summary: string;
  backTitle: string;
  backBody: string;
  references: string;
  frontImage?: string | StaticImageData;
  frontImageAlt?: string;
};

export function ValueFlipCard({
  title,
  summary,
  backTitle,
  backBody,
  references,
  frontImage,
  frontImageAlt,
}: ValueFlipCardProps) {
  const [flipped, setFlipped] = useState(false);

  return (
    <button
      type="button"
      className={`value-card value-card--flip${flipped ? " value-card--flip--active" : ""}`.trim()}
      onClick={() => setFlipped((current) => !current)}
      aria-pressed={flipped}
      aria-label={`${title} value card. ${flipped ? "Showing back." : "Showing front."} Click to flip.`}
    >
      <span className="value-card__stage">
        <span className="value-card__inner">
          <span className="value-card__face value-card__face--front">
            {frontImage ? (
              <span className="value-card__visual">
                <Image
                  src={typeof frontImage === "string" ? withBasePath(frontImage) : frontImage}
                  alt={frontImageAlt ?? title}
                  fill
                  sizes="(max-width: 1080px) 100vw, 25vw"
                  className="value-card__visual-image"
                />
              </span>
            ) : null}
            <span className="value-card__content">
              <span className="eyebrow eyebrow--small">Core value</span>
              <h3>{title}</h3>
              <p>{summary}</p>
            </span>
            <span className="value-card__hint">Tap to read more</span>
          </span>

          <span className="value-card__face value-card__face--back">
            <span className="value-card__content">
              <span className="eyebrow eyebrow--small">{backTitle}</span>
              <h3>{backTitle}</h3>
              <p>{backBody}</p>
              <p className="value-card__references">{references}</p>
            </span>
            <span className="value-card__hint">Tap to return</span>
          </span>
        </span>
      </span>
    </button>
  );
}
