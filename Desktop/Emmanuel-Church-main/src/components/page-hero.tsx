import Link from "next/link";
import type { ReactNode } from "react";
import { ArrowRightIcon } from "./icons";

type PageHeroProps = {
  eyebrow: string;
  title: string;
  description: string;
  mediaLayout?: "split" | "full";
  layoutClassName?: string;
  action?: {
    label: string;
    href: string;
    external?: boolean;
  };
  actionDetail?: ReactNode;
  media?: ReactNode;
};

export function PageHero({
  eyebrow,
  title,
  description,
  mediaLayout = "split",
  layoutClassName,
  action,
  actionDetail,
  media,
}: PageHeroProps) {
  const hasMedia = Boolean(media);
  const isFullBleedMedia = hasMedia && mediaLayout === "full";

  return (
    <section className={`page-hero${isFullBleedMedia ? " page-hero--media-full" : ""}`}>
      <div
        className={`site-shell page-hero__inner${
          hasMedia ? " page-hero__inner--media" : ""
        }${isFullBleedMedia ? " page-hero__inner--media-full" : ""}`}
      >
        <div
          className={`page-hero__layout${
            isFullBleedMedia ? " page-hero__layout--media-full" : ""
          }${layoutClassName ? ` ${layoutClassName}` : ""}`}
        >
          <div
            className={`page-hero__content${
              isFullBleedMedia ? " page-hero__content--media-full" : ""
            }`}
          >
            <p className="eyebrow">{eyebrow}</p>
            <h1>{title}</h1>
            <p>{description}</p>
          </div>
          {media ? (
            <div
              className={`page-hero__media${
                isFullBleedMedia ? " page-hero__media--full" : ""
              }`}
            >
              {media}
            </div>
          ) : null}
        </div>
        {action ? (
          <div className={`page-hero__actions${isFullBleedMedia ? " page-hero__actions--full" : ""}`}>
            <Link
              href={action.href}
              target={action.external ? "_blank" : undefined}
              rel={action.external ? "noreferrer" : undefined}
              className="section-heading__action page-hero__action"
            >
              <span>{action.label}</span>
              <ArrowRightIcon className="icon icon--sm" />
            </Link>
            {actionDetail ? <div className="page-hero__action-detail">{actionDetail}</div> : null}
          </div>
        ) : null}
      </div>
    </section>
  );
}
