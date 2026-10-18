# The oracle for mini_nginx: the same config check and request routing in
# Python, with `re` for the patterns. expected.out is its output.
import os, re, shutil
import mk

KNOWN = {"worker_processes", "events", "worker_connections", "http", "include",
         "default_type", "upstream", "server", "listen", "server_name", "root",
         "index", "rewrite", "location", "return", "try_files", "add_header",
         "proxy_pass", "alias", "types"}
REASONS = {200: "OK", 301: "Moved Permanently", 302: "Found", 400: "Bad Request",
           403: "Forbidden", 404: "Not Found", 500: "Internal Server Error"}
HEADER_CODES = {200, 201, 204, 206, 301, 302, 303, 304, 307, 308}
MAX_URI_CHANGES = 10


class ConfError(Exception):
    pass


class Directive:
    def __init__(self, name, args, line):
        self.name = name
        self.args = args
        self.line = line
        self.block = None


# ------------------------------------------------------------ the parser

def tokenize(text, path):
    """Tokens as (kind, text, line): kind is 'word', ';', '{', '}'."""
    toks = []
    i = 0
    line = 1
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\n":
            line += 1
            i += 1
        elif c in " \t\r":
            i += 1
        elif c == "#":
            while i < n and text[i] != "\n":
                i += 1
        elif c in ";{}":
            toks.append((c, c, line))
            i += 1
        elif c in "\"'":
            q = c
            i += 1
            out = ""
            start = line
            while True:
                if i >= n:
                    raise ConfError("unexpected end of file, expecting %s in %s:%d" % ('"' if q == '"' else "'", path, line))
                c = text[i]
                if c == "\\" and i + 1 < n:
                    e = text[i + 1]
                    out += {"n": "\n", "t": "\t", "r": "\r"}.get(e, e if e in "\"'\\" else "\\" + e)
                    i += 2
                    continue
                if c == q:
                    i += 1
                    break
                if c == "\n":
                    line += 1
                out += c
                i += 1
            toks.append(("word", out, start))
        else:
            out = ""
            while i < n and text[i] not in " \t\r\n;{}":
                out += text[i]
                i += 1
            toks.append(("word", out, line))
    return toks, line


def parse_block(toks, pos, path, eof_line, top, in_types, base_dir):
    out = []
    while True:
        if pos >= len(toks):
            if top:
                return out, pos
            raise ConfError('unexpected end of file, expecting "}" in %s:%d' % (path, eof_line))
        kind, text, line = toks[pos]
        if kind == "}":
            if top:
                raise ConfError('unexpected "}" in %s:%d' % (path, line))
            return out, pos + 1
        if kind != "word":
            raise ConfError('unexpected "%s" in %s:%d' % (kind, path, line))
        name = text
        args = []
        pos += 1
        while True:
            if pos >= len(toks):
                raise ConfError('unexpected end of file, expecting ";" or "}" in %s:%d' % (path, eof_line))
            k, t, l = toks[pos]
            if k == "word":
                args.append(t)
                pos += 1
            elif k == "}":
                raise ConfError('unexpected "}" in %s:%d' % (path, l))
            else:
                break
        if not in_types and name not in KNOWN:
            raise ConfError('unknown directive "%s" in %s:%d' % (name, path, line))
        d = Directive(name, args, line)
        k = toks[pos][0]
        pos += 1
        if k == "{":
            d.block, pos = parse_block(toks, pos, path, eof_line, False, name == "types", base_dir)
            out.append(d)
        elif name == "include" and not in_types:
            out.extend(load(os.path.join(base_dir, args[0])))
        else:
            out.append(d)
    return out, pos


def load(path):
    text = open(path).read()
    toks, eof_line = tokenize(text, path)
    tree, _ = parse_block(toks, 0, path, eof_line, True, False, os.path.dirname(path))
    return tree


# ------------------------------------------------------------ the model

class Location:
    def __init__(self, d):
        if len(d.args) == 2:
            self.mod, self.pattern = d.args
        else:
            self.mod, self.pattern = "", d.args[0]
        self.body = d.block
        self.regex = None
        if self.mod == "~":
            self.regex = re.compile(py_re(self.pattern))
        elif self.mod == "~*":
            self.regex = re.compile("(?i)" + py_re(self.pattern))

    def label(self):
        return (self.mod + " " if self.mod else "") + self.pattern

    def first(self, name):
        for d in self.body:
            if d.name == name:
                return d
        return None


class Server:
    def __init__(self, d, http):
        self.listen = 80
        self.default = False
        self.names = []
        self.root = None
        self.index = ["index.html"]
        self.rewrites = []
        self.locations = []
        self.http = http
        for c in d.block:
            if c.name == "listen":
                self.listen = int(c.args[0])
                self.default = "default_server" in c.args[1:]
            elif c.name == "server_name":
                self.names = c.args
            elif c.name == "root":
                self.root = c.args[0]
            elif c.name == "index":
                self.index = c.args
            elif c.name in ("rewrite", "return"):
                self.rewrites.append(c)
            elif c.name == "location":
                self.locations.append(Location(c))

    def label(self):
        return self.names[0] if self.names else '""'


def py_re(p):
    return p.replace("(?<", "(?P<")


# ------------------------------------------------------------ requests

def normalize(uri):
    """Decoded, merged and resolved, or None for a path above the root."""
    out = bytearray()
    raw = uri.encode()
    i = 0
    while i < len(raw):
        if raw[i] == ord("%") and i + 2 < len(raw) + 0 and re.fullmatch(b"[0-9A-Fa-f]{2}", raw[i + 1:i + 3]):
            out.append(int(raw[i + 1:i + 3], 16))
            i += 3
        else:
            out.append(raw[i])
            i += 1
    parts = []
    segs = out.decode().split("/")
    for s in segs[1:]:
        if s == "" or s == ".":
            continue
        if s == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(s)
    path = "/" + "/".join(parts)
    if (segs[-1] in ("", ".", "..")) and path != "/":
        path += "/"
    return path


class Req:
    def __init__(self, port, host, target):
        self.port = port
        self.host = host.lower().split(":")[0]
        q = target.find("?")
        self.raw_uri = target if q < 0 else target[:q]
        self.args = "" if q < 0 else target[q + 1:]
        self.request_uri = target
        self.uri = None
        self.caps = []
        self.named = {}
        self.lines = []

    def var(self, name):
        if name.isdigit():
            i = int(name)
            return self.caps[i] if i < len(self.caps) and self.caps[i] is not None else ""
        if name == "uri":
            return self.uri
        if name == "args":
            return self.args
        if name == "host":
            return self.host
        if name == "request_uri":
            return self.request_uri
        if name == "scheme":
            return "http"
        if name == "server_port":
            return str(self.port)
        return self.named.get(name, "")

    def expand(self, s):
        out = ""
        i = 0
        while i < len(s):
            if s[i] == "$" and i + 1 < len(s):
                if s[i + 1] == "{":
                    j = s.index("}", i)
                    out += self.var(s[i + 2:j])
                    i = j + 1
                    continue
                j = i + 1
                if s[j].isdigit():
                    out += self.var(s[j])
                    i = j + 1
                    continue
                while j < len(s) and (s[j].isalnum() or s[j] == "_"):
                    j += 1
                if j > i + 1:
                    out += self.var(s[i + 1:j])
                    i = j
                    continue
            out += s[i]
            i += 1
        return out

    def set_caps(self, m):
        self.caps = [m.group(0)] + list(m.groups())
        for k, v in m.groupdict().items():
            if v is not None:
                self.named[k] = v

    def location_url(self, target):
        if target.startswith("http://") or target.startswith("https://"):
            return target
        port = "" if self.port == 80 else ":%d" % self.port
        return "http://%s%s%s" % (self.host, port, target)


def pick_server(servers, port, host):
    cands = [s for s in servers if s.listen == port]
    for s in cands:
        if host in s.names:
            return s, None
    best = None
    for s in cands:
        for n in s.names:
            if n.startswith("*.") and host.endswith(n[1:]):
                if best is None or len(n) > len(best[1]):
                    best = (s, n)
    if best:
        return best[0], None
    for s in cands:
        for n in s.names:
            if n.endswith(".*") and host.startswith(n[:-1]):
                if best is None or len(n) > len(best[1]):
                    best = (s, n)
    if best:
        return best[0], None
    for s in cands:
        for n in s.names:
            if n.startswith("~"):
                m = re.search(py_re(n[1:]), host)
                if m:
                    return s, m
    for s in cands:
        if s.default:
            return s, None
    return (cands[0] if cands else None), None


def find_location(srv, req):
    for loc in srv.locations:
        if loc.mod == "=" and loc.pattern == req.uri:
            return loc
    best = None
    for loc in srv.locations:
        if loc.mod in ("", "^~") and req.uri.startswith(loc.pattern):
            if best is None or len(loc.pattern) > len(best.pattern):
                best = loc
    if best is not None and best.mod == "^~":
        return best
    for loc in srv.locations:
        if loc.regex is not None:
            m = loc.regex.search(req.uri)
            if m:
                req.set_caps(m)
                return loc
    return best


class Done(Exception):
    def __init__(self, status, text=None, location=None, path=None):
        self.status = status
        self.text = text
        self.location = location
        self.path = path


def run_rewrites(directives, req):
    """'last', 'break' or None; raises Done for a return or redirect."""
    for d in directives:
        if d.name == "return":
            code = int(d.args[0])
            arg = req.expand(d.args[1]) if len(d.args) > 1 else None
            if code in (301, 302, 303, 307, 308):
                raise Done(code, location=req.location_url(arg))
            raise Done(code, text=arg)
        m = re.search(py_re(d.args[0]), req.uri)
        if not m:
            continue
        req.set_caps(m)
        repl = req.expand(d.args[1])
        flag = d.args[2] if len(d.args) > 2 else ""
        if "?" in repl:
            q = repl.index("?")
            new_args = repl[q + 1:]
            repl = repl[:q]
            if new_args.endswith("?"):
                req.args = new_args[:-1]
            elif new_args and req.args:
                req.args = new_args + "&" + req.args
            elif new_args:
                req.args = new_args
        redirect = repl.startswith("http://") or repl.startswith("https://")
        if redirect or flag in ("redirect", "permanent"):
            url = req.location_url(repl) + ("?" + req.args if req.args else "")
            req.lines.append("rewrite: %s (%s)" % (url, flag or "redirect"))
            raise Done(301 if flag == "permanent" else 302, location=url)
        req.uri = repl
        req.lines.append("rewrite: %s%s (%s)" % (repl, "?" + req.args if req.args else "", flag or "continue"))
        if flag in ("last", "break"):
            return flag
    return None


def path_for(srv, loc, req, uri):
    alias = loc.first("alias") if loc else None
    if alias is not None:
        return req.expand(alias.args[0]) + uri[len(loc.pattern):]
    root = loc.first("root") if loc else None
    base = root.args[0] if root is not None else (srv.root or "html")
    return req.expand(base) + uri


def is_file(p):
    return os.path.isfile(p)


def is_dir(p):
    return os.path.isdir(p)


def handle(srv, req, upstreams, rr):
    changes = 0
    server_phase = True
    while True:
        if server_phase:
            run_rewrites(srv.rewrites, req)
        server_phase = False
        loc = find_location(srv, req)
        if loc is None:
            raise Done(404)
        req.lines.append("location: " + loc.label())
        flag = run_rewrites([d for d in loc.body if d.name in ("rewrite", "return")], req)
        if flag == "last":
            changes += 1
            if changes > MAX_URI_CHANGES:
                raise Done(500, text="rewrite or internal redirection cycle")
            continue
        pp = loc.first("proxy_pass")
        if pp is not None:
            name = pp.args[0].split("://", 1)[1]
            peers = upstreams.get(name, [name])
            i = rr.get(name, 0)
            rr[name] = i + 1
            peer = peers[i % len(peers)]
            target = req.uri + ("?" + req.args if req.args else "")
            raise Done(200, text="proxied to http://%s%s" % (peer, target))
        tf = loc.first("try_files")
        uri = req.uri
        if tf is not None:
            hit = None
            for a in tf.args[:-1]:
                cand = req.expand(a)
                p = path_for(srv, loc, req, cand)
                if (cand.endswith("/") and is_dir(p)) or (not cand.endswith("/") and is_file(p)):
                    hit = cand
                    break
            if hit is None:
                last = tf.args[-1]
                if last.startswith("="):
                    req.lines.append("try_files: " + last)
                    raise Done(int(last[1:]))
                target = req.expand(last)
                req.lines.append("internal redirect: " + target)
                q = target.find("?")
                if q >= 0:
                    req.args = target[q + 1:]
                    target = target[:q]
                req.uri = target
                changes += 1
                if changes > MAX_URI_CHANGES:
                    raise Done(500, text="rewrite or internal redirection cycle")
                server_phase = True
                continue
            req.lines.append("try_files: " + hit)
            uri = hit
        path = path_for(srv, loc, req, uri)
        if uri.endswith("/"):
            for name in srv.index:
                if is_file(path + name):
                    req.lines.append("index: " + uri + name)
                    req.uri = uri + name
                    changes += 1
                    break
            else:
                if is_dir(path):
                    raise Done(403, text='directory index of "%s" is forbidden' % path)
                raise Done(404)
            server_phase = True
            continue
        if is_file(path):
            raise Done(200, path=path)
        if is_dir(path):
            raise Done(301, location=req.location_url(uri + "/"))
        raise Done(404, text='open() "%s" failed' % path)


def headers_of(srv, loc):
    hs = []
    if loc is not None:
        hs = [d for d in loc.body if d.name == "add_header"]
    return hs


def show(s):
    return s.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def mime(types, default, path):
    name = path.rsplit("/", 1)[-1]
    if "." not in name:
        return default
    return types.get(name.rsplit(".", 1)[1].lower(), default)


def serve(servers, upstreams, rr, types, default, port, host, target):
    req = Req(port, host, target)
    print("GET %d %s %s" % (port, host, target))
    srv, m = pick_server(servers, port, req.host)
    if srv is None:
        print("  no server listens on %d" % port)
        return
    if m is not None:
        req.set_caps(m)
    print("  server: %s (listen %d)" % (srv.label(), srv.listen))
    n = normalize(req.raw_uri)
    if n is None:
        d = Done(400)
    else:
        req.uri = n
        if n != req.raw_uri:
            print("  normalized: " + n)
        try:
            handle(srv, req, upstreams, rr)
            d = Done(404)
        except Done as e:
            d = e
    for l in req.lines:
        print("  " + l)
    last_loc = None
    for l in req.lines:
        if l.startswith("location: "):
            last_loc = l[len("location: "):]
    out = "  %d" % d.status
    if d.status == 444:
        out += " (connection closed)"
    elif d.path is not None:
        size = os.path.getsize(d.path)
        out += " %s %d bytes %s" % (mime(types, default, d.path), size, d.path)
    elif d.location is not None:
        out += " Location: " + d.location
    elif d.text is not None:
        out += ' "%s"' % show(d.text)
    else:
        out += " " + REASONS.get(d.status, "")
    print(out)
    if d.status in HEADER_CODES and last_loc is not None:
        loc = [l for l in srv.locations if l.label() == last_loc][0]
        for h in headers_of(srv, loc):
            print("  header: %s: %s" % (h.args[0], h.args[1]))


def check(path):
    try:
        tree = load(path)
    except ConfError as e:
        print("nginx: [emerg] " + str(e))
        print("nginx: configuration file %s test failed" % path)
        return None
    print("nginx: the configuration file %s syntax is ok" % path)
    print("nginx: configuration file %s test is successful" % path)
    return tree


def main():
    shutil.rmtree("data", ignore_errors=True)
    mk.write_all()
    for b in ("data/broken1.conf", "data/broken2.conf", "data/broken3.conf"):
        check(b)
    tree = check("data/nginx.conf")
    http = [d for d in tree if d.name == "http"][0]
    types = {}
    default = "text/plain"
    upstreams = {}
    servers = []
    for d in http.block:
        if d.name == "types":
            for t in d.block:
                for ext in t.args:
                    types[ext] = t.name
        elif d.name == "default_type":
            default = d.args[0]
        elif d.name == "upstream":
            upstreams[d.args[0]] = [s.args[0] for s in d.block if s.name == "server"]
        elif d.name == "server":
            servers.append(Server(d, http))
    nloc = sum(len(s.locations) for s in servers)
    print("%d servers, %d locations, %d upstreams, %d types" % (len(servers), nloc, len(upstreams), len(types)))
    print()
    rr = {}
    for line in open("data/requests.txt").read().split("\n"):
        if line == "" or line.startswith("#"):
            continue
        method, port, host, target = line.split(" ")
        serve(servers, upstreams, rr, types, default, int(port), host, target)
    for name, peers in upstreams.items():
        print("upstream %s: %d request(s) over %d peers" % (name, rr.get(name, 0), len(peers)))


main()
