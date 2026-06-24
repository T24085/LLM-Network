import Link from "next/link";
import { PageHero } from "./page-hero";
import { SectionHeading, SectionShell } from "./section";
import { ArrowRightIcon } from "./icons";

type MinistryPageProps = {
  eyebrow: string;
  title: string;
  description: string;
  highlight: string;
  details: string[];
  cta: {
    label: string;
    href: string;
    external?: boolean;
  };
  secondary?: {
    label: string;
    href: string;
    external?: boolean;
  };
};

export function MinistryPage({
  eyebrow,
  title,
  description,
  highlight,
  details,
  cta,
  secondary,
}: MinistryPageProps) {
  return (
    <>
      <PageHero eyebrow={eyebrow} title={title} description={description} action={cta} />
      <SectionShell>
        <SectionHeading eyebrow="Overview" title={highlight} />
        <div className="content-copy">
          {details.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </div>
        {secondary ? (
          <div style={{ marginTop: "1.5rem" }}>
            <Link
              href={secondary.href}
              target={secondary.external ? "_blank" : undefined}
              rel={secondary.external ? "noreferrer" : undefined}
              className="button button--light"
            >
              <span>{secondary.label}</span>
              <ArrowRightIcon className="icon icon--sm" />
            </Link>
          </div>
        ) : null}
      </SectionShell>
    </>
  );
}
