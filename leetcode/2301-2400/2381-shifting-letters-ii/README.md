# 2381. Shifting Letters II

You are given a string `s` of lowercase English letters and a 2D integer
array `shifts` where `shifts[i] = [start_i, end_i, direction_i]`. For
every `i`, **shift** the characters in `s` from the index `start_i` to
the index `end_i` (**inclusive**) forward if `direction_i = 1`, or shift
the characters backward if `direction_i = 0`.

Shifting a character **forward** means replacing it with the **next**
letter in the alphabet (wrapping around so that `'z'` becomes `'a'`).
Similarly, shifting a character **backward** means replacing it with the
**previous** letter in the alphabet (wrapping around so that `'a'`
becomes `'z'`).

Return *the final string after all such shifts to* `s` *are applied*.

```
s = "abc", shifts = [[0,1,0],[1,2,1],[0,2,1]]  ->  "ace"
s = "dztz", shifts = [[0,0,0],[1,1,1]]         ->  "catz"
```

**Constraints:** `1 <= s.length, shifts.length <= 5 * 10^4`;
`shifts[i].length == 3`; `0 <= start_i <= end_i < s.length`;
`0 <= direction_i <= 1`; `s` consists of lowercase English letters.

Shifts commute, so each letter moves by the forward shifts that cover
it less the backward ones, modulo 26. A shift over a range adds a step
at its start and takes it back after its end, so the running sum of
those marks is each letter's step.

## Approaches

| file | mechanism |
|---|---|
| `shift.kara` ★ | a difference array: each shift's step added at its start and taken back after its end, the running sum each letter's step, applied by `rem_euclid(26)`. O(n + q) |
| `shift_each.kara` | each shift applied in turn, every letter of its range stepped one place forward or back around the alphabet. O(sum of the ranges) |
| `shift_fenwick.kara` | a Fenwick tree: each shift two point updates, each letter's step a prefix sum. O((n + q) log n) |
| `shift_events.kara` | each shift two events, its step at its start and the step taken back after its end, sorted by place and swept along the letters. O(q log q + n) |
| `shift_iter.kara` | iterators: the difference array folded from the shifts, its running sums by `scan`, each letter `zip`ped with its step |
| `shift_solution.kara` | LeetCode's Rust template: `vec![0i32; n + 1]`, the bounds cast `as usize`, and the letters rebuilt from `chars().enumerate()` into a `String::with_capacity`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; `a` shifted
back to `z`; `5 * 10^4` letters with `5 * 10^4` shifts of up to 100
letters, and with 200 shifts of every letter, as checksums of the
letters; then 2000 random strings of 1 to 30 letters with 0 to 30
shifts, with a checksum and how many come back unchanged. `shift.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 3000 random strings of up to 20 letters against every shift
applied letter by letter.

Two arms were first written as Rust writes them, and `karac fix` carried
each in one edit: the each arm's `map(|c| c - b'a')` collected into a
`Vec[i64]`, which `check` reports since `collect` does not widen its
items, written `(c - b'a') as i64`; and the iter arm's `scan` closure,
which wrote its state through `*total += x` and returned `Some(*total)`
as Rust's does, rewritten to take the state by value and return
`Some((total, total))`, as Kāra's `scan` asks. The ★ arm's
`(b[i] - b'a') as i64` was reported as a cast that widens anyway, and
dropped by the same fix.

`check` first reports 7 errors on the template, and `karac fix` carries
it in one call, reporting 16 edits: `struct Solution;` given its braces;
`Vec<..>` its brackets; `vec![0i32; n + 1]` written `Vec.filled(n + 1,
0i32)`; `String::with_capacity` and `Solution::` written with a dot;
the `&` of the wrapper's `|&x|` dropped; `c as u8` on a `char` written
`c as u32 as u8`; and the wrapper's `s.clone()` passed as `s`. The
`as usize` bounds, `rem_euclid` and `(b'a' + v as u8) as char` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each letter checked against every shift, counting the forward
ones that cover it less the backward ones, then walked that many places
through the alphabet written out, one place at a time. No difference
array. It checks 300 random strings of 1 to 30 letters with 0 to 30
shifts; then 30 of up to 600 letters with up to 600 shifts; then 30 of
up to 300 letters whose shifts all go one way. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | as long as the string, every letter from a to z, and a letter no shift covers unchanged |
| P3 | the string reversed and every shift mirrored: the answer reversed |
| P4 | every shift followed by its opposite: the string unchanged |
| P5 | the first half of the shifts applied, then the rest to that: the same answer |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a shift range mirrors with the string: the shift
`[a, b, d]` on a string of `n` letters covers the same letters as
`[n-1-b, n-1-a, d]` on the reversed string. P4 and P5 hold because the
shifts commute: a letter's place depends only on how many forward and
backward shifts cover it, whatever their order, and a shift and its
opposite cancel.

The differential prints `360 cases: checksum 409573116, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and applies every shift letter by letter. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every shift taken forward | P1 320, P4 342, P6 320 |
| M5 | ★: an alphabet of 25 | P1 267, P2 23, P4 189, P6 267 |
| M6 | ★: each letter shifted before its own step | P1 343, P2 67, P3 334, P6 343 |
| M7 | each: a backward shift of two | P1 320, P4 343, P6 320 |
| M10 | each: the directions swapped | P1 343, P6 343 |
| M11 | each: forward stopping at z | P1 215, P4 216, P6 215 |
| M12 | fenwick: the tree updated one by one | P1 327, P2 62, P3 327, P6 327 |
| M15 | fenwick: the step added at the range's end | P1 332, P3 332, P6 332 |
| M16 | fenwick: the prefix walked down one by one | P1 331, P2 71, P3 334, P6 331 |
| M17 | events: the events never sorted | P1 332, P3 305, P4 343, P5 331, P6 332 |
| M19 | events: one event per letter | P1 317, P2 28, P3 308, P4 343, P5 315, P6 317 |
| M20 | events: the step taken back at the range's end | P1 343, P3 332, P6 343 |
| M24 | iter: each step its own difference | P1 334, P2 67, P3 334, P6 334 |
| M25 | iter: the letters zipped with the next step | P1 343, P2 73, P3 334, P6 343 |
| M26 | iter: a forward step of two | P1 317, P4 343, P6 317 |
| M28 | solution: the step never taken back | P1 330, P2 64, P3 334, P6 330 |
| M31 | solution: an alphabet of 27 | P1 223, P2 148, P6 223 |

P1 and P6 kill all seventeen, P3 ten, P2 nine, P4 seven and P5 two.
P4, every shift followed by its opposite, fails the edits whose forward
and backward steps are not opposites: every shift taken forward (M1),
an alphabet of 25 (M5), a backward or forward step of two (M7, M26),
forward stopping at z (M11), and the events arm's events never sorted
and one event per letter (M17, M19). Those two alone fail P5, the shifts
applied in two halves, since how wrong they go depends on how many
shifts one call holds. P3, the string and the shifts mirrored, fails
the edits that move one end of a range and not the other, and passes
those that treat both ends alike, as the directions swapped (M10) or an
alphabet of 25 or 27 (M5, M31).

Of the thirty-one, fourteen were not kept. The step taken back at the
range's end in the ★, fenwick and template arms (M3, M14, M30), the each
arm's range's last letter left out and range from one past its start
(M8, M9), and the iter arm's range from one past its start (M23) fail as
the events arm's step taken back at the range's end (M20); the ★ arm's
running sum never carried and the template's (M4, M29) as the iter arm's
each step its own difference (M24); the ★ arm's step never taken back
(M2) as the template's (M28); the fenwick arm's each letter read one
place early and the events arm's event applied one letter late (M13,
M18) as the ★ arm's each letter shifted before its own step (M6); the
template's every shift taken forward (M27) as the ★ arm's (M1); the
events arm's backward shift of two (M21) as the each arm's (M7); and the
iter arm's directions swapped (M22) as the each arm's (M10). The iter
arm's every step doubled failed as the directions swapped too, and was
replaced by a forward step of two (M26).

## Verification

Every arm prints the same output as `shift.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 to 7.9 s, the each arm the
slowest as it steps every letter of every range, and the differential
10.1 s there and 1.2 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds a string of `5 * 10^4` letters and 10 lists of
`5 * 10^4` shifts once from the harness's generator, list `l`'s shifts
up to `10^l` letters long, capped at the string, then makes 200 passes,
pass `p` applying list `p % 10` and folding each letter of the answer
plus `p` into the checksum, with the ★ arm in all five languages. Every
implementation prints `200 passes over 5 * 10^4 letters: checksum
754771922`. Every implementation allocates its difference array and
its answer afresh in each call.

BENCHTAB
