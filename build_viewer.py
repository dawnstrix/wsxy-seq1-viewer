#!/usr/bin/env python3
"""把 data/ 下的 CSV 打包成一个可离线打开的单文件 HTML 查询器：index.html"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


data = {
    "ops": read("operators.csv"),
    "bonds": read("bonds.csv"),
    "strategies": read("strategies.csv"),
    "equipment": read("equipment.csv"),
    "enemies": read("enemies.csv"),
    "modes": read("modes.csv"),
}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

html = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>卫戍协议·规程 序列I 数据查询</title>
<style>
:root{
--bg:#12161c;--panel:#1b2129;--line:#2b3440;--text:#e6edf3;--dim:#93a1b0;--acc:#4cc2ff;--acctext:#08222f;
--hover:#1e262f;--badge:#26313c;--tagbg:#22303c;--block:#151b22;--imgbg:#0d1117;
--chipbg:#202a34;--chipon:#0d3b2e;--chiponbd:#2f8f68;--chiponfg:#c9ffe9;--chipn:#8fe0c0;
--allbg:#14342a;--allbd:#2a5c47;--allfg:#8fe0c0;
--corebg:#3a2a12;--corebd:#6b4a1c;--corefg:#ffcf8a;
--spbg:#2a1f33;--spbd:#4a3560;--spfg:#d9b8ff;
--scroll:#33404d;--qlvbg:#2a3742;--qlvfg:#b9c8d6;--elitebg:#4a3a12;--elitefg:#ffd88a;
--shadow:0 24px 70px rgba(0,0,0,.55);
}
html[data-theme=protocol]{
--bg:#0a1310;--panel:#0f1d17;--line:#234234;--text:#d8efe3;--dim:#7ea992;--acc:#5fe0a0;--acctext:#04180f;
--hover:#13251c;--badge:#1b3327;--tagbg:#12241b;--block:#0c1813;--imgbg:#0a1410;
--chipbg:#12241b;--chipon:#1c4a35;--chiponbd:#3f9d72;--chiponfg:#bff5d9;--chipn:#7fe0b0;
--allbg:#153324;--allbd:#2f6448;--allfg:#9fe6c4;
--corebg:#2a2412;--corebd:#5f5526;--corefg:#e8cf8a;
--spbg:#231a2e;--spbd:#463459;--spfg:#cbb3e8;
--scroll:#2a4737;--qlvbg:#163023;--qlvfg:#9fc4ad;--elitebg:#3a2f12;--elitefg:#f0d79a;
--shadow:0 30px 80px rgba(0,0,0,.7);
}
html[data-theme=light]{
--bg:#eef1ea;--panel:#fbfcf8;--line:#d3dbd0;--text:#1e2a23;--dim:#5f7063;--acc:#2f7d5b;--acctext:#ffffff;
--hover:#edf4ec;--badge:#dfe8de;--tagbg:#eaf1e8;--block:#f4f8f2;--imgbg:#e6ece4;
--chipbg:#f0f4ee;--chipon:#d8efe2;--chiponbd:#4f9d76;--chiponfg:#14503a;--chipn:#2f7d5b;
--allbg:#e2f0e7;--allbd:#a8ceb9;--allfg:#1f6b4c;
--corebg:#f7ecd7;--corebd:#dcc191;--corefg:#8a5a13;
--spbg:#efe6f7;--spbd:#cdb9e6;--spfg:#5b3d7f;
--scroll:#b9c6ba;--qlvbg:#e6ece4;--qlvfg:#45564b;--elitebg:#f7ecd7;--elitefg:#8a5a13;
--shadow:0 20px 50px rgba(40,60,40,.18);
}
*{box-sizing:border-box}
html[data-theme=protocol] body{background:
  radial-gradient(900px 420px at 50% -140px,rgba(95,224,160,.10),transparent 70%),
  repeating-linear-gradient(180deg,rgba(95,224,160,.028) 0 1px,transparent 1px 4px),
  linear-gradient(180deg,#0b1511,#0a1310 60%)}
html[data-theme=protocol] header{background:#0a1310;border-bottom:1px solid #2a4f3c}
html[data-theme=protocol] .tabs button{border-radius:3px}
html[data-theme=protocol] .tabs button.on{box-shadow:0 0 0 1px rgba(95,224,160,.35),0 0 18px rgba(95,224,160,.18)}
html[data-theme=protocol] .card,html[data-theme=protocol] .filters,html[data-theme=protocol] .mbox{border-radius:5px}
html[data-theme=protocol] .chip,html[data-theme=protocol] .tag,html[data-theme=protocol] .mchip,html[data-theme=protocol] .bchip{border-radius:3px}
html[data-theme=protocol] .mbox::before,html[data-theme=protocol] .mbox::after{content:"";position:absolute;width:16px;height:16px;border:2px solid var(--acc);opacity:.45;pointer-events:none}
html[data-theme=protocol] .mbox::before{left:7px;top:7px;border-right:0;border-bottom:0}
html[data-theme=protocol] .mbox::after{right:7px;bottom:7px;border-left:0;border-top:0}
.sec{display:flex;align-items:center;gap:8px;margin:16px 0 8px;color:var(--acc);font-weight:700;font-size:12.5px;letter-spacing:.12em}
.sec span::before{content:"[ "}
.sec span::after{content:" ]"}
.sec::after{content:"";flex:1;height:1px;background:var(--line);margin-left:8px}
.hero{position:relative;border:1px solid var(--line);border-radius:5px;padding:18px 22px;margin:0 0 14px;overflow:hidden;background:linear-gradient(120deg,var(--panel),var(--bg))}
html[data-theme=protocol] .hero{background:
  radial-gradient(520px 180px at 10% 20%,rgba(95,224,160,.14),transparent 70%),
  repeating-linear-gradient(90deg,rgba(95,224,160,.04) 0 1px,transparent 1px 3px),
  linear-gradient(140deg,#12271d,#0b1712 60%)}
html[data-theme=protocol] .hero::before{content:"";position:absolute;left:10px;top:10px;width:22px;height:22px;border:2px solid var(--acc);border-right:0;border-bottom:0;opacity:.5}
.htitle{font-size:26px;font-weight:800;letter-spacing:.18em;color:var(--text)}
.hsub{font-size:11px;letter-spacing:.3em;color:var(--acc);margin-top:3px}
.hstats{margin-top:10px;color:var(--dim);font-size:12px;display:flex;gap:18px;flex-wrap:wrap}
.hstats b{color:var(--text);font-weight:600}
.cls{width:16px;height:16px;object-fit:contain;vertical-align:-3px;margin-right:4px;opacity:.95}
body{margin:0;background:var(--bg);color:var(--text);overflow-x:hidden;font:14px/1.55 -apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;transition:background .18s,color .18s}
header{padding:16px 20px 8px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:8}
h1{margin:0 0 4px;font-size:18px}
.sub{color:var(--dim);font-size:12px}
.themeBtn{position:absolute;right:18px;top:14px;background:var(--panel);border:1px solid var(--line);color:var(--text);border-radius:99px;padding:5px 12px;font-size:12px;cursor:pointer}
.themeBtn:hover{border-color:var(--acc)}
.tabs{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap}
.tabs button{background:var(--panel);color:var(--text);border:1px solid var(--line);padding:6px 14px;border-radius:99px;cursor:pointer}
.tabs button.on{background:var(--acc);color:var(--acctext);border-color:var(--acc);font-weight:600}
.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
input[type=search],select{background:var(--panel);border:1px solid var(--line);color:var(--text);padding:7px 10px;border-radius:8px;outline:none}
input[type=search]{min-width:220px}
main{padding:14px 20px 70px;max-width:1440px;margin:0 auto}
.count{color:var(--dim);font-size:12px;margin:0 0 8px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}
th{position:sticky;top:0;background:var(--panel);cursor:pointer;white-space:nowrap;z-index:2}
tr:hover td{background:var(--hover)}
.rank{display:inline-block;min-width:26px;text-align:center;border-radius:6px;padding:0 6px;background:var(--badge);font-weight:600}
.r1{background:#39434d;color:#cfd8e0}
.r2{background:#1f6f4f;color:#d6ffe9}
.r3{background:#2b6fa8;color:#e6f3ff}
.r4{background:#6b4fae;color:#efe6ff}
.r5{background:#d9a72c;color:#2a1e00}
.r6{background:#f07a1f;color:#2a1200}
.tag{display:inline-block;background:var(--tagbg);border:1px solid var(--line);border-radius:99px;padding:0 8px;margin:1px 3px 1px 0;font-size:12px;white-space:nowrap}
.core{background:var(--corebg);border-color:var(--corebd);color:var(--corefg)}
.special{background:var(--spbg);border-color:var(--spbd);color:var(--spfg)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column}
.card h2{margin:0 0 6px;font-size:16px}
.eff{white-space:pre-wrap;color:var(--text);flex:1}
.members{color:var(--dim);font-size:12px;margin-top:auto;padding-top:10px;border-top:1px dashed var(--line);line-height:2;min-height:80px}
.mchip{display:inline-flex;align-items:center;gap:5px;background:var(--tagbg);border:1px solid var(--line);border-radius:99px;padding:1px 8px 1px 2px;margin:2px 3px 2px 0;font-size:12px;color:var(--text)}
.mchip img{width:22px;height:22px;border-radius:50%;object-fit:cover;background:var(--imgbg)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px;grid-auto-rows:1fr}
.small{color:var(--dim);font-size:12px}
.avatar{width:34px;height:34px;border-radius:8px;object-fit:cover;vertical-align:middle;margin-right:8px;background:var(--imgbg);flex:none}
.opname{display:flex;align-items:center;gap:6px}
.ico{width:42px;height:42px;border-radius:10px;object-fit:contain;background:#26332d;flex:none}
.cardhead{display:flex;align-items:center;gap:10px;margin-bottom:4px}
.cardhead h2{margin:0}
.ico-s{width:26px;height:26px;object-fit:contain;vertical-align:middle;margin-right:6px;background:#26332d;border-radius:6px}
/* ---- 浮窗 ---- */
[data-op]{cursor:pointer}
[data-op]:hover b{color:var(--acc)}
.modal{position:fixed;inset:0;z-index:60;display:none;align-items:center;justify-content:center;padding:22px}
.modal.show{display:flex}
.mask{position:absolute;inset:0;background:rgba(0,0,0,.66);backdrop-filter:blur(3px)}
html[data-theme=light] .mask{background:rgba(30,40,32,.35)}
.mbox{position:relative;display:flex;flex-direction:column;width:min(720px,100%);max-height:min(86vh,880px);background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px 22px 16px;box-shadow:var(--shadow);overflow:hidden}
.mbox.wide{width:min(940px,100%)}
#mbody{overflow:auto;overscroll-behavior:contain;padding-right:8px;margin-right:-4px}
#mbody::-webkit-scrollbar{width:8px}
#mbody::-webkit-scrollbar-thumb{background:var(--scroll);border-radius:8px}
.mx{position:absolute;right:8px;top:6px;background:transparent;border:0;color:var(--dim);font-size:24px;line-height:1;cursor:pointer;padding:4px 8px;z-index:2}
.mx:hover{color:var(--text)}
.mhead{display:flex;gap:14px;align-items:center;padding-right:34px}
.mhead img.big{width:92px;height:92px;border-radius:14px;object-fit:cover;background:var(--imgbg);flex:none}
.mhead img.big.bondico{object-fit:contain;background:#26332d;padding:8px}
.mname{font-size:20px;font-weight:700;margin-bottom:2px}
.mmeta{color:var(--dim);font-size:12.5px}
.mrow{display:flex;gap:10px;align-items:flex-start;margin-top:12px}
.mkey{color:var(--dim);font-size:12px;min-width:62px;flex:none;padding-top:4px}
.mval{flex:1;min-width:0}
.mblock{background:var(--block);border:1px solid var(--line);border-radius:10px;padding:10px 12px;white-space:pre-wrap;font-size:13.5px;line-height:1.78;color:var(--text)}
/* 普通 / 精锐：上下各占一半 */
.mduo{display:flex;flex-direction:column;gap:8px;height:clamp(220px,32vh,300px)}
.mhalf{flex:1 1 0;display:flex;flex-direction:column;min-height:0;background:var(--block);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
.mhalf .hl{font-size:11.5px;color:var(--dim);letter-spacing:.04em;margin-bottom:2px;flex:none}
.mhalf .ht{flex:1;min-height:0;overflow:auto;white-space:pre-wrap;font-size:13.5px;line-height:1.75}
.mhalf.elite{border-color:var(--corebd)}
.mhalf.elite .hl{color:var(--corefg)}
.bondlink{cursor:pointer}
.bondlink:hover{filter:brightness(1.25)}
.bico{width:16px;height:16px;object-fit:contain;border-radius:50%;vertical-align:-3px;margin-right:4px;background:var(--imgbg)}
.tag .n{color:var(--dim);font-size:11px;margin-left:3px}
.mfoot{display:flex;gap:8px;justify-content:flex-end;margin-top:14px}
.btn{background:var(--tagbg);border:1px solid var(--line);color:var(--text);border-radius:8px;padding:6px 14px;cursor:pointer;font-size:13px}
.btn:hover{border-color:var(--acc)}
.mbgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:8px;margin-top:4px}
.mbop{display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;background:var(--block);border:1px solid var(--line);border-radius:10px;padding:10px 8px;cursor:pointer}
.mbop:hover{border-color:var(--acc);background:var(--hover)}
.mbop > img{width:58px;height:58px;border-radius:10px;object-fit:cover;background:var(--imgbg);flex:none}
.mbop .nm{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.mbop .sm{font-size:11px;color:var(--dim);display:flex;align-items:center;justify-content:center;gap:4px;flex-wrap:wrap}
.backlink{background:transparent;border:0;color:var(--acc);cursor:pointer;font-size:12.5px;padding:0;margin-bottom:8px}
.backlink:hover{text-decoration:underline}
.cardhead.clickable{cursor:pointer;border-radius:8px}
.cardhead.clickable:hover h2{color:var(--acc)}
/* ---- 分类查询 ---- */
.filters{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin-bottom:12px}
.frow{display:flex;gap:8px;align-items:flex-start;padding:6px 0;border-bottom:1px solid var(--line)}
.frow:last-child{border-bottom:0}
.flabel{color:var(--dim);font-size:12px;min-width:66px;padding-top:5px}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{background:var(--chipbg);border:1px solid var(--line);border-radius:8px;color:var(--text);padding:3px 9px;font-size:12px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;user-select:none}
.chip:hover{border-color:var(--acc)}
.chip.on{background:var(--chipon);border-color:var(--chiponbd);color:var(--chiponfg)}
.chip .n{color:var(--dim);font-size:11px}
.chip.on .n{color:var(--chipn)}
.chip img{width:18px;height:18px;object-fit:contain;border-radius:4px}
.allbtn{background:var(--allbg);border:1px solid var(--allbd);color:var(--allfg);border-radius:8px;font-size:12px;padding:3px 8px;cursor:pointer}
.allbtn.off{background:var(--chipbg);border-color:var(--line);color:var(--dim)}
.qlist{display:flex;flex-direction:column}
.qrow{display:flex;gap:12px;padding:6px 8px 6px 10px;border-bottom:1px solid var(--line);border-left:3px solid transparent;align-items:stretch;min-height:112px;transition:background .12s,border-color .12s}
.qrow:hover{background:var(--hover);border-left-color:var(--acc)}
.qrow:hover .qname{color:var(--acc)}
.qava{width:74px;flex:none;text-align:center;display:flex;flex-direction:column;justify-content:center}
.qava img{width:64px;height:64px;border-radius:10px;object-fit:cover;background:var(--imgbg)}
.qname{font-weight:600;font-size:13px}
.qbody{flex:1;min-width:0;display:flex;flex-direction:column}
.qline{flex:1 1 0;display:flex;gap:8px;align-items:center;padding:5px 0;min-width:0}
.qline + .qline{border-top:1px dashed var(--line)}
.qlv{flex:none;font-size:11px;border-radius:5px;padding:1px 6px;background:var(--qlvbg);color:var(--qlvfg);margin-top:2px}
.qlv.elite{background:var(--elitebg);color:var(--elitefg)}
.bchips{display:flex;gap:4px;flex-wrap:wrap;flex:none}
.bchip{display:inline-flex;align-items:center;gap:4px;background:var(--tagbg);border:1px solid var(--line);border-radius:99px;padding:0 7px 0 1px;font-size:11px;color:var(--text);white-space:nowrap}
.bchip img{width:18px;height:18px;object-fit:contain;border-radius:50%;background:var(--imgbg)}
.qtraits{color:var(--text);font-size:12.5px;min-width:0}
.qempty{color:var(--dim);padding:40px 0;text-align:center}
@media(max-width:700px){th:nth-child(6),td:nth-child(6),th:nth-child(7),td:nth-child(7){display:none}}
@media(max-width:560px){
  .modal{padding:10px}
  .mbox{padding:16px 14px 12px;max-height:92vh;border-radius:14px}
  .mhead{gap:10px}
  .mhead img.big{width:72px;height:72px;border-radius:12px}
  .mname{font-size:18px}
  .mrow{gap:6px}
  .mkey{min-width:48px}
  .mbgrid{grid-template-columns:1fr 1fr;gap:6px}
  .mbop{padding:5px 6px}
  .mbop > img{width:34px;height:34px}
  .mfoot .small{display:none}
  .mduo{height:clamp(260px,45vh,340px)}
  .themeBtn{position:static;margin-top:8px}
}
</style>
</head>
<body>
<header>
  <h1>卫戍协议·规程 序列I · 数据查询</h1>
  <button class="themeBtn" id="themeBtn">☀ 浅色</button>
  <div class="sub">数据源：PRTS 镜像官方 gamedata（activity_table / character_table）+ PRTS wiki ｜ 抓取于 2026-11-13</div>
  <div class="tabs" id="tabs"></div>
  <div class="bar" id="bar"></div>
</header>
<main><div class="count" id="count"></div><div id="view"></div></main>
<div class="modal" id="modal" aria-hidden="true">
  <div class="mask" data-close></div>
  <div class="mbox" role="dialog" aria-modal="true">
    <button class="mx" data-close aria-label="关闭">×</button>
    <div id="mbody"></div>
  </div>
</div>
<script>
const D = __PAYLOAD__;
const THEME_KEY='wsxy-theme', THEMES=['protocol','dark','light'], THEME_NAME={protocol:'协议',dark:'深色',light:'浅色'};
function applyTheme(t){
  if(!THEME_NAME[t]) t='protocol';
  document.documentElement.dataset.theme=t;
  try{localStorage.setItem(THEME_KEY,t);}catch(e){}
  const b=document.getElementById('themeBtn');
  if(b) b.textContent = '🎨 '+THEME_NAME[t];
}
(function(){
  let t='protocol';
  try{t=localStorage.getItem(THEME_KEY)||'protocol';}catch(e){}
  applyTheme(t);
})();
const RANK_CLS = {1:'r1',2:'r2',3:'r3',4:'r4',5:'r5',6:'r6'};
const RANK_NUM = {'Ⅰ':1,'Ⅱ':2,'Ⅲ':3,'Ⅳ':4,'Ⅴ':5,'Ⅵ':6};
const TABS = [['query','分类查询'],['ops','干员'],['bonds','盟约'],['strategies','策略'],['equipment','装备'],['enemies','敌人'],['modes','模式']];
const HP=new URLSearchParams(location.hash.replace(/^#/,''));
let tab=HP.get('tab')||'query', sortKey=null, sortAsc=true;
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const bondIcon = {}; D.bonds.forEach(b=>bondIcon[b['盟约']]=b['图标']||'');
const opAvatar = {}; D.ops.forEach(o=>opAvatar[o['干员']]=o['头像']||'');
const CORE = D.bonds.filter(b=>b['类型']==='核心盟约').map(b=>b['盟约']);
const EXTRA = D.bonds.filter(b=>b['类型']!=='核心盟约').map(b=>b['盟约']);
const RANKS = ['Ⅰ','Ⅱ','Ⅲ','Ⅳ','Ⅴ','Ⅵ'];
const TRAITS = [...new Set(D.ops.map(o=>o['特质类型']).filter(Boolean))];
const sel = {rank:new Set(),core:new Set(),extra:new Set(),trait:new Set()};

function tabBtns(){
  $('#tabs').innerHTML=TABS.map(([k,n])=>`<button data-t="${k}" class="${k===tab?'on':''}">${n} <span class="small">${(D[k==='query'?'ops':k]||[]).length}</span></button>`).join('');
  $('#tabs').querySelectorAll('button').forEach(b=>b.onclick=()=>{tab=b.dataset.t;sortKey=null;location.hash='tab='+tab;render();});
}
function rankBadge(r){return `<span class="rank ${RANK_CLS[r]||''}">${'ⅠⅡⅢⅣⅤⅥ'[r-1]||r}</span>`}
function tag(s,cls=''){return s?`<span class="tag ${cls}">${esc(s)}</span>`:''}
function bondChip(name){const ic=bondIcon[name];return `<span class="bchip">${ic?`<img loading="lazy" src="${esc(ic)}" alt="">`:''}${esc(name)}</span>`}

function render(){
  tabBtns();
  if(tab==='query'){ $('#bar').innerHTML=''; renderQuery(); return; }
  $('#bar').innerHTML=filterOpts();
  const q=$('#q'), f1=$('#f1'), f2=$('#f2'), f3=$('#f3');
  const draw=()=>{ let rows=drawRows(); $('#count').textContent=`共 ${rows.length} 条`; };
  [q,f1,f2,f3].forEach(el=>{ if(el){el.oninput=draw; el.onchange=draw;} });
  drawRows();
}

function filterOpts(){
  if(tab==='ops'){
    const ranks=[...new Set(D.ops.map(o=>o['等阶']))].sort();
    const bonds=[...new Set(D.ops.flatMap(o=>o['盟约'].split(' / ')).filter(Boolean))];
    const profs=[...new Set(D.ops.map(o=>o['职业']).filter(Boolean))];
    return `<input type="search" id="q" placeholder="搜索干员 / 特质 / 盟约…">
      <select id="f1"><option value="">全部等阶</option>${ranks.map(r=>`<option>${r}</option>`).join('')}</select>
      <select id="f2"><option value="">全部盟约</option>${bonds.map(b=>`<option>${esc(b)}</option>`).join('')}</select>
      <select id="f3"><option value="">全部职业</option>${profs.map(p=>`<option>${esc(p)}</option>`).join('')}</select>`;
  }
  if(tab==='bonds') return `<input type="search" id="q" placeholder="搜索盟约 / 成员…">
    <select id="f1"><option value="">全部类型</option><option>核心盟约</option><option>附加盟约</option><option>特殊附加盟约</option></select>`;
  if(tab==='strategies') return `<input type="search" id="q" placeholder="搜索策略 / 发起人 / 效果…">`;
  if(tab==='equipment') return `<input type="search" id="q" placeholder="搜索装备 / 效果…">`;
  if(tab==='enemies') return `<input type="search" id="q" placeholder="搜索敌人…">`;
  return '';
}

function drawRows(){
  const q=$('#q'), f1=$('#f1'), f2=$('#f2'), f3=$('#f3');
  const s=(q?.value||'').trim().toLowerCase(), v1=f1?.value||'', v2=f2?.value||'', v3=f3?.value||'';
  if(tab==='ops'){
    let rows=D.ops.filter(o=>(!s||JSON.stringify(o).toLowerCase().includes(s))&&(!v1||o['等阶']===v1)&&(!v2||o['盟约'].split(' / ').includes(v2))&&(!v3||o['职业']===v3));
    if(sortKey) rows=[...rows].sort((a,b)=>String(a[sortKey]).localeCompare(String(b[sortKey]),'zh')*(sortAsc?1:-1));
    $('#view').innerHTML=`<table><thead><tr>${['等阶','干员','职业','盟约','特质类型','初始特质','精锐特质'].map(h=>`<th data-k="${h}">${h}</th>`).join('')}</tr></thead><tbody>`+
      rows.map(o=>`<tr><td>${rankBadge(+o['等阶'])}</td><td><span class="opname" data-op="${esc(o['干员'])}">${o['头像']?`<img class="avatar" loading="lazy" src="${esc(o['头像'])}" alt="">`:''}<b>${esc(o['干员'])}</b></span></td><td>${esc(o['职业'])}</td>
      <td>${o['盟约'].split(' / ').filter(Boolean).map(b=>tag(b)).join('')}</td><td>${esc(o['特质类型'])}</td>
      <td>${esc(o['初始特质'])}</td><td>${esc(o['精锐特质'])}</td></tr>`).join('')+'</tbody></table>';
    bindSort(); return rows;
  }
  if(tab==='bonds'){
    let rows=D.bonds.filter(b=>(!s||JSON.stringify(b).toLowerCase().includes(s))&&(!v1||b['类型']===v1));
    $('#view').innerHTML='<div class="grid">'+rows.map(b=>`<div class="card">
      <div class="cardhead clickable" data-bond="${esc(b['盟约'])}" title="点击查看该盟约全部干员">${b['图标']?`<img class="ico" loading="lazy" src="${esc(b['图标'])}" alt="">`:''}<h2>${esc(b['盟约'])} ${tag(b['类型'],b['类型']==='核心盟约'?'core':(b['类型']==='特殊附加盟约'?'special':''))}</h2></div>
      <div class="small">${esc(b['激活人数'])} 人激活 ｜ ${esc(b['成员数'])} 名成员</div>
      <div class="eff">${esc(b['效果'])}</div>
      <div class="members">${b['成员'].split(' / ').filter(Boolean).map(m=>`<span class="mchip" data-op="${esc(m)}">${opAvatar[m]?`<img loading="lazy" src="${esc(opAvatar[m])}" alt="">`:''}${esc(m)}</span>`).join('')}</div></div>`).join('')+'</div>';
    return rows;
  }
  if(tab==='strategies'){
    let rows=D.strategies.filter(r=>!s||JSON.stringify(r).toLowerCase().includes(s));
    $('#view').innerHTML=`<table><thead><tr><th>发起人</th><th>策略</th><th>初始生命</th><th>效果</th></tr></thead><tbody>`+
      rows.map(r=>`<tr><td><span class="opname" data-op="${esc(r['发起人'])}">${r['图标']?`<img class="avatar" loading="lazy" src="${esc(r['图标'])}" alt="">`:''}${esc(r['发起人'])}</span></td><td><b>${esc(r['策略'])}</b></td><td>${esc(r['初始生命'])}</td><td class="eff">${esc(r['效果'])}</td></tr>`).join('')+'</tbody></table>';
    return rows;
  }
  if(tab==='equipment'){
    let rows=D.equipment.filter(r=>!s||JSON.stringify(r).toLowerCase().includes(s));
    $('#view').innerHTML=`<table><thead><tr><th>装备</th><th>基础售价</th><th>进阶售价</th><th>基础效果</th><th>进阶效果</th></tr></thead><tbody>`+
      rows.map(r=>`<tr><td><span class="opname">${r['图标']?`<img class="ico-s" loading="lazy" src="${esc(r['图标'])}" alt="">`:''}<b>${esc(r['装备'])}</b></span></td><td>${esc(r['基础售价'])}</td><td>${esc(r['进阶售价'])}</td><td>${esc(r['基础效果'])}</td><td>${esc(r['进阶效果'])}</td></tr>`).join('')+'</tbody></table>';
    return rows;
  }
  if(tab==='enemies'){
    let rows=D.enemies.filter(r=>!s||JSON.stringify(r).toLowerCase().includes(s));
    $('#view').innerHTML=`<table><thead><tr><th>类型</th><th>敌人</th><th>标准</th><th>险境</th><th>绝境</th><th>终极</th><th>说明</th></tr></thead><tbody>`+
      rows.map(r=>`<tr><td>${esc(r['类型'])}</td><td><span class="opname">${r['图标']?`<img class="avatar" loading="lazy" src="${esc(r['图标'])}" alt="">`:''}<b>${esc(r['敌人'])}</b></span></td><td>${esc(r['标准模拟'])}</td><td>${esc(r['险境模拟'])}</td><td>${esc(r['绝境模拟'])}</td><td>${esc(r['终极模拟'])}</td><td class="small">${esc(r['描述'])}</td></tr>`).join('')+'</tbody></table>';
    return rows;
  }
  let rows=D.modes.filter(r=>!s||JSON.stringify(r).toLowerCase().includes(s));
  $('#view').innerHTML=`<table><thead><tr><th>模式</th><th>编号</th><th>说明</th><th>难度</th></tr></thead><tbody>`+
    rows.map(r=>`<tr><td>${esc(r['模式'])}</td><td>${esc(r['编号'])}</td><td>${esc(r['说明'])}</td><td>${esc(r['难度系数'])}</td></tr>`).join('')+'</tbody></table>';
  return rows;
}

function bindSort(){
  $('#view').querySelectorAll('th').forEach(th=>th.onclick=()=>{
    const k=th.dataset.k; if(!k) return;
    if(sortKey===k) sortAsc=!sortAsc; else {sortKey=k;sortAsc=true;}
    render();
  });
}

/* ---------- 分类查询 ---------- */
function matchOp(o, skip){
  const r=String(o['等阶']), b=o['盟约'].split(' / '), t=o['特质类型'];
  if(skip!=='rank' && sel.rank.size && !sel.rank.has(r)) return false;
  if(skip!=='core' && sel.core.size && !b.some(x=>sel.core.has(x))) return false;
  if(skip!=='extra' && sel.extra.size && !b.some(x=>sel.extra.has(x))) return false;
  if(skip!=='trait' && sel.trait.size && !sel.trait.has(t)) return false;
  return true;
}
function facetCount(group, val){
  return D.ops.filter(o=>{
    if(!matchOp(o, group)) return false;
    if(group==='rank') return String(o['等阶'])===String(RANK_NUM[val]||val);
    if(group==='trait') return o['特质类型']===val;
    return o['盟约'].split(' / ').includes(val);
  }).length;
}
function chip(group, val, label, icon){
  const on=sel[group].has(val);
  const n=facetCount(group,val);
  return `<span class="chip ${on?'on':''}" data-g="${group}" data-v="${esc(val)}">${icon?`<img loading="lazy" src="${esc(icon)}" alt="">`:''}${esc(label||val)}<span class="n">${n}</span></span>`;
}
function renderQuery(){
  const rows=D.ops.filter(o=>matchOp(o));
  const frows=[
    ['rank','等阶',RANKS.map(r=>chip('rank',r,r))],
    ['core','核心盟约',CORE.map(b=>chip('core',b,b,bondIcon[b]))],
    ['extra','附加盟约',EXTRA.map(b=>chip('extra',b,b,bondIcon[b]))],
    ['trait','特质词条',TRAITS.map(t=>chip('trait',t,t))]
  ].map(([g,label,chips])=>`<div class="frow"><div class="flabel">${label}</div>
      <button class="allbtn ${sel[g].size?'':'off'}" data-all="${g}">${sel[g].size?'清空':'全选'}</button>
      <div class="chips">${chips.join('')}</div></div>`).join('');
  const list=rows.map(o=>{
    const bonds=o['盟约'].split(' / ').filter(Boolean).map(bondChip).join('');
    return `<div class="qrow" data-op="${esc(o['干员'])}">
      <div class="qava" data-op="${esc(o['干员'])}">${o['头像']?`<img loading="lazy" src="${esc(o['头像'])}" alt="">`:''}
        <div style="margin-top:4px">${rankBadge(+o['等阶'])}</div><div class="qname">${esc(o['干员'])}</div></div>
      <div class="qbody">
        <div class="qline"><span class="qlv">普通</span><span class="bchips">${bonds}</span><span class="qtraits">${esc(o['初始特质'])}</span></div>
        <div class="qline"><span class="qlv elite">精锐</span><span class="bchips">${bonds}</span><span class="qtraits">${esc(o['精锐特质'])}</span></div>
      </div></div>`;
  }).join('');
  $('#view').innerHTML=`<div class="hero"><div class="htitle">卫戍协议</div><div class="hsub">规程 · REGULATION · 序列 I</div>
      <div class="hstats"><span>干员 <b>${D.ops.length}</b></span><span>盟约 <b>${D.bonds.length}</b></span><span>策略 <b>${D.strategies.length}</b></span><span>装备 <b>${D.equipment.length}</b></span></div></div>
    <div class="filters">${frows}</div>
    <div class="qlist">${rows.length?list:'<div class="qempty">没有符合条件的干员</div>'}</div>`;
  const picked=[...sel.rank].map(v=>'等阶 '+v).concat([...sel.core],[...sel.extra],[...sel.trait]);
  $('#count').textContent=`${rows.length} / ${D.ops.length} 名干员`+(picked.length?' ｜ 筛选：'+picked.join('、'):'');
  $('#view').querySelectorAll('.chip').forEach(c=>c.onclick=()=>{
    const g=c.dataset.g, v=c.dataset.v, set=sel[g];
    set.has(v)?set.delete(v):set.add(v); renderQuery();
  });
  $('#view').querySelectorAll('.allbtn').forEach(b=>b.onclick=()=>{
    const g=b.dataset.all;
    if(sel[g].size){sel[g].clear();}
    else{(g==='rank'?RANKS:(g==='core'?CORE:(g==='extra'?EXTRA:TRAITS))).forEach(v=>sel[g].add(v));}
    renderQuery();
  });
}

/* ---------- 浮窗：干员 / 盟约 ---------- */
const modal=$('#modal'), mbody=$('#mbody');
function closeModal(){modal.classList.remove('show');modal.setAttribute('aria-hidden','true');mview='';curBond=null;}
function setWide(on){modal.querySelector('.mbox').classList.toggle('wide',!!on);}
function openModal(){modal.classList.add('show');modal.setAttribute('aria-hidden','false');mbody.scrollTop=0;}
function bondCount(name){return D.ops.filter(o=>o['盟约'].split(' / ').includes(name)).length;}
function rankText(n){return 'ⅠⅡⅢⅣⅤⅥ'[+n-1]||n;}

function openBond(name){
  const b=D.bonds.find(x=>x['盟约']===name); if(!b) return;
  const cls=b['类型']==='核心盟约'?'core':(b['类型']==='特殊附加盟约'?'special':'');
  const ops=D.ops.filter(o=>o['盟约'].split(' / ').includes(name))
                 .sort((a,c)=>((+a['等阶'])-(+c['等阶']))||a['干员'].localeCompare(c['干员'],'zh'));
  const list=ops.map(o=>`<div class="mbop" data-op="${esc(o['干员'])}" title="点击查看 ${esc(o['干员'])}">
      ${o['头像']?`<img loading="lazy" src="${esc(o['头像'])}" alt="">`:''}
      ${rankBadge(+o['等阶'])}
      <div class="nm">${esc(o['干员'])}</div>
      <div class="sm">${o['职业']?`<img class="cls" src="assets/classes/${esc(o['职业'])}.png" alt="">`:''}${esc(o['职业']||'—')} ｜ ${esc(o['特质类型'])}</div></div>`).join('');
  mbody.innerHTML=`
    <div class="mhead">
      ${b['图标']?`<img class="big bondico" src="${esc(b['图标'])}" alt="">`:''}
      <div><div class="mname">${esc(b['盟约'])} ${tag(b['类型'],cls)}</div>
        <div class="mmeta">${esc(b['激活人数'])} 人激活 ｜ 共 ${ops.length} 名干员</div></div></div>
    <div class="sec"><span>盟约效果</span></div>
    <div class="mrow"><div class="mkey">效果</div><div class="mval"><div class="mblock">${esc(b['效果'])}</div></div></div>
    <div class="sec"><span>同盟约干员</span></div>
    <div class="mrow"><div class="mkey">干员</div><div class="mval"><div class="mbgrid">${list||'<span class="small">暂无</span>'}</div></div></div>
    <div class="mfoot"><span class="small" style="margin-right:auto;align-self:center">点击干员查看详细数据</span>
      <button class="btn" data-jump="${esc(name)}">在查询中筛选</button>
      <button class="btn" data-close>关闭</button></div>`;
  setWide(true); mview='bond'; openModal();
}

function openOp(name, fromBond){
  const o=D.ops.find(x=>x['干员']===name); if(!o) return;
  const bonds=o['盟约'].split(' / ').filter(Boolean).map(b=>{
    const bi=D.bonds.find(x=>x['盟约']===b)||{};
    const cls=bi['类型']==='核心盟约'?'core':(bi['类型']==='特殊附加盟约'?'special':'');
    return `<span class="tag bondlink ${cls}" data-bond="${esc(b)}" title="点击查看该盟约全部干员">${bondIcon[b]?`<img class="bico" loading="lazy" src="${esc(bondIcon[b])}" alt="">`:''}${esc(b)}<span class="n">${bondCount(b)}</span></span>`;
  }).join('');
  const back=fromBond?`<button class="backlink" data-bond="${esc(fromBond)}">← 返回「${esc(fromBond)}」</button>`:'';
  mbody.innerHTML=`
    ${back}
    <div class="mhead">
      ${o['头像']?`<img class="big" src="${esc(o['头像'])}" alt="">`:''}
      <div><div class="mname">${esc(o['干员'])}</div>
        <div class="mmeta">${rankBadge(+o['等阶'])} 阶 ｜ ${o['职业']?`<img class="cls" src="assets/classes/${esc(o['职业'])}.png" alt="">`:''}${esc(o['职业']||'—')} ｜ 采购等级 ${esc(o['采购等级']||'—')}</div>
        <div class="mmeta">装备栏 ${esc(o['装备栏']||'—')} ｜ 升级需要 ${esc(o['升级所需数量']||'—')} 个同名</div>
      </div></div>
    <div class="sec"><span>干员数据</span></div>
    <div class="mrow"><div class="mkey">盟约</div><div class="mval">${bonds||'<span class="small">无</span>'}</div></div>
    <div class="mrow"><div class="mkey">特质类型</div><div class="mval">${esc(o['特质类型'])}</div></div>
    <div class="sec"><span>特质</span></div>
    <div class="mrow"><div class="mkey">普通 / 精锐</div><div class="mval"><div class="mduo">
      <div class="mhalf"><div class="hl">普通</div><div class="ht">${esc(o['初始特质'])}</div></div>
      <div class="mhalf elite"><div class="hl">精锐</div><div class="ht">${esc(o['精锐特质'])}</div></div>
    </div></div></div>
    <div class="mfoot"><span class="small" style="margin-right:auto;align-self:center">点击盟约查看该盟约全部干员</span>
      <button class="btn" data-close>关闭</button></div>`;
  setWide(false); mview='op'; openModal();
}

function jumpBond(name){
  const bi=D.bonds.find(x=>x['盟约']===name);
  Object.keys(sel).forEach(k=>sel[k].clear());
  sel[(bi&&bi['类型']==='核心盟约')?'core':'extra'].add(name);
  closeModal(); tab='query'; sortKey=null; location.hash='tab=query'; render();
  window.scrollTo({top:0,behavior:'smooth'});
}

let curBond=null, mview='';
document.addEventListener('click',e=>{
  if(e.target.closest('[data-close]')){closeModal();return;}
  const jp=e.target.closest('[data-jump]'); if(jp){jumpBond(jp.dataset.jump);return;}
  const op=e.target.closest('[data-op]');
  if(op){ openOp(op.dataset.op, mview==='bond'?curBond:null); return; }
  const bd=e.target.closest('[data-bond]');
  if(bd){ curBond=bd.dataset.bond; openBond(bd.dataset.bond); return; }
});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});

if(HP.get('bond')){
  const bn=HP.get('bond'), bi=D.bonds.find(x=>x['盟约']===bn);
  if(bi) sel[bi['类型']==='核心盟约'?'core':'extra'].add(bn);
}
document.getElementById('themeBtn').addEventListener('click',()=>{
  const cur=document.documentElement.dataset.theme||'protocol';
  applyTheme(THEMES[(THEMES.indexOf(cur)+1)%THEMES.length]);
});
if(HP.get('theme')) applyTheme(HP.get('theme'));
render();
if(HP.get('op')) openOp(HP.get('op'));
if(HP.get('bondview')){curBond=HP.get('bondview');openBond(HP.get('bondview'));}
</script>
</body>
</html>
"""

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
    fh.write(html.replace("__PAYLOAD__", payload))
print("已生成", os.path.join(ROOT, "index.html"), f"{os.path.getsize(os.path.join(ROOT,'index.html'))/1024:.0f} KB")
