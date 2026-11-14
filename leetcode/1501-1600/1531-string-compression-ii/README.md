# 1531. String Compression II

Run-length encoding is a string compression method that replaces each run
of two or more equal characters with the character followed by the run's
length. A single character is kept as it is, with no `1` after it. For
example, `"aabccc"` is encoded as `"a2bc3"`.

Given a string `s` and an integer `k`, delete at most `k` characters from
`s` so that the run-length encoding of what is left is as short as
possible, and return that length.

```
s = "aaabcccd", k = 2     ->  4   (delete b and d: "a3c3")
s = "aabbaa", k = 2       ->  2   (delete both b's: "a4")
s = "aaaaaaaaaaa", k = 0  ->  3   ("a11")
```

**Constraints:** `1 <= s.length <= 100`; `0 <= k <= s.length`; `s`
contains only lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `compression.kara` ★ | `best[i][j]`, the shortest encoding of the suffix from `i` with `j` deletions left, bottom up. Place `i` is either deleted, or kept as the start of a run: the run walks right, keeping the letters equal to `s[i]` and deleting the others while the deletions last, and every place it could stop is tried. O(n² k) |
| `compression_memo.kara` | the ★ arm's recurrence asked top down, each `shortest(i, j)` kept in a table so it is worked out once. O(n² k) |
| `compression_runs.kara` | left to right over what the kept text ends with: its last letter, that letter's run, and the deletions spent, a `Map` per step holding the shortest encoding of each state. Each letter is deleted, grows the run (the encoding grows only when the count gains a digit, at 1, 9 and 99) or starts a new one |
| `compression_solution.kara` | LeetCode's Rust template (the ★ arm with `vec![vec![0i32; k + 1]; n + 1]`, `usize` indices and `i32` counts), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, the alphabet
with 25 deletions, `a` with 1, `aaaaaaaaaab` with 1 and 100 `a`s with
none, then checksums of the answers for 3000 random strings of 1 to 12
letters over up to 3 and 300 of 1 to 100 letters over up to 4, each with
`k` from 0 to its length. `compression.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of at most `k` places deleted, the rest run-length
encoded, the shortest kept. It checks 3000 strings of 1 to 10 letters
over up to 3, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed has the same answer |
| P3 | one more deletion never lengthens the answer, and `k` at the length gives 0 |
| P4 | the answer is at least 0 when `k` is the length and at least 1 otherwise, at most the encoding with nothing deleted, and that encoding exactly at `k = 0` |
| P5 | the letters renamed (a to b, b to c, c to a) leave the answer |
| P6 | each arm agrees with at least one of the other three |

The differential prints `3000 problems: checksum 973553233, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Twelve edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All twelve are killed, each
the same way under both backends; M6 by a crash, an index out of bounds,
under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run of 10 written with one digit (the memo arm shares `run_length`, so the two agree) | P1 16, P4 200 |
| M2 | ★: a deletion only when two are left | P1 832, P2 30, P3 3000, P6 832 |
| M3 | ★: the run stops one deletion early | P1 842, P2 168, P4 3000, P6 842 |
| M4 | ★: the letters a run deletes not spent | P1 632, P2 193, P6 632 |
| M5 | memo: a suffix no longer than the deletions left not cut to 0 | P1 2220, P3, P4 3000 each, P6 2220 |
| M6 | memo: the run walks one deletion past the budget | index out of bounds |
| M7 | memo: a deletion that spends nothing | P1 1802, P4 1802, P6 1802 |
| M8 | runs: the second digit added on growing a run of 10, not of 9 | P1 8, P4 100, P6 8 |
| M9 | runs: a run that stops growing at 3 | P1 652, P4 952, P6 652 |
| M10 | runs: one deletion past `k` | P1 1599, P4 2389, P6 1599 |
| M11 | template: a run of 10 written with one digit | P1 8, P4 100, P6 8 |
| M12 | template: the run stops one deletion early | P1 239, P2 93, P6 239 |

## Benchmarks

The bench builds 300 random strings of 1 to 100 letters once, each over
its own first 1 to 4 letters with `k` from 0 to its length, and answers
each 10 times by the ★ arm, in all five languages. Every implementation
prints `10 passes over 300 strings of up to 100 letters: checksum
293299235`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `a90821c8d` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.252 s |
| Rust (`rustc -O`) | 0.282 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.299 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.316 s |
| Kāra (`karac build`) | 0.317 s |
| Go | 0.388 s |
| Python | 17.1 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.31 s and 0.31 s on one run).

Kāra is 1.06x Rust under overflow checks by median. Not traced. The inner
loop is a byte compare, a branch and a `min` over table reads, which
leaves the optimizer little to vectorize in any language; the two Rust
rows are close for the same reason.

## Verification

All four arms print the same output as `compression.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `fcd87e1f1`.

## Writing it

The ★, memo and runs arms were written in Kāra and checked as written.

The Rust template took 3, 4 and 2 edits over three rounds: `i32::MAX` to
`i32.MAX`, `let (mut same, mut diff)` to `let mut (same, diff)` and
`Solution::` to `Solution.`; then `s.as_bytes()` to `s.bytes()`, the
inner `vec![0i32; k + 1]` to `Vec.filled(k + 1, 0i32)`, `let len = if ..`
to `let len: i32 = if ..`, and the closing `as i64` dropped (an `i32`
widens); then `k as usize` to `k as i64` with the outer `vec!` to
`Vec.filled`. It checks and agrees with no hand edit.

The `let len: i32` edit is new. When this kata was first drafted, the
`len` bound to an `if` of literals was typed `i64` at once and refused at
`best.min(len + ..)` with no fix, so the template stopped there. Since
kara `a6491451e1` (B-2026-11-10-49) an `if` of literals binds a literal
variable, and the refusal names `len` and offers the annotation as a
machine-applicable edit (B-2026-11-08-20's message).
