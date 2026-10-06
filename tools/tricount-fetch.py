#!/usr/bin/env python3
"""Read-only Tricount share-link fetch (Alex's folio spike, Oct 5 2026).
Registers an anonymous app session against the bunq Tricount API (same
endpoints the mobile app uses), then reads the shared registry by its
public link key. Never writes anything. urllib only."""
import json, uuid, os, urllib.request, urllib.parse, http.client
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

BASE = "https://api.tricount.bunq.com"
KEY = "tzeCkFokMjbNGkCtYN"
SESS = os.path.expanduser("~/.cache/tricount-session.json")
UA = "Tricount/8.0.0 (Android)"

def http(method, url, headers=None, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"User-Agent": UA,
                                          "X-Bunq-Client-Request-Id": str(uuid.uuid4()),
                                          "Content-Type": "application/json",
                                          **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            try:
                body = r.read().decode()
            except http.client.IncompleteRead as e:
                # egress proxy sometimes cuts chunked streams mid-flight; keep what arrived
                body = e.partial.decode(errors="replace")
            return r.status, json.loads(body)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]

def register():
    app_id = str(uuid.uuid4())
    pub = rsa.generate_private_key(public_exponent=65537, key_size=2048).public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.PKCS1).decode()
    code, resp = http("POST", BASE + "/v1/session-registry-installation",
                      headers={"app-id": app_id},
                      body={"app_installation_uuid": app_id, "client_public_key": pub,
                            "device_description": "Android"})
    if code != 200:
        raise RuntimeError("register failed: %s %s" % (code, resp))
    items = resp["Response"]
    sess = {"app_id": app_id,
            "token": next(i["Token"]["token"] for i in items if "Token" in i),
            "user_id": next(i["UserPerson"]["id"] for i in items if "UserPerson" in i)}
    os.makedirs(os.path.dirname(SESS), exist_ok=True)
    json.dump(sess, open(SESS, "w"))
    return sess

def load_session():
    if os.path.exists(SESS):
        return json.load(open(SESS))
    return register()

def api(method, path, params=None, body=None):
    sess = load_session()
    url = BASE + path.format(user_id=sess["user_id"])
    if params:
        url += "?" + urllib.parse.urlencode(params)
    code, resp = http(method, url, headers={"app-id": sess["app_id"],
                                           "X-Bunq-Client-Authentication": sess["token"]}, body=body)
    if code in (401, 403):
        sess = register()
        url = BASE + path.format(user_id=sess["user_id"])
        if params:
            url += "?" + urllib.parse.urlencode(params)
        code, resp = http(method, url, headers={"app-id": sess["app_id"],
                                               "X-Bunq-Client-Authentication": sess["token"]}, body=body)
    if code != 200:
        raise RuntimeError("api failed: %s %s" % (code, resp))
    return resp

if __name__ == "__main__":
    raw = api("GET", "/v1/user/{user_id}/registry", params={"public_identifier_token": KEY})
    json.dump(raw, open("/tmp/tricount-raw.json", "w"), indent=1)
    print("saved /tmp/tricount-raw.json,", len(json.dumps(raw)), "bytes")
