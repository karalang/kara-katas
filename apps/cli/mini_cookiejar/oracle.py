# Runs data/ through Python 3.13's own http.cookiejar module and prints
# what expected.out holds. Run it from the app directory, after mk.py.
import os
import shutil
import time
import logging
import warnings
import urllib.request
import http.cookiejar as cj

NOW = [0]
time.time = lambda: NOW[0]
os.environ["TZ"] = "UTC"
time.tzset()

# What the module logs when debug is on: why each cookie was or was not
# set or returned.
LOG = []


class Collect(logging.Handler):
    def emit(self, record):
        LOG.append(record.getMessage())


cj.debug = True
logger = logging.getLogger("http.cookiejar")
logger.setLevel(logging.DEBUG)
logger.addHandler(Collect())
logger.propagate = False


def flush_log():
    for line in LOG:
        print("  debug| " + line)
    del LOG[:]


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    return [line.split("\t") for line in text.split("\n")[:-1]]


# A response is anything with info().get_all(); a real one would be an
# http.client.HTTPResponse.
class Headers:
    def __init__(self, pairs):
        self.pairs = pairs

    def get_all(self, name, default=None):
        found = [v for k, v in self.pairs if k.lower() == name.lower()]
        return found if found else default

    def __str__(self):
        return "%d header(s)" % len(self.pairs)


class Response:
    def __init__(self, pairs):
        self.headers = Headers(pairs)

    def info(self):
        return self.headers


def make_request(url, fields):
    kw = {}
    headers = {}
    for f in fields:
        if f.startswith("origin="):
            kw["origin_req_host"] = f[7:]
        elif f.startswith("unverifiable="):
            kw["unverifiable"] = f[13:] == "1"
        else:
            k, _, v = f.partition(": ")
            headers[k] = v
    return urllib.request.Request(url, headers=headers, **kw)


def header_pairs(fields):
    out = []
    for f in fields:
        if f.startswith("origin=") or f.startswith("unverifiable="):
            continue
        k, _, v = f.partition(": ")
        out.append((k, v))
    return out


def new_jar(fields):
    kind = fields[0]
    kw = {}
    for f in fields[1:]:
        k, _, v = f.partition("=")
        if k in ("blocked_domains", "allowed_domains", "secure_protocols"):
            kw[k] = tuple(v.split(","))
        elif k == "strict_ns_domain":
            kw[k] = int(v)
        else:
            kw[k] = v == "1"
    policy = cj.DefaultCookiePolicy(**kw)
    cls = {"cookie": cj.CookieJar, "lwp": cj.LWPCookieJar,
           "mozilla": cj.MozillaCookieJar}[kind]
    return cls(policy=policy)


def show_file(path):
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    for line in text.split("\n")[:-1]:
        print("  file|" + (" " + line if line else ""))
    if not text.endswith("\n"):
        print("  file| (no newline at end)")


def run_fn(name, args):
    if name == "http2time":
        return repr(cj.http2time(args[0]))
    if name == "iso2time":
        return repr(cj.iso2time(args[0]))
    if name == "time2isoz":
        return repr(cj.time2isoz(int(args[0])))
    if name == "time2netscape":
        return repr(cj.time2netscape(int(args[0])))
    if name == "split_header_words":
        return repr(cj.split_header_words(args))
    if name == "join_header_words":
        return repr(cj.join_header_words(cj.split_header_words(args)))
    if name == "parse_ns_headers":
        return repr(cj.parse_ns_headers(args))
    if name == "domain_match":
        return repr(cj.domain_match(args[0], args[1]))
    if name == "user_domain_match":
        return repr(cj.user_domain_match(args[0], args[1]))
    if name == "is_HDN":
        return repr(cj.is_HDN(args[0]))
    if name == "reach":
        return repr(cj.reach(args[0]))
    if name == "escape_path":
        return repr(cj.escape_path(args[0]))
    raise ValueError(name)


def file_arg(f):
    return None if f == "-" else f


def run_op(jar, f):
    op = f[0]
    if op == "fn":
        print("  " + run_fn(f[1], f[2:]))
    elif op == "set":
        req = make_request(f[1], f[2:])
        jar.extract_cookies(Response(header_pairs(f[2:])), req)
    elif op == "get":
        req = make_request(f[1], f[2:])
        jar.add_cookie_header(req)
        sent = req.unredirected_hdrs
        for k in sorted(sent):
            print("  %s: %s" % (k, sent[k]))
        if not sent:
            print("  (no cookie header)")
    elif op == "list":
        for c in jar:
            print("  %s" % c)
    elif op == "repr":
        for c in jar:
            print("  %r" % c)
    elif op == "len":
        print("  %d" % len(jar))
    elif op == "clear":
        jar.clear(*f[1:])
    elif op == "clear_session":
        jar.clear_session_cookies()
    elif op == "clear_expired":
        jar.clear_expired_cookies()
    elif op == "save":
        jar.save(file_arg(f[1]), f[2] == "1", f[3] == "1")
        show_file(f[1])
    elif op == "load":
        jar.load(file_arg(f[1]), f[2] == "1", f[3] == "1")
    elif op == "revert":
        jar.revert(file_arg(f[1]), f[2] == "1", f[3] == "1")


def run_jobs():
    jar = None
    for f in read_tsv("data/jobs.tsv"):
        if f[0] == "job":
            print("== " + f[1])
            continue
        print("> " + " | ".join(f))
        if f[0] == "now":
            NOW[0] = int(f[1])
            continue
        if f[0] == "jar":
            jar = new_jar(f[1:])
            continue
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                run_op(jar, f)
            except Exception as e:
                flush_log()
                for w in caught:
                    print("  warning| " + str(w.message).split("\n")[0])
                print("  ! %s: %s" % (type(e).__name__, e))
                continue
        flush_log()


# ------------------------------------------------------------ the programs

def login_program():
    print("== program: a login session that survives a restart")
    NOW[0] = 1700000000
    jar = cj.MozillaCookieJar()
    url = None
    for f in read_tsv("data/session.tsv"):
        if f[0] == "GET":
            url = f[1]
            req = urllib.request.Request(url)
            jar.add_cookie_header(req)
            print("GET %s" % url)
            print("  Cookie: %s" % req.unredirected_hdrs.get("Cookie", "(none)"))
            LOG.clear()
        elif f[0] == "RESP":
            pairs = header_pairs(f[1:])
            jar.extract_cookies(Response(pairs), urllib.request.Request(url))
            LOG.clear()
            print("  %d cookie header(s) back, jar holds %d" % (len(pairs), len(jar)))
            NOW[0] += 60
        elif f[0] == "SAVE":
            jar.save(f[1], ignore_discard=True)
            print("saved %s with session cookies:" % f[1])
            show_file(f[1])
            jar.save(f[1])
            print("saved %s without them:" % f[1])
            show_file(f[1])
        elif f[0] == "RESTART":
            NOW[0] += 3600 * 2
            jar = cj.MozillaCookieJar(f"work/session.txt")
            jar.load()
            print("restarted two hours later; loaded %d cookie(s): %s"
                  % (len(jar), ", ".join(c.name for c in jar)))


def audit_program():
    print("== program: a third-party cookie audit")
    NOW[0] = 1700000000
    policy = cj.DefaultCookiePolicy(blocked_domains=[".doubleclick.net"],
                                    strict_ns_unverifiable=True)
    jar = cj.CookieJar(policy)
    for f in read_tsv("data/audit.tsv"):
        page, url = f[0], f[1]
        req = urllib.request.Request(url, origin_req_host=page,
                                     unverifiable=not url.startswith("http://" + page + "/"))
        before = len(jar)
        jar.extract_cookies(Response(header_pairs(f[2:])), req)
        reasons = [line.strip() for line in LOG
                   if line.startswith("   ") and not line.startswith("    ")]
        LOG.clear()
        kept = len(jar) - before
        third = "third-party" if req.unverifiable else "first-party"
        print("%s on %s (%s): %d of %d kept" % (url, page, third, kept, len(f) - 2))
        for r in reasons:
            print("  " + r)
    print("jar:")
    by_domain = {}
    for c in jar:
        by_domain.setdefault(c.domain, []).append(c.name)
    for d in sorted(by_domain):
        print("  %-14s %s" % (d, " ".join(sorted(by_domain[d]))))


if os.path.exists("work"):
    shutil.rmtree("work")
os.makedirs("work")
run_jobs()
login_program()
audit_program()
