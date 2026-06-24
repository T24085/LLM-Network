import Image from "next/image";
import Link from "next/link";
import { ArrowRightIcon } from "@/components/icons";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { ministryLinks } from "@/data/site";
import churchMinistriesImage from "../../../Who we are - ABOUT/Church Ministries.png";

export default function ConnectPage() {
  return (
    <>
      <PageHero
        eyebrow="Connect"
        title="The places where church life happens."
        description="From preschool through adult discipleship, Emmanuel's ministries give people a place to belong and a path to grow."
        mediaLayout="full"
        action={{ label: "Plan Your Visit", href: "/contact" }}
        media={
          <div className="page-hero__media-frame">
            <Image
              src={churchMinistriesImage}
              alt="Jesus with a gathered ministry group"
              fill
              priority
              sizes="(max-width: 1080px) 100vw, 42vw"
              className="page-hero__media-image page-hero__media-image--connect"
            />
          </div>
        }
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Ministry map"
          title="Clear pathways for every age and stage."
          description="Each ministry has a clear role: children, students, adults, worship, and midweek gatherings."
        />

        <div className="resource-grid">
          {ministryLinks.map((item) => (
            <article key={item.href} className="resource-card">
              <p className="eyebrow eyebrow--small">Ministry</p>
              <h3>{item.label}</h3>
              <p>{item.description}</p>
              <Link href={item.href} className="resource-card__action">
                Open page <ArrowRightIcon className="icon icon--xs" />
              </Link>
            </article>
          ))}
        </div>
      </SectionShell>
    </>
  );
}
