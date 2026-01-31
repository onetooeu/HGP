
(function(){
  const KEY = "hgpedu_theme_safe_mode";
  function setSafe(on){
    document.body.classList.toggle("safe-mode", on);
    try{ localStorage.setItem(KEY, on ? "1" : "0"); }catch(e){}
  }
  function init(){
    let safe = false;
    try{ safe = localStorage.getItem(KEY)==="1"; }catch(e){}
    setSafe(safe);

    // Fake 90s counter (deterministic-ish)
    const now = new Date();
    const seed = (now.getUTCFullYear()*10000 + (now.getUTCMonth()+1)*100 + now.getUTCDate());
    const counter = (seed * 7919) % 900000 + 100000;
    const el = document.getElementById("warez-counter");
    if(el) el.textContent = String(counter);

    // Random slogan
    const slogans = [
      "WELCOME TO HGPeDU :: TRUST FIRST / FEAR NEVER",
      "NEON MODE ENABLED :: STATIC WEB, LIVING PIPELINE",
      "ISSUE-DRIVEN PORTAL :: AUTOPILOT ONLINE",
      "TFWS v2 READY :: ONETOO INTEGRATION ACTIVE",
      "NO BACKEND. NO EXCUSES. PURE VERIFIED CONTENT."
    ];
    const sEl = document.getElementById("warez-slogan");
    if(sEl) sEl.textContent = slogans[Math.floor(Math.random()*slogans.length)];

    // Toggle button
    const btn = document.getElementById("btn-safe-toggle");
    if(btn){
      btn.addEventListener("click", ()=>{
        const on = !document.body.classList.contains("safe-mode");
        setSafe(on);
        btn.textContent = on ? "SAFE MODE: ON" : "SAFE MODE: OFF";
      });
      btn.textContent = document.body.classList.contains("safe-mode") ? "SAFE MODE: ON" : "SAFE MODE: OFF";
    }

    // Local guestbook (pure client-side)
    const gForm = document.getElementById("guestbook-form");
    const gList = document.getElementById("guestbook-list");
    const gKey = "hgpedu_guestbook_v1";
    function render(){
      if(!gList) return;
      let items=[];
      try{ items = JSON.parse(localStorage.getItem(gKey)||"[]"); }catch(e){}
      gList.innerHTML = "";
      for(const it of items.slice(-12).reverse()){
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `<div class="badge">${it.ts}</div><div style="margin-top:8px;font-family:var(--mono);color:var(--neonG);">${escapeHtml(it.name||"anon")}</div><div style="margin-top:6px;color:var(--muted);">${escapeHtml(it.msg||"")}</div>`;
        gList.appendChild(div);
      }
    }
    function escapeHtml(s){ return String(s).replace(/[&<>"']/g, m=>({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[m])); }
    if(gForm){
      gForm.addEventListener("submit",(e)=>{
        e.preventDefault();
        const name = (document.getElementById("gb-name")?.value||"").trim().slice(0,40);
        const msg = (document.getElementById("gb-msg")?.value||"").trim().slice(0,220);
        if(!msg) return;
        let items=[];
        try{ items = JSON.parse(localStorage.getItem(gKey)||"[]"); }catch(e){}
        items.push({ts:new Date().toISOString().replace("T"," ").slice(0,19)+"Z", name, msg});
        localStorage.setItem(gKey, JSON.stringify(items));
        document.getElementById("gb-msg").value="";
        render();
      });
      render();
    }
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
