#!/usr/bin/env node
/**
 * Compatibility shim for legacy invocations.
 *
 * Favicon handling now lives in helper-paths-builder.js, which also repairs
 * helper asset paths. Keep this file so older commands still work.
 *
 * Usage: node favicon-builder.js
 */
const { main } = require('./helper-paths-builder');

if (require.main === module) {
  console.warn('⚠️  favicon-builder.js is deprecated. Running helper-paths-builder.js instead.');
  main();
}
