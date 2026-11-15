# 2207. Maximize Number of Subsequences in a String

You are given a **0-indexed** string `text` and another **0-indexed**
string `pattern` of length `2`, both of which consist of only lowercase
English letters.

You can add **either** `pattern[0]` **or** `pattern[1]` anywhere in
`text` **exactly once**. Note that the character can be added even at
the beginning or at the end of `text`.

Return *the **maximum** number of times* `pattern` *can occur as a
**subsequence** of the modified* `text`.

A **subsequence** is a string that can be derived from another string by
deleting some or no characters without changing the order of the
remaining characters.

```
text = "abdcdbc", pattern = "ac"  ->  4
text = "aabb", pattern = "ab"     ->  6
```

**Constraints:** `1 <= text.length <= 10^5`; `pattern.length == 2`;
`text` and `pattern` consist only of lowercase English letters.

A first letter is worth most at the front, where it pairs with every
second letter, and a second letter at the end, where it pairs with every
first; so one pass counts each letter and the pairs so far, and the
answer is the pairs plus the larger count. Checking the second letter
before counting the first keeps a pattern of one letter twice right.
O(n).

## Approaches

| file | mechanism |
|---|---|
| `subsequences.kara` ★ | one pass over `chars()` with three running counts: the first letters so far, the second letters, and the pairs, each second letter adding the first letters before it |
| `subsequences_prefix.kara` | the letters as a `Vec[char]`, a prefix count of the first letter before each index, summed at every second letter; then the front and the end compared |
| `subsequences_insert.kara` | the two best texts built as `String`s, the first letter pushed at the front and the second at the end, each counted by a pass that knows nothing of the addition |
| `subsequences_struct.kara` | a `struct Tally` fed one letter at a time, keeping its counts and pairs, then asked for its best with one letter added |
| `subsequences_iter.kara` | one `fold` over the letters carrying the two counts and the pairs as a tuple |
| `subsequences_solution.kara` | LeetCode's Rust template: two `String`s in, `i64` out, the pattern by `as_bytes()` and one pass over `text.bytes()`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and four more
(a pattern of one letter twice, a text holding neither letter, the second
letter only, and the second letter before every first), each with its
answer; then the largest answer and a checksum for 3000 random texts of 1
to 30 letters from 2, 3 and 26; then the constraints' largest, 50000 a
then 50000 b, and 10^5 a with "aa" and with "ba". `subsequences.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in two rounds of 5 and 4 edits: first
`let (mut a, mut b, mut ans)` to `let mut (a, b, ans)` and `struct
Solution;` to `struct Solution {}`; then `as_bytes()` to Kāra's
`bytes()` and the three `0i64` to `0`.

The arms read the pattern's letters by `pattern.chars().collect()` into
a `Vec[char]` and index it. A first draft wrote `pattern.char_at(0)`,
which is an `Option[char]`, and compared a letter with it; the check
refuses that, rightly, with no edit to offer, since which of
`.unwrap()` or a match is meant is the author's call.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each pattern letter put at every position of the text in
turn, and each text so made counted by every pair of indices i < j
holding the pattern's two letters; no running count. It checks 300
random texts of 1 to 12 letters from 2, 3 and 26 in turn, the pattern
from the same letters; then 30 whose pattern is one letter twice; then 30
of 20 to 30 letters from 3. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | it is at least how often either pattern letter appears, and at most the pairs among n + 1 letters |
| P3 | the text reversed and the pattern's letters swapped: the same |
| P4 | every letter not in the pattern made another not in it: the same |
| P5 | one more of the pattern's second letter appended: at least one more |
| P6 | each arm agrees with at least three of the other five |

The harness picks P4's spare letter as the first of x, y and z not in
the pattern, binding the list first: `['x', 'y', 'z'].iter()...` in one
`let` keeps a reference into a temporary, which the check refuses with
its reason (core semantics §5.5), as Rust does.

The differential prints `360 cases: checksum 985335608, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that inserts
each letter by slicing and counts by `itertools.combinations`. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-nine edits to the differential, seven to the ★ arm, five to the
prefix arm and to the template arm, six to the insert arm, and eight to
the struct and iter arms, each run under `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two
to the Rust-template arm. Each kept one is killed, fails the same way
under both backends and not by a crash, and no two kept ones fail the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first letter counted before the second is checked | P1 101, P2 6, P6 101 |
| M5 | ★: the pattern's letters swapped | P1 118, P5 94, P6 118 |
| M6 | ★: no letter added | P1 283, P2 131, P5 96, P6 283 |
| M8 | prefix: nothing gained at the front | P1 65, P2 24, P3 159, P5 80, P6 65 |
| M9 | prefix: the prefix counting the second letter | P1 159, P2 61, P3 159, P6 159 |
| M10 | prefix: the last letter never read as a second | P1 101, P2 7, P3 129, P5 185, P6 101 |
| M13 | insert: the first letter put at the end of the second text | P1 94, P2 43, P3 159, P6 94 |
| M14 | insert: a first letter counted before the second is checked | P1 117, P2 6, P6 117 |
| M16 | insert: the back text counted with the letters swapped | P1 98, P2 37, P3 131, P5 13, P6 98 |
| M22 | struct: every letter fed twice | P1 283, P2 93, P6 283 |
| M34 | struct: a first letter seen at all counted once | P1 175, P2 34, P3 124, P6 175 |
| M35 | struct: the seconds starting at 1 | P1 266, P2 7, P3 159, P6 266 |
| M27 | iter: the firsts starting at 1 | P1 360, P2 18, P3 79, P6 360 |
| M36 | iter: the firsts reset by any other letter | P1 200, P2 37, P3 122, P6 200 |
| M39 | iter: a letter before 'n' taken as the first | P1 269, P3 187, P4 269, P6 269 |
| M30 | solution: both counts added | P1 233, P2 6, P6 233 |
| M32 | solution: the pairs on the first letter | P1 147, P2 41, P3 159, P5 243, P6 147 |

P1 and P6 kill all seventeen, P2 fifteen, P3 eleven, P5 six and P4 one.
P2 misses the ★ arm's letters swapped (M5) and the iter arm's letters
before n taken as first (M39), whose answers stay within the bounds. P3
reverses the text and swaps the letters, and misses the six edits that
treat the two ends alike: the counts taken in the wrong order (M1, M14),
the letters swapped (M5), no letter added (M6), every letter fed twice
(M22) and both counts added (M30). P4 changes only letters outside the
pattern, so it kills only the edit that reads one (M39). P5 appends a
second letter and kills the six whose answer then fails to grow (M5,
M6, M8, M10, M16, M32).

Of the thirty-nine, twenty-two were not kept, and every one is killed;
none crashes, none differs between the backends, and none is
equivalent. Seventeen fail as a kept one does: the first letter counted
before the second is checked in the struct, iter and template arms and
the prefix taken through index j (M18, M25, M31, M7) as M1; the only
second letter added at the end in the ★ arm, the first letter put at the
end and nothing put at the front in the insert arm, the seconds never
counted in the struct arm and counted on the first letter in the iter
arm (M3, M12, M17, M19, M24) as M8; the struct arm's tally with the
letters swapped (M21) as M5; the insert arm's front text alone and the
template's second letter alone at the end (M15, M33) as M13; and the
iter arm's seconds starting at 1 (M37) as M35. Four fail alike and none
is kept: the smaller count added in the ★, struct and iter arms and the
prefix arm's worse end (M2, M20, M28, M11). Four more fail alike, each
second letter adding the seconds so far in the ★, struct and template
arms and the iter arm's pairs grown by the seconds (M4, M23, M29, M26).
The ★ arm's every letter but the first taken as second (M38) fails its
own way and is left out for the count of three. M34 to M39 were added
when the first thirty-three left the struct and iter arms one distinct
signature each, and P4 none.

## Verification

Every arm prints the same output as `subsequences.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output
for every arm and the differential. `karac check --output=json` reports
nothing on any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 s to 0.9 s and the
differential 0.7 s.

## Benchmarks

The bench builds 12 texts of 10^5 letters once, from 2, 3 and 26 letters
in turn, then answers each 50 times over with the ★ arm in all five
languages, every pass asking each text about its own pattern. Every
implementation prints `50 passes over 12 texts: checksum 449083032`.

BENCHTAB
