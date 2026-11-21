# 2434. Using a Robot to Print the Lexicographically Smallest String

You are given a string `s` and a robot that currently holds an empty
string `t`. Apply one of the following operations until `s` and `t`
**are both empty**:

- Remove the **first** character of a string `s` and give it to the
  robot. The robot will append this character to the string `t`.
- Remove the **last** character of a string `t` and give it to the
  robot. The robot will write this character on paper.

Return *the lexicographically smallest string that can be written on
the paper.*

```
s = "zza"   ->  "azz"
s = "bac"   ->  "abc"
s = "bdda"  ->  "addb"
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of only English
lowercase letters.

`t` is a stack. Its top should be written whenever no letter still in
`s` is smaller, because a smaller letter still to come is better put
first, and holding back a letter no larger than everything left can
only let a larger one in front of it. So after each letter moves to
`t`, the stack is popped while its top is at most the smallest letter
left in `s`; the ways of writing it differ in how that smallest letter
is known.

## Approaches

| file | mechanism |
|---|---|
| `robot.kara` ★ | the letters left in `s` counted in 26 places, a pointer kept at the smallest with a count, which only moves up, and the stack popped after each push while its top is no larger. O(n + 26) |
| `robot_naive.kara` | the greedy read directly: after each push, the smallest letter left found by scanning the rest of `s`. O(n^2) |
| `robot_suffix.kara` | suffix minima: `low[i]` the smallest letter from `i` on, built from the back with `z` past the end, and the stack popped while its top is at most `low[i + 1]`. O(n) |
| `robot_sorted.kara` | a `SortedMap[u8, i64]` of the letters left and their counts, a letter removed when its count reaches 0, so the smallest left is the map's `first` key. O(n log 26) |
| `robot_iter.kara` | iterators: the suffix minima by `scan` over the letters `rev`ersed, then the letters `zip`ped with the minima after them, each step `fold`ed into the stack and the paper. O(n) |
| `robot_solution.kara` | LeetCode's Rust template: `s.as_bytes()`, the suffix minima in `vec![b'z'; n + 1]`, and the stack popped by `while let Some(&c) = t.last()` into a `String::with_capacity(n)` by `push(c as char)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; one
letter; letters already in order; the alphabet backwards, which comes
out in order; a run of one letter with a smaller one last; `10^4`
random letters from 26 and the alphabet backwards over and over for
`10^4` letters, each as a checksum; and 3000 random words of 1 to 12
letters from the first 1 to 4, as a checksum of every answer's
checksum. The largest cases hold `10^4` letters, not the constraints'
`10^5`, because the naive arm scans the rest of `s` after every push.
`robot.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on every word of 1 to 8 letters from `abc`, 9840 of
them, against every sequence of the two operations.

`check` first reports 5 errors on the template, and `karac fix` carries
it in one call, reporting 9 edits: the brackets of `Vec<u8>`; `Vec::new`
and `String::with_capacity` written with `.`; the `&` of `Some(&c)`
dropped and `.cloned()` put on `t.last()`, the copy Kāra writes on the
value rather than in the pattern; `struct Solution;` given its braces;
and, once the template parses, `s.as_bytes()` written `s.bytes()` and
`vec![b'z'; n + 1]` written `Vec.filled(n + 1, b'z')`. The `while let`
loop, `t.pop()` as a statement, `break` and `c as char` stand as Kāra.

Two other spellings came up while writing the arms. The iter arm's
`scan` was first written as Rust has it, the state written in place by
`*m = (*m).min(c)`, which drew `E0200`: Kāra's `scan` closure takes
the state by value and returns `Some((next_state, item))`, and the
message gave that form. And the differential's `s.bytes()` is a
read-only `Slice[u8]`, so sorting or reversing a word's letters takes
`.to_vec()` first, as the messages said.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every sequence of the two operations tried by recursion,
moving the next letter of `s` to `t` or writing `t`'s last letter, and
the least paper among those that empty both kept. No greedy rule is
used. It checks 300 random words of 1 to 8 letters from the first 1 to
4; then 30 of 9 letters from 2; then 30 of 1 to 8 letters from the
first 25. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every letter raised by one: the answer raised by one |
| P3 | the answer holds the word's letters, each as often |
| P4 | the answer is no larger than the word itself |
| P5 | every letter raised by one and an `a` put after: `a`, then the raised word backwards |
| P6 | each arm agrees with at least three of the other five |

P2 holds because raising every letter keeps their order. P4 holds
because writing each letter as soon as it arrives is one of the
sequences, and it writes the word. P5 holds because no raised letter is
as small as the `a` still to come, so every letter waits on the stack
until the `a` arrives and is written first, and the stack then empties
from the top. The cases use at most 25 letters, so raising stays within
the alphabet.

The differential prints `360 cases: checksum 601325840, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every sequence. On a failure it prints the
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
| M1 | ★: a strictly smaller top only | P1 106, P4 25, P6 106 |
| M3 | ★: the pointer moved one at most | P1 95, P2 23, P3 87, P5 269, P6 95 |
| M5 | ★: the stack written from the bottom | P1 221, P5 360, P6 221 |
| M8 | naive: the last letter never scanned | P1 145, P5 360, P6 145 |
| M9 | naive: the largest left taken | P1 269, P2 176, P3 269, P5 360, P6 269 |
| M10 | naive: only the next letter looked at | P1 140, P5 298, P6 140 |
| M12 | suffix: the minimum from the front | P1 239, P3 202, P5 360, P6 239 |
| M15 | suffix: the end bound a | P1 269, P2 284, P3 269, P5 360, P6 269 |
| M16 | suffix: the minimum two on | P1 221, P4 12, P5 360, P6 221 |
| M17 | sorted: a count never removed | P1 239, P3 239, P5 360, P6 239 |
| M18 | sorted: the last key taken | P1 175, P5 298, P6 175 |
| M21 | sorted: a strictly smaller top only | P1 106, P2 4, P4 25, P5 4, P6 106 |
| M22 | iter: the minima never turned back | P1 65, P4 2, P6 65 |
| M24 | iter: the minima not skipped | P1 163, P3 145, P5 360, P6 163 |
| M26 | iter: the paper written in reverse | P1 239, P4 189, P5 360, P6 239 |
| M28 | solution: the letter just pushed written instead | P1 221, P3 221, P5 360, P6 221 |
| M31 | solution: the first letter pushed twice | P1 360, P3 360, P4 121, P5 360, P6 360 |


P1 and P6 kill all seventeen, P5 fifteen, P3 eight, P4 six and P2
four.

Fourteen are not kept. Twelve fail exactly as a kept one: the ★ arm's
count never taken down (M2) as the sorted arm's count never removed
(M17), both leaving a letter counted after it has gone; the ★ arm's one
letter written at most (M4) as the template's letter just pushed
written instead (M28); the naive arm's current letter in the scan, the
suffix arm's and the template's minimum at the letter itself (M7, M13,
M27) as the iter arm's minima not skipped (M24), each comparing with a
minimum that still holds the letter just pushed; the naive arm's and
the template's strictly smaller top only (M11, M30) as the sorted
arm's (M21); the suffix arm's letter itself left out and the iter arm's
maximum scanned (M14, M23) as the ★ arm's stack written from the bottom
(M5); the sorted arm's nothing left read as `a` (M19) as the naive
arm's largest left taken (M9); and the iter arm's state never carried
and the template's suffix minimum from `z` each time (M25, M29) as the
naive arm's only the next letter looked at (M10), each comparing with
the next letter alone. The ★ arm's strictly smaller top only (M1) fails
apart from the other arms' (M21): once no letter is left the ★ arm's
pointer stands past `z`, at 26, so the stack still empties at the end,
where the others compare with `z` and leave a `z` behind, which only
the raised words of P2 and P5 hold.

The ★ arm's pointer one letter high (M6) survives and is equivalent: the
pointer stops at 25 rather than 26 when no letter is left, and every
letter is no larger than `z`, so the stack empties either way. The
sorted arm's each letter counted once (M20) ends in `key not found`
under both backends, a letter's second copy reaching a key already
removed, a crash.

## Verification

Every arm prints the same output as `robot.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 to 0.9 s, but for the naive
arm, which takes 54 s there, 3.8 s under `karac __mir-llvm-asan` and
0.4 s under `karac run`: on the cases of `10^4` letters it scans `5 *
10^7` of them. The differential takes 5.3 s under `karac __mir-run`,
3.3 s under `karac __mir-llvm-asan` and 0.9 s under `karac run`.

## Benchmarks

The bench builds a word of `10^5` letters, the constraints' longest,
once from its own generator, from the first 8 letters. It then makes
300 passes; pass `p` sets one letter, so no answer can be carried from
one pass to the next, then answers the word and folds every letter of
the paper into the checksum. The bench uses the ★ arm, the counts and
the pointer, in all five languages. Every implementation prints `300
passes over 10^5 letters: checksum 753922089`. The stack and the paper
are fresh growable lists in every language (`Vec`, `Vec`, a slice by
`append`, a Python list), and in C buffers grown by doubling with
`realloc`.

BENCHTAB
