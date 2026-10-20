# Runs data/jobs.tsv through unidiff 0.7.5 (the unidiff/ package next to
# this file, unchanged) and prints what it did. mini_unidiff.kara must
# print the same bytes.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from unidiff import PatchSet  # noqa: E402
from unidiff.constants import LINE_TYPE_NO_NEWLINE  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s)


def path_of(rel):
    return os.path.join(HERE, "data", rel)


def read(rel):
    with open(path_of(rel), encoding="utf-8", newline="") as f:
        return f.read()


def read_or_none(rel):
    if not os.path.exists(path_of(rel)):
        return None
    return read(rel)


def esc(s):
    return s.replace("\\", "\\\\").replace("\r", "\\r").replace("\t", "\\t").replace("\n", "\\n")


def err(e):
    return "error: %s: %s" % (type(e).__name__, esc(str(e)))


def load(rel, mode):
    if mode == "file":
        return PatchSet.from_filename(path_of(rel))
    if mode == "meta":
        return PatchSet(read(rel), metadata_only=True)
    return PatchSet.from_string(read(rel))


def paths(files):
    return "[" + ", ".join(repr(f.path) for f in files) + "]"


# ------------------------------------------------------------- parse

def dump(ps, text):
    emit("files: %d added: %d removed: %d" % (len(ps), ps.added, ps.removed))
    emit("added_files: %s" % paths(ps.added_files))
    emit("removed_files: %s" % paths(ps.removed_files))
    emit("modified_files: %s" % paths(ps.modified_files))
    for f in ps:
        emit("%r" % f)
        emit("  source=%r target=%r" % (f.source_file, f.target_file))
        emit("  source_timestamp=%r target_timestamp=%r" % (f.source_timestamp, f.target_timestamp))
        emit("  binary=%s rename=%s added_file=%s removed_file=%s modified_file=%s +%d -%d"
             % (f.is_binary_file, f.is_rename, f.is_added_file, f.is_removed_file, f.is_modified_file,
                f.added, f.removed))
        if f.patch_info is None:
            emit("  info: None")
        else:
            emit("  info: %r, %d lines" % (f.patch_info, len(f.patch_info)))
            for line in f.patch_info:
                emit("  | " + esc(line))
        for h in f:
            emit("  %r" % h)
            emit("    section=%r added=%d removed=%d valid=%s lines=%d"
                 % (h.section_header, h.added, h.removed, h.is_valid(), len(h)))
            for line in h:
                emit("    %r %r src=%s tgt=%s diff=%s"
                     % (line.line_type, line.value, line.source_line_no, line.target_line_no, line.diff_line_no))
    s = str(ps)
    if s == text:
        emit("str: same")
    else:
        emit("str: differs")
        for line in s.splitlines(keepends=True):
            emit("  > " + esc(line))


def parse_job(rel, mode):
    text = read(rel)
    if mode == "file":
        text = text.replace("\r\n", "\n").replace("\r", "\n")
    ps = load(rel, mode)
    dump(ps, text)


# --------------------------------------------------------------- stat

def stat_job(rel):
    ps = PatchSet.from_string(read(rel))
    width = 40
    most = max([f.added + f.removed for f in ps] + [0])
    name_w = max([len(f.path) for f in ps] + [0])
    for f in ps:
        n = f.added + f.removed
        if f.is_binary_file:
            emit(" %s | Bin" % f.path.ljust(name_w))
            continue
        plus, minus = f.added, f.removed
        if most > width:
            plus = (f.added * width + most - 1) // most if f.added else 0
            minus = (f.removed * width + most - 1) // most if f.removed else 0
        emit(" %s | %4d %s%s" % (f.path.ljust(name_w), n, "+" * plus, "-" * minus))
    files = len(ps)
    emit(" %d file%s changed, %d insertion%s(+), %d deletion%s(-)"
         % (files, "" if files == 1 else "s", ps.added, "" if ps.added == 1 else "s",
            ps.removed, "" if ps.removed == 1 else "s"))


# -------------------------------------------------------------- apply

def strip_prefix(name, p):
    return name[2:] if name.startswith(p) else name


def apply_file(f, orig, reverse):
    lines = orig.splitlines(keepends=True)
    out = []
    pos = 0
    for n, h in enumerate(f, 1):
        start, length = (h.target_start, h.target_length) if reverse else (h.source_start, h.source_length)
        at = start - 1 if length > 0 else start
        if at < pos or at > len(lines):
            return None, "hunk #%d FAILED at %d" % (n, start)
        out.extend(lines[pos:at])
        pos = at
        body = list(h)
        for i, line in enumerate(body):
            kind = line.line_type
            if kind == LINE_TYPE_NO_NEWLINE or kind == "":
                continue
            if reverse and kind == "+":
                kind = "-"
            elif reverse and kind == "-":
                kind = "+"
            value = line.value
            if i + 1 < len(body) and body[i + 1].line_type == LINE_TYPE_NO_NEWLINE and value.endswith("\n"):
                value = value[:-1]
            if kind == "+":
                out.append(value)
                continue
            if pos >= len(lines) or lines[pos] != value:
                return None, "hunk #%d FAILED at %d" % (n, start)
            pos += 1
            if kind == " ":
                out.append(value)
    out.extend(lines[pos:])
    return "".join(out), None


def apply_job(rel, base, want, reverse):
    ps = PatchSet.from_string(read(rel))
    ok = 0
    for f in ps:
        src = strip_prefix(f.source_file, "a/")
        dst = strip_prefix(f.target_file, "b/")
        if reverse:
            src, dst = dst, src
        if f.is_binary_file:
            emit("%s: binary, skipped" % f.path)
            continue
        orig = read_or_none(base + "/" + src) if src != "/dev/null" else ""
        if orig is None:
            emit("%s: %s is missing" % (f.path, src))
            continue
        result, fail = apply_file(f, orig, reverse)
        if fail is not None:
            emit("%s: %s" % (f.path, fail))
            continue
        expect = read_or_none(want + "/" + dst) if dst != "/dev/null" else None
        if dst == "/dev/null":
            emit("%s: deleted, %s" % (f.path, "empty" if result == "" else "NOT EMPTY"))
            ok += 1 if result == "" else 0
            continue
        same = result == expect
        ok += 1 if same else 0
        emit("%s -> %s: %d lines, %s" % (f.path, dst, len(result.splitlines()),
                                         "matches" if same else "DIFFERS"))
    emit("%d of %d files ok" % (ok, len(ps)))


# ----------------------------------------------------------- position

def position_job(rel, comments):
    ps = PatchSet.from_string(read(rel))
    for c in read(comments).splitlines():
        name, no = c.split("\t")
        no = int(no)
        found = [f for f in ps if f.path == name]
        if not found:
            emit("%s:%d: file not in diff" % (name, no))
            continue
        f = found[0]
        pos = 0
        hit = None
        for k, h in enumerate(f):
            if k > 0:
                pos += 1
            for line in h:
                pos += 1
                if hit is None and line.target_line_no == no and line.line_type in ("+", " "):
                    hit = (pos, line)
        if hit is None:
            emit("%s:%d: outside the diff" % (name, no))
        else:
            pos, line = hit
            emit("%s:%d: position %d, %s, diff line %d"
                 % (name, no, pos, "added" if line.is_added else "context", line.diff_line_no))


# --------------------------------------------------------------- scan

def scan_job(rel, rules):
    ps = PatchSet.from_string(read(rel))
    words = read(rules).splitlines()
    hits = 0
    for f in ps:
        for h in f:
            for line in h:
                if not line.is_added:
                    continue
                for w in words:
                    if w in line.value:
                        hits += 1
                        emit("%s:%d: %s: %s" % (f.path, line.target_line_no, w, esc(line.value.strip())))
    emit("%d findings" % hits)


def main():
    for line in read("jobs.tsv").splitlines():
        job = line.split("\t")
        emit("== " + " ".join(job))
        try:
            if job[0] == "parse":
                parse_job(job[1], job[2])
            elif job[0] == "stat":
                stat_job(job[1])
            elif job[0] == "apply":
                apply_job(job[1], job[2], job[3], False)
            elif job[0] == "revert":
                apply_job(job[1], job[2], job[3], True)
            elif job[0] == "position":
                position_job(job[1], job[2])
            else:
                scan_job(job[1], job[2])
        except Exception as e:
            # A parse error, or a property of a file the parser left
            # half-built (a binary file with no target).
            emit(err(e))
    sys.stdout.write("\n".join(OUT) + "\n")


main()
