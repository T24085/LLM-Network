import Image from "next/image";
import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { ValueFlipCard } from "@/components/value-flip-card";
import { withBasePath } from "@/lib/site-path";

import kidsReading from "../../../../Who we are - ABOUT/4d08689b-f470-40e1-87e6-796b5977e046.jpg";
import familyFromSide from "../../../../Who we are - ABOUT/96f1f8f7-05f7-497e-9979-d244d6a342b3.jpg";
import worshipRaisedHand from "../../../../Who we are - ABOUT/929c30f1-6dab-45a3-aef8-021bb46432f3.jpg";
import girlsStudying from "../../../../Who we are - ABOUT/d38f9698-c5e5-424a-ba1b-b554f9cf9009.jpg";

async function getDoctrineStatementHtml() {
  try {
    const response = await fetch("http://www.ecabilene.org/worship/who-we-are", {
      cache: "force-cache",
    });

    if (!response.ok) {
      return "";
    }

    const html = await response.text();
    const marker = "Doctrines of Emmanuel Church, Inc.</p></div></header>";
    const markerIndex = html.indexOf(marker);

    if (markerIndex < 0) {
      return "";
    }

    const articleStart = html.lastIndexOf("<article", markerIndex);
    const articleEnd = html.indexOf("</article>", markerIndex);

    if (articleStart < 0 || articleEnd < 0) {
      return "";
    }

    const article = html.slice(articleStart, articleEnd + "</article>".length);
    return article
      .replace(/<header class="text-content text-0 title-text editable"[\s\S]*?<\/header>\s*/i, "")
      .replace(/<h2[^>]*>\s*<\/h2>/gi, "");
  } catch {
    return "";
  }
}

export default async function WhoWeArePage() {
  const doctrineHtml = await getDoctrineStatementHtml();

  return (
    <>
      <PageHero
        eyebrow="Worship"
        title="Who We Are."
        description="At Emmanuel Church, we aim to extend God's grace, teach His Word, and live under the illumination of His truth."
        mediaLayout="full"
        layoutClassName="page-hero__layout--worship"
        action={{ label: "Meet the staff", href: "/our-staff" }}
        media={
          <div className="page-hero__media-frame">
            <Image
              src={withBasePath("/images/hero-cross-logo.png")}
              alt="A sunrise cross artwork for Emmanuel Church"
              fill
              priority
              sizes="(max-width: 1080px) 100vw, 100vw"
              className="page-hero__media-image page-hero__media-image--worship"
            />
          </div>
        }
      />

      <SectionShell className="section-shell--tight who-we-are-mission">
        <div className="who-we-are-mission__panel surface-card">
          <div className="who-we-are-mission__copy">
            <p className="eyebrow eyebrow--small">Mission</p>
            <h2>Love, Grace, Worship, Truth.</h2>
            <p className="who-we-are-mission__lede">
              These themes run through the church's doctrinal teaching and ministry language.
            </p>
            <p>
              Emmanuel Church says its mission is to see people transformed and families
              strengthened through the love, grace, worship, and truth of Jesus Christ.
            </p>
          </div>
          <figure className="who-we-are-mission__graphic surface-card">
            <div className="who-we-are-mission__media">
              <Image
                src={withBasePath("/who-we-are/mission-graphic.jpg")}
                alt="Love, grace, worship, and truth graphic for Emmanuel Church"
                fill
                sizes="(max-width: 1080px) 100vw, 34vw"
                className="cover-image"
              />
            </div>
          </figure>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Identity"
          title="Truth, Worship, and Family in one picture"
          description="These images hold the page together visually: doctrine in the logo, discipleship in the classroom, and worship in the gathered church."
        />
        <div className="who-we-are-showcase">
          <figure className="who-we-are-showcase__feature surface-card">
            <div className="who-we-are-showcase__media who-we-are-showcase__media--feature">
              <Image
                src={withBasePath("/who-we-are/truth.png")}
                alt="Truth logo for Emmanuel Church"
                fill
                sizes="(max-width: 1080px) 100vw, 42vw"
                className="cover-image"
                priority
              />
            </div>
            <figcaption>
              <span className="eyebrow eyebrow--small">Truth</span>
              <strong>Scripture gives the whole church its center.</strong>
              <p>What Emmanuel teaches on paper should show up in worship, study, and family life.</p>
            </figcaption>
          </figure>

          <div className="who-we-are-showcase__grid">
            <figure className="who-we-are-showcase__tile surface-card">
              <div className="who-we-are-showcase__media">
                <Image
                  src={kidsReading}
                  alt="A child reading in a classroom chair"
                  fill
                  sizes="(max-width: 1080px) 50vw, 22vw"
                  className="cover-image"
                />
              </div>
              <figcaption>
                <span className="eyebrow eyebrow--small">Children</span>
                <strong>Discipleship starts young.</strong>
              </figcaption>
            </figure>

            <figure className="who-we-are-showcase__tile surface-card">
              <div className="who-we-are-showcase__media">
                <Image
                  src={familyFromSide}
                  alt="Families gathered together in the church"
                  fill
                  sizes="(max-width: 1080px) 50vw, 22vw"
                  className="cover-image"
                />
              </div>
              <figcaption>
                <span className="eyebrow eyebrow--small">Family</span>
                <strong>Faith is carried together.</strong>
              </figcaption>
            </figure>

            <figure className="who-we-are-showcase__tile surface-card">
              <div className="who-we-are-showcase__media">
                <Image
                  src={worshipRaisedHand}
                  alt="A worshiper raising a hand during service"
                  fill
                  sizes="(max-width: 1080px) 50vw, 22vw"
                  className="cover-image"
                />
              </div>
              <figcaption>
                <span className="eyebrow eyebrow--small">Worship</span>
                <strong>We gather to respond to God.</strong>
              </figcaption>
            </figure>

            <figure className="who-we-are-showcase__tile surface-card">
              <div className="who-we-are-showcase__media">
                <Image
                  src={girlsStudying}
                  alt="Girls working through a Bible lesson at a table"
                  fill
                  sizes="(max-width: 1080px) 50vw, 22vw"
                  className="cover-image"
                />
              </div>
              <figcaption>
                <span className="eyebrow eyebrow--small">Study</span>
                <strong>Learning and worship stay connected.</strong>
              </figcaption>
            </figure>
          </div>
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading eyebrow="Core values" title="The Pillars Behind the Ministry." />
        <div className="content-grid">
          <ValueFlipCard
            title="Love"
            summary="Love shapes the posture of the church and the way we serve one another."
            backTitle="Love transforms people and families"
            backBody="Love is the foundation of our Mission and the Core Value from which all other Core Values and ministries grow. Love originates with God and is expressed through His people. It is the covering for every motivation and action that we take, make, or create. If we are without God's love, we have little ability to make a difference in the lives of people or families. Others will identify us as Christ followers because of love. God first loved us and because of His love, we can love others."
            references="(1 John 4:7-12, 1 Corinthians 13, Matthew 22:36-40)"
            frontImage="/images/who-we-are/love.png"
            frontImageAlt="Love watercolor card"
          />
          <ValueFlipCard
            title="Grace"
            summary="Grace is God's undeserved gift, made clear in Jesus Christ."
            backTitle="Grace transforms people and families"
            backBody="At Emmanuel Church, we desire to be a people who extend the grace of God to others. Grace is getting something we don’t deserve and is perfectly illustrated in God’s gift of Jesus Christ. Jesus’ death and resurrection are supreme examples of grace. In His death Jesus paid a price for our sins that we simply could not pay. Only the blood of Jesus, given as an offering of grace, can erase our sins. We don’t deserve this precious gift, but He freely offers it to all people. In His resurrection Jesus has overcome death and through grace has paved the way for us to live eternally with Him. We truly are saved through faith because of God’s grace."
            references="(John 1:16-17; Ephesians 2:1-10; Romans 3:23-25; Romans 5:17)"
            frontImage="/images/who-we-are/grace.png"
            frontImageAlt="Grace watercolor card"
          />
          <ValueFlipCard
            title="Worship"
            summary="Worship is our response of praise, prayer, generosity, and surrender."
            backTitle="Worship transforms people and families"
            backBody="At Emmanuel Church, we desire to be a people who live a lifestyle of Worship. Worship is our outward and inward expression of thanksgiving and praise to the One who created us. Worship includes corporate and private singing, prayer, giving, and submission to God in all areas of our lives. It is first and foremost a response to who God is and a response to what He’s done for us. Worship is to be a lifestyle that fills our journey with Christ, and not merely a corporate activity. When we worship we put Jesus first and seek to be led by the Holy Spirit as we purposely seek to be in His amazing presence."
            references="(Leviticus 26:1; 1 Samuel 12:21; Exodus 34:14; Psalm 29:2; Psalm 81:9; Psalm 99:9; Matthew 4:10; John 4:24)"
            frontImage="/images/who-we-are/worship.png"
            frontImageAlt="Worship watercolor card"
          />
          <ValueFlipCard
            title="Truth"
            summary="God's truth is revealed by the Holy Spirit and lived out with confidence."
            backTitle="Truth is illuminated by the Holy Spirit"
            backBody="At Emmanuel Church, we desire to be a people who are led by the Holy Spirit as He illuminates God’s Truth. The Holy Spirit transforms people and families. The Holy Spirit’s role is to illuminate God’s Truth and to empower us to share the good news of Jesus Christ with others. God’s Word represents absolute truth, is without error, inspired by the Holy Spirit through men, and is our guide for daily living. It is the Holy Spirit that woos us through Prevenient Grace to accept Jesus Christ as Lord and Savior. In saying “yes” to Jesus we experience His Saving Grace. Our God exists as God the Father, Jesus the Son, and the Holy Spirit, all working on our behalf as Christ followers. God’s Sanctifying Grace is at work in each of us as we are being made more and more like Christ. As we embrace the Spirit-filled life, evidence is found in our display of the Fruit of the Spirit. God has sent His Holy Spirit as a rich deposit in each believer to guide us and teach us until the return of His Son, Jesus Christ."
            references="(John 14:26; Matthew 3:11; Matthew 28:19; John 15:26; Acts 1:8; Romans 14:16-18; Titus 3:4-6; 2 Peter 1:20-21; Galatians 5:22-23)"
            frontImage="/images/who-we-are/truth.png"
            frontImageAlt="Truth watercolor card"
          />
        </div>
      </SectionShell>

      <SectionShell>
        <SectionHeading
          eyebrow="Doctrine"
          title="Doctrines of Emmanuel Church, Inc."
          description="A basis for fellowship, shared understanding, and faithful teaching."
        />
        <details className="doctrines-panel">
          <summary>
            <span>Open the full statement</span>
            <span className="doctrines-panel__summary-hint">Long-form doctrinal appendix</span>
          </summary>
          <div className="doctrines-panel__content">
            {doctrineHtml ? (
              <div dangerouslySetInnerHTML={{ __html: doctrineHtml }} />
            ) : (
              <p>
                The full doctrinal statement could not be loaded at the moment.
              </p>
            )}
          </div>
        </details>
      </SectionShell>
    </>
  );
}
