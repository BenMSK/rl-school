# Korean mode. ko.html is GENERATED from index.html (the only source) + the translations in i18n/ko/. Never edit ko.html.
#   python tools/i18n.py extract          refresh i18n/ko/<chunk>.en.txt from index.html; re-key existing .ko.txt (new or changed units get "TODO")
#   python tools/i18n.py check [chunk]    validate translations (tags kept, numbers kept, nothing missing)
#   python tools/i18n.py build [chunk] [out.html]   write ko.html (with a chunk name: only that chunk + common + ui, for previews)
#   python tools/i18n.py js <widget|data> print one widget's source, or the data JSON (lines are long; use this instead of an editor)
# Text: <chunk>.en.txt holds numbered units ("@@ 12" header, then the HTML of one text block); <chunk>.ko.txt holds the
# same numbers with the Korean ("=" alone means: keep the English as is). Chunks: common (blocks repeated in 3+ places),
# ui (header, overview, footer), d1..d14, p-<paper>.
# Script: js.<name>.txt holds snippet pairs: "@@ <widget name | data | *>", the exact English source snippet, "==", the Korean one.
import re, sys, os, glob, json, subprocess, collections
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
D = "i18n/ko"
INLINE = set("a strong b em i sub sup code span tspan br img".split())
SKIP = {"script", "style", "pre"}
TOK = re.compile(r"<!--.*?-->|<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>", re.S)
ATTR = re.compile(r'\s(alt|aria-label|content)="([^"]*)"')
SRC = re.compile(r'<a class="src".*?</a>', re.S)
plain = lambda t: re.sub(r"&#?\w+;", " ", re.sub(r"<[^>]+>", " ", t))
has = lambda t: re.search(r"[A-Za-z]{2}", plain(SRC.sub(" ", t)))
read = lambda f: open(f, encoding="utf8").read()

def units(s):
    """[(start, end, kind)] of every translatable run: maximal inline content inside a block, plus alt/aria-label values."""
    out = []; run = None; pos = 0
    def flush(end):
        nonlocal run
        if run is None: return
        a, b = run, end; run = None
        while a < b and s[a].isspace(): a += 1
        while b > a and s[b-1].isspace(): b -= 1
        if has(s[a:b]): out.append((a, b, ""))
    while True:
        m = TOK.search(s, pos)
        if not m: break
        if run is None and s[pos:m.start()].strip(): run = pos
        pos = m.end(); name = (m.group(2) or "").lower()
        if not name or name not in INLINE: flush(m.start())
        elif run is None: run = m.start()
        if name and not m.group(1):
            for am in ATTR.finditer(m.group(3)):
                if am.group(1) == "content" and 'name="description"' not in m.group(3): continue
                if has(am.group(2)): out.append((m.start(3) + am.start(2), m.start(3) + am.end(2), "attr"))
            if name in SKIP: pos = s.index("</" + name, pos)
    flush(len(s))
    runs = [(a, b) for a, b, k in out if not k]  # an attribute inside a text run travels with its tag, untranslated
    return sorted(u for u in out if not u[2] or not any(a <= u[0] < b for a, b in runs))

def chunker(s):
    spans = [(m.start(), s.index("</section>", m.start()), "d" + m.group(1)) for m in re.finditer(r'<section class="day" data-day="([1-9]\d*)"', s)]
    spans += [(m.start(), s.index("</article>", m.start()), m.group(1)) for m in re.finditer(r'<article class="entry" id="([\w-]+)"', s)]
    return lambda p: next((c for a, b, c in spans if a <= p < b), "ui")

def chunked(s):
    """{chunk: [(en, kind)]} in document order, deduplicated; blocks seen in 3+ chunks move to 'common'."""
    ch = chunker(s); U = [(s[a:b], k, ch(a)) for a, b, k in units(s)]
    seen = collections.defaultdict(set)
    for en, k, c in U: seen[en].add(c)
    out = collections.defaultdict(list); done = set()
    for en, k, c in U:
        c = "common" if len(seen[en]) >= 3 else c
        if (c, en) not in done: done.add((c, en)); out[c].append((en, k))
    return out

def parse(f):
    out = {}; cur = None
    for line in read(f).split("\n"):
        if line.startswith("@@ "): cur = line[3:].strip(); out[cur] = []
        elif cur is not None: out[cur].append(line)
    return {k: "\n".join(v).strip("\n") for k, v in out.items()}

def wrap(t):  # the Read tool cuts lines at 2000 chars: break long units after a sentence (display only; the .ko file is keyed by number)
    while True:
        lines = t.split("\n"); i = next((i for i, l in enumerate(lines) if len(l) > 1500), None)
        if i is None: return t
        l = lines[i]; cut = [m.end() for m in re.finditer(r"[.:;)] (?=[^<>]*(?:<|$))", l) if 300 < m.end() < 1500]
        if not cut: return t
        lines[i] = l[:cut[-1]].rstrip() + "\n" + l[cut[-1]:]; t = "\n".join(lines)

def tm(only=None):
    """{chunk: {en: ko}} from the stored pairs; the .en.txt snapshot is matched to the .ko.txt by number."""
    T = {}
    for f in sorted(glob.glob(D + "/*.en.txt")):
        c = os.path.basename(f)[:-7]; kf = f[:-7] + ".ko.txt"
        if not os.path.exists(kf) or (only and c not in (only, "common", "ui")): continue
        en, ko = parse(f), parse(kf)
        T[c] = {norm(en[k]): (en[k] if ko[k].strip() == "=" else ko[k]) for k in en if k in ko and "TODO" not in k and ko[k].strip()}
    return T
norm = lambda t: re.sub(r"\s+", " ", t).strip()

def extract(s):
    os.makedirs(D, exist_ok=True); T = tm(); G = {k: v for c in T.values() for k, v in c.items()}
    for c, U in chunked(s).items():
        open(f"{D}/{c}.en.txt", "w", encoding="utf8", newline="\n").write("".join(f"@@ {i+1}{' attr' if k else ''}\n{wrap(en)}\n" for i, (en, k) in enumerate(U)))
        if os.path.exists(f"{D}/{c}.ko.txt"):
            body = ""; todo = 0
            for i, (en, k) in enumerate(U):
                ko = T.get(c, {}).get(norm(en)) or G.get(norm(en)); todo += not ko
                body += f"@@ {i+1}{' attr' if k else ''}{'' if ko else ' TODO'}\n{'=' if ko == en else ko or en}\n"
            open(f"{D}/{c}.ko.txt", "w", encoding="utf8", newline="\n").write(body)
            if todo: print(f"{c}: {todo} units need translating (marked TODO in {c}.ko.txt; remove the word TODO when done)")
        print(f"{c}: {len(U)} units, {sum(len(en) for en, k in U)//1000} KB")

NUM = re.compile(r"\d+(?:[.,]\d+)*")
def check(only=None):
    bad = 0
    for f in sorted(glob.glob(D + "/*.en.txt")):
        c = os.path.basename(f)[:-7]; kf = f[:-7] + ".ko.txt"
        if only and c != only: continue
        if not os.path.exists(kf): print(f"{c}: no {c}.ko.txt yet"); bad += 1; continue
        en, ko = parse(f), parse(kf); E = []
        for k in ko:
            if k.replace(" TODO", "") not in en: E.append(f"@@ {k}: no such unit in {c}.en.txt")
        for k, e in en.items():
            e = norm(e)
            if k not in ko: E.append(f"@@ {k}: missing" + (" (still marked TODO)" if k + " TODO" in ko else "")); continue
            o = ko[k].strip()
            if o == "=": continue
            if not o: E.append(f"@@ {k}: empty"); continue
            if k.endswith("attr"):
                if re.search(r'["<>]', o): E.append(f'@@ {k}: an attribute value must not contain " < >')
                continue
            te, to = sorted(re.findall(r"<[^>]+>", e)), sorted(re.findall(r"<[^>]+>", norm(o)))
            if te != to:
                d = collections.Counter(te); d.subtract(to)
                E.append(f"@@ {k}: tags differ from the English: " + ", ".join(("missing " if n > 0 else "extra ") + t[:70] for t, n in d.items() if n)); continue
            st = []
            for m in TOK.finditer(o):
                n = (m.group(2) or "").lower()
                if n in ("br", "img") or not n: continue
                if not m.group(1): st.append(n)
                elif not st or st.pop() != n: E.append(f"@@ {k}: inline tags are not nested properly near </{n}>"); break
            if re.search(r"[<>]", re.sub(r"<[^>]+>", "", o)) or re.search(r"&(?!#?\w+;)", o): E.append(f"@@ {k}: stray < > or & outside a tag (write &lt; &gt; &amp;)")
            ne, no = collections.Counter(NUM.findall(plain(e))), collections.Counter(NUM.findall(plain(o)))
            if ne - no: E.append(f"@@ {k}: numbers in the English but not in the Korean: {' '.join((ne - no).elements())}  (keep digits as digits; ignore only if deliberate)")
            if len(re.findall(r"[A-Za-z]", plain(SRC.sub('', e)))) > 60 and not re.search(r"[가-힣]", o): E.append(f"@@ {k}: no Korean in a long unit; untranslated?")
        print(f"{c}: {len(en)} units, {len(E)} findings"); [print("  " + x) for x in E]; bad += len(E)
    return bad

def jspairs(only=None):
    P = []
    for f in sorted(glob.glob(D + "/js.*.txt")):
        if only and os.path.basename(f)[3:-4] not in (only, "ui"): continue
        scope = None; en = []; ko = None
        for line in read(f).split("\n") + ["@@ end"]:
            if line.startswith("@@ "):
                if scope and ko is not None: P.append((scope, "\n".join(en).strip("\n"), "\n".join(ko).strip("\n"), f))
                scope = line[3:].strip(); en = []; ko = None
            elif line.strip() == "==" and ko is None: ko = []
            elif scope: (en if ko is None else ko).append(line)
    return P

def widgets(js):  # {name: (start, end)} of each "VIZ.name=" block in the script
    M = list(re.finditer(r"^VIZ\.(\w+)=", js, re.M)); stop = js.index("\n// ----------", M[-1].start())
    return {m.group(1): (m.start(), M[i+1].start() if i + 1 < len(M) else stop) for i, m in enumerate(M)}

def build(s, only=None, out="ko.html"):
    T = tm(only); G = {k: v for c in T.values() for k, v in c.items()}; ch = chunker(s); miss = collections.Counter()
    a0 = s.index('<script id="data"'); html, js = s[:a0], s[a0:]
    for a, b, k in reversed(units(html)):
        c = ch(a); en = norm(html[a:b]); ko = T.get(c, {}).get(en) or T.get("common", {}).get(en) or G.get(en)
        if ko: html = html[:a] + ko + html[b:]
        else: miss[c] += 1
    P = jspairs(only); W = widgets(js); d0 = js.index("</script>"); err = []
    for scope in list(W) + ["data", "*"]:  # widget-scoped pairs first, then the shared ones over the whole script
        a, b = W[scope] if scope in W else (0, d0) if scope == "data" else (0, len(js)); seg = js[a:b]
        for sc, en, ko, f in sorted((p for p in P if p[0] == scope), key=lambda p: -len(p[1])):
            if en not in seg: err.append(f"{os.path.basename(f)}: @@ {sc}: snippet not found (or already replaced by a longer one): {en[:90]}"); continue
            seg = seg.replace(en, ko)
        js = js[:a] + seg + js[b:]; W = widgets(js)
    for p in P:
        if p[0] not in W and p[0] not in ("data", "*"): err.append(f"{os.path.basename(p[3])}: unknown scope @@ {p[0]}")
    s = (html + js).replace('<html lang="en">', '<html lang="ko">', 1).replace('href="ko.html"', 'href="index.html"', 1).replace("</head>", KO_HEAD + "</head>", 1)
    open(out, "w", encoding="utf8", newline="\n").write(s)
    tmp = out + ".check.js"; open(tmp, "w", encoding="utf8").write(s[s.rindex("<script>") + 8:s.rindex("</script>")])
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True, encoding="utf8"); os.remove(tmp)
    if r.returncode: err.append("the translated script does not parse:\n" + r.stderr[:1500])
    try: json.loads(s[s.index(">", s.index('<script id="data"')) + 1:s.index("</script>", s.index('<script id="data"'))])
    except ValueError as e: err.append("the data JSON no longer parses: " + str(e))
    print(f"wrote {out}: {len(s)//1000} KB; untranslated units: {dict(miss) or 'none'}; script errors: {len(err)}"); [print("  " + e) for e in err]
    return len(err)

KO_HEAD = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap">
<style>/* Korean mode: Hangul falls through Inter/Space Grotesk to Noto Sans KR; break lines between words, not inside them */
:root{--f-display:"Space Grotesk",Inter,"Noto Sans KR",system-ui,sans-serif;--f-body:Inter,"Noto Sans KR",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
body{word-break:keep-all;overflow-wrap:break-word}</style>
"""

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""; arg = sys.argv[2:]; s = read("index.html")
    if cmd == "extract": extract(s)
    elif cmd == "check": sys.exit(1 if check(*arg[:1]) else 0)
    elif cmd == "build":
        only = next((a for a in arg if not a.endswith(".html")), None); out = next((a for a in arg if a.endswith(".html")), "ko.html")
        sys.exit(1 if build(s, only, out) else 0)
    elif cmd == "js" and arg[0] == "data": a = s.index('<script id="data"'); print(s[a:s.index("</script>", a)])
    elif cmd == "js": a, b = widgets(s[s.rindex("<script>"):])[arg[0]]; print(s[s.rindex("<script>"):][a:b])
    else: print(read(__file__).split("import")[0])
