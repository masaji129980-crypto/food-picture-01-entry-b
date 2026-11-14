// "Sate Grill Night" — food-picture-01 entry (Node 22, standard library only).
// Its picture is the entry.png beside this file, drawn in code by draw.py, and
// the program copies it to /output/entry.png. The gate takes a whole PNG or
// JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly
// the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

// Fail loudly instead of copying nothing if the picture is missing.
const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) throw new Error('entry.png is missing from the repository');

copyFileSync(source, join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
