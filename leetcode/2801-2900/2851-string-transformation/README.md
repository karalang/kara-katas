# 2851. String Transformation

You are given two strings `s` and `t` of equal length `n`. You can
perform the following operation on the string `s`:

- Remove a **suffix** of `s` of length `l` where `0 < l < n` and append
  it at the start of `s`. For example, let `s = 'abcd'` then in one
  operation you can remove the suffix `'cd'` and append it in front of
  `s` making `s = 'cdab'`.

You are also given an integer `k`. Return *the number of ways in which*
`s` *can be transformed into* `t` *in **exactly*** `k` *operations.*

Since the answer can be large, return it **modulo** `10^9 + 7`.

```
s = "abcd", t = "cdab", k = 2      ->  2
s = "ababab", t = "ababab", k = 1  ->  2
```

**Constraints:** `2 <= s.length <= 5 * 10^5`; `1 <= k <= 10^15`;
`s.length == t.length`; `s` and `t` consist of only lowercase English
alphabets.

## Approaches

| file | mechanism |
|---|---|
| `ways.kara` ★ | a move is a rotation by a shift other than 0, so k moves land on shift r in as many ways as k nonzero shifts sum to r mod n: ((n - 1)^k + (n - 1)(-1)^k) / n for 0, ((n - 1)^k - (-1)^k) / n for each other shift, the division by n's inverse mod p; the shifts that turn s into t are where the prefix function of t finds it in s + s |
| `ways_matrix.kara` | the pair (ways at shift 0, ways at a given other shift) by a 2 x 2 `Array[Array[i64, 2], 2]` matrix raised to k by squaring; the matching shifts by the Z-function of t + s + s |
| `ways_halves.kara` | the same pair as a walk on the cyclic group, two runs of moves joined by convolution and k split in halves by recursion; the matching shifts by a rolling hash of t against every window of s + s under two moduli |
| `ways_rotate.kara` | every rotation made in turn with `rotate_right` on a `Vec[u8]` and compared with t whole, O(n^2) for the harness's sizes; the closed form over `u64` with a recursive power |
| `ways_solution.kara` | a Rust solution as LeetCode's Rust users write it: `const MOD: i64 = 1_000_000_007`, a top-level `fn pow_mod(mut b: i64, mut e: i64)`, the prefix function over `vec![0usize; n]` and a KMP scan of s + s from `as_bytes()`, and the closed form, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; two letters
swapped 10^15 times, LeetCode's most, and 10^15 + 1 times; 2000 of one
letter, every rotation a match, 10^15 times; then 3000 random pairs of
2 to 6 letters over a and b with k up to 20, and 60 of up to 2000
letters, each a block of up to 8 repeated, t a rotation of s two times
in three, k up to about 10^12, as a count with a way and a checksum.
`ways.py` mirrors the ★ arm and its output is byte-identical.

```
2 2
1 1 0
815044104
3000 short pairs: 629 with a way, checksum 991092421
60 long pairs: 49 with a way, checksum 394584470
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: from s, every suffix of length 1 to n - 1 taken to the
front, k times over, the ways to reach each string counted in a
`Map[String, i64]`, and t's count. It draws 2000 random pairs of 2 to 6
letters over a and b with k up to 12, t a rotation of s half the time,
then 50 of up to 1500 letters, each a block of up to 8 repeated, t a
rotation of s two times in three, k up to about 10^12, all before any
arm answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 6 letters, the answer is the literal reading's |
| P2 | s and t swapped: the same answer |
| P3 | both strings reversed: the same answer |
| P4 | every letter of both moved on one, c to a: the same answer |
| P5 | t not found in s + s: 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 1138 with a way: checksum
604832829, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Eight are killed, each the same
way under both backends. M5 and M7 survive and are equivalent in output:
with the Z-box never moved on, no z[i] is seeded from an earlier box, so
each is counted out from zero, which gives the same Z-function in
quadratic time; and the second modulus only guards against a collision
under the first, which no window of these cases has with t.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a match at shift 0 counted as any other | P1 492, P6 523 |
| M2 | ★: the sign of (-1)^k never turned | P1 477, P6 492 |
| M3 | ★: the prefix function not fallen back on a mismatch | P2 1, P3 3, P6 2 |
| M4 | matrix: a move from another shift staying among n - 1 others | P1 1071, P6 1116 |
| M5 | matrix: the Z-box never moved on | survives: equivalent (above) |
| M6 | halves: an odd k's last move left off | P1 684, P6 729 |
| M7 | halves: one modulus's mismatches ignored | survives: equivalent (above) |
| M8 | rotate: the rotation by two each turn | P1 498, P6 507 |
| M9 | rotate: an odd k's ways to shift 0 given the even form | P1 252, P6 283 |
| M10 | solution: every match counted at shift 0 | P1 919, P6 964 |

## Benchmarks

The bench draws 10 pairs of 5 * 10^5 letters, LeetCode's most, each s a
block of up to 8 letters repeated, half of them with one letter
changed, t a rotation of s two times in three and otherwise s with one
letter changed, k up to about 10^15, all of them first, then answers
each 5 times by the ★ arm in all five languages; every answer builds s
+ s and the prefix function afresh. Draws wider than the generator's
0 to 32767 take two of them, `a * 32768 + b`. Every implementation
prints `10 pairs of 500000, 5 rounds: checksum 670548033`.

BENCHTAB

## Verification

All five arms print the same output as `ways.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, halves and rotate arms, as first written, read the strings with
`s.bytes().chain(s.bytes())`, `t.bytes().collect()` and
`t.bytes().fold(..)`, and `karac check` reported E0236, "no method
'chain' on type 'Slice': iterator adaptors/terminals require an
explicit `.iter()`"; `karac fix` wrote the `.iter()`. The harness's
`unit.byte_at(i)`, a method no language has, drew E0236 with no fix
and became `unit.bytes()[i]` by hand.

The matrix arm wrote its matrices as Rust does, `[[i64; 2]; 2]` in
`times`'s signature, `let step = [[0, a], [1, b]];`, `let mut result =
[[1, 0], [0, 1]];`, and the step squared through a copy, `let mut b =
step;`. `karac fix` wrote `Array[Array[i64, 2], 2]` for the types
(E0001), `let mut (lo, hi)` for the Z-box's `let (mut lo, mut hi)`, and
`: Array[Array[i64, 2], 2]` on `result`, whose list literal is a `Vec`
with no expected type (design.md § Collection literals). But `b`, a
copy of `step`, was used as an `Array` with neither the explanation nor
a fix, so four E0200 errors were left and nothing to apply. Since kara
0d28296389 (B-2026-11-21-203) the hint follows `let b = step` back to the literal's binding,
"`b` holds `step`, and `step` (bound at 38:9) is a `Vec`", and `karac
fix` declares `step`, from which `b` takes its type; the arm then
checked clean in one run.

LeetCode's Rust template took 25 `karac fix` edits in one run, the
wrapper included: the `mut b` and `mut e` parameters became plain ones
rebound with `let mut b = b;` (E0002); `1i64`, `0usize`, `0i64` lost
their suffixes and `vec![0usize; n]` became `Vec.filled(n, 0)`;
`as_bytes()` became `bytes()` and the `chain` took `.iter()`; `&&`
became `and`; `let (mut zero, mut other)` became `let mut (zero,
other)`; `struct Solution {}` added for the `impl`; in the wrapper
`&str` became `Str`, `Solution::` took `.` and the `as i64` went. The
`let n = n as i64;` lost its cast, `usize` being `i64`, and was left as
`let n = n;`, a binding of itself. Since kara 0d28296389 the
`self_rebinding` lint names it and its fix deletes the line (B-2026-11-21-206).
