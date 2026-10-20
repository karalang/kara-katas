# Runs data/jobs.tsv through intervaltree 3.1.0 (the intervaltree/
# package next to this file, unchanged, on the sortedcontainers 2.4.0
# copy beside it) and prints what it did. mini_intervaltree.kara must
# print the same bytes.
#
# An IntervalTree is a set, and a set's order is its hash table's, so
# every set of intervals is printed sorted, as the tree's own repr does.
# The tree's shape (print_structure, score) depends on that order too,
# and is not printed; nor is find_nested on intervals with the same
# range, which it tells apart by the set's order.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from intervaltree import Interval, IntervalTree  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s)


def read(rel):
    with open(os.path.join(HERE, "data", rel), encoding="utf-8") as f:
        return f.read()


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def data_of(s):
    if s == "_":
        return None
    if s.startswith("#"):
        return int(s[1:])
    return s


def iv_of(tok):
    f = tok.split(":")
    return Interval(int(f[0]), int(f[1]), data_of(f[2]) if len(f) > 2 else None)


def num_or_iv(tok):
    return iv_of(tok) if ":" in tok else int(tok)


def arg(s):
    return None if s == "_" else int(s)


def ivlist(xs):
    return repr(sorted(xs))


def datafunc(iv, islower):
    return "%s%s" % (iv.data, "<" if islower else ">")


def join(a, b):
    return "%s+%s" % (a, b)


def count(a, b):
    return a + 1


def iv_cmd(op, a, b):
    if op == "overlaps":
        return a.overlaps(b)
    if op == "overlap_size":
        return a.overlap_size(b)
    if op == "contains_point":
        return a.contains_point(b)
    if op == "contains_interval":
        return a.contains_interval(b)
    if op == "range_matches":
        return a.range_matches(b)
    if op == "distance_to":
        return a.distance_to(b)
    if op == "length":
        return a.length()
    if op == "is_null":
        return a.is_null()
    if op == "lt":
        return a.lt(b)
    if op == "le":
        return a.le(b)
    if op == "gt":
        return a.gt(b)
    if op == "ge":
        return a.ge(b)
    if op == "<":
        return a < b
    if op == ">":
        return a > b
    if op == "==":
        return a == b
    return repr(a)


def tree_cmd(t, c, a):
    if c == "add":
        return t.add(iv_of(a[0]))
    if c == "set":
        t[int(a[0]):int(a[1])] = data_of(a[2])
        return None
    if c == "update":
        return t.update([iv_of(x) for x in a])
    if c == "remove":
        return t.remove(iv_of(a[0]))
    if c == "discard":
        return t.discard(iv_of(a[0]))
    if c == "at":
        return ivlist(t.at(int(a[0])))
    if c == "overlap":
        return ivlist(t.overlap(int(a[0]), int(a[1])))
    if c == "envelop":
        return ivlist(t.envelop(int(a[0]), int(a[1])))
    if c == "overlaps":
        return t.overlaps(int(a[0])) if len(a) == 1 else t.overlaps(int(a[0]), int(a[1]))
    if c == "contains":
        return iv_of(a[0]) in t
    if c == "get":
        return ivlist(t[arg(a[0]):arg(a[1])])
    if c == "del":
        del t[int(a[0])]
        return None
    if c == "remove_overlap":
        return t.remove_overlap(int(a[0])) if len(a) == 1 else t.remove_overlap(int(a[0]), int(a[1]))
    if c == "remove_envelop":
        return t.remove_envelop(int(a[0]), int(a[1]))
    if c == "chop":
        return t.chop(int(a[0]), int(a[1]))
    if c == "chopf":
        return t.chop(int(a[0]), int(a[1]), datafunc)
    if c == "slice":
        return t.slice(int(a[0]))
    if c == "slicef":
        return t.slice(int(a[0]), datafunc)
    if c == "split_overlaps":
        return t.split_overlaps()
    if c == "merge":
        return t.merge_overlaps(strict=a[0] == "1")
    if c == "merge_join":
        return t.merge_overlaps(join, strict=a[0] == "1")
    if c == "merge_count":
        return t.merge_overlaps(count, 0, strict=a[0] == "1")
    if c == "merge_equals":
        return t.merge_equals()
    if c == "merge_equals_join":
        return t.merge_equals(join)
    if c == "merge_equals_count":
        return t.merge_equals(count, 0)
    if c == "begin":
        return t.begin()
    if c == "end":
        return t.end()
    if c == "span":
        return t.span()
    if c == "range":
        return t.range()
    if c == "len":
        return len(t)
    if c == "is_empty":
        return t.is_empty()
    other = [iv_of(x) for x in a]
    if c == "union":
        return t.union(other)
    if c == "intersection":
        return t.intersection(other)
    if c == "difference":
        return t.difference(other)
    if c == "symmetric_difference":
        return t.symmetric_difference(other)
    if c == "difference_update":
        return t.difference_update(other)
    if c == "intersection_update":
        return t.intersection_update(other)
    if c == "symmetric_difference_update":
        return t.symmetric_difference_update(other)
    if c == "eq":
        return t == IntervalTree(other)
    if c == "copy":
        u = t.copy()
        return "%s %r" % (u == t, u)
    if c == "clear":
        return t.clear()
    if c == "from_tuples":
        return IntervalTree.from_tuples([(x.begin, x.end, x.data) for x in other])
    raise AssertionError(c)


def trace_job(rel):
    t = IntervalTree()
    for line in read(rel).splitlines():
        f = line.split()
        c, a = f[0], f[1:]
        if c == "verify":
            t.verify()
            emit("verify: ok")
            continue
        if c == "repr":
            emit("repr: %r" % t)
            continue
        if c == "items":
            emit("items: " + ivlist(t.items()))
            continue
        try:
            if c == "iv":
                r = iv_cmd(a[0], iv_of(a[1]), num_or_iv(a[2]) if len(a) > 2 else None)
            else:
                r = tree_cmd(t, c, a)
        except Exception as e:
            emit("%s: %s" % (line, err(e)))
            continue
        emit("%s: %s" % (line, r if isinstance(r, str) else repr(r)))


# ---------------------------------------------------------------- genome

def names(xs):
    return " ".join(iv.data for iv in sorted(xs)) or "-"


def genome_job(genes_rel, variants_rel, reads_rel):
    by_chrom = {}
    for line in read(genes_rel).splitlines():
        chrom, s, e, name, strand = line.split("\t")
        by_chrom.setdefault(chrom, []).append(Interval(int(s), int(e), "%s(%s)" % (name, strand)))
    trees = {}
    for chrom in sorted(by_chrom):
        t = IntervalTree(by_chrom[chrom])
        trees[chrom] = t
        t.verify()
        emit("%s: %d genes, %d..%d, span %d" % (chrom, len(t), t.begin(), t.end(), t.span()))
        cover = t.copy()
        cover.merge_overlaps(count, 0, strict=False)
        total = sum(iv.length() for iv in cover)
        multi = sorted(iv for iv in cover if iv.data > 1)
        emit("  covered %d bp in %d blocks; blocks of 2 or more genes: %s" % (
            total, len(cover), " ".join("%d-%d(%d)" % (iv.begin, iv.end, iv.data) for iv in multi[:6]) or "-"))
        found = t.find_nested()
        for parent in sorted(found)[:5]:
            emit("  inside %s: %s" % (parent.data, names(found[parent])))
    for line in read(variants_rel).splitlines():
        chrom, pos, rsid, change = line.split("\t")
        pos = int(pos)
        t = trees.get(chrom)
        if t is None:
            emit("%s %s:%d %s: no annotation for %s" % (rsid, chrom, pos, change, chrom))
            continue
        hits = t[pos]
        if hits:
            emit("%s %s:%d %s: in %s" % (rsid, chrom, pos, change, names(hits)))
        else:
            near = sorted((iv.distance_to(pos), iv) for iv in t)[0]
            emit("%s %s:%d %s: intergenic, nearest %s at %d bp" % (rsid, chrom, pos, change, near[1].data, near[0]))
    for line in read(reads_rel).splitlines():
        chrom, s, e, name = line.split("\t")
        t = trees[chrom]
        s, e = int(s), int(e)
        over = t.overlap(s, e)
        emit("%s %s:%d-%d: overlaps %s; contains %s" % (name, chrom, s, e, names(over), names(t.envelop(s, e))))


# -------------------------------------------------------------- calendar

def hm(m):
    return "%02d:%02d" % (m // 60, m % 60)


def part(iv, islower):
    return "%s (%s)" % (iv.data, "before" if islower else "after")


def calendar_job(rel):
    days = {}
    for line in read(rel).splitlines():
        f = line.split()
        if f[0] in ("block", "cancel", "free"):
            rooms = days.setdefault(f[1], {"atlas": IntervalTree(), "boreal": IntervalTree()})
        if f[0] == "block":
            s, e = int(f[2]), int(f[3])
            for room in sorted(rooms):
                t = rooms[room]
                hit = t.overlap(s, e)
                t.chop(s, e, part)
                emit("block %s %s %s-%s %s: moved %d, now %s" % (f[1], room, hm(s), hm(e), f[4], len(hit),
                                                              ", ".join("%s-%s %s" % (hm(iv.begin), hm(iv.end), iv.data) for iv in sorted(t.overlap(s - 60, e + 60))) or "-"))
        elif f[0] == "cancel":
            s = int(f[2])
            for room in sorted(rooms):
                t = rooms[room]
                hit = sorted(t.at(s))
                del t[s]
                emit("cancel %s %s %s: %s" % (f[1], room, hm(s), ", ".join("%s-%s %s" % (hm(iv.begin), hm(iv.end), iv.data) for iv in hit) or "nothing"))
        elif f[0] == "free":
            need = int(f[2])
            busy = rooms["atlas"].union(rooms["boreal"])
            busy.merge_overlaps(strict=False)
            gaps = []
            t = 480
            for iv in sorted(busy):
                if iv.begin - t >= need:
                    gaps.append("%s-%s" % (hm(t), hm(iv.begin)))
                t = max(t, iv.end)
            if 1080 - t >= need:
                gaps.append("%s-%s" % (hm(t), hm(1080)))
            emit("free %s %d min in both rooms: %s" % (f[1], need, " ".join(gaps) or "none"))
        else:
            day, room, s, e, what = f[0], f[1], int(f[2]), int(f[3]), f[4]
            rooms = days.setdefault(day, {"atlas": IntervalTree(), "boreal": IntervalTree()})
            t = rooms[room]
            if t.overlaps(s, e):
                emit("%s %s %s-%s %s: clashes with %s" % (day, room, hm(s), hm(e), what,
                                                          ", ".join("%s-%s %s" % (hm(iv.begin), hm(iv.end), iv.data) for iv in sorted(t[s:e]))))
            else:
                t.addi(s, e, what)
                emit("%s %s %s-%s %s: booked" % (day, room, hm(s), hm(e), what))
    for day in sorted(days):
        for room in sorted(days[day]):
            t = days[day][room]
            t.verify()
            emit("agenda %s %s (%d)" % (day, room, len(t)))
            for iv in sorted(t):
                emit("  %s-%s %s" % (hm(iv.begin), hm(iv.end), iv.data))


# ------------------------------------------------------------- allowlist

def ip_num(s):
    a, b, c, d = (int(x) for x in s.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def ip_str(n):
    return "%d.%d.%d.%d" % (n >> 24, (n >> 16) & 255, (n >> 8) & 255, n & 255)


def cidr(s):
    addr, size = s.split("/")
    start = ip_num(addr)
    return start, start + (1 << (32 - int(size)))


def span_str(iv):
    return "%s-%s" % (ip_str(iv.begin), ip_str(iv.end - 1))


def allowlist_job(rel):
    t = IntervalTree()
    for line in read(rel).splitlines():
        f = line.split()
        if f[0] == "allow":
            s, e = cidr(f[1])
            t.addi(s, e, f[2])
        elif f[0] == "deny":
            s, e = cidr(f[1])
            cut = sorted(t.overlap(s, e))
            t.chop(s, e)
            emit("deny %s: cut %s" % (f[1], ", ".join("%s %s" % (span_str(iv), iv.data) for iv in cut) or "nothing"))
        else:
            n = ip_num(f[1])
            hit = sorted(t[n])
            if hit:
                emit("check %s: allowed by %s" % (f[1], ", ".join("%s %s" % (span_str(iv), iv.data) for iv in hit)))
            else:
                emit("check %s: refused" % f[1])
    t.verify()
    emit("ranges: %d, %s to %s" % (len(t), ip_str(t.begin()), ip_str(t.end() - 1)))
    flat = t.copy()
    flat.split_overlaps()
    flat.merge_equals(join)
    emit("disjoint ranges: %d" % len(flat))
    for iv in sorted(flat):
        emit("  %s %s" % (span_str(iv), iv.data))


# ------------------------------------------------------------- subtitles

def ts(ms):
    return "%02d:%02d.%03d" % (ms // 60000, ms // 1000 % 60, ms % 1000)


def cue_part(iv, islower):
    return iv.data + (" [a]" if islower else " [b]")


def subtitles_job(rel):
    t = IntervalTree()
    for line in read(rel).splitlines():
        f = line.split("\t")
        if line.startswith("cut "):
            p = int(line.split()[1])
            hit = sorted(t.at(p))
            t.slice(p, cue_part)
            emit("cut at %s splits %s" % (ts(p), ", ".join(iv.data for iv in hit) or "nothing"))
            continue
        t.addi(int(f[1]), int(f[2]), "%s %s" % (f[0], f[3]))
    t.verify()
    emit("cues: %d, %s to %s" % (len(t), ts(t.begin()), ts(t.end())))
    stacked = t.copy()
    stacked.split_overlaps()
    stacked.merge_equals(join)
    shown = 0
    for iv in sorted(stacked):
        if "+" in iv.data:
            shown += 1
            if shown <= 12:
                emit("  %s-%s stacked: %s" % (ts(iv.begin), ts(iv.end), iv.data))
    emit("stacked stretches: %d" % shown)
    single = t.copy()
    single.merge_overlaps(count, 0)
    emit("on-screen blocks: %d, longest %s" % (len(single), max((iv.length(), iv) for iv in single)[1].length()))


def main():
    for line in read("jobs.tsv").splitlines():
        job = line.split("\t")
        emit("== " + " ".join(job))
        if job[0] == "trace":
            trace_job(job[1])
        elif job[0] == "genome":
            genome_job(job[1], job[2], job[3])
        elif job[0] == "calendar":
            calendar_job(job[1])
        elif job[0] == "allowlist":
            allowlist_job(job[1])
        else:
            subtitles_job(job[1])
    sys.stdout.write("".join(s + "\n" for s in OUT))


if __name__ == "__main__":
    main()
