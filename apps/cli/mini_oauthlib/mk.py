# Writes data/: jobs.jsonl, the list of things to do, and the files the
# request audit reads (consumers.tsv and requests.log, a day of signed API
# calls as a server's access log would keep them).
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from oauthlib.oauth1 import Client  # noqa: E402

random.seed(131)
os.makedirs("data", exist_ok=True)

jobs = []


def sec(name):
    jobs.append("== " + name)


def job(op, **kw):
    d = {"op": op}
    d.update(kw)
    jobs.append(json.dumps(d, ensure_ascii=False))


# ------------------------------------------------------------ OAuth 1
sec("oauth1 escape")
for s in ["Ladies + Gentlemen", "An encoded string!", "Dogs, Cats & Mice", "☃", "-._~",
          "a/b?c=d#e", "", "100%", "日本語 text", "oauth_token=x&y"]:
    job("escape", s=s)
for s in ["%7E%2f%2F", "a+b", "%E2%98%83", "%zz", "%", "caf%C3%A9"]:
    job("unescape", s=s)

sec("oauth1 urldecode")
for q in ["a=1&b=2", "c2&a3=2+q", "a=%20&b=", "x=1;y=2", "a=1&&b=2", "name=caf%C3%A9",
          "q=hello world", "a=<b", "a=%zz", "a=%4", "a=%4G", "a=%", "", "=v&k=",
          "a=1&a=2", "path=/x/y?z", "a=é", "tilde=~&star=*"]:
    job("urldecode", q=q)

sec("oauth1 authorization header")
for h in [
    'OAuth realm="Example", oauth_consumer_key="9djdj82h48djs9d2", oauth_token="kkk9d7dh3k39sjv7"',
    'oauth oauth_nonce="7d8f3e4a", oauth_version="1.0"',
    'OAuth oauth_callback="http%3A%2F%2Fprinter.example.com%2Fready"',
    'OAuth a="1,2", b="x\\"y"',
    'OAuth a=plain, b="quoted"',
    'OAuth a="1", a="2"',
    'OAuth a=',
    'OAuth novalue',
    'Bearer abc',
    'OAuth ',
    'OAuth a="1",,b="2"',
    'OAUTH x="y"',
]:
    job("authheader", h=h)

sec("oauth1 base string URI")
for uri, host in [
    ("http://EXAMPLE.COM:80/r%20v/X?id=123", None),
    ("https://www.example.net:8080/?q=1", None),
    ("https://api.example.com:443/1/statuses", None),
    ("http://api.example.com:443/1/statuses", None),
    ("HTTPS://Example.com", None),
    ("https://example.com/a b;p=1?x#frag", None),
    ("http://[2001:DB8:0:0:0:0:0:1]:8000/v1", None),
    ("http://[::FFFF:0:0:1]/", None),
    ("http://[fe80:0:0:0:200:f8ff:fe21:67cf]:80/", None),
    ("http://192.168.000.001/x", None),
    ("http://10.0.0.1:0/x", None),
    ("http://example.com:99999/x", None),
    ("http://example.com:8x/x", None),
    ("/relative/path", None),
    ("http:///nohost", None),
    ("https://internal:8443/token", "api.Example.com"),
    ("https://internal:8443/token", "api.example.com:9000"),
    ("http://internal/token", "proxy.example.com:80"),
    ("https://internal/token", "[::1]:8443"),
    ("mailto:someone@example.com", None),
]:
    if host is None:
        job("bsuri", uri=uri)
    else:
        job("bsuri", uri=uri, host=host)

sec("oauth1 collect and normalize")
rfc_header = ('OAuth realm="Example", oauth_consumer_key="9djdj82h48djs9d2", '
              'oauth_token="kkk9d7dh3k39sjv7", oauth_signature_method="HMAC-SHA1", '
              'oauth_timestamp="137131201", oauth_nonce="7d8f3e4a", '
              'oauth_signature="djosJKDKJSD8743243%2Fjdk33klY%3D"')
job("collect", query="b5=%3D%253D&a3=a&c%40=&a2=r%20b", body="c2&a3=2+q",
    headers={"Authorization": rfc_header})
job("collect", query="b5=%3D%253D&a3=a&c%40=&a2=r%20b", body="c2&a3=2+q",
    headers={"authorization": rfc_header}, with_realm=True, exclude_sig=False)
job("collect", query="", body=[["a", "1"], ["oauth_x", "%41"]], headers={})
job("collect", query="oauth_extra=%2541", body=None, headers={"Content-Type": "text/plain"})
job("collect", query="", body='{"json": true}', headers={})
job("collect", query="a=1", body="", headers={"Authorization": "Basic Zm9vOmJhcg=="})
job("normalize", params=[["b5", "=%3D"], ["a3", "a"], ["c@", ""], ["a2", "r b"],
                         ["oauth_consumer_key", "9djdj82h48djs9d2"], ["oauth_token", "kkk9d7dh3k39sjv7"],
                         ["oauth_signature_method", "HMAC-SHA1"], ["oauth_timestamp", "137131201"],
                         ["oauth_nonce", "7d8f3e4a"], ["c2", ""], ["a3", "2 q"]])
job("normalize", params=[["z", "1"], ["a", "2"], ["a", "10"], ["A", "1"], ["é", "x"], ["a b", "~"]])
job("normalize", params=[])
job("basestring", method="post", uri="http://example.com/request",
    params="a2=r%20b&a3=2%20q&a3=a&b5=%3D%253D&c%40=&c2=&oauth_consumer_key=9djdj82h48djs9d2")

sec("oauth1 signing")
twitter = {"client_key": "xvz1evFS4wEEPTGEFPHBog",
           "client_secret": "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw",
           "resource_owner_key": "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb",
           "resource_owner_secret": "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE",
           "nonce": "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", "timestamp": "1318622958"}
tweet = "https://api.twitter.com/1.1/statuses/update.json?include_entities=true"
form = {"Content-Type": "application/x-www-form-urlencoded"}
job("sign1", client=twitter, uri=tweet, method="POST",
    body="status=Hello%20Ladies%20%2b%20Gentlemen%2c%20a%20signed%20OAuth%20request%21", headers=form)
job("verify1", cs=twitter["client_secret"], rs=twitter["resource_owner_secret"])
job("verify1", cs=twitter["client_secret"], rs="wrong-secret")
job("verify1", cs=twitter["client_secret"], rs=twitter["resource_owner_secret"], method="PUT")
job("verify1", cs=twitter["client_secret"], rs=twitter["resource_owner_secret"],
    add=["status", "Goodbye"])
job("sign1", client=dict(twitter, realm="Twitter API"), uri=tweet, method="POST",
    body=[["status", "Hello Ladies + Gentlemen, a signed OAuth request!"]], headers=form)

photos = {"client_key": "dpf43f3p2l4k3l03", "client_secret": "kd94hf93k423kf44",
          "resource_owner_key": "nnch734d00sl2jdk", "resource_owner_secret": "pfkkdhi9sl3r4s00",
          "nonce": "kllo9940pd9333jh", "timestamp": "1191242096"}
pic = "http://photos.example.net/photos?file=vacation.jpg&size=original"
for method in ["HMAC-SHA1", "HMAC-SHA256", "HMAC-SHA512", "PLAINTEXT"]:
    for stype in ["AUTH_HEADER", "QUERY"]:
        job("sign1", client=dict(photos, signature_method=method, signature_type=stype), uri=pic,
            method="GET", body=None, headers={})
        job("verify1", cs=photos["client_secret"], rs=photos["resource_owner_secret"])
job("verify1", cs=photos["client_secret"], rs="")
job("sign1", client=dict(photos, signature_type="BODY"), uri="http://photos.example.net/photos",
    method="POST", body="file=vacation.jpg&size=original&tags=", headers=form)
job("verify1", cs=photos["client_secret"], rs=photos["resource_owner_secret"])
job("verify1", cs=photos["client_secret"], rs=photos["resource_owner_secret"],
    uri="http://photos.example.net/photos2")
job("sign1", client=dict(photos, signature_type="BODY"), uri="http://photos.example.net/photos",
    method="POST", body="file=a.jpg", headers={"content-type": "application/x-www-form-urlencoded"})

request_token = {"client_key": "dpf43f3p2l4k3l03", "client_secret": "kd94hf93k423kf44",
                 "callback_uri": "http://printer.example.com/ready", "signature_method": "PLAINTEXT",
                 "nonce": "wIjqoS", "timestamp": "137131200", "realm": "Photos"}
job("sign1", client=request_token, uri="https://photos.example.net/initiate", method="POST", body=None,
    headers={})
job("sign1", client={"client_key": "dpf43f3p2l4k3l03", "client_secret": "kd94hf93k423kf44",
                     "resource_owner_key": "hh5s93j4hdidpola", "resource_owner_secret": "hdhd0244k9j7ao03",
                     "verifier": "hfdp7dh39dks9884", "nonce": "walatlh", "timestamp": "137131201"},
    uri="https://photos.example.net/token", method="POST", body=None, headers={})
job("verify1", cs="kd94hf93k423kf44", rs="hdhd0244k9j7ao03")

api = {"client_key": "ck-demo", "client_secret": "cs&demo secret", "resource_owner_key": "tok/42",
       "resource_owner_secret": "ts~42", "nonce": "n0nce", "timestamp": "1700000000"}
json_h = {"Content-Type": "application/json", "Accept": "application/json"}
job("sign1", client=api, uri="https://api.example.com/v2/items", method="POST",
    body='{"name": "lamp", "qty": 2}', headers=json_h)
job("verify1", cs=api["client_secret"], rs=api["resource_owner_secret"])
job("sign1", client=dict(api, signature_method="HMAC-SHA256"), uri="https://api.example.com/v2/items/7",
    method="PUT", body="raw text body", headers={"Content-Type": "text/plain"})
job("sign1", client=api, uri="https://api.example.com/v2/search?q=caf%C3%A9&page=2&sort=", method="get",
    body=None, headers={"Host": "public.example.com"})
job("verify1", cs=api["client_secret"], rs=api["resource_owner_secret"])
job("sign1", client=dict(api, signature_type="QUERY"), uri="https://internal:8443/v2/search?q=x",
    method="GET", body=None, headers={"host": "public.example.com"})
job("sign1", client=api, uri="https://internal:8443/v2/search?q=x", method="GET", body=None,
    headers={"host": "public.example.com"})
job("sign1", client=api, uri="https://api.example.com/v2/upload", method="POST", body="a=1",
    headers={"Content-Type": "multipart/form-data; boundary=xyz"})
job("sign1", client=api, uri="https://api.example.com/v2/upload", method="POST", body="--xyz--",
    headers={"Content-Type": "multipart/form-data; boundary=xyz"})
job("sign1", client=api, uri="https://api.example.com/v2/form", method="POST", body='{"a": 1}',
    headers=form)
job("sign1", client=api, uri="https://api.example.com/v2/form", method="POST", body="a=1&b=2",
    headers={})
job("sign1", client=api, uri="https://api.example.com/v2/form", method="POST", body="",
    headers={"Content-Type": "text/plain"})
job("sign1", client=api, uri="https://api.example.com/v2/form", method="POST", body="token",
    headers={"Content-Type": "application/json"})
job("sign1", client=dict(api, signature_type="BODY"), uri="https://api.example.com/v2/form",
    method="POST", body='{"a": 1}', headers=json_h)
job("sign1", client=api, uri="https://api.example.com/v2/form", method="GET", body="a=1",
    headers=form)
job("sign1", client=api, uri="https://api.example.com/v2/form", method="HEAD", body=[["a", "1"]],
    headers=form)
job("sign1", client=dict(api, signature_method="HMAC-MD5"), uri="https://api.example.com/v2/x",
    method="GET", body=None, headers={})
job("sign1", client=dict(api, signature_type="COOKIE"), uri="https://api.example.com/v2/x",
    method="GET", body=None, headers={})
job("sign1", client=api, uri="https://api.example.com/v2/x?q=a b", method="GET", body=None, headers={})
job("sign1", client=api, uri="https://api.example.com/v2/x?q=%zz", method="GET", body=None, headers={})
job("sign1", client={"client_key": "only-key", "nonce": "1", "timestamp": "2"},
    uri="http://[2001:db8::1]:8080/a;b?c=d", method="DELETE", body=None, headers={})
job("verify1", cs="", rs="")
job("verify1", cs=None, rs=None)
job("sign1", client=dict(api, signature_type="QUERY"), uri="https://api.example.com/v2/x?a=1#top",
    method="GET", body=None, headers={})
job("sign1", client=dict(api, signature_type="QUERY"), uri="https://api.example.com/v2/x?b=2&a=1",
    method="POST", body="z=9", headers=form)
job("verify1", cs=api["client_secret"], rs=api["resource_owner_secret"])
job("sign1", client=dict(api, client_secret="", resource_owner_secret=None, signature_method="PLAINTEXT"),
    uri="https://api.example.com/", method="GET", body=None, headers={}, realm="override")

# ------------------------------------------------------------ OAuth 2
sec("oauth2 errors")
for err, desc, uri, state in [
    ("access_denied", "The user denied the request.", None, "xyz"),
    ("invalid_request", None, None, None),
    ("invalid_client", "Client authentication failed.", "https://example.com/docs/errors#client", None),
    ("invalid_grant", "Code expired", None, None),
    ("invalid_token", None, None, "s t"),
    ("insufficient_scope", "", None, None),
    ("slow_down", "Polling too fast", None, None),
    ("temporarily_unavailable", "Back in 5 minutes & counting", None, "ab/cd"),
    ("unsupported_grant_type", "grant_type=password is disabled", None, None),
    ("server_error", "Ünïcode \"quoted\"", None, None),
]:
    job("error", error=err, description=desc, uri=uri, state=state)

sec("oauth2 web application flow")
job("client2", kind="web", args={"client_id": "s6BhdRkqt3", "scope": ["openid", "profile"],
                                 "redirect_url": "https://client.example.com/cb"})
job("auth_request", args={"authorization_url": "https://server.example.com/authorize", "state": "xyz"})
job("auth_request", args={"authorization_url": "https://server.example.com/authorize?audience=api",
                          "state": "st-2", "scope": "email", "prompt": "consent", "login_hint": "",
                          "access_type": "offline"})
job("auth_request", args={"authorization_url": "http://server.example.com/authorize", "state": "x"})
job("challenge", verifier="dBjftJeZ4CVP-1JzbJyiE3BXlqBFOrk_7wRxJhN6oBQ", method="S256")
job("challenge", verifier="dBjftJeZ4CVP-1JzbJyiE3BXlqBFOrk_7wRxJhN6oBQ", method=None)
job("challenge", verifier="plain-verifier-value", method="plain")
job("challenge", verifier=None, method="S256")
job("request_uri", args={"uri": "https://server.example.com/authorize", "state": "pkce-1",
                         "code_challenge": "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
                         "code_challenge_method": "S256", "redirect_uri": "https://client.example.com/cb"})
job("request_uri", args={"uri": "https://server.example.com/authorize#frag", "scope": [],
                         "state": None, "nonce": "n-0S6_WzA2Mj", "max_age": 0, "display": "page"})
job("parse_callback", args={"uri": "https://client.example.com/cb?code=SplxlOBeZQQYbYS6WxSbIA&state=xyz",
                            "state": "xyz"})
job("parse_callback", args={"uri": "https://client.example.com/cb?code=abc&state=other", "state": "xyz"})
job("parse_callback", args={"uri": "https://client.example.com/cb?state=xyz", "state": "xyz"})
job("parse_callback", args={"uri": "https://client.example.com/cb?error=access_denied&"
                            "error_description=User+said+no&state=xyz", "state": "xyz"})
job("parse_callback", args={"uri": "https://client.example.com/cb?error=invalid_scope", "state": None})
job("parse_callback", args={"uri": "http://client.example.com/cb?code=x", "state": None})
job("parse_callback", args={"uri": "https://client.example.com/cb?code=c1&code=c2&extra=&state=xyz"})
job("token_request", args={"token_url": "https://server.example.com/token",
                           "authorization_response": "https://client.example.com/cb?code=SplxlOBeZQQYbYS6WxSbIA&state=xyz",
                           "state": "xyz", "client_secret": "7Fjfp0ZBr1KtDRbnfVdmIw"})
job("token_request", args={"token_url": "https://server.example.com/token", "code_verifier": "ver-1",
                           "include_client_id": False, "audience": "api", "empty": ""})
job("token_request", args={"token_url": "https://server.example.com/token", "body": "a=1&b=",
                           "redirect_url": "https://client.example.com/other", "code": "explicit"})
job("token_request", args={"token_url": "https://server.example.com/token",
                           "authorization_response": "https://client.example.com/cb?code=zzz&state=bad"})
job("request_body", args={"client_id": "someone-else"})
job("request_body", args={"client_id": "s6BhdRkqt3", "scope": ["a", "b"], "count": 3})
job("parse_token", args={"body": json.dumps({"access_token": "2YotnFZFEjr1zCsicMWpAA", "token_type": "Bearer",
                                             "expires_in": 3600, "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
                                             "scope": "openid profile"})})
job("add_token", args={"uri": "https://api.example.com/me"})
job("add_token", args={"uri": "https://api.example.com/me?fields=name", "token_placement": "query"})
job("add_token", args={"uri": "https://api.example.com/me", "http_method": "POST", "body": "a=1",
                       "headers": {"Accept": "*/*"}, "token_placement": "body"})
job("add_token", args={"uri": "https://api.example.com/me", "token_placement": "cookie"})
job("add_token", args={"uri": "http://api.example.com/me"})
job("parse_token", args={"body": json.dumps({"access_token": "x", "token_type": "Bearer", "scope": "profile openid"})})
job("parse_token", args={"body": json.dumps({"access_token": "x", "token_type": "Bearer", "scope": "email"}),
                         "scope": "profile"})
job("parse_token", args={"body": json.dumps({"access_token": "y", "token_type": "bearer"}), "scope": "admin"})
job("parse_token", args={"body": "access_token=z1&token_type=bearer&expires_in=120&scope=write+read&blank=",
                         "scope": "read write"})
job("parse_token", args={"body": "access_token=z1&expires_in=soon"})
job("parse_token", args={"body": json.dumps({"error": "invalid_grant", "error_description": "Code was already redeemed."})})
job("parse_token", args={"body": json.dumps({"error": "invalid_request"})})
job("parse_token", args={"body": json.dumps({"error": "authorization_pending", "interval": 5})})
job("parse_token", args={"body": json.dumps({"token_type": "Bearer"})})
job("parse_token", args={"body": ""})
job("parse_token", args={"body": json.dumps({"access_token": "nested", "token_type": "Bearer", "expires_in": None,
                                             "id_token": "eyJ.x.y", "aud": ["a", "b"], "ok": True,
                                             "meta": {"region": "eu", "n": 2}, "ratio": None})})
job("refresh", args={"token_url": "https://server.example.com/token"})
job("refresh", args={"token_url": "https://server.example.com/token", "refresh_token": "override",
                     "scope": ["openid"], "client_id": "s6BhdRkqt3", "client_secret": "sec"})
job("refresh", args={"token_url": "http://server.example.com/token"})
job("revoke", args={"revocation_url": "https://server.example.com/revoke", "token": "2YotnFZFEjr1zCsicMWpAA"})
job("revoke", args={"revocation_url": "https://server.example.com/revoke", "token": "tGzv3JOkF0XG5Qx2TlKWIA",
                    "token_type_hint": "refresh_token", "body": "client_id=s6BhdRkqt3"})
job("revoke", args={"revocation_url": "https://server.example.com/revoke?x=1", "token": "t",
                    "token_type_hint": None, "callback": "package.myCallback", "extra": "1"})
job("revoke", args={"revocation_url": "http://server.example.com/revoke", "token": "t"})

sec("oauth2 backend application flow")
job("client2", kind="backend", args={"client_id": "svc-reporting"})
job("request_body", args={})
job("request_body", args={"scope": "metrics.read", "include_client_id": True, "client_secret": "s3cr3t-value"})
job("token_request", args={"token_url": "https://auth.example.com/oauth/token", "scope": ["a", "b"],
                           "audience": "https://api.example.com"})
job("parse_token", args={"body": json.dumps({"access_token": "svc-tok", "token_type": "Bearer", "expires_in": "900"})})
job("add_token", args={"uri": "https://api.example.com/reports", "headers": {"X-Trace": "1"}})
job("add_token", args={"uri": "https://api.example.com/reports", "token_placement": "body"})

sec("oauth2 clients built from saved tokens")
job("client2", kind="web", args={"client_id": "c", "token": {"access_token": "old", "expires_at": 1600000000,
                                                            "token_type": "Bearer"}})
job("add_token", args={"uri": "https://api.example.com/x"})
job("client2", kind="web", args={"client_id": "c", "token": {"access_token": "fresh", "expires_at": "1800000000"}})
job("add_token", args={"uri": "https://api.example.com/x"})
job("client2", kind="web", args={"client_id": "c", "token": {"access_token": "odd", "expires_at": "tomorrow"}})
job("add_token", args={"uri": "https://api.example.com/x"})
job("client2", kind="web", args={"client_id": "c", "token_type": "JWT", "access_token": "j"})
job("add_token", args={"uri": "https://api.example.com/x"})
job("client2", kind="web", args={"client_id": "c"})
job("add_token", args={"uri": "https://api.example.com/x"})
job("client2", kind="web", args={"client_id": "c", "default_token_placement": "query",
                                 "token": {"access_token": "q-tok", "refresh_token": "r", "expires_in": 60}})
job("add_token", args={"uri": "https://api.example.com/x?y=1"})
job("refresh", args={"token_url": "https://server.example.com/token", "body": "keep=1"})
job("client2", kind="web", args={"client_id": "mac-client", "token": {
    "access_token": "h480djs93hd8", "token_type": "MAC", "mac_key": "489dks293j39",
    "mac_algorithm": "hmac-sha-1"}})
job("add_token", args={"uri": "https://example.com:8443/resource/1?b=1&a=2", "nonce": "264095:dj83hs9s",
                       "ext": "a,b,c"})
job("add_token", args={"uri": "https://example.com/resource/1", "http_method": "post", "body": "hello=world",
                       "nonce": "264095:7d8f3e4a"})
job("add_token", args={"uri": "https://example.com/resource/1", "token_placement": "query", "nonce": "1:2"})
job("client2", kind="web", args={"client_id": "mac-client", "token": {
    "access_token": "h480djs93hd8", "token_type": "mac", "mac_key": "489dks293j39",
    "mac_algorithm": "hmac-sha-256"}})
job("add_token", args={"uri": "https://example.com/resource/1", "nonce": "264095:dj83hs9s",
                       "headers": {"Accept": "text/html"}})
job("client2", kind="web", args={"client_id": "mac-client", "token": {
    "access_token": "h", "token_type": "MAC", "mac_key": "k", "mac_algorithm": "hmac-md5"}})
job("add_token", args={"uri": "https://example.com/resource/1", "nonce": "1:2"})

# ------------------------------------------------------------ audit
CONSUMERS = [("ck-mobile", "m0b1le-s3cret"), ("ck-partner", "p@rtner~key"), ("ck-cron", "cr0n")]
TOKENS = {"ck-mobile": [("u-1001", "u1001-ts"), ("u-1002", "u1002-ts")],
          "ck-partner": [("p-77", "p77/ts")], "ck-cron": [(None, None)]}
with open("data/consumers.tsv", "w") as f:
    f.write("# consumer key\tconsumer secret\ttoken\ttoken secret\n")
    for key, secret in CONSUMERS:
        for tok, ts in TOKENS[key]:
            f.write("%s\t%s\t%s\t%s\n" % (key, secret, tok or "-", ts or "-"))

NOW = 1700000000
paths = ["/v1/orders", "/v1/orders/1187", "/v1/users/me", "/v1/search?q=red+shoes&page=2",
         "/v1/inventory?sku=A-12&sku=A-13", "/v1/reports/daily"]
lines = []
for i in range(36):
    key, secret = CONSUMERS[i % 3]
    tok, ts = TOKENS[key][i % len(TOKENS[key])]
    method = ["GET", "POST", "GET", "DELETE", "GET", "PUT"][i % 6]
    path = paths[i % len(paths)]
    meth = ["HMAC-SHA1", "HMAC-SHA256", "HMAC-SHA1", "PLAINTEXT", "HMAC-SHA512", "HMAC-SHA1"][i % 6]
    stamp = NOW - 300 + i * 17
    nonce = "n%04d" % random.randrange(10000)
    body = None
    headers = {}
    if method in ("POST", "PUT"):
        body = "qty=%d&note=%s" % (i, ["gift", "rush+order", "", "a%2Fb"][i % 4])
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
    c = Client(key, client_secret=secret, resource_owner_key=tok, resource_owner_secret=ts,
               signature_method=meth, nonce=nonce, timestamp=str(stamp))
    uri, h, b = c.sign("https://api.shop.example" + path, method, body, headers)
    auth = h["Authorization"]
    # Some requests are spoiled the ways real ones go wrong.
    if i % 11 == 4:
        auth = auth.replace('oauth_signature="', 'oauth_signature="X')
    if i % 13 == 7:
        b = (b or "") + "&qty=999"
    if i == 20:
        auth = auth.replace("ck-cron", "ck-unknown")
    if i == 25:
        auth = auth.replace(str(stamp), str(stamp - 4000))
    if i == 30:
        lines.append(lines[2])
    if i == 33:
        auth = auth.replace("oauth_nonce", "oauth_nonse")
    lines.append("\t".join([method, uri, auth, b if b is not None else "-"]))
lines.append("GET\thttps://api.shop.example/v1/health\tBasic Zm9vOmJhcg==\t-")
lines.append("GET\thttps://api.shop.example/v1/x\tOAuth broken\t-")
with open("data/requests.log", "w") as f:
    f.write("\n".join(lines) + "\n")

sec("request audit")
job("audit", log="requests.log", consumers="consumers.tsv", now=NOW, window=600)

with open("data/jobs.jsonl", "w", encoding="utf-8") as f:
    f.write("\n".join(jobs) + "\n")
print(len([j for j in jobs if not j.startswith("== ")]), "jobs")
