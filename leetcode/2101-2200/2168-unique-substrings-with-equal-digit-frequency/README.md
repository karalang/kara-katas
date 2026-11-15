# 2168. Unique Substrings With Equal Digit Frequency

Given a digit string `s`, return *the number of **unique substrings** of
`s` where every digit appears the same number of times.*

```
s = "1212"   ->  5     ("1", "2", "12", "21", "1212")
s = "12321"  ->  9
```

**Constraints:** `1 <= s.length <= 1000`; `s` consists of digits.

From each start the substring grows one digit at a time, and a count of
each digit, of the digits it has and of the most any one has says at
once whether it is even: every digit it has appears equally often
exactly when the most times the digits is its length. The even ones are
told apart by their text. O(n^2) substrings.

## Approaches

| file | mechanism |
|---|---|
| `equal.kara` ★ | from each start, the running counts, the digits and the most; each even substring into a `Set[String]`, whose size is the answer |
| `equal_hash.kara` | two polynomial hashes of each substring as it grows, modulo 10^9 + 7 and 998244353, and its length, in a `Set[(i64, i64, i64)]` instead of the text |
| `equal_trie.kara` | every substring from each start walked down a trie of the digits, ten children to a node in one flat `Vec[i64]`; a node counted when it is made, if its substring is even |
| `equal_tally.kara` | a `struct Tally` of a growing substring's digits, `add`ed to (`mut ref self`) and asked if it is `even`; every even substring pushed onto a `Vec[String]`, which is sorted and `dedup`ed |
| `equal_iter.kara` | for each start, the digits after it by `scan`, its state the count of each digit, giving whether each end is even; those `filter`ed, `map`ped to their text, and gathered from every start by `flat_map` into a `SortedSet[String]` |
| `equal_solution.kara` | LeetCode's Rust template: a `HashSet<&[u8]>` of slices of `s.as_bytes()`, `[0usize; 10]`, `(b[j] - b'0') as usize`, `mx.max(cnt[d])`, `seen.len() as i32`; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one digit, one digit repeated, every digit once, and two digits taking
turns), each with its count; then the total and a checksum over 2000
random strings of 1 to 20 digits, from 0 to 1, 0 to 2 or 0 to 9 in
turn; then the constraints' largest, 1000 digits at random from 0 to 9
and from 0 to 1, and the ten digits a hundred times over. `equal.py`
mirrors the ★ arm and its output is byte-identical.

The tally arm was carried by `karac fix` in one round of 2 edits: its
`[i64; 10]` field to `Array[i64, 10]`, and an `as i64` on a digit that
is one already dropped.

The iterator arm is written as Rust's `scan` is, writing the state
through `counts[..] += 1` and returning `Some(even)`, and `karac fix`
carries it in two rounds of one edit each: an `as i64` on the digit
dropped; then the closure rewritten to take the state by value, `let mut
counts = counts;` at its top and `Some((counts, even))` at its end, since
Kāra's `scan` closure returns the next state with the item. A state
written through an index was at first not rewritten, and drew a bare
type mismatch and four errors after it; that is ledger row
B-2026-11-14-64, fixed in karac 1617e3a972.

`karac fix` carries the template in four rounds of 10, 2, 3 and 3
edits: Rust's spellings (the `use` dropped, `HashSet<&[u8]>` to
`HashSet[Slice[u8]]`, `HashSet::new()` to `HashSet.new()`, the slice's
`&` dropped, `struct Solution;` to `struct Solution {}`, `&str` to `Str`
and `Solution::` to `.`, among them); then `HashSet` to `Set`, once the
`use` that named it is gone; then `as_bytes()` to `bytes()`, `let mut mx
= 0` to `let mut mx: usize = 0` for the `usize` counts it is compared
with, and the adapter's widening `as i64` dropped; then every `usize` to
`i64` (`[0usize; 10]`, `mx`, and `as usize`), since a program that mixes
`usize` with the default `i64` has every `as usize` go (B-2026-11-08-49).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring, its digits counted from scratch, kept in a
list if it is even and not in the list already, and the list's length.
It checks 300 random strings of 1 to 12 digits, from 0 to 1, 0 to 2 or
0 to 9 in turn; then 30 of two digits taking turns with one slip; then
30 of distinct digits. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the string reversed: the same count |
| P3 | every digit renamed by `d -> (3d + 7) mod 10`, which is one to one: the same count |
| P4 | the count at least the distinct digits, and at most n(n + 1)/2 |
| P5 | the string written twice: the count no less |
| P6 | each arm agrees with at least three of the other five |

P2 holds since a substring reversed has the same digits as often, and
the reversed string's substrings are the substrings reversed. P5 holds
since every substring of the string is one of the string twice.

The differential prints `360 strings: checksum 118912365, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
strings. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, four to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the most the latest count | P1 37, P2 34, P6 37 |
| M4 | ★: every substring at least even | P1 243, P6 243 |
| M26 | ★: the counts carried from the start before | P1 308, P2 136, P4 80, P6 308 |
| M6 | hash: the hashes of the last digit alone | P1 216, P2 109, P6 216 |
| M7 | hash: the most one under its count | P1 355, P4 250, P6 355 |
| M8 | hash: a kind counted at its second digit | P1 360, P4 213, P6 360 |
| M9 | trie: a substring counted every time it is walked | P1 254, P6 254 |
| M10 | trie: the walk never going down | P1 319, P2 144, P4 141, P6 319 |
| M11 | trie: 0 and 9 sharing a child | P1 36, P3 44, P6 36 |
| M16 | tally: the length grown only by a new digit | P1 211, P6 211 |
| M17 | tally: the text one digit short | P1 308, P2 59, P6 308 |
| M27 | tally: even when one digit is one over | P1 231, P6 231 |
| M19 | iter: every slot a kind | P1 360, P4 360, P6 360 |
| M20 | iter: the first start never taken | P1 318, P2 134, P4 57, P6 318 |
| M28 | iter: even when one digit is one short | P1 349, P4 212, P6 349 |
| M29 | solution: a single digit never counted | P1 360, P4 57, P6 360 |
| M30 | solution: the count one short | P1 360, P4 41, P6 360 |

P1 and P6 kill all seventeen, P4 nine, P2 six, P3 one and P5 none. P4
bounds the count by the distinct digits below and by the substrings
above, and sees an edit that loses single digits or counts too many;
it misses an edit whose count stays between, such as the ★ arm's every
substring at least even (M4), which counts more but never more than
there are. P2 reverses the string and sees an edit that reads one end
differently from the other: the most taken as the latest count (M3), the
counts carried over (M26), a hash of the last digit only (M6), the trie
never going down (M10), the text one digit short (M17), and the first
start skipped (M20). P3 renames the digits and sees only the
trie's 0 and 9 sharing a child (M11), the one edit that treats one digit
unlike another. P5 doubles the string, and every edit here still counts
at least as many on the longer one.

Of the thirty, thirteen were not kept. Five are equivalent. The hash
arm's key without the length (M5) still tells texts apart: each digit
enters its hashes as d + 1, so a text's hash is its numeral in bases 11
and 13 with no zero digit, and two texts of different lengths would have
to meet under both moduli at once. The trie's most started at 1 (M12) is
the most of a substring that has at least one digit already. The tally
arm's even by the length shared out (M15), `most == length / kinds`, is
the same test, since no digit has more than the most and so the length
is never more than the most times the digits. The iter arm's most read as the fewest of the digits it has
(M21) is the same test too: the fewest times the digits is the length
only when every digit has the fewest. And the template's adapter
reversing the string (M23) gives the same count, as P2 says. Eight fail
as a kept one does: the ★ arm's kind counted at every digit, and the
template's kind counted twice, as M16; the ★ arm's text one digit short,
the iter arm's each end one short, and the template's slice one digit
short, as M17; the tally arm's list never deduplicated or never sorted,
as M9; and the template's most the latest count, as M3.

## Verification

Every arm prints the same output as `equal.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, hash and template arms take 2.1 s to 2.6
s, the tally and trie arms 6.3 s and 6.6 s, and the iter arm 64 s, past
the corpus's 60 s cap: it builds a `scan` chain for each start of the
1000-digit strings, and the interpreter's adapters cost several times
the loops they stand for, which is filed as karac B-2026-11-14-62.
The differential takes 4.7 s.

## Benchmarks

The bench builds one string of 1000 digits from 0 to 2 once, then
solves it 200 times, each time after one digit is replaced, so that no
solve repeats one before, with the ★ arm in all five languages. Every
implementation prints `200 solves: checksum 142253529`.

BENCHTAB
