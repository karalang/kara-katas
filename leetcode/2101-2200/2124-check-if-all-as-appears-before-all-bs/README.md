# 2124. Check if All A's Appears Before All B's

Given a string `s` consisting of only the characters `'a'` and `'b'`,
return `true` if every `'a'` appears before every `'b'` in the string.
Otherwise, return `false`.

```
s = "aaabbb"  ->  true
s = "abab"    ->  false
s = "bbb"     ->  true
```

**Constraints:** `1 <= s.length <= 100`; `s[i]` is either `'a'` or
`'b'`.

Every a stands before every b exactly when no b stands right before an
a: a b anywhere before an a means that somewhere between them a b is
followed by an a. So the answer is that `"ba"` does not occur, or that
the last a comes before the first b, or that once the a's at the front
are skipped only b's are left.

## Approaches

| file | mechanism |
|---|---|
| `abba.kara` ★ | `not s.contains("ba")`. O(n) |
| `abba_scan.kara` | one pass over `bytes().iter().enumerate()` keeping the first b and the last a; in order when there is no b or the last a is before it |
| `abba_iter.kara` | `chars().skip_while(..)` past the a's, then `all(..)` the rest b's |
| `abba_sorted.kara` | the letters collected into a `Vec[char]`, sorted and collected back into a `String`; in order when that is the string. O(n log n) |
| `abba_struct.kara` | a `struct Reader { past_b }` whose `read` (`mut ref self`) remembers a b and refuses an a after it, through a `match` on the char |
| `abba_solution.kara` | LeetCode's Rust template: `s.find('b').map_or(true, \|i\| !s[i..].contains('a'))`, carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one a, one b, `"ba"`, `"ab"`), each with its answer; then the
strings in order and a checksum over 5000 random strings of 1 to 20
letters, every other one some a's then some b's with the pair at the
split perhaps swapped; then the constraints' longest, 50 a's then 50
b's, and the same with its middle pair swapped. `abba.py` mirrors the ★
arm and its output is byte-identical.

No compiler gap was met in the arms.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of positions compared, false when a b stands
before an a. It checks 300 random strings of 1 to 8 letters; then 30 of
up to 100 letters, some a's then some b's with one pair perhaps
swapped; then 30 of one letter repeated. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed with a and b swapped: the same answer |
| P3 | an a put in front: the same answer |
| P4 | a b put at the end: the same answer |
| P5 | the string written twice: in order exactly when the string is and has one letter only |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 strings: checksum 325433050, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
strings. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only `"bba"` refused | P1 107, P2 96, P5 83, P6 107 |
| M3 | ★: one letter only accepted | P1 58, P3 55, P4 59, P6 58 |
| M5 | ★: `"ba"` alone accepted | P1 13, P3 13, P4 13, P6 13 |
| M7 | scan: the last b kept, not the first | P1 93, P2 90, P4 95, P5 151, P6 93 |
| M10 | scan: a later b taken as an a | P1 73, P2 84, P4 40, P5 16, P6 73 |
| M11 | scan: the last a starting at 0 | P1 55, P2 114, P3 55, P6 55 |
| M12 | iter: the b's skipped instead | P1 117, P2 114, P3 55, P6 117 |
| M13 | iter: any b after the a's enough | P1 247, P2 114, P4 59, P5 246, P6 247 |
| M14 | iter: the first letter ignored | P1 39, P2 46, P3 39, P6 39 |
| M19 | sorted: only the first letter compared | P1 81, P2 90, P3 107, P5 139, P6 81 |
| M20 | sorted: the first letter dropped | P1 172, P6 172 |
| M21 | sorted: repeated letters merged | P1 110, P3 46, P4 29, P5 49, P6 110 |
| M22 | struct: a b never remembered | P1 188, P5 246, P6 188 |
| M23 | struct: an a allowed only after a b | P1 224, P2 204, P3 162, P5 107, P6 224 |
| M24 | struct: each b toggling the state | P1 40, P2 56, P5 51, P6 40 |
| M30 | solution: the part before the b searched | P1 165, P2 90, P3 162, P4 59, P5 107, P6 165 |
| M31 | solution: an a appended by the adapter | P1 113, P2 114, P4 59, P6 113 |

P1 and P6 kill all seventeen, P2 twelve, P5 ten, P3 nine and P4 eight.
P2 sees the edits that treat the front of the string unlike its back,
or the a's unlike the b's; it misses those that are wrong the same way
from both ends (M3, M5, M20, M21, M22). P3 and P4 see the edits that a
letter added where it cannot matter changes: a length tested (M3, M21),
the first or last place read wrongly (M11, M12, M14, M19), `"ba"` with
nothing around it (M5). P5 sees an answer that writing the string twice
does not turn false, which is any edit that accepts a b before an a it
should have refused.

Of the thirty-two, fifteen were not kept. Two are equivalent: the scan
arm allowing the last a at the first b, which no letter can be both,
and the Rust arm searching the rest after the b rather than from it,
which is a b. One survives and is not equivalent: the ★ arm refusing a
string of 100 letters, which the arm's own last line catches; every
in-order string the differential tests stays under 99 letters, so even
with a letter added it is never refused. Six fail as a kept one does:
the ★ arm refusing a final a after a b and the Rust arm finding the
last b as M7; the iter arm filtering out the a's, the sorted arm never
sorting and the struct arm accepting an a out of order as M22; and the
Rust arm finding the first a as M12. Six are killed with checks of
their own but were left out because their arms keep their share: the
edits that answer for the string read the other way (the ★ arm refusing
`"ab"`, the iter arm reading backwards, the sorted arm sorting
backwards, the struct arm taking the a's as the b's: P1 92, P3 89, P4
93, P6 92), and a string with no b answered false (the scan arm and the
Rust arm: P1 59, P2 114, P4 59, P6 59).

## Verification

Every arm prints the same output as `abba.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.14 s to 0.2 s and the
differential 0.28 s.

`karac fix` carries the template in two rounds of 4 and 2 edits: Rust's
spellings (`!` to `not`, `struct Solution;` to `struct Solution {}`,
`&str` to `Str`, `::` to `.`); then the char needles `'b'` and `'a'` of
`find` and `contains` to the strings `"b"` and `"a"`.

## Benchmarks

The bench builds 100000 strings of 100 letters once, each some a's then
some b's with a quarter of them given one letter out of order, then
checks every string 50 times, one string's letter flipped before each
round so that no round repeats one before, with the ★ arm in all five
languages. Every implementation prints `5000000 checks: 3776805 in
order, checksum 718624022`.

The first measurement of this bench found the ★ arm's `contains("ba")`
about six times slower than Rust's `str::contains` (0.42 s against
0.065 s on x86), nearly all of it the search: the same loop without it
took 0.03 s. A haystack over 64 bytes goes to karac's runtime, which
calls `memchr` for the needle's first byte and compares from each place
it finds; here the first byte, `b`, fills the second half of every
string, so each search made a call for each `b` before handing over to
a shift-table search whose 256-byte table it built each time. A needle
of two bytes now goes to a scan that compares both bytes at 32 places
at a time with no branch, which the compiler vectorizes, as Rust's
search does; the bench went from 0.38 s to 0.068 s on the same machine,
and katas 796 and 1016, whose longer needles keep the old search, did
not move (karac fa7746a0b2, `find_pair_agrees_with_a_naive_search` in
`runtime/src/mir.rs`).

BENCHTAB
