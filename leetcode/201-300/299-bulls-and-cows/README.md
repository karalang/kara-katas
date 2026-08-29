# 299. Bulls and Cows

`secret` and `guess` are equal-length digit strings. A **bull** is a digit that
is right in the right place; a **cow** is a digit that occurs in the secret but
somewhere else. Report them as `"xAyB"`.

```
secret "1807", guess "7810"  ->  "1A3B"    8, 0 and 1 are all misplaced
secret "1123", guess "0111"  ->  "1A1B"    NOT "1A2B"
secret "1122", guess "2211"  ->  "0A4B"    a total derangement
secret "0000", guess "1111"  ->  "0A0B"    disjoint
```

## The whole problem is the second example

Bulls are trivial — one pass, compare position by position. Cows are where every
naive reading goes wrong, because *"occurs elsewhere"* is a **multiset**
question, not a membership one.

Guess `"0111"` holds three `1`s; secret `"1123"` holds two. One of the guess's
`1`s is already a bull, so it is spent. Of the two that remain, only **one** can
be paired against the secret's one leftover `1` — the third has nothing left to
match. So the cow count for a digit `d` is

```
min( count of d among non-bull secret positions,
     count of d among non-bull guess  positions )
```

summed over `d`. Asking instead *"does this guess digit appear anywhere in the
secret?"* double-counts, and so does *"how many `d` does the secret hold?"*
without excluding bulls. Both produce `1A2B`, and **both are invisible until a
digit repeats** — which is why the differential here generates repeats
deliberately rather than trusting the LeetCode samples, none of which catch it.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `bulls_and_cows.kara` ★ | two tallies, reconciled afterwards with `min` | O(n), two passes |
| `bulls_and_cows_onepass.kara` | one **signed balance**, reconciled as it goes | O(n), one pass |
| `bulls_and_cows_naive.kara` | mark bulls, then match positions and cross them off | O(n²), no arithmetic on counts |
| `differential.kara` | 27,000 generated cases, three arms, six properties | — |
| `bench/bullscore.kara` | 400k boards × 12 scoring passes | benchmark lane |

The three arms are deliberately *not* three spellings of one idea. The naive
version does no arithmetic on counts at all — it is a **matching**, not a tally —
so when the differential says all three agree, that is three independent
readings agreeing.

### The signed balance, since it is the one that needs an argument

`bulls_and_cows_onepass.kara` keeps a single array where `cnt[d] > 0` means the
secret has unclaimed `d`s and `cnt[d] < 0` means the guess does. At each non-bull
position it offers both digits against the standing debt:

```kara
if cnt[sd] < 0 { cows = cows + 1; }   cnt[sd] = cnt[sd] + 1;   // a guess sd was waiting
if cnt[gd] > 0 { cows = cows + 1; }   cnt[gd] = cnt[gd] - 1;   // a secret gd was waiting
```

The **directed** comparison is what makes it correct. A cow is booked only when
the *opposite* side already has an unclaimed copy, so the two halves of a pair
can never both book it. Reading `cnt[d] != 0` instead would count a digit against
its own side and inflate the answer — and that mutation is one the differential
catches.

## `Array[i64, 10]`, not `Vec` — and what the loose spelling costs

The tally has exactly ten slots because there are ten digits. The length is known
at compile time and never changes, so the honest type is `Array[i64, 10]`
(spelled `Array[0; 10]` as a repeat literal), not a `Vec`.

This started as a benchmark bug of my own making. The first version of
`bench/bullscore.kara` built its two tallies with `Vec.filled(4, 0)` inside the
scoring loop, against C's `long s_left[4] = {0}` and Rust's `[0i64; 4]` — a stack
slot and a couple of stores. That is two heap allocations per board, **9.6M over
the lane**, and it is not the same algorithm the mirrors were running:

| Kāra bench inner tally | mean (10 runs) |
|---|---:|
| `Vec.filled(4, 0)` ×2 per board | 452.7 ms ± 2.4 |
| `Array[i64, 4]` ×2 per board | **165.7 ms ± 1.8** |

Same checksum, same instruction count in the part that matters, **2.73× ± 0.03**. The
published table below uses the `Array` version. This is the identical failure
mode [#298](../298-binary-tree-longest-consecutive-sequence/) found in its *C*
mirror — a mirror that quietly does less work than its siblings — and it is worth
recording that it recurred one kata later, in the other direction, written by
someone who had just finished writing that warning down.

## Properties, not just agreement

Three arms that agree could still share a misreading, so the differential also
checks six facts that follow from the **statement** rather than from any code:

| | property |
|---|---|
| P1 | the three arms agree |
| P2 | `bulls + cows <= n`, both non-negative |
| P3 | a self-guess is `nA0B`, and nothing else is |
| P4 | symmetry — swapping secret and guess changes neither count |
| P5 | `bulls + cows` equals the multiset intersection, computed independently |
| P6 | a permutation of the secret saturates: `bulls + cows == n` |

**P5 is the load-bearing one.** It is computed by a fourth routine that ignores
positions entirely — tally both strings in full, sum the per-digit minimum. That
is the textbook definition of what bulls-plus-cows counts, and it is exactly the
identity the `"1123"`/`"0111"` case breaks for a naive implementation.

P2–P6 read only arm A's answer, which looks like a gap until you notice P1 runs
on the same case: once the arms are known to agree, a property holding for A
holds for all three.

Both halves are **mutation-tested** rather than assumed:

| mutation | caught by | cases |
|---|---|---:|
| arm C forgets to cross off a matched position | P1 | 7,283 / 27,000 |
| all three arms given the *same* misreading | P5 | 20,235 / 27,000 |

The second is the one that matters: a shared misreading sails past three-way
agreement on many inputs, and only the independent oracle notices.

### Alphabet size is the knob

Random 10-digit strings almost never repeat a digit in an interesting way, so a
suite built on them exercises the easy path only and reports green on an
implementation that gets the entire point of the problem wrong. The generator
sweeps alphabets of **2, 3, 4 and 10** — at alphabet 2 over length 8, collisions
are the rule and the multiset reconciliation is under constant pressure.

## Benchmarks

Build 400,000 secret/guess pairs once over a 4-digit alphabet, then make 12
scoring passes. Length 4 over 4 digits is the game as actually played and, more
usefully, a regime where **a repeat appears in about 96% of boards** — so the
`min(count, count)` path is under constant load rather than being skipped. Sink:
a polynomial hash folding *both* numbers for every board on every pass, so an
optimizer cannot drop the cow reconciliation. All five languages print
`checksum 951123599`.

The boards are decoded into a flat digit array **once**, outside the timed loop.
The kata's own function starts with `s.chars().collect()`, and benching that
would put a UTF-8 decode and two allocations in front of about twenty integer
operations — the lane would report allocator throughput under a
bulls-and-cows-shaped name.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each. See [BENCHMARKS.md](../../../BENCHMARKS.md) for methodology and caveats.

| | mean | vs C |
|---|---:|---:|
| c (`-O3`) | 94.4 ms | 1.00× |
| rust (`-O`) | 111.1 ms | 1.18× |
| c (`-march=x86-64-v3`, matched ISA) | 111.5 ms | 1.18× |
| rust (`-O -C overflow-checks=on -C target-cpu=x86-64-v3`, matched) | 119.4 ms | 1.26× |
| rust (`-O -C overflow-checks=on`, equal safety) | 123.9 ms | 1.31× |
| **kara** (codegen, seq) | **173.8 ms** | **1.84×** |
| go | 195.8 ms | 2.07× |
| python | 7.015 s | 74.3× |

**Kāra is ahead of Go and 1.46× behind the equal-safety, matched-ISA Rust** —
the fairest single comparison in the table, since Kāra checks integer overflow
by default and targets a baseline ISA. Note that C *loses* 18% when forced to
`-march=x86-64-v3`, which is worth remembering before reading any matched-ISA
row as the "real" number.

### Elsewhere

| | kara | c | rust | go |
|---|---:|---:|---:|---:|
| binary size | 337.5 KiB | 15.7 KiB | 3863.0 KiB | 2178.4 KiB |
| peak RSS | 26.9 MiB | 25.9 MiB | 26.4 MiB | 26.5 MiB |
| compile (cold) | 379 ms | 101 ms | 134 ms | — |

Memory is a four-way tie here — the working set is two 1.6M-element arrays that
every language allocates identically, and unlike
[#298](../298-binary-tree-longest-consecutive-sequence/) there is no refcounted
node to pay for.

## Running it

```bash
karac run   bulls_and_cows.kara
karac build bulls_and_cows.kara && ./bulls_and_cows
karac run   --interp differential.kara
python3     bulls_and_cows.py
KARA_BENCH_INCLUDE_PY=1 BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
