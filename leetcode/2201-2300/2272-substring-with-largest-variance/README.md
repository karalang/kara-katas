# 2272. Substring With Largest Variance

The **variance** of a string is defined as the largest difference
between the number of occurrences of **any** `2` characters present in
the string. Note the two characters may or may not be the same.

Given a string `s` consisting of lowercase English letters only, return
*the **largest variance** possible among all **substrings** of* `s`.

A **substring** is a contiguous sequence of characters within a string.

```
s = "aababbb"  ->  3
s = "abcde"    ->  0
```

**Constraints:** `1 <= s.length <= 10^4`; `s` consists of lowercase
English letters.

Fix the letter counted most, `a`, and the one counted least, `b`: with
`a` as +1 and `b` as -1, the variance is the largest sum of a substring
that holds at least one `b`. Kadane's scan finds it in one pass, once
per ordered pair of letters present. O(k^2 n) for k letters used, or
O(k n) when each pair walks only its own letters.

## Approaches

| file | mechanism |
|---|---|
| `variance.kara` ★ | per ordered pair of letters present, two sums ending at each letter: `diff`, never below 0, and `with_b`, the best holding a `b`, seeded far below 0 |
| `variance_firstb.kara` | the editorial's scan: one running variance that restarts at -1 on a `b` that would take it below 0, remembering that it began with a `b` (`first_b`) so a later `b` drops that one instead |
| `variance_positions.kara` | the places of each letter listed once; a pair merges its two lists in order, so the scan visits only its own letters, O(k n) |
| `variance_struct.kara` | `struct Kadane` per pair, its letters, two sums and best; `feed` (`mut ref self`) takes a letter, and every pair is fed in one pass |
| `variance_iter.kara` | in chains: the letters present by `filter`, the ordered pairs by `flat_map`, each pair's best by a `fold` carrying `(diff, with_b, best)`, then `max` |
| `variance_solution.kara` | LeetCode's Rust template: `String` in, `i32` out; `as_bytes()`, each pair tested with `contains(&a)`, `diff_with_b` seeded at `-(s.len() as i32)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (two letters, 0; one `b` after four `a`, 3; one `b` among six
`a`, 5; a `b` at each end, 3; two letters alternating, 1), each with
its variance; then 2000 random strings of 1 to 40 letters from the
first 2, 3, 5 or 26, with a checksum; then three of the constraints'
longest, 10^4 letters: random from the first 5 (212), `a` with one `b`
in the middle (9998), and random from the first 3 (109).
`variance.py` mirrors the ★ arm and its output is byte-identical.

The ★ arm first ran every ordered pair of the 26 letters, present or
not, and with a random 10^4 letters from all 26 among the long cases
it took 42 s under the interpreter. Every arm now skips a pair whose
letters are not both in the string, as the template does with
`contains`, and the long random case draws from the first 5 letters.

The positions arm first bound `let pa = places[a];`, a move out of an
index. `karac check` explains that `places[a]` is a `ref Vec[i64]`
there, and since the binding is only read, `karac fix` writes `let pa
= ref places[a];`.

`karac fix` carries the template in one round, reporting 13 edits:
`as_bytes()` to `bytes()`, `let mut ans: i32 = 0` and `let mut diff:
i32 = 0`, which the `i32` return and `diff_with_b` name, the `||` to
`or` and `!` to `not`, `contains(&a)` to `contains(a)`, the pattern
`&c` to `c`, `struct Solution;` to `struct Solution {}`, `Solution::` to
`Solution.`, and the adapter's `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring, its letters counted, and the largest count
less the smallest among the letters it holds. No pairs and no running
sums. It checks 300 random strings of 1 to 12 letters from the first 2,
3, 4 or 26; then 30 of one letter with another put in once; then 30 of
runs of two letters. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the variance is the literal reading's |
| P2 | the string reversed: the same variance |
| P3 | the letters relabelled, the alphabet turned by seven: the same variance |
| P4 | at least 0 and at most the length less 2, and 0 for fewer than two letters |
| P5 | the string twice over: at least the same variance |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 608123394, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that takes
`max - min` of a `Counter` of every slice. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the b that opens a sum not counted | P1 318, P4 73, P6 318 |
| M4 | ★: only pairs in alphabetical order | P1 73, P3 7, P6 73 |
| M5 | ★: the best taken only at a b | P1 175, P2 149, P6 175 |
| M7 | firstb: the first b dropped whatever the variance | P1 8, P2 13, P6 8 |
| M8 | firstb: the restart at 0 | P1 188, P2 115, P4 31, P6 188 |
| M11 | firstb: a b counted twice | P1 126, P2 121, P6 126 |
| M12 | positions: the lists merged b first | P1 61, P6 61 |
| M13 | positions: the difference reset at a b | P1 17, P6 17 |
| M16 | positions: the walk stopped at either list's end | P1 156, P2 114, P6 156 |
| M17 | struct: the difference never floored | P1 45, P2 65, P6 45 |
| M18 | struct: the sum with a b lowered from itself | P1 260, P6 260 |
| M21 | struct: the least pair kept | P1 249, P6 249 |
| M22 | iter: the best not taken at an a | P1 148, P2 140, P6 148 |
| M25 | iter: other letters resetting the difference | P1 19, P2 33, P6 19 |
| M26 | iter: the sum with a b seeded at 0 | P1 121, P2 83, P4 31, P6 121 |
| M29 | solution: the plain difference scored | P1 183, P4 40, P6 183 |
| M30 | solution: the first letter skipped | P1 119, P2 115, P6 119 |

P1 and P6 kill all seventeen, P2 ten, P4 four, P3 one, and P5 none.
This kata's properties are weak, and P1 carries it. P2 catches the
edits that make the scan depend on its direction: a `b` that ends a
substring treated unlike one that starts it, a walk cut short, the
first letter skipped. P4 catches a variance with no `b` in it: a sum
with a `b` seeded at 0, a restart at 0, a `b` not counted, the plain
difference scored. P3 catches only the pairs taken in alphabetical
order, which relabelling reorders, and only in 7 cases, since the
variance usually comes from the more frequent letter whichever order
the pair is in. Doubling the string never lowers a wrong arm's answer
either.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Thirteen fail as a kept one does: the ★ arm's, the
iter arm's and the template's difference never floored (M1, M23, M27) as
the struct arm's (M17); the ★ arm's, the firstb arm's, the struct arm's
and the template's sum with a b seeded at 0 or scored before any b (M3,
M9, M19, M28) as the iter arm's (M26); the ★ and positions arms' sum
with a b not raised by an a (M6, M14) as the ★ arm's best taken only at
a b (M5); and the positions, struct, iter and template arms' pairs in
alphabetical order (M15, M20, M24, M31) as the ★ arm's (M4). One fails
in a way of its own and is left out because its arm keeps enough: the
firstb arm's first b never marked (M10).

Two edits of the first draft were replaced because they failed as
others did: the ★ arm's sum with a b lowered from itself, as the
struct arm's M18, and the template's sum with a b not raised by an a,
as the ★ arm's M5. They are now M2 and M30.

## Verification

Every arm prints the same output as `variance.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the positions arm takes 2.0 s, the
differential 3.6 s, the firstb and struct arms 4.0 s, the ★ arm 4.8 s,
the template 4.9 s, and the iter arm 6.1 s.

## Benchmarks

The bench answers 40 strings of the constraints' longest, 10^4 letters,
from the first 3, 5, 10 and 26 letters in turn, with the ★ arm in all
five languages. Every implementation prints `40 strings of 10^4:
checksum 995777966`. Each builds its string a letter at a time from the
same generator and scans every ordered pair of letters present.

BENCHTAB
