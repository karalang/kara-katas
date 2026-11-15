# 2182. Construct String With Repeat Limit

You are given a string `s` and an integer `repeatLimit`. Construct a new
string `repeatLimitedString` using the characters of `s` such that no
letter appears **more than** `repeatLimit` times **in a row**. You do
**not** have to use all characters from `s`.

Return *the **lexicographically largest*** `repeatLimitedString`
*possible*.

A string `a` is **lexicographically larger** than a string `b` if in
the first position where `a` and `b` differ, string `a` has a letter
that appears later in the alphabet than the corresponding letter in
`b`. If the first `min(a.length, b.length)` characters do not differ,
then the longer string is the lexicographically larger one.

```
s = "cczazcc", repeatLimit = 3  ->  "zzcccac"
s = "aababab", repeatLimit = 2  ->  "bbabaa"
```

**Constraints:** `1 <= repeatLimit <= s.length <= 10^5`; `s` consists
of lowercase English letters.

Greedy: the largest letter left goes next, as many times as the limit
allows; if some of it is still left, one of the next largest goes
between, so that it can run again. When nothing smaller is left to go
between, the rest of the largest cannot be used, and the string ends.
O(n + 26).

## Approaches

| file | mechanism |
|---|---|
| `repeat_limit.kara` ★ | the letters counted in a `Vec.filled(26, 0)`, the largest left written up to the limit, and one of the next largest between |
| `repeat_limit_heap.kara` | each letter and its count in a `PriorityQueue.max_first()`: the largest popped and written up to the limit, the next largest popped for one letter between, each pushed back while any is left; `while let` and `let .. else` |
| `repeat_limit_sorted.kara` | the bytes sorted largest first with `sort` and `reverse`, then walked with a run count; a letter that would run past the limit `swap`ped with the first smaller one further on, found by a second index that only moves forward, and the rest `truncate`d where none is left; `String.from_utf8` |
| `repeat_limit_struct.kara` | a `struct Tally` of the letters left, made `of` a string, that finds the `largest_below` a letter (`ref self`, an `Option`) and `take`s up to some of one (`mut ref self`), saying how many it took |
| `repeat_limit_iter.kara` | the counts by `fold`; each step `find`s the largest letter left over a `rev`ersed range, writes its run `collect`ed into a `String` from a `map`, and `find`s the next largest below it for the letter between |
| `repeat_limit_solution.kara` | LeetCode's Rust template: `[0usize; 26]` counts, `(b - b'a') as usize` indices, two `i32` cursors for the largest letter and the one between, a `Vec<u8>` of `b'a' + i as u8`, `String::from_utf8(..).unwrap()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and five
more (one letter, one letter past its limit, a limit of one with no
repeats, two letters taking turns, and the largest letter run out with
the next one left over), each with its string; then the letters kept
and a checksum over 2000 random strings of 1 to 30 letters, from a to c
or a to z in turn, with a limit of 1 to 5; then the constraints'
largest, 10^5 letters: at random with a limit of 1, and all z but one a,
with limits of 1, 50000 and 100000. `repeat_limit.py` mirrors the ★ arm
and its output is byte-identical.

`karac fix` carries the template in one round of 8 edits: `Vec<u8>` to
`Vec[u8]`, `Vec::new()` and `String::from_utf8` to `.`, the two `&&` to
`and`, `struct Solution;` to `struct Solution {}`, and `Solution::` to
`.`. Its `usize` counts stay: the counts, the limit and the indices are
all `usize`, so none of them mixes with an `i64`.

The ★ arm's checksum was written `t.bytes().fold(..)`, and `karac fix`
adds the `.iter()` that a `Slice` needs before an adaptor.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every string that can be made from some of the letters, no
letter more than the limit times in a row, built letter by letter by a
recursion, and the largest of them all kept. No counting down from the
largest letter and no greedy step. It checks 300 random strings of 1 to
6 letters from a to c or a to e in turn, with a limit of 1 to 3; then
30 of one letter; then 30 with a limit of 6. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the string is the statement read literally |
| P2 | the letters reversed: the same string |
| P3 | a limit of the length: every letter, largest first |
| P4 | every letter 21 later in the alphabet, a to e made v to z: the string 21 later too |
| P5 | the string uses no more of a letter than there is, runs no letter past the limit, and starts with the largest letter |
| P6 | each arm agrees with at least three of the other five |

P2 holds since the answer depends only on how many of each letter there
are. P3 holds since with a limit of the length no run is too long, and
the largest string of them all is every letter, largest first. P4 holds
since moving every letter by the same amount keeps their order. P5
holds since the answer is one of the strings the statement allows, and
the largest letter of all can always come first.

The differential prints `360 strings: checksum 814926668, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
strings. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, five to each Kāra arm and three
to the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one more than the limit taken | P1 107, P5 107, P6 107 |
| M4 | ★: the rest given up once it runs on | P1 62, P6 62 |
| M5 | ★: z never looked at | P4 96 |
| M6 | heap: the smallest letter first | P1 241, P3 241, P5 241, P6 241 |
| M8 | heap: the largest pushed back with one more | P1 47, P5 47, P6 47 |
| M10 | heap: a remainder of one never pushed back | P1 53, P5 22, P6 53 |
| M13 | sorted: the second index never moved past the first | P1 52, P5 45, P6 52 |
| M14 | sorted: the letter past the limit kept at the end | P1 64, P5 64, P6 64 |
| M15 | sorted: a run swapped with the last letter | P1 33, P5 2, P6 33 |
| M17 | struct: at most 2 taken | P1 28, P3 85, P6 28 |
| M18 | struct: the top left below the largest after a letter between | P1 62, P5 23, P6 62 |
| M19 | struct: a used-up letter's neighbour skipped | P1 170, P3 183, P6 170 |
| M21 | iter: a never the largest | P1 180, P3 196, P4 180, P5 29, P6 180 |
| M24 | iter: the run one short | P1 360, P3 360, P5 268, P6 360 |
| M25 | iter: each letter counted twice | P1 292, P3 241, P5 292, P6 292 |
| M26 | solution: the second cursor never brought below the first | P1 107, P4 16, P5 107, P6 107 |
| M28 | solution: the second cursor from x | P4 7 |

P1 and P6 kill fifteen, P5 twelve, P3 six, P4 four and P2 none. P2
reverses the letters, and every arm reads only how many of each there
are, so no edit sees the order. Two edits are seen by P4 alone: z never
looked at (M5) and the template's second cursor starting from x (M28),
since the differential's own strings use a to e only, and P4 moves them
to v to z. P4 also sees an edit that treats a letter's place in the
alphabet apart: a never the largest (M21), and the second cursor left
above the first (M26). P3 asks for every letter, largest first, and
sees an edit that drops letters without breaking the rule, or writes
them out of order: at most 2 taken (M17), a letter skipped (M19), the
run one short (M24), the smallest first (M6), a never the largest
(M21), and every letter counted twice (M25). P5 misses an edit that
stays a valid string but not the largest: the rest given up (M4), at
most 2 taken (M17), and the skipped neighbour (M19), besides the two
that P4 alone sees.

Of the twenty-eight, eleven were not kept, none of them equivalent. Six
fail as a kept one does: the ★ arm's letter between sought from the
largest itself, the sorted arm's run counted from 0, the struct arm's
largest at most the top, the iter arm's letter between sought from the
largest, and the template's adapter limit one more, as M1, each letting
a run go one past the limit; and the sorted arm never reversed, as M6.
Five were left out to keep three to an arm: the ★ arm's letter between
sought two below (M3), the heap arm's letter between used up at once
(M7) and one left over dropped (M9), the struct arm's two taken for the
letter between (M20), and the iter arm's letter between never counted
off (M23).

## Verification

Every arm prints the same output as `repeat_limit.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, sorted, struct and template arms take
0.9 s to 1.0 s, and the heap and iter arms 2.1 s and 2.2 s. The
differential takes 0.7 s.

## Benchmarks

The bench builds one row of 10^6 random letters once; then solves 400
windows of 10^5 letters, the constraints' longest, each at a random
start and with a limit of 1 to 3, so that no solve repeats one before,
with the ★ arm in all five languages, and folds every letter of every
answer into a checksum. C works over a pointer and a length, Rust and
Go over a slice of the row; Kāra and Python copy each window into a
string of its own, as the ★ arm takes a `String`. Every implementation
prints `400 solves: checksum 915609220`.

BENCHTAB
