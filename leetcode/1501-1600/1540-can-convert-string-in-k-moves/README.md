# 1540. Can Convert String in K Moves

Given two strings `s` and `t` and an integer `k`, convert `s` into `t` in
`k` moves or fewer. In the `i`-th move (`1 <= i <= k`) you may either
pick an index `j` of `s` that no earlier move picked and shift `s[j]`
forward `i` times (`z` wraps to `a`), or do nothing. Return whether `s`
can be made equal to `t`.

```
s = "input", t = "ouput", k = 9  ->  true   (i shifted 6 times, n 7 times)
s = "abc", t = "bcd", k = 10     ->  false  (each needs 1 shift; only move 1 gives one)
s = "aab", t = "bbb", k = 27     ->  true   (moves 1 and 27)
```

**Constraints:** `1 <= s.length, t.length <= 10^5`; `0 <= k <= 10^9`;
`s` and `t` contain only lowercase English letters.

## Approaches

Each place needs the shift `d = (t[i] - s[i]) mod 26`, and the moves that
shift by `d` are `d`, `d + 26`, `d + 52`, ... Every arm rests on that.

| file | mechanism |
|---|---|
| `convert.kara` ★ | the places counted by shift in a `[0; 26]` array; the `c` places that need `d` take the moves up to `d + 26 (c - 1)`, and the answer is whether every such last move is at most `k`. O(n) |
| `convert_greedy.kara` | the places in order over `zip`ped `bytes()`, each taking the next move left for its shift from a `Vec` of next moves, refused as soon as one passes `k`. O(n) |
| `convert_room.kara` | each shift's room: of the moves 1 to `k`, `k / 26` shift by each `d` and one more for every `d` up to `k % 26`; the needs counted in a `Map` with `entry().or_insert()`, then `all` over it. O(n) |
| `convert_iter.kara` | `zip`, `map` and `filter` collect the shifts that are not 0; sorted, each run of one shift is walked, its `j`-th place taking move `d + 26 j`. O(n log n) |
| `convert_solution.kara` | LeetCode's Rust template (`can_convert_string(s: String, t: String, k: i32) -> bool`, the ★ arm over `as_bytes()` with `[0i32; 26]`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's three examples, then
`a -> a` at 0, `a -> b` at 0, strings of different lengths, `az -> ba` at
1 and 26, `aaa -> zzz` at 77 and 76; 100000 `a`s to `b`s at 2599975 and
2599974; then the count of `true` and a checksum for 3000 random pairs of
up to 12 letters with `k` up to 80, 300 of up to 1000 with `k` up to 2000
and 30 of up to 100000 with `k` up to 10^9, one pair in ten of different
lengths. `convert.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a backtracking search for one move from 1 to `k` for each
place that must change, no move used twice, each shifting its place's
letter to `t`'s. It checks 3000 pairs of 1 to 8 letters over the first 1
to 4, one in ten of different lengths, with `k` from 0 to 60, every
random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a yes stays yes at `k + 1`, and a no stays no at `k - 1` |
| P3 | the same letter put after both leaves the answer |
| P4 | every letter of both moved on by one (`z` to `a`) leaves the answer |
| P5 | both reversed leave the answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 805414936, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. All eleven are
killed, each the same way under both backends; M10 by a crash, an index
out of bounds, under both. Most mutants keep P2 to P5, which an
answer that is wrong the same way everywhere can hold, so P1 and P6
carry this table.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last move taken as `d + 26 c` | P1 564, P6 564 |
| M2 | ★: shift 1 never checked | P1 113, P6 113 |
| M3 | ★: the shift taken from `t` to `s` | P1 428, P6 428 |
| M4 | greedy: a move equal to `k` refused | P1 33, P6 33 |
| M5 | greedy: the next move 25 on, not 26 | P1 20, P6 20 |
| M6 | room: the extra move only below `k % 26` | P1 33, P6 33 |
| M7 | room: `(k + 1) / 26` moves for each shift | P1 18, P2 34, P6 18 |
| M8 | iter: a run continues on any shift not below the last | P1 376, P6 376 |
| M9 | iter: shifts of 0 kept | P1 760, P3 333, P6 760 |
| M10 | template: only a shorter `s` refused | index out of bounds |
| M11 | template: a shift counted once however many places need it | P1 435, P6 435 |

## Benchmarks

The bench builds 100 pairs of 1 to 20000 letters, each over its own
first 1 to 26 letters with `k` from 0 to 40000, once, and asks every
pair 50 times by the ★ arm, in all five languages. Every implementation
prints `50 passes over 100 pairs of up to 20000 letters: 3150 true,
checksum 217367894`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `3d1fc8e26` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.077 s |
| C (`clang -O3`) | 0.077 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.077 s |
| Kāra (`karac build`) | 0.081 s |
| Go | 0.082 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.087 s |
| Python | 3.7 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.07 s and 0.07 s on one run).

Kāra is 0.89x Rust under overflow checks by median. Not traced. The work
is a byte subtract, a `%` and an increment into a 26-entry table per
place, and building the 4 million random letters is a share of every
row, so the rows sit close together.

## Verification

All five arms print the same output as `convert.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `3d1fc8e26`.

## Writing it

The greedy and room arms were written in Kāra and checked as written.
The ★ arm was first written with `Array[i64, 26].filled(0)` for the
table, which has no such method, and was rewritten by hand to `[0; 26]`,
Kāra's fixed array: the refusal, `no method 'filled' on `Array[…]``,
elides the type and points nowhere, filed as B-2026-11-14-6. The iterator arm took one edit from `karac fix`:
`filter(|d| *d > 0)` to `filter(|d| d > 0)`, an `i64` being copied into
the closure.

The Rust template took 2, 1 and 1 changed lines over three rounds:
`&&` to `and` and `Solution::` to `Solution.`; then `struct Solution {}`
added; then `s.as_bytes()` and `t.as_bytes()` to `bytes()`. Its
`[0i32; 26]` and `as usize` index needed nothing. It checks and agrees
with no hand edit.
