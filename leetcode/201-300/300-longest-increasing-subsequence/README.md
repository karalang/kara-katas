# 300. Longest Increasing Subsequence

Return the length of the longest **strictly** increasing subsequence. A
subsequence keeps relative order but need not be contiguous.

```
[10, 9, 2, 5, 3, 7, 101, 18]  ->  4     e.g. 2, 3, 7, 101
[0, 1, 0, 3, 2, 3]            ->  4     0, 1, 2, 3
[7, 7, 7, 7]                  ->  1     STRICT, so equal values don't chain
[5, 4, 3, 2, 1]               ->  1
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `longest_increasing_subsequence.kara` ★ | patience sorting, binary search over `tails` | O(n log n) |
| `longest_increasing_subsequence_dp.kara` | `best[i]` = LIS ending at `i`, the definition transcribed | O(n²) |
| `longest_increasing_subsequence_reconstruct.kara` | patience sorting + parent pointers, returns a **witness** | O(n log n) |
| `differential.kara` | 6,750 generated cases, three arms, six properties | — |
| `bench/lisscan.kara` | 3000 arrays × 512 elements × 24 passes | benchmark lane |

### Where strictness lives, and why that matters for testing

The fast arm decides strictness inside a binary search — the `>=` half of
`if tails[mid] < x`. The DP decides it in a guard, `nums[j] < nums[i]`. Two
unrelated spellings in two unrelated places, which is what makes a differential
between them actually *test* strictness rather than duplicate one decision.

### `tails` is a summary, not a witness

`tails[k]` is the **smallest value** that can end an increasing subsequence of
length `k+1`. Its length is the answer, but its contents are frequently not a
subsequence of the input at all:

```
nums  = [3, 4, 1, 2]
tails = [1, 2]          <- correct length 2, but 3,4 was the run it displaced
```

Printing `tails` as the answer is a real and common bug that yields the correct
**length** always and the correct **sequence** only sometimes — invisible to any
test that checks the number. `..._reconstruct.kara` recovers a real witness with
parent pointers, and that is what lets the differential check something a length
cannot express.

## Properties, not just agreement

| | property |
|---|---|
| P1 | the three arms agree |
| P2 | `0 <= len <= n`, and `len >= 1` whenever `n >= 1` |
| P3 | ascending → `n`; strictly descending → 1; all-equal → 1 |
| P4 | **reverse-and-negate invariance** — that transform maps increasing subsequences bijectively onto increasing subsequences, so the length cannot change |
| P5 | the witness is **real**: strictly increasing, genuinely a subsequence, and as long as the number claimed |
| P6 | appending a new maximum extends the answer by exactly 1 |

P5 is the closest thing here to an independent oracle. A length is a single
integer — an implementation can return the right one for the wrong reason on
every input a generator is likely to produce. A witness can be interrogated, and
none of the three questions asked of it cares how it was computed.

### Mutation-tested, because a differential that cannot fail is decoration

| mutation | caught by | cases (of 6,750) |
|---|---|---|
| arm A non-strict (`<` → `<=`) | P1, P3, P5 | 2,989 / 59 / 2,989 |
| arm B non-strict | P1, P3 | 2,989 / 59 |
| arm C non-strict | P1, P5 | 2,989 / 6,173 |
| arm C wrong parent slot | P1, P5 | 2,600 / 2,600 |
| **all three arms non-strict** | **P3, P5 only** | **59 / 3,184** |

The last row is the one that justifies the properties. With every arm carrying
the same misreading, **P1 drops to zero** — three-way agreement is completely
blind — and only the statement-derived checks notice.

> A methodological note, since it nearly went the other way: the first run of
> this battery reported two mutations *surviving*. They had not survived; the
> anchor string I was patching also occurs in a **doc comment**, so those two
> runs edited prose and tested an unmutated file. Anchoring on line numbers
> instead produced the table above. A mutation test that reports "survived" is
> making a claim about your test suite, and it is worth confirming the mutation
> actually applied before believing it.

## Benchmarks

Build 3,000 arrays of 512 elements once, then 24 patience-sorting passes.
`build-once + punch` (BENCHMARKS.md). Patience sorting is a binary search per
element with a data-dependent access pattern, so unlike
[#299](../299-bulls-and-cows/)'s flat tally there is nothing here for a
vectorizer to take. The `tails` buffer is `Array[i64, 512]`, allocated once and
reused by resetting a logical length — matching C's `long tails[512]` and Rust's
`[0i64; 512]` exactly, which is the mirror-symmetry lesson #299 learned the hard
way. All five languages print `checksum 122670492`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each. See [BENCHMARKS.md](../../../BENCHMARKS.md) for methodology and caveats.

| | mean | vs kara |
|---|---:|---:|
| **kara** (codegen, seq) | **714.0 ms** | **1.00×** |
| c (`-O3 -march=x86-64-v3`, matched ISA) | 934.9 ms | 1.31× |
| c (`-O3`) | 958.7 ms | 1.34× |
| go | 1.057 s | 1.48× |
| rust (`-O`) | 1.071 s | 1.50× |
| rust (`-O -C overflow-checks=on`, equal safety) | 1.075 s | 1.51× |
| python | 15.437 s | 21.6× |

**Kāra is the fastest mirror here**, ahead of `clang -O3` by 1.31×. That is an
unusual enough result to be worth saying how hard it was pushed on:

- **Not auto-parallelism.** `KARAC_AUTO_PAR=0` measures 716.3 ms against the
  default's 713.8 — 1.00× — and user time tracks wall in both, so the timed
  build is single-threaded.
- **Not a handicapped C mirror.** The first draft of `lisscan.c` used `long`
  for the search indices and cost **1.249 s**. That is a 1.31× self-inflicted
  penalty: clang emits the sign-correction sequence for a signed `/ 2`.
  Rewriting the indices as `size_t` — the idiomatic C choice, and what the Rust
  mirror already had via `usize` — lands at 950 ms, and `>> 1` or
  `unsigned long` land in the same place (949.9 / 963.3). The published mirror
  uses `size_t`.
- **Not aliasing.** `restrict` on the data pointer changes nothing (963.3 ms).

### The one-character cliff — `kara B-2026-08-29-62`

Rewriting the midpoint as `lo + ((hi - lo) >> 1)` — the same value, and the
rewrite a performance-minded programmer reaches for believing a shift beats a
divide — makes the Kāra lane **1.61× slower**:

| | `/ 2` | `>> 1` |
|---|---:|---:|
| wall | 709.1 ms | 1.144 s |
| instructions | 18,459,532 | 17,082,883 (**−7.5%**) |
| branches | 2,952,946 | 5,793,071 (+96%) |
| mispredicts | 178,447 | **700,820 (+293%)** |

Fewer instructions, 61% slower. The `/ 2` spelling is if-converted to branchless
`cmovge`/`cmovl`; the `>> 1` spelling is not, and leaves a coin-flip branch on
every search step. Ruled out, each measured: the shift operator's own cost (an
isolated loop measures both at 101 ms), bounds checks (the two disassemblies are
6258 and 6261 lines), and division semantics (Kāra's `/` truncates toward zero
exactly like C's, on both backends).

**The same micro-decision runs the opposite way in C**, which is what makes the
pair worth keeping: signed `/ 2` costs clang 31% and the shift recovers it, while
in Kāra the shift *loses* 61%. Two languages, one source-level choice, opposite
signs.

### Elsewhere

| | kara | c | rust | go |
|---|---:|---:|---:|---:|
| binary size | 337.5 KiB | 15.7 KiB | 3862.8 KiB | 2178.5 KiB |
| compile (cold) | 387 ms | 94 ms | 134 ms | — |

## Running it

```bash
karac run   longest_increasing_subsequence.kara
karac build longest_increasing_subsequence.kara && ./longest_increasing_subsequence
karac run   --interp differential.kara
python3     longest_increasing_subsequence.py
KARA_BENCH_INCLUDE_PY=1 BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
