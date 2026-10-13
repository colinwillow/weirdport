import fs from 'fs';
const DRACO = 'vendor/draco/';
const TMP = 'tools/.vishelp-draco.cjs';
// ---- GLB ----------------------------------------------------------------
function readGLB(p) {
  const b = fs.readFileSync(p);
  let o = 12, json = null, bin = null;
  while (o < b.length) {
    const len = b.readUInt32LE(o), type = b.readUInt32LE(o + 4);
    const d = b.subarray(o + 8, o + 8 + len);
    if (type === 0x4E4F534A) json = JSON.parse(d.toString('utf8'));
    else if (type === 0x004E4942) bin = d;
    o += 8 + len; if (len % 4) o += 4 - (len % 4);
  }
  return { json, bin };
}
const mul = (a, b) => { const o = new Array(16);
  for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) {
    let s = 0; for (let k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k]; o[c * 4 + r] = s; }
  return o; };
function nodeWorld(g) {
  const I = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1];
  const local = n => {
    if (n.matrix) return n.matrix.slice();
    const t = n.translation || [0,0,0], q = n.rotation || [0,0,0,1], s = n.scale || [1,1,1];
    const [x,y,z,w] = q;
    const m = [1-2*(y*y+z*z), 2*(x*y+z*w), 2*(x*z-y*w), 0,
               2*(x*y-z*w), 1-2*(x*x+z*z), 2*(y*z+x*w), 0,
               2*(x*z+y*w), 2*(y*z-x*w), 1-2*(x*x+y*y), 0, 0,0,0,1];
    for (let c = 0; c < 3; c++) for (let r = 0; r < 3; r++) m[c*4+r] *= s[c];
    m[12]=t[0]; m[13]=t[1]; m[14]=t[2]; return m;
  };
  const out = new Array(g.nodes.length).fill(null);
  const walk = (i, parent) => { const n = g.nodes[i], w = mul(parent, local(n)); out[i] = w;
    for (const c of (n.children || [])) walk(c, w); };
  for (const r of g.scenes[g.scene || 0].nodes) walk(r, I);
  return out;
}
const xf = (m, x, y, z) => [m[0]*x+m[4]*y+m[8]*z+m[12], m[1]*x+m[5]*y+m[9]*z+m[13], m[2]*x+m[6]*y+m[10]*z+m[14]];

// ---- draco --------------------------------------------------------------
let D = null;
async function draco() {
  if (D) return D;
  // the repo is "type": "module", so the vendored .js will not require(). A .cjs copy will.
  fs.writeFileSync(TMP, fs.readFileSync(DRACO + 'draco_wasm_wrapper.js'));
  const { createRequire } = await import('module');
  const req = createRequire(import.meta.url);
  const Mod = req(process.cwd() + '/' + TMP);
  D = await Mod({ wasmBinary: fs.readFileSync(DRACO + 'draco_decoder.wasm') });
  return D;
}
async function decodePrim(g, bin, pr) {
  const d = await draco();
  const ext = pr.extensions && pr.extensions['KHR_draco_mesh_compression'];
  if (!ext) return null;
  const bv = g.bufferViews[ext.bufferView];
  const buf = bin.subarray(bv.byteOffset || 0, (bv.byteOffset || 0) + bv.byteLength);
  const dec = new d.Decoder(), ab = new d.DecoderBuffer();
  ab.Init(new Int8Array(buf), buf.length);
  const geom = new d.Mesh();
  const st = dec.DecodeBufferToMesh(ab, geom);
  if (!st.ok() || geom.ptr === 0) throw new Error('draco decode failed: ' + st.error_msg());
  const at = dec.GetAttributeByUniqueId(geom, ext.attributes.POSITION);
  const count = geom.num_points(), nb = count * 3 * 4;
  let ptr = d._malloc(nb);
  dec.GetAttributeDataArrayForAllPoints(geom, at, d.DT_FLOAT32, nb, ptr);
  const pos = new Float32Array(d.HEAPF32.buffer, ptr, count * 3).slice();
  d._free(ptr);
  const nF = geom.num_faces(); ptr = d._malloc(nF * 3 * 4);
  dec.GetTrianglesUInt32Array(geom, nF * 3 * 4, ptr);
  const index = new Uint32Array(d.HEAPU32.buffer, ptr, nF * 3).slice();
  d._free(ptr);
  d.destroy(geom); d.destroy(ab); d.destroy(dec);
  return { pos, index };
}


export { readGLB, nodeWorld, xf, decodePrim };
