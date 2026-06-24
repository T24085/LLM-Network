import Image from "next/image";
import Link from "next/link";
import {
  ArrowRightIcon,
  BookIcon,
  CalendarIcon,
  HeartIcon,
  PlayIcon,
  UsersIcon,
} from "@/components/icons";
import { HeroVideo } from "@/components/hero-video";
import { SectionHeading, SectionShell } from "@/components/section";
import { StaffGrid } from "@/components/staff-grid";
import { ValueFlipCard } from "@/components/value-flip-card";
import { withBasePath } from "@/lib/site-path";
import {
  featureCards,
  ministryLinks,
  serviceRhythm,
  site,
} from "@/data/site";
import loveCard from "../../Who we are - ABOUT/CornerStone Love.png";
import graceCard from "../../Who we are - ABOUT/CornerStone Grace.png";
import worshipCard from "../../Who we are - ABOUT/Corner Stone Worship.png";
import truthCard from "../../Who we are - ABOUT/CornerStone Truth.png";

const iconMap = [BookIcon, UsersIcon, HeartIcon, CalendarIcon];

const homepageValues = [
  {
    title: "Love",
    summary: "Love shapes the posture of the church and the way we serve one another.",
    backTitle: "Love transforms people and families",
    backBody:
      "Love is the foundation of our Mission and the Core Value from which all other Core Values and ministries grow. Love originates with God and is expressed through His people. It is the covering for every motivation and action that we take, make, or create. If we are without God's love, we have little ability to make a difference in the lives of people or families. Others will identify us as Christ followers because of love. God first loved us and because of His love, we can love others.",
    references: "(1 John 4:7-12, 1 Corinthians 13, Matthew 22:36-40)",
    frontImage: loveCard,
    frontImageAlt: "CornerStone Love watercolor card",
  },
  {
    title: "Grace",
    summary: "Grace is God's undeserved gift, made clear in Jesus Christ.",
    backTitle: "Grace transforms people and families",
    backBody:
      "At Emmanuel Church, we desire to be a people who extend the grace of God to others. Grace is getting something we don’t deserve and is perfectly illustrated in God’s gift of Jesus Christ. Jesus’ death and resurrection are supreme examples of grace. In His death Jesus paid a price for our sins that we simply could not pay. Only the blood of Jesus, given as an offering of grace, can erase our sins. We don’t deserve this precious gift, but He freely offers it to all people. In His resurrection Jesus has overcome death and through grace has paved the way for us to live eternally with Him. We truly are saved through faith because of God’s grace.",
    references: "(John 1:16-17; Ephesians 2:1-10; Romans 3:23-25; Romans 5:17)",
    frontImage: graceCard,
    frontImageAlt: "CornerStone Grace watercolor card",
  },
  {
    title: "Worship",
    summary: "Worship is our response of praise, prayer, generosity, and surrender.",
    backTitle: "Worship transforms people and families",
    backBody:
      "At Emmanuel Church, we desire to be a people who live a lifestyle of Worship. Worship is our outward and inward expression of thanksgiving and praise to the One who created us. Worship includes corporate and private singing, prayer, giving, and submission to God in all areas of our lives. It is first and foremost a response to who God is and a response to what He’s done for us. Worship is to be a lifestyle that fills our journey with Christ, and not merely a corporate activity. When we worship we put Jesus first and seek to be led by the Holy Spirit as we purposely seek to be in His amazing presence.",
    references: "(Leviticus 26:1; 1 Samuel 12:21; Exodus 34:14; Psalm 29:2; Psalm 81:9; Psalm 99:9; Matthew 4:10; John 4:24)",
    frontImage: worshipCard,
    frontImageAlt: "CornerStone Worship watercolor card",
  },
  {
    title: "Truth",
    summary: "God's truth is revealed by the Holy Spirit and lived out with confidence.",
    backTitle: "Truth is illuminated by the Holy Spirit",
    backBody:
      "At Emmanuel Church, we desire to be a people who are led by the Holy Spirit as He illuminates God’s Truth. The Holy Spirit transforms people and families. The Holy Spirit’s role is to illuminate God’s Truth and to empower us to share the good news of Jesus Christ with others. God’s Word represents absolute truth, is without error, inspired by the Holy Spirit through men, and is our guide for daily living. It is the Holy Spirit that woos us through Prevenient Grace to accept Jesus Christ as Lord and Savior. In saying “yes” to Jesus we experience His Saving Grace. Our God exists as God the Father, Jesus the Son, and the Holy Spirit, all working on our behalf as Christ followers. God’s Sanctifying Grace is at work in each of us as we are being made more and more like Christ. As we embrace the Spirit-filled life, evidence is found in our display of the Fruit of the Spirit. God has sent His Holy Spirit as a rich deposit in each believer to guide us and teach us until the return of His Son, Jesus Christ.",
    references: "(John 14:26; Matthew 3:11; Matthew 28:19; John 15:26; Acts 1:8; Romans 14:16-18; Titus 3:4-6; 2 Peter 1:20-21; Galatians 5:22-23)",
    frontImage: truthCard,
    frontImageAlt: "CornerStone Truth watercolor card",
  },
];

export default function HomePage() {
  return (
    <>
      <section className="hero">
        <HeroVideo />
        <div className="hero__overlay" />
        <div className="site-shell hero__inner">
          <div className="hero__copy">
            <div className="hero__headline">
              <p className="eyebrow">Knowing Christ. Making Him known.</p>
              <h1>Emmanuel Church</h1>
              <p className="hero__lede">
                We exist to glorify God by making disciples of Jesus Christ through the power of the gospel.
              </p>
            </div>
            <div className="hero__actions">
              <Link href="/contact" className="button button--gold">
                Plan Your Visit
              </Link>
              <Link href="/resources/live-stream" className="button button--light">
                <PlayIcon className="icon icon--sm" />
                <span>Watch Latest Sermon</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      <SectionShell className="section-shell--feature-rail">
        <div className="hero__card-row" aria-label="Core priorities">
          {featureCards.map((card, index) => {
            const Icon = iconMap[index] ?? ArrowRightIcon;
            return (
              <article key={card.title} className="feature-card">
                <div className="feature-card__icon" aria-hidden="true">
                  <Icon className="icon" />
                </div>
                <div>
                  <h3>{card.title}</h3>
                  <p>{card.text}</p>
                </div>
                <Link href={card.href} className="feature-card__link">
                  Learn more <ArrowRightIcon className="icon icon--xs" />
                </Link>
              </article>
            );
          })}
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Welcome to Emmanuel Church"
          title="We're Glad you're Here."
          description="Emmanuel Church is a place where you can know Christ, grow in your faith, and find a family. If you're new to church or looking for a home, we'd love to meet you."
          action={{ label: "More About Us", href: "/worship/who-we-are" }}
        />
        <div className="split-grid">
          <article className="split-panel split-panel--image">
            <Image
              src={withBasePath("/images/building-banner.jpg")}
              alt="Emmanuel Church exterior"
              fill
              priority
              sizes="(max-width: 1080px) 100vw, 60vw"
              className="split-panel__image cover-image"
            />
            <div className="split-panel__overlay" />
            <div className="split-panel__content">
              <p className="eyebrow">Sunday rhythms</p>
              <h3>Traditional at 8:45. Contemporary at 11:00.</h3>
              <p>
                Discipleship Hour runs from 10:00am to 10:45am for all ages, with nursery care,
                children's ministry, and a family-friendly welcome center on the south side of the
                building.
              </p>
            </div>
          </article>

          <aside className="split-panel">
            <div className="split-panel__content" style={{ paddingBottom: "1.4rem" }}>
              <p className="eyebrow">Weekly rhythm</p>
              <div className="stat-grid">
                {serviceRhythm.map((item) => (
                  <div key={item.label} className="stat-card">
                    <div>
                      <div className="stat-card__label">{item.label}</div>
                      <div className="stat-card__value">{item.value}</div>
                    </div>
                    <div className="stat-card__detail">{item.detail}</div>
                  </div>
                ))}
              </div>
              <div className="hero__actions" style={{ marginTop: "1.35rem" }}>
                <Link href="/resources/church-calendar" className="button button--gold">
                  View Calendar
                </Link>
                <Link
                  href={site.mapHref}
                  target="_blank"
                  rel="noreferrer"
                  className="button button--light"
                >
                  <CalendarIcon className="icon icon--sm" />
                  <span>Locate Us</span>
                </Link>
              </div>
            </div>
          </aside>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Our Mission"
          title="Four words that shape the whole church."
          description="Love, Grace, Worship, and Truth are not slogans here. They are the language of the church and the frame for everything we do."
        />
        <div className="content-grid">
          {homepageValues.map((value) => (
            <ValueFlipCard
              key={value.title}
              title={value.title}
              summary={value.summary}
              backTitle={value.backTitle}
              backBody={value.backBody}
              references={value.references}
              frontImage={value.frontImage}
              frontImageAlt={value.frontImageAlt}
            />
          ))}
        </div>
        <div className="inline-banner">
          <div className="inline-banner__inner">
            <div className="inline-banner__copy">
              <p className="eyebrow">Know. Grow. Send.</p>
              <h3>The gospel forms people and families.</h3>
              <p>
                Emmanuel's mission is transformation through the gospel, and every ministry should
                serve that aim with clarity and care.
              </p>
            </div>
            <div className="inline-banner__media">
              <Image
                src={withBasePath("/images/hero-cross-logo.png")}
                alt=""
                fill
                sizes="(max-width: 1080px) 100vw, 40vw"
                className="inline-banner__image cover-image"
              />
            </div>
          </div>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Featured Staff"
          title="A clear face for every ministry."
          description="Portraits and contact details are organized so the people leading each ministry are easy to find."
          action={{ label: "Meet the full staff", href: "/our-staff" }}
        />
        <StaffGrid limit={6} />
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Ministries"
          title="Ministries that form a real church family."
          description="Each ministry plays a clear role in the life of the church: children, students, adults, worship, and midweek gatherings."
          action={{ label: "Explore ministries", href: "/connect" }}
        />
        <div className="resource-grid">
          {ministryLinks.slice(0, 3).map((item) => (
            <Link key={item.href} href={item.href} className="resource-card resource-card--linked">
              <p className="eyebrow eyebrow--small">Connect</p>
              <h3>{item.label}</h3>
              <p>{item.description}</p>
              <span className="resource-card__action resource-card__action--button">
                Open page <ArrowRightIcon className="icon icon--xs" />
              </span>
            </Link>
          ))}
        </div>
      </SectionShell>

      <SectionShell className="section-shell--tight">
        <div className="quote-strip">
          <div className="quote-strip__row">
            <div className="quote-strip__verse">
              <p className="eyebrow eyebrow--small">Sermon rhythm</p>
              <strong>Let the word of Christ dwell in you richly.</strong>
              <p>Colossians 3:16</p>
            </div>
            <Link href="/resources/sermons" className="button button--light quote-strip__action">
              <span>View Sermons</span>
              <ArrowRightIcon className="icon icon--sm" />
            </Link>
          </div>
        </div>
      </SectionShell>
    </>
  );
}
