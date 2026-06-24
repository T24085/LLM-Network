import Link from "next/link";
import { ArrowRightIcon } from "@/components/icons";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";

export default function WeeklySermonStudyGuidesPage() {
  return (
    <>
      <PageHero
        eyebrow="Resources"
        title="Weekly Sermon Study Guides"
        description="A space for message notes, discussion prompts, and future downloadable guides."
        action={{ label: "View sermons", href: "/resources/sermons" }}
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Study"
          title="A place to deepen the week's message."
          description="The route stays available so message notes and study material can be added without changing the structure."
        />
        <div className="resource-grid">
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Next step</p>
            <h3>Message notes</h3>
            <p>Use this route for outlines, group questions, or downloads later on.</p>
            <Link className="resource-card__action" href="/resources/sermons">
              <ArrowRightIcon className="icon icon--xs" />
              <span>View sermons</span>
            </Link>
          </article>
        </div>
      </SectionShell>
    </>
  );
}
