import { cp, readdir, rm } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, "..");
const exportRoot = resolve(repoRoot, "out");

async function syncExport() {
  const entries = await readdir(exportRoot, { withFileTypes: true });

  for (const entry of entries) {
    const source = resolve(exportRoot, entry.name);
    const target = resolve(repoRoot, entry.name);

    await rm(target, { recursive: true, force: true });
    await cp(source, target, { recursive: true, force: true, preserveTimestamps: true });
  }

  console.log(`Synced ${entries.length} exported entries from out/ into the repository root.`);
}

syncExport().catch((error) => {
  console.error(error);
  process.exit(1);
});
