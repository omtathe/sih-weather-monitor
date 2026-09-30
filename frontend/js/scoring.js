// Offline scoring (mirror of ml/extract.py and ml/score.py). Used when the backend is off.
const hav=(a,b,c,d)=>{const R=6371,r=x=>x*Math.PI/180,dl=r(c-a),dn=r(d-b),h=Math.sin(dl/2)**2+Math.cos(r(a))*Math.cos(r(c))*Math.sin(dn/2)**2;return 2*R*Math.asin(Math.sqrt(h))};
function extract(p){
  const t=p.text.toLowerCase();
  let c=CITIES.find(c=>c.a.some(a=>t.includes(a)));
  if(!c&&p.gps){const n=CITIES.map(c=>[hav(p.gps[0],p.gps[1],c.la,c.lo),c]).sort((a,b)=>a[0]-b[0])[0];if(n[0]<150)c=n[1]}
  const ev=EVENTS.find(e=>e[2].some(k=>t.includes(k)));
  return{city:c?c.n:null,state:c?c.s:null,c,event:ev?ev[0]:null,letter:ev?ev[1]:"?"};
}
const isClick=t=>CLICK.some(k=>t.toLowerCase().includes(k));
function verify(p,others){
  const r=[],add=(s,d)=>r.push([s,d]);let s=30;add("Starting score",30);
  const x=p.x;
  if(x.city){s+=10;add("Location found in text: "+x.city,10)}
  if(p.gps&&x.c){const d=hav(p.gps[0],p.gps[1],x.c.la,x.c.lo);if(d<120){s+=15;add("GPS matches the named city",15)}else{s-=25;add("GPS is "+Math.round(d)+" km from the named city",-25)}}
  if(!x.city){s-=15;add("No location could be found",-15)}
  if(x.event){s+=5;add("Event type recognised: "+x.event,5)}
  if(p.trusted){s+=30;add("Trusted source ("+p.src+")",30)}
  if(p.age<30){s-=15;add("Account is only "+p.age+" days old",-15)}else if(p.age>365){s+=5;add("Established account",5)}
  if(p.media){s+=5;add("Photo attached",5)}
  if(ADVISORY.some(a=>a.s===x.state&&a.e===x.event)){s+=20;add("Matches an active IMD advisory",20)}
  const co=others.filter(o=>o.x.city===x.city&&o.x.event===x.event&&x.city&&x.event&&!isClick(o.text));
  if(co.length){s+=10;add(co.length+" other report(s) agree",10)}
  const norm=t=>t.toLowerCase().replace(/\W+/g," ").trim();
  const dup=others.find(o=>norm(o.text)===norm(p.text)||(p.media&&o.media&&o.media===p.media));
  if(dup){s-=40;add("Same text or photo already used in report #"+dup.id,-40)}
  if(isClick(p.text)){s-=25;add("Clickbait wording",-25)}
  if((p.text.match(/!/g)||[]).length>=3||/[A-Z]{6,}/.test(p.text)){s-=10;add("Shouting style (caps or many !)",-10)}
  s=Math.max(0,Math.min(100,s));
  return{score:s,label:s>=70?"Verified":s>=40?"Suspicious":"Fake",reasons:r};
}
