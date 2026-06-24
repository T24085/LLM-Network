import Image from "next/image";
import Link from "next/link";
import { ArrowRightIcon, MailIcon, PhoneIcon } from "@/components/icons";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { site } from "@/data/site";
import { withBasePath } from "@/lib/site-path";
import extremeEncountersCabin from "../../../../Momentum Youth/extreme-encounters-cabin.jpg";
import extremeEncountersGroup from "../../../../Momentum Youth/extreme-encounters-group.jpeg";
import extremeEncountersReading from "../../../../Momentum Youth/extreme-encounters-reading.jpeg";
import extremeEncountersSunset from "../../../../Momentum Youth/extreme-encounters-sunset.png";

const shawnEmail = "shawn.ammons@sonlife.com";
const shawnCell = "316-650-0446";
const shawnCellHref = `tel:${shawnCell.replace(/[^0-9+]/g, "")}`;

const momentumValues = [
  {
    eyebrow: "Scripture",
    title: "Students are grounded in biblical truth.",
    body: "Momentum keeps the Bible at the center so teens hear more than advice and more than hype.",
  },
  {
    eyebrow: "Community",
    title: "Meaningful relationships are part of the ministry.",
    body: "The page frames Momentum as a place where students belong, grow, and are known by leaders.",
  },
  {
    eyebrow: "Discipleship",
    title: "The goal is invitation into real growth.",
    body: "Momentum is presented as a ministry that points students toward commitment, not just attendance.",
  },
  {
    eyebrow: "Mission",
    title: "Students are invited to make a difference.",
    body: "The live page calls for volunteers and training around the vision and values of Momentum.",
  },
];

const momentumCards = [
  {
    eyebrow: "More information",
    title: "Momentum Youth is a core part of Connect.",
    body: "The public site places Momentum Youth directly in the main navigation, not in a hidden submenu.",
    action: {
      label: "Contact the office",
      href: "/contact",
    },
  },
  {
    eyebrow: "Extreme Kansas Camp",
    title: "Middle school students attend camp at Milford Lake.",
    body: "The live page points students to Extreme Kansas Camp as a key part of the Momentum rhythm.",
    action: {
      label: "Open Extreme Encounters",
      href: "https://www.extremeencounters.org/",
      external: true,
    },
  },
  {
    eyebrow: "Stay up-to-date",
    title: "Use the church calendar for current events and rhythms.",
    body: "If a family needs the broader schedule, the calendar is the best public source for church-wide dates.",
    action: {
      label: "View the calendar",
      href: "/resources/church-calendar",
    },
  },
  {
    eyebrow: "Volunteer team",
    title: "Training is available for people who want to serve.",
    body: "The live page asks interested people to contact the office about upcoming training to learn the vision and values of Momentum.",
    action: {
      label: "Ask about training",
      href: "/contact",
    },
  },
];

const momentumGallery = [
  {
    src: extremeEncountersGroup,
    alt: "Extreme Encounters camp group photo",
    className: "momentum-gallery__item--wide",
  },
  {
    src: extremeEncountersReading,
    alt: "Students reading together under a tree at camp",
    className: "momentum-gallery__item--portrait",
  },
  {
    src: extremeEncountersCabin,
    alt: "Cabin building at Extreme Encounters",
    className: "momentum-gallery__item--landscape",
  },
  {
    src: extremeEncountersSunset,
    alt: "Students gathered at sunset during camp",
    className: "momentum-gallery__item--wide",
  },
];

export default function MomentumYouthPage() {
  return (
    <>
      <PageHero
        eyebrow="Connect"
        title="A student ministry with room for faith to move."
        description="Momentum Youth serves middle and high school students through teaching, community, and discipleship."
        action={{ label: "Email Pastor Shawn", href: `mailto:${shawnEmail}`, external: true }}
        actionDetail={
          <div className="page-hero__countdown page-hero__countdown--contact">
            <div className="page-hero__countdown-photo">
              <Image
                src={withBasePath("/staff/Shawn-Ammons-Youth-Pastor.png")}
                alt="Pastor Shawn Ammons"
                fill
                sizes="56px"
                className="cover-image"
              />
            </div>
            <div className="page-hero__countdown-copy">
              <span className="page-hero__countdown-label">Momentum Youth</span>
              <strong>{shawnCell}</strong>
              <span>{shawnEmail}</span>
            </div>
          </div>
        }
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Overview"
          title="Students shaped by the gospel, not just entertained by church."
          description="Momentum Youth is the church's primary student ministry, built to give teenagers biblical truth, meaningful relationships, and a clear invitation into discipleship."
        />

        <div className="split-grid">
          <article className="surface-card">
            <div className="surface-card__body content-copy momentum-overview__copy">
              <p>
                Momentum Youth serves middle and high school students and is positioned as a core part of church
                life rather than a side offering.
              </p>
              <p>
                The live page also includes a direct invitation for people who want to make a difference:
                contact the office about an upcoming training to learn the vision and values of Momentum.
              </p>
              <p>
                The ministry is designed to help students grow in Scripture, in community, and in purpose.
              </p>

              <div className="momentum-overview__actions">
                <a className="button button--gold button--small" href={`mailto:${shawnEmail}`}>
                  <MailIcon className="icon icon--xs" />
                  <span>Contact Pastor Shawn</span>
                </a>
                <a className="button button--light button--small" href={shawnCellHref}>
                  <PhoneIcon className="icon icon--xs" />
                  <span>Call {shawnCell}</span>
                </a>
              </div>
            </div>
          </article>

          <article className="surface-card momentum-feature-card">
            <div className="momentum-feature-card__inner">
              <p className="eyebrow eyebrow--small">What Momentum emphasizes</p>
              <div className="momentum-feature-card__rail">
                <span>Middle School</span>
                <span>High School</span>
                <span>Biblical Teaching</span>
                <span>Community</span>
                <span>Discipleship</span>
                <span>Mission</span>
              </div>
              <p>
                A student ministry designed to keep teenagers rooted in Scripture and connected to the church
                family around them.
              </p>
            </div>
          </article>
        </div>

        <div className="resource-grid momentum-values">
          {momentumValues.map((item) => (
            <article key={item.title} className="resource-card">
              <p className="eyebrow eyebrow--small">{item.eyebrow}</p>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Camp & community"
          title="Scenes from Extreme Encounters."
          description="Momentum Youth points students toward camp as one of the ministry's anchor experiences, and these photos add some of that energy to the page."
        />

        <div className="momentum-gallery">
          {momentumGallery.map((image) => (
            <article key={image.alt} className={`surface-card momentum-gallery__item ${image.className}`}>
              <div className="momentum-gallery__media">
                <Image
                  src={withBasePath(image.src)}
                  alt={image.alt}
                  fill
                  sizes="(max-width: 1080px) 100vw, 50vw"
                  className="momentum-gallery__image"
                />
              </div>
            </article>
          ))}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Leadership"
          title="For more information, contact Pastor Shawn Ammons."
          description="The live page lists Shawn's cell number and email, and points interested volunteers toward upcoming training."
        />

        <div className="resource-grid">
          <article className="resource-card momentum-contact-card">
            <p className="eyebrow eyebrow--small">Pastor</p>
            <h3>Shawn Ammons</h3>
            <p>Youth pastor for Momentum Youth.</p>
            <a className="resource-card__action" href={shawnCellHref}>
              <PhoneIcon className="icon icon--xs" />
              <span>Cell {shawnCell}</span>
            </a>
          </article>
          <article className="resource-card momentum-contact-card">
            <p className="eyebrow eyebrow--small">Email</p>
            <h3>shawn.ammons@sonlife.com</h3>
            <p>Direct email from the live Momentum Youth page.</p>
            <a className="resource-card__action" href={`mailto:${shawnEmail}`}>
              <MailIcon className="icon icon--xs" />
              <span>Email Shawn</span>
            </a>
          </article>
          <article className="resource-card momentum-contact-card">
            <p className="eyebrow eyebrow--small">Office</p>
            <h3>Emmanuel Church</h3>
            <p>{site.address}</p>
            <Link className="resource-card__action" href="/contact">
              <ArrowRightIcon className="icon icon--xs" />
              <span>Contact the office</span>
            </Link>
          </article>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="More information"
          title="The live site points students and volunteers to a few key destinations."
          description="These are the main public touchpoints from the Momentum Youth page."
        />

        <div className="resource-grid">
          {momentumCards.map((card) => (
            <article key={card.title} className="resource-card momentum-link-card">
              <p className="eyebrow eyebrow--small">{card.eyebrow}</p>
              <h3>{card.title}</h3>
              <p>{card.body}</p>
              <a
                className="resource-card__action"
                href={card.action.href}
                target={card.action.external ? "_blank" : undefined}
                rel={card.action.external ? "noreferrer" : undefined}
              >
                <ArrowRightIcon className="icon icon--xs" />
                <span>{card.action.label}</span>
              </a>
            </article>
          ))}
        </div>
      </SectionShell>

      <a
        className="momentum-fab"
        href="https://www.extremeencounters.org/"
        target="_blank"
        rel="noreferrer"
        aria-label="Open Extreme Encounters"
      >
        <span>Extreme Encounters</span>
        <ArrowRightIcon className="icon icon--xs" />
      </a>
    </>
  );
}
