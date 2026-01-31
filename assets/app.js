
async function fetchText(url){
  const r = await fetch(url, { cache: "no-store" });
  if(!r.ok) throw new Error("HTTP " + r.status);
  return await r.text();
}
async function fetchJson(url){
  const r = await fetch(url, { cache: "no-store" });
  if(!r.ok) throw new Error("HTTP " + r.status);
  return await r.json();
}
function row(name, url, ok, detail){
  return `<tr>
    <td>${name}</td>
    <td><a href="${url}" target="_blank" rel="noopener">${url}</a></td>
    <td class="${ok ? "status-ok":"status-bad"}">${ok ? "OK":"FAIL"}</td>
    <td>${detail || ""}</td>
  </tr>`;
}
async function runTrustInspector(base){
  const el = document.getElementById("trust-table-body");
  if(!el) return;
  el.innerHTML = "";
  const endpoints = [
    ["AI Trust Hub", `${base}/.well-known/ai-trust-hub.json`, "json"],
    ["TFWS v2", `${base}/.well-known/tfws-v2.json`, "json"],
    ["AI Governance", `${base}/.well-known/ai-governance.json`, "json"],
    ["AI Search Publisher", `${base}/.well-known/ai-search.publisher.json`, "json"],
    ["Integrity (sha256)", `${base}/.well-known/sha256.json`, "json"],
    ["Integrity Signature", `${base}/.well-known/sha256.json.minisig`, "text"],
    ["Minisign Public Key", `${base}/.well-known/minisign.pub`, "text"],
    ["ONETOO Sync", `${base}/.well-known/onetoo-sync.json`, "json"],
  ];
  for(const [name,url,type] of endpoints){
    try{
      if(type==="json"){
        const j = await fetchJson(url);
        el.innerHTML += row(name,url,true,`schema: ${j.schema_version || j.schema || "n/a"}`);
      } else {
        const t = await fetchText(url);
        el.innerHTML += row(name,url,true,(t.trim().split("\n")[0]||"").slice(0,80));
      }
    } catch(e){
      el.innerHTML += row(name,url,false,String(e.message||e));
    }
  }
}
window.HGP = { runTrustInspector };
