import { ArrowUpRight } from 'lucide-react';
import { type Package } from '../data/pricing';
import { intakeFormUrl } from '../data/site';
import { PayPalCartTrigger } from './PayPalCartTrigger';

type PackageActionProps = {
  pkg: Package;
  context?: 'pricing' | 'modal';
};

export function PackageAction({ pkg, context = 'pricing' }: PackageActionProps) {
  if (pkg.cartAddToCartId) {
    if (context === 'modal') {
      return (
        <a className="button button--secondary button--full" href="#pricing">
          Purchase in pricing section
          <ArrowUpRight size={16} />
        </a>
      );
    }

    return (
      <PayPalCartTrigger
        action="AddToCart"
        buttonId={pkg.cartAddToCartId}
        label={pkg.cta}
      />
    );
  }

  return (
    <a
      className={pkg.featured ? 'button button--primary button--full' : 'button button--ghost button--full'}
      href={intakeFormUrl}
      target="_blank"
      rel="noreferrer"
    >
      {pkg.cta}
      <ArrowUpRight size={16} />
    </a>
  );
}
