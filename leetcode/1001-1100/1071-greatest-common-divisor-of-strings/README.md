# 1071. Greatest Common Divisor of Strings

For two strings `s` and `t`, `t` divides `s` if and only if `s = t + t +
... + t`, that is, `t` concatenated with itself one or more times. Given
two strings `str1` and `str2`, return the largest string `x` such that
`x` divides both `str1` and `str2`.

```
str1 = "ABCABC", str2 = "ABC"   ->  "ABC"
str1 = "ABABAB", str2 = "ABAB"  ->  "AB"
str1 = "LEET", str2 = "CODE"    ->  ""
```

**Constraints:** `1 <= str1.length, str2.length <= 1000`; both consist of
English uppercase letters.

A string that divides `str1` is a prefix of it, and if any string divides
both, so does the prefix as long as the gcd of the two lengths, which is
then the longest. So the question is only whether one exists.

The arms take the two strings as `String` and return the answer as a
`String`, empty when there is none.

## Approaches

| file | mechanism |
|---|---|
| `gcd_strings.kara` ★ | the two concatenations compared: `a + b == b + a` exactly when both are copies of one string, and then the answer is `a.substring(0, gcd(a.len(), b.len()))`. O(n1 + n2) |
| `gcd_strings_brute.kara` | every length from the shorter string's down: the first prefix of `a` whose copies make up both strings, each checked piece by piece with `substring`. O(min(n1, n2) * (n1 + n2)) |
| `gcd_strings_euclid.kara` | Euclid's algorithm on the strings: a string that divides both divides the longer with the shorter cut off its front, so the shorter must begin the longer (`starts_with`), and the pair shrinks until one is empty |
| `gcd_strings_period.kara` | each string's shortest root by the prefix function (`border: Vec[i64]` over `s.bytes()`): the longest border leaves the shortest period, which is the root when it divides the length. The strings share a divisor exactly when their roots are the same, and the answer is that root `.repeat` the gcd of their counts. O(n1 + n2) |
| `gcd_strings_letters.kara` | letter by letter (`a.chars().collect()`): every letter of either string must be the letter of `a` at its place modulo the gcd of the lengths. O(n1 + n2) |
| `gcd_strings_solution.kara` | LeetCode's Rust template (`struct Solution;`, `format!("{}{}", str1, str2)`, `String::new()`, a `fn gcd(a: usize, b: usize)` nested in the method, `str1[..g].to_string()`, `Solution::`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for LeetCode's three
examples and six more; how many of 3000 random pairs up to 24 letters and
of 300 up to 1000 letters have an answer, its letters in all and a
checksum; and the answers' lengths for 1000 `A`s against runs of 999,
600, 250 and 1, for 333 `ABC`s against 111, 222, 1 and 332 copies, and
for 500 `AB`s against 499 and an `AC`. `gcd_strings.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every prefix of `a`, copies of it laid end to end with
`push_str` until they are as long as each string, and the longest prefix
that makes up both. It checks 2000 problems, 1000 over one or two letters
of a root of 1 to 3 letters repeated 1 to 5 times, and 1000 over up to
four letters of a root up to 6 letters repeated up to 10 times. The first
string is always copies of the root; the second is too, but one time in
three one of its letters is changed and one time in six it is a random
string of its own. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the two strings swapped give the same answer |
| P3 | the answer is empty or as long as the gcd of the two lengths |
| P4 | `a` and `a` answer `a`, and `a + b` and `b` answer what `a` and `b` do |
| P5 | each string doubled answers the answer doubled |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 420250950, 84000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 problems gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm; every kept edit fails the same way under both backends, none
by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the answer one letter short | P1 1551, P3 1219, P4 2000, P5 1551, P6 1551 |
| M2 | ★: the concatenations never differ (`a + b != a + b`) | P1 449, P2 276, P5 81, P6 449 |
| M3 | ★: no answer given as the first letter | P1 449, P2 164, P3 315, P5 449, P6 449 |
| M4 | brute: `b` never checked | P1 1052, P2 1212, P3 871, P4 1323, P5 200, P6 1052 |
| M5 | brute: a piece checked at every start, overlapping | P1 1219, P3 763, P4 1919, P5 1095, P6 1219 |
| M6 | Euclid: the empty string returned at the end | P1 1551, P4 2000, P6 1551 |
| M7 | Euclid: the shorter anywhere in the longer (`contains`) | P1 68, P4 381, P5 49, P6 68 |
| M8 | Euclid: a one-letter string ends the descent | P1 348, P2 2, P3 346, P4 98, P5 348, P6 348 |
| M9 | period: a period that does not divide the length taken as the root | P1 30, P3 2, P4 33, P5 30, P6 30 |
| M10 | period: the root, not the root repeated | P1 923, P3 923, P4 1844, P5 1551, P6 923 |
| M11 | period: the roots compared by length only | P1 27, P2 27, P4 27, P6 27 |
| M12 | letters: `a` never checked past the gcd | P1 2, P2 152, P5 1, P6 2 |
| M13 | letters: `b` checked against its own prefix | P1 81, P2 81, P4 81, P5 54, P6 81 |
| M14 | solution: the gcd taken with one more | P1 1382, P2 676, P3 1382, P4 2778, P5 1551, P6 1382 |
| M15 | solution: no answer given as the whole of `str1` | P1 449, P2 449, P3 352, P4 449, P6 449 |

P1 and P6 kill all fifteen, P4 and P5 twelve, P2 and P3 nine. P2 sees
an edit only when it treats the two strings differently, and P3 only
when it gives an answer of the wrong length: the Euclid edits that
answer empty or match the shorter anywhere (M6, M7) keep the length
right, and so do M2, M11, M12 and M13, which answer when they should not
or the other way round. M12 is the edit P2 sees best (152 failures,
against P1's 2): the first string of every problem is copies of a root,
so it hardly ever fails the check the edit skips, and only swapping
brings the changed second string into first place.

Of the fifteen not kept, two crash: the ★ arm's gcd by quotients
(`star_gcd(b, a / b)`) recurses without end on two equal numbers, and
the solution's gcd one step deep (`b` for `solution_gcd(b, a % b)`) can
exceed the first string's length, so `str1[..g]` is out of range. Six
fail as a kept edit or as each other: the answer one letter short in the
letters arm and the solution's first letter dropped as M1; the solution's
concatenations compared by length as M2; the shorter length for the gcd
in the ★ and letters arms alike; Euclid's shorter-first answering nothing
as M6; and Euclid's `ends_with` as M7. The brute arm's whole shorter
string never tried, one-letter roots never tried and every other length
tried, the period arm's one fallback a letter and a mismatch falling back
to nothing, and the letters arm's first letter of `b` unchecked each fail
in a way of their own.

## Verification

Every arm prints the same output as `gcd_strings.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.3 s to 0.8 s (period)
and the differential 2.6 s.

Every file went through `karac fix`. In the differential it wrote
`answers[w].clone()` for a `String` read out of a `Vec` by index. The
Rust arm reaches a clean check in two rounds: the syntax (`struct
Solution {}`, both `format!` calls to `f"{str1}{str2}"` and
`f"{str2}{str1}"`, `String.new()`, the nested `fn gcd` moved above the
impl, `Solution.`), then the nested function's `usize`s to `i64`. The kata
found two compiler gaps, fixed in kara `9671efaf31` with
`tests/kata_1071_check_gaps.rs`, `tests/kata_1071_native_ref_arg.rs` and
the core pin `corpus/core/ok_ref_number_as_native_argument`:

- **A `ref` number reached a library native as its address.** The ★
  arm's `[999, 600, 250, 1].iter().map(|n| gcd_of_strings(a1000,
  "A".repeat(n)).len())` passes `n`, a `ref i64`, to `String.repeat`.
  `karac check` accepts it (core semantics §5.10: a `ref` to a `Copy`
  value is read as the value wherever the value is expected), but MIR
  handed the native the reference: `karac __mir-run` stopped with
  "expected a library value, found Int(999)" and the LLVM backend
  panicked compiling the call. `substring` and `rotate_left` failed the
  same way. Kara B-2026-11-08-50.
- **Two `format!` calls in one condition.** In `if format!(..) !=
  format!(..) {` the condition ended at the first call's name, so only
  that call was reported, and the `!=` threw the rest of the function out
  of step: "expected `;`", "Expected expression, found `}`", top-level
  statements, and a `karac fix` that put a `;` after the function's tail
  expression. A Rust macro call is now read as an operand where its name
  is parsed, so both calls are reported and fixed in one round. Kara
  B-2026-11-08-51.

## Benchmarks

The bench builds 20000 pairs once, in all five languages, the way the
differential does but larger: copies of a root of 1 to 20 letters over 1
to 4 letters, up to 50 copies each, the second string changed in one
letter one time in three and a random string of up to 1000 letters one
time in six. It answers every pair 50 times with the ★ arm. Every
implementation prints `1000000 calls: 713200 found, 19028000 letters,
checksum 264579271`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with kara `9671efaf31`
on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.136 to 0.193 s | 0.144 s |
| Kāra (`karac build`) | 0.141 to 0.171 s | 0.146 s |
| C (`clang -O3`) | 0.142 to 0.176 s | 0.148 s |
| Rust (`rustc -O`) | 0.221 to 0.282 s | 0.238 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.247 to 0.308 s | 0.257 s |
| Go | 0.358 to 0.415 s | 0.387 s |
| Python | 1.05 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.139 s) is below its real time.

The work is the two concatenations: each call builds `a + b` and `b + a`
and compares them, up to 2000 letters a side. Kāra and C allocate each
concatenation once at its full length and copy both halves into it.
Rust's `a.to_string() + b`, the usual way to write it, allocates `a` at
its own length and then grows the buffer to append `b`, so it allocates
and copies twice. Written with `String::with_capacity` and two
`push_str`s, the same Rust program runs in 0.136 to 0.155 s (median
0.140 s over seven runs beside Kāra's 0.148 s), level with Kāra and C;
that version is not the bench, since it is not how the template writes
the condition. Go's user time (0.506 s) is above its real time, so its
collector runs beside the program on the garbage of a million pairs of
concatenations, which is the likely cause of its 2.7x (inferred, not
measured with counters).
