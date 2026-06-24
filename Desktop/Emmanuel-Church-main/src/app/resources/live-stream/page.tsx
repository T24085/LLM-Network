import Link from "next/link";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { ArrowRightIcon } from "@/components/icons";
import { site } from "@/data/site";

export default function LiveStreamPage() {
  return (
    <>
      <PageHero
        eyebrow="Resources"
        title="Live Stream"
        description="Watch Emmanuel Church live through the online.church platform."
        action={{ label: "Open live stream", href: site.onlineChurch, external: true }}
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Watch"
          title="The live platform and the sermon archive."
          description="This page keeps the live destination front and center while leaving room for future embedding or a custom video pipeline."
        />

        <div className="resource-grid">
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Live</p>
            <h3>Online Church Platform</h3>
            <p>The current destination for Sunday services.</p>
            <a
              className="resource-card__action"
              href={site.onlineChurch}
              target="_blank"
              rel="noreferrer"
            >
              <ArrowRightIcon className="icon icon--xs" />
              <span>Open platform</span>
            </a>
          </article>
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Archive</p>
            <h3>Sermons</h3>
            <p>Past messages are available from the sermons page.</p>
            <Link className="resource-card__action" href="/resources/sermons">
              <ArrowRightIcon className="icon icon--xs" />
              <span>View sermons</span>
            </Link>
          </article>
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Bible app</p>
            <h3>YouVersion events</h3>
            <p>The church also points worshipers to the Bible app for sermon notes.</p>
            <a className="resource-card__action" href={site.bibleApp} target="_blank" rel="noreferrer">
              <ArrowRightIcon className="icon icon--xs" />
              <span>Open Bible.com</span>
            </a>
          </article>
        </div>
      </SectionShell>
    </>
  );
}
