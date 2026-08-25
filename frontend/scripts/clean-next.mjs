import { rmSync } from "node:fs";
import { join } from "node:path";

// Avoid development-server stalls when a prior production build owns .next.
rmSync(join(process.cwd(), ".next"), { recursive: true, force: true });
