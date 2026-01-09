
(function(){
  const q = (sel, root=document) => root.querySelector(sel);
  const qa = (sel, root=document) => Array.from(root.querySelectorAll(sel));

  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      const s = q('#siteSearch');
      if (s) s.focus();
    }
  });

  function buildIndex(){
    const main = q('main');
    if (!main) return [];
    const items = [];
    qa('[data-search]', main).forEach(el => {
      items.push({ el, text: (el.getAttribute('data-search') + ' ' + el.textContent).toLowerCase() });
    });
    qa('h2,h3,summary', main).forEach(el => items.push({ el, text: el.textContent.toLowerCase() }));
    return items;
  }
  let idx = null;
  function onSearch(){
    const input = q('#siteSearch');
    const out = q('#searchResults');
    if (!input || !out) return;
    if (!idx) idx = buildIndex();

    const term = input.value.trim().toLowerCase();
    out.innerHTML = '';
    if (!term) return;

    const hits = idx.filter(x => x.text.includes(term)).slice(0, 14);
    hits.forEach(h => {
      const a = document.createElement('a');
      a.href = '#';
      a.textContent = h.el.textContent.trim().replace(/\s+/g,' ').slice(0, 120);
      a.className = 'pill';
      a.style.display = 'inline-block';
      a.onclick = (ev) => {
        ev.preventDefault();
        const d = h.el.closest('details');
        if (d) d.open = true;
        h.el.scrollIntoView({behavior:'smooth', block:'start'});
        h.el.style.outline = '2px solid rgba(124,196,255,.55)';
        setTimeout(()=> h.el.style.outline='none', 1200);
      };
      out.appendChild(a);
    });
  }
  document.addEventListener('input', (e) => {
    if (e.target && e.target.id === 'siteSearch') onSearch();
  });

  function landauerCalc(){
    const kB = 1.380649e-23;
    const ln2 = Math.log(2);
    const TEl = q('#T');
    const PEl = q('#P');
    const ebitEl = q('#Ebit');
    const bpsEl = q('#Bps');
    const Tv = q('#Tval');
    const Pv = q('#Pval');
    if (!TEl || !PEl || !ebitEl || !bpsEl) return;

    const T = parseFloat(TEl.value);
    const P = parseFloat(PEl.value);
    const ebit = kB*T*ln2;
    const bps = P/ebit;
    ebitEl.textContent = ebit.toExponential(3) + ' J/bit';
    bpsEl.textContent = bps.toExponential(3) + ' bit/s';
    if (Tv) Tv.textContent = TEl.value + ' K';
    if (Pv) Pv.textContent = Number(PEl.value).toFixed(3) + ' W';
  }
  function hookLandauer(){
    if (!q('#T')) return;
    ['#T','#P'].forEach(id => q(id).addEventListener('input', landauerCalc));
    landauerCalc();
  }

  function hookChecklist(){
    const box = q('#gateChecklist');
    if (!box) return;
    const key = location.pathname.includes('/en/') ? 'hgp_gate_en' : 'hgp_gate_sk';
    const saved = JSON.parse(localStorage.getItem(key) || '{}');
    qa('input[type=checkbox]', box).forEach(cb => {
      if (saved[cb.id]) cb.checked = true;
      cb.addEventListener('change', () => {
        saved[cb.id] = cb.checked;
        localStorage.setItem(key, JSON.stringify(saved));
      });
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    hookLandauer();
    hookChecklist();
  });
})();
