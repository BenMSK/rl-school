// Rasterize the school icon into apple-touch-icon.png (180), icon-192.png, icon-512.png. No dependencies.
// Edit ICON so it matches the <svg class="logo"> in index.html (64-unit space). The background fills the whole
// square: iOS and Android round the corners themselves.
// usage: node tools/makeicon.js <outdir>
const fs = require("fs"), path = require("path"), zlib = require("zlib");
const outDir = process.argv[2] || ".";

const ICON = {
  bg: ["#E2BB6A", "#D3A350"],            // diagonal gradient, top-left → bottom-right (same colour twice = flat)
  shapes: [                              // painted in order; kinds: rect [x,y,w,h,r] · circle [cx,cy,r] · ellipse [cx,cy,rx,ry] · poly [[x,y],…]
    // Go board corner: a 4×4 grid of lines, then two black and two white stones (AlphaGo, 2016)
    ...[11, 25, 39, 53].flatMap(v => [{ rect: [8, v - 0.8, 48, 1.6, 0], fill: "#5C4326" }, { rect: [v - 0.8, 8, 1.6, 48, 0], fill: "#5C4326" }]),
    { circle: [25, 25, 6.6], fill: "#1A1A1A" }, { circle: [23, 23, 1.8], fill: "#5E5E5E" },
    { circle: [39, 39, 6.6], fill: "#1A1A1A" }, { circle: [37, 37, 1.8], fill: "#5E5E5E" },
    { circle: [39, 25, 6.6], fill: "#5C4326" }, { circle: [39, 25, 5.9], fill: "#FAFAFA" },
    { circle: [25, 39, 6.6], fill: "#5C4326" }, { circle: [25, 39, 5.9], fill: "#FAFAFA" },
  ],
};

const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const lerp = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
function inRect(x, y, [rx, ry, w, hh, r]) {
  if (x < rx || x > rx + w || y < ry || y > ry + hh) return false;
  const cx = Math.max(rx + r, Math.min(x, rx + w - r)), cy = Math.max(ry + r, Math.min(y, ry + hh - r));
  return Math.hypot(x - cx, y - cy) <= r;
}
function inPoly(x, y, pts) { let inside = false; for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) { const [xi, yi] = pts[i], [xj, yj] = pts[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside; } return inside; }
const inside = (x, y, s) =>
  s.rect ? inRect(x, y, s.rect) :
  s.circle ? Math.hypot(x - s.circle[0], y - s.circle[1]) <= s.circle[2] :
  s.ellipse ? ((x - s.ellipse[0]) / s.ellipse[2]) ** 2 + ((y - s.ellipse[1]) / s.ellipse[3]) ** 2 <= 1 :
  s.poly ? inPoly(x, y, s.poly) : false;

const BG1 = hex(ICON.bg[0]), BG2 = hex(ICON.bg[1]), FILLS = ICON.shapes.map(s => hex(s.fill));
function shade(x, y) {
  let c = lerp(BG1, BG2, Math.max(0, Math.min(1, (x + y) / 128)));
  ICON.shapes.forEach((s, i) => { if (inside(x, y, s)) c = FILLS[i]; });
  return c;
}
function render(W) {
  const SS = 4, rows = [];
  for (let py = 0; py < W; py++) {
    const row = Buffer.alloc(1 + W * 3); row[0] = 0;
    for (let px = 0; px < W; px++) {
      let r = 0, g = 0, b = 0;
      for (let sy = 0; sy < SS; sy++) for (let sx = 0; sx < SS; sx++) { const c = shade((px + (sx + 0.5) / SS) * 64 / W, (py + (sy + 0.5) / SS) * 64 / W); r += c[0]; g += c[1]; b += c[2]; }
      const n = SS * SS; row[1 + px * 3] = Math.round(r / n); row[2 + px * 3] = Math.round(g / n); row[3 + px * 3] = Math.round(b / n);
    }
    rows.push(row);
  }
  return png(W, W, Buffer.concat(rows));
}
const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = buf => { let c = 0xFFFFFFFF; for (const b of buf) c = CRC[(c ^ b) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
function chunk(type, data) { const len = Buffer.alloc(4); len.writeUInt32BE(data.length); const td = Buffer.concat([Buffer.from(type, "ascii"), data]); const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td)); return Buffer.concat([len, td, crc]); }
function png(w, hh, raw) { const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(hh, 4); ihdr[8] = 8; ihdr[9] = 2; return Buffer.concat([Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]), chunk("IHDR", ihdr), chunk("IDAT", zlib.deflateSync(raw, { level: 9 })), chunk("IEND", Buffer.alloc(0))]); }

for (const [name, size] of [["apple-touch-icon.png", 180], ["icon-192.png", 192], ["icon-512.png", 512]]) {
  const file = path.join(outDir, name); fs.writeFileSync(file, render(size)); console.log(name, size + "px", fs.statSync(file).size, "bytes");
}
