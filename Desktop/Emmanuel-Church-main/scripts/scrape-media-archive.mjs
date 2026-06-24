import { readFile, writeFile } from "node:fs/promises";

const OUTPUT = new URL("../src/data/media-archive.json", import.meta.url);
const VIMEO_START_URL = "https://vimeo.com/ecabilene/videos";
const MAX_VIMEO_PAGES = Number(process.env.MEDIA_ARCHIVE_MAX_PAGES || "60");

const HTML_ENTITIES = {
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

function decodeHtml(value) {
  return value
    .replace(/&#(\d+);/g, (_, number) => String.fromCodePoint(Number(number)))
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&([a-z]+);/gi, (match, entity) => HTML_ENTITIES[entity] || match);
}

function cleanText(value) {
  return decodeHtml(value).replace(/\s+/g, " ").trim();
}

function formatDateLabel(datetime) {
  const [year, month, day] = datetime.slice(0, 10).split("-").map(Number);
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "UTC",
    month: "long",
    day: "numeric",
    year: "numeric",
  }).format(new Date(Date.UTC(year, month - 1, day)));
}

function dateKeyFromLabel(date) {
  return new Date(`${date} 12:00:00 UTC`).getTime();
}

function dateKeyFromDatetime(datetime) {
  const [year, month, day] = datetime.slice(0, 10).split("-").map(Number);
  return Date.UTC(year, month - 1, day);
}

function extractPageNumber(url) {
  const match = url.match(/page:(\d+)/);
  return match ? Number(match[1]) : 1;
}

async function fetchText(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}: ${response.status} ${response.statusText}`);
  }

  return response.text();
}

function parseVimeoPage(html) {
  const nextHref = html.match(/<link rel="next" href="([^"]+)"/)?.[1] || null;
  const items = [...html.matchAll(/<li id="clip_(\d+)"[\s\S]*?<\/li>/g)].map((match) => {
    const block = match[0];
    const id = Number(match[1]);
    const linkHref = block.match(/<a href="([^"]+)" title="([^"]+)">/)?.[1] || `https://vimeo.com/${id}`;
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
      href: `https://vimeo.com${linkHref.startsWith("/") ? linkHref : `/${linkHref}`}`,
      kind: "video",
    };
  });

  return {
    items,
    nextHref,
  };
}

async function scrapeVimeoArchive() {
  const pages = [];
  let currentUrl = VIMEO_START_URL;
  let pageNumber = 1;

  for (; pageNumber <= MAX_VIMEO_PAGES && currentUrl; pageNumber += 1) {
    const html = await fetchText(currentUrl);
    const { items, nextHref } = parseVimeoPage(html);

    if (items.length === 0) {
      break;
    }

    pages.push({
      page: pageNumber,
      items,
    });

    currentUrl = nextHref ? new URL(nextHref, currentUrl).href : null;
  }

  return pages;
}

async function loadLegacyArchive() {
  const raw = await readFile(OUTPUT, "utf8");
  const archive = JSON.parse(raw);

  return archive.map((page) => ({
    ...page,
    items: page.items.map((item) => ({
      ...item,
      dateKey: item.date ? dateKeyFromLabel(item.date) : 0,
    })),
  }));
}

function mergeArchives(vimeoPages, legacyPages) {
  const cutoffPage = vimeoPages[vimeoPages.length - 1];
  const cutoffItem = cutoffPage?.items?.[cutoffPage.items.length - 1];
  const cutoffKey = cutoffItem?.dateKey ?? 0;

  const merged = [...vimeoPages];
  let nextPageNumber = merged.length + 1;

  for (const page of legacyPages) {
    const items = page.items.filter((item) => item.dateKey < cutoffKey);

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
}

function stripInternalFields(archive) {
  return archive.map((page) => ({
    page: page.page,
    items: page.items.map(({ dateKey, ...item }) => item),
  }));
}

async function scrape() {
  const vimeoPages = await scrapeVimeoArchive();
  const legacyPages = await loadLegacyArchive();
  const archive = mergeArchives(vimeoPages, legacyPages);
  const output = `${JSON.stringify(stripInternalFields(archive), null, 2)}\n`;

  await writeFile(OUTPUT, output, "utf8");
  console.log(`Wrote ${archive.length} pages to ${OUTPUT.pathname}`);
}

scrape().catch((error) => {
  console.error(error);
  process.exit(1);
});
