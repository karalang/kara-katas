# 318. Maximum Product of Word Lengths

Given a list of lowercase words, return the largest `len(a) * len(b)` over
pairs that share no letter — or `0` if every pair collides.

```
["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]   -> 16   "abcw" x "xtfn"
["a", "ab", "abc", "d", "cd", "bcd", "abcd"]      ->  4   "ab"   x "cd"
["a", "aa", "aaa", "aaaa"]                        ->  0   every pair shares 'a'
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `max_product.kara` ★ | 26-bit letter masks, every pair tested with one `&` | `O(n² + nL)` |
| `max_product_dedup.kara` | collapse equal letter sets to their longest word first | `O(d² + nL)`, `d` = distinct masks |
| `max_product_sets.kara` | 26-slot presence table per pair, no bit arithmetic at all | `O(n²L)` |
| `max_product_sorted.kara` | descending length, the product bound cutting each row | `O(n log n + n²)` worst case |
| `differential.kara` | four arms, twelve properties, 2,175 word lists | — |
| `bench/max_product.kara` | 6,000-word corpus, 15 rewrite passes | — |

## Four ways to find the pair

**★ The letter set is 26 bits.** The statement asks whether two words share a
letter, which is a set intersection, and running a set intersection inside an
`O(n²)` pair loop makes the whole thing `O(n²L)`. But there are only 26
letters, so a word's letter set fits in an integer and the intersection test
becomes `masks[i] & masks[j] == 0` — one instruction, independent of how long
the words are. Building the masks is one pass over the input; after that the
word lengths never have to be looked at again except to multiply.

What the mask throws away is worth being explicit about, because it is what
makes the encoding safe: it forgets both the ORDER and the MULTIPLICITY of the
letters, and the disjointness test cannot see either. It does *not* forget the
length — that is kept separately in `lens`, precisely because the mask cannot
reconstruct it. `"aaaa"` and `"a"` share a mask and give different answers.

**Collapse equal letter sets.** The pair test only ever reads the mask, so two
words with the same letter set are interchangeable in every pair they take
part in — and between two such words the longer one wins every product the
shorter one would. The shorter one can therefore be deleted before the pair
loop runs at all. That turns the quadratic factor from "number of words" into
"number of distinct letter sets". On an anagram-heavy input (`eat`/`tea`/`ate`
is one mask, not three) the collapse is dramatic; on an input of all-distinct
masks it costs one map build and saves nothing.

The map is a `SortedMap`, not a `Map`. Nothing in this arm depends on the walk
order — `best` is a maximum, and a maximum is order-independent — but Kāra's
`Map` iterates in per-process hash order, and a kata that walks one at all is
one refactor away from printing in that order. The fix is to not have the
surface. (Repo rule; kara `B-2026-08-21-6`.)

**The literal reading, with no mask anywhere.** This arm does exactly what the
statement says: mark one word's letters in a 26-slot presence table, scan the
other against it. It is the slow arm, and that is the point — it is the
*oracle*, and it shares no machinery with the other three. No `1 <<`, no `&`,
no `word_mask`. A sign error in the shift, an off-by-one in the alphabet base,
an `&` written where `|` was meant: none of those can hide here, because none
of them exist here. The presence table is rebuilt per pair rather than cached
per word, which makes the arm `O(n²L)` and keeps it honest — nothing is
precomputed, so nothing precomputed can be stale.

**Sort, then let the bound cut.** The three arms above visit all `n(n-1)/2`
pairs unconditionally: the answer is a maximum, and there is no reason to look
at a pair before you have looked at the rest. Sorting longest-first supplies
that reason. In descending order the products along each inner row are
non-increasing, so the moment `lens[i] * lens[j] <= best` no later `j` in that
row can beat `best` — break out of the row, not just skip the pair. The outer
loop gets its own bound for the same reason: once `lens[i] * lens[i]` cannot
beat `best`, no pair starting at `i` or later can either.

That break is what makes this a different failure surface rather than a
reordering of ★. It is a claim about a whole remaining row, made from one
product, and it is sound only because the row is sorted. Reverse the sort and
the arm silently returns a too-small answer on exactly the inputs where the
pruning fires — which is why the differential runs it against the unsorted
arms on thousands of cases rather than on the LeetCode examples, where the
first pair usually *is* the answer.

## Differential

`karac run differential.kara` sweeps every list size up to 9 across four
word-length caps and five alphabet widths (2,160 lists), plus fifteen patterned
ones the sweep will not reliably produce: all-alphabet words, anagram families,
two long colliding words hiding a shorter disjoint pair below them, and five
private-alphabet families.

```
cases 2175 nonzero 1367 pairable 1693 nonempty 1934 private-alphabet 28
DIFFERENTIAL OK
```

| # | property |
|---|---|
| P1 | arm A (mask) agrees with the set oracle |
| P2 | arm B (dedup) agrees with the set oracle |
| P3 | arm D (sorted) agrees with the set oracle |
| P4 | the answer is invariant under reordering — reversed, and a seeded shuffle |
| P5 | appending a copy of a word already present changes nothing |
| P6 | the answer is invariant under a bijective relabelling of the alphabet (all four arms) |
| P7 | deleting a word never increases the answer |
| P8 | appending a word never decreases the answer |
| P9 | the winning pair is really disjoint and really realises the answer; and a `0` answer means no disjoint pair exists at all |
| P10 | lengthening a word with a letter it already holds leaves the answer in `[old, old + longest]`, because the mask does not move |
| P11 | when every word owns a private alphabet, the answer is the product of the two longest lengths |
| P12 | the mask and the presence table describe the same set — bit-by-bit and pair-by-pair |

P4–P8 and P10 relate two invocations of the *same* arm, which is weight the
oracle cannot carry: a mutant wrong in the same direction on both inputs still
has to be wrong CONSISTENTLY under relabelling and reordering to slip them.
P12 is the only property that pins the two representations to each other
directly rather than through an answer, and that turned out to matter — see
M2 below.

## Mutation testing

Fifteen content-anchored edits to `differential.kara`, each run through the
full sweep. HANG, PANIC and BUILD-FAIL all count as kills, not just
`DIFFERENTIAL FAILED` — a mutation that makes the program crash has been
caught, and scoring only the property lines would have recorded it as silent.

| # | mutation | predicted | outcome | properties that fired |
|---|---|---|---|---|
| M1 | arm A pairs *colliding* words instead of disjoint ones | kill | **killed** | P1, P5, P6, P7, P8, P10, P11 |
| M2 | `1 << (letter + 1)` — every letter shifted up one bit | *silent* | **killed** | P12 only |
| M3 | `1 << (letter % 25)` — `z` collapses onto `a` | kill | **killed** | P1–P6, P8, P9, P10, P12 |
| M4 | `m ^ (1 << letter)` — XOR cancels a repeated letter | kill | **killed** | P1–P7, P9, P10, P12 |
| M5 | arm B keeps the *shortest* word of each letter set | kill | **killed** | P2, P6 |
| M6 | arm B keeps the *last* word of each letter set | kill | **killed** | P2, P6 |
| M7 | arm D sorts ascending, making its row break unsound | kill | **killed** | P3, P4, P6, P11 |
| M8 | arm D's outer bound drops the square (`li` for `li*li`) | kill | **killed** | P3, P4, P6 |
| M9 | arm D breaks on `<` instead of `<=` | *silent* | silent | — |
| M10 | the oracle never reports a collision | kill | **killed** | P1–P6, P8, P9, P10, P12 |
| M11 | the oracle skips every adjacent pair | kill | **killed** | P1–P7, P9, P10 |
| M12 | the oracle *sums* the lengths instead of multiplying | kill | **killed** | P1–P7, P9, P10 |
| M13 | the witness reports the pair `(i, i)` | kill | **killed** | P9 |
| M14 | the relabelling permutation is no longer a bijection | kill | **killed** | P6 |
| M15 | arm A's inner loop starts at `i`, pairing a word with itself | *silent* | silent | — |

**13 killed, 2 silent, 1 prediction wrong — and the wrong one is the useful
one.** M2 shifts every letter up one bit. That is a bijection on bits, and
disjointness only needs injectivity, so I predicted every answer would be
unchanged. Every answer *was* unchanged: P1 through P11 all stayed green
across 2,175 lists. P12 killed it on its own, because P12 is the one property
that asserts the mask *convention* — bit `k` is letter `k` — rather than an
answer computed from it.

So M2 is an answer-equivalent mutant caught by a representation property, and
it is the reason P12 earns its place. Without P12 the harness would have
scored M2 silent and been right to: nothing about the problem's answers can
distinguish the two encodings. With P12 the kata additionally pins down what
`word_mask` is *supposed* to return, which is what a reader of
`max_product.kara` is entitled to rely on.

The two genuine equivalents both survive for reasons worth stating. M9 weakens
arm D's break from `<=` to `<`: still sound, it just wastes a row it could
have skipped, so no answer moves. M15 lets arm A pair a word with itself —
`masks[i] & masks[i]` is non-zero for every non-empty word, and no input word
is empty, so the self-pair is never counted. That second one is a live
precondition rather than a tautology: feed this kata a list containing `""`
and M15 stops being equivalent.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` — the full A/B set the repo requires.

The benchmark mirror is verified on JIT, AOT-sequential and AOT-auto-par, and
against all four language twins, but deliberately *not* under `--interp`: it
is 15 passes of a 6,000-word `O(n²)` scan, which the tree-walk backend would
take hours to finish. The kata's semantics are covered by the four arms and
the differential, which do run on every backend.

## Benchmarks

`bench/max_product.kara` and its four mirrors build a 6,000-word corpus once
(lengths 1–16, each word drawn from its own random 7-letter window of the
alphabet) and then run 15 passes. Each pass rewrites exactly ONE word and
re-answers the whole corpus.

What each pass measures is deliberately *not* the bare global maximum. Over
6,000 words that answer saturates: the best disjoint pair of two 16-letter
words almost always survives one word being rewritten, so the answer sits at
256 pass after pass and the punch measures nothing. (Confirmed rather than
assumed — an instrumented build prints `top 256` on all 15 passes.) So each
pass instead records, for every word, the best partner it can pair with: the
same pair scan, with the result scattered across the corpus rather than
collapsed into one register. That moves on every rewrite — `total` walks
817376, 817456, 817408, … — and it keeps the inner loop honest, because a loop
that stores cannot be turned into a pure reduction.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container. Python is its own
lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 1162.7 ms ± 11.8 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 1163.9 ms ± 6.7 | 1.00× |
| rust `-O` | 1170.9 ms ± 8.0 | 1.01× |
| rust `-O -C overflow-checks=on` (equal-safety) | 1184.2 ms ± 6.7 | 1.02× |
| c `clang -O3` | 1199.4 ms ± 14.2 | 1.03× |
| **kāra `karac build`** | **1215.6 ms ± 15.9** | **1.05×** |
| go `go build` | 1350.1 ms ± 13.1 | 1.16× |
| python 3.11 | 18411 ms ± 680 | 15.8× |

Six of the seven compiled legs land inside 5% of each other, which is the
honest headline: **this workload measures the floor, not the ceiling.** The
inner loop is one load, one `AND`, one compare and a branch that is almost
never taken, and there is very little for a backend to be clever about. None
of the three binaries vectorises it — `objdump` finds zero packed-integer
instructions in any of them — because the two conditional stores into
`best[i]` and `best[j]` are a scatter, and a scatter defeats the same
vectoriser in clang, rustc and karac alike. A kata where every backend is
blocked by the same wall is a weak discriminator between backends, and it
should be read as "karac's scalar codegen has no gap here", not as a
throughput claim.

Two secondary readings do survive:

- **Equal-safety costs ~1%.** Kāra checks integer overflow by default and
  `rustc -O` silently wraps, so the comparison that matters is against
  `-C overflow-checks=on`: 1184.2 ms vs 1170.9 ms, a 1.1% tax on Rust, and
  Kāra pays the same kind of tax inside its own 1215.6 ms. Over 270M pair
  tests per run the checks are simply not where the time goes.
- **The matched-ISA twins barely move.** `-march=x86-64-v3` buys C 3.0% and
  Rust 0.7% — again, nothing to vectorise.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 93.5 ms ± 1.9 | 15.8 KiB | 2.41 MiB |
| rust | 156.2 ms ± 5.1 | 3864.2 KiB | 2.80 MiB |
| kāra | 336.9 ms ± 16.7 | 341.5 KiB | 3.19 MiB |
| go | — | 2179.3 KiB | 2.52 MiB |
| python | — | — | 8.83 MiB |

`karac build` is 3.6× clang's cold compile and 2.2× rustc's; its binary is 22×
clang's and 11× smaller than rustc's. Raw numbers in
`bench/results.container-x86.json`; methodology and caveats in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

Nothing to file. Every arm type-checked on the first `karac check` except the
demo loop in `max_product.kara`, where `let ws = cases[k];` moved out of an
index expression; `karac fix` applied the suggested `.clone()` and the file was
clean. No workarounds, no contorted phrasing, no `KARAC_AUTO_PAR=0`-only pass.
