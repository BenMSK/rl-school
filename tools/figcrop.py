# Crop "Figure N" from a PDF: find the caption block, grow a box over the drawings/images above it, render it.
# usage: python figcrop.py <pdf> <figure label e.g. 1 or 2.1> <out.png> [zoom]
import sys, re, pymupdf as fitz
pdf, lab, out = sys.argv[1:4]; zoom = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0; pad = float(sys.argv[5]) if len(sys.argv) > 5 else 5
doc = fitz.open(pdf)
pat = re.compile(r'^\s*Figure\s*' + re.escape(lab) + r'(?!\d)(?!\.\d)\s*[:.|]?\s', re.I)
M = 22
for page in doc:
    blocks = page.get_text("blocks")
    caps = [b for b in blocks if b[6] == 0 and pat.match(b[4]) and len(b[4].strip()) > 15]
    if not caps: continue
    c = caps[0]; cx0, cy0, cx1, cy1 = c[:4]; H = page.rect.height; W = page.rect.width
    items = [fitz.Rect(d["rect"]) for d in page.get_drawings()] + [fitz.Rect(i["bbox"]) for i in page.get_image_info()]
    items = [r for r in items if r.y1 <= cy0 + 3 and r.height < H * 0.85 and r.width < W * 0.98 and not r.is_empty]
    seed = fitz.Rect(cx0 - 20, cy0 - 90, cx1 + 20, cy0 + 3); box = None
    for r in items:
        if r.intersects(seed): box = r if box is None else box | r
    if box is None: print("no seed on page", page.number + 1); continue
    changed = True
    while changed:
        changed = False; g = fitz.Rect(box.x0 - M, box.y0 - M, box.x1 + M, box.y1 + M)
        for r in items:
            if r.intersects(g) and not box.contains(r): box |= r; changed = True
    g = fitz.Rect(box.x0 - M, box.y0 - M, box.x1 + M, box.y1 + M)
    for b in blocks:  # pull in figure text (axis labels) that mostly sits inside the box, never the caption or body text
        r = fitz.Rect(b[:4])
        if b[6] == 0 and r.y1 <= cy0 + 1 and (r & g).get_area() > 0.5 * r.get_area() and not pat.match(b[4]): box |= r
    clip = fitz.Rect(box.x0 - pad, box.y0 - 5, box.x1 + 5, min(box.y1 + 5, cy0 - 1)) & page.rect
    page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False).save(out)
    print(out, "page", page.number + 1, "clip", [round(v) for v in clip]); break
else: print("NOT FOUND", pdf, lab)
