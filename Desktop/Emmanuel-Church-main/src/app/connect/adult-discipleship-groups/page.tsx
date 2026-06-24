import Image from "next/image";
import Link from "next/link";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { ArrowRightIcon } from "@/components/icons";
import { withBasePath } from "@/lib/site-path";

const avenueCards = [
  {
    title: "LIFE GROUPS",
    eyebrow: "Relationships, discipleship, leadership",
    description:
      "Life Groups are 6-12 people who are doing the Christian life together in three areas: Relationships, Discipleship, and Leadership. The goal is to build relationships, encourage one another, serve, and grow in obedience and maturity through Bible study and prayer. Simply put, they live LIFE together.",
    image: "/images/adult-discipleship/life-groups.jpg",
    imageAlt: "Life Groups discipleship image",
    points: ["Gathering", "Regularly", "Offering", "Understanding and Prayer"],
  },
  {
    title: "TRIADS",
    eyebrow: "Accountability and growth",
    description:
      "Triads are three people (all men or all women) who meet together weekly, monthly, or as scheduled to hold each other accountable for spiritual growth and transformation. The goal is to develop transparent trust in each other around the truth of God's Word.",
    image: "/images/adult-discipleship/triads.jpg",
    imageAlt: "Triads discipleship image",
    points: ["Transparent trust", "Spiritual growth", "Shared accountability"],
  },
  {
    title: "COUPLES CONNECT",
    eyebrow: "Marriage journey",
    description:
      "Couples Connect is a discipleship connection between a young or newly-married couple and an older, more experienced married couple, for the purpose of encouragement and spiritual growth in the marriage journey.",
    image: "/images/adult-discipleship/couples-connect.jpg",
    imageAlt: "Couples Connect discipleship image",
    points: ["Young or newly-married couples", "Older, experienced couples", "Encouragement and growth"],
  },
];

const discipleshipClasses = [
  {
    title: "Common Ground",
    description: "Room 202 - Rebecca Stoffer",
    image: "/images/adult-discipleship/sticky/common-ground.jpg",
  },
  {
    title: "Current Topics",
    description: "Room 211 - Ryan & Sarah Stirtz",
    image: "/images/adult-discipleship/sticky/current-topics.jpg",
  },
  {
    title: "Heart Connections Class",
    description: "Room 205 - Scott Hill",
    image: "/images/adult-discipleship/sticky/heart-connections-class.jpg",
  },
  {
    title: "Kum Join Us Men's Class",
    description: "Room 208 - Rod Osland",
    image: "/images/adult-discipleship/sticky/kum-join-us-mens-class.jpg",
  },
  {
    title: "Ladies Class",
    description: "Room 203 - Mona Koop",
    image: "/images/adult-discipleship/sticky/ladies-class.jpg",
  },
  {
    title: "Faithful Followers",
    description: "Room 204 - Dan Razak",
    image: "/images/adult-discipleship/sticky/faithful-followers.jpg",
  },
  {
    title: "Willing Workers",
    description: "Conference Room - Rod Osland",
    image: "/images/adult-discipleship/sticky/willing-workers.jpg",
  },
  {
    title: "Women's Study",
    description: "Room 201 - Sherry Osland",
    image: "/images/adult-discipleship/sticky/womens-study.jpg",
  },
];

const processSteps = [
  "Contact Joyce Steffen at (785) 280-1258 or at joycebradsteffen@gmail.com",
  "Joyce will help you assess a good place to connect for Discipleship",
  "You'll be introduced to the leader (Discipleship Class, Life Group, and/or Triad)",
  "Joyce will follow up to see how it's going.",
];

export default function AdultDiscipleshipGroupsPage() {
  return (
    <>
      <PageHero
        eyebrow="Connect"
        title="Discipleship at Emmanuel Church: A Great Place to Get Connected"
        description="Part of the Emmanuel Church Vision Statement is to Disciple Believers. In order to do this, we have three main avenues of connection so discipleship can be fostered in the life of a believer."
        action={{ label: "See the process", href: "#process" }}
        actionDetail={
          <span>10am Sunday mornings and off-site groups during the week.</span>
        }
      />

      <SectionShell>
        <SectionHeading
          eyebrow="Overview"
          title="All who attend Emmanuel are encouraged to join one or more of these avenues."
          description="These discipleship paths help people continue to experience God's Sanctifying Grace in a proactive way."
        />

        <article className="surface-card adult-discipleship-intro">
          <div className="adult-discipleship-intro__copy content-copy">
            <p>
              For more information:
            </p>
            <p>
              Contact{" "}
              <a href="mailto:joycebradsteffen@gmail.com">Joyce Steffen</a> at{" "}
              <a href="tel:+17852801258">(785) 280-1258</a>
            </p>
            <p>
              Discipleship at Emmanuel Church is built around connection, accountability,
              and growth. The goal is not just attendance, but a shared walk of maturity in
              Christ.
            </p>
          </div>

          <figure className="adult-discipleship-intro__media">
            <Image
              src={withBasePath("/images/adult-discipleship/intro-hero.jpg")}
              alt="Adult discipleship groups at Emmanuel Church"
              fill
              sizes="(max-width: 900px) 100vw, 38vw"
              className="cover-image"
            />
          </figure>
        </article>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Three avenues"
          title="The church gives people three main places to grow."
          description="Life Groups, Triads, and Couples Connect give believers a clearer path toward spiritual maturity."
        />

        <div className="adult-discipleship-avenues">
          {avenueCards.map((card) => (
            <article key={card.title} className="adult-discipleship-avenue">
              <div className="adult-discipleship-avenue__media">
                <Image
                  src={withBasePath(card.image)}
                  alt={card.imageAlt}
                  fill
                  sizes="(max-width: 900px) 100vw, 33vw"
                  className="cover-image"
                />
              </div>
              <div className="adult-discipleship-avenue__body">
                <p className="eyebrow eyebrow--small">{card.eyebrow}</p>
                <h3>{card.title}</h3>
                <p>{card.description}</p>
                {card.points.length ? (
                  <ul className="adult-discipleship-points">
                    {card.points.map((point) => (
                      <li key={point}>{point}</li>
                    ))}
                  </ul>
                ) : null}
              </div>
            </article>
          ))}
        </div>
      </SectionShell>

      <SectionShell id="adult-groups" className="adult-discipleship-section">
        <SectionHeading
          eyebrow="Sunday mornings"
          title="Adult Discipleship Groups"
          description="10am Sunday Mornings"
        />

        <div className="adult-discipleship-purpose">
          <div className="adult-discipleship-purpose__panel content-copy">
            <p className="adult-discipleship-purpose__lead">
              Discipleship Classes are the teaching ministry of the church with four purposes.
            </p>
            <ol className="adult-discipleship-purpose__list">
              <li>
                <strong>Reaching</strong> those that need to hear the Gospel
              </li>
              <li>
                <strong>Teaching</strong> - Guided learning that meets the needs of a specific group
              </li>
              <li>
                <strong>Winning People to Christ</strong> - Communicating the Gospel in an
                understandable way, motivating people to respond to Jesus
              </li>
              <li>
                <strong>Caring</strong> - Spiritual nurturing to lead all class members into maturity in Christ
              </li>
            </ol>
            <p>
              We offer many small group meetings during our discipleship hour on Sunday mornings
              (10am) as well as off-site meetings during the week.
            </p>
          </div>

          <div className="adult-discipleship-purpose__accent">
            <p className="eyebrow eyebrow--small">Group</p>
            <p className="adult-discipleship-acronym">
              <span>G</span>
              <span>R</span>
              <span>O</span>
              <span>U</span>
              <span>P</span>
            </p>
            <p>Gathering regularly, offering understanding and prayer.</p>
          </div>
        </div>

        <div className="adult-discipleship-roster adult-discipleship-roster--sticky">
          {discipleshipClasses.map((group) => (
            <article key={group.title} className="adult-discipleship-card">
              <div className="adult-discipleship-card__media">
                <Image
                  src={withBasePath(group.image)}
                  alt={group.title}
                  fill
                  sizes="(max-width: 900px) 100vw, 25vw"
                  className="cover-image"
                />
              </div>
              <div className="adult-discipleship-card__body">
                <h3>{group.title}</h3>
                {group.description ? <p>{group.description}</p> : null}
              </div>
            </article>
          ))}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Process"
          title="How do I get connected to one or more of these groups?"
          description="Here's the process:"
          action={{
            label: "Email Joyce",
            href: "mailto:joycebradsteffen@gmail.com",
            external: true,
          }}
        />

        <ol className="adult-discipleship-steps">
          {processSteps.map((step, index) => (
            <li key={step}>
              <span className="adult-discipleship-step__number" aria-hidden="true">
                {index + 1}
              </span>
              <span>{step}</span>
            </li>
          ))}
        </ol>
      </SectionShell>

      <SectionShell className="section-shell--tight">
        <div className="adult-discipleship-footer-callout">
          <div>
            <p className="eyebrow eyebrow--small">Need a next step?</p>
            <h2>Emmanuel Church is ready to help you find a good place to connect.</h2>
          </div>
          <Link href="#adult-groups" className="button button--light">
            <span>Review the classes</span>
            <ArrowRightIcon className="icon icon--sm" />
          </Link>
        </div>
      </SectionShell>
    </>
  );
}
