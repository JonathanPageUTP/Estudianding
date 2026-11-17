/* Utilidades compartidas sobre pokedex.js (cargar pokedex.js antes que este archivo). */
(function(){
"use strict";
var K = ["hp","atk","def","spa","spd","spe"];
var SN = {hp:"PS",atk:"Ataque",def:"Defensa",spa:"At. Esp.",spd:"Def. Esp.",spe:"Velocidad"};
function obj(r){
  var b = {}, y = {};
  K.forEach(function(k, j){ b[k] = r[3][j]; y[k] = r[4][j]; });
  var sf = r[7][0] || null, se = r[7][1] || null;
  /* stab: el más fuerte; stabs: el mejor físico (F) y el mejor especial (E) */
  var st = sf && se ? (sf[2] >= se[2] ? sf : se) : (sf || se);
  return {id:r[0], n:r[1], t:r[2], b:b, y:y, a:r[5], pre:r[6], stab:st, stabs:{F:sf, E:se}, ok:!!r[8], eg:r[9] || [], gr:r[10], evo:r[11] || []};
}
var byName = {};
(window.PKDX || []).forEach(function(r){ byName[r[1].toLowerCase()] = r; });
function find(n){ if(!n) return null; var r = byName[String(n).trim().toLowerCase()]; return r ? obj(r) : null; }
function byId(id){ for(var i = 0; i < PKDX.length; i++) if(PKDX[i][0] === id) return obj(PKDX[i]); return null; }
/* Rol aproximado a partir de las estadísticas base */
function rol(p){
  var b = p.b;
  if(b.spe <= 45 && b.def + b.spd >= b.atk + b.spa + 60) return "def";
  if(b.atk >= b.spa + 15) return "fis";
  if(b.spa >= b.atk + 15) return "esp";
  return "mix";
}
function evText(p){
  var s = K.filter(function(k){ return p.y[k]; }).map(function(k){ return "+" + p.y[k] + " " + SN[k]; });
  return s.length ? s.join(" · ") : "nada";
}
function datalist(id){
  var dl = document.getElementById(id); if(!dl) return;
  dl.innerHTML = PKDX.map(function(r){ return '<option value="' + r[1] + '">'; }).join("");
}
/* Cadena de evolución completa, p. ej. "Sandile → Krokorok (nivel 29) → Krookodile (nivel 40)" */
function chain(p){
  var base = p, guard = 0;
  while(base.pre && guard++ < 5){ var q = find(base.pre); if(!q) break; base = q; }
  var lines = [];
  (function walk(x, txt){
    if(!x.evo.length){ lines.push(txt); return; }
    x.evo.forEach(function(e){ var n = find(e[0]); var t = txt + " → <b>" + e[0] + "</b> <small>(" + e[1] + ")</small>"; if(n) walk(n, t); else lines.push(t); });
  })(base, "<b>" + base.n + "</b>");
  if(lines.length === 1 && lines[0] === "<b>" + p.n + "</b>") return "";
  return lines.map(function(l){ return l.split("<b>" + p.n + "</b>").join('<b style="color:var(--accent)">' + p.n + '</b>'); });
}
window.PK = {K:K, SN:SN, find:find, byId:byId, rol:rol, evText:evText, datalist:datalist, chain:chain,
  all:function(){ return PKDX.map(obj); }};
})();
