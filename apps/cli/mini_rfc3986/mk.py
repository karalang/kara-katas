# Writes data/: the jobs (data/jobs.jsonl), built from rfc3986's own
# test suite (its fixtures, parameter lists and literals), and a webhook
# registry for the report at the end (data/webhooks.tsv).
#
# A job is a list of steps. The first step makes a value (a URI
# reference, an IRI, a parse result, a builder or a validator) and each
# later step calls a method on it; a step that returns a new value of
# one of those kinds makes it the current one. oracle.py prints every
# step's result.
import itertools, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

SNOWMAN = "\u2603"

# conftest.py
valid_hosts = [
    "[21DA:00D3:0000:2F3B:02AA:00FF:FE28:9C5A]", "[::1]", "[::1%25lo]",
    "[FF02:0:0:0:0:0:0:2%25en01]", "[FF02:30:0:0:0:0:0:5%25en1]",
    "[FF02:30:0:0:0:0:0:5%25%26]", "[FF02:30:0:0:0:0:0:5%2525]",
    "[21DA:D3:0:2F3B:2AA:FF:FE28:9C5A]", "[FE80::2AA:FF:FE9A:4CA2]", "[FF02::2]",
    "[FFFF::]", "[FF02:3::5]", "[FF02:0:0:0:0:0:0:2]", "[FF02:30:0:0:0:0:0:5]",
    "127.0.0.1", "www.example.com", "localhost", "http-bin.org",
    "%2Fvar%2Frun%2Fsocket", "6g9m8V6",
]
invalid_hosts = [
    "[FF02::3::5]", "[FADF:01]", "[FADF:01%en0]", "[FADF::01%]",
    "localhost:80:80:80", "256.256.256.256", SNOWMAN,
]
equivalent_hostnames = ["example.com", "eXample.com", "example.COM", "EXAMPLE.com", "ExAMPLE.com"]
equivalent_schemes = ["https", "HTTPS", "HttPs", "hTTpS", "HtTpS"]

FIXTURES = [
    "http://%s", "ftp://%s:21", "ssh://user:pass@%s:22", "ssh://user%%20!=:pass@%s:22",
    "http://%s/path/to/resource", "http://%s/path/to/resource?key=value",
    "https://user:pass@%s:443/path/to/resource?key=value#fragment", "//%s",
    "https://%s/%% ", "https://%s?a=%%", "https://%s#perc%%ent",
]

# Literals from the test modules, and a few more of the same kinds.
LITERALS = [
    "#foobar", "#fragment", "%", "/", "/path/to/file", "../foo/bar", "./foo/bar", "/../foo/bar",
    "/./foo/bar", "//a/./b/../b/%63/%7Bfoo%7D", "a/./b/../b/%63/%7Bfoo%7D", "//github.com",
    "//google.com#fragment", "//google.com", "//google.com?query=value",
    "//user:password@github.com", "//user@github.com", "/a/b/c/./../../g", "mid/content=5/../6",
    "/foo%20bar/biz%2Abaz", "/%21%22%23%ah%12%ff", "/%CE%B2/%CF%8C", "?foo=bar", "?query",
    "HTTP://EXAMPLE.COM", "http+unix://%2Ftmp%2FTEST.sock/get", "http://B%C3%BC:%E1%BA%9E@gOoGle.com",
    "http://Bü:ẞ@gOoGle.com", "http://[::1%eth0]", "http://example.com?utf8=%E2%98%83",
    "http://foo.bar:1234/baz", "http://foo:b@r@[::1]:80/get", "http://xn--10cl1a0b660p.com",
    "http://xn--bcher-kva.de", "http://xn--zca.com:443", "https://", "https://httpbin.org/get?",
    "https://httpbin.org:", "https://httpbin.org:443/get", "mailto:user@example.com",
    "https://sigmavirus24:not-my-re%40l-password@github.com/sigmavirus24/rfc3986",
    "https://user:pass@xdavidhu.me\\test.corp.google.com:8080/path/to/something?param=value#hash",
    "smtp://", "telnet://", "git://github.com", "https://github.com?a=0&e=f",
    "ssh://ssh@git.openstack.org:22/sigmavirus24?foo=bar#fragment", "ssh://git.openstack.org:22/#fragment",
    "http://example.com/" + SNOWMAN, "http://" + SNOWMAN + ".com/path", "http://userinfo@" + SNOWMAN + ".com",
    "https://i\u2764.ws", "http://user:@example.com", "http://:pass@example.com", "http://example.com:/a",
    "http://example.com:65536/", "http://example.com:00080/", "https://300.1.1.1/", "https://1.2.3/",
    "https://[v1.fe80::a+en1]/", "https://[::ffff:192.0.2.128]/", "https://[::1]:8443/hooks",
    "file:///etc/hosts", "file://localhost/c:/WINDOWS/clock.avi", "urn:isbn:0451450523",
    "news:comp.infosystems.www.servers.unix", "tel:+1-816-555-1212", "ldap://[2001:db8::7]/c=GB?objectClass?one",
    "data:text/plain;charset=utf-8,hello%20world", "HTTPS://Example.COM:443/%7Euser/./a/../b?q=%2f%2F#Frag",
    "http://example.com/a b?c d#e f", "http://example.com/%zz/%A", "foo:b@r", "a:b:c",
    "http://a/b/c/d;p?q", "", "//", "///", "http://@/", "http://[::1", "http://example.com]/",
]

# The IPv6 literals take four of the templates: the IPv6 alternation is
# the slowest pattern to backtrack through.
IPV6_FIXTURES = [FIXTURES[0], FIXTURES[2], FIXTURES[6], FIXTURES[7]]

URIS = []
for tpl in FIXTURES:
    for h in valid_hosts:
        if tpl in IPV6_FIXTURES or not h.startswith("["):
            URIS.append(tpl % h)
for h in invalid_hosts:
    URIS.append("https://%s" % h)
for s, h in itertools.product(equivalent_schemes, equivalent_hostnames):
    URIS.append("%s://%s" % (s, h))
for s in equivalent_schemes:
    URIS.append("%s:" % s)
URIS += LITERALS
seen = set()
URIS = [u for u in URIS if not (u in seen or seen.add(u))]

jobs = []


def job(*steps):
    jobs.append(list(steps))


for u in URIS:
    job(["uri", u], ["unsplit"], ["authority_info"], ["is_absolute"], ["is_valid"],
        ["is_valid", {"require_scheme": True, "require_authority": True, "require_path": True}],
        ["normalize"], ["unsplit"])
for u in URIS:
    job(["urlparse", u], ["attr", "netloc"], ["unsplit"])
for u in URIS[::3]:
    job(["parse", u, True, True], ["geturl"])
    job(["parse", u, False, False], ["unsplit"])
    job(["validator"], ["check_validity_of", "scheme", "userinfo", "host", "port", "path", "query", "fragment"],
        ["validate", u])

# bytes in
for u in ["http://example.com?utf8=" + SNOWMAN, "http://" + SNOWMAN + ".com", "https://httpbin.org:443/get",
          "https://user@httpbin.org", "http://userinfo@" + SNOWMAN + ".com"]:
    job(["uri_b", u.encode().hex()], ["is_valid"], ["eq", "http://example.com?utf8=%E2%98%83"])
    job(["urlparse_b", u.encode().hex()], ["attr", "host"], ["attr", "userinfo"])

# test_unicode_support / test_parseresult
for p in ["443:80", "443:80:443", "abcdef", "port", "43port", "99999", "0080"]:
    job(["urlparse", f"https://httpbin.org:{p}/get"], ["attr", "port"])
    job(["parse_bytes", f"https://httpbin.org:{p}/get", False, True], ["attr", "port"])
job(["urlparse", "https://i\u2764.ws"], ["encode", "idna"], ["geturl"])
job(["urlparse", "http://" + SNOWMAN + ".com"], ["unsplit_idna"])
job(["urlparse", "http://" + SNOWMAN + ".com/path"], ["unsplit_idna"], ["copy_with", {"host": "example.org"}])
job(["parse_bytes", "http://" + SNOWMAN + ".com/path", False, True], ["unsplit_idna"], ["unsplit"])
job(["parse_bytes", "http://" + SNOWMAN + ".com/path", False, False], ["unsplit"])
job(["parse", "http://" + SNOWMAN + ".com", True, True])
for parts in [{"scheme": "https", "host": "httpbin.org"}, {"scheme": "https", "userinfo": "user", "host": "httpbin.org"},
              {"scheme": "https", "host": "httpbin.org", "port": 443, "path": "/get"},
              {"scheme": "HTTPS", "host": "HTTPBIN.ORG"}, {"scheme": "http", "host": SNOWMAN, "path": "/path"},
              {"scheme": "https", "host": "[::1%eth0]", "port": 8443, "query": "a=%2f"},
              {"host": "example.com", "path": "a/./b/../c"}]:
    job(["parts", parts], ["unsplit"])
    job(["parts_bytes", dict(parts, lazy=False)], ["unsplit"])
    job(["parts_bytes", parts], ["unsplit"])
for u in valid_hosts[:6] + ["github.com"]:
    full = "https://user:pass@%s:443/path/to/resource?key=value#fragment" % u
    job(["parse", full, True, True], ["copy_with", {"path": "/parse/result/tests/are/fun"}],
        ["copy_with", {"port": 8443}], ["copy_with", {"userinfo": "admin"}], ["unsplit"], ["encode", None],
        ["copy_with", {"path": "/x/" + SNOWMAN}], ["unsplit"])
    job(["parse_bytes", full, True, True], ["copy_with", {"query": "a=b"}], ["unsplit"], ["attr", "authority"])
    job(["uri", full], ["copy_with", {"scheme": None, "fragment": None}], ["unsplit"], ["copy_with", {"path": "#foobar"}])

# test_uri: equality, resolution, encodings
for a, b in [("http://example.com", "HTTP://EXAMPLE.COM"), ("http://example.com/a/../b", "http://example.com/b"),
             ("http://example.com/%7e", "http://example.com/%7E"), ("https://a.b", "https://a.b/"),
             ("http://Bü:ẞ@gOoGle.com", "http://B%C3%BC:%E1%BA%9E@gOoGle.com"), ("//a/b", "//A/b")]:
    job(["uri", a], ["eq", b])
job(["uri", "https://example.com"], ["eq_tuple", ["https", "example.com", None, None, None]])
job(["iri", "http://Bü:ẞ@βόλος.com/β/ό?λ#ος"],
    ["eq_tuple", ["http", "Bü:ẞ@βόλος.com", "/%CE%B2/%CF%8C", "%CE%BB", "%CE%BF%CF%82"]])

BASE = "http://a/b/c/d;p?q"
RFC_NORMAL = ["g:h", "g", "./g", "g/", "/g", "//g", "?y", "g?y", "#s", "g#s", "g?y#s", ";x", "g;x", "g;x?y#s",
              "", ".", "./", "..", "../", "../g", "../..", "../../", "../../g"]
RFC_ABNORMAL = ["../../../g", "../../../../g", "/./g", "/../g", "g.", ".g", "g..", "..g", "./../g", "./g/.",
                "g/./h", "g/../h", "g;x=1/./y", "g;x=1/../y", "g?y/./x", "g?y/../x", "g#s/./x", "g#s/../x", "http:g"]
for r in RFC_NORMAL + RFC_ABNORMAL:
    job(["uri", r], ["resolve", BASE, False], ["unsplit"])
job(["uri", "http:g"], ["resolve", BASE, True], ["unsplit"])
for base in ["https://example.com", "https://example.com/path", "//example.com/a", "/relative", "foo:bar/baz",
             "https://example.com?q=1"]:
    for r in ["../", "/boom", "?x=1", "#frag", "mid/6", "", "https://other.org/x/../y"]:
        job(["uri", r], ["resolve", base, False], ["unsplit"])
job(["uri", "https://example.com/path"], ["resolve", "relative/path", False])

# test_iri
IRIS = ["http://Bücher.de", "http://faß.de", "http://βόλος.com/β/ό?λ#ος", "http://ශ්\u200dරී.com",
        "http://نامه\u200cای.com", "http://Bü:ẞ@gOoGle.com", "http://ẞ.com:443", "http://ẞ.foo.com",
        "http://Bẞ.com", "http+unix://%2Ftmp%2FTEST.sock/get", "http://♥.net", "http://\u0378.net",
        "http://㛼.com", "https://user:pass@München.example:8080/straße?ä=ö#ü", "http://ex\u200dample.com",
        "http://xn--nxasmm1c.com", "http://Ελλάδα.gr/", "http://日本語.jp/パス", "http://a.b.\u0661\u0662.com",
        "http://\u05d0\u05d1.\u05d2\u05d3/", "ftp://[::1]/" + SNOWMAN, "//straße.de"]
for i in IRIS:
    job(["iri", i], ["authority_info"], ["unsplit"], ["eq", i], ["encode_iri"], ["unsplit"])

# test_builder
job(["builder"])
job(["builder_from", "http://foo.bar:1234/baz"])
job(["builder_from", "https://bar.foo:4321/boom"])
for s in ["https", "hTTps", "Https", "HtTpS", "HTTPS"]:
    job(["builder"], ["add_scheme", s])
for u, p in [("user", "pass"), ("user", None), ("user@domain.com", "password"), ("user", "pass:word"),
             (None, None), ("Bü", "ẞ ü/?#")]:
    job(["builder"], ["add_credentials", u, p])
for h in ["google.com", "GOOGLE.COM", "gOOgLe.COM", "goOgLE.com", "[::ff%etH0]", "[::ff%25etH0]", "[::FF%etH0]",
          "[::1%25]", "[::1%2525]", "[::1%25%25]", "[::Af%Ff]", "[::Af%25Ff]", "[::af%25%Ff]", "[::1%eth0]",
          "[::1%25eth0]", "[FADF:01]"]:
    job(["builder"], ["add_host", h])
for p in [-100, "-100", -1, "-1", 65536, "65536", 1000000, "1000000", "", "abc", "0b10", 0, "0", 1, "1", 22,
          "22", 80, "80", 443, "443", 65535, "65535", " 8080 ", "+80", "8_0", "\uff18\uff10"]:
    job(["builder"], ["add_port", p])
for p in ["sigmavirus24/rfc3986", "/sigmavirus24/rfc3986", "a/./b/../c", "/%7euser/%2f"]:
    job(["builder"], ["add_path", p])
for items in [[["a", "b c"]], [["a", "b+c"]], [["a", "b"], ["c", "d"]], [["a", "b"], ["username", "@d"]],
              [["percent", "%"]], [["q", "caf\u00e9 & cr\u00e8me"], ["n", "1/2"]]]:
    job(["builder"], ["add_query_from", items])
job(["builder"], ["add_query", "username=@foo"])
job(["builder"], ["add_query", "a=%2f%2F"])
job(["builder"], ["add_fragment", "section-2.5.1"])
job(["builder"], ["add_fragment", "%7esec"])
for u, e in [("https://api.github.com", "/users"), ("https://api.github.com", "/users/"),
             ("https://api.github.com", "users"), ("https://api.github.com", "users/"), ("", "users/"),
             ("", "users"), ("?foo=bar", "users"), ("https://api.github.com/users/", "sigmavirus24"),
             ("https://api.github.com/users", "sigmavirus24"), ("https://api.github.com/users", "/sigmavirus24")]:
    job(["builder_from", u], ["extend_path", e], ["geturl"])
for u in ["https://github.com", "https://github.com?a=0", "https://github.com?a=0&e=f", "https://github.com?a=&b"]:
    job(["builder_from", u], ["extend_query_with", [["a", "b c"], ["d", "e&f"]]], ["geturl"])
job(["builder"], ["add_scheme", "https"], ["add_credentials", "sigmavirus24", "not-my-re@l-password"],
    ["add_host", "github.com"], ["add_path", "sigmavirus24/rfc3986"], ["finalize"], ["unsplit"])
job(["builder"], ["add_scheme", "HTTPS"], ["add_host", "API.Example.com"], ["add_port", "8443"],
    ["add_path", "v2"], ["extend_path", "orders/../items"], ["add_query_from", [["page", "2"], ["sort", "-date"]]],
    ["add_fragment", "top"], ["geturl"])

# test_validators
job(["validator"], ["allow_schemes", "http", "https"])
job(["validator"], ["require_presence_of", "frob"])
job(["validator"], ["check_validity_of", "frob"])
job(["validator"], ["allow_ports", "80", "100", "65536", "-1"], ["validate", "http://a:65536/"])
job(["validator"], ["allow_ports", "abc"])
for u in ["https://user:password@github.com", "https://user:password@github.com/path",
          "https://user:password@github.com/path?query", "https://user:password@github.com/path?query#frag",
          "//user:password@github.com", "https://user@github.com", "https://user@github.com/path",
          "https://user@github.com/path?query", "https://user@github.com/path?query#frag", "//user@github.com",
          "//github.com", "https://github.com", "https://user:@github.com"]:
    job(["validator"], ["forbid_use_of_password"], ["validate", u], ["allow_use_of_password"], ["validate", u])
for u in ["https://", "/path/to/resource"]:
    job(["validator"], ["validate", u], ["require_presence_of", "host"], ["validate", u])
for u in ["https://", "//google.com", "//google.com?query=value", "//google.com#fragment", "https://google.com",
          "https://google.com#fragment", "https://google.com?query=value"]:
    job(["validator"], ["require_presence_of", "path"], ["validate", u])
for u in ["//google.com", "//google.com?query=value", "//google.com#fragment"]:
    job(["validator"], ["require_presence_of", "scheme", "path"], ["validate", u])
for u in ["smtp://", "telnet://"]:
    job(["validator"], ["allow_schemes", "https", "http"], ["validate", u])
for u in ["git://github.com", "http://github.com", "ssh://gitlab.com", "https://gitlab.com"]:
    job(["validator"], ["allow_schemes", "https", "ssh"], ["allow_hosts", "github.com", "git.openstack.org"],
        ["validate", u])
GOOD = ["https://github.com/sigmavirus24", "ssh://github.com/sigmavirus24", "ssh://ssh@github.com:22/sigmavirus24",
        "https://github.com:443/sigmavirus24", "https://gitlab.com/sigmavirus24", "ssh://ssh@gitlab.com:22/sigmavirus24",
        "https://bitbucket.org:443/sigmavirus24", "ssh://ssh@git.openstack.org:22/sigmavirus24?foo=bar#fragment",
        "ssh://git.openstack.org:22/#fragment", "ssh://git.openstack.org:22/", "https://GitHub.com/x",
        "https://github.com:8443/x", "https://evil.com/sigmavirus24", "ftp://github.com/x"]
for u in GOOD:
    job(["validator"], ["allow_schemes", "https", "ssh"],
        ["allow_hosts", "github.com", "bitbucket.org", "gitlab.com", "git.openstack.org"],
        ["allow_ports", "22", "443"], ["require_presence_of", "scheme", "host", "path"],
        ["check_validity_of", "scheme", "userinfo", "host", "port", "path", "query", "fragment"], ["validate", u])
for h in invalid_hosts:
    job(["validator"], ["check_validity_of", "host"], ["validate", "https://%s" % h])
    job(["validator"], ["check_validity_of", "host", "path"], ["validate_with_path", "https://%s" % h, "#foobar"])
job(["validator"], ["check_validity_of", "host"], ["validate", "http://[::1%eth0]"])
job(["uri", "http://[::1%eth0]"], ["normalize"], ["attr", "host"])
job(["validator"], ["check_validity_of", "HOST", "Port"], ["validate", "http://a:99999"])

# test_normalizers and the module functions
for s in ["HTTP", "hTtP", "https", ""]:
    job(["fn", "normalize_scheme", s])
for a in [["user%2aName", "EXAMPLE.COM", "8080"], [None, "[::1%eth0]", None], [None, None, None],
          ["u", "Example.com", ""], ["%3athis_should_be_lowercase%DF%ab%4c", "h", "1"]]:
    job(["fn", "normalize_authority", a])
for h in ["[::1%25]", "[::1%%25]", "[::1%25%25]", "[::1%2525]", "[::1%25eth0]", "[::1%eth0]", "[::Af%Ff]",
          "[::Af%%Ff]", "[::Af%25Ff]", "[::af%25%Ff]", "[::ff%etH0]", "[::FF%etH0]", "WWW.Example.COM", "[FFFF::]"]:
    job(["fn", "normalize_host", h])
for p in ["/%3athis_should_be_lowercase%DF%ab%4c", "/a/b/c/./../../g", "mid/content=5/../6", "/foo/bar/.",
          "/foo/bar/..", "/../foo", "./a", "..", "/", "", "/a//b/./c/"]:
    job(["fn", "normalize_path", p])
    job(["fn", "remove_dot_segments", p])
for q in ["a=%2f&b=%ab", "", "x"]:
    job(["fn", "normalize_query", q])
    job(["fn", "normalize_fragment", q])
for s in ["/%", "/%20%25", "/%20/%", "/%21%22%23%ah%12%ff", "/%25a", "/%25ag", "/%2520/%25", "/%a", "/%af",
          "/%ag", "perc%25ent", "fiz%DF", "a=%25", "/%25", "/~", "\u03bb", "/" + SNOWMAN + "%41", "a b",
          "[]@!$&'()*+,;=", "%2B+"]:
    job(["fn", "encode_component", s])
for s in ["user", "us er", "a@b.c", "p:w/d?"]:
    job(["fn", "normalize_username", s])
    job(["fn", "normalize_password", s])
for s in ["127.0.0.1", "256.1.1.1", "1.2.3.4.5", "01.002.3.4"]:
    job(["fn", "valid_ipv4_host_address", s])
for s in ["user:pass@host:80", "a@b@c", "[::1]:80", "[::1]", "host", "host:", ":80", "u@", "u@[v1.x]:9:9", ""]:
    job(["fn", "split_authority", s])
for h in valid_hosts + invalid_hosts + [None]:
    job(["fn", "host_is_valid", h])
for u in ["http://example.com", "http://" + SNOWMAN + ".com", "//a/b", "HTTP://a/./b/../c"]:
    job(["fn", "is_valid_uri", u])
    job(["fn", "is_valid_uri", u, {"require_scheme": True, "require_path": True}])
    job(["fn", "normalize_uri", u])

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "jobs.jsonl"), "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")

# A webhook registry: tenant, base URL of the tenant's API, and the
# callback each tenant registered (absolute or relative to its base).
HOOKS = [
    ("acme", "https://api.acme.example/v1/", "hooks/orders"),
    ("acme", "https://api.acme.example/v1/", "./hooks/orders"),
    ("acme", "https://api.acme.example/v1/", "HTTPS://API.ACME.EXAMPLE:443/v1/hooks/%6frders"),
    ("acme", "https://api.acme.example/v1/", "../v1/hooks/refunds?since=2026-10-01"),
    ("globex", "https://globex.example/", "https://hooks.globex.example:8443/in#ignored"),
    ("globex", "https://globex.example/", "http://hooks.globex.example/in"),
    ("globex", "https://globex.example/", "https://admin:hunter2@hooks.globex.example/in"),
    ("globex", "https://globex.example/", "https://hooks.globex.example:22/in"),
    ("initech", "https://initech.example/app/", "//cb.initech.example/tps-reports"),
    ("initech", "https://initech.example/app/", "https://[2001:DB8::1]:8443/cb"),
    ("initech", "https://initech.example/app/", "https://[::1%eth0]/cb"),
    ("initech", "https://initech.example/app/", "https://300.1.1.1/cb"),
    ("umbrella", "https://umbrella.example/", "https://hooks.umbrella.example/" + SNOWMAN + "?x=%zz"),
    ("umbrella", "https://umbrella.example/", "https://Bücher.example/notify"),
    ("umbrella", "https://umbrella.example/", "mailto:ops@umbrella.example"),
    ("umbrella", "https://umbrella.example/", "https://hooks.umbrella.example:99999/"),
    ("umbrella", "https://umbrella.example/", "https://hooks.umbrella.example/a/b/../../c/./d"),
    ("hooli", "https://hooli.example/x/y", "?only=query"),
    ("hooli", "https://hooli.example/x/y", "#frag-only"),
    ("hooli", "https://hooli.example/x/y", ""),
]
with open(os.path.join(DATA, "webhooks.tsv"), "w", encoding="utf-8") as f:
    f.write("# tenant\tbase\tcallback\n")
    for row in HOOKS:
        f.write("\t".join(row) + "\n")
print(len(jobs), "jobs,", sum(len(j) for j in jobs), "steps")
