import Image from "next/image";
import Link from "next/link";
import { staff } from "@/data/site";
import { withBasePath } from "@/lib/site-path";
import { MailIcon, ArrowRightIcon } from "./icons";

export function StaffGrid({ limit }: { limit?: number }) {
  const items = typeof limit === "number" ? staff.slice(0, limit) : staff;

  return (
    <div className="staff-grid">
      {items.map((person) => (
        <article key={person.name} className="staff-card">
          <div className="staff-card__media">
            <Image
              src={withBasePath(person.image)}
              alt={person.name}
              fill
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 33vw, 300px"
              className="cover-image"
            />
          </div>
          <div className="staff-card__body">
            <p className="eyebrow eyebrow--small">{person.role}</p>
            <h3>{person.name}</h3>
            <div className="staff-card__actions">
              {person.email ? (
                <Link className="text-link" href={`mailto:${person.email}`}>
                  <MailIcon className="icon icon--xs" />
                  <span>{person.email}</span>
                </Link>
              ) : (
                <span className="muted">Contact the office for direct scheduling.</span>
              )}
              <Link href="/our-staff" className="text-link text-link--secondary">
                <span>Read more</span>
                <ArrowRightIcon className="icon icon--xs" />
              </Link>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
