import { ArrowUpRight, X } from 'lucide-react';
import { addOns } from '../data/pricing';
import { intakeFormUrl } from '../data/site';
import { PayPalCartTrigger } from './PayPalCartTrigger';

type PricingModalProps = {
  open: boolean;
  onClose: () => void;
};

export function PricingModal({ open, onClose }: PricingModalProps) {
  if (!open) {
    return null;
  }

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div className="modal" role="dialog" aria-modal="true" aria-labelledby="pricing-modal-title" onClick={(event) => event.stopPropagation()}>
        <button className="modal__close" type="button" aria-label="Close pricing modal" onClick={onClose}>
          <X size={18} />
        </button>

        <div className="modal__header">
          <p className="section-label">Website packages</p>
          <h2 id="pricing-modal-title">Custom websites with a sharper way to turn attention into action.</h2>
          <p className="modal__lede">
            Built for creators, models, brands, and businesses that want presence, clarity, and a polished finish.
          </p>
        </div>

        <div className="modal__summary">
          <p>
            The package breakdown stays in the pricing section, so the original information remains in one place.
            Use the cards below to compare the options, then choose the one that fits.
          </p>
          <a className="button button--secondary" href="#pricing" onClick={onClose}>
            Go to Pricing
            <ArrowUpRight size={16} />
          </a>
        </div>

        <div className="modal__addons">
          <div className="modal__addons-head">
            <h3>Add-ons</h3>
            <p>Enhancements that can be added to any project.</p>
          </div>
          <div className="modal__addons-grid">
            {addOns.map((addon) => (
              <div className="addon-item" key={addon.name}>
                <div className="addon-row">
                  <span>{addon.name}</span>
                  <strong>{addon.price}</strong>
                </div>
                {addon.cartAddToCartId ? (
                  <div className="addon-item__action">
                    <PayPalCartTrigger action="AddToCart" buttonId={addon.cartAddToCartId} label="Add to Cart" />
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        </div>

        <div className="modal__footer">
          <p>Every project is built custom. No templates, no shortcuts, just a focused site designed to look sharp and perform fast.</p>
          <a className="button button--primary" href={intakeFormUrl} target="_blank" rel="noreferrer">
            Start Your Website
            <ArrowUpRight size={16} />
          </a>
        </div>
      </div>
    </div>
  );
}
