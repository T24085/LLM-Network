import legacyMediaArchivePages from "@/data/media-archive.json";

const VIMEO_ARCHIVE_URL = "https://vimeo.com/ecabilene/videos";
const ARCHIVE_REVALIDATE_SECONDS = 6 * 60 * 60;
const LEGACY_PAGE_START_INDEX = 19;

const HTML_ENTITIES: Record<string, string> = {
  amp: "&",
  apos: "'",
  gt: ">",
  hellip: "…",
  laquo: "«",
  ldquo: "“",
  lsquo: "‘",
  nbsp: " ",
  quot: '"',
  raquo: "»",
  rdquo: "”",
  rsquo: "’",
  shy: "­",
  lt: "<",
};

export type MediaArchiveItem = {
  id: number;
  title: string;
  date: string;
  thumbnail: string | null;
  embedSrc: string | null;
  kind: "video" | "audio";
  href?: string;
};

export type MediaArchivePage = {
  page: number;
  items: MediaArchiveItem[];
};

function decodeHtml(value: string) {
  return value
    .replace(/&#(\d+);/g, (_, number: string) => String.fromCodePoint(Number(number)))
    .replace(/&#x([0-9a-f]+);/gi, (_, hex: string) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&([a-z]+);/gi, (match, entity: string) => HTML_ENTITIES[entity] || match);
}

function cleanText(value: string) {
  return decodeHtml(value).replace(/\s+/g, " ").trim();
}

function formatDateLabel(datetime: string) {
  const [year, month, day] = datetime.slice(0, 10).split("-").map(Number);
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "UTC",
    month: "long",
    day: "numeric",
    year: "numeric",
  }).format(new Date(Date.UTC(year, month - 1, day)));
}

function dateKeyFromLabel(date: string) {
  return new Date(`${date} 12:00:00 UTC`).getTime();
}

function dateKeyFromDatetime(datetime: string) {
  const [year, month, day] = datetime.slice(0, 10).split("-").map(Number);
  return Date.UTC(year, month - 1, day);
}

async function fetchText(url: string) {
  const response = await fetch(url, {
    next: { revalidate: ARCHIVE_REVALIDATE_SECONDS },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}: ${response.status} ${response.statusText}`);
  }

  return response.text();
}

function parseVimeoPage(html: string) {
  const nextHref = html.match(/<link rel="next" href="([^"]+)"/)?.[1] || null;
  const items = [...html.matchAll(/<li id="clip_(\d+)"[\s\S]*?<\/li>/g)].map((match) => {
    const block = match[0];
    const id = Number(match[1]);
    const linkPath = block.match(/<a href="([^"]+)" title="([^"]+)">/)?.[1] || `/${id}`;
    const title = cleanText(
      block.match(/<div class="l-ellipsis">([\s\S]*?)<\/div>/)?.[1] ||
        block.match(/<a href="([^"]+)" title="([^"]+)">/)?.[2] ||
        ""
    );
    const thumbnail = block.match(/<img[^>]+src="([^"]+)"/)?.[1] || null;
    const datetime = block.match(/<time datetime="([^"]+)"/)?.[1] || null;

    return {
      id,
      title,
      date: datetime ? formatDateLabel(datetime) : "",
      dateKey: datetime ? dateKeyFromDatetime(datetime) : 0,
      thumbnail,
      embedSrc: `https://player.vimeo.com/video/${id}`,
      href: `https://vimeo.com${linkPath.startsWith("/") ? linkPath : `/${linkPath}`}`,
      kind: "video" as const,
    };
  });

  return {
    items,
    nextHref,
  };
}

async function loadVimeoArchivePages() {
  const pages: Array<MediaArchivePage & { dateKey?: number }> = [];
  let currentUrl: string | null = VIMEO_ARCHIVE_URL;
  let pageNumber = 1;

  while (currentUrl) {
    const html = await fetchText(currentUrl);
    const { items, nextHref } = parseVimeoPage(html);

    if (items.length === 0) {
      break;
    }

    pages.push({
      page: pageNumber,
      items: items.map(({ dateKey, ...item }) => item),
      dateKey: items[items.length - 1]?.dateKey,
    });

    currentUrl = nextHref ? new URL(nextHref, currentUrl).href : null;
    pageNumber += 1;
  }

  return pages;
}

function loadLegacyArchivePages(): MediaArchivePage[] {
  return (legacyMediaArchivePages as MediaArchivePage[]).slice(LEGACY_PAGE_START_INDEX);
}

export async function loadMediaArchivePages() {
  try {
    const vimeoPages = await loadVimeoArchivePages();
    const legacyPages = loadLegacyArchivePages();
    const cutoffDateKey = vimeoPages.length > 0 ? vimeoPages[vimeoPages.length - 1]?.dateKey ?? 0 : 0;

    if (vimeoPages.length === 0) {
      return legacyMediaArchivePages as MediaArchivePage[];
    }

    const merged: MediaArchivePage[] = [...vimeoPages.map(({ dateKey: _dateKey, ...page }) => page)];
    let nextPageNumber = merged.length + 1;

    for (const page of legacyPages) {
      const items = page.items.filter((item) => dateKeyFromLabel(item.date) < cutoffDateKey);

      if (items.length === 0) {
        continue;
      }

      merged.push({
        page: nextPageNumber,
        items,
      });
      nextPageNumber += 1;
    }

    return merged;
  } catch {
    return legacyMediaArchivePages as MediaArchivePage[];
  }
}

export const mediaArchiveRevalidateSeconds = ARCHIVE_REVALIDATE_SECONDS;
