# Writes data/: command traces that drive intervaltree's IntervalTree and
# Interval through their whole API, the inputs of four programs built on
# interval trees (a genome annotation lookup, a meeting-room calendar, an
# IP allowlist and a subtitle timeline), and data/jobs.tsv, the jobs
# mini_intervaltree.kara and oracle.py run.
#
# A trace line is a command and its arguments. An interval is written
# begin:end or begin:end:data, where data is text, or #n for an int, or
# _ for None.
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


TAGS = ["a", "b", "c", "x", "#1", "#2", "_", "_"]


def iv(r, lo, hi, null_ok=False):
    b = r.randint(lo, hi)
    e = b + r.randint(0 if null_ok and r.random() < 0.05 else 1, 25)
    t = r.choice(TAGS)
    return "%d:%d" % (b, e) if t == "_" and r.random() < 0.5 else "%d:%d:%s" % (b, e, t)


def ivs(r, k, lo, hi):
    return " ".join(iv(r, lo, hi) for _ in range(k))


# The corners of Interval that a random trace rarely reaches.
EDGES = [
    "iv overlap_size 5:10:a 7",
    "iv overlap_size 5:10:a 12",
    "iv lt 5:5 7",
    "iv ge 3:9 4:4:x",
    "iv le 3:9 4:4:x",
    "iv gt 3:9 9",
    "iv gt 3:9 2:3",
    "iv distance_to 3:9 12",
    "iv distance_to 3:9 1",
    "iv distance_to 3:9 5",
    "iv < 3:9 3",
    "iv > 3:9 3",
    "iv == 3:9:a 3:9:#1",
    "iv < 3:9:a 3:9:#1",
    "iv > 3:9:a 3:9:#1",
    "iv < 3:9 3:9:a",
    "iv < 3:9:b 3:9:a",
    "iv < 3:9:#2 3:9:#10",
    "iv repr 3:9:a",
    "iv repr -4:-1:#7",
    "iv length 9:3",
    "add 4:4",
    "add 4:2:a",
    "add 1:5:a",
    "add 1:5:a",
    "add 1:5:#1",
    "add 1:5",
    "remove 1:5:b",
    "len",
    "at 1",
    "at 5",
    "remove 1:5:#1",
    "discard 1:5:#1",
    "remove 1:5:#1",
    "span",
    "range",
    "clear",
    "begin",
    "end",
    "span",
    "range",
    "at 3",
    "overlap 1 2",
    "overlaps 3",
    "overlaps 3 1",
    "remove 0:1",
    "split_overlaps",
    "merge 1",
    "repr",
    "verify",
]


def tree_trace(seed, ops, span):
    r = random.Random(seed)
    out = list(EDGES) if seed == 1 else []
    added = []
    for i in range(ops):
        if i % 30 == 29:
            out.append("verify")
            out.append("repr")
            continue
        c = r.random()
        p = str(r.randint(-5, span + 5))
        b = r.randint(-5, span + 5)
        e = b + r.randint(-2, 30)
        if c < 0.22:
            x = iv(r, 0, span, True)
            added.append(x)
            out.append("add " + x)
        elif c < 0.25:
            out.append("set %d %d %s" % (b, e, r.choice(TAGS)))
        elif c < 0.28:
            out.append("update " + ivs(r, r.randint(1, 6), 0, span))
        elif c < 0.32:
            x = r.choice(added) if added and r.random() < 0.7 else iv(r, 0, span)
            out.append(r.choice(["remove ", "discard "]) + x)
        elif c < 0.36:
            out.append("at " + p)
        elif c < 0.40:
            out.append("overlap %d %d" % (b, e))
        elif c < 0.43:
            out.append("envelop %d %d" % (b, e))
        elif c < 0.46:
            out.append("overlaps " + p if r.random() < 0.5 else "overlaps %d %d" % (b, e))
        elif c < 0.48:
            x = r.choice(added) if added and r.random() < 0.6 else iv(r, 0, span)
            out.append("contains " + x)
        elif c < 0.51:
            out.append("get " + r.choice(["%d %d" % (b, e), "_ %d" % e, "%d _" % b, "_ _"]))
        elif c < 0.53:
            out.append("del " + p)
        elif c < 0.55:
            out.append("remove_overlap " + (p if r.random() < 0.4 else "%d %d" % (b, e)))
        elif c < 0.57:
            out.append("remove_envelop %d %d" % (b, e))
        elif c < 0.60:
            out.append(r.choice(["chop ", "chopf "]) + "%d %d" % (b, max(b + 1, e)))
        elif c < 0.63:
            out.append(r.choice(["slice ", "slicef "]) + p)
        elif c < 0.645:
            out.append("split_overlaps")
        elif c < 0.66:
            out.append(r.choice(["merge 1", "merge 0", "merge_join 1", "merge_join 0", "merge_count 0", "merge_count 1"]))
        elif c < 0.67:
            out.append(r.choice(["merge_equals", "merge_equals_join", "merge_equals_count"]))
        elif c < 0.69:
            out.append("len")
        elif c < 0.72:
            out.append(r.choice(["begin", "end", "span", "range", "len", "is_empty"]))
        elif c < 0.78:
            op = r.choice(["union", "intersection", "difference", "symmetric_difference",
                           "difference_update", "intersection_update", "symmetric_difference_update", "eq"])
            pool = added[-8:]
            mine = [x for x in pool if r.random() < 0.6]
            out.append(op + " " + " ".join(mine + [iv(r, 0, span) for _ in range(r.randint(0, 3))]))
        elif c < 0.79:
            out.append("copy")
        elif c < 0.795:
            out.append("clear")
            added = []
        elif c < 0.80:
            out.append("from_tuples " + ivs(r, r.randint(0, 12), 0, span))
        else:
            a = iv(r, 0, 40, True)
            x = iv(r, 0, 40, True) if r.random() < 0.7 else str(r.randint(-2, 70))
            op = r.choice(["overlaps", "overlap_size", "contains_point", "contains_interval", "range_matches",
                           "distance_to", "length", "is_null", "lt", "le", "gt", "ge", "<", ">", "==", "repr"])
            if op == "contains_point":
                x = str(r.randint(-2, 70))
            if op in ("contains_interval", "range_matches", "=="):
                x = iv(r, 0, 40, True)
            out.append("iv %s %s %s" % (op, a, x))
    out += ["verify", "repr", "items"]
    return "\n".join(out) + "\n"


def genes():
    r = random.Random(21)
    lines = []
    for chrom in ["chr1", "chr2", "chrX"]:
        pos = 1000
        for g in range(40):
            pos += r.randint(-3000, 9000)
            pos = max(pos, 100)
            length = r.randint(500, 12000)
            name = "%s%s%d" % (r.choice(["BRC", "TP", "MYC", "KRA", "EGF", "PTE", "APO", "CDK"]), chrom[-1], g)
            strand = r.choice("+-")
            lines.append("%s\t%d\t%d\t%s\t%s" % (chrom, pos, pos + length, name, strand))
    return "\n".join(lines) + "\n"


def variants():
    r = random.Random(22)
    lines = []
    for i in range(90):
        chrom = r.choice(["chr1", "chr2", "chrX", "chr3"])
        ref = r.choice("ACGT")
        alt = r.choice([b for b in "ACGT" if b != ref])
        lines.append("%s\t%d\trs%d\t%s>%s" % (chrom, r.randint(500, 200000), 1000 + i, ref, alt))
    return "\n".join(lines) + "\n"


def reads():
    r = random.Random(23)
    lines = []
    for i in range(60):
        chrom = r.choice(["chr1", "chr2", "chrX"])
        s = r.randint(500, 200000)
        lines.append("%s\t%d\t%d\tread%d" % (chrom, s, s + r.choice([150, 150, 300, 2000, 9000]), i))
    return "\n".join(lines) + "\n"


def meetings():
    r = random.Random(24)
    lines = []
    for day in ["mon", "tue", "wed"]:
        for k in range(18):
            room = r.choice(["atlas", "boreal"])
            s = r.randrange(480, 1080, 15)
            lines.append("%s %s %d %d %s" % (day, room, s, s + r.choice([15, 30, 45, 60, 90, 120]),
                                             r.choice(["standup", "review", "1on1", "planning", "interview", "sync"])))
        lines.append("block %s 720 780 lunch" % day)
        lines.append("cancel %s %d" % (day, r.randrange(480, 1080, 15)))
        lines.append("free %s %d" % (day, r.choice([30, 60])))
    return "\n".join(lines) + "\n"


def ip(n):
    return "%d.%d.%d.%d" % (n >> 24, (n >> 16) & 255, (n >> 8) & 255, n & 255)


def allowlist():
    r = random.Random(25)
    lines = []
    for i in range(30):
        base = r.choice([10 << 24, (172 << 24) | (16 << 16), (192 << 24) | (168 << 16), (203 << 24) | (113 << 8)])
        size = r.choice([16, 20, 24, 24, 28, 30, 32])
        block = 1 << (32 - size)
        start = base + r.randint(0, max(0, (1 << 14) // block)) * block if block < (1 << 14) else base
        start &= ~(block - 1)
        lines.append("allow %s/%d %s" % (ip(start), size, r.choice(["office", "vpn", "partner", "ci", "lab"])))
    for i in range(6):
        lines.append("deny %s/%d" % (ip((10 << 24) + r.randint(0, 255) * 256), r.choice([24, 28])))
    for i in range(50):
        base = r.choice([10 << 24, (172 << 24) | (16 << 16), (192 << 24) | (168 << 16), (8 << 24)])
        lines.append("check %s" % ip(base + r.randint(0, 1 << 14)))
    return "\n".join(lines) + "\n"


def subtitles():
    r = random.Random(26)
    lines = []
    t = 0
    for i in range(1, 61):
        t += r.randint(200, 3500)
        length = r.randint(800, 5000)
        lines.append("%d\t%d\t%d\t%s" % (i, t, t + length, r.choice(["Hello.", "Where were you?", "[music]", "Run!",
                                                                    "I told you.", "[door slams]", "No.", "Look out!"])))
    lines.append("cut 30000")
    lines.append("cut 61000")
    return "\n".join(lines) + "\n"


def main():
    write("traces/small.txt", tree_trace(1, 900, 40))
    write("traces/wide.txt", tree_trace(2, 900, 400))
    write("traces/dense.txt", tree_trace(3, 600, 12))
    write("genes.tsv", genes())
    write("variants.tsv", variants())
    write("reads.tsv", reads())
    write("meetings.txt", meetings())
    write("allowlist.txt", allowlist())
    write("subtitles.tsv", subtitles())
    jobs = [
        "trace\ttraces/small.txt",
        "trace\ttraces/wide.txt",
        "trace\ttraces/dense.txt",
        "genome\tgenes.tsv\tvariants.tsv\treads.tsv",
        "calendar\tmeetings.txt",
        "allowlist\tallowlist.txt",
        "subtitles\tsubtitles.tsv",
    ]
    write("jobs.tsv", "\n".join(jobs) + "\n")


if __name__ == "__main__":
    main()
