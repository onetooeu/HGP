// ONETOO Showroom++ Trust Inspector
// Static-only: fetches JSON endpoints and reports status. Falls back to curl snippets.
async function fetchJson(url) {
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text) e.textContent = text;
  return e;
}

function renderStatusRow(container, name, url, ok, detail) {
  const row = el("div", "trust-row");
  row.appendChild(el("div", "trust-name", name));
  const a = el("a", "trust-url", url);
  a.href = url; a.target = "_blank"; a.rel="noopener";
  row.appendChild(a);
  row.appendChild(el("div", ok ? "trust-ok" : "trust-fail", ok ? "OK" : "FAIL"));
  row.appendChild(el("div", "trust-detail", detail || ""));
  container.appendChild(row);
}

async function runInspector(baseUrl) {
  const out = document.getElementById("trust-results");
  out.innerHTML = "";
  const endpoints = [
    ["AI Trust Hub", `${baseUrl}/.well-known/ai-trust-hub.json`],
    ["TFWS v2", `${baseUrl}/.well-known/tfws-v2.json`],
    ["AI Governance", `${baseUrl}/.well-known/ai-governance.json`],
    ["AI Search Publisher", `${baseUrl}/.well-known/ai-search.publisher.json`],
    ["Integrity (sha256)", `${baseUrl}/.well-known/sha256.json`],
    ["Integrity Signature", `${baseUrl}/.well-known/sha256.json.minisig`],
    ["Minisign Public Key", `${baseUrl}/.well-known/minisign.pub`],
    ["ONETOO Sync", `${baseUrl}/.well-known/onetoo-sync.json`],
  ];

  for (const [name, url] of endpoints) {
    try {
      if (url.endsWith(".minisig") || url.endsWith(".pub")) {
        const res = await fetch(url, { cache:"no-store" });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const t = await res.text();
        renderStatusRow(out, name, url, true, `${t.trim().split("\n")[0].slice(0, 80)}`);
      } else {
        const j = await fetchJson(url);
        renderStatusRow(out, name, url, true, `schema: ${j.schema_version || j.schema || "n/a"}`);
      }
    } catch (e) {
      renderStatusRow(out, name, url, false, String(e.message || e));
    }
  }

  const curl = document.getElementById("trust-curl");
  curl.textContent =
`# Fallback (no browser CORS needed)
curl -sS ${baseUrl}/.well-known/ai-trust-hub.json | head
curl -sS ${baseUrl}/.well-known/tfws-v2.json | head
curl -sS ${baseUrl}/.well-known/sha256.json | head

# Verify integrity signature (requires minisign)
minisign -Vm sha256.json -x sha256.json.minisig -p minisign.pub
`;
}

window.HGPInspector = { runInspector };
