#!/usr/bin/env python3
"""Find README claims about Kara that the CURRENT feed contradicts.

A candidate generator, NOT a verdict. Every hit must be read against the file
before anything is edited — an earlier, looser version of this script produced
119 "contradictions" of which the first handful were all false positives:
negated claims, compile-time claims judged against runtime rows, par-lane claims
judged against seq, and sentences whose verb attached to Go rather than Kara.

Usage:
  check-bench-claims.py            report contradictions, minus accepted misparses
  check-bench-claims.py --all      report everything, ignoring the baseline
  check-bench-claims.py --accept   record every current hit as a verified misparse

Precision measures in place:
  * negation-aware      -- "does not lead C" is not a claim that it leads C
  * lane-aware          -- both the ### heading AND the sentence itself, so an
                           inline "compiles this 2.3x faster than rustc" or a
                           rayon/auto-par sentence is never judged against seq
  * cross-kata-aware    -- "the alloc-bound siblings (#113 / #114) sit the other
                           way" is a claim about OTHER katas, not this one
  * comparator-aware    -- "rustc -O"/"wrapping" compares vs rust; "checked"/
                           "overflow-checks"/"safety-matched" vs rust_ovf
  * magnitude-gated     -- ratios within MARGIN of parity are not contradictions
  * subject-gated       -- the direction verb must follow a Kara mention with no
                           other language name between them

KNOWN LIMITS -- these produce false positives and are NOT worth solving here,
because each needs real parsing rather than another regex:
  * verb attachment across clauses ("... than Rust's Rc<RefCell>; Go's
    bump-allocator leads the lane" -- the lead is Go's)
  * ratio phrasing that means the opposite ("kara is 1.14x THE SEQ LEADER (C)"
    states a deficit, not a lead)
  * a sentence quoting a claim in order to refute it ("turned the container's
    rosy 'kara ahead of Rust' reading into an honest 1.06x gap")
  * claims about a source variant the feed does not carry (#95's RC-sharing
    generate_trees_share build)

That is what the baseline is for. `--accept` records hits a human has READ and
judged to be misparses into bench-claims-baseline.json, keyed by kata + a hash
of the sentence + the comparator. They stay suppressed until either the sentence
changes (hash moves) or the underlying ratio drifts more than DRIFT (25%), at
which point the earlier judgement may no longer hold and the hit returns.

Without this, every re-bench re-surfaces the same verified-fine claims and
someone eventually "corrects" a correct one -- which is exactly what nearly
happened to #51/#52, whose "ahead of safety-matched Rust" is TRUE against
rust_ovf and only looked wrong because the sentence's "default-safe" matched a
wrapping-Rust pattern.
"""
import json
import glob
import os
import re
import sys
import hashlib

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

# A sentence can be off-lane even under an on-lane heading. These three classes
# were all false positives in the 2026-07-28 triage:
#   "Kara compiles this 2.3x faster than rustc -O"   -> compile lane
#   "the auto-parallelizer's split pulls ahead"      -> par lane
#   "the alloc-bound siblings (#113 / #114) sit ..." -> a claim about OTHER katas
OFF_LANE_SENTENCE = re.compile(
    r"compiles? this|compile-cold|compile \(cold\)|binary size|peak RSS"
    r"|rayon|auto-par|auto-concurrency|intra-K[\u0101a]ra|goroutine|pthread|par \{",
    re.I,
)
CROSS_KATA = re.compile(r"\.\./\d+-|\bsiblings?\b|\bcorpus's other\b", re.I)


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
    # A sentence can be off-lane even under an on-lane heading, and a sentence
    # comparing OTHER katas is not a claim about this one. Both were confirmed
    # false-positive classes in the 2026-07-28 triage.
    if OFF_LANE_SENTENCE.search(sent) or CROSS_KATA.search(sent):
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


BASELINE = os.path.join(os.path.dirname(__file__), "bench-claims-baseline.json")
# How far the underlying ratio may drift before a baselined hit is re-surfaced.
DRIFT = 0.25


def sent_key(sent):
    return hashlib.sha1(re.sub(r"\s+", " ", sent).strip().encode()).hexdigest()[:12]


def load_baseline():
    if not os.path.exists(BASELINE):
        return {}
    return {
        (e["kata"], e["sha"], e["lang"]): e for e in json.load(open(BASELINE))["accepted"]
    }


def main():
    accept = "--accept" in sys.argv
    show_all = "--all" in sys.argv
    base = {} if (accept or show_all) else load_baseline()
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
                sha = sent_key(sent)
                prev = base.get((kata["id"], sha, lang))
                # Suppress a hit a human already read and accepted — UNLESS the
                # underlying ratio has since moved materially, in which case the
                # earlier "this is a misparse" judgement may no longer hold.
                if prev and abs(worst[1] / prev["ratio"] - 1) <= DRIFT:
                    continue
                hits.append((abs(worst[1] - 1), kata["id"], kata["slug"], d, lang,
                             cf, re.sub(r"\s+", " ", sent).strip(), det, sha, worst[1]))

    hits.sort(reverse=True)

    if accept:
        out = [{"kata": kid, "sha": sha, "lang": lang, "ratio": round(ratio, 4),
                "slug": slug, "claim": sent[:160]}
               for _, kid, slug, _, lang, _, sent, _, sha, ratio in hits]
        json.dump({"_comment": (
            "Claims a human READ and judged to be checker misparses, not real "
            "contradictions. Re-surfaces automatically if the sentence changes "
            f"(sha) or its ratio drifts more than {DRIFT:.0%}. Run with --all to "
            "see everything including these. Never accept a hit you have not "
            "verified against bench/results.json."),
            "accepted": out}, open(BASELINE, "w"), indent=1)
        print(f"accepted {len(out)} hits into {os.path.relpath(BASELINE)}")
        return

    n_sup = len(load_baseline()) if not show_all else 0
    print(f"CONTRADICTED (candidates): {len(hits)} across {len({h[1] for h in hits})} katas"
          + (f"   ({n_sup} accepted-as-misparse suppressed; --all to include)" if n_sup else "")
          + "\n")
    for sev, kid, slug, d, lang, cf, sent, det, sha, ratio in hits[:30]:
        print(f"#{kid} {slug}   [severity {sev*100:.0f}%]  {sha}")
        print(f"   claims kara FASTER than {lang}" if cf else f"   claims kara SLOWER than {lang}")
        print(f"   feed: {det}")
        print(f"   \"{sent[:180]}\"\n")


if __name__ == "__main__":
    main()
