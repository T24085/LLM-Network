"use client";

import { useMemo, useState } from "react";
import type { MediaArchivePage } from "@/lib/media-archive";
import { SermonPlayer, type SermonPlayerItem } from "./sermon-player";

type MediaArchiveBrowserProps = {
  pages: MediaArchivePage[];
};

export function MediaArchiveBrowser({ pages }: MediaArchiveBrowserProps) {
  const [pageIndex, setPageIndex] = useState(0);

  const activePage = pages[pageIndex] ?? pages[0];
  const currentPage = activePage?.page ?? 1;

  const pageNumbers = useMemo(() => pages.map((page) => page.page), [pages]);
  const activeSermons = useMemo<SermonPlayerItem[]>(
    () =>
      (activePage?.items || []).map((item) => ({
        label: item.title,
        href: item.href || "https://www.ecabilene.org/resources/sermons",
        mediaId: item.id,
        embedSrc: item.embedSrc,
        thumbnail: item.thumbnail || undefined,
        date: item.date || null,
        kind: item.kind,
      })),
    [activePage]
  );

  if (!activePage) {
    return null;
  }

  const jumpToPage = (nextIndex: number) => {
    if (nextIndex < 0 || nextIndex >= pages.length) {
      return;
    }

    setPageIndex(nextIndex);
  };

  return (
    <div className="media-archive-browser">
      <div className="media-archive-browser__pager surface-card">
        <button
          type="button"
          className="media-archive-browser__nav"
          onClick={() => jumpToPage(pageIndex - 1)}
          disabled={pageIndex === 0}
        >
          Previous
        </button>

        <div className="media-archive-browser__pages" aria-label="Media archive pages">
          {pageNumbers.map((pageNumber, index) => {
            const active = index === pageIndex;
            return (
              <button
                key={pageNumber}
                type="button"
                className={`media-archive-browser__page ${active ? "media-archive-browser__page--active" : ""}`.trim()}
                onClick={() => setPageIndex(index)}
                aria-pressed={active}
              >
                {pageNumber}
              </button>
            );
          })}
        </div>

        <button
          type="button"
          className="media-archive-browser__nav"
          onClick={() => jumpToPage(pageIndex + 1)}
          disabled={pageIndex >= pages.length - 1}
        >
          Next
        </button>
      </div>

      <div className="media-archive-browser__summary">
        <span>Page {currentPage}</span>
        <span>{activePage.items.length} videos on this page</span>
      </div>

      <SermonPlayer key={currentPage} sermons={activeSermons} />
    </div>
  );
}
