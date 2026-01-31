// HGPeDU · ONETOO Suite helpers (static, client-side)
// Purpose: render service registry + run optional non-invasive status probes.
//
// NOTE: This file intentionally uses only 'self' script-src and fetch() to allowlisted origins via CSP connect-src.
// If a probe fails due to CORS, it will be shown as "blocked" rather than treated as "down".

(function(){
  function el(tag, attrs, ...kids){
    const n = document.createElement(tag);
    if (attrs){
      for (const [k,v] of Object.entries(attrs)){
        if (k === "class") n.className = v;
        else if (k === "html") n.innerHTML = v;
        else n.setAttribute(k, v);
      }
    }
    for (const k of kids){
      if (k == null) continue;
      if (typeof k === "string") n.appendChild(document.createTextNode(k));
      else n.appendChild(k);
    }
    return n;
  }

  async function fetchJson(url){
    const r = await fetch(url, { cache: "no-store" });
    if (!r.ok) throw new Error("HTTP " + r.status);
    return await r.json();
  }

  function fmtUrl(u){
    try{
      const x = new URL(u);
      return x.origin + x.pathname;
    }catch(_){ return String(u); }
  }

  function badge(text){
    return el("span",{class:"badge",style:"margin-left:8px"}, text);
  }

  function serviceCard(s){
    const top = el("div",{class:"card"});
    const h = el("div",{style:"display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap"});
    const title = el("div",{style:"font-weight:800;font-size:18px"}, s.title || s.id || "service");
    const type = badge((s.type||"service").toUpperCase());
    h.appendChild(el("div",null,title,type));

    const btns = el("div",{style:"display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end"});
    if (s.url) btns.appendChild(el("a",{class:"btn",href:s.url,target:"_blank",rel:"noopener"}, "Open"));
    if (s.base_url) btns.appendChild(el("a",{class:"btn",href:s.base_url,target:"_blank",rel:"noopener"}, "Open base"));
    h.appendChild(btns);

    top.appendChild(h);

    if (s.notes) top.appendChild(el("div",{class:"muted",style:"margin-top:8px"}, s.notes));

    if (s.endpoints && s.endpoints.length){
      const list = el("ul",{style:"margin-top:10px"});
      for (const e of s.endpoints){
        const t = (e.method? (e.method+" ") : "") + (e.path||e.url||"");
        const li = el("li",null, t);
        if (e.url) li.appendChild(el("span",{class:"muted"}, " · " + fmtUrl(e.url)));
        list.appendChild(li);
      }
      top.appendChild(list);
    }

    if (s.well_known && s.well_known.length){
      const list = el("ul",{style:"margin-top:10px"});
      for (const w of s.well_known){
        const u = (s.url? (new URL(w.path, s.url)).toString(): w.path);
        list.appendChild(el("li",null,
          el("a",{href:u,target:"_blank",rel:"noopener"}, w.name || w.path),
          el("span",{class:"muted"}, " · " + (w.path||""))
        ));
      }
      top.appendChild(list);
    }

    return top;
  }

  // Status probes (best-effort, non-invasive)
  async function probe(url){
    // Try GET with small timeout. We cannot use HEAD reliably due to CORS; GET to a light endpoint is better.
    const ctrl = new AbortController();
    const to = setTimeout(()=>ctrl.abort(), 3500);
    try{
      const r = await fetch(url, { cache:"no-store", signal: ctrl.signal });
      clearTimeout(to);
      return { ok: r.ok, status: r.status, statusText: r.statusText };
    }catch(e){
      clearTimeout(to);
      const msg = (e && e.name === "AbortError") ? "timeout" : (e && e.message ? e.message : String(e));
      return { ok:false, error: msg };
    }
  }

  function statusRow(label, url){
    const tr = el("tr",null,
      el("td",null, label),
      el("td",null, el("a",{href:url,target:"_blank",rel:"noopener"}, fmtUrl(url))),
      el("td",{class:"muted"}, "checking…")
    );
    return tr;
  }

  async function runStatus(table, checks){
    const rows = [];
    for (const c of checks){
      const tr = statusRow(c.label, c.url);
      rows.push({tr, c});
      table.querySelector("tbody").appendChild(tr);
    }
    for (const r of rows){
      const cell = r.tr.children[2];
      const res = await probe(r.c.url);
      if (res.ok) cell.textContent = "OK (" + res.status + ")";
      else if (res.error) cell.textContent = "FAIL (" + res.error + ")";
      else cell.textContent = "FAIL (" + (res.status||"?") + ")";
      cell.className = res.ok ? "" : "muted";
    }
  }

  window.__HGPEU_ONETOO = {
    fetchJson, serviceCard, runStatus
  };
})();
