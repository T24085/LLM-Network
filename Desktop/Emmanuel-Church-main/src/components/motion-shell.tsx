"use client";

import type { ReactNode } from "react";
import { useEffect } from "react";
import { usePathname } from "next/navigation";

const revealSelectors = [
  ".page-hero",
  ".section-shell",
  ".section-heading",
  ".hero__copy",
  ".hero__card-row",
  ".feature-card",
  ".value-card",
  ".resource-card",
  ".staff-card",
  ".split-panel",
  ".quote-strip",
  ".inline-banner",
  ".link-list__item",
].join(", ");

export function MotionShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  useEffect(() => {
    const root = document.documentElement;
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const hero = document.querySelector<HTMLElement>(".hero");

    root.classList.add("motion-ready");
    root.classList.toggle("motion-reduce", reducedMotion);

    if (reducedMotion) {
      root.style.removeProperty("--hero-parallax");
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        }
      },
      {
        threshold: 0.18,
        rootMargin: "0px 0px -6% 0px",
      }
    );

    const observed = new WeakSet<Element>();
    const observeTargets = () => {
      document.querySelectorAll(revealSelectors).forEach((element) => {
        if (!observed.has(element)) {
          observed.add(element);
          observer.observe(element);
        }
      });
    };

    observeTargets();

    const mutationObserver = new MutationObserver(() => {
      window.requestAnimationFrame(observeTargets);
    });

    mutationObserver.observe(document.body, {
      childList: true,
      subtree: true,
    });

    let rafId = 0;
    const updateHeroParallax = () => {
      rafId = 0;
      if (!hero) {
        root.style.removeProperty("--hero-parallax");
        return;
      }

      const heroRect = hero.getBoundingClientRect();
      const viewportHeight = window.innerHeight || 1;
      const scrolled = Math.max(0, -heroRect.top);
      const travel = heroRect.height || viewportHeight;
      const progress = Math.min(1, scrolled / travel);
      const maxShift = window.innerWidth < 768 ? 18 : 56;
      const shift = Math.round(progress * maxShift);

      root.style.setProperty("--hero-parallax", `${shift}px`);
    };

    const onScroll = () => {
      if (!rafId) {
        rafId = window.requestAnimationFrame(updateHeroParallax);
      }

      root.classList.toggle("site-scrolled", window.scrollY > 12);
    };

    updateHeroParallax();
    root.classList.toggle("site-scrolled", window.scrollY > 12);
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);

    return () => {
      mutationObserver.disconnect();
      observer.disconnect();
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (rafId) {
        window.cancelAnimationFrame(rafId);
      }
      root.style.removeProperty("--hero-parallax");
    };
  }, [pathname]);

  return children;
}
