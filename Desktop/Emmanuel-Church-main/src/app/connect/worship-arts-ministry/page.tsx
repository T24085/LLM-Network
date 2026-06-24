import Image from "next/image";
import Link from "next/link";
import {
  ArrowRightIcon,
  BookIcon,
  CalendarIcon,
  HeartIcon,
  MailIcon,
  PhoneIcon,
  UsersIcon,
} from "@/components/icons";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { site } from "@/data/site";
import { withBasePath } from "@/lib/site-path";

const marcName = "Pastor Marc Riegel";
const marcPhone = "(785) 263-3342";
const marcPhoneHref = "tel:7852633342";
const marcEmail = "mriegel@ecabilene.org";
const lauraEmail = "lediger@ecabilene.org";

const worshipValues = [
  {
    eyebrow: "Reverence",
    title: "Lead with awe, not performance.",
    body: "The team exists to help the church respond to God with humility, gratitude, and clarity.",
    icon: HeartIcon,
  },
  {
    eyebrow: "Excellence",
    title: "Prepare well and serve with care.",
    body: "Musical and technical leaders give their best so gathered worship stays focused and distraction-free.",
    icon: BookIcon,
  },
  {
    eyebrow: "Teamwork",
    title: "Voices, instruments, and tech serve as one body.",
    body: "Every role matters because worship arts is built around collaboration and shared responsibility.",
    icon: UsersIcon,
  },
  {
    eyebrow: "Formation",
    title: "Every service shapes discipleship.",
    body: "Rehearsals, planning, and service all form people as worshipers before they ever step on stage.",
    icon: CalendarIcon,
  },
];

const worshipModes = [
  {
    eyebrow: "Praise teams",
    title: "Lead the church in Sunday worship.",
    body: "Singers and musicians help guide the congregation through adult and youth worship services.",
  },
  {
    eyebrow: "Tech teams",
    title: "Support sound, screens, lighting, and streaming.",
    body: "Behind-the-scenes volunteers shape the environment so worship stays clear and attentive.",
  },
  {
    eyebrow: "Seasonal choirs",
    title: "Lift the room during key church moments.",
    body: "Choirs gather around the calendar for special Sundays and seasonal worship emphasis.",
  },
];

const worshipSteps = [
  {
    eyebrow: "Step 1",
    title: "Reach out to the ministry team.",
    body: "Start with Pastor Marc or the church office so someone can help you find the right place to serve.",
  },
  {
    eyebrow: "Step 2",
    title: "Talk through your gifts and schedule.",
    body: "The team will help you understand the expectations for singers, musicians, or production volunteers.",
  },
  {
    eyebrow: "Step 3",
    title: "Join rehearsal or training.",
    body: "Worship teams stay sharp through preparation, prayer, and a willingness to learn together.",
  },
  {
    eyebrow: "Step 4",
    title: "Serve consistently and keep growing.",
    body: "The goal is not just filling a slot. The goal is forming leaders who help the church worship well.",
  },
];

export default function WorshipArtsMinistryPage() {
  return (
    <>
      <PageHero
        eyebrow="Connect"
        title="Worship that is visually, vocally, and spiritually disciplined."
        description="Worship Arts Ministry helps Emmanuel gather with reverence through music, production, and choir moments that keep the room centered on Jesus."
        action={{ label: "Email Worship Arts", href: `mailto:${lauraEmail}` }}
        actionDetail={
          <div className="page-hero__countdown">
            <span className="page-hero__countdown-label">For more information</span>
            <strong>{marcName}</strong>
            <span>
              {marcPhone} · {marcEmail}
            </span>
          </div>
        }
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Overview"
          title="Worship is central to Emmanuel's identity."
          description="This ministry is not only about singing. It is about leading the church to respond to God with humility, skill, and confidence."
        />

        <div className="split-grid">
          <article className="surface-card">
            <div className="surface-card__body content-copy">
              <p>
                Worship Arts Ministry keeps the gathered church focused on Jesus through praise teams,
                production support, and seasonal choir moments that strengthen Sunday worship.
              </p>
              <p>
                The work is shaped by reverence, excellence, teamwork, and discipleship. Those values
                are what make the ministry feel more like formation than performance.
              </p>
              <p>
                The team is led by Worship Arts Pastor Laura Ediger, with Pastor Marc Riegel available
                for more information at {marcPhone}.
              </p>

              <div style={{ display: "flex", flexWrap: "wrap", gap: "0.75rem", marginTop: "1.25rem" }}>
                <a className="button button--gold button--small" href={`mailto:${lauraEmail}`}>
                  <MailIcon className="icon icon--xs" />
                  <span>Email Worship Arts</span>
                </a>
                <a className="button button--light button--small" href={marcPhoneHref}>
                  <PhoneIcon className="icon icon--xs" />
                  <span>Call {marcPhone}</span>
                </a>
                <Link className="button button--light button--small" href="/contact">
                  <ArrowRightIcon className="icon icon--xs" />
                  <span>Contact the office</span>
                </Link>
              </div>
            </div>
          </article>

          <article className="surface-card surface-card--light">
            <div className="surface-card__body">
              <div
                style={{
                  position: "relative",
                  aspectRatio: "4 / 5",
                  borderRadius: "var(--radius-md)",
                  overflow: "hidden",
                  marginBottom: "1rem",
                  background: "rgba(24, 33, 43, 0.06)",
                }}
              >
                <Image
                  src={withBasePath("/staff/Laura-Ediger-Worship-Arts-Pastor.png")}
                  alt="Laura Ediger, Worship Arts Pastor"
                  fill
                  sizes="(max-width: 1080px) 100vw, 40vw"
                  style={{ objectFit: "cover" }}
                />
              </div>
              <p className="eyebrow eyebrow--small">Worship Arts Pastor</p>
              <h3>Laura Ediger</h3>
              <p>
                Leads the ministry teams that help Emmanuel worship with clarity, beauty, and
                reverence.
              </p>
              <p className="eyebrow eyebrow--small" style={{ marginTop: "1rem" }}>
                Associate oversight and contact
              </p>
              <p style={{ marginTop: "0.35rem" }}>
                {marcName} · {marcPhone}
              </p>
            </div>
          </article>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Core commitments"
          title="Four priorities shape the way the team leads worship."
          description="These are the values that keep the ministry centered, disciplined, and useful to the gathered church."
        />

        <div className="resource-grid">
          {worshipValues.map((item) => {
            const Icon = item.icon;
            return (
              <article key={item.title} className="resource-card">
                <p className="eyebrow eyebrow--small">{item.eyebrow}</p>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
                <div style={{ marginTop: "1rem", color: "var(--gold-strong)" }}>
                  <Icon className="icon" />
                </div>
              </article>
            );
          })}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Serving lanes"
          title="The live page keeps the ministry structure simple."
          description="There are three main ways to get involved: praise teams, tech teams, and seasonal choirs."
        />

        <div className="resource-grid">
          {worshipModes.map((item) => (
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
          eyebrow="How to join"
          title="Take the next step if you want to sing, play, or serve behind the scenes."
          description="The path is straightforward: reach out, talk through your gifts, train well, and serve consistently."
        />

        <div className="resource-grid">
          {worshipSteps.map((item) => (
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
          eyebrow="Leadership"
          title="Who to contact if you want to get involved."
          description="The ministry stays close to the church office so people can find the right person quickly."
        />

        <div className="resource-grid">
          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Pastor</p>
            <h3>{marcName}</h3>
            <p>Primary contact for Worship Arts Ministry.</p>
            <a className="resource-card__action" href={marcPhoneHref}>
              <PhoneIcon className="icon icon--xs" />
              <span>{marcPhone}</span>
            </a>
            <a className="resource-card__action" href={`mailto:${marcEmail}`}>
              <MailIcon className="icon icon--xs" />
              <span>{marcEmail}</span>
            </a>
          </article>

          <article className="resource-card">
            <p className="eyebrow eyebrow--small">Worship Arts Pastor</p>
            <h3>Laura Ediger</h3>
            <p>Leads worship arts ministry teams and planning.</p>
            <a className="resource-card__action" href={`mailto:${lauraEmail}`}>
              <MailIcon className="icon icon--xs" />
              <span>{lauraEmail}</span>
            </a>
          </article>

          <article className="resource-card">
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
    </>
  );
}
