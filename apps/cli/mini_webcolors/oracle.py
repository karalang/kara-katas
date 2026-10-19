# Runs data/jobs.tsv through webcolors 24.11.1 (the files in webcolors/,
# unchanged) and prints what each operation returns; the audit job reads
# data/site.css. Run mk.py first.
import colorsys
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webcolors  # noqa: E402


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


def fmt(x, places):
    return f"{x:.{places}f}"


# ---------------------------------------------------------------- the audit

COLOR_PROPS = {"color", "background-color", "background", "border",
               "border-color", "border-top", "border-bottom", "outline",
               "fill", "stroke"}


def strip_comments(css):
    out, i = [], 0
    while i < len(css):
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            i = len(css) if j < 0 else j + 2
        else:
            out.append(css[i])
            i += 1
    return "".join(out)


def rules(css):
    css = strip_comments(css)
    out, i = [], 0
    while True:
        a = css.find("{", i)
        if a < 0:
            return out
        b = css.find("}", a)
        selector = css[i:a].strip()
        decls = []
        for d in css[a + 1:b].split(";"):
            if ":" not in d:
                continue
            prop, value = d.split(":", 1)
            decls.append((prop.strip().lower(), value.strip()))
        out.append((selector, decls))
        i = b + 1


def tokens(value):
    out, cur, depth = [], "", 0
    for c in value:
        if depth == 0 and (c in " \t\n" or c == ","):
            if cur:
                out.append(cur)
            cur = ""
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        cur += c
    if cur:
        out.append(cur)
    return out


def parse_color(tok, custom):
    # A token's color as a normalized hex, None when the token is not
    # meant as a color, or a ValueError when it is a broken one.
    low = tok.lower()
    if tok.startswith("#"):
        return webcolors.normalize_hex(tok)
    if low.startswith("rgb(") and tok.endswith(")"):
        args = [a.strip() for a in tok[4:-1].split(",")]
        if len(args) != 3:
            raise ValueError(f"rgb() takes three values, not {len(args)}")
        if all(a.endswith("%") for a in args):
            return webcolors.rgb_percent_to_hex(tuple(args))
        return webcolors.rgb_to_hex(tuple(int(a) for a in args))
    if low.startswith("var(") and tok.endswith(")"):
        name = tok[4:-1].strip()
        if name not in custom:
            raise ValueError(f"{name} is not defined")
        return custom[name]
    try:
        return webcolors.name_to_hex(tok)
    except ValueError:
        return None


def luminance(rgb):
    def chan(v):
        c = v / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def describe(h):
    rgb = webcolors.hex_to_rgb(h)
    try:
        name = webcolors.hex_to_name(h)
    except ValueError:
        name = "-"
    pct = webcolors.rgb_to_rgb_percent(rgb)
    hh, ll, ss = colorsys.rgb_to_hls(rgb.red / 255, rgb.green / 255, rgb.blue / 255)
    return (f"{h} {name} rgb({rgb.red}, {rgb.green}, {rgb.blue}) "
            f"rgb({pct.red}, {pct.green}, {pct.blue}) "
            f"hsl({fmt(hh * 360, 0)}, {fmt(ss * 100, 1)}%, {fmt(ll * 100, 1)}%)")


def nearest(h):
    rgb = webcolors.hex_to_rgb(h)
    best, best_d = "", -1
    for n in webcolors.names():
        o = webcolors.name_to_rgb(n)
        d = (o.red - rgb.red) ** 2 + (o.green - rgb.green) ** 2 + (o.blue - rgb.blue) ** 2
        if best_d < 0 or d < best_d:
            best, best_d = n, d
    return best, best_d


def audit(path):
    with open(path, encoding="utf-8") as fh:
        css = fh.read()
    custom, uses = {}, {}
    n_rules = n_decls = n_bad = n_pairs = n_fail = 0
    for selector, decls in rules(css):
        n_rules += 1
        print(f"   {selector}")
        resolved = {}
        for prop, value in decls:
            if not (prop in COLOR_PROPS or prop.startswith("--")):
                continue
            n_decls += 1
            found = []
            try:
                for tok in tokens(value):
                    h = parse_color(tok, custom)
                    if h is not None:
                        found.append((tok, h))
            except ValueError as e:
                n_bad += 1
                print(f"     {prop}: {value} -> invalid: {e}")
                continue
            if not found:
                if prop in ("color", "background-color"):
                    n_bad += 1
                    print(f"     {prop}: {value} -> not a color")
                continue
            for tok, h in found:
                print(f"     {prop}: {tok} -> {describe(h)}")
                uses[h] = uses.get(h, 0) + 1
            if prop.startswith("--"):
                custom[prop] = found[0][1]
            if prop == "background" and "background-color" not in resolved:
                resolved["background-color"] = found[0][1]
            resolved[prop] = found[0][1]
        if "color" in resolved and "background-color" in resolved:
            n_pairs += 1
            fg = luminance(webcolors.hex_to_rgb(resolved["color"]))
            bg = luminance(webcolors.hex_to_rgb(resolved["background-color"]))
            hi, lo = max(fg, bg), min(fg, bg)
            ratio = (hi + 0.05) / (lo + 0.05)
            if ratio >= 7:
                grade = "AAA"
            elif ratio >= 4.5:
                grade = "AA"
            elif ratio >= 3:
                grade = "AA large text only"
            else:
                grade = "fails"
                n_fail += 1
            print(f"     contrast {fmt(ratio, 2)}:1 (L {fmt(fg, 4)} on {fmt(bg, 4)}) {grade}")
    print("   palette:")
    for h in sorted(uses):
        try:
            name = webcolors.hex_to_name(h)
        except ValueError:
            n, d = nearest(h)
            name = f"~{n} (distance^2 {d})"
        print(f"     {h} x{uses[h]} {name}")
    print(f"   {n_rules} rules, {n_decls} color declarations, {n_bad} invalid, "
          f"{len(uses)} distinct colors, {n_pairs} contrast pairs, {n_fail} failing")


# ---------------------------------------------------------------- operations

def triple(args):
    return tuple(int(a) for a in args[:3])


def run(f):
    op, args = f[0], f[1:]
    if op == "audit":
        print("-- audit " + repr(args[0]))
        audit(os.path.join("data", args[0]))
        return
    print("-- " + op + "".join(" " + repr(a) for a in args))
    w = webcolors
    try:
        if op == "names":
            r = w.names(args[0])
        elif op == "name_to_hex":
            r = w.name_to_hex(args[0], args[1])
        elif op == "name_to_rgb":
            r = w.name_to_rgb(args[0], args[1])
        elif op == "name_to_rgb_percent":
            r = w.name_to_rgb_percent(args[0], args[1])
        elif op == "normalize_hex":
            r = w.normalize_hex(args[0])
        elif op == "hex_to_name":
            r = w.hex_to_name(args[0], args[1])
        elif op == "hex_to_rgb":
            r = w.hex_to_rgb(args[0])
        elif op == "hex_to_rgb_percent":
            r = w.hex_to_rgb_percent(args[0])
        elif op == "normalize_integer_triplet":
            r = w.normalize_integer_triplet(triple(args))
        elif op == "rgb_to_hex":
            r = w.rgb_to_hex(triple(args))
        elif op == "rgb_to_rgb_percent":
            r = w.rgb_to_rgb_percent(triple(args))
        elif op == "rgb_to_name":
            r = w.rgb_to_name(triple(args), args[3])
        elif op == "html5_serialize_simple_color":
            r = w.html5_serialize_simple_color(triple(args))
        elif op == "normalize_percent_triplet":
            r = w.normalize_percent_triplet(tuple(args[:3]))
        elif op == "rgb_percent_to_rgb":
            r = w.rgb_percent_to_rgb(tuple(args[:3]))
        elif op == "rgb_percent_to_hex":
            r = w.rgb_percent_to_hex(tuple(args[:3]))
        elif op == "rgb_percent_to_name":
            r = w.rgb_percent_to_name(tuple(args[:3]), args[3])
        elif op == "html5_parse_simple_color":
            r = w.html5_parse_simple_color(args[0])
        elif op == "html5_parse_legacy_color":
            r = w.html5_parse_legacy_color(args[0])
        elif op == "percent_roundtrip":
            same = 0
            for d in range(256):
                p = w.rgb_to_rgb_percent((d, d, d))
                back = w.rgb_percent_to_rgb(p)
                if back.red == d:
                    same += 1
                else:
                    print(f"   {d} -> {p.red} -> {back.red}")
            print(f"   {same} of 256 come back")
            return
        elif op == "name_roundtrip":
            all_names = w.names(args[0])
            same = 0
            for n in all_names:
                h = w.name_to_hex(n, args[0])
                p = w.rgb_to_rgb_percent(w.hex_to_rgb(h))
                h2 = w.rgb_percent_to_hex(p)
                n2 = w.hex_to_name(h2, args[0])
                if n2 == n:
                    same += 1
                else:
                    print(f"   {n} -> {h} -> {p.red} {p.green} {p.blue} -> {h2} -> {n2}")
            print(f"   {len(all_names)} names, {same} come back as themselves")
            return
        else:
            raise SystemExit("unknown op " + op)
    except ValueError as e:
        print(f"   error: ValueError: {e}")
        return
    print(f"   {r!r}")


with open("data/jobs.tsv", encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if line.startswith("== "):
            print(line)
            continue
        run([unesc(x) for x in line.split("\t")])
