# Runs data/ through Python 3.13's own tokenize module and prints what
# expected.out holds. Run it from the app directory, after mk.py.
import ast
import io
import keyword
import os
import tokenize
from tokenize import tok_name

SKIP = {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
        tokenize.DEDENT, tokenize.ENDMARKER, tokenize.ENCODING}


def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [line[:-1] if line.endswith("\n") else line for line in f]


# Runs a tokenizer to the end or to its error: the tokens it made, and
# the error as `python -m tokenize` reports it (message, line, column).
def run(gen):
    toks = []
    try:
        for t in gen:
            toks.append(t)
    except (IndentationError, TabError) as e:
        line, col = e.args[1][1:3]
        return toks, (type(e).__name__, e.args[0], line, col)
    except tokenize.TokenError as e:
        line, col = e.args[1]
        return toks, ("TokenError", e.args[0], line, col)
    return toks, None


def file_tokens(path):
    with open(path, "rb") as f:
        return run(tokenize.tokenize(f.readline))


def source_text(path):
    # the text the tokenizer read, decoded as detect_encoding said
    with open(path, "rb") as f:
        enc, _ = tokenize.detect_encoding(f.readline)
    with open(path, "rb") as f:
        raw = f.read()
    return raw.decode(enc)


def project_files():
    out = []
    for root, dirs, files in os.walk("data/project"):
        for f in files:
            out.append(os.path.join(root, f))
    return sorted(out)


def broken_files():
    return sorted("data/broken/" + f for f in os.listdir("data/broken"))


# ------------------------------------------------------------ jobs

def run_jobs():
    print("== snippets")
    for line in read_lines("data/jobs.tsv"):
        op, lit = line.split("\t")
        src = ast.literal_eval(lit)
        print("snippet " + lit)
        toks, err = run(tokenize.generate_tokens(io.StringIO(src).readline))
        for t in toks:
            print("  %d,%d-%d,%d %s %r" % (t.start + t.end + (tok_name[t.exact_type], t.string)))
        if err:
            print("  ! %s: %s at %d,%d" % err)


# ------------------------------------------------------------ programs

# python -m tokenize -e FILE
def dump(path):
    print("== python -m tokenize -e " + path)
    toks, err = file_tokens(path)
    for t in toks:
        token_range = "%d,%d-%d,%d:" % (t.start + t.end)
        print(("%-20s%-15s%-15r" % (token_range, tok_name[t.exact_type], t.string)).rstrip())
    if err:
        print("%s:%d:%d: error: %s" % (path, err[2], err[3], err[1]))


# Line counts in the manner of `radon raw`: a line is code if a token
# other than a comment or layout token covers it, doc if a string that is
# a statement by itself does, comment if it holds a comment, and blank
# otherwise.
def stats(paths):
    print("== stats")
    print("%-34s %5s %5s %5s %5s %5s %7s %6s %5s %5s" % (
        "file", "lines", "code", "doc", "cmnt", "blank", "logical", "tokens", "paren", "depth"))
    for path in paths:
        toks, err = file_tokens(path)
        nlines = len(source_text(path).splitlines())
        code, doc, comment = set(), set(), set()
        for i, t in enumerate(toks):
            if t.type == tokenize.COMMENT:
                comment.add(t.start[0])
            if t.type in SKIP:
                continue
            j = i - 1
            while j >= 0 and toks[j].type in (tokenize.COMMENT, tokenize.NL):
                j -= 1
            k = i + 1
            while k < len(toks) and toks[k].type == tokenize.COMMENT:
                k += 1
            alone = (t.type == tokenize.STRING
                     and (j < 0 or toks[j].type in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING))
                     and k < len(toks) and toks[k].type == tokenize.NEWLINE)
            target = doc if alone else code
            for row in range(t.start[0], t.end[0] + 1):
                target.add(row)
        doc -= code
        comment -= code | doc
        blank = nlines - len(code) - len(doc) - len(comment)
        logical = sum(1 for t in toks if t.type == tokenize.NEWLINE)
        paren = depth = maxp = maxd = 0
        for t in toks:
            if t.type == tokenize.OP and t.string in "([{":
                paren += 1
                maxp = max(maxp, paren)
            elif t.type == tokenize.OP and t.string in ")]}":
                paren -= 1
            elif t.type == tokenize.INDENT:
                depth += 1
                maxd = max(maxd, depth)
            elif t.type == tokenize.DEDENT:
                depth -= 1
        name = path[len("data/"):]
        print("%-34s %5d %5d %5d %5d %5d %7d %6d %5d %5d" % (
            name, nlines, len(code), len(doc), len(comment), blank, logical, len(toks), maxp, maxd))
        if err:
            print("  stopped at %d,%d: %s: %s" % (err[2], err[3], err[0], err[1]))


TAGS = ("TODO", "FIXME", "XXX")


def is_word(c):
    return c.isalnum() or c == "_"


def todos(paths):
    print("== todo comments")
    for path in paths:
        toks, err = file_tokens(path)
        for t in toks:
            if t.type != tokenize.COMMENT:
                continue
            text = t.string
            best = None
            for tag in TAGS:
                i = text.find(tag)
                while i >= 0:
                    before = text[i - 1] if i > 0 else " "
                    after = text[i + len(tag)] if i + len(tag) < len(text) else " "
                    if not is_word(before) and not is_word(after):
                        if best is None or i < best[0]:
                            best = (i, tag)
                        break
                    i = text.find(tag, i + 1)
            if best is None:
                continue
            i, tag = best
            rest = text[i + len(tag):].lstrip(":").strip()
            print("%s:%d:%d: %s %s" % (path, t.start[0], t.start[1] + i, tag, rest))


# A few flake8 checks that need only tokens.
def lint(paths):
    print("== lint")
    for path in paths:
        toks, err = file_tokens(path)
        lines = source_text(path).splitlines()
        found = []
        for n, line in enumerate(lines, 1):
            if len(line) > 79:
                found.append((n, 80, "E501 line too long (%d > 79 characters)" % len(line)))
            lead = line[:len(line) - len(line.lstrip(" \t"))]
            if "\t" in lead and line.strip():
                found.append((n, 1, "W191 indentation contains tabs"))
        sig = [t for t in toks if t.type not in SKIP or t.type == tokenize.COMMENT]
        fstack = []
        for i, t in enumerate(sig):
            prev = sig[i - 1] if i > 0 else None
            nxt = sig[i + 1] if i + 1 < len(sig) else None
            row, col = t.start
            if t.type == tokenize.OP and t.string in ("==", "!="):
                if (nxt and nxt.string == "None") or (prev and prev.string == "None"):
                    found.append((row, col + 1, "E711 comparison to None should be 'if cond is None:'"
                                  if t.string == "==" else "E711 comparison to None should be 'if cond is not None:'"))
            if t.type == tokenize.NAME and t.string == "except" and nxt and nxt.string == ":":
                found.append((row, col + 1, "E722 do not use bare 'except'"))
            if (t.type == tokenize.NAME and t.string == "print" and nxt and nxt.string == "("
                    and not (prev and prev.string in (".", "def"))):
                found.append((row, col + 1, "T201 print found"))
            if t.type == tokenize.FSTRING_START:
                fstack.append([t, False])
            elif t.type == tokenize.OP and t.string == "{" and fstack:
                fstack[-1][1] = True
            elif t.type == tokenize.FSTRING_END:
                start, used = fstack.pop()
                if not used:
                    found.append((start.start[0], start.start[1] + 1, "F541 f-string is missing placeholders"))
            if t.type == tokenize.COMMENT:
                before = lines[row - 1][:col]
                if before.strip():
                    if len(before) - len(before.rstrip()) < 2:
                        found.append((row, col + 1, "E261 at least two spaces before inline comment"))
                    if not t.string.startswith("# "):
                        found.append((row, col + 1, "E262 inline comment should start with '# '"))
        for row, col, msg in sorted(found):
            print("%s:%d:%d: %s" % (path, row, col, msg))
        if err:
            print("%s:%d:%d: E902 %s: %s" % (path, err[2], err[3], err[0], err[1]))


# Renames a function: every NAME token spelled `old` that is not an
# attribute, in every file, shown as the lines that change.
def rename(paths, old, new):
    print("== rename %s -> %s" % (old, new))
    for path in paths:
        toks, err = file_tokens(path)
        lines = source_text(path).splitlines()
        edits = {}
        sig = [t for t in toks if t.type not in SKIP]
        for i, t in enumerate(sig):
            if t.type == tokenize.NAME and t.string == old and not (i > 0 and sig[i - 1].string == "."):
                edits.setdefault(t.start[0], []).append(t.start[1])
        for row in sorted(edits):
            line = lines[row - 1]
            for col in sorted(edits[row], reverse=True):
                line = line[:col] + new + line[col + len(old):]
            print("%s:%d: -%s" % (path, row, lines[row - 1]))
            print("%s:%d: +%s" % (path, row, line))


# Drops the comments from a file: a line that held only a comment goes,
# and a line with code keeps the code, without the spaces before the
# comment.
def strip_comments(path):
    print("== strip comments " + path)
    toks, err = file_tokens(path)
    lines = source_text(path).splitlines()
    cut = {}
    has_code = set()
    for t in toks:
        if t.type == tokenize.COMMENT:
            cut[t.start[0]] = t.start[1]
        elif t.type not in SKIP:
            for row in range(t.start[0], t.end[0] + 1):
                has_code.add(row)
    for n, line in enumerate(lines, 1):
        if n in cut:
            if n not in has_code:
                continue
            line = line[:cut[n]].rstrip()
        print("| " + line)


run_jobs()
files = project_files()
for path in files:
    dump(path)
for path in broken_files():
    dump(path)
stats(files + broken_files())
todos(files)
lint(files)
rename(files, "fetch_rows", "load_rows")
strip_comments("data/project/inventory/report.py")
