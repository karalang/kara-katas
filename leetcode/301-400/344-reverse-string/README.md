# 344. Reverse String

Write a function that reverses a string given as an array of characters. Do
it in place, with `O(1)` extra memory.

```
['h','e','l','l','o']      ->  ['o','l','l','e','h']
['H','a','n','n','a','h']  ->  ['h','a','n','n','a','H']
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `reverse_string.kara` ★ | two indices walking toward each other, swapping through a temporary | `O(n)` time, `O(1)` space |
| `reverse_string_swap.kara` | `s.swap(k, n - 1 - k)` over the first half | `O(n)` time, `O(1)` space |
| `reverse_string_builtin.kara` | the slice's own `s.reverse()` | `O(n)` time, `O(1)` space |
| `reverse_string_recursive.kara` | swap the outer pair, recurse on what lies between | `O(n)` time, `O(n)` stack |
| `reverse_string_tuple.kara` | the two-index walk, swapping with `s[i], s[j] = s[j], s[i]` | `O(n)` time, `O(1)` space |
| `differential.kara` | the five arms and a copy-from-the-back oracle on every length `0..300`, five properties | — |
| `bench/reverse_string.kara` | 4,000 punches, each reversing 200,000 characters in place, by the ★ arm | — |

Every arm prints the same 10 lines: the two examples, the edge lengths 0, 1
and 2, a palindrome, three strings with non-ASCII characters, and a
100,000-letter string reversed twice. A Kāra `char` is one Unicode code
point, so `"añb€c🦀d"` reverses code point by code point to `"d🦀c€bña"`.
That is what LeetCode's `char[]` input means; reversing a string's grapheme
clusters, so that a combining accent stays on its letter, is a different and
harder problem. `reverse_string.py` mirrors the ★ arm and its output is
byte-identical.

The function takes `s: mut Slice[char]`, the in-place borrow, and the caller
passes its `Vec[char]` as `mut s`. The recursive arm recurses 50,000 deep on
the long case and runs on every surface; the problem's `O(1)` bound is the
loop arms'.

## Differential

`differential.kara` runs all five arms on every length in `0..300`, each
filled pseudo-randomly from an alphabet that mixes one-, two-, three- and
four-byte code points, and compares them with a sixth version that builds a
new `Vec` from the last element down.

| | property |
|---|---|
| P1 | all five arms equal the copy |
| P2 | reversing twice gives the input back |
| P3 | element `k` of the result is element `n - 1 - k` of the input |
| P4 | `rev(a ++ b) == rev(b) ++ rev(a)`, splitting each input in the middle |
| P5 | `s ++ rev(s)` is a palindrome, so reversing it changes nothing |

`failures 0` and all properties hold on every surface, with checksum
18813595.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each run under
`karac run`. All twelve are killed.

| # | mutation | how |
|---|---|---|
| M1 | two-index: return early below length 3, not 2 | P1 at length 2 only, 1 failure |
| M2 | two-index: `j -= 2` | P1, 297 failures |
| M3 | two-index: `s[j] = s[i]` instead of the temporary | P1 and P2, 598 failures |
| M4 | swap: stop at `n / 2 - 1` | P1, 568 failures |
| M5 | swap: partner `n - k - 2` | P1, 598 failures |
| M6 | recursion: shrink `hi` by 0 | P1, 298 failures |
| M7 | recursion: start at `n - 2` | P1, 299 failures |
| M8 | tuple: `s[i], s[j] = s[j], s[j]` | P1, 299 failures |
| M9 | oracle: stop at `k > 0` | index out of bounds in P3 |
| M10 | builtin: `s.sort()` | P1, 596 failures |
| M11 | tuple: `i += 2` | P1, 595 failures |
| M12 | two-index: `while i + 1 < j` | P1, 141 failures |

M1 is the boundary case: only a two-character input tells it apart, which is
why the differential starts at length 0 rather than at a length that looks
interesting.

## Verification

All five arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py`, 6
programs, 0 divergences). Built with `KARAC_AUTO_PAR=0`, the ★, tuple and
recursive arms and the differential are valgrind-clean (`0 errors`). The
default auto-par builds of the three arms report one "possibly lost" record
of 1,216 bytes, the thread-local storage of worker threads still alive at
exit, and no lost or invalid access.

The benchmark kernel's sink matches all four language twins and Python
(`sink 258295624`). `karac run --interp` was not run on the kernel: at 400
million swaps it would take tens of minutes.

## Benchmarks

`bench/reverse_string.kara` and its four mirrors time the ★ arm as written.
200,000 characters are drawn once from a 32-letter alphabet, half ASCII and
half Greek. Each of 4,000 punches replaces one character at a random
position, reverses the whole array in place, and reads one character back at
another random position, which is folded into a rolling hash, the sink. The
read position is drawn after the reversal, so no compiler can skip one.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10448+g76727438c`, measured 2026-10-05, with the timed lane built
with `KARAC_AUTO_PAR=0`. Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O` | 78.2 ms ± 2.4 | 1.00× |
| rust `-O -C overflow-checks=on` (equal-safety) | 80.0 ms ± 6.8 | 1.02× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 90.3 ms ± 9.8 | 1.15× |
| c `clang -O3` | 321.9 ms ± 9.2 | 4.12× |
| **kāra `karac build`** | **322.8 ms ± 11.5** | **4.13×** |
| c `-march=x86-64-v3` (matched-ISA) | 329.5 ms ± 35.9 | 4.21× |
| go `go build` | 333.4 ms ± 15.2 | 4.26× |
| python 3 | 21497 ms ± 529 | 275× |

**Kāra ties C and Go, and all three are 4× behind Rust.** The gap is
vectorization, not safety: the Rust binary reverses four characters per step
(`movdqu` loads, `pshufd $0x1b` to reverse the lanes, `movdqu` stores), and
executes 0.80 billion instructions to C's 3.60 billion (valgrind
`--tool=lackey`). C and Kāra run the scalar loop the source spells. rustc
here carries LLVM 21; clang and karac carry LLVM 18. That the newer
vectorizer is what recognises the converging two-index swap is an inference
from that difference, not something measured by building the C with a newer
clang.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 88.6 ms ± 2.4 | 15.7 KiB | 2.2 MiB |
| rust | 133.0 ms ± 4.2 | 3863.3 KiB | 2.9 MiB |
| kāra | 333.1 ms ± 13.0 | 337.4 KiB | 3.1 MiB |
| go | — | 2178.8 KiB | 5.8 MiB |
| python | — | — | 17.0 MiB |

`karac build` is 3.8× clang's cold compile and 2.5× rustc's. Its binary is
21× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

Writing this kata turned up four gaps in the tools around the language,
none in the compiled code. All four are fixed in the kara repo.

- **B-2026-10-05-46 (crash): a parse error in a file that also held
  a multi-assign crashed `karac check`, `check --output=json`, `run` and
  `build`.** The differential had a typo, `!same(..)` for `not same(..)`.
  Instead of the parse error, every command printed a Rust panic:
  `StmtKind::MultiAssign is removed by the desugar pass before reaching this
  phase`. The lints that run beside the parse errors walk a tree that never
  reached that pass, and the tuple arm's swap is a multi-assign. Only `karac
  fix` worked, and it fixed the typo.
- **B-2026-10-05-47 (diagnostics): `(s[i], s[j]) = (s[j], s[i])` was
  refused with the right advice and no edit.** A parenthesized tuple is a
  value, not a place, and the error says to drop the parentheses. `karac fix`
  reported nothing to apply, because the error carried no edit. It now
  carries one that drops the parentheses on both sides at once, since `a, b =
  (c, d)` does not parse either.
- **B-2026-10-05-48 (diagnostics): `{x:?}` in an f-string said
  "unsupported type `?`".** That reads as if the author mistyped a format
  type. `?` is Debug formatting, which the design reserves and has not built
  yet. The error now says so, and suggests `{x}`. The kata writes its quotes
  by hand, `"\"{text}\""`, which is what `{text:?}` would print here once it
  exists.
- **B-2026-10-05-72 (diagnostics): `char.from_u32(n)` said only "no
  associated function 'from_u32' on type 'char'".** The benchmark builds its
  Greek letters from code points, and `from_u32` is the Rust spelling. Kāra
  spells it `char.try_from(n)`, and the error now says so, as it does for
  `i64.max_value()` (`i64.MAX`).

The author already knows the language, so none of this counts toward the
machine-fix rate.
