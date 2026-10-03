# 330. Patching Array

Given a sorted array of positive integers `nums` and an integer `n`, add as
few numbers as possible ("patches") so that every integer in `[1, n]` is the
sum of some elements of the array, each element used at most once. Return
the number of patches.

```
nums = [1, 3],      n = 6   ->  1     (patch 2)
nums = [1, 5, 10],  n = 20  ->  2     (patch 2 and 4)
nums = [1, 2, 2],   n = 5   ->  0
```

## Approaches

Keep `miss`, the smallest sum not yet reachable, so that every sum in
`[1, miss)` is. If the next unused number `x` is at most `miss`, taking it
makes every sum in `[1, miss + x)` reachable. If it is larger, nothing left
can ever make `miss`, so a patch is needed, and patching `miss` itself
doubles the range to `[1, 2 * miss)`, further than any other patch reaches.
The three arms take that one greedy step three ways.

| file | mechanism | cost |
|---|---|---|
| `patching_array.kara` ★ | a `while` loop over `miss` with an index into the array | `O(len + log n)` time, `O(1)` space |
| `patching_array_recursive.kara` | one greedy step per call, recursing on the rest | `O(len + log n)` time and stack |
| `patching_array_list.kara` | a `for` over the array that patches before each number it cannot use yet, returning the patches themselves | `O(len + log n)` time, `O(log n)` space |
| `differential.kara` | the three arms, a brute-force minimality check and eight properties on 908 cases | — |
| `bench/patching_array.kara` | 1,500 queries against one array of 100,000 values, by the ★ arm | — |

Every arm prints the same 17 lines: the three examples, nine edge cases (an
empty array with `n` = 1, 8 and 2³¹ − 1, `[1]` and `[2]` with `n = 1`, the
classic `[1, 2, 31, 33]` with `n` = 2³¹ − 1, eight ones, `[5, 6, 7]`, and one
number larger than `n`), four random arrays, and one of 1,000 values with
`n` = 2³¹ − 1. The three arms' output is byte-identical, and
`patching_array.py` mirrors the ★ arm.

`miss` never exceeds `2n`, so the arms are exact for any `n` below 2⁶² and
trap on overflow beyond that rather than wrapping.

## Differential

`differential.kara` checks 108 hand-picked cases (nine arrays, each with `n`
from 1 to 12), 600 random small cases (up to 6 values in `[1, 16]`, `n` up to
14), which it also brute-forces, and 200 random large cases (up to 39 values
in `[1, 100000]`, `n` up to about 2.1 million), checked by the properties alone.

| | property |
|---|---|
| P1 | the three arms agree |
| P2 | the list arm's patches, added to `nums`, cover every sum in `[1, n]` (small cases) |
| P3 | no multiset of `answer - 1` patches covers `[1, n]` (small cases) |
| P4 | the answer never exceeds the answer for an empty array |
| P5 | the answer is non-decreasing in `n` |
| P6 | adding a number to `nums` never raises the answer |
| P7 | `nums` plus its own patches needs no further patch |
| P8 | the patches are strictly increasing and each is at most `n` |

P2 and P3 are the oracle: together they say the greedy's answer is both
achievable and optimal. Coverage is a subset-sum table, and P3 tries every
multiset of `answer - 1` values from `[1, n]`, which is enough because a set
of patches that covers `[1, n]` still covers it with one more patch added.

`908 cases (585 of 600 small random ones need a patch), 0 failures`, on
every surface.

## Mutation testing

Fourteen edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: take a number only when strictly below `miss` | **killed** | P1, P3, P7 |
| M2 | ★: loop while `miss < n` | **killed** | P1 |
| M3 | ★: a patch adds 1 instead of `miss` | **killed** | P1, P3 |
| M4 | ★: a patch adds `miss + 1` | **killed** | P1 |
| M5 | ★: start `miss` at 0 | **killed** | never terminates: `miss += miss` stays 0 |
| M6 | ★: start `miss` at 2 | **killed** | P1 |
| M7 | ★: skip the next number after patching | **killed** | P1, P3 |
| M8 | recursive: take a number only when strictly below `miss` | **killed** | P1 |
| M9 | recursive: stop when `miss >= n` | **killed** | P1 |
| M10 | list: patch while `x >= miss` | **killed** | P1 |
| M11 | list: no early `break` once `[1, n]` is covered | silent (equivalent) | — |
| M12 | list: patch `miss + 1` | **killed** | P1, P2, P7, P8 |
| M13 | all three arms: take a number only when strictly below `miss` | **killed** | P3, P7 |
| M14 | all three arms: patch `miss + 1` | **killed** | P2, P7, P8 |

M11 is equivalent: once `miss > n` the trailing `while` patches nothing, and
taking further numbers only grows `miss`. M13 and M14 break every arm the
same way, so P1 cannot see them, and they are what shows the oracle has
teeth: M13 answers too high and only the brute force (P3) and P7 notice; M14
patches the wrong numbers and the coverage table (P2) catches it.

## Verification

All three arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and all four programs are
valgrind-clean (`All heap blocks were freed`) at `-O0` with
`KARAC_AUTO_PAR=0`. The three arms' output is byte-identical to
`patching_array.py`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 767665033`).

## Benchmarks

`bench/patching_array.kara` and its four mirrors time the ★ arm as written.
One sorted array of 100,000 values in `[50, 1050]` is built once. Each of
1,500 punches picks `n` in `[1, 2 * sum]` and counts the patches with the
greedy, so every query walks most of the array. The sink is a rolling hash
of each answer and `n`.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, on a 4-core x86-64 Linux container, karac built from `main`
at `2fec9c7c5` with the interpreter change for B-2026-10-03-1 applied (it
does not touch codegen), measured 2026-10-03. Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O` | 85.3 ms ± 7.6 | 1.00× |
| c `clang -O3` | 91.0 ms ± 11.3 | 1.07× |
| c `-march=x86-64-v3` (matched-ISA) | 101.5 ms ± 22.6 | 1.19× |
| **kāra `karac build`** | **109.2 ms ± 4.4** | **1.28×** |
| rust `-O -C overflow-checks=on` (equal-safety) | 118.8 ms ± 6.2 | 1.39× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 119.7 ms ± 9.2 | 1.40× |
| go `go build` | 127.4 ms ± 4.5 | 1.49× |
| python 3 | 5933 ms ± 210 | 69.6× |

**Kāra is 8% ahead of equal-safety Rust and 20% behind C.** The kernel is
one add and one compare per element, and both Kāra and checked Rust spend
an overflow check on each `miss += x`. The C rows are noisy on this host (the
matched-ISA row ranged 88 to 166 ms), so the order of the two C rows is not
meaningful. Where the 28% to unchecked Rust goes has not been measured.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 68.2 ms ± 2.5 | 15.9 KiB | 2.8 MiB |
| rust | 167.0 ms ± 4.3 | 3869.8 KiB | 3.5 MiB |
| kāra | 295.9 ms ± 9.7 | 358.0 KiB | 3.2 MiB |
| go | — | 2191.1 KiB | 2.5 MiB |
| python | — | — | 11.4 MiB |

`karac build` is 4.3× clang's cold compile and 1.8× rustc's. Kāra's binary is
23× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**No wrong answers from a finished program**, and every arm was
byte-identical on every surface from the first run. Writing the harness found
one output bug in auto-par builds, one codegen gap and one slowdown:

- **B-2026-10-03-2 (run-vs-build, medium, fixed in `21be9bcc1`): a panic in
  an auto-parallelised statement group lost the output before it.** While
  the harness still had a case that overflowed, the default `karac build`
  printed the panic and nothing else, where `KARAC_AUTO_PAR=0`, the JIT and
  `--interp` printed every line before the failing call first. Each branch
  of an auto-par group writes into a capture that only the group's join
  replays, and a Kāra panic exits the process from inside the branch, so the
  join never ran. When a later branch panicked faster than an earlier one,
  the later panic was the one reported, one the sequential program never
  reaches. The panic path now waits for the earlier branches, replays their
  output and its own, and defers to an earlier panic.
- **B-2026-10-03-3 (run-vs-build, medium, open): a stored iterator cannot be
  pulled by hand under `karac build` or `karac run`.** The natural cursor
  spelling of the greedy, `let mut it = nums.iter().peekable()` with
  `it.peek()` and `it.next()`, type-checks and runs under `--interp`, but
  codegen refuses `next()` on a bound iterator and has no handler for a
  bound `peekable()`. It is the one way of writing this kata that does not
  build, so no arm uses it; an arm will be added when the gap closes.
- **B-2026-10-03-1 (perf, low, fixed in `671a33989`): `--interp` sent every
  arithmetic operator through the general call path.** `a + b` is lowered
  to `i64.add(a, b)`, and each one resolved its callee, analysed argument
  modes and consulted per-call memos before reaching the operator, while
  every scope lookup paid for SipHash. Operator calls now dispatch directly
  and scopes use a faster hash: 17% fewer instructions on a scalar loop, and
  the differential takes 12.9 s under `--interp` instead of 13.5 s. The
  larger cost the same profile found, in the drop-schedule audit's parameter
  memo, was fixed by that work in `e9591b6a1`.

`karac check` flagged a `mut` marker on an argument that was already `mut
ref` in the ★ arm's harness (E0219), and `karac fix` removed it. That says little about the
diagnostics: the author already knows the language, which is why authoring
like this never counts toward the machine-fix rate.
