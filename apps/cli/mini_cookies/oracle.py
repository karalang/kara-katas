# The reference: the same program written with Python 3.13's
# http.cookies (and urllib.parse.quote, which its js_output uses).
from http.cookies import SimpleCookie, CookieError


def lines(path):
    return open(path, encoding="utf-8").read().splitlines()


def show_morsels(c):
    for key, m in c.items():
        attrs = [f"{k}={v!r}" for k, v in m.items() if v != ""]
        print(f"  {key!r}: value={m.value!r} coded={m.coded_value!r} {' '.join(attrs)}".rstrip())


def show_load():
    print("== load")
    for line in lines("data/headers.txt"):
        print(repr(line))
        c = SimpleCookie()
        try:
            c.load(line)
        except CookieError as e:
            print(f"  CookieError: {e}")
        print(f"  {c!r}")
        show_morsels(c)
        for out in c.output().split("\r\n"):
            if out:
                print(f"  | {out}")


def attempt(label, f):
    try:
        f()
        print(f"{label}: ok")
    except CookieError as e:
        print(f"{label}: CookieError: {e}")


def show_build():
    print("== build")
    c = SimpleCookie()
    c["sid"] = "abc123"
    c["sid"]["path"] = "/"
    c["sid"]["max-age"] = 3600
    c["sid"]["httponly"] = True
    c["sid"]["secure"] = True
    c["sid"]["samesite"] = "Strict"
    c["pref"] = 'dark mode; "x"'
    c["pref"]["expires"] = "Thu, 01 Jan 2027 00:00:00 GMT"
    c["pref"]["comment"] = "user's choice"
    c["pref"]["Domain"] = "example.com"
    c["n"] = 42
    c["latin"] = "café \\ back"
    c["empty"] = ""
    c["sym"] = "a:b|c~d"
    attempt("c['café'] = 'x'", lambda: c.__setitem__("café", "x"))
    attempt("c['path'] = 'x'", lambda: c.__setitem__("path", "x"))
    attempt("c['a b'] = 'x'", lambda: c.__setitem__("a b", "x"))
    attempt("c['sid']['bogus'] = 1", lambda: c["sid"].__setitem__("bogus", 1))
    attempt("c['ctl'] = 'a\\nb'", lambda: c.__setitem__("ctl", "a\nb"))
    attempt("c['sid']['domain'] = 'ex\\x01.com'", lambda: c["sid"].__setitem__("domain", "ex\x01.com"))
    attempt("c['sid']['VERSION'] = '1'", lambda: c["sid"].__setitem__("VERSION", "1"))
    print(repr(c))
    show_morsels(c)
    for out in c.output().split("\r\n"):
        print(f"| {out}")
    for out in c.output(attrs=["path", "httponly"], header="Cookie:").split("\r\n"):
        print(f"| {out}")
    print(repr(c["pref"]))
    print(c["sid"].js_output(), end="|\n")


# ------------------------------------------------------------ the jar

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def days_from_civil(y, m, d):
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def parse_http_date(s):
    # "Wdy, DD Mon YYYY HH:MM:SS GMT", with - or space between the date parts
    _, comma, rest = s.partition(",")
    if not comma:
        return None
    parts = rest.replace("-", " ").split()
    if len(parts) != 5 or parts[4] != "GMT" or parts[1] not in MONTHS:
        return None
    if not (parts[0].isdigit() and parts[2].isdigit()):
        return None
    hms = parts[3].split(":")
    if len(hms) != 3 or not all(x.isdigit() for x in hms):
        return None
    day, year = int(parts[0]), int(parts[2])
    h, mi, se = (int(x) for x in hms)
    days = days_from_civil(year, MONTHS.index(parts[1]) + 1, day)
    return days * 86400 + h * 3600 + mi * 60 + se


def split_url(url):
    scheme, _, rest = url.partition("://")
    host, slash, path = rest.partition("/")
    path = "/" + path.partition("?")[0]
    return scheme, host.partition(":")[0].lower(), path


def default_path(path):
    if not path.startswith("/") or path.count("/") == 1:
        return "/"
    return path[:path.rfind("/")]


def domain_match(host, domain):
    return host == domain or host.endswith("." + domain)


def path_match(req, cpath):
    if req == cpath:
        return True
    if req.startswith(cpath):
        return cpath.endswith("/") or req[len(cpath)] == "/"
    return False


class Jar:
    def __init__(self):
        self.cookies = []   # dicts, in creation order
        self.now = 0
        self.serial = 0

    def store(self, url, header):
        scheme, host, path = split_url(url)
        c = SimpleCookie()
        try:
            c.load(header)
        except CookieError as e:
            print(f"  {header!r}: CookieError: {e}")
            return
        if not c:
            print(f"  {header!r}: nothing parsed")
            return
        for name, m in c.items():
            domain = m["domain"].lower().lstrip(".")
            if domain:
                if "." not in domain:
                    print(f"  {name}: rejected, domain {domain!r} is too broad")
                    continue
                if not domain_match(host, domain):
                    print(f"  {name}: rejected, domain {domain!r} does not match {host!r}")
                    continue
                host_only = False
            else:
                domain = host
                host_only = True
            cpath = m["path"] if m["path"].startswith("/") else default_path(path)
            if m["secure"] and scheme != "https":
                print(f"  {name}: rejected, Secure from an insecure origin")
                continue
            expiry = None
            if m["max-age"] != "":
                try:
                    age = int(m["max-age"])
                    expiry = self.now + age if age > 0 else 0
                except ValueError:
                    print(f"  {name}: Max-Age {m['max-age']!r} ignored")
            if expiry is None and m["expires"] != "":
                expiry = parse_http_date(m["expires"])
                if expiry is None:
                    print(f"  {name}: Expires {m['expires']!r} ignored")
            old = None
            for k in self.cookies:
                if (k["name"], k["domain"], k["path"]) == (name, domain, cpath):
                    old = k
            if old is not None:
                self.cookies.remove(old)
            if expiry is not None and expiry <= self.now:
                print(f"  {name}: {'deleted' if old else 'already expired'}")
                continue
            self.serial += 1
            created = old["created"] if old else self.serial
            self.cookies.append({"name": name, "value": m.coded_value, "domain": domain, "path": cpath,
                                 "host_only": host_only, "secure": bool(m["secure"]),
                                 "httponly": bool(m["httponly"]), "expiry": expiry, "created": created})
            print(f"  {name}: stored for {'' if host_only else '.'}{domain}{cpath}")

    def header_for(self, url):
        scheme, host, path = split_url(url)
        out = []
        for k in self.cookies:
            if k["expiry"] is not None and k["expiry"] <= self.now:
                continue
            if k["host_only"] and host != k["domain"]:
                continue
            if not k["host_only"] and not domain_match(host, k["domain"]):
                continue
            if not path_match(path, k["path"]):
                continue
            if k["secure"] and scheme != "https":
                continue
            out.append(k)
        out.sort(key=lambda k: (-len(k["path"]), k["created"]))
        return "; ".join(f"{k['name']}={k['value']}" for k in out)

    def dump(self):
        live = [k for k in self.cookies if k["expiry"] is None or k["expiry"] > self.now]
        for k in sorted(live, key=lambda k: (k["domain"], k["path"], k["name"])):
            flags = [f for f in ("secure", "httponly") if k[f]]
            if k["host_only"]:
                flags.append("host-only")
            exp = "session" if k["expiry"] is None else f"expires in {k['expiry'] - self.now}s"
            print(f"  {k['domain']}{k['path']} {k['name']}={k['value']} {exp} {' '.join(flags)}".rstrip())


def show_jar():
    print("== jar")
    jar = Jar()
    url = ""
    for line in lines("data/jar.txt"):
        words = line.split(" ", 1)
        if words[0] == "at":
            jar.now = int(words[1])
            print(f"-- at {jar.now}")
        elif words[0] == "resp":
            url = words[1]
            print(f"-- response from {url}")
        elif words[0] == "Set-Cookie:":
            jar.store(url, words[1])
        elif words[0] == "req":
            h = jar.header_for(words[1])
            print(f"-- request to {words[1]}")
            print(f"  Cookie: {h}" if h else "  (no cookies)")
        elif words[0] == "dump":
            print("-- jar")
            jar.dump()


show_load()
show_build()
show_jar()
