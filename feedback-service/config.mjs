import { readFileSync } from 'node:fs';

export const config = JSON.parse(readFileSync(new URL('./config.json', import.meta.url), 'utf8'));
