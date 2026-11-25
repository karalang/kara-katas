# 1374. Generate a String With Characters That Have Odd Counts

Given an integer `n`, return a string with `n` characters such that
each character in such string occurs an odd number of times.

The returned string must contain only lowercase English letters. If
there are multiple valid strings, return any of them.

```
n = 4  ->  "pppz"
n = 2  ->  "xy"
n = 7  ->  "holasss"
```

**Constraints:** `1 <= n <= 500`.

Each arm is `fn generate_the_string(n: i32) -> String`.

## Approaches

Any valid string is accepted, so every arm here gives the same one: the
smallest in dictionary order. For an odd `n` that is `n` a's. For an
even `n`, `n` a's hold an even number of a's, and the next string in
dictionary order, `n - 1` a's and a `b`, is valid. LeetCode's examples
read `aaab`, `ab` and `aaaaaaa` here.

| file | mechanism |
|---|---|
| `generate_the_string.kara` ★ | `"a".repeat(n)` for an odd `n`, and `"a".repeat(n - 1) + "b"` for an even one. O(n) |
| `generate_the_string_counts.kara` | how many of each letter the answer holds, in an `Array[i32, 26]`, then the letters written out in order with `String.push`. O(n) |
| `generate_the_string_greedy.kara` | each place takes the smallest letter after which the rest can still be filled: the places left must give one more to every letter held an even number of times, and any extra must come in pairs or start a letter not yet used. O(26² n) |
| `generate_the_string_bytes.kara` | `n` bytes of `a` in a `Vec[u8]`, the last made a `b` when `n` is even, and the bytes read by `String.from_utf8`. O(n) |
| `generate_the_string_solution.kara` | a Rust solution as LeetCode's Rust users write it (`"a".repeat((n - 1) as usize)`, then `s.push(if n % 2 == 0 { 'b' } else { 'a' })`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples (`aaab ab
aaaaaaa`), and the strings for every `n` from 1 to 500, folded into a
checksum (`n from 1 to 500: 125250 letters, 250 b's, checksum
614920486`). `generate_the_string.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, greedy and bytes arms check clean as first
written. The counts arm, written with Rust's `[i32; 26]` for the type,
takes one round of 2 fixes, the two edits that make it `Array[i32,
26]`. The Rust solution takes one round of 3 fixes by `karac fix`'s
count, from 2 parse errors: `struct Solution;` to `struct Solution {}`,
`Solution::` to `Solution.`, and `as usize` to `as i64`. Every arm
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the strings of `n` lowercase letters counted through in
dictionary order from `n` a's, and the first in which every letter that
appears does so an odd number of times. It checks every `n` from 1 to
500, the constraints' range, LeetCode's three among them.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | `n` letters, all lowercase, each that appears an odd number of times |
| P3 | for `n + 2`, the same string after two a's |
| P4 | any one letter but an `a` made the letter before it, the string no longer valid |
| P5 | the letters in order, never falling |
| P6 | the ★ arm's string |

All 15,000 checks pass on every arm: `500 cases: checksum 614920486,
15000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, counting through the strings
the same way, gives the same checksum, the harness's own.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks. One first edit was replaced: the solution's last
letter left off for an odd `n` failed P1, P2 and P6 on 250 checks each,
as the greedy arm's edit does, though on the odd `n` where that one
fails on the even.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the two parities swapped | P1 500, P2 499, P4 250, P6 2000 |
| M2 | ★: the b put first | P1 250, P3 250, P5 250, P6 1000 |
| M3 | counts: a `c` in place of the `b` | P1 250, P4 250, P6 250 |
| M4 | counts: the a's not cut by one for the `b` | P1 250, P2 250, P4 250, P6 250 |
| M5 | greedy: an odd number of places left never filled by a new letter | P1 250, P2 250, P6 250 |
| M6 | greedy: an unused letter counted as held an even number of times | P1 500, P2 262, P3 25, P6 500 |
| M7 | bytes: only a multiple of 4 given the `b` | P1 125, P2 125, P3 250, P6 125 |
| M8 | bytes: a capital `B` | P1 250, P2 250, P5 250, P6 250 |
| M9 | solution: `n` a's before the last letter | P1 500, P2 500, P4 250, P6 500 |
| M10 | solution: the last letter always a `b` | P1 250, P2 249, P4 250, P6 250 |

P1 and P6 kill all ten, P2 eight, P4 five, P3 three and P5 two. Validity
(P2) misses only the two edits whose strings are still valid, just not
the smallest: the `b` put first (M2) and a `c` for the `b` (M3).
Lowering a letter (P4) catches the edits that leave a letter higher than
it need be, a `c` (M3), or a `b` where an `a` would do (M10); and those
whose string holds an even run of a's, which one lowered `b` makes odd
and valid again (M1, M4, M9). Two letters more (P3) catches the edits
that treat `n` and `n + 2` differently: the `b` moved to the front by
the two a's (M2), a `b` only every fourth `n` (M7), and the greedy arm
counting the unused letters among those held an even number of times,
which then leaves every `n` below 26 empty (M6). Order (P5) catches a
`b` ahead of the a's (M2), and a capital `B`, which sorts before them
(M8).

## Benchmarks

The bench makes 10^7 rounds, each making the string for an `n` from 1
to 500, the constraints' range, drawn from the checksum so far, and
reading its length and one letter at a place drawn the same way, with
the ★ arm. Every implementation prints `10000000 rounds: checksum
772263524`. The work is one heap string of up to 500 bytes a round,
filled and freed, the same in every language; C fills a `malloc`
buffer with `memset`, Rust and Go use their own `repeat`.

BENCHTAB
