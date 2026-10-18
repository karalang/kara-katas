#!/usr/bin/env python3
"""Python 3.13's html.parser over data/jobs.tsv: writes expected.out's text
to stdout. Run mk.py first."""
import html
from html.parser import HTMLParser


def esc(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\r":
            out.append("\\r")
        elif o < 32 or 0x7f <= o <= 0x9f:
            out.append("\\x%02x" % o)
        else:
            out.append(ch)
    return "".join(out)


def attr_text(attrs):
    parts = []
    for name, value in attrs:
        if value is None:
            parts.append(" " + esc(name))
        else:
            parts.append(' %s="%s"' % (esc(name), esc(value)))
    return "".join(parts)


class Collector(HTMLParser):
    def __init__(self, convert):
        super().__init__(convert_charrefs=convert)
        self.lines = []

    def emit(self, text):
        line, off = self.getpos()
        self.lines.append("  %d:%d %s" % (line, off, text))

    def handle_starttag(self, tag, attrs):
        self.emit("start " + tag + attr_text(attrs))

    def handle_startendtag(self, tag, attrs):
        self.emit("startend " + tag + attr_text(attrs))

    def handle_endtag(self, tag):
        self.emit("end " + tag)

    def handle_data(self, data):
        self.emit('data "%s"' % esc(data))

    def handle_comment(self, data):
        self.emit('comment "%s"' % esc(data))

    def handle_decl(self, decl):
        self.emit('decl "%s"' % esc(decl))

    def handle_pi(self, data):
        self.emit('pi "%s"' % esc(data))

    def unknown_decl(self, data):
        self.emit('unknown_decl "%s"' % esc(data))

    def handle_charref(self, name):
        self.emit("charref " + esc(name))

    def handle_entityref(self, name):
        self.emit("entityref " + esc(name))


def source(arg):
    if arg.startswith("@"):
        with open("data/pages/" + arg[1:], encoding="utf-8") as f:
            return f.read()
    return arg.replace("\\n", "\n")


def events(arg, convert, chunk):
    text = source(arg)
    p = Collector(convert == "1")
    n = int(chunk)
    if n == 0:
        p.feed(text)
    else:
        for k in range(0, len(text), n):
            p.feed(text[k:k + n])
    p.close()
    for line in p.lines:
        print(line)
    print("  end %d:%d" % p.getpos())


LINK_ATTRS = {"a": "href", "link": "href", "img": "src", "script": "src",
              "iframe": "src", "form": "action"}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []
        self.title = None
        self.in_title = False
        self.description = None

    def handle_starttag(self, tag, attrs):
        want = LINK_ATTRS.get(tag)
        for name, value in attrs:
            if name == want and value is not None:
                self.found.append("%s %s %s" % (tag, name, value))
        if tag == "title":
            self.in_title = True
            self.title = ""
        if tag == "meta":
            d = dict(attrs)
            if d.get("name") == "description" and d.get("content") is not None:
                self.description = d["content"]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def links(arg):
    p = Links()
    p.feed(source(arg))
    p.close()
    for f in p.found:
        print("  " + esc(f))
    print("  title: " + ("(none)" if p.title is None else esc(p.title)))
    print("  description: " + ("(none)" if p.description is None else esc(p.description)))


WS = " \t\n\r\f"


def collapse(s):
    out = []
    space = False
    for ch in s:
        if ch in WS:
            space = True
        else:
            if space and out:
                out.append(" ")
            elif space and not out:
                out.append(" ")
            space = False
            out.append(ch)
    if space:
        out.append(" ")
    return "".join(out)


BLOCKS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "pre", "br", "div",
          "tr", "article", "nav", "footer", "ul", "ol", "section", "header",
          "form", "label", "select", "option", "textarea", "plaintext"}
SKIP = {"script", "style", "title"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
        self.pre = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if tag == "pre":
            self.pre += 1
        if tag in BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip > 0:
            self.skip -= 1
        if tag == "pre" and self.pre > 0:
            self.pre -= 1
        if tag in BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip > 0:
            return
        if self.pre > 0:
            self.parts.append(data)
        else:
            self.parts.append(collapse(data))


def text(arg):
    p = Text()
    p.feed(source(arg))
    p.close()
    for line in "".join(p.parts).split("\n"):
        line = line.strip(WS)
        if line:
            print("  | " + esc(line))


class Toc(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cur = None
        self.items = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3"):
            ident = None
            for name, value in attrs:
                if name == "id":
                    ident = value
            self.cur = [int(tag[1]), ident, ""]

    def handle_endtag(self, tag):
        if self.cur is not None and tag == "h%d" % self.cur[0]:
            self.items.append(self.cur)
            self.cur = None

    def handle_data(self, data):
        if self.cur is not None:
            self.cur[2] += data


def toc(arg):
    p = Toc()
    p.feed(source(arg))
    p.close()
    if not p.items:
        print("  (no headings)")
    for level, ident, t in p.items:
        anchor = "" if ident is None else " (#%s)" % ident
        print("  " + "  " * (level - 1) + esc(collapse(t).strip(WS)) + esc(anchor))


ALLOWED = {"a": ["href", "title"], "b": [], "i": [], "em": [], "strong": [],
           "p": [], "ul": [], "li": [], "code": [], "pre": [], "br": [],
           "h1": [], "h2": [], "h3": []}
DROP = {"script", "style", "iframe", "title"}


class Sanitizer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []
        self.drop = 0
        self.removed_tags = 0
        self.removed_attrs = 0

    def handle_starttag(self, tag, attrs):
        self.start(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self.start(tag, attrs, True)

    def start(self, tag, attrs, closed):
        if tag in DROP:
            if not closed:
                self.drop += 1
            self.removed_tags += 1
            return
        if self.drop > 0:
            return
        if tag not in ALLOWED:
            self.removed_tags += 1
            self.removed_attrs += len(attrs)
            return
        s = "<" + tag
        for name, value in attrs:
            if name not in ALLOWED[tag] or value is None:
                self.removed_attrs += 1
                continue
            if name == "href" and value.strip(WS).lower().startswith("javascript:"):
                self.removed_attrs += 1
                continue
            s += ' %s="%s"' % (name, html.escape(value))
        if tag == "a":
            s += ' rel="nofollow"'
        s += ">"
        self.out.append(s)
        if closed and tag != "br":
            self.out.append("</%s>" % tag)

    def handle_endtag(self, tag):
        if tag in DROP:
            if self.drop > 0:
                self.drop -= 1
            return
        if self.drop > 0:
            return
        if tag not in ALLOWED:
            return
        if tag != "br":
            self.out.append("</%s>" % tag)

    def handle_data(self, data):
        if self.drop == 0:
            self.out.append(html.escape(data, quote=False))


def sanitize(arg):
    p = Sanitizer()
    p.feed(source(arg))
    p.close()
    for line in "".join(p.out).split("\n"):
        print("  | " + esc(line))
    print("  removed %d tags, %d attributes" % (p.removed_tags, p.removed_attrs))


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        jobs = f.read().splitlines()
    for job in jobs:
        f = job.split("\t")
        print("== " + esc(" | ".join(f)))
        kind = f[0]
        if kind == "events":
            events(f[1], f[2], f[3])
        elif kind == "unescape":
            print("  " + esc(html.unescape(f[1])))
        elif kind == "escape":
            print("  " + esc(html.escape(f[1], quote=f[2] == "1")))
        elif kind == "links":
            links(f[1])
        elif kind == "text":
            text(f[1])
        elif kind == "toc":
            toc(f[1])
        elif kind == "sanitize":
            sanitize(f[1])


main()
