#!/usr/bin/env python3
"""Bienvenue folio server (Oct 2026).

Serves the Tricount folio as JSON on the home LAN so the TV app (a browser,
blocked by Tricount's missing CORS headers) can read it with a plain GET.

Endpoints (all with Access-Control-Allow-Origin: *):
  GET /folio.json           -> cached folio; refreshes from Tricount if older than TTL
  GET /folio.json?refresh=1 -> force a fresh fetch from Tricount
  GET /health               -> {"ok": true, ...} server/cache status

The Tricount share key + static public key are read from the TV build's
local-config.js on every refresh, so swapping trips needs no restart.
Session token is cached next to this script. Nothing is ever written to Tricount.

Stdlib only. Run: pythonw.exe folio-server.py   (port 8080)
"""
import json
import os
import re
import threading
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL_CONFIG = r"C:\Users\maple\tizen-homebrew\bienvenue-src\local-config.js"
CACHE_FILE = os.path.join(HERE, "folio-cache.json")
SESS_FILE = os.path.join(HERE, "tricount-session.json")
LOG_FILE = os.path.join(HERE, "folio-server.log")
PORT = 8080
TTL = 15 * 60  # refresh from Tricount when cache is older than this (seconds)
BASE = "https://api.tricount.bunq.com"
UA = "Tricount/8.0.0 (Android)"

_lock = threading.Lock()


def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S") + " " + msg
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass
    try:
        print(line, flush=True)  # may fail under pythonw (no stdout) - file log is the truth
    except (AttributeError, OSError, ValueError):
        pass


def read_cfg():
    """Extract tricount {key, publicKey} from the TV build's local-config.js."""
    with open(LOCAL_CONFIG, encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"\.tricount\s*=\s*\{(.*?)\}", src, re.S)
    if not m:
        raise RuntimeError("tricount assignment not found in local-config.js")
    blk = m.group(1)
    key = re.search(r'key\s*:\s*"([^"]+)"', blk).group(1)
    pub = re.search(r'publicKey\s*:\s*"([^"]+)"', blk, re.S).group(1)
    pub = pub.replace("\\n", "\n")  # JS-escaped newlines -> real PEM newlines
    return key, pub


def tri_http(method, url, headers=None, body=None):
    import uuid
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"User-Agent": UA, "Content-Type": "application/json",
                 "X-Bunq-Client-Request-Id": str(uuid.uuid4()),  # required on every call
                 **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        log("HTTP %s %s -> %s %s" % (method, url, e.code, detail))
        raise


def tri_register(pubkey):
    import uuid
    app_id = str(uuid.uuid4())  # API validates this is a real UUID
    log("registering app_id=%s pubkey_len=%d pubkey_head=%s" % (
        app_id, len(pubkey), pubkey[:40].replace("\n", "\\n")))
    resp = tri_http(
        "POST", BASE + "/v1/session-registry-installation",
        headers={"app-id": app_id, "X-Bunq-Client-Request-Id": app_id},
        body={"app_installation_uuid": app_id, "client_public_key": pubkey,
              "device_description": "Bienvenue TV"})
    items = resp["Response"]
    sess = {"app_id": app_id,
            "token": next(i["Token"]["token"] for i in items if "Token" in i),
            "user_id": next(i["UserPerson"]["id"] for i in items if "UserPerson" in i)}
    with open(SESS_FILE, "w", encoding="utf-8") as f:
        json.dump(sess, f)
    return sess


def tri_get(sess, key):
    url = (BASE + "/v1/user/%s/registry?public_identifier_token=%s"
           % (sess["user_id"], urllib.parse.quote(key)))
    try:
        return tri_http("GET", url,
                        headers={"app-id": sess["app_id"],
                                 "X-Bunq-Client-Authentication": sess["token"]})
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise PermissionError("auth expired")
        raise


def tri_name(mship):
    inner = mship.get("RegistryMembershipNonUser") or mship
    alias = inner.get("alias") or {}
    return alias.get("display_name") or str(inner.get("id"))


def parse_folio(raw):
    """Port of the TV app's triParse: balances = paid - share."""
    reg = raw["Response"][0]["Registry"]

    def entry_obj(w):
        e = w["RegistryEntry"]
        return json.loads(e) if isinstance(e, str) else e

    paid, owed, expenses, total = {}, {}, [], 0.0
    for w in reg.get("all_registry_entry", []):
        e = entry_obj(w)
        if e.get("status") != "ACTIVE":
            continue
        amt = -float(e["amount"]["value"])
        payer = tri_name(e["membership_owned"])
        paid[payer] = paid.get(payer, 0) + amt
        total += amt
        for a in e.get("allocations", []):
            who = tri_name(a["membership"])
            owed[who] = owed.get(who, 0) + (-float(a["amount"]["value"]))
        expenses.append({"date": str(e.get("date", ""))[:10],
                         "desc": e.get("description") or "Expense",
                         "payer": payer, "amt": round(amt, 2)})
    expenses.sort(key=lambda x: x["date"], reverse=True)
    members = {}
    for m in set(list(paid) + list(owed)):
        p, o = paid.get(m, 0), owed.get(m, 0)
        members[m] = {"name": m, "paid": round(p, 2), "share": round(o, 2),
                      "balance": round(p - o, 2)}
    return {"title": reg.get("title"), "currency": reg.get("currency"),
            "total": round(total, 2), "members": members,
            "expenses": expenses[:14]}


def load_cache():
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def save_cache(payload):
    tmp = CACHE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    os.replace(tmp, CACHE_FILE)


def refresh(force=False):
    """Return (payload, served_stale). Fetches from Tricount when forced or TTL expired."""
    cached = load_cache()
    if not force and cached and time.time() - cached.get("updated_at", 0) < TTL:
        return cached, False
    with _lock:  # avoid stampedes; re-check inside
        cached = load_cache()
        if not force and cached and time.time() - cached.get("updated_at", 0) < TTL:
            return cached, False
        key, pubkey = read_cfg()
        try:
            sess = json.load(open(SESS_FILE, encoding="utf-8")) if os.path.exists(SESS_FILE) else None
        except ValueError:
            sess = None
        try:
            raw = tri_get(sess, key) if sess else None
            if raw is None:
                raise PermissionError("no session")
        except (PermissionError, urllib.error.HTTPError, urllib.error.URLError):
            log("session invalid, re-registering")
            sess = tri_register(pubkey)
            raw = tri_get(sess, key)
        payload = {"updated_at": int(time.time()), "stale": False,
                   "folio": parse_folio(raw)}
        save_cache(payload)
        log("refreshed folio: %s %s total=%s" % (
            payload["folio"].get("title"), payload["folio"].get("currency"),
            payload["folio"].get("total")))
        return payload, False


class Handler(BaseHTTPRequestHandler):
    server_version = "BienvenueFolio/1.0"

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parts = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parts.query)
        if parts.path == "/health":
            cached = load_cache()
            self._json(200, {"ok": True, "time": int(time.time()),
                             "cache_updated_at": cached.get("updated_at") if cached else None})
            return
        if parts.path == "/folio.json":
            try:
                payload, _ = refresh(force="refresh" in qs)
                self._json(200, payload)
            except Exception as e:  # Tricount down etc: serve stale if we have it
                log("refresh failed: %r" % e)
                cached = load_cache()
                if cached:
                    cached = dict(cached, stale=True)
                    self._json(200, cached)
                else:
                    self._json(502, {"error": "tricount unavailable", "detail": str(e)[:200]})
            return
        self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        log("%s %s" % (self.address_string(), fmt % args))


def main():
    log("starting on port %d (TTL %ds)" % (PORT, TTL))
    try:
        payload, _ = refresh()
        log("initial cache ready, updated_at=%s" % payload["updated_at"])
    except Exception as e:
        log("initial refresh failed (will retry on request): %r" % e)
    try:
        ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
    except Exception:
        import traceback
        log("FATAL: " + traceback.format_exc().replace("\n", " | "))
        raise


if __name__ == "__main__":
    main()
