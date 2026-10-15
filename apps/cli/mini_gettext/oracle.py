# The oracle: mini_gettext written with Python 3.13's gettext. The .po
# compiler is the program's own, modelled on CPython's
# Tools/i18n/msgfmt.py; the .mo loader, the plural-form compiler and the
# lookups are gettext's.
import gettext, os, struct

SAMPLES = [0, 1, 2, 3, 4, 5, 7, 11, 12, 21, 22, 25, 100, 101, 111, 1000]

def unescape(s, lno):
    out, i = bytearray(), 0
    while i < len(s):
        c = s[i]
        if c == 0x5c:
            i += 1
            e = s[i:i + 1]
            m = {b"n": b"\n", b"t": b"\t", b"r": b"\r", b'"': b'"', b"\\": b"\\"}
            if e not in m:
                raise ValueError(f"line {lno}: unknown escape \\{e.decode('latin-1')}")
            out += m[e]
        else:
            out.append(c)
        i += 1
    return bytes(out)

def msgfmt(path):
    # returns (messages, stats) where messages maps key bytes to value bytes
    ID, STR, CTXT = 1, 2, 3
    messages = {}
    stats = {"fuzzy": 0, "empty": 0}
    section = None
    msgctxt = None
    msgid = msgstr = b""
    fuzzy = False
    is_plural = False

    def add():
        if fuzzy:
            stats["fuzzy"] += 1
        elif not msgstr or all(not p for p in msgstr.split(b"\0")):
            stats["empty"] += 1
        else:
            key = msgid if msgctxt is None else msgctxt + b"\x04" + msgid
            messages[key] = msgstr

    lines = open(path, "rb").read().split(b"\n")
    for lno, l in enumerate(lines, 1):
        if l[:1] == b"#" and section == STR:
            add()
            section, msgctxt, fuzzy = None, None, False
        if l[:2] == b"#," and b"fuzzy" in l:
            fuzzy = True
        if l[:1] == b"#":
            continue
        if l.startswith(b"msgctxt"):
            if section == STR:
                add()
                fuzzy = False
            section, msgctxt = CTXT, b""
            l = l[7:]
        elif l.startswith(b"msgid_plural"):
            if section != ID:
                raise ValueError(f"line {lno}: msgid_plural not preceded by msgid")
            l = l[12:]
            msgid += b"\0"
            is_plural = True
        elif l.startswith(b"msgid"):
            if section == STR:
                add()
                msgctxt, fuzzy = None, False
            section = ID
            l = l[5:]
            msgid = msgstr = b""
            is_plural = False
        elif l.startswith(b"msgstr"):
            section = STR
            if l.startswith(b"msgstr["):
                if not is_plural:
                    raise ValueError(f"line {lno}: plural without msgid_plural")
                l = l.split(b"]", 1)[1]
                if msgstr:
                    msgstr += b"\0"
            else:
                if is_plural:
                    raise ValueError(f"line {lno}: indexed msgstr required for plural")
                l = l[6:]
        l = l.strip()
        if not l:
            continue
        if len(l) < 2 or l[:1] != b'"' or l[-1:] != b'"':
            raise ValueError(f"line {lno}: syntax error before: {l.decode('latin-1')}")
        s = unescape(l[1:-1], lno)
        if section == CTXT:
            msgctxt += s
        elif section == ID:
            msgid += s
        elif section == STR:
            msgstr += s
        else:
            raise ValueError(f"line {lno}: syntax error before: {l.decode('latin-1')}")
    if section == STR:
        add()
    return messages, stats

def generate(messages):
    keys = sorted(messages)
    ids = strs = b""
    offs = []
    for k in keys:
        offs.append((len(ids), len(k), len(strs), len(messages[k])))
        ids += k + b"\0"
        strs += messages[k] + b"\0"
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    ko, vo = [], []
    for o1, l1, o2, l2 in offs:
        ko += [l1, o1 + keystart]
        vo += [l2, o2 + valuestart]
    out = struct.pack("<Iiiiiii", 0x950412de, 0, len(keys), 28, 28 + len(keys) * 8, 0, 0)
    out += struct.pack(f"<{len(ko + vo)}i", *(ko + vo))
    return out + ids + strs

def compile_all():
    print("== compile")
    for name in sorted(os.listdir("data/po")):
        lang = name[:-3]
        try:
            messages, stats = msgfmt(f"data/po/{name}")
        except ValueError as e:
            print(f"{name}: {e}")
            continue
        data = generate(messages)
        os.makedirs(f"data/locale/{lang}/LC_MESSAGES", exist_ok=True)
        with open(f"data/locale/{lang}/LC_MESSAGES/shop.mo", "wb") as f:
            f.write(data)
        plural = sum(1 for k in messages if b"\0" in k)
        ctx = sum(1 for k in messages if b"\x04" in k)
        print(f"{name}: {len(messages)} messages ({plural} plural, {ctx} with context), "
              f"{stats['fuzzy']} fuzzy and {stats['empty']} untranslated left out, {len(data)} bytes, "
              f"head {data[:28].hex()}")

def load(path):
    with open(path, "rb") as f:
        return gettext.GNUTranslations(f)

def show_catalog(path):
    try:
        t = load(path)
    except (OSError, ValueError) as e:
        print(f"{path}: {type(e).__name__}: {e}")
        return None
    info = t.info()
    print(f"{path}: charset {t.charset()}, {len(t._catalog)} entries")
    for k in sorted(info):
        print(f"  {k}: {info[k]!r}")
    print(f"  plural: {[t.plural(n) for n in SAMPLES]}")
    return t

def render(t, line):
    kind, rest = line.split(" ", 1)
    args = {"shop": "Kāra Books", "id": 1042}
    if kind == "_":
        rest = rest.replace("\\n", "\n")
        return [repr(t.gettext(rest).format(**args))]
    if kind == "p":
        ctx, msg = rest.split("|")
        return [f"{ctx}: {t.pgettext(ctx, msg)!r}"]
    parts = rest.split("|")
    if kind == "n":
        one, many, ns = parts
        return [f"{n}: {t.ngettext(one, many, int(n)).format(n=n)!r}" for n in ns.split(" ")]
    ctx, one, many, ns = parts
    return [f"{ctx} {n}: {t.npgettext(ctx, one, many, int(n)).format(n=n)!r}" for n in ns.split(" ")]

def show_ui():
    print("== ui")
    ui = [l for l in open("data/ui.txt").read().splitlines() if l and not l.startswith("#")]
    for chain in open("data/langs.txt").read().splitlines():
        langs = chain.split(" ")
        print(f"-- {' -> '.join(langs)} -> source")
        t = None
        for lang in langs:
            c = load(f"data/locale/{lang}/LC_MESSAGES/shop.mo")
            if t is None:
                t = c
            else:
                t.add_fallback(c)
        for line in ui:
            for out in render(t, line):
                print(f"  {line.split(' ', 1)[0]} {out}")

def show_plurals():
    print("== plural forms")
    for p in open("data/plurals.txt").read().split("\n")[:-1]:
        shown = p if len(p) < 60 else p[:57] + "..."
        try:
            f = gettext.c2py(p)
        except ValueError as e:
            print(f"{shown!r}: ValueError: {e}")
            continue
        expr, _ = gettext._parse(gettext._tokenize(p))
        vals = []
        for n in SAMPLES:
            try:
                vals.append(str(f(n)))
            except ZeroDivisionError as e:
                vals.append("ZeroDivisionError")
        print(f"{shown!r}: {expr if len(expr) < 90 else expr[:87] + '...'}")
        print(f"  {' '.join(vals)}")

def show_broken():
    print("== broken")
    for name in sorted(os.listdir("data/broken")):
        t = show_catalog(f"data/broken/{name}")
        if t is not None:
            print(f"  {t.gettext('Your cart')!r} {t.ngettext('{n} day left', '{n} days left', 2)!r} "
                  f"{t.ngettext('b', 'bs', 5)!r} {t.gettext('b')!r}")

def main():
    compile_all()
    print("== catalogs")
    for name in sorted(os.listdir("data/locale")):
        show_catalog(f"data/locale/{name}/LC_MESSAGES/shop.mo")
    show_ui()
    show_plurals()
    show_broken()

main()
