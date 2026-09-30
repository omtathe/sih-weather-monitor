// Sample data, city list, event keywords and simulated IMD advisories.
// Keep in sync with ml/data.py
const W=520,H=520,proj=(la,lo)=>[(lo-67)/32*W,(38-la)/32*H];
const IN=[[68.2,23.7],[69,22.4],[70.4,20.9],[72.8,21.2],[72.8,19],[73.8,15.5],[74.8,12.9],[76.2,9.9],[77.5,8.1],[78.2,8.8],[80.3,13.1],[83.3,17.7],[85.8,19.8],[88,21.6],[89,22.2],[88.9,24.5],[89.8,26],[91,26.2],[92,25.5],[92.5,22.5],[94,24],[95.2,26.5],[97.3,28.2],[95,29.3],[92,27.8],[89,27],[88.5,27.8],[88,26.5],[84,27.3],[80.5,29.5],[79,31],[78.7,32.5],[78,35],[76,36],[74.5,34.8],[74,33],[75,32.4],[74.6,31.5],[72,28],[70,26],[68.5,24.3]];
const CITIES=[["Mumbai","Maharashtra",19.08,72.88,["मुंबई","andheri","thane"]],["Pune","Maharashtra",18.52,73.86,["पुणे"]],["Nashik","Maharashtra",20,73.79,[]],["Nagpur","Maharashtra",21.15,79.09,[]],["Amravati","Maharashtra",20.93,77.75,[]],["Delhi","Delhi",28.61,77.21,["दिल्ली"]],["Chennai","Tamil Nadu",13.08,80.27,[]],["Kolkata","West Bengal",22.57,88.36,[]],["Bengaluru","Karnataka",12.97,77.59,["bangalore","bellandur"]],["Hyderabad","Telangana",17.39,78.49,[]],["Ahmedabad","Gujarat",23.02,72.57,[]],["Jaipur","Rajasthan",26.91,75.79,[]],["Lucknow","Uttar Pradesh",26.85,80.95,[]],["Patna","Bihar",25.59,85.14,[]],["Guwahati","Assam",26.18,91.74,[]],["Kochi","Kerala",9.93,76.27,[]],["Bhubaneswar","Odisha",20.3,85.82,[]],["Shimla","Himachal Pradesh",31.1,77.17,[]],["Kedarnath","Uttarakhand",30.73,79.07,[]],["Srinagar","Jammu and Kashmir",34.08,74.8,[]]].map(c=>({n:c[0],s:c[1],la:c[2],lo:c[3],a:[c[0].toLowerCase(),...c[4]]}));
const EVENTS=[["cloudburst","C",["cloudburst","बादल फटा"]],["landslide","L",["landslide","भूस्खलन"]],["flood","F",["flood","waterlogging","बाढ़","overflowing","submerged"]],["hail","H",["hail"]],["heatwave","T",["heatwave","heat wave","लू"]],["cyclone","Y",["cyclone"]],["rain","R",["heavy rain","rain","बारिश"]]];
const ADVISORY=[{s:"Maharashtra",e:"flood"},{s:"Uttarakhand",e:"cloudburst"},{s:"Assam",e:"flood"}];
const CLICK=["shocking","unbelievable","100% true","forward","share this","breaking!!!","must watch"];
const now=Date.now();
const SEED=[
["IMD issues red alert for heavy rain in Mumbai and Thane. Waterlogging likely in low-lying areas.","IMD Official",240,null,0,4000,1],
["Andheri subway completely flooded, buses stopped. Photo from my office window #MumbaiRains","X",200,[19.12,72.84],"m1",900,0],
["मुंबई में भारी बारिश, कई इलाकों में बाढ़ जैसे हालात","News RSS",170,null,0,3000,1],
["SHOCKING!!! Mumbai sea water entering city, 100% TRUE, forward to everyone!!!","X",150,null,0,6,0],
["Flood in Delhi right now, see this video","Facebook",120,[28.6,77.2],"m1",20,0],
["Cloudburst near Kedarnath, road washed away, landslide on the highway","Reddit",95,[30.73,79.07],"k1",500,0],
["Hailstorm hit Nashik grape farms this evening, big hailstones everywhere","Facebook",70,[20,73.78],"n1",300,0],
["Heatwave in Chennai, 47 degrees today, hottest day ever","X",55,null,0,200,0],
["Brahmaputra overflowing in Guwahati, water inside Fancy Bazar shops","Reddit",40,[26.18,91.74],"g1",700,0],
["Pune looks like Venice after the rain, lol","X",20,null,0,1200,0]
].map((r,i)=>({id:i+1,text:r[0],src:r[1],t:now-r[2]*60000,gps:r[3],media:r[4],age:r[5],trusted:!!r[6]}));
