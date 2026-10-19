# Runs data/jobs.jsonl through oauthlib itself; the output is expected.out.
import json
import os
import sys
import time
from types import SimpleNamespace
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

time.time = lambda: 1700000000.0

from oauthlib import common  # noqa: E402
from oauthlib.oauth1 import Client  # noqa: E402
from oauthlib.oauth1.rfc5849 import signature, utils  # noqa: E402
from oauthlib.oauth2 import BackendApplicationClient, WebApplicationClient  # noqa: E402
from oauthlib.oauth2.rfc6749.errors import raise_from_error  # noqa: E402

VERIFY = {
    "HMAC-SHA1": signature.verify_hmac_sha1,
    "HMAC-SHA256": signature.verify_hmac_sha256,
    "HMAC-SHA512": signature.verify_hmac_sha512,
    "PLAINTEXT": signature.verify_plaintext,
}


def failure(e):
    return "raised %s: %s" % (type(e).__name__, e)


def body_arg(b):
    return [tuple(p) for p in b] if isinstance(b, list) else b


last = {}
client2 = [None]


def sign1(j):
    c = Client(**j["client"])
    try:
        uri, headers, body = c.sign(j["uri"], j["method"], body_arg(j["body"]), dict(j["headers"]),
                                    realm=j.get("realm"))
    except Exception as e:  # noqa: BLE001
        print("   " + failure(e))
        last.clear()
        return
    print("   uri     " + repr(uri))
    print("   headers " + repr(headers))
    print("   body    " + repr(body))
    last.update(uri=uri, headers=headers, body=body, method=j["method"])


def verify1(j):
    if not last:
        print("   nothing to verify")
        return
    uri = j.get("uri", last["uri"])
    q = urlparse(uri).query
    params = signature.collect_parameters(uri_query=q, body=last["body"], headers=last["headers"])
    every = dict(signature.collect_parameters(uri_query=q, body=last["body"], headers=last["headers"],
                                              exclude_oauth_signature=False))
    if "add" in j:
        params.append(tuple(j["add"]))
    r = SimpleNamespace(uri=uri, http_method=j.get("method", last["method"]), params=params,
                        signature=every["oauth_signature"])
    ok = VERIFY[every["oauth_signature_method"]](r, j["cs"], j["rs"])
    print("   %s %s" % (every["oauth_signature_method"], "valid" if ok else "INVALID"))


def show_client(c):
    print("   client access_token=%r refresh_token=%r token_type=%r expires_in=%r expires_at=%r code=%r state=%r"
          % (c.access_token, c.refresh_token, c.token_type, c.expires_in, c._expires_at, c.code, c.state))


def show_triple(t):
    uri, headers, body = t
    print("   uri     " + repr(uri))
    print("   headers " + repr(headers))
    print("   body    " + repr(body))


def oauth2(op, args):
    c = client2[0]
    if op == "client2":
        return
    if op == "auth_request":
        show_triple(c.prepare_authorization_request(**args))
    elif op == "request_uri":
        print("   " + repr(c.prepare_request_uri(**args)))
    elif op == "parse_callback":
        try:
            print("   " + repr(c.parse_request_uri_response(**args)))
        finally:
            show_client(c)
    elif op == "token_request":
        try:
            show_triple(c.prepare_token_request(**args))
        finally:
            show_client(c)
    elif op == "request_body":
        print("   " + repr(c.prepare_request_body(**args)))
    elif op == "parse_token":
        try:
            print("   " + repr(c.parse_request_body_response(**args)))
        finally:
            show_client(c)
    elif op == "add_token":
        show_triple(c.add_token(**args))
    elif op == "refresh":
        show_triple(c.prepare_refresh_token_request(**args))
    elif op == "revoke":
        show_triple(c.prepare_token_revocation_request(**args))


def error_job(j):
    params = {"error_description": j["description"], "error_uri": j["uri"], "state": j["state"]}
    try:
        raise_from_error(j["error"], params)
    except Exception as e:  # noqa: BLE001
        print("   %s status %d: %s" % (type(e).__name__, e.status_code, e))
        print("   twotuples  " + repr(e.twotuples))
        print("   urlencoded " + e.urlencoded)
        print("   json       " + e.json)
        print("   headers    " + repr(e.headers))
        print("   in_uri     " + e.in_uri("https://client.example.com/cb?lang=en"))


def challenge(j):
    try:
        out = client2[0].create_code_challenge(j["verifier"], j["method"])
    except Exception as e:  # noqa: BLE001
        print("   " + failure(e))
        return
    c = client2[0]
    print("   returned %r; code_challenge=%r code_challenge_method=%r"
          % (out, c.code_challenge, c.code_challenge_method))


def audit(j):
    secrets = {}
    tokens = {}
    with open("data/" + j["consumers"]) as f:
        for line in f:
            if line.startswith("#"):
                continue
            key, secret, tok, ts = line.rstrip("\n").split("\t")
            secrets[key] = secret
            if tok != "-":
                tokens[(key, tok)] = ts
    seen = set()
    ok = {}
    bad = {}
    reasons = {}
    with open("data/" + j["log"]) as f:
        lines = [line.rstrip("\n") for line in f]
    for n, line in enumerate(lines, 1):
        method, uri, auth, body = line.split("\t")
        body = None if body == "-" else body
        path = urlparse(uri).path
        verdict, who = check(method, uri, auth, body, secrets, tokens, seen, j["now"], j["window"])
        print("   %2d %-6s %-22s %-11s %s" % (n, method, path, who, verdict))
        if verdict == "ok":
            ok[who] = ok.get(who, 0) + 1
        else:
            bad[who] = bad.get(who, 0) + 1
            reason = verdict.split(":")[0]
            reasons[reason] = reasons.get(reason, 0) + 1
    for who in sorted(set(ok) | set(bad)):
        print("   %-11s %2d accepted %2d rejected" % (who, ok.get(who, 0), bad.get(who, 0)))
    for reason in sorted(reasons):
        print("   %-26s %2d" % (reason, reasons[reason]))


def check(method, uri, auth, body, secrets, tokens, seen, now, window):
    try:
        given = dict(utils.parse_authorization_header(auth))
    except ValueError as e:
        return "malformed header: %s" % e, "-"
    key = given.get("oauth_consumer_key", "-")
    for name in ["oauth_consumer_key", "oauth_signature_method", "oauth_signature", "oauth_nonce",
                 "oauth_timestamp"]:
        if name not in given:
            return "missing parameter: %s" % name, key
    if key not in secrets:
        return "unknown consumer: %s" % key, key
    tok = given.get("oauth_token")
    token_secret = None
    if tok is not None:
        if (key, tok) not in tokens:
            return "unknown token: %s" % tok, key
        token_secret = tokens[(key, tok)]
    age = now - int(given["oauth_timestamp"])
    if abs(age) > window:
        return "stale timestamp: %d s" % age, key
    nonce = (key, given["oauth_nonce"], given["oauth_timestamp"])
    if nonce in seen:
        return "replayed nonce: %s" % given["oauth_nonce"], key
    headers = {"Authorization": auth}
    q = urlparse(uri).query
    params = signature.collect_parameters(uri_query=q, body=body, headers=headers)
    sig = common.unquote(given["oauth_signature"])
    method_name = given["oauth_signature_method"]
    if method_name not in VERIFY:
        return "unsupported method: %s" % method_name, key
    r = SimpleNamespace(uri=uri, http_method=method, params=params, signature=sig)
    if not VERIFY[method_name](r, secrets[key], token_secret):
        return "bad signature: %s" % method_name, key
    seen.add(nonce)
    return "ok", key


def main():
    with open("data/jobs.jsonl", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    for line in lines:
        if line.startswith("== "):
            print(line)
            continue
        j = json.loads(line)
        op = j["op"]
        print("-- " + line)
        try:
            run(op, j)
        except Exception as e:  # noqa: BLE001
            print("   " + failure(e))


def run(op, j):
    if op == "escape":
        e = utils.escape(j["s"])
        print("   %r -> %r -> %r" % (j["s"], e, utils.unescape(e)))
    elif op == "unescape":
        print("   %r -> %r" % (j["s"], utils.unescape(j["s"])))
    elif op == "urldecode":
        print("   " + repr(common.urldecode(j["q"])))
    elif op == "authheader":
        print("   " + repr(utils.parse_authorization_header(j["h"])))
    elif op == "bsuri":
        print("   " + repr(signature.base_string_uri(j["uri"], j.get("host"))))
    elif op == "collect":
        print("   " + repr(signature.collect_parameters(
            uri_query=j["query"], body=body_arg(j["body"]), headers=j["headers"],
            exclude_oauth_signature=j.get("exclude_sig", True), with_realm=j.get("with_realm", False))))
    elif op == "normalize":
        print("   " + repr(signature.normalize_parameters([tuple(p) for p in j["params"]])))
    elif op == "basestring":
        print("   " + repr(signature.signature_base_string(j["method"], j["uri"], j["params"])))
    elif op == "sign1":
        sign1(j)
    elif op == "verify1":
        verify1(j)
    elif op == "error":
        error_job(j)
    elif op == "client2":
        cls = WebApplicationClient if j["kind"] == "web" else BackendApplicationClient
        client2[0] = cls(**j["args"])
        show_client(client2[0])
    elif op == "challenge":
        challenge(j)
    elif op == "audit":
        audit(j)
    else:
        oauth2(op, j["args"])


main()
