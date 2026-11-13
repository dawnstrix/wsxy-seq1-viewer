#!/usr/bin/env python3
"""生成极简单文件版 lite.html：不依赖 assets，双击即用。"""
import csv, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")

def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))

ops = []
for r in read("operators.csv"):
    ops.append({
        "n": r["干员"], "r": int(r["等阶"]), "c": r["职业"],
        "b": [x for x in r["盟约"].split(" / ") if x],
        "t": r["特质类型"], "a": r["初始特质"], "e": r["精锐特质"],
    })
bonds = {r["盟约"]: r["类型"] for r in read("bonds.csv")}

payload = json.dumps({"ops": ops, "bonds": bonds}, ensure_ascii=False).replace("</", "<\\/")

html = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>卫戍协议 序列I · 极简查询</title>
<style>
:root{--bg:#0f1419;--fg:#e6edf3;--dim:#93a1b0;--line:#2b3440;--card:#1b2129;--acc:#5fe0a0;
--r1:#39434d;--r2:#1f6f4f;--r3:#2b6fa8;--r4:#6b4fae;--r5:#d9a72c;--r6:#f07a1f}
@media (prefers-color-scheme: light){
:root{--bg:#f4f6f2;--fg:#1e2a23;--dim:#5f7063;--line:#d3dbd0;--card:#fff;--acc:#2f7d5b}
}
*{box-sizing:border-box}
body{margin:0;overflow-x:hidden;background:var(--bg);color:var(--fg);font:14px/1.6 -apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}
header{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 16px;z-index:5}
h1{margin:0;font-size:16px;letter-spacing:.05em}
.sub{color:var(--dim);font-size:12px;margin-top:2px}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
input,select{background:var(--card);border:1px solid var(--line);color:var(--fg);border-radius:7px;padding:6px 10px;font-size:13px;outline:none}
input{flex:1;min-width:180px}
input:focus,select:focus{border-color:var(--acc)}
.ranks{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.ranks button{background:var(--card);border:1px solid var(--line);color:var(--fg);border-radius:6px;padding:2px 10px;cursor:pointer;font-size:12px}
.ranks button.on{border-color:var(--acc);color:var(--acc)}
main{max-width:1000px;margin:0 auto;padding:12px 16px 60px}
.count{color:var(--dim);font-size:12px;margin-bottom:6px}
.row{display:grid;grid-template-columns:176px 1fr;gap:12px;align-items:start;border-bottom:1px solid var(--line);padding:9px 6px;cursor:pointer}
.row>div{min-width:0}
.row:hover{background:color-mix(in srgb,var(--acc) 8%,transparent)}
.nm{display:flex;align-items:center;gap:6px;font-weight:600}
.rank{display:inline-block;min-width:22px;text-align:center;border-radius:5px;font-size:12px;font-weight:700;padding:0 4px;background:var(--r1);color:#fff}
.r2{background:var(--r2)}.r3{background:var(--r3)}.r4{background:var(--r4)}.r5{background:var(--r5)}.r6{background:var(--r6)}
.cls{color:var(--dim);font-size:12.5px}
.bonds{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:3px}
.b{font-size:11px;border:1px solid var(--line);border-radius:99px;padding:0 7px;color:var(--dim);white-space:nowrap}
.b.core{color:var(--acc);border-color:color-mix(in srgb,var(--acc) 45%,var(--line))}
.traits{font-size:12.5px}
.t{display:flex;gap:6px;margin-top:2px}
.t b{color:var(--dim);font-weight:400;flex:none;width:30px;font-size:11.5px;padding-top:1px}
.tx{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.row.open .tx{white-space:pre-wrap;overflow:visible}
.row.open{background:var(--card);border-radius:8px;border-bottom-color:transparent}
.empty{color:var(--dim);text-align:center;padding:40px 0}
footer{color:var(--dim);font-size:11px;text-align:center;padding:20px 16px 40px}
@media(max-width:640px){
 .row{grid-template-columns:1fr;gap:4px}
 .cls{order:3}
}
</style>
</head>
<body>
<header>
  <h1>卫戍协议 · 规程 序列I</h1>
  <div class="sub">极简查询 · 143 干员 / 26 盟约 · 数据抓取 2026-11-13</div>
  <div class="bar">
    <input id="q" type="search" placeholder="搜索干员 / 盟约 / 特质…" autocomplete="off">
    <select id="cls"><option value="">全部职业</option></select>
    <select id="bond"><option value="">全部盟约</option></select>
  </div>
  <div class="ranks" id="ranks"></div>
</header>
<main>
  <div class="count" id="count"></div>
  <div id="list"></div>
</main>
<footer>数据来自 PRTS wiki / 官方 gamedata · 非官方工具 · 点击条目展开全文</footer>
<script>
const D = __PAYLOAD__;
const RN = "ⅠⅡⅢⅣⅤⅥ";
const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const state = { q: "", r: new Set(), c: "", b: "" };

const classes = [...new Set(D.ops.map(o => o.c))].filter(Boolean).sort();
const bondNames = [...new Set(D.ops.flatMap(o => o.b))].sort((a, b) => a.localeCompare(b, "zh"));

$("#cls").insertAdjacentHTML("beforeend", classes.map(c => `<option>${esc(c)}</option>`).join(""));
$("#bond").insertAdjacentHTML("beforeend", bondNames.map(b => `<option>${esc(b)}</option>`).join(""));
$("#ranks").innerHTML = `<button data-r="0" class="on">全部</button>` +
  [1,2,3,4,5,6].map(n => `<button data-r="${n}">${RN[n-1]}</button>`).join("");
$("#ranks").addEventListener("click", e => {
  const btn = e.target.closest("button[data-r]"); if (!btn) return;
  const r = +btn.dataset.r;
  if (r === 0) state.r.clear();
  else state.r.has(r) ? state.r.delete(r) : state.r.add(r);
  syncRankButtons(); render();
});
function syncRankButtons(){
  document.querySelectorAll("#ranks button").forEach(b => {
    const r = +b.dataset.r;
    b.classList.toggle("on", r === 0 ? state.r.size === 0 : state.r.has(r));
  });
}
$("#q").addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); render(); });
$("#cls").addEventListener("change", e => { state.c = e.target.value; render(); });
$("#bond").addEventListener("change", e => { state.b = e.target.value; render(); });

function match(o){
  if (state.r.size && !state.r.has(o.r)) return false;
  if (state.c && o.c !== state.c) return false;
  if (state.b && !o.b.includes(state.b)) return false;
  if (!state.q) return true;
  return (o.n + " " + o.c + " " + o.b.join(" ") + " " + o.t + " " + o.a + " " + o.e).toLowerCase().includes(state.q);
}

function render(){
  const rows = D.ops.filter(match);
  $("#count").textContent = `${rows.length} / ${D.ops.length} 名干员`;
  $("#list").innerHTML = rows.length ? rows.map(o => `
    <div class="row" data-n="${esc(o.n)}">
      <div><div class="nm"><span class="rank r${o.r}">${RN[o.r-1]}</span>${esc(o.n)}</div>
        <div class="cls">${esc(o.c || "—")} · ${esc(o.t)}</div></div>
      <div>
        <div class="bonds">${o.b.map(b => `<span class="b ${D.bonds[b]==="核心盟约"?"core":""}">${esc(b)}</span>`).join("")}</div>
        <div class="traits">
          <div class="t"><b>普通</b><div class="tx">${esc(o.a)}</div></div>
          <div class="t"><b>精锐</b><div class="tx">${esc(o.e)}</div></div>
        </div>
      </div>
    </div>`).join("") : `<div class="empty">没有符合条件的干员</div>`;
}
$("#list").addEventListener("click", e => {
  const row = e.target.closest(".row"); if (row) row.classList.toggle("open");
});
render();
</script>
</body>
</html>
"""

with open(os.path.join(ROOT, "lite.html"), "w", encoding="utf-8") as fh:
    fh.write(html.replace("__PAYLOAD__", payload))
print("已生成 lite.html", f"{os.path.getsize(os.path.join(ROOT,'lite.html'))/1024:.0f} KB")
