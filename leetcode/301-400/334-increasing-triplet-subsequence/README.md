# 334. Increasing Triplet Subsequence

Given an array `nums`, return whether there are indices `i < j < k` with
`nums[i] < nums[j] < nums[k]`, in `O(n)` time and `O(1)` extra space.

```
[1, 2, 3, 4, 5]     ->  true
[5, 4, 3, 2, 1]     ->  false
[2, 1, 5, 0, 4, 6]  ->  true    (0, 4, 6)
```

## Approaches

Keep `first`, the smallest value so far, and `second`, the smallest value so
far that has a smaller value before it. A value above `second` finishes a
triplet. Lowering `first` below an existing `second` looks wrong but is
safe, because `second` still has its own smaller value earlier in the array.
Two arms spell that out, and two decide the question another way.

| file | mechanism | cost |
|---|---|---|
| `increasing_triplet.kara` ★ | the two thresholds as `Option[i64]`, starting at `None`, with guarded `match` arms | `O(n)` time, `O(1)` space |
| `increasing_triplet_sentinel.kara` | the same thresholds in the usual spelling: both start at `i64.MAX` and every comparison is `<=` | `O(n)` time, `O(1)` space |
| `increasing_triplet_bounds.kara` | a middle element with a smaller value before it and a larger one after it: a suffix-maximum array, then one pass with the prefix minimum | `O(n)` time and space |
| `increasing_triplet_tails.kara` | the general "increasing subsequence of length k" by patience tails, with k = 3 | `O(n · k)` time, `O(k)` space |
| `differential.kara` | the four arms, a brute-force oracle and eight properties on 23,845 arrays | — |
| `bench/increasing_triplet.kara` | 100 scans of a 1,000,000-value array, by the ★ arm | — |

The sentinel arm needs no special case for `i64.MAX` in the input: with `<=`
an equal value replaces a threshold rather than passing it, so `i64.MAX` can
never be above either one. The edge cases check that, along with `i64.MIN`.

Every arm prints the same 23 lines: the three examples, eleven edge cases
(empty, one and two values, three equal values, a plateau, the classic
`[2, 1, 5, 0, 3]` false case where `first` drops below `second`, the
`[5, 1, 6, 0, 7]` true case that needs the old `second`, two more mixed
cases, and the two extreme-value arrays), eight random arrays of 3 to 24
values, and a run of 100,000 values in decreasing pairs, which has no
triplet until one more value is appended. The four arms' output is
byte-identical, and `increasing_triplet.py` mirrors the ★ arm.

## Differential

`differential.kara` checks every array of 0 to 7 values from {0, 1, 2, 3}
(21,845 arrays) against a brute-force oracle that tries every triple of
indices. It then runs eight properties on 2,000 random arrays of 0 to 60
values, with value ranges of 2, 5, 50 and 1,000,000, a tenth of them sorted
descending with one swap so that triplets are rare.

| | property |
|---|---|
| P1 | the four arms agree |
| P2 | the answer equals the brute-force oracle (exhaustive and random) |
| P3 | an increasing subsequence of length 4 implies one of length 3, and one of length 3 implies one of length 2 |
| P4 | reversing the array and negating every value keeps the answer |
| P5 | if the first half has a triplet, the whole array does |
| P6 | an array with an increasing pair gains a triplet when its maximum plus one is appended |
| P7 | `x -> 3x + 7` keeps the answer |
| P8 | the sorted, de-duplicated values have a triplet exactly when there are at least three |

`21845 exhaustive arrays (12182 with a triplet), 2000 random arrays (1300
with a triplet), 0 failures`, on every surface.

## Mutation testing

Fourteen edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: a value equal to `second` finishes a triplet | **killed** | P1, P2, P4 |
| M2 | ★: a value equal to `first` becomes `second` | **killed** | P1, P2, P4 |
| M3 | ★: never lower `first` once it is set | **killed** | P1, P2, P3, P4, P6 |
| M4 | ★: update the thresholds before testing `second` | **killed** | P1, P2, P3, P6, P8 |
| M5 | sentinels: strict comparison against `first` | **killed** | P1 |
| M6 | sentinels: strict comparison against `second` | **killed** | P1 |
| M7 | sentinels: reset `second` when `first` drops | **killed** | P1 |
| M8 | bounds: compare with the suffix maximum that includes the middle | silent (equivalent) | — |
| M9 | bounds: lower the prefix minimum before the check | silent (equivalent) | — |
| M10 | bounds: skip the last middle candidate | **killed** | P1 |
| M11 | tails: replace the first tail at most `x` instead of below it | **killed** | P1, P3, P6 |
| M12 | tails: append instead of replacing | **killed** | P1, P3 |
| M13 | all four arms: allow equal neighbours | **killed** | P2 |
| M14 | oracle: accept non-decreasing triples | **killed** | P2 |

M7 is the tempting "fix" for the case where `first` drops below `second`,
and it is wrong: `[5, 1, 6, 0, 7]` loses its triplet. M8 and M9 are
equivalent. The suffix maximum including the middle, `max(nums[j],
after[j + 1])`, is above `nums[j]` exactly when `after[j + 1]` is. And
lowering the prefix minimum to `nums[j]` first can only make `before <
nums[j]` false in the case where it was already false. M13 breaks every arm
the same way, so P1 cannot see it, and only the oracle catches it.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and all five programs are
valgrind-clean at `-O0` with `KARAC_AUTO_PAR=0`: no bytes lost, and `All
heap blocks were freed` with `KARAC_BUF_CACHE=0`. With the runtime's buffer
cache on, the four arms end with one 1 MiB block "still reachable": the
100,000-value array's buffer, which `karac_free_buf` parks for reuse instead
of returning to libc because it is at least 1 MiB. That is the cache working
as designed, not a leak. The four arms' output is byte-identical to
`increasing_triplet.py`.

## Benchmarks

`bench/increasing_triplet.kara` and its four mirrors time the ★ arm as
written. One array of 1,000,000 values is built once as decreasing pairs,
`t - 1, t`, each pair below the one before, so it has no triplet. Each of 100
punches picks the first slot of a random pair. Half of the punches raise it
above the previous pair's top, which finishes a triplet exactly there, and
the other half leave the array alone, so that solve scans all of it. Then the
slot is put back. The sink is a rolling hash of each answer and position.
The C and Go mirrors carry each threshold as a value and a "set" flag, which
is what `Option[i64]` amounts to.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, karac built
from `main` at `bc22c5fe2` with this thread's unpushed commits (none touches
the code this kernel compiles to), measured 2026-10-03. Python is its own
lane.

| implementation | mean | vs fastest |
|---|---|---|
| **kāra `karac build`** | **83.7 ms ± 4.7** | **1.00×** |
| rust `-O -C overflow-checks=on` (equal-safety) | 85.4 ms ± 2.3 | 1.02× |
| c `clang -O3` | 85.7 ms ± 3.3 | 1.02× |
| rust `-O` | 87.7 ms ± 4.0 | 1.05× |
| c `-march=x86-64-v3` (matched-ISA) | 88.2 ms ± 4.9 | 1.05× |
| go `go build` | 92.1 ms ± 6.9 | 1.10× |
| rust `-C target-cpu=x86-64-v3` (matched) | 99.5 ms ± 3.4 | 1.19× |
| python 3 | 1638.1 ms ± 58.1 | 19.6× |

**Kāra, equal-safety Rust and C are tied within the noise.** Each step is two
compares on values streaming from memory, and the 1,000,000-value array is
8 MB, so the scan is probably bound by memory bandwidth rather than by the
code; that is inferred from the tie, not measured. The matched-ISA Rust row
being slowest has not been looked into.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 71.9 ms ± 2.2 | 15.7 KiB | 9.0 MiB |
| rust | 106.7 ms ± 4.5 | 3863.3 KiB | 9.6 MiB |
| kāra | 300.8 ms ± 15.4 | 350.0 KiB | 10.5 MiB |
| go | — | 2161.7 KiB | 9.6 MiB |
| python | — | — | 46.0 MiB |

`karac build` is 4.2× clang's cold compile and 2.8× rustc's. Kāra's binary is
22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

The benchmark kernel's sink matches all four language twins and Python
(`sink 215681120`).

## Compiler findings

**None.** Every arm was byte-identical on every surface from the first run,
and nothing was lost under valgrind. The one surprise, a 1 MiB block still
reachable at exit, is the runtime's buffer cache (above). `karac check`
reported nothing on any of the five programs. That says little about the
diagnostics: the author already knows the language, which is why authoring
like this never counts toward the machine-fix rate.
