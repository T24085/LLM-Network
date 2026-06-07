import { useEffect, useRef } from 'react';

type PayPalCartAction = 'AddToCart' | 'Cart';

type PayPalCartTriggerProps = {
  action: PayPalCartAction;
  buttonId: string;
  label: string;
  className?: string;
};

function initializePayPalCart(action: PayPalCartAction, buttonId: string) {
  const cart = window.cartPaypal;

  if (!cart) {
    return false;
  }

  cart[action]({ id: buttonId });
  return true;
}

export function PayPalCartTrigger({
  action,
  buttonId,
  label,
  className,
}: PayPalCartTriggerProps) {
  const nativeButtonRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    let timer: number | null = null;

    const tryInitialize = () => {
      if (!nativeButtonRef.current) {
        return false;
      }

      const ready = initializePayPalCart(action, buttonId);
      return ready;
    };

    if (tryInitialize()) {
      return undefined;
    }

    timer = window.setInterval(() => {
      if (tryInitialize() && timer !== null) {
        window.clearInterval(timer);
        timer = null;
      }
    }, 100);

    return () => {
      if (timer !== null) {
        window.clearInterval(timer);
      }
    };
  }, [action, buttonId]);

  const NativeElement = action === 'Cart' ? 'paypal-cart-button' : 'paypal-add-to-cart-button';

  return (
    <div className={className ? `paypal-cart-trigger ${className}` : 'paypal-cart-trigger'}>
      <NativeElement
        ref={(node) => {
          nativeButtonRef.current = node;
        }}
        data-id={buttonId}
        className="paypal-cart-trigger__native"
        aria-label={label}
      />
    </div>
  );
}
