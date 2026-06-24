import Link from "next/link";
import { ArrowRightIcon, CalendarIcon, MailIcon, PhoneIcon } from "@/components/icons";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { site } from "@/data/site";

const rachelEmail = "rbishop@ecabilene.org";
const rachelPhoneHref = `tel:${site.phone.replace(/[^0-9+]/g, "")}`;

const blastRhythm = [
  {
    eyebrow: "Season",
    title: "September through November, then January through April.",
    body: "B.L.A.S.T. follows the school-year rhythm so Wednesday nights stay connected to the church calendar and the family schedule.",
  },
  {
    eyebrow: "Time",
    title: "Classes begin at 6:30 pm and end at 7:30 pm.",
    body: "All ages gather during the same window so families can arrive once, settle in, and move through the night together.",
  },
  {
    eyebrow: "Location",
    title: "Children finish in the Emmanuel Kids Wing.",
    body: "Pickup is handled where kids already know the space and leaders can send them home in an orderly way.",
  },
  {
    eyebrow: "Sunday tie-in",
    title: "Children's Church and family care are part of the same rhythm.",
    body: "The ministry is designed to support children during both Sunday services and to give parents a private place to care for little ones.",
  },
];

const blastActivities = [
  {
    eyebrow: "Music",
    title: "Worship time opens the night.",
    body: "Children experience God through singing and a shared time of praise before the lesson and activities begin.",
  },
  {
    eyebrow: "Lesson",
    title: "Interactive teaching keeps the night engaging.",
    body: "The ministry uses age-appropriate lessons so children can hear truth in a way that is simple and memorable.",
  },
  {
    eyebrow: "Play",
    title: "Games and crafts are built into the evening.",
    body: "B.L.A.S.T. gives kids room to move, make, and enjoy the night while staying inside a gospel-shaped rhythm.",
  },
  {
    eyebrow: "Groups",
    title: "Small-group time closes the night.",
    body: "The last part of the evening helps kids connect with leaders and process what they learned together.",
  },
];

const ageGroups = [
  {
    eyebrow: "Nursery",
    title: "Room 102",
    body: "6 weeks to 2 years old.",
  },
  {
    eyebrow: "Pre-K",
    title: "Rooms 101 and 103",
    body: "Ages 3-5 years.",
  },
  {
    eyebrow: "Elementary",
    title: "Worship Center, then kids hall",
    body: "Kids begin together, then split into age groups with small-group time at the end.",
  },
];

const familyCare = [
  {
    eyebrow: "Children's Church",
    title: "Both Sunday services",
    body: "Children participate in praise and worship and hear a lesson tailored for them during both services every week.",
  },
  {
    eyebrow: "Nursing moms",
    title: "Room 210",
    body: "A private room where parents can watch the live stream of each service with a little one.",
  },
  {
    eyebrow: "Contact",
    title: "Rachel Bishop",
    body: "Children's Pastor and Preschool Director who helps families find the right room and the right next step.",
  },
];

const nextSteps = [
  {
    eyebrow: "Kids",
    title: "Open Emmanuel Kids",
    body: "Review Sunday rhythms, check-in details, and family guidance for children from nursery through elementary.",
    href: "/connect/emmanuel-kids",
  },
  {
    eyebrow: "Students",
    title: "Open Momentum Youth",
    body: "See how middle and high school students connect through teaching, community, and discipleship.",
    href: "/connect/momentum-youth",
  },
  {
    eyebrow: "Calendar",
    title: "Stay up to date",
    body: "Use the church calendar for current Wednesday nights, seasonal breaks, and church-wide events.",
    href: "/resources/church-calendar",
  },
];

export default function WednesdayNightBlastPage() {
  return (
    <>
      <PageHero
        eyebrow="Connect"
        title='Wednesday Night "B.L.A.S.T."'
        description="A weekly midweek gathering for kids and families that keeps the church's Wednesday rhythm clear, joyful, and easy to follow."
        action={{ label: "View calendar", href: site.calendarHref, external: true }}
        actionDetail={
          <div className="page-hero__countdown">
            <span className="page-hero__countdown-label">Wednesday nights</span>
            <strong>6:30-7:30 pm</strong>
            <span>September-November and January-April.</span>
          </div>
        }
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Overview"
          title="A family night with a clear midweek anchor."
          description="B.L.A.S.T. is built to give children a place to learn, sing, play, and grow while parents have a simple Wednesday rhythm to follow."
        />

        <div className="split-grid">
          <article className="surface-card">
            <div className="surface-card__body content-copy blast-overview__copy">
              <p>
                The B.L.A.S.T. begins with classes for all ages from 6:30-7:30 pm. The goal is not
                to fill a night with noise, but to create a weekly gathering that helps kids
                experience God in age-appropriate ways.
              </p>
              <p>
                Children move through music and worship time, interactive lessons, games, crafts,
                and small-group time. It is a simple structure, but it gives Wednesday nights a
                consistent shape that families can trust.
              </p>
              <div className="blast-overview__actions">
                <a className="button button--gold button--small" href={`mailto:${rachelEmail}`}>
                  <MailIcon className="icon icon--xs" />
                  <span>Email Rachel Bishop</span>
                </a>
                <a className="button button--light button--small" href={rachelPhoneHref}>
                  <PhoneIcon className="icon icon--xs" />
                  <span>Call the office</span>
                </a>
              </div>
            </div>
          </article>

          <article className="surface-card blast-feature-card">
            <div className="blast-feature-card__inner">
              <p className="eyebrow eyebrow--small">What Wednesday feels like</p>
              <div className="blast-feature-card__list">
                {blastActivities.map((item) => (
                  <div key={item.title} className="blast-feature-card__item">
                    <p className="eyebrow eyebrow--small">{item.eyebrow}</p>
                    <h3>{item.title}</h3>
                    <p>{item.body}</p>
                  </div>
                ))}
              </div>
            </div>
          </article>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Schedule"
          title="The Wednesday rhythm is easy to follow."
          description="These are the essentials families need when they arrive on Wednesday night."
        />

        <div className="resource-grid">
          {blastRhythm.map((item) => (
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
          eyebrow="Age groups"
          title="Each room is set up for a specific age range."
          description="Families can drop children in the correct room quickly and know where pickup will happen at the end of the night."
        />

        <div className="resource-grid">
          {ageGroups.map((group) => (
            <article key={group.title} className="resource-card blast-age-card">
              <p className="eyebrow eyebrow--small">{group.eyebrow}</p>
              <h3>{group.title}</h3>
              <p>{group.body}</p>
            </article>
          ))}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Family care"
          title="The whole evening is designed with families in mind."
          description="Children's Church, a nursing moms room, and a clear contact person keep the night accessible for parents and caregivers."
        />

        <div className="resource-grid">
          {familyCare.map((item) => (
            <article key={item.title} className="resource-card blast-care-card">
              <p className="eyebrow eyebrow--small">{item.eyebrow}</p>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Next steps"
          title="Use B.L.A.S.T. alongside the rest of the church rhythm."
          description="Families moving through Wednesday nights usually need one of these additional pages too."
        />

        <div className="resource-grid">
          {nextSteps.map((step) => (
            <article key={step.title} className="resource-card blast-link-card">
              <p className="eyebrow eyebrow--small">{step.eyebrow}</p>
              <h3>{step.title}</h3>
              <p>{step.body}</p>
              <Link className="resource-card__action" href={step.href}>
                <ArrowRightIcon className="icon icon--xs" />
                <span>Open page</span>
              </Link>
            </article>
          ))}
        </div>

        <div className="blast-inline-note">
          <CalendarIcon className="icon icon--sm" />
          <div>
            <strong>Check the calendar for current Wednesday nights and seasonal breaks.</strong>
            <p>
              The public calendar is the best place to confirm what is happening this week.
            </p>
          </div>
        </div>
      </SectionShell>
    </>
  );
}
