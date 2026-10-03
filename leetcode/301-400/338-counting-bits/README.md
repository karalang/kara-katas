# 338. Counting Bits

Given `n`, return a list of `n + 1` numbers whose `i`-th entry is the number
of 1 bits in `i`.

```
2  ->  [0, 1, 1]
5  ->  [0, 1, 1, 2, 1, 2]
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `counting_bits.kara` ★ | `i >> 1` drops the lowest bit of `i` and is already counted, so `ans[i] = ans[i >> 1] + (i & 1)` | `O(n)` |
| `counting_bits_lowbit.kara` | `i & (i - 1)` clears the lowest 1 bit of `i` and is already counted, so `ans[i] = ans[i & (i - 1)] + 1` | `O(n)` |
| `counting_bits_builtin.kara` | each number on its own with `count_ones`, which lowers to the processor's population count | `O(n)` |
| `counting_bits_kernighan.kara` | each number on its own with Kernighan's loop, which clears the lowest 1 bit until none is left, collected from a `map` over `0..=n` | `O(n log n)` |
| `differential.kara` | the four arms, a bit-by-bit oracle and eight properties | — |
| `bench/counting_bits.kara` | 300 solves for `n` near 1,000,000, by the ★ arm | — |

Every arm prints the same 12 lines: the two examples, `n` = 0, 1, 16, 31 and
33 in full, and a summary (length, total, largest count and a hash of every
entry) for `n` = 1,000, 65,535, 65,536, 100,000 and 1,048,575. The four arms'
output is byte-identical, and `counting_bits.py` mirrors the ★ arm.

## Differential

`differential.kara` compares the four arms with an oracle that tests each of
a number's bits in turn, for every `n` from 0 to 300 and for `n` = 4,096 and
65,536, then checks properties on the answer for 65,536.

| | property |
|---|---|
| P1 | the four arms agree |
| P2 | they equal the oracle |
| P3 | the answer has `n + 1` entries, each between 0 and 63 |
| P4 | the answer for `n` is the start of the answer for any larger `n` |
| P5 | doubling a number keeps its count, and doubling it and adding one adds one |
| P6 | `2^k` has one bit, `2^k - 1` has `k`, and the counts below `2^k` add up to `k * 2^(k-1)`, for `k` up to 16 |
| P7 | a sum has at most as many bits as its two parts together, on 5,000 random pairs |
| P8 | `i ^ j` has the bits of `i` and of `j` minus twice the bits they share, on the same pairs |

`303 values of n checked (counts sum to 713575)`, `5000 random pairs, 0
failures`, on every surface.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each run with every
failure printed rather than the first ten.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: adds the lowest bit of `i - 1` | **killed** | P1, P2, P5, P6, P7, P8 |
| M2 | ★: shifts by two | **killed** | P1, P2, P5, P6, P7 |
| M3 | ★: the loop stops one short | **killed** | P1, P2, P4, P5, P6 |
| M4 | lowbit: clears the lowest bit of `i + 1` | **killed** | P1 |
| M5 | lowbit: starts at 0, so 0 counts one bit | **killed** | P1 |
| M6 | builtin: counts zeros | **killed** | P1 |
| M7 | builtin: the range leaves out `n` | **killed** | P1 |
| M8 | kernighan: stops while one bit is left | **killed** | P1 |
| M9 | kernighan: counts one fewer when the two lowest bits are set | **killed** | P1 |
| M10 | oracle: skips bit 0 | **killed** | P2 |
| M11 | oracle: skips bit 62 | silent (unreachable) | — |
| M12 | oracle: counts only a clear lowest bit | **killed** | P2 |

M11 is silent because no number the differential tries reaches bit 62; it is
not equivalent in general, but LeetCode's `n` is at most 100,000. A first
version of M8, clearing with `x & (x + 1)`, never terminates (2 maps to 2),
so it was replaced. P1 catches everything the non-★ mutations do, because
each arm is compared against the ★ arm's answer first.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and all five programs are
valgrind-clean at `-O0` with `KARAC_AUTO_PAR=0` and `KARAC_BUF_CACHE=0`
(`All heap blocks were freed`, no errors). The four arms' output is
byte-identical to `counting_bits.py`.

With a release karac the arms take 0.2 to 0.3 s on the JIT. Under `--interp`
the three linear arms take about 5.2 s and the differential 7.8 s; the
Kernighan arm takes 34 s, since it runs an inner loop and a closure call for
every number. That is most likely the interpreter's per-call cost, filed from
kata 336 as B-2026-10-03-21 (inferred, not profiled here).

## Benchmarks

`bench/counting_bits.kara` and its four mirrors time the ★ arm as written.
Round `r` of 300 solves for `n = 1,000,000 - r`, so each answer is a fresh
8 MB `Vec`. Three of its entries and its length are folded into a rolling
hash, which is the sink.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, measured
2026-10-03. karac was built from `main` at `8995731ee` with this thread's
fixes for B-2026-10-03-23, -24 and -25 (none touches this kernel), and linked
against a runtime carrying the B-2026-10-03-48 fix (see Compiler findings).
Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| c `-march=x86-64-v3` (matched-ISA) | 234.5 ms ± 8.1 | 1.00× |
| c `clang -O3` | 245.0 ms ± 10.3 | 1.04× |
| **kāra `karac build`** | **349.1 ms ± 24.0** | **1.49×** |
| rust `-O` | 456.0 ms ± 16.1 | 1.94× |
| go `go build` | 493.1 ms ± 16.9 | 2.10× |
| rust `-O -C overflow-checks=on` (equal-safety) | 526.7 ms ± 11.5 | 2.25× |
| rust `-C target-cpu=x86-64-v3` (matched) | 526.6 ms ± 10.4 | 2.25× |
| python 3 | 13719 ms ± 158 | 58.5× |

Kāra is 34% faster than equal-safety Rust here and 1.4× behind C. Why Rust
trails was not profiled. Before the B-2026-10-03-48 fix the same Kāra binary
took 950 ms, two-thirds of it in the kernel.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 83.7 ms ± 6.1 | 15.7 KiB | 9.2 MiB |
| rust | 121.2 ms ± 5.4 | 3862.5 KiB | 9.8 MiB |
| kāra | 301.8 ms ± 10.4 | 337.6 KiB | 10.1 MiB |
| go | — | 2161.8 KiB | 17.6 MiB |
| python | — | — | 22.9 MiB |

`karac build` is 3.6× clang's cold compile and 2.5× rustc's. Kāra's binary is
21× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

The benchmark kernel's sink matches all four language twins and Python
(`sink 679242184`).

## Compiler findings

- **B-2026-10-03-48 (perf, medium): a large `Vec` built and dropped in a loop
  re-faulted all its pages every round.** The bench first measured 950 ms
  against equal-safety Rust's 517 ms, with 643 ms of it system time, and
  `strace` showed an `mmap` and `munmap` per round. Two runtime causes. The
  runtime's glibc tuning pinned the mmap threshold at 1 MiB, which also turns
  off glibc's dynamic threshold, so every block from 1 to 32 MiB was mapped and
  unmapped for the life of the program. Separately, the `vec![0; n]` path never
  reused the buffers the runtime parks on free, so two 8 MB buffers sat unused
  and peak memory was 25 MiB. Fixed in the kara repo: the bench went to about
  0.35 s and 10 MiB.
- **B-2026-10-03-47 (miscompile, medium): under `--interp`, a method call
  inside an f-string could read another hole's type.** Found probing
  `count_ones`, `leading_zeros` and `trailing_zeros` across integer widths:
  an `i64`'s `leading_zeros()` printed inside an f-string came out as the
  `i32` answer when an `i32` call appeared later in the file. Every compiled
  surface was right. Fixed in the kara repo. The kata's arms never call a bit
  method inside an f-string, so they were not affected.
- **B-2026-10-03-21 (perf, low, open)**, filed from kata 336: the
  interpreter's per-call cost, which is probably most of the Kernighan arm's
  34 s under `--interp` (inferred, not profiled).

`karac check` reported no diagnostics on any arm. `karac fix` made four
machine-applicable fixes in `differential.kara`, each turning a `!` into
`not`. That says little about the diagnostics overall: the author already
knows the language, which is why authoring like this never counts toward the
machine-fix rate.
