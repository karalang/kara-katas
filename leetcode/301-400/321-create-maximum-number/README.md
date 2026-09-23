# 321. Create Maximum Number

Two arrays of digits, `nums1` (length `m`) and `nums2` (length `n`), and a
length `k <= m + n`. Build the largest `k`-digit number whose digits come from
the two arrays, keeping each array's digits in their original relative order.

```
nums1 = [3, 4, 6, 5]   nums2 = [9, 1, 2, 5, 8, 3]   k = 5  ->  [9, 8, 6, 5, 3]
nums1 = [6, 7]         nums2 = [6, 0, 4]            k = 5  ->  [6, 7, 6, 0, 4]
nums1 = [3, 9]         nums2 = [8, 9]               k = 3  ->  [9, 8, 9]
```

It reads like one search over interleavings, but it is really three small
problems stacked on top of each other, and each one is easy on its own:

1. **Split.** Some number `i` of the answer's digits came from `nums1` and the
   other `k - i` from `nums2`. Try every feasible `i`.
2. **Shrink.** For a fixed `i`, the digits taken from `nums1` should be the
   largest length-`i` subsequence of `nums1`. Whatever the merge does next, a
   larger subsequence can only produce a larger merge. That is a monotonic
   stack with a budget of `m - i` pops.
3. **Merge.** Interleave the two kept subsequences into the largest sequence:
   take the larger head, and when the heads are equal, take from the side whose
   **whole remaining suffix** is larger.

Step 3's tie rule is the one line of the problem that has to be right. In the
second example both heads are 6. Taking `nums2`'s 6 first gives
`6 6 7 0 4`, and taking `nums1`'s 6 first lets the 7 through next, giving
`6 7 6 0 4`. Looking one digit past the tie doesn't settle it either, because
the suffixes can agree for many positions before they differ.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `create_max_number.kara` ★ | every split, shrink each side by stack, merge on suffixes | `O(k (m + n + k²))` worst |
| `create_max_number_dp.kara` | `best(i, j, l)` over every suffix pair and length | `O(m n k²)` |
| `create_max_number_frontier.kara` | one digit at a time, keeping every state that ties | `O(k m n (m + n))` worst |
| `create_max_number_brute.kara` | every subsequence pair, every interleaving | `Σᵢ C(m,i) C(n,k−i) C(k,i)` |
| `differential.kara` | four arms, thirteen properties | — |
| `bench/create_max_number.kara` | 24 passes × three `k` over 1500- and 1700-digit arrays | — |

All four arms print the same twelve fixed cases and three small random ones.
The ★ arm also prints three large random cases (up to `m = 150`), which only
it and the Python mirror can finish quickly.

## Four ways to find the largest number

**★ Split, shrink, merge.** This is the decomposition above. Each split runs two
stack shrinks and one merge. The merge's suffix compare is `O(k)` in the worst
case (long runs of equal digits), so a split costs up to `O(k²)`. On random
digits the compare usually stops within a digit or two, and a split costs
closer to `O(m + n)`. The best merge over all splits is the answer.

The stack has one trap, and the mutation table below found it on me. The pop
condition is `top < incoming`, strictly less. Popping an **equal** top looks
harmless, since the stack ends up holding the same digit, but it spends one
of the `m - i` drops for nothing. With `[5, 5, 1, 9]` and `keep = 3` there is
one drop to spend. Spent on the second 5, it leaves nothing to remove the 1,
and the result is `5 1 9` where it should be `5 5 9`.

**Dynamic programming.** This arm never learns that the problem splits. It
asks one question for every suffix pair and every length:
`best(i, j, l)` is the largest length-`l` sequence that `nums1[i..]` and
`nums2[j..]` can produce. The first digit of that sequence is `nums1[i]`,
`nums2[j]`, or neither, and "neither" means one of the two heads is skipped:

```
best(i, j, l) = max of   nums1[i] :: best(i+1, j, l-1)      nums2[j] :: best(i, j+1, l-1)
                         best(i+1, j, l)                    best(i, j+1, l)
```

The max is taken over the options that are feasible, where `(m-i) + (n-j) >= l`.
Nothing in it is greedy, and that is why it is here. The ★ arm makes three
claims: every split is tried, the largest subsequence is always the right one
to merge, and the tie rule picks the right side. This arm can contradict any
of them. The table is filled one length at a time and only two layers are kept.

**Frontier.** This one builds the answer left to right and asks only "what is
the largest digit that can go here?". The hard part is that the largest digit
may be available in more than one way, and *which* 6 was taken decides whether
the 7 is reachable next. The ★ arm settles that in advance with a suffix
compare. This arm doesn't settle it at all. It keeps **every** state `(i, j)`
that produces the best prefix so far, and moves them all forward together.
Ties are never broken by a rule. They survive until the arrays themselves tell
them apart. The one pruning step takes the *first* feasible occurrence of a
digit on each side. That is safe: a later occurrence of the same digit gives
the same prefix and leaves strictly fewer options.

**Brute force.** This arm does what the statement says and nothing else. For
every split it enumerates every subsequence of each side, and for every pair it
enumerates every interleaving, keeping the largest. There is no stack, no
suffix compare, no feasibility argument and no dominance argument, which makes
it the oracle. It is also only ever run where the leaf count is in the
millions, not beyond.

## Differential

`karac run differential.kara` has three tiers:

- Every `(m, n)` up to 5 × 5, in four radixes (all zeros, two digits, three
  digits, all ten), at every `k` from 0 to `m + n`. The brute force joins in
  wherever `m + n <= 8`.
- Six hand-picked tie cases whose equal heads have suffixes that agree for a
  while.
- 24 random cases up to 12 × 12.

```
cases 952 brute-cases 763 samples 15232 relabel-cases 680
DIFFERENTIAL OK
```

| # | property |
|---|---|
| P1 | the DP arm agrees with the ★ arm |
| P2 | the frontier arm agrees with the ★ arm |
| P3 | the brute force agrees with the ★ arm (where `m + n <= 8`) |
| P4 | the answer has exactly `k` digits, each `0..9` |
| P5 | the answer is **realizable**: an interleaving of a subsequence of `nums1` and a subsequence of `nums2` |
| P6 | no randomly sampled realizable sequence beats it (16 per case) |
| P7 | swapping the two arrays does not change it |
| P8 | appending a digit (0, 9, or random) to either array never makes it smaller |
| P9 | its first digit is the largest digit that can lead a `k`-digit answer |
| P10 | at `k = m + n` it uses every digit exactly once (same multiset) |
| P11 | the order-preserving relabel `d → 2d + 1` commutes with it |
| P12 | it is a fixed point: `max(answer, [], k) == answer` |
| P13 | no one-digit deletion of the `(k+1)`-answer beats the `k`-answer |

P5 and P6 are the two that check the answer rather than an arm. P5 says the
answer was legally **built**. An arm that invents a digit, reorders an array,
or reuses a position fails it, however large its answer is. P6 checks the
other half. It samples the statement's own search space (a random split, a
random subsequence of each side, a random interleaving) and asks whether
anything in it beats the answer. It keeps working at sizes the brute force
can't reach. "Legal" and "not beaten" together are the whole definition of
the problem. P13 connects different `k` to each other: deleting any digit of
the `(k+1)`-answer gives a legal `k`-digit sequence, so none of those
deletions may beat the `k`-answer.

The sizes are set by the tree-walk interpreter, not by the JIT. The whole
harness takes 0.7 s under `karac run` and about 1 min 45 s under
`karac run --interp`. The first cut, with twice the draws, 2.5× the P6
samples, a larger medium tier and the brute force on every small case, took
just over six minutes there.

## Mutation testing

Sixteen content-anchored edits to `differential.kara`, each run through the
full harness under `karac run`. A panic or hang counts as a kill alongside
`DIFFERENTIAL FAILED`.

| # | mutation | predicted | outcome | properties that fired |
|---|---|---|---|---|
| M1 | the ★ stack also pops on an **equal** top (`<` → `<=`) | *silent* | **killed** | P1, P2, P3, P6, P8, P13 |
| M2 | the ★ stack pops without spending its drop budget | kill | **killed** | P1, P2, P3, P4, P9, P12 |
| M3 | the ★ stack never trims its tail back to `keep` | kill | **killed** | P1, P2, P3, P4, P12, P13 |
| M4 | a proper prefix counts as *larger* in the merge compare | kill | **killed** | panic (index past the end in `merge`) |
| M5 | the merge breaks ties on the next digit, not the whole suffix | kill | **killed** | P1, P2, P3, P6, P7 |
| M6 | the split range forgets `k - i <= n` | kill | **killed** | P1, P2, P3, P4, P7, P9, P10, P12, P13 |
| M7 | the last split is never tried | kill | **killed** | panic (P9 reads `ans[0]` of an empty answer) |
| M8 | the split loop keeps the *smaller* candidate | kill | **killed** | P1, P2, P3, P6, P8, P9, P13 |
| M9 | the DP drops its two "skip a head" transitions | kill | **killed** | P1 |
| M10 | the DP's feasibility test is off by one | kill | **killed** | P1 |
| M11 | the frontier's lookahead demands one digit too many | kill | **killed** | P2 |
| M12 | the frontier never clears its dedupe grid between steps | kill | *silent* | — |
| M13 | the frontier never considers digit 0 | kill | **killed** | P2 |
| M14 | the brute force only takes `nums2` once `nums1` is exhausted | kill | **killed** | P3 |
| M15 | the merge compare's final `>` becomes `>=` | *silent* | silent | — |
| M16 | P6's selection sampling uses `<=` instead of `<` | *silent* | silent | — |

**13 killed, 3 silent, and two predictions wrong.**

M1 is the one worth reading. I predicted it silent, reasoning that popping an
equal digit and pushing it back leaves the stack unchanged. The stack contents
are unchanged, but the budget isn't. The worked example is in the ★ section
above, and it is now called out there because the mutant found it. It is the
same trap as "Remove K Digits" (#402), and it is invisible on any input
without a repeated digit.

M12 I predicted would die: a dedupe grid that is never cleared should drop a
state the second time it is reached. It stayed silent. A 300,000-case offline
run (a Python transcription of the frontier arm, with and without the reset,
against the ★ arm on random inputs up to 9 × 9) found no input where the
missing reset changes the answer. So it is most likely an equivalent mutant.
A state that recurs at a later step would already be dominated by the state it
came from. That is not proved here, and the reset stays, because it is what
makes the arm obviously correct rather than correct by an argument nobody
wrote down.

M15 and M16 are genuine equivalents. After the compare loop exits with both
sides remaining, the two digits are known to differ, so `>` and `>=` agree.
Selection sampling picks exactly `want` elements whichever comparison it uses,
because it is forced to take every remaining element once the remainder equals
what is still needed. Only the distribution changes, and P6 needs legality,
not uniformity.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. `scripts/surface-sweep.py --filter
321-create` reports `5 programs · 5 clean · 0 DIVERGENCES`. The ★ arm's full
output, including the three large folds, is byte-identical to
`create_max_number.py`.

The benchmark kernel is verified on JIT, AOT-sequential and AOT-auto-par, and
its sink matches all four language twins (`sink 618358101 digits 125100`). It
is not run under `--interp`, because at 24 passes the tree-walk backend would
take far too long. The kata's semantics are covered by the arms and the
differential, which do run on every backend.

## Benchmarks

`bench/create_max_number.kara` and its four mirrors run 24 passes. Each pass
draws two fresh digit arrays (1500 and 1700 digits) from an LCG and answers
three `k`: 500, 1600, and `m + n - 7(p + 1)`, which is nearly the whole input.
For each `k` every feasible split runs two monotonic-stack shrinks and one
suffix-compare merge: 501 splits for `k = 500`, 1501 for `k = 1600`, and
between 8 and 169 for the near-total `k`, which comes to about 50,000 splits
per run. Every digit of every answer is folded into a rolling hash.

The stacks, the merge output and the running best all live in buffers
allocated once, with explicit lengths, in every mirror. So the five mirrors
measure the same stack and merge work, not five allocator policies. The
shrink writes into a fixed-length buffer, so it spends a drop on a digit that
arrives while the buffer is full. That is equivalent to the ★ arm's
push-then-trim, and every mirror does it the same way.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`, the file
> `scripts/consolidate-bench.sh` feeds into the top-level chart) is not
> measured yet, and `bench-lib.sh` refuses to write it from Linux. Absolute
> milliseconds are NOT comparable between hosts. Only the **within-file
> cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.shallow+gca1b99e66`, measured 2026-09-23. Python is its own lane at
3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `-march=x86-64-v3` (matched-ISA) | 720.8 ms ± 11.9 | 1.00× |
| c `clang -O3` | 759.1 ms ± 17.6 | 1.05× |
| rust `-O` | 912.0 ms ± 13.4 | 1.27× |
| **kāra `karac build`** | **956.0 ms ± 10.9** | **1.33×** |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 966.6 ms ± 18.8 | 1.34× |
| rust `-O -C overflow-checks=on` (equal-safety) | 1013.5 ms ± 16.6 | 1.41× |
| go `go build` | 1119.5 ms ± 17.1 | 1.55× |
| python 3 | 34090 ms ± 111 | 47.3× |

**Kāra is 1.26× behind `clang -O3` and 4.8% behind unchecked `rustc -O`. At
equal safety it is 5.7% ahead of Rust.** On this kata the equal-safety
comparison measures something real. The merge's inner loop, the stack's pop
loop and the rolling hash are all integer arithmetic on indices and digits,
so Rust's overflow checks cost it 11% here (912.0 → 1013.5 ms). Kāra checks
the same arithmetic by default and lands between Rust's two builds. The
matched-ISA twins barely move: C gains 5% from `x86-64-v3`, and the checked
Rust gains 4.6%. The work is branchy compares, not something that vectorises.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 118.1 ms ± 2.6 | 15.8 KiB | 1.66 MiB |
| rust | 201.0 ms ± 2.0 | 3865.7 KiB | 2.38 MiB |
| kāra | 380.0 ms ± 11.3 | 341.6 KiB | 2.48 MiB |
| go | — | 2180.0 KiB | 1.77 MiB |
| python | — | — | 8.07 MiB |

`karac build` is 3.2× clang's cold compile and 1.9× rustc's. Its binary is 22×
clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**One filed and since fixed: [`B-2026-09-23-2`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)
— a `ref`/`mut ref` bool or numeric scalar was refused as an `if` or `while`
condition, as the operand of unary `not` or `-`, and as either operand of
`and`/`or`.** The brute-force arm carries its running maximum through the
recursive interleaving walk as `best: mut ref Vec[i64], have: mut ref bool`,
and reads `if not have or greater(cur, best)`. `karac check` refused it with
`E0209 unary 'not' requires 'bool', found 'mut ref bool'`. Probing every
position showed the same scalar was accepted in `==`, arithmetic, casts,
annotated lets and arguments, and refused in exactly the five positions above,
so `if flag == true` compiled and `if flag` did not. kara `42a9f2c` had made
ref scalars "read as their value type in every value position", and these five
were missed. All surfaces refused alike, so nothing diverged.

kara `6a9665a18` fixed it, along with the bitwise operators, unary `~` and match
guards, which had the same gap. The brute arm has its `have` flag back. While
the row was open it seeded the maximum with `k` copies of `-1` instead.

The only other diagnostics were two `E0001`s in the benchmark kernel, and those
are a language rule, not a gap: single-letter constants `M` and `N` are
Type-class names, so the kernel uses `LEN1` and `LEN2` (in every mirror, for
parity). No `KARAC_AUTO_PAR=0`-only pass, and nothing else contorted.
