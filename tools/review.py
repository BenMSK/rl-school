# Review one lesson or paper entry in a private copy of index.html: audit every SVG label (runs off the canvas, overlaps
# another label, crossed by a line) and screenshot each diagram and widget on its own.
# usage: python tools/review.py d8            (or p-dqn)   [dark] [noshot]
# Prints the findings and the PNG paths (view them in any image viewer). Never writes index.html. Needs Microsoft Edge.
import os, re, sys, json, html, shutil, subprocess, tempfile
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
target = sys.argv[1]; scheme = "0" if "dark" in sys.argv[2:] else "1"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
out = os.path.join(tempfile.gettempdir(), "rlreview", target); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
shutil.copytree("img", os.path.join(out, "img"))
base = open("index.html", encoding="utf8").read()
def run(js, name, size="1000,1000", shot=False):
    f = os.path.join(out, name + ".html"); open(f, "w", encoding="utf8").write(base.replace("</body>", "<script>" + js + "</script></body>", 1))
    url = "file:///" + f.replace("\\", "/") + "#" + target
    args = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=10000", "--window-size=" + size, "--blink-settings=preferredColorScheme=" + scheme]
    if shot:
        png = os.path.join(out, name + ".png"); subprocess.run(args + ["--screenshot=" + png, url], capture_output=True, stdin=subprocess.DEVNULL); return png
    r = subprocess.run(args + ["--dump-dom", url], capture_output=True, stdin=subprocess.DEVNULL, text=True, encoding="utf8")
    m = re.search(r'data-out="([^"]*)"', r.stdout); return json.loads(html.unescape(m.group(1))) if m else None
AUDIT = r'''setTimeout(()=>{ const out=[]; try{ const sec=document.getElementById("%s"); let fi=0, vi=0;
 sec.querySelectorAll("figure.fig:not(.pimg) svg[viewBox], .viz").forEach(el=>{ const name=el.classList.contains("viz")?"widget "+(vi++)+" ("+el.dataset.viz+")":"figure "+(fi++);
  (el.matches("svg")?[el]:[...el.querySelectorAll("svg[viewBox]")]).forEach(svg=>{ if(!svg.getBBox().width) return; const vb=svg.viewBox.baseVal;
   const T=[...svg.querySelectorAll("text")].map(t=>{ const b=t.getBBox(), m=t.transform.baseVal.length?t.transform.baseVal.consolidate().matrix:{b:0,e:0}; return (b.width&&!m.b)?{t,s:t.textContent.trim().slice(0,34),x0:b.x+m.e,x1:b.x+m.e+b.width,y0:b.y,y1:b.y+b.height}:null; }).filter(Boolean);
   const L=[...svg.querySelectorAll("line,path,polyline")].map(l=>{ const len=l.getTotalLength?l.getTotalLength():0; const pts=[]; for(let i=0;i<=40;i++){ const p=l.getPointAtLength(len*i/40); pts.push(p); } return pts; });
   T.forEach(a=>{ if(a.x0<vb.x-1||a.x1>vb.x+vb.width+1) out.push(name+": «"+a.s+"» runs off the canvas");
     T.forEach(c=>{ if(c===a||c.t.compareDocumentPosition(a.t)&Node.DOCUMENT_POSITION_PRECEDING) return; const w=Math.min(a.x1,c.x1)-Math.max(a.x0,c.x0), h=Math.min(a.y1,c.y1)-Math.max(a.y0,c.y0); if(w>1&&h>2) out.push(name+": «"+a.s+"» overlaps «"+c.s+"»"); });
     if(!a.t.dataset.top&&L.some(pts=>pts.filter(p=>p.x>a.x0+2&&p.x<a.x1-2&&p.y>a.y0+3&&p.y<a.y1-3).length>=2)) out.push(name+": a line crosses «"+a.s+"»"); }); }); });
 }catch(e){ out.push("audit error: "+e.message); } document.body.setAttribute("data-out",JSON.stringify(out)); },1200);''' % target
ISO = r'''setTimeout(()=>{ const sec=document.getElementById("%s"); const els=[...sec.querySelectorAll("figure.fig:not(.pimg), .viz")]; const keep=els[%d];
 [...sec.children].forEach(c=>{ if(!(c===keep||c.contains(keep))) c.style.display="none"; }); if(keep.parentElement!==sec) [...keep.parentElement.children].forEach(c=>{ if(c!==keep) c.style.display="none"; });
 const nav=document.querySelector(".dnav"); if(nav) nav.style.display="none"; window.dispatchEvent(new HashChangeEvent("hashchange")); },900);'''
findings = run(AUDIT, "audit"); findings = ["(audit failed to run)"] if findings is None else findings
print("AUDIT", target, "-", len(findings), "findings"); [print("  " + f) for f in findings]
frag = re.search(r'id="%s"[^>]*>(.*?)</(section|article)>' % re.escape(target), base, re.S).group(1)
n = len(re.findall(r'<figure class="fig">|class="viz"', frag))
for i in range(0 if "noshot" in sys.argv[2:] else n): print("PNG", run(ISO % (target, i), "el%02d" % i, size="1000,1400", shot=True))
