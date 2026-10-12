# 400. Nth Digit

Given an integer `n`, return the `n`th digit (counting from 1) of the
infinite sequence `123456789101112131415...`, the positive integers
written one after another.

```
n = 3   -> 3
n = 11  -> 0   (the 0 of 10)
```

**Constraints:** `1 <= n <= 2^31 - 1`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `nth_digit.kara` ★ | skip whole blocks of equal length (9 numbers of one digit, 90 of two, 900 of three, ...); then `n` falls in a known number at a known position, and the digit comes off by division | O(log n) | O(1) |
| `nth_digit_search.kara` | `digits_upto(x)`, the digits written for 1 to `x`, has a closed form; binary search for the smallest `x` with `digits_upto(x) >= n`, then read the digit off `x` written as text | O(log^2 n) | O(1) |
| `nth_digit_recursive.kara` | the ★ arm's block skip as a recursion, and the digit taken by a second recursion that drops trailing digits | O(log n) | O(log n) stack |
| `nth_digit_count.kara` | the brute-force walk, subtracting each number's length from `n`, with its loop unrolled: while the next `10^j` numbers have the same length and fit inside `n`, it takes them in one step | O(log^2 n) | O(1) |
| `differential.kara` | the four arms on 3,000 random cases whose answers are known by construction, five properties | — | — |

Every arm prints the same 16 lines: the two LeetCode examples, twelve
edge cases (positions 1, 9, 10, 12, 189 to 192, 2889 and 2890, at the
edges of the blocks of one- to four-digit numbers, and positions 10^9
and 2^31 - 1), the first 60 digits of the sequence as one string, and for 3,000 random
positions from 1 to 2^31 - 1 the sum of the digits and a checksum.
`nth_digit.py` mirrors the ★ arm and its output is byte-identical.

The plain brute force, one number at a time, takes about 2.4 x 10^8
steps for `n` = 2^31 - 1, too many for the MIR interpreter to finish
the harness, so the count arm unrolls it rather than leaving it out.

## Differential

`differential.kara` holds copies of the four arms. It writes the
sequence out as text up to 3,000 digits, and counts the digits of
1, 2, ..., x one power of ten at a time (`written(x)`). For each of
3,000 random cases:

| | property |
|---|---|
| P1 | position `case + 1`, for `case` from 0 to 2,999, matches the sequence written out as text |
| P2 | the digits of `10^k`, for `k` from 1 to 8, are a 1 and `k` zeros: `10^k` starts right after `written(10^k - 1)` |
| P3 | position `written(10^k - 1)`, the end of the block of `k`-digit numbers, is 9 |
| P4 | position `written(x - 1) + i + 1` is digit `i` of `x` written as text, for a random `x` up to 2 x 10^8 |
| P5 | position `written(x)` is the last digit of `x`, `x % 10` |

It prints `3000 cases, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | blocks: a position at the end of a block skips into the next | P1 3, P3 3000 |
| M2 | blocks: the digit is read from the right instead of the left | P1 1867, P2 1362, P4 2559, P5 2728 |
| M3 | search: the digit is read from the next number | P1 1136, P2 664, P3 3000, P4 388, P5 3000 |
| M4 | search: a power of ten does not count as reaching itself | panics: index out of bounds |
| M5 | recursive: the number is found from `n`, not `n - 1` | P1 2687, P2 1362, P4 2730, P5 2728 |
| M6 | recursive: the next block starts one past the right place | P1 3, P2 698 |
| M7 | count: a jump may cross into the next block by one number | P1 2686, P2 1212, P3 2612, P4 2730, P5 2698 |
| M8 | count: the digit is read from the right | P1 1867, P2 1362, P4 2559, P5 2728 |

M4 stops the differential instead of failing a property: undercounting
the digits up to a power of ten makes the search arm read a position
past the end of its number. A first M3 and M4 (a count that misses one
number per power, and a search that settles one number low) stopped
the same way and were replaced by mutations a property can see; M4 has
no such variant, since any wrong `x` in that arm reads out of range. M1
and M6 are each caught almost only at block ends, by P3 and P2: those
are the positions where they differ from the right answer. M2 and M8 are
one mistake in two arms.

## Verification

All four arms print the same output as `nth_digit.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file. The
differential prints `60000 checks, 0 failures` on all six.

## Benchmarks

The bench program uses the ★ arm. It makes 10,000,000 calls, each on a
random `n` from 1 to 2^31 - 1, and folds the digits into a sum and a
checksum. Every implementation prints `10000000 calls: total 43357930,
checksum 227851270`; a 50,000-call cut of the Kāra program under
`karac __mir-run` prints the same as the C program cut the same way.
Spot timings on a shared 4-core container (`bench.sh` timings need a
quiet machine), each about the same from run to run within 0.05 s:

| | time |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.30 s |
| Kāra (legacy `karac build`) | 0.31 s |
| C (`clang -O3`) | 0.33 s |
| Rust (`rustc -O`) | 0.33 s |
| Go | 0.42 s |
| Python | 18 s |

All four compiled programs are within noise of each other here; the
work is a few divisions per call. The Kāra program also prints the same
line under `karac __mir-llvm-run` in 1.5 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark. The
`karac build` time is the frozen legacy backend.

## Compiler findings

No new findings. The differential's first draft wrote
`let digits = f"{x}".bytes();`. `karac check` accepted it, and the MIR
borrow checker refused it (`drop of _59 while it is borrowed`, E0516)
because the formatted string is a temporary that dies at the end of the
statement while `digits` still views it. The refusal is right, as in
Rust; the gap is that `karac check` does not run the MIR borrow checker
yet, a class Thread A has in hand (see kata 382). The differential now
binds the string first.
