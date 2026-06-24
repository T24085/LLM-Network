import Link from "next/link";
import { contactEmails, externalLinks, resourceLinks, site } from "@/data/site";
import { ArrowRightIcon, MailIcon, PhoneIcon, LocationIcon } from "./icons";

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="site-shell site-footer__inner">
        <div className="site-footer__brand">
          <p className="eyebrow">Emmanuel Church</p>
          <h2>Rooted in the gospel. Present in Abilene.</h2>
          <p>
            {site.address}
            <br />
            {site.phone}
          </p>
        </div>

        <div className="site-footer__columns">
          <div>
            <h3>Explore</h3>
            <div className="site-footer__links">
              {resourceLinks.slice(0, 5).map((item) => (
                <Link key={item.href} href={item.href} className="site-footer__link">
                  {item.label}
                  <ArrowRightIcon className="icon icon--xs" />
                </Link>
              ))}
            </div>
          </div>

          <div>
            <h3>Contact</h3>
            <div className="site-footer__links">
              <a className="site-footer__link" href={`tel:${site.phone.replace(/[^0-9+]/g, "")}`}>
                <PhoneIcon className="icon icon--xs" />
                <span>{site.phone}</span>
              </a>
              <a className="site-footer__link" href={`mailto:${contactEmails[0]}`}>
                <MailIcon className="icon icon--xs" />
                <span>Primary staff email</span>
              </a>
              <a className="site-footer__link" href={site.mapHref} target="_blank" rel="noreferrer">
                <LocationIcon className="icon icon--xs" />
                <span>Locate us</span>
              </a>
            </div>
          </div>

          <div>
            <h3>External</h3>
            <div className="site-footer__links">
              {externalLinks.map((item) => (
                <a
                  key={item.href}
                  className="site-footer__link"
                  href={item.href}
                  target="_blank"
                  rel="noreferrer"
                >
                  <span>{item.label}</span>
                  <ArrowRightIcon className="icon icon--xs" />
                </a>
              ))}
            </div>
          </div>

          <div>
            <h3>Emails</h3>
            <div className="site-footer__links">
              {contactEmails.map((email) => (
                <a key={email} className="site-footer__link" href={`mailto:${email}`}>
                  <MailIcon className="icon icon--xs" />
                  <span>{email}</span>
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
