# Runs data/jobs.tsv through jellyfish 0.11.2's pure-Python
# implementation (jellyfish/_jellyfish.py next to this file, unchanged)
# and prints what it did. mini_jellyfish.kara must print the same bytes.
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "jellyfish"))

import _jellyfish as jf  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s)


def read(rel):
    with open(os.path.join(HERE, "data", rel), encoding="utf-8") as f:
        return f.read()


def rows(rel):
    with open(os.path.join(HERE, "data", rel), encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


# ------------------------------------------------------------ vectors

ONE = {
    "soundex": jf.soundex,
    "metaphone": jf.metaphone,
    "nysiis": jf.nysiis,
    "match_rating_codex": jf.match_rating_codex,
}
TWO = {
    "levenshtein": jf.levenshtein_distance,
    "wagner_fischer": jf.levenshtein_distance,
    "damerau_levenshtein": jf.damerau_levenshtein_distance,
    "hamming": jf.hamming_distance,
    "jaro_distance": jf.jaro_similarity,
    "jaro_winkler": jf.jaro_winkler_similarity,
    "jaro_winkler_longtol": lambda a, b: jf.jaro_winkler_similarity(a, b, True),
    "match_rating_comparison": jf.match_rating_comparison,
}


def vectors_job(rel):
    name = os.path.basename(rel)[:-4]
    for row in rows(rel):
        if name in ONE:
            got = ONE[name](row[0])
            emit("%s(%r) = %r, expected %r" % (name, row[0], got, row[1]))
        else:
            got = TWO[name](row[0], row[1])
            emit("%s(%r, %r) = %r, expected %r" % (name, row[0], row[1], got, row[2]))


# ------------------------------------------------------ encode, compare

def encode_job(rel):
    for name in read(rel).splitlines():
        emit("%r: soundex=%r metaphone=%r nysiis=%r mrc=%r" % (
            name, jf.soundex(name), jf.metaphone(name), jf.nysiis(name), jf.match_rating_codex(name)))


def compare_job(rel):
    for line in read(rel).splitlines():
        a, b = line.split("\t")
        emit("%r %r" % (a, b))
        emit("  levenshtein=%d damerau=%d hamming=%d" % (
            jf.levenshtein_distance(a, b), jf.damerau_levenshtein_distance(a, b), jf.hamming_distance(a, b)))
        emit("  jaro=%r jaro_winkler=%r long=%r" % (
            jf.jaro_similarity(a, b), jf.jaro_winkler_similarity(a, b), jf.jaro_winkler_similarity(a, b, True)))
        emit("  mra=%r same_soundex=%r same_metaphone=%r same_nysiis=%r" % (
            jf.match_rating_comparison(a, b), jf.soundex(a) == jf.soundex(b),
            jf.metaphone(a) == jf.metaphone(b), jf.nysiis(a) == jf.nysiis(b)))


# ------------------------------------------------------------- dedupe

def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def dedupe_job(rel):
    recs = []
    for row in rows(rel)[1:]:
        recs.append({"id": int(row[0]), "first": row[1], "last": row[2], "email": row[3], "city": row[4]})
    recs.sort(key=lambda r: r["id"])
    blocks = {}
    for i, r in enumerate(recs):
        last = r["last"].strip().lower()
        for key in ("S:" + jf.soundex(last), "M:" + jf.metaphone(last)):
            blocks.setdefault(key, []).append(i)
    pairs = set()
    for key in blocks:
        members = blocks[key]
        for x in range(len(members)):
            for y in range(x + 1, len(members)):
                pairs.add((members[x], members[y]))
    emit("%d records, %d blocks, %d candidate pairs" % (len(recs), len(blocks), len(pairs)))
    parent = list(range(len(recs)))
    for i, j in sorted(pairs):
        a, b = recs[i], recs[j]
        jl = jf.jaro_winkler_similarity(a["last"].lower(), b["last"].lower())
        jfi = jf.jaro_winkler_similarity(a["first"].lower(), b["first"].lower())
        ea = a["email"].split("@")[0]
        eb = b["email"].split("@")[0]
        ed = jf.damerau_levenshtein_distance(ea, eb)
        mra = jf.match_rating_comparison(a["last"], b["last"])
        score = (0.5 * jl + 0.35 * jfi) + 0.15 * (1.0 - min(ed, 5) / 5.0)
        same = score >= 0.9 or (score >= 0.82 and mra is True and a["city"] == b["city"])
        if same:
            parent[find(parent, i)] = find(parent, j)
        emit("  %d~%d last=%r first=%r email=%d mra=%r score=%r %s" % (
            a["id"], b["id"], jl, jfi, ed, mra, score, "MATCH" if same else "-"))
    clusters = {}
    for i in range(len(recs)):
        clusters.setdefault(find(parent, i), []).append(i)
    groups = sorted(sorted(recs[i]["id"] for i in c) for c in clusters.values() if len(c) > 1)
    emit("%d duplicate groups" % len(groups))
    by_id = {r["id"]: r for r in recs}
    for g in groups:
        emit("  " + "; ".join("%d %s %s <%s>" % (n, by_id[n]["first"], by_id[n]["last"], by_id[n]["email"])
                              for n in g))


# ------------------------------------------------------------ suggest

def suggest_job(cmds_rel, typos_rel):
    cmds = read(cmds_rel).splitlines()
    for t in read(typos_rel).splitlines():
        if t in cmds:
            emit("%s: a command" % t)
            continue
        scored = []
        for c in cmds:
            d = jf.damerau_levenshtein_distance(t.lower(), c)
            if d <= 2:
                scored.append((d, -jf.jaro_winkler_similarity(t.lower(), c), c))
        scored.sort()
        if not scored:
            emit("git: '%s' is not a git command. See 'git --help'." % t)
            continue
        emit("git: '%s' is not a git command. The most similar command%s" % (
            t, " is" if len(scored) == 1 else "s are"))
        for d, s, c in scored[:4]:
            emit("        %s (distance %d, similarity %r)" % (c, d, -s))


# ------------------------------------------------------------- search

def search_job(names_rel, queries_rel):
    names = read(names_rel).splitlines()
    for q in read(queries_rel).splitlines():
        emit("? %s" % q)
        for label, enc in (("soundex", jf.soundex), ("nysiis", jf.nysiis), ("metaphone", jf.metaphone)):
            code = enc(q)
            hits = [n for n in names if enc(n) == code]
            emit("  %s %s: %s" % (label, code, ", ".join(hits) if hits else "-"))
        mra = [n for n in names if jf.match_rating_comparison(q, n) is True]
        emit("  match rating: %s" % (", ".join(mra) if mra else "-"))
        best = []
        for n in names:
            best.append((-jf.jaro_winkler_similarity(q.lower(), n.lower()), n))
        best.sort()
        emit("  closest: %s" % ", ".join("%s %r" % (n, -s) for s, n in best[:3]))


# ------------------------------------------------------------- lookup

def tokens(s):
    out = []
    word = ""
    for ch in s.lower():
        if ch.isalnum():
            word += ch
        elif word:
            out.append(word)
            word = ""
    if word:
        out.append(word)
    return out


def lookup_job(products_rel, queries_rel):
    products = read(products_rel).splitlines()
    for q in read(queries_rel).splitlines():
        qt = tokens(q)
        scored = []
        for p in products:
            pt = tokens(p)
            total = 0.0
            for w in qt:
                best = 0.0
                for v in pt:
                    s = jf.jaro_winkler_similarity(w, v)
                    if s > best:
                        best = s
                total += best
            whole = jf.jaro_winkler_similarity("".join(qt), "".join(pt))
            score = (total / len(qt) if qt else 0.0) * 0.7 + whole * 0.3
            scored.append((-score, p))
        scored.sort()
        top = [(p, -s) for s, p in scored[:3] if -s >= 0.75]
        emit("%r -> %s" % (q, "; ".join("%s (%r)" % t for t in top) if top else "no match"))


def main():
    for line in read("jobs.tsv").splitlines():
        job = line.split("\t")
        emit("== " + " ".join(job))
        if job[0] == "vectors":
            vectors_job(job[1])
        elif job[0] == "encode":
            encode_job(job[1])
        elif job[0] == "compare":
            compare_job(job[1])
        elif job[0] == "dedupe":
            dedupe_job(job[1])
        elif job[0] == "suggest":
            suggest_job(job[1], job[2])
        elif job[0] == "search":
            search_job(job[1], job[2])
        else:
            lookup_job(job[1], job[2])
    sys.stdout.write("\n".join(OUT) + "\n")


main()
