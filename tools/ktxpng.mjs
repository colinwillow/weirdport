// tools/ktxpng.mjs -- a loose PNG (a sprite sheet, an atlas, a trim) -> .ktx2 beside it.   npm run ktxpng <png> [etc1s]
//
// `npm run ktx` does a GLB's embedded textures; this does the ones `TextureLoader` fetches on their own (m425, F0a-2d-2):
// the impact atlas, the fire and water sheets, the Weirdport trim. Same encoder, same point (resident memory: a 2K RGBA
// sheet is 8 MB on the GPU as a PNG and ~2.7 as UASTC with mips), one difference: **`isYFlip: true`**, because a PNG
// through `TextureLoader` is sampled with `flipY` and a KTX2 through `KTX2Loader` is not -- the flip is baked into the
// pixels so the sheets' frame maths (`grid`, `cut`) reads the same picture. The game takes the twin at load when the bump
// has hashed it (`texTwin`); his PNG stays where it is.
import fs from 'fs';
import { encodeToKTX2 } from 'ktx2-encoder';
import sharp from 'sharp';

const SRC = process.argv[2];
if (!SRC || !/\.png$/i.test(SRC)) { console.error('usage: npm run ktxpng <file.png> [etc1s] [nomip]'); process.exit(1); }
const ETC1S = process.argv.slice(3).includes('etc1s'), NOMIP = process.argv.slice(3).includes('nomip');   // nomip: a sheet sampled with LinearFilter never reads a mip, and the chain is a third of the bytes
const OUT = SRC.replace(/\.png$/i, '.ktx2');
const decode = async buf => { const { data, info } = await sharp(Buffer.from(buf)).ensureAlpha().raw().toBuffer({ resolveWithObject: true }); return { width: info.width, height: info.height, data: new Uint8Array(data) }; };
const src = new Uint8Array(fs.readFileSync(SRC));
const meta = await sharp(Buffer.from(src)).metadata();
const opt = ETC1S ? { isUASTC: false, qualityLevel: 200, compressionLevel: 2 } : { isUASTC: true, needSupercompression: true };
const out = await encodeToKTX2(src, { ...opt, isYFlip: true, generateMipmap: !NOMIP, imageDecoder: decode });
fs.writeFileSync(OUT, Buffer.from(out));
const px = meta.width * meta.height, mip = NOMIP ? 1 : 4 / 3, rgba = px * 4 * mip, res = (ETC1S ? px * .5 : px) * mip;
console.log(SRC + ' -> ' + OUT + '  ' + meta.width + 'x' + meta.height + ' ' + (ETC1S ? 'ETC1S' : 'UASTC + zstd') + (NOMIP ? ', no mips' : '') + ', y-flipped for TextureLoader\'s orientation');
console.log('  wire      ' + (src.length / 1e6).toFixed(1) + ' MB -> ' + (out.byteLength / 1e6).toFixed(1) + ' MB');
console.log('  RESIDENT  ' + (rgba / 1048576).toFixed(0) + ' MB -> ~' + (res / 1048576).toFixed(1) + ' MB');
