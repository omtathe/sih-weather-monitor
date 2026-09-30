// Rendering and event handlers.
const COL={Verified:"var(--ok)",Suspicious:"var(--warn)",Fake:"var(--bad)"};
let sel=null;
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const ago=t=>{const m=Math.round((Date.now()-t)/60000);return m<60?m+" min ago":Math.round(m/60)+" h ago"};
EVENTS.forEach(e=>{const o=document.createElement("option");o.value=e[0];o.textContent=e[0][0].toUpperCase()+e[0].slice(1);$("fe").appendChild(o)});
function pos(p){if(p.gps)return proj(p.gps[0],p.gps[1]);if(p.x.c){const j=(p.id*37%11-5);return proj(p.x.c.la,p.x.c.lo).map((v,i)=>v+j*(i?1:1.4))}return null}
function filtered(){return db.filter(p=>(!$("fe").value||p.x.event===$("fe").value)&&(!$("fl").value||p.label===$("fl").value))}
function render(){
  const f=filtered(),cnt=l=>db.filter(p=>p.label===l).length;
  $("stats").innerHTML=[["Reports",db.length],["Verified",cnt("Verified")],["Suspicious",cnt("Suspicious")],["Fake",cnt("Fake")]].map(a=>`<div class="stat"><b>${a[1]}</b><span>${a[0]}</span></div>`).join("");
  const g={};db.filter(p=>p.label==="Verified"&&p.x.state&&p.x.event).forEach(p=>{const k=p.x.state+"|"+p.x.event;g[k]=(g[k]||0)+1});
  const al=Object.entries(g).map(([k,n])=>{const[s,e]=k.split("|");return{s,e,n,adv:ADVISORY.some(a=>a.s===s&&a.e===e)}}).sort((a,b)=>b.adv-a.adv||b.n-a.n);
  $("alerts").innerHTML=al.length?al.map(a=>`<div class="alert"><b>${esc(a.e)} alert, ${esc(a.s)}</b><small>${a.n} verified report(s)${a.adv?", IMD advisory active":""}</small></div>`).join(""):`<div class="alert none">No alerts yet.</div>`;
  let svg=`<polygon class="land" points="${IN.map(p=>proj(p[1],p[0]).map(v=>v.toFixed(1)).join(",")).join(" ")}"/>`;
  f.forEach(p=>{const q=pos(p);if(!q)return;svg+=`<g class="pin${sel===p.id?" sel":""}" data-id="${p.id}" tabindex="0" role="button" aria-label="Report ${p.id}, ${p.label}"><circle cx="${q[0]}" cy="${q[1]}" r="10" fill="${COL[p.label]}"/><text x="${q[0]}" y="${q[1]}">${p.x.letter}</text><title>${esc(p.text)}</title></g>`});
  $("map").innerHTML=svg;
  $("list").innerHTML=f.length?f.slice().reverse().map(p=>`<div class="item${sel===p.id?" sel":""}" data-id="${p.id}" tabindex="0"><span class="dot" style="background:${COL[p.label]}"></span><div><p>${esc(p.text)}</p><small>${esc(p.src)}, ${ago(p.t)}, ${p.x.city?esc(p.x.city):"location unknown"}, score ${p.score}</small></div></div>`).join(""):`<div class="item">No reports match these filters. Clear a filter to see more.</div>`;
  const p=db.find(d=>d.id===sel);
  $("detail").innerHTML=p?`<span class="tag" style="background:${COL[p.label]}">${p.label}, ${p.score}/100</span><div class="bar"><i style="width:${p.score}%;background:${COL[p.label]}"></i></div><div>${esc(p.text)}</div><ul class="reasons">${p.reasons.map(r=>`<li><span>${esc(r[0])}</span><span class="${r[1]>=0?"plus":"minus"}">${r[1]>0?"+":""}${r[1]}</span></li>`).join("")}</ul>`:"Select a report to see why it got its score.";
}
function pick(e){const el=e.target.closest("[data-id]");if(el){sel=+el.dataset.id;render()}}
["map","list"].forEach(i=>{$(i).addEventListener("click",pick);$(i).addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();pick(e)}})});
$("fe").onchange=$("fl").onchange=render;
$("ex1").onclick=()=>{$("in").value="Heavy flooding in Pune near Swargate, roads blocked and traffic stuck";$("src").value="X";$("acct").value="900";$("med").value="1"};
$("ex2").onclick=()=>{$("in").value="SHOCKING!!! Dam burst in Delhi, 100% TRUE, forward to everyone!!!";$("src").value="X";$("acct").value="6";$("med").value="m1"};
