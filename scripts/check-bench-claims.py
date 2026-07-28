#!/usr/bin/env python3
"""Find README claims about Kara that the CURRENT feed contradicts.

A candidate generator, NOT a verdict. Every hit must be read against the file
before anything is edited — an earlier, looser version of this script produced
119 "contradictions" of which the first handful were all false positives:
negated claims, compile-time claims judged against runtime rows, par-lane claims
judged against seq, and sentences whose verb attached to Go rather than Kara.

Precision measures now in place:
  * negation-aware      -- "does not lead C" is not a claim that it leads C
  * lane-aware          -- a sentence under "### Compile elapsed" or a par-lane
                           heading is never judged against the seq runtime rows
  * comparator-aware    -- "rustc -O"/"wrapping" compares vs rust, "checked"/
                           "overflow-checks" vs rust_ovf
  * magnitude-gated     -- ratios within MARGIN of parity are not contradictions
  * subject-gated       -- the direction verb must follow a Kara mention and not
                           be preceded by another language closer to the verb
"""
import json
import glob
import os
import re

GEN = "The kata's tiny fixed inputs aren't a workload"
SUF = ("_ovf", "_rschk", "_overflow_checks", "_chk")
MARGIN = 0.05          # within +-5% of parity, direction is noise

AHEAD = r"(?:ahead of|leads?|faster than|beats?|outruns?|outperforms?|edges? out)"
BEHIND = r"(?:behind|slower than|trails?|loses? to|lags?)"
NEG = r"(?:not|n't|no longer|never|rather than|instead of)"
LANG = {
    "c": r"(?:\bC\b(?!\+\+)|clang)",
    "rust": r"(?:\bRust\b|rustc|rayon)",
    "go": r"(?:\bGo\b|golang|goroutine)",
}
# Headings whose prose is about something other than the seq runtime lane.
OFF_LANE = re.compile(
    r"compile|binary size|memory|rss|par lane|auto-par|parallel|python|why this kata",
    re.I,
)


def norm(m):
    l, a = m["lang"], m["approach"]
    if l == "rust":
        for s in SUF:
            if a.endswith(s):
                return "rust_ovf", a[: -len(s)]
    return l, a


def feed_for(rj):
    r = json.load(open(rj))
    by = {}
    for m in r.get("measurements", []):
        if not m.get("runtime") or m.get("lane") not in (None, "seq"):
            continue
        l, a = norm(m)
        by.setdefault(a, {}).setdefault(l, m["runtime"]["mean_ms"])
    return r["kata"], by


def seq_sentences(body):
    """Yield (sentence, heading) for prose under seq-relevant headings only."""
    heading = ""
    for block in re.split(r"\n(?=### )", body):
        h = block.split("\n", 1)[0]
        heading = h if h.startswith("###") else heading
        if OFF_LANE.search(heading):
            continue
        prose = "\n".join(
            l for l in block.split("\n")
            if not l.lstrip().startswith(("|", ">", "#"))
        )
        for s in re.split(r"(?<=[.!?])\s+", prose):
            yield s, heading


def judge(by, sent):
    out = []
    if not re.search(r"k[āa]ra", sent, re.I):
        return out
    for lang, pat in LANG.items():
        if not re.search(pat, sent):
            continue
        a = re.search(AHEAD + r"[^.]{0,40}?" + pat, sent, re.I)
        b = re.search(BEHIND + r"[^.]{0,40}?" + pat, sent, re.I)
        if bool(a) == bool(b):
            continue
        m = a or b
        # negation immediately before the verb flips/voids the claim
        pre = sent[max(0, m.start() - 45):m.start()]
        if re.search(NEG + r"\s*$", pre, re.I) or re.search(NEG + r"\W+\w{0,12}$", pre, re.I):
            continue
        # the verb must belong to Kara: require a kara mention before it with no
        # other language name in between
        head = sent[:m.start()]
        km = list(re.finditer(r"k[āa]ra", head, re.I))
        if not km:
            continue
        between = head[km[-1].end():]
        if any(re.search(p, between) for k, p in LANG.items() if k != lang):
            continue
        claimed_faster = bool(a)

        # which rust does the sentence mean?
        key = lang
        if lang == "rust":
            if re.search(r"overflow-checks|checked|equal-safety|safety-matched|safety matched", sent, re.I):
                key = "rust_ovf"
            elif re.search(r"rustc -O\b|wrapping|stock Rust|`rust -O`", sent, re.I):
                key = "rust"
            else:
                key = None          # ambiguous -> require BOTH to contradict
        cmps = []
        for app, langs in by.items():
            if "kara" not in langs:
                continue
            keys = [key] if key else [k for k in ("rust", "rust_ovf") if k in langs]
            for k in keys:
                if k in langs:
                    cmps.append((app, langs["kara"] / langs[k], k))
        if not cmps:
            continue
        material = [c for c in cmps if abs(c[1] - 1) > MARGIN]
        if not material:
            continue
        if any((r < 1) == claimed_faster for _, r, _ in material):
            continue
        worst = max(material, key=lambda c: abs(c[1] - 1))
        out.append((lang, claimed_faster, worst,
                    "; ".join(f"{a}: kara/{k}={r:.2f}x" for a, r, k in material)))
    return out


def main():
    hits = []
    for rj in sorted(glob.glob("leetcode/*/*/bench/results.json")):
        d = os.path.dirname(os.path.dirname(rj))
        rd = f"{d}/README.md"
        if not os.path.exists(rd):
            continue
        hand = [
            s for s in re.findall(r"\n## Benchmarks\n(.*?)(?=\n## |\Z)", open(rd).read(), re.S)
            if not (GEN in s and "\n### " not in s)
        ]
        if not hand:
            continue
        kata, by = feed_for(rj)
        for sent, heading in seq_sentences("\n".join(hand)):
            for lang, cf, worst, det in judge(by, sent):
                hits.append((abs(worst[1] - 1), kata["id"], kata["slug"], d,
                             lang, cf, re.sub(r"\s+", " ", sent).strip(), det, heading))

    hits.sort(reverse=True)
    print(f"CONTRADICTED (candidates): {len(hits)} across {len({h[1] for h in hits})} katas\n")
    for sev, kid, slug, d, lang, cf, sent, det, heading in hits[:30]:
        print(f"#{kid} {slug}   [severity {sev*100:.0f}%]")
        print(f"   claims kara FASTER than {lang}" if cf else f"   claims kara SLOWER than {lang}")
        print(f"   feed: {det}")
        print(f"   \"{sent[:180]}\"\n")


if __name__ == "__main__":
    main()
