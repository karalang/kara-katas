# 1247. Minimum Swaps to Make Strings Equal

You are given two strings `s1` and `s2` of equal length consisting of
letters `"x"` and `"y"` only. Your task is to make these two strings
equal to each other. You can swap any two characters that belong to
**different** strings, which means: swap `s1[i]` and `s2[j]`.

Return *the minimum number of swaps required to make `s1` and `s2`
equal*, or return `-1` if it is impossible to do so.

```
s1 = "xx", s2 = "yy"                  ->  1   (swap s1[0] and s2[1])
s1 = "xy", s2 = "yx"                  ->  2
s1 = "xx", s2 = "xy"                  ->  -1
s1 = "xxyyxyxyxx", s2 = "xyyxyxxxyx"  ->  4
```

**Constraints:** `1 <= s1.length, s2.length <= 1000`; `s1.length ==
s2.length`; `s1` and `s2` hold only `"x"` and `"y"`.

The arms are `fn minimum_swap(s1: Str, s2: Str) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `minimum_swap.kara` ★ | counting over `chars()` zipped: the places with `x` over `y` and those with `y` over `x`; two of a kind take one swap, one of each two, and an odd total cannot be fixed |
| `minimum_swap_bytes.kara` | the same count over `bytes()`, each pair of places matched as a tuple of byte literals, `(b'x', b'y')`, and the answer matched on the two counts' parities |
| `minimum_swap_swaps.kara` | doing it: the strings as `Vec[char]`, the places that differ gathered by kind, the swaps made, two of a kind at a time and then the one of each left over, and the strings compared at the end |
| `minimum_swap_iter.kara` | the two counts as `zip`, `filter` and `count` chains, the answer `(xy + 1) / 2 + (yx + 1) / 2` |
| `minimum_swap_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s1.bytes().zip(s2.bytes())`, `let (mut xy, mut yx)`, `&&`, an `i32` answer), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, four more properties |

Every arm prints the same 3 lines: LeetCode's four examples; the number
found impossible, the total of the rest and a checksum of every answer
for 1000 random pairs of 1 to 1000 letters, each string with its own
chance of `x` (`528 impossible, total 62528, checksum 649697542`); and
two pairs of 1000 letters, the constraints' top, every place different:
`xyxy..` against `yxyx..` and all `x` against all `y`.
`minimum_swap.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac run` and `karac build`, and
under the AddressSanitizer build.

The Mend loop: the ★ and iterator arms checked clean as first written.
The bytes arm was first written with Rust's `s1.as_bytes()`, which
`karac fix` rewrites to `s1.bytes()`, a `Slice[u8]`. The swaps arm was
first written `for kind in [xy, yx].iter()`, which moves the two lists
into the array while the last step still reads them, E0500; the fix
clones them there, `[xy.clone(), yx.clone()]`, and drops the `.iter()`.
The solution arm takes one round of fixes, 8 by `karac fix`'s count, and
then checks clean: `struct Solution;` to `struct Solution {}`, `let
(mut xy, mut yx)` to `let mut (xy, yx)`, `&&` to `and`, and the `zip` of
two `bytes()` to a `zip` of their `iter()`s.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms, renamed, and the
statement read literally: a breadth-first search over every pair of
strings the swaps reach, each string a bit mask of its `x`s, each move
any `s1[i]` swapped with any `s2[j]`, until the two are equal, and `-1`
when no pair reached is. 2000 random pairs of 1 to 5 letters, each
string with its own chance of `x`.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | `s1` and `s2` traded give the same answer |
| P3 | every `x` made a `y` and every `y` an `x`, in both, gives the same answer |
| P4 | the places reordered by one random permutation, the same in both, give the same answer |
| P5 | `-1` exactly when the two strings together hold an odd number of `x` |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 pairs: checksum 487608876,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: one of each kind fixed with one swap, not two | P1 151, P6 604 |
| S2 | ★: every `y` counted as `y` over `x`, matching places too | P1 782, P2 285, P3 1263, P5 641, P6 3128 |
| B1 | bytes: one of each kind fixed with one swap, not two | P1 151, P6 151 |
| B2 | bytes: `y` over `x` counted as `x` over `y` | P1 151, P6 151 |
| W1 | swaps: every third place of a kind skipped | P1 63, P5 63, P6 63 |
| W2 | swaps: the last two places counted as one swap | P1 151, P6 151 |
| I1 | iterator: the halves rounded down, so one of each costs nothing | P1 151, P6 151 |
| I2 | iterator: `y` over `y` counted, not `y` over `x` | P1 1121, P2 1271, P3 1658, P5 872, P6 1121 |
| L1 | solution: impossible when `x` over `y` is odd, whatever `y` over `x` | P1 649, P2 971, P3 971, P5 649, P6 649 |
| L2 | solution: each `x` over `y` counted twice | P1 842, P2 1383, P3 1383, P5 624, P6 842 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). Five (S1, B1, B2, W2, I1) get wrong only the cases
with one place of each kind left over, 151 of the 2000; they keep the
two strings' roles, the letters' symmetry and the parity, so only the
literal reading sees them. W1, which skips places, leaves strings
unequal and answers `-1`, which P5 sees too. P4, the places reordered, catches none: every arm counts, and no
mutation looks at where a place is.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the places that differ counted by kind over the two strings zipped)
on 2000 random pairs of 1000 letters built once, each with its own mix
of x and y, each asked 20 times; every answer folded into a checksum.
Every program prints `20 rounds of 2000 pairs of 1000 letters: checksum
630840906`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.311 to 0.339 s | 0.318 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.311 to 0.366 s | 0.319 s |
| Rust (`rustc -O`) | 0.224 to 0.241 s | 0.227 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.318 to 0.381 s | 0.322 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.309 to 0.360 s | 0.323 s |
| C (`clang -O3`) | 0.247 to 0.283 s | 0.260 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.248 to 0.277 s | 0.260 s |
| Go | 0.310 to 0.345 s | 0.326 s |
| Python | 3.701 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.322 s
against 0.319 s), and the two ranges overlap. C is about 18% ahead of
Kāra (0.260 s against 0.319 s); Go runs level with Kāra (0.326 s against
0.319 s). Python takes about 12x Kāra's time. No profile was taken.
