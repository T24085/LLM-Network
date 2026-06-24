import type { StaticImageData } from "next/image";

const basePath = process.env.NODE_ENV === "production" ? "/Emmanuel-Church" : "";

export function withBasePath(path: string): string;
export function withBasePath(path: StaticImageData): StaticImageData;
export function withBasePath(path: string | StaticImageData) {
  if (typeof path !== "string") {
    return path;
  }

  if (!path.startsWith("/")) {
    return path;
  }

  return `${basePath}${path}`;
}
