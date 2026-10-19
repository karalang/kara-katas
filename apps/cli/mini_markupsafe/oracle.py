# Runs data/jobs.tsv through markupsafe 3.0.4 (the Python files in
# markupsafe/, unchanged; the C speedups are left out, so markupsafe
# uses its own pure-Python escape) and prints what each operation
# returns. Run mk.py first.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from markupsafe import Markup, escape, escape_silent, soft_str  # noqa: E402


class User:
    """A model with __html__ and __html_format__, as a framework's user."""

    def __init__(self, name, email, id):
        self.name, self.email, self.id = name, email, id

    def __html__(self):
        return Markup('<a href="mailto:{0}">{1}</a>').format(self.email, self.name)

    def __html_format__(self, spec):
        if spec in ("", "link"):
            return self.__html__()
        if spec == "name":
            return escape(self.name)
        raise ValueError(f"Invalid format spec {spec!r} for User")

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def __repr__(self):
        return f"User({self.name!r}, {self.id})"


class Badge:
    """A widget with __html__ only."""

    def __init__(self, label):
        self.label = label

    def __html__(self):
        return f'<span class="badge">{escape(self.label)}</span>'

    def __repr__(self):
        return f"Badge({self.label!r})"


class Plain:
    """An object with no __html__."""

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Plain({self.text!r})"


ENV = {"Markup": Markup, "User": User, "Badge": Badge, "Plain": Plain, "__builtins__": {}}


def val(x):
    return eval(x, ENV)


def unesc(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append({"t": "\t", "n": "\n", "\\": "\\"}[s[i + 1]])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def call(m, meth, args):
    a = val("(" + args + ",)") if args else ()
    if meth == "getitem":
        return m[a[0]]
    if meth == "slice":
        return m[slice(*a)]
    return getattr(m, meth)(*a)


def preview(html):
    text = Markup(html).striptags()
    return text if len(text) <= 40 else text[:39] + "…"


def thread(title, comments):
    out = [Markup("<h1>%s</h1>") % title, Markup("<ul>")]
    for user, body, score, tags, html in comments:
        badges = Markup(" ").join(Badge(t) for t in tags)
        lines = escape(body).split("\n")
        out.append(Markup('<li id="c{0}"><p>{1:link} {2:+d}{3}</p>').format(
            user.id, user, score, (Markup(" ") + badges) if tags else ""))
        out.append(Markup("<div>{}</div>").format(Markup("<br>").join(lines)))
        if html is not None:
            out.append(Markup('<p class="preview" title="%s">%s</p>') % (preview(html), Markup(html)))
        out.append(Markup("</li>"))
    out.append(Markup("</ul>"))
    out.append(Markup("<p>%d comments by %s</p>") % (len(comments), ", ".join(str(c[0]) for c in comments)))
    return Markup("\n").join(out)


def run(f):
    op, args = f[0], f[1:]
    print("-- " + op + "".join(" " + a for a in args))
    if op == "thread":
        for line in thread(val(args[0]), val(args[1])).split("\n"):
            print("   " + line)
        return
    try:
        if op == "escape":
            r = escape(val(args[0]))
        elif op == "escape_silent":
            r = escape_silent(val(args[0]))
        elif op == "soft_str":
            r = soft_str(val(args[0]))
        elif op == "markup":
            r = Markup(val(args[0]))
        elif op == "str":
            r = str(val(args[0]))
        elif op == "repr":
            r = repr(val(args[0]))
        elif op == "add":
            r = val(args[0]) + val(args[1])
        elif op == "mul":
            r = val(args[0]) * val(args[1])
        elif op == "rmul":
            r = val(args[0]) * val(args[1])
        elif op == "mod":
            r = val(args[0]) % val(args[1])
        elif op == "format":
            r = val(args[0]).format(*val(args[1]), **val(args[2]))
        elif op == "format_map":
            r = val(args[0]).format_map(val(args[1]))
        elif op == "call":
            r = call(val(args[0]), args[1], args[2])
        elif op == "striptags":
            r = val(args[0]).striptags()
        elif op == "unescape":
            r = val(args[0]).unescape()
        else:
            raise SystemExit("unknown op " + op)
    except (TypeError, ValueError, KeyError, IndexError, AttributeError) as e:
        print(f"   error: {type(e).__name__}: {e}")
        return
    print(f"   {r!r}")


with open("data/jobs.tsv", encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if line.startswith("== "):
            print(line)
            continue
        run([unesc(x) for x in line.split("\t")])
