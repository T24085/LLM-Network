import Image from "next/image";
import Link from "next/link";
import { ArrowRightIcon } from "@/components/icons";
import { MediaArchiveBrowser } from "@/components/media-archive-browser";
import { PageHero } from "@/components/page-hero";
import { NextSermonCountdown } from "@/components/next-sermon-countdown";
import { SectionHeading, SectionShell } from "@/components/section";
import type { SermonPlayerItem } from "@/components/sermon-player";
import {
  loadMediaArchivePages,
  mediaArchiveRevalidateSeconds,
  type MediaArchivePage,
} from "@/lib/media-archive";
import { withBasePath } from "@/lib/site-path";
import { sermonArchive, site } from "@/data/site";

export const revalidate = 21600;

function extractMediaId(href: string) {
  const match = href.match(/\/media\/\d+-\d+-(\d+)\//);
  return match ? Number(match[1]) : null;
}

function buildEmbedSrc(thirdPartyId: string | number | null | undefined) {
  if (!thirdPartyId) {
    return null;
  }

  const id = String(thirdPartyId).trim();
  if (!id) {
    return null;
  }

  if (/^\d+$/.test(id)) {
    const params = new URLSearchParams({
      title: "0",
      byline: "0",
      portrait: "0",
      dnt: "1",
    });

    return `https://player.vimeo.com/video/${id}?${params.toString()}`;
  }

  return `https://www.youtube.com/embed/${id}`;
}

async function loadTeachingSeries(): Promise<SermonPlayerItem[]> {
  return Promise.all(
    sermonArchive.map(async (sermon) => {
      const mediaId = extractMediaId(sermon.href);

      if (!mediaId) {
        return {
          label: sermon.label,
          href: sermon.href,
          mediaId: 0,
          embedSrc: null,
          audioUrl: null,
          kind: "audio" as const,
        };
      }

      try {
        const pageResponse = await fetch(sermon.href, {
          next: { revalidate: mediaArchiveRevalidateSeconds },
        });
        const html = await pageResponse.text();
        const widgetMatch = html.match(
          /<script type="application\/json" class="js-react-on-rails-component" data-component-name="MediaWidget" data-dom-id="MediaWidget-react-component-[^"]+">([^<]+)<\/script>/
        );
        const widgetProps = widgetMatch ? (JSON.parse(widgetMatch[1]) as { id?: string }) : {};
        const playerId = widgetProps.id;

        if (!playerId) {
          throw new Error("Missing media player id");
        }

        const response = await fetch(
          `http://mediaplayer.cloversites.com/players/${playerId}?draft=0&media_id=${mediaId}`,
          { next: { revalidate: mediaArchiveRevalidateSeconds } }
        );
        const data = (await response.json()) as {
          media?: Array<{
            title?: string;
            date_string?: string | null;
            speaker?: string | null;
            series?: string | null;
            third_party_id?: string | number | null;
            download_url?: string | null;
            audio?: boolean;
            video?: boolean;
            thumbnails?: { large?: string | null };
          }>;
        };
        const media = data.media?.[0];
        const embedSrc = buildEmbedSrc(media?.third_party_id);

        return {
          label: media?.title || sermon.label,
          href: sermon.href,
          mediaId,
          embedSrc,
          audioUrl: media?.download_url || null,
          date: media?.date_string || null,
          speaker: media?.speaker || null,
          series: media?.series || null,
          thumbnail: media?.thumbnails?.large || null,
          kind: embedSrc ? "video" : "audio",
        };
      } catch {
        return {
          label: sermon.label,
          href: sermon.href,
          mediaId,
          embedSrc: null,
          audioUrl: null,
          kind: "audio",
        };
      }
    })
  );
}

export default async function SermonsPage() {
  const teachingSeries = await loadTeachingSeries();
  const audioSermons = teachingSeries.filter((sermon) => sermon.kind !== "video" || !sermon.embedSrc);
  const mediaPages = (await loadMediaArchivePages()) as MediaArchivePage[];

  return (
    <>
      <PageHero
        eyebrow="Resources"
        title="Sermons"
        description="Watch Emmanuel Church's current video archive inline, with the older teaching series kept below."
        mediaLayout="full"
        action={{ label: "Watch the latest message", href: site.onlineChurch, external: true }}
        actionDetail={<NextSermonCountdown />}
        media={
          <div className="page-hero__media-frame">
            <NextSermonCountdown compact className="page-hero__countdown--overlay" />
            <Image
              src={withBasePath("/images/sermon-on-the-mount-banner.png")}
              alt="The Sermon on the Mount illustration"
              fill
              priority
              sizes="(max-width: 1080px) 100vw, 100vw"
              className="page-hero__media-image"
            />
          </div>
        }
      />

      <div className="sermons-static">
        <SectionShell>
          <SectionHeading
            eyebrow="Media Archive"
            title="The current video archive from Emmanuel Church LIVE."
            description="These are the live archive videos, presented here with the original pagination intact."
          />

          <MediaArchiveBrowser pages={mediaPages} />
        </SectionShell>

        <SectionShell className="section-shell--tight">
          <SectionHeading
            eyebrow="Teaching Series"
            title={`${audioSermons.length} older teaching-series messages remain available.`}
            description="These recordings came from the legacy sermon library and stay available separately from the video archive."
          />

          <details className="audio-archive surface-card">
            <summary>
              <span>Open older archive</span>
              <span>{audioSermons.length} messages</span>
            </summary>
            <div className="audio-archive__body">
              <div className="link-list">
                {audioSermons.map((sermon) => (
                  <a
                    key={sermon.href}
                    className="link-list__item"
                    href={sermon.href}
                    target="_blank"
                    rel="noreferrer"
                  >
                    <div className="link-list__copy">
                      <span className="sermon-player__tag">Audio</span>
                      <h3 className="link-list__title">{sermon.label}</h3>
                      <p>{sermon.date || sermon.series || "Open the original Emmanuel Church sermon page."}</p>
                    </div>
                    <ArrowRightIcon className="icon icon--sm" />
                  </a>
                ))}
              </div>
            </div>
          </details>
        </SectionShell>

        <SectionShell className="section-shell--tight">
          <SectionHeading
            eyebrow="Teaching tools"
            title="Additional resources around the sermon archive."
            description="These are the public destinations Emmanuel uses alongside the sermon library."
          />

          <div className="resource-grid">
            <article className="resource-card">
              <p className="eyebrow eyebrow--small">Latest</p>
              <h3>Emmanuel Church LIVE</h3>
              <p>Open the current online platform for live services and message replay.</p>
              <a
                className="resource-card__action"
                href={site.onlineChurch}
                target="_blank"
                rel="noreferrer"
              >
                <ArrowRightIcon className="icon icon--xs" />
                <span>Open live platform</span>
              </a>
            </article>
            <article className="resource-card">
              <p className="eyebrow eyebrow--small">Notes</p>
              <h3>YouVersion events</h3>
              <p>The church points people to Bible.com for sermon notes and follow-along events.</p>
              <a className="resource-card__action" href={site.bibleApp} target="_blank" rel="noreferrer">
                <ArrowRightIcon className="icon icon--xs" />
                <span>Open Bible.com</span>
              </a>
            </article>
            <article className="resource-card">
              <p className="eyebrow eyebrow--small">Study</p>
              <h3>Weekly sermon study guides</h3>
              <p>Use this route for future message notes, study questions, or downloadable guides.</p>
              <Link className="resource-card__action" href="/resources/weekly-sermon-study-guides">
                <ArrowRightIcon className="icon icon--xs" />
                <span>Open study guides</span>
              </Link>
            </article>
          </div>
        </SectionShell>
      </div>
    </>
  );
}
