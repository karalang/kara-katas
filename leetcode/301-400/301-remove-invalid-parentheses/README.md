# 301. Remove Invalid Parentheses

Remove the **minimum** number of `(` and `)` so the string becomes valid, and
return **every** distinct string achievable with that minimum. Characters that
are not parentheses are never removed.

```
"()())()"   ->  ["(())()", "()()()"]
"(a)())()"  ->  ["(a())()", "(a)()()"]
")("        ->  [""]
"()(()"     ->  ["()()"]          only ONE, though two different '(' qualify
```

That last line is the whole problem in miniature. Both the `(` at index 2 and
the one at index 3 can be the one removed, and both choices produce `"()()"` —
so a search that branches on *positions* finds two answers where the statement
has one. Every arm here differs mainly in what it does about that.

## Approaches

| file | mechanism | dedup |
|---|---|---|
| `remove_invalid_parentheses.kara` ★ | bounded DFS; budget from a one-pass count | a `Set` |
| `remove_invalid_parentheses_bfs.kara` | level-order by removal count | a `Set`, per level |
| `remove_invalid_parentheses_unique.kara` | scan to the first violation, canonicalise the choice | **none** |
| `differential.kara` | 1,320 generated cases, three arms, an exhaustive oracle, seven properties | — |
| `bench/parenrepair.kara` | 2,000 strings × 24 bytes × 64 passes | benchmark lane |

### Two questions, and they fail independently

The statement asks for the minimum removal **count** and the complete **set** of
strings achieving it. An implementation can be right about one and wrong about
the other, and the most common bugs are exactly that shape: a dedup guard one
notch too strong drops real answers while every answer it *does* return stays
valid and minimal. Nothing about eyeballing the output catches that.

So the three arms are chosen so that no two of them can be wrong about
minimality the same way:

| arm | why its answer is minimal |
|---|---|
| A | **counting** — a one-pass tally of unmatchable `(` and `)` |
| B | **search order** — the shallowest level that contains anything valid |
| C | **construction** — a deletion only ever happens at a real violation |

Arm A's argument is the one worth spelling out, since it is what turns an
exponential search into a bounded one. Scan left to right carrying `open`:
a `(` increments it, a `)` decrements it unless it is already zero — in which
case that `)` can never be matched by anything to its left or right, so it must
go. Whatever `open` remains at the end is unmatchable `(`. Those two counters
are a **lower** bound because each character they name is individually doomed,
and an **achievable** one because deleting exactly them leaves a valid string.
The DFS then never searches for the minimum; it enumerates the ways to spend a
budget it already knows, and a leaf is valid by construction — budget zero and
`open` zero — rather than by re-validating.

### What the `Set` costs, measured

Arms A and B generate duplicates and discard them. Over the 2,000-string
benchmark corpus, arm A reaches **147,246 leaves to produce 28,179 distinct
answers** — 5.23× wasted work, every unit of it a string built, hashed, and
thrown away. The worst single case in that corpus, `")(())))))aaa(()((((a))aa"`,
reaches **240 leaves for 2 answers**.

`..._unique.kara` gets that to 1.00× by removing the two ways a duplicate can
arise rather than detecting them afterwards:

- **the same deletions in a different order** — killed by `last_j`: a recursive
  call may only delete at a position at or after the one its parent deleted, so
  each *set* of positions is reached by exactly one increasing sequence;
- **a different member of a run of identical parens** — killed by
  `bytes[j - 1] != close`: only the first `)` of a consecutive run is a legal
  deletion point, since deleting any other yields the same string.

Together those make the enumeration a bijection onto the answer set. It is a
much better algorithm and a much harder one to be sure of, which is why both
spellings are here and why the differential leans on the pair.

### The mirror trick

The scan in arm C only ever finds an unmatchable `)` — a surplus `(` produces no
violation at all, since the counter simply ends positive. Rather than write a
second, mirror-image scan, reverse the string and run the *same* scan with `(`
and `)` swapped. A surplus `(` in the original is a surplus `)` in the reversal,
and the recursion bottoms out having reversed twice, so what it emits is in the
original orientation.

That symmetry is also a statement about the answer *set* — `answers(mirror(s))`
must equal `mirror(answers(s))` — which is property P6 below, checked
independently of the arm that exploits it.

### Output order is not the problem's to choose

The statement permits any order, and the `Set` walk inside arms A and B would
give a different one on **every run** — `Map`/`Set` iteration is per-process
random (see the repo `CLAUDE.md`). Under this corpus's A/B rule that is
indistinguishable from a run/build divergence, so every arm sorts bytewise
before returning. The sort is hand-written rather than delegated, in all five
languages, so the mirrors are provably identical rather than coincidentally so.

## Properties, not just agreement

| | property |
|---|---|
| P1 | the three arms agree, as sorted sequences |
| P2 | every returned string is valid |
| P3 | every returned string is a subsequence of the input, and its non-paren characters are the input's, unchanged and in order |
| P4 | all answers share one length, equal to `n` minus the one-pass budget |
| P5 | no arm returns a duplicate, and no arm returns nothing |
| P6 | `answers(mirror(s)) == mirror(answers(s))` — reverse and swap the paren kinds |
| P7 | an **exhaustive** oracle agrees: every subset of the paren positions, deleted, keeping the valid results with the fewest deletions |

P7 is the closest thing here to an independent check, and it earns that by
embodying no argument at all. It does not reason about minimality — it *measures*
it, over 2^p subsets — so it cannot be subtly wrong in a way that a clever arm
might be. It is exponential, so it runs only where p ≤ 10; that is 1,237 of the
1,320 cases, and it is exactly the short, tie-dense region where dedup logic
actually breaks.

P5 checks **all three** arms rather than just the one P2–P4 interrogate. Arm C's
two canonicalisation guards exist nowhere else in the file, so a P5 that looked
only at arm A would have left them covered by P1 alone — see the table below for
what that costs.

## Mutation-tested, because a differential that cannot fail is decoration

Each row is one line changed in `differential.kara`, rebuilt and rerun. Counts
are cases flagged, out of 1,320.

| mutation | caught by | counts |
|---|---|---|
| A keeps `)` with nothing open | P1, P2, P6, P7 | 870 / 1315 / 435 / 372 |
| A's budget miscounts an unmatched `)` | P1, P4, P5, P6, P7 | 1116 / 12 / 558 / 558 / 514 |
| A drops the `Set` dedup | P1, P5, P6, P7 | 844 / 2367 / 422 / 360 |
| C drops the run canonicalisation | P1, P5, P6 | 422 / 2367 / 422 |
| C drops the `last_j` floor | P1, P5, P6 | 59 / 218 / 59 |
| C resumes the scan past the violation | P1, P5, P6 | 814 / 4 / 813 |
| B does not stop at the first valid level | **P1 only** | 579 |
| shared `is_valid` accepts an unmatched `)` | P1, P7 — **P2 blind** | 594 / 523 |

Two rows carry the argument.

**Row 7** is why three arms and not two. Making arm B search one level too deep
leaves every answer it returns valid, minimal-looking, unique, correctly shaped,
and mirror-symmetric — six of the seven properties see nothing, because they are
statements about a single answer set and that set is internally consistent. Only
cross-arm disagreement notices.

**Row 8** is the converse, and the more uncomfortable one. `is_valid` is shared
between arm B, the oracle, and property P2. Break it and **P2 reports zero** — a
property checked with the same predicate the arms use is not an independent
check, however statement-shaped it looks. What catches it is P1 (arm A computes
validity a different way, so it disagrees) and P7. The lesson generalises past
this kata: a property is only as independent as its least independent helper.

## Benchmarks

Build 2,000 random 24-byte strings over `(`, `)`, `a` once, then punch 64
repair passes through them — `build-once + punch` ([BENCHMARKS.md](../../../BENCHMARKS.md)).
All five languages print `results 1803456` / `checksum 440593484`.

**The benchmarked arm is `..._unique`, not the ★ one, and that is a deliberate
methodology choice.** The canonical solution deduplicates with a hash set, and a
hash set is the one data structure whose implementation differs most across
these five languages: Go's map, Python's set, Rust's SipHash-by-default
`HashMap`, and whatever table a C mirror would have to grow by hand. Timing that
would mostly time five hash tables. The unique-by-construction arm needs no set,
so all five mirrors run the same recursion over the same bytes.

Every mirror works in one preallocated scratch buffer of 32 × 32 bytes indexed
by recursion depth — level `d` reads at `d × 32` and writes its child at
`(d + 1) × 32` — which is what C would write as `unsigned char scratch[32][32]`.
Spelling it as a flat index in the other four keeps them symmetric, the lesson
[#299](../../201-300/299-bulls-and-cows/) and
[#300](../../201-300/300-longest-increasing-subsequence/) each learned by
getting it wrong first. Nothing allocates inside the timed loop, and the sink
folds each repaired string into a rolling mod-p hash rather than collecting it,
so the measurement is the search rather than the collection.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each. See [BENCHMARKS.md](../../../BENCHMARKS.md) for methodology and caveats.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3`) | 427.8 ms | 0.61× |
| c (`-O3 -march=x86-64-v3`, matched ISA) | 428.4 ms | 0.61× |
| rust (`-O`) | 534.1 ms | 0.76× |
| go | 554.8 ms | 0.79× |
| **kara** (codegen, seq) | **701.9 ms** | **1.00×** |
| rust (`-O -C overflow-checks=on`, equal safety) | 736.2 ms | 1.05× |
| rust (equal safety + matched ISA) | 756.6 ms | 1.08× |
| python | 21.249 s | 30.3× |

The equal-safety row is the one to read first. Kāra checks integer overflow by
default; `rustc -O` silently wraps. Turning Rust's checks on to match costs it
38% here — 534.1 → 736.2 ms — and puts Kāra **ahead of Rust at equal safety**,
1.05×, while still carrying bounds checks on every `scratch[...]` access that
the C mirror's raw pointers do not.

Against unchecked builds Kāra is 1.31× behind `rustc -O` and 1.64× behind
`clang -O3`. Two things it is *not*:

- **Not auto-parallelism, in either direction.** The default build measures
  682.7 ms against `KARAC_AUTO_PAR=0`'s 678.6 — 1.01×, inside the noise — and
  user time tracks wall in both, so the timed build is single-threaded. The
  recursion is a serial dependence chain over one shared scratch buffer; there
  is nothing here to parallelise and auto-par correctly declines to try.
- **Not a vectorization gap.** Where the recursion branches is decided by where
  the paren counter first goes negative, so the control flow is data-dependent
  and no mirror gets to vectorize the inner loops. This is the same property
  that makes #300's patience sort an honest sequential comparison.

The remaining gap is the ordinary one: bounds checks plus a younger backend on
byte-at-a-time copy loops.

### Elsewhere

| | kara | c | rust | go |
|---|---:|---:|---:|---:|
| binary size | 341.5 KiB | 15.8 KiB | 3864.1 KiB | 2179.0 KiB |
| compile (cold) | 467.5 ms | 140.0 ms | 164.3 ms | — |
| peak RSS | 2.5 MiB | 1.7 MiB | 2.1 MiB | 1.8 MiB |

Python's peak RSS is 8.0 MiB.

## Running it

```bash
karac run   remove_invalid_parentheses.kara
karac build remove_invalid_parentheses.kara && ./remove_invalid_parentheses
karac run   remove_invalid_parentheses_bfs.kara
karac run   remove_invalid_parentheses_unique.kara
karac run   --interp differential.kara
python3     remove_invalid_parentheses.py
KARA_BENCH_INCLUDE_PY=1 BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
