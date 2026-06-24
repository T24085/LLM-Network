"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { primaryNav, site } from "@/data/site";
import { ArrowRightIcon, CloseIcon, MenuIcon } from "./icons";

function isActive(pathname: string, href: string) {
  if (href === "/") {
    return pathname === href;
  }

  return pathname === href || pathname.startsWith(`${href}/`);
}

export function SiteHeader() {
  const pathname = usePathname();
  const mobileMenuRef = useRef<HTMLDetailsElement>(null);

  useEffect(() => {
    if (mobileMenuRef.current) {
      mobileMenuRef.current.open = false;
    }
  }, [pathname]);

  const closeMobileMenu = () => {
    if (mobileMenuRef.current) {
      mobileMenuRef.current.open = false;
    }
  };

  return (
    <header className="site-header">
      <div className="site-shell site-header__inner">
        <Link href="/" className="brand" aria-label={site.name}>
          <span className="brand__icon" aria-hidden="true">
            <span className="brand__cross brand__cross--vertical" />
            <span className="brand__cross brand__cross--horizontal" />
          </span>
          <span className="brand__wordmark">
            <span>Emmanuel</span>
            <span>Church</span>
          </span>
        </Link>

        <nav className="site-nav" aria-label="Primary">
          {primaryNav.map((item) => {
            const active = isActive(pathname, item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`site-nav__link${active ? " site-nav__link--active" : ""}`}
                aria-current={active ? "page" : undefined}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="site-header__actions">
          <button className="icon-button" type="button" aria-label="Search">
            <span className="icon-button__ring" />
          </button>
          <Link href="/contact" className="button button--gold">
            Plan Your Visit
          </Link>
        </div>

        <details ref={mobileMenuRef} className="mobile-menu">
          <summary className="mobile-menu__summary" aria-label="Open menu">
            <MenuIcon className="icon icon--sm" />
            <CloseIcon className="icon icon--sm mobile-menu__close" />
          </summary>
          <div className="mobile-menu__panel">
            <div className="mobile-menu__top">
              <Link
                href="/"
                className="mobile-menu__brand"
                aria-label={site.name}
                onClick={closeMobileMenu}
              >
                Emmanuel Church
              </Link>
              <Link href="/contact" className="button button--gold button--small" onClick={closeMobileMenu}>
                Plan Visit
              </Link>
            </div>
            <nav className="mobile-menu__nav" aria-label="Mobile">
              {primaryNav.map((item) => {
                const active = isActive(pathname, item.href);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`mobile-menu__link${active ? " mobile-menu__link--active" : ""}`}
                    aria-current={active ? "page" : undefined}
                    onClick={closeMobileMenu}
                  >
                    {item.label}
                    <ArrowRightIcon className="icon icon--xs" />
                  </Link>
                );
              })}
            </nav>
          </div>
        </details>
      </div>
    </header>
  );
}
