import Image from "next/image";
import Link from "next/link";
import { ArrowRightIcon, MailIcon, PhoneIcon } from "@/components/icons";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { site } from "@/data/site";
import { withBasePath } from "@/lib/site-path";
import preschoolCrafts from "../../../../Emmanuel Preschool/04eeb886-3cfe-4ddc-9898-06c1d298d88d.png";
import preschoolClassroom from "../../../../Emmanuel Preschool/93cd6249-c99d-4f38-979c-a8eb4951ac15.jpg";
import preschoolLogo from "../../../../Emmanuel Preschool/c3b52863-0605-4eab-bad9-07d9bf181c66.png";
import preschoolCalendar from "../../../../Emmanuel Preschool/f2dc041b-e023-42fa-a285-41b3575f7b31.png";

const preschoolEmail = "preschool@ecabilene.org";

const classOptions = [
  {
    eyebrow: "2 day class",
    title: "Tuesday / Thursday AM",
    detail: "8:00-11:00 AM",
    price: "$80/month",
  },
  {
    eyebrow: "3 day class",
    title: "Monday / Wednesday / Friday AM",
    detail: "8:00-11:00 AM",
    price: "$100/month",
  },
  {
    eyebrow: "5 day class",
    title: "Monday-Friday AM",
    detail: "12:00-3:00 PM",
    price: "$150/month",
  },
];

const missionCards = [
  {
    eyebrow: "Christ-centered",
    title: "Bible themes woven into the classroom.",
    body: "The preschool includes topics from the Old and New Testament, with emphasis on one God, Jesus as His son, and Jesus sent as our rescuer.",
  },
  {
    eyebrow: "Whole-child growth",
    title: "Academic and social/emotional skills matter together.",
    body: "The program gives children the foundation they need for kindergarten while helping them grow in confidence, communication, and relationships.",
  },
  {
    eyebrow: "Licensed care",
    title: "KDHE licensed and standards-minded.",
    body: "Emmanuel Preschool adheres to the standards set by Kansas licensing and keeps safety, structure, and development at the center of the day.",
  },
];

const policyCards = [
  {
    eyebrow: "Open to all",
    title: "Families from every background are welcome.",
    body: "The preschool is open to all children regardless of race, color, creed, religion, national origin, ancestry, physical handicap, or sex.",
  },
  {
    eyebrow: "Readiness",
    title: "Children must be 3 and potty-trained.",
    body: "Every child must be at least 3 years old prior to attendance and must be potty-trained before starting.",
  },
  {
    eyebrow: "Health records",
    title: "Forms, exam, and immunizations are required.",
    body: "Each child must have a medical examination within 6 months of school starting and updated immunization records signed and on file.",
  },
  {
    eyebrow: "Enrollment fee",
    title: "$25 nonrefundable fee holds the spot.",
    body: "Applications are accepted once the required forms are received. Class size is limited to 10 children per class, and other applications are placed on a waiting list.",
  },
  {
    eyebrow: "Program rules",
    title: "Dismissal policy follows the live site copy.",
    body: "The preschool reserves the right to dismiss a child if they are consistently incompatible with other children or if monthly tuition is not paid on time.",
  },
];

export default function EmmanuelPreschoolPage() {
  return (
    <>
      <a
        className="preschool-floating-form button button--gold"
        href="https://emmanuel.fellowshiponego.com/external/form/79f34db5-a551-42f4-a93a-17019fe114b7"
        target="_blank"
        rel="noreferrer"
      >
        <span>Enrollment Form</span>
        <ArrowRightIcon className="icon icon--sm" />
      </a>

      <PageHero
        eyebrow="Connect"
        title="Christ-centered preschool with a firm academic foundation."
        description="Emmanuel Preschool serves children ages 3-5 with early learning, spiritual formation, and the daily rhythms that prepare them for kindergarten."
        action={{ label: "Email the preschool", href: `mailto:${preschoolEmail}` }}
        actionDetail={
          <div className="page-hero__countdown page-hero__countdown--contact">
            <div className="page-hero__countdown-photo">
              <Image
                src={withBasePath("/staff/Rachel-Bishop-Kid-s-Pastor-Preschool-Director.png")}
                alt="Rachel Bishop"
                fill
                sizes="56px"
                className="cover-image"
              />
            </div>
            <div className="page-hero__countdown-copy">
              <span className="page-hero__countdown-label">2025-2026</span>
              <strong>Enrollment has begun</strong>
              <span>Contact Rachel Bishop or Marie Malo at (785) 263-3342.</span>
            </div>
          </div>
        }
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Overview"
          title="A Christ-centered start for young learners."
          description="Emmanuel's Preschool is a ministry of Emmanuel Church whose goal is to provide a Christ-centered and academic setting for children ages 3-5 and give them a firm foundation for kindergarten."
        />

        <div className="split-grid">
          <article className="surface-card">
            <div className="surface-card__body content-copy preschool-overview__copy">
              <p>
                Emmanuel's Preschool includes topics from the Old and New Testament, with an emphasis on the
                truth that we have one God, that Jesus is His son, and that Jesus was sent to be our rescuer.
              </p>
              <p>
                The program also places equal importance on giving each child the academic and social/emotional
                skills needed to help them be successful in kindergarten.
              </p>
              <p>
                Enrollment is open for the current school year. The preschool office can help with forms,
                questions, and next steps.
              </p>

              <div className="preschool-overview__actions">
                <a className="button button--gold button--small" href={`mailto:${preschoolEmail}`}>
                  <MailIcon className="icon icon--xs" />
                  <span>Email preschool</span>
                </a>
                <Link className="button button--light button--small" href="/our-staff">
                  <span>View staff</span>
                  <ArrowRightIcon className="icon icon--xs" />
                </Link>
              </div>
            </div>
          </article>

          <article className="surface-card preschool-hero-card">
            <div className="preschool-hero-card__media">
              <Image
                src={preschoolLogo}
                alt="Emmanuel Preschool logo collage"
                fill
                priority
                sizes="(max-width: 1080px) 100vw, 48vw"
                className="preschool-hero-card__image"
              />
              <div className="preschool-hero-card__overlay">
                <p className="eyebrow eyebrow--small">Classroom life</p>
                <strong>Faith, learning, and play in one rhythm.</strong>
              </div>
            </div>
          </article>
        </div>

        <div className="resource-grid preschool-facts">
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Ages</p>
            <h3>3-5 years old</h3>
            <p>The preschool is built for children who are ready for an early-learning classroom experience.</p>
          </article>
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">License</p>
            <h3>KDHE licensed</h3>
            <p>The school follows the standards set by Kansas licensing.</p>
          </article>
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Class size</p>
            <h3>10 children maximum</h3>
            <p>Applications beyond the limit are placed on a waiting list.</p>
          </article>
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Daily rhythm</p>
            <h3>Structured and playful</h3>
            <p>Circle time, small groups, snack, music and movement, and recreation shape the day.</p>
          </article>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Gallery"
          title="A glimpse into the preschool classroom."
          description="The shared photos capture the activity, color, and attention to detail that define the preschool environment."
        />

        <div className="preschool-gallery">
          <figure className="surface-card preschool-gallery__item preschool-gallery__item--lead">
            <Image
              src={preschoolCrafts}
              alt="Children gathered around a classroom activity table"
              fill
              sizes="(max-width: 1080px) 100vw, 60vw"
              className="preschool-gallery__image"
            />
          </figure>

          <div className="preschool-gallery__stack">
            <figure className="surface-card preschool-gallery__item">
              <Image
                src={preschoolCalendar}
                alt="Children learning in front of a classroom calendar and wall display"
                fill
                sizes="(max-width: 1080px) 100vw, 32vw"
                className="preschool-gallery__image"
              />
            </figure>
            <figure className="surface-card preschool-gallery__item">
              <Image
                src={preschoolClassroom}
                alt="Children and a teacher posing together with classroom crafts"
                fill
                sizes="(max-width: 1080px) 100vw, 32vw"
                className="preschool-gallery__image"
              />
            </figure>
          </div>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Mission & services"
          title="The preschool day is built around learning, formation, and safety."
          description="All classes are taught in a way that encourages individual and group activities, structured learning, free play, creativity, imagination, social development, and safety."
        />

        <div className="resource-grid">
          {missionCards.map((card) => (
            <article key={card.title} className="resource-card">
              <p className="eyebrow eyebrow--small">{card.eyebrow}</p>
              <h3>{card.title}</h3>
              <p>{card.body}</p>
            </article>
          ))}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Classes"
          title="Three morning class options are currently listed."
          description="These options reflect the current preschool page, including the nonrefundable enrollment fee and monthly tuition."
        />

        <div className="resource-grid">
          {classOptions.map((option) => (
            <article key={option.eyebrow} className="resource-card preschool-class-card">
              <p className="eyebrow eyebrow--small">{option.eyebrow}</p>
              <h3>{option.title}</h3>
              <p>{option.detail}</p>
              <strong className="preschool-class-card__price">{option.price}</strong>
            </article>
          ))}
          <article className="resource-card preschool-class-card">
            <p className="eyebrow eyebrow--small">Enrollment fee</p>
            <h3>$25 nonrefundable</h3>
            <p>The fee holds your child's spot once the required paperwork has been received.</p>
            <strong className="preschool-class-card__price">Waiting list applies after 10 students</strong>
          </article>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Admissions"
          title="Policies are simple, direct, and already in use."
          description="These are the current enrollment policies and contact points listed for Emmanuel Preschool."
        />

        <div className="resource-grid">
          {policyCards.map((card) => (
            <article key={card.title} className="resource-card">
              <p className="eyebrow eyebrow--small">{card.eyebrow}</p>
              <h3>{card.title}</h3>
              <p>{card.body}</p>
            </article>
          ))}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Contact"
          title="For more information, contact the preschool office."
          description="Rachel Bishop directs the preschool, and Marie Malo serves as the preschool teacher."
        />

        <div className="resource-grid">
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Director</p>
            <h3>Rachel Bishop</h3>
            <p>Preschool director and Kids pastor.</p>
            <a className="resource-card__action" href={`tel:${site.phone.replace(/[^0-9+]/g, "")}`}>
              <PhoneIcon className="icon icon--xs" />
              <span>{site.phone}</span>
            </a>
          </article>
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Teacher</p>
            <h3>Marie Malo</h3>
            <p>Preschool teacher and classroom support.</p>
            <a className="resource-card__action" href={`mailto:${preschoolEmail}`}>
              <MailIcon className="icon icon--xs" />
              <span>{preschoolEmail}</span>
            </a>
          </article>
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Office</p>
            <h3>Emmanuel Church</h3>
            <p>{site.address}</p>
            <Link className="resource-card__action" href="/contact">
              <ArrowRightIcon className="icon icon--xs" />
              <span>View contact page</span>
            </Link>
          </article>
        </div>
      </SectionShell>
    </>
  );
}
