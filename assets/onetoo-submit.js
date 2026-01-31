/*
  HGPEdu – Direct ONETOO submit (EXPERIMENTAL)

  - No long-lived secret token in client
  - Signed payload (WebCrypto ECDSA P-256) with a stable key stored in localStorage
  - Optional client-side PoW (Hashcash-like) to reduce spam
  - Submit via fetch() as text/plain to minimize CORS preflight
  - Fire-and-forget: CI ledger remains authoritative
*/
(function(){
  const CFG = {
    // Public POST endpoint (must accept unauthenticated submissions, otherwise this won't work)
    ONETOO_SUBMIT_URL: "https://search.onetoo.eu/contrib/v2/public/submit",

    KEY_ID: "hgpedu-browserkey-v1",

    POW_ENABLED: true,
    POW_DIFFICULTY_BITS: 18,

    // Hard caps
    MAX_BYTES: 12000,

    // Anti-spam throttle (client-side only; server must still rate-limit)
    COOLDOWN_MS: 30000,

    // Browser compatibility mode:
    // - "no-cors" = best chance request is actually sent (response is opaque)
    // - "cors"    = you may read response if server allows CORS
    SUBMIT_MODE: "no-cors",

    // If true, cooldown starts immediately when attempting SEND (even if network fails)
    COOLDOWN_ON_ATTEMPT: true
  };

  const te = new TextEncoder();

  const b64u = {
    enc(bytes){
      let bin = "";
      for (let i=0;i<bytes.length;i++) bin += String.fromCharCode(bytes[i]);
      return btoa(bin).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
    },
    dec(s){
      s = (s||"").replace(/-/g,"+").replace(/_/g,"/");
      while(s.length % 4) s += "=";
      const bin = atob(s);
      const out = new Uint8Array(bin.length);
      for(let i=0;i<bin.length;i++) out[i] = bin.charCodeAt(i);
      return out;
    }
  };

  function stableJson(obj){
    const seen = new WeakSet();
    const norm = (v)=>{
      if(v && typeof v === "object"){
        if(seen.has(v)) throw new Error("circular");
        seen.add(v);
        if(Array.isArray(v)) return v.map(norm);
        const out = {};
        Object.keys(v).sort().forEach(k=>{
          if(v[k] === undefined) return;
          out[k] = norm(v[k]);
        });
        return out;
      }
      return v;
    };
    return JSON.stringify(norm(obj));
  }

  function utf8Len(str){ return te.encode(str).length; }

  async function sha256Bytes(bytes){
    return new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
  }

  function leadingZeroBits(bytes){
    let z = 0;
    for(const b of bytes){
      if(b === 0){ z += 8; continue; }
      for(let i=7;i>=0;i--){
        if((b >> i) & 1) return z;
        z++;
      }
    }
    return z;
  }

  async function powFind(messageBytes, difficultyBits){
    const prefix = te.encode("::");
    let nonce = 0;
    const start = Date.now();
    while(true){
      nonce++;
      const nbytes = te.encode(String(nonce));
      const buf = new Uint8Array(messageBytes.length + prefix.length + nbytes.length);
      buf.set(messageBytes, 0);
      buf.set(prefix, messageBytes.length);
      buf.set(nbytes, messageBytes.length + prefix.length);
      const h = await sha256Bytes(buf);
      if(leadingZeroBits(h) >= difficultyBits){
        return { nonce: String(nonce), ms: Date.now() - start, h: b64u.enc(h), timeout: false };
      }
      if(nonce % 500 === 0) await new Promise(r=>setTimeout(r,0));
      if(Date.now() - start > 20000){
        return { nonce: String(nonce), ms: Date.now() - start, h: b64u.enc(h), timeout: true };
      }
    }
  }

  const LS_PRIV = "hgpedu.submit.ecdsaP256.pkcs8.b64u";
  const LS_PUB  = "hgpedu.submit.ecdsaP256.spki.b64u";
  const LS_LAST = "hgpedu.submit.last_ms";

  async function ensureKeypair(){
    const privB64 = localStorage.getItem(LS_PRIV);
    const pubB64  = localStorage.getItem(LS_PUB);
    if(privB64 && pubB64){
      const priv = await crypto.subtle.importKey(
        "pkcs8", b64u.dec(privB64),
        { name:"ECDSA", namedCurve:"P-256" },
        false, ["sign"]
      );
      const pub = await crypto.subtle.importKey(
        "spki", b64u.dec(pubB64),
        { name:"ECDSA", namedCurve:"P-256" },
        true, ["verify"]
      );
      return { priv, pub, pubB64 };
    }
    const kp = await crypto.subtle.generateKey(
      { name:"ECDSA", namedCurve:"P-256" },
      true, ["sign","verify"]
    );
    const pkcs8 = new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey));
    const spki  = new Uint8Array(await crypto.subtle.exportKey("spki", kp.publicKey));
    localStorage.setItem(LS_PRIV, b64u.enc(pkcs8));
    localStorage.setItem(LS_PUB,  b64u.enc(spki));
    return { priv: kp.privateKey, pub: kp.publicKey, pubB64: b64u.enc(spki) };
  }

  async function sign(privKey, messageStr){
    const msg = te.encode(messageStr);
    const sig = new Uint8Array(await crypto.subtle.sign(
      { name:"ECDSA", hash:"SHA-256" },
      privKey, msg
    ));
    return b64u.enc(sig); // DER-encoded signature from WebCrypto (OK if server verifies the same way)
  }

  function cooldownOk(){
    const last = Number(localStorage.getItem(LS_LAST) || "0");
    return (Date.now() - last) >= CFG.COOLDOWN_MS;
  }
  function markCooldown(){ localStorage.setItem(LS_LAST, String(Date.now())); }

  function validateBasic(payload){
    // Minimal sanity checks (avoid empty spam)
    const title = String(payload?.title || "").trim();
    const url = String(payload?.url || "").trim();
    if(!title) throw new Error("Missing title.");
    if(!url) throw new Error("Missing URL.");
    try { new URL(url); } catch(e){ throw new Error("URL is not valid."); }
    if(!CFG.ONETOO_SUBMIT_URL) throw new Error("ONETOO_SUBMIT_URL not configured.");
    try { new URL(CFG.ONETOO_SUBMIT_URL); } catch(e){ throw new Error("ONETOO_SUBMIT_URL is not a valid URL."); }
  }

  async function submitPayload(payload, ui){
    validateBasic(payload);

    const json0 = stableJson(payload);
    if(utf8Len(json0) > CFG.MAX_BYTES) throw new Error("Payload too large.");
    if(!cooldownOk()) throw new Error("Cooldown active. Try later.");

    ui?.setState?.("PREPARE", "Preparing key + signature…");
    const kp = await ensureKeypair();

    const submit = {
      kid: CFG.KEY_ID,
      alg: "ECDSA_P256_SHA256",
      ts: Date.now(),
      origin: location.origin,
      pub_spki_b64u: kp.pubB64,
      pow: null,
      sig: null
    };

    const signedObj = JSON.parse(json0);
    signedObj.submit = submit;

    const toSign1 = stableJson(signedObj);

    if(CFG.POW_ENABLED){
      ui?.setState?.("POW", `Computing PoW (${CFG.POW_DIFFICULTY_BITS} bits)…`);
      const pow = await powFind(te.encode(toSign1), CFG.POW_DIFFICULTY_BITS);
      signedObj.submit.pow = {
        v: 1,
        diff_bits: CFG.POW_DIFFICULTY_BITS,
        nonce: pow.nonce,
        hash_b64u: pow.h,
        ms: pow.ms,
        timeout: !!pow.timeout
      };
    }

    const toSign2 = stableJson(signedObj);

    ui?.setState?.("SIGN", "Signing…");
    signedObj.submit.sig = await sign(kp.priv, toSign2);

    const finalStr = stableJson(signedObj);
    if(utf8Len(finalStr) > CFG.MAX_BYTES) throw new Error("Payload too large.");

    ui?.setState?.("SEND", "Submitting to ONETOO…");
    if(CFG.COOLDOWN_ON_ATTEMPT) markCooldown();

    try{
      const res = await fetch(CFG.ONETOO_SUBMIT_URL, {
        method: "POST",
        headers: { "Content-Type": "text/plain;charset=UTF-8" },
        body: finalStr,
        mode: CFG.SUBMIT_MODE,      // "no-cors" recommended for experiments
        credentials: "omit",
        cache: "no-store",
        redirect: "follow"
      });

      // no-cors always yields opaque, which is fine
      if(res.type === "opaque"){
        ui?.setState?.("SENT", "Sent (opaque). CORS blocks reading response. Check CI ledger.");
        return { ok: true, opaque: true };
      }

      if(res.ok){
        if(!CFG.COOLDOWN_ON_ATTEMPT) markCooldown();
        ui?.setState?.("OK", "Submitted. Check CI ledger for status.");
        return { ok: true, opaque: false, status: res.status };
      }

      ui?.setState?.("ERR", "HTTP " + res.status + ". Check CI ledger.");
      return { ok: false, opaque: false, status: res.status };

    }catch(e){
      ui?.setState?.("SENT", "Submit attempted, but fetch error (CORS/network). Check CI ledger.");
      return { ok: false, opaque: true, error: String(e||"") };
    }
  }

  // Optional helper: allow users/devs to reset keypair in console if needed
  function resetKeypair(){
    localStorage.removeItem(LS_PRIV);
    localStorage.removeItem(LS_PUB);
  }

  window.HGPEduDirectSubmit = { config: CFG, submitPayload, resetKeypair };
})();