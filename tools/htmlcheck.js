// Tag balance + content checks for a school index.html.   usage: node htmlcheck.js index.html
const fs=require("fs");
const html=fs.readFileSync(process.argv[2],"utf8");
// strip script/style bodies and comments
let s=html.replace(/<script[\s\S]*?<\/script>/g, m=>"<script></script>".padEnd(m.length," "))
          .replace(/<style[\s\S]*?<\/style>/g, m=>"<style></style>".padEnd(m.length," "))
          .replace(/<!--[\s\S]*?-->/g, m=>" ".repeat(m.length));
const VOID=new Set(["meta","link","input","br","hr","img","use","path","circle","ellipse","rect","polygon","line","text","source","wbr"]);
const re=/<(\/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*?)(\/?)>/g;
const stack=[]; let m, errors=0;
function line(i){ return s.slice(0,i).split("\n").length; }
while((m=re.exec(s))){
  const close=m[1]==="/", tag=m[2].toLowerCase(), self=m[4]==="/";
  if(!close){
    if(self||VOID.has(tag)) continue;
    stack.push({tag, line: line(m.index)});
  } else {
    if(VOID.has(tag)) continue;
    const top=stack[stack.length-1];
    if(!top){ console.log("stray close </"+tag+"> at line", line(m.index)); errors++; continue; }
    if(top.tag!==tag){
      // find nearest matching
      let j=stack.length-1; while(j>=0 && stack[j].tag!==tag) j--;
      if(j<0){ console.log("close </"+tag+"> without open at line", line(m.index), "(top is <"+top.tag+"> from line "+top.line+")"); errors++; continue; }
      for(let k=stack.length-1;k>j;k--) { console.log("unclosed <"+stack[k].tag+"> opened at line", stack[k].line, "closed implicitly by </"+tag+"> at line", line(m.index)); errors++; }
      stack.length=j;
    } else stack.pop();
  }
}
for(const t of stack){ console.log("never closed <"+t.tag+"> from line", t.line); errors++; }
// content checks: quiz answer in range, every widget defined, no duplicate ids
const qs=[...html.matchAll(/<div class="q"[^>]*>/g)];
qs.forEach((m,k)=>{ const a=/data-a="(\d+)"/.exec(m[0]), seg=html.slice(m.index, k+1<qs.length? qs[k+1].index : undefined), n=(seg.match(/class="opt"/g)||[]).length;
  if(!a||+a[1]>=n){ console.log("quiz at line", line(m.index), "data-a", a?a[1]:"missing", "but", n, "options"); errors++; } });
const viz=new Set([...html.matchAll(/VIZ\.([\w$]+)\s*=/g)].map(m=>m[1]));
for(const m of html.matchAll(/data-viz="([^"]+)"/g)) if(!viz.has(m[1])){ console.log("widget", m[1], "at line", line(m.index), "has no VIZ."+m[1]+" function"); errors++; }
const ids={}; for(const m of s.matchAll(/\sid="([^"]+)"/g)){ if(ids[m[1]]){ console.log("duplicate id", m[1], "at line", line(m.index)); errors++; } ids[m[1]]=1; }
console.log("errors:", errors);
