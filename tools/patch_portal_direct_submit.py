#!/usr/bin/env python3
import sys, re, pathlib

BLOCK_SK = '''
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">
      <button class="btn" id="makeJsonBtn" type="button">JSON</button>
      <a class="btn" id="downloadBtn" href="#" download="hgp-submission.json">Stiahnuť JSON</a>
      <a class="btn" id="issueBtn" href="#" target="_blank" rel="noopener">Otvoriť GitHub Issue</a>
      <button class="btn" id="submitOnetooBtn" type="button" title="Experimentálne: priamy submit do ONETOO (bez tokenu, podpis + PoW)">Submit do ONETOO</button>
    </div>

    <div id="onetooSubmitState" class="badge" style="margin-top:10px;display:inline-block">ONETOO submit: EXPERIMENTAL</div>
'''

BLOCK_EN = '''
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">
      <button class="btn" id="makeJsonBtn" type="button">JSON</button>
      <a class="btn" id="downloadBtn" href="#" download="hgp-submission.json">Download JSON</a>
      <a class="btn" id="issueBtn" href="#" target="_blank" rel="noopener">Open GitHub Issue</a>
      <button class="btn" id="submitOnetooBtn" type="button" title="Experimental: direct submit to ONETOO (no token, signature + PoW)">Submit to ONETOO</button>
    </div>

    <div id="onetooSubmitState" class="badge" style="margin-top:10px;display:inline-block">ONETOO submit: EXPERIMENTAL</div>
'''

WIRING = '''
<script src="/assets/onetoo-submit.js?v=20260114-direct-submit"></script>
<script>
(function(){
  function ui(){
    const el = document.getElementById("onetooSubmitState");
    return {
      setState: (st, msg)=>{
        if(!el) return;
        el.textContent = "ONETOO submit: " + st + (msg ? " · " + msg : "");
      }
    };
  }

  function buildPayloadFromForm(){
    return {
      type: "hgp.portal.submission",
      version: "2.0",
      date: new Date().toISOString(),
      title: (document.getElementById("title").value || "").trim(),
      url: (document.getElementById("url").value || "").trim(),
      summary: (document.getElementById("summary").value || "").trim(),
      categories: (document.getElementById("category").value || "").split(",").map(s=>s.trim()).filter(Boolean),
      author: (document.getElementById("author").value || "").trim(),
      contact: ((document.getElementById("contact").value || "").trim() || null),
      license: ((document.getElementById("license").value || "").trim() || "CC BY 4.0"),
      safety: { no_build_instructions: true, no_hv_schematics: true }
    };
  }

  const btn = document.getElementById("submitOnetooBtn");
  if(btn && window.HGPEduDirectSubmit){
    btn.addEventListener("click", async ()=>{
      const u = ui();
      try{
        u.setState("START", "Submitting…");
        await window.HGPEduDirectSubmit.submitPayload(buildPayloadFromForm(), u);
      }catch(e){
        u.setState("ERR", String(e||""));
      }
    });
  }
})();
</script>
'''

def patch(path: pathlib.Path):
    s = path.read_text(encoding="utf-8")
    p = str(path).replace("\\", "/")
    is_en = p.startswith("en/") or "/en/" in p

    if 'id="submitOnetooBtn"' not in s:
        m = re.search(r'(<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">[\s\S]*?<\/div>)', s)
        if not m:
            raise SystemExit(f"Cannot find button row in {path}")
        block = BLOCK_EN if is_en else BLOCK_SK
        s = s[:m.start(1)] + block + s[m.end(1):]

    if "/assets/onetoo-submit.js" not in s:
        s = s.replace("</body>", WIRING + "\n</body>")

    path.write_text(s, encoding="utf-8")

def main():
    if len(sys.argv) < 2:
        print("Usage: patch_portal_direct_submit.py <file1> [file2...]")
        raise SystemExit(2)
    for p in sys.argv[1:]:
        patch(pathlib.Path(p))
        print("PATCHED", p)

if __name__ == "__main__":
    main()
