import Link from "next/link";
import Image from "next/image";
import { ArrowRightIcon } from "@/components/icons";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { site } from "@/data/site";
import { withBasePath } from "@/lib/site-path";

export default function OnlineGivingPage() {
  return (
    <>
      <a
        className="giving-fab"
        href={site.givingHref}
        target="_blank"
        rel="noreferrer"
        aria-label="Open the donation page"
      >
        <span>Donate Now</span>
        <ArrowRightIcon className="icon icon--xs" />
      </a>

      <PageHero
        eyebrow="Resources"
        title="Online Giving"
        description="Give through Fellowship One Giving."
        action={{ label: "Give online", href: site.givingHref, external: true }}
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Giving"
          title="A clear way to give."
          description="Fellowship One Giving is Emmanuel's current online portal. Give once, manage your account, and choose whether to cover processing fees."
        />
        <div className="giving-showcase">
          <figure className="giving-showcase__media">
            <Image
              src={withBasePath("/images/giving/giving-jesus.png")}
              alt="Jesus giving bread to a child"
              fill
              sizes="(max-width: 1080px) 100vw, 58vw"
              className="cover-image"
              priority
            />
          </figure>

          <aside className="giving-showcase__copy">
            <p className="eyebrow">Online giving</p>
            <h3>Generosity is part of discipleship.</h3>
            <p>
              Use Fellowship One Giving for one-time gifts, recurring support, and account
              access in one place.
            </p>
            <div className="hero__actions">
              <a className="button button--gold" href={site.givingHref} target="_blank" rel="noreferrer">
                Give now
              </a>
              <Link className="button button--light" href="/contact">
                <span>Need help?</span>
              </Link>
            </div>
          </aside>
        </div>
        <div className="resource-grid">
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Donation portal</p>
            <h3>Fellowship One Giving</h3>
            <p>The church's current online giving portal.</p>
            <a className="resource-card__action" href={site.givingHref} target="_blank" rel="noreferrer">
              <ArrowRightIcon className="icon icon--xs" />
              <span>Make a donation</span>
            </a>
          </article>
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Support</p>
            <h3>Need help?</h3>
            <p>Reach the office for login help, receipts, or support from the right staff member.</p>
            <Link className="resource-card__action" href="/contact">
              <ArrowRightIcon className="icon icon--xs" />
              <span>Contact us</span>
            </Link>
          </article>
        </div>
      </SectionShell>
    </>
  );
}
