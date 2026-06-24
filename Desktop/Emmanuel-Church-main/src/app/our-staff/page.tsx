import { PageHero } from "@/components/page-hero";
import { SectionHeading, SectionShell } from "@/components/section";
import { StaffGrid } from "@/components/staff-grid";

export default function OurStaffPage() {
  return (
    <div className="our-staff-page">
      <PageHero
        eyebrow="Our Staff"
        title="People, names, and roles that make the church easy to find."
        description="Use the staff directory to email the right person directly or contact the office for general help."
        action={{ label: "Contact the office", href: "/contact" }}
      />
      <SectionShell>
        <SectionHeading
          eyebrow="Directory"
          title="Meet the people serving Emmanuel Church."
          description="Browse the staff directory by portrait, name, and role to find the right person quickly."
        />
        <StaffGrid />
      </SectionShell>
    </div>
  );
}
