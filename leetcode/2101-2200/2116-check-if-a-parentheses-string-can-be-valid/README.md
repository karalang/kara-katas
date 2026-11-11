# 2116. Check if a Parentheses String Can Be Valid

A parentheses string is a non-empty string consisting only of `'('` and
`')'`. It is valid if any of the following conditions is true:

- It is `()`.
- It can be written as `AB` (`A` concatenated with `B`), where `A` and
  `B` are valid parentheses strings.
- It can be written as `(A)`, where `A` is a valid parentheses string.

You are given a parentheses string `s` and a string `locked`, both of
length `n`. `locked` is a binary string consisting only of `'0'`s and
`'1'`s. For each index `i` of `locked`, if `locked[i]` is `'1'`, you
cannot change `s[i]`; if `locked[i]` is `'0'`, you can change `s[i]` to
either `'('` or `')'`.

Return `true` if you can make `s` a valid parentheses string. Otherwise,
return `false`.

```
s = "))()))", locked = "010100"  ->  true
s = "()()",   locked = "0000"    ->  true
s = ")",      locked = "0"       ->  false
```

**Constraints:** `n == s.length == locked.length`; `1 <= n <= 10^5`;
`s[i]` is `'('` or `')'`; `locked[i]` is `'0'` or `'1'`.

A string balances when no prefix closes more than it opens and the whole
closes as much as it opens. With some positions free, an odd length
never balances; otherwise two greedy passes decide it. Left to right,
treat every free position as `(`: if even then a prefix has more locked
`)` than it can open, nothing helps. Right to left, the same with every
free position a `)`. When both hold, a choice exists, which is what the
range arm makes explicit by tracking the least and the most the open
count can be.

## Approaches

| file | mechanism |
|---|---|
| `valid.kara` ★ | two greedy passes over `bytes()`, forward counting `(` and free positions against locked `)`, backward the reverse; O(n), O(1) space |
| `valid_range.kara` | one pass over `chars().zip(..)` keeping `lo` and `hi`, the least and the most the open count can be, `lo` clamped at zero with `max`; valid when `lo` ends at zero. O(n) |
| `valid_stacks.kara` | a stack of locked `(` positions and one of free positions; a locked `)` pops a locked `(` first, then a free one; at the end each locked `(` left needs a free position after it, and the free ones left pair up. O(n) |
| `valid_iter.kara` | the ★ arm's passes as `all` over a `Vec[(u8, u8)]` of zipped bytes, the balance a `mut` captured by the closure, the backward pass over `rev().collect()` |
| `valid_struct.kara` | a `struct Pass { opener, balance }` with a `feed` method (`mut ref self`); one `Pass` fed forward and one backward in the same loop |
| `valid_solution.kara` | LeetCode's Rust template: the two passes over `as_bytes()`, carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (a pair locked backwards, all free, a locked `(` with only free
positions after it, an odd length), each with its answer; then the
number that can be valid among 4000 random strings of 1 to 24
characters, each position locked with chance one half, and a checksum;
then the constraints' largest, 100000 locked `)` with the first half
free, and with one fewer free. `valid.py` mirrors the ★ arm and its
output is byte-identical.

Three arms were first written with Rust's spellings and carried by
`karac fix`: the ★ arm in two rounds (`||` to `or`, then `as_bytes()` to
`bytes()`, which the parse errors held back), the struct arm in one
(`!` to `not`), and the template as below.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of choosing the free positions tried one by one
(depth first, a choice dropped once its prefix closes more than it
opens), valid when one of them balances. It checks 300 random strings of
1 to 12 characters, each position locked with chance one half; then 30
of even length up to 40 with at most 10 free positions; then 30
balanced strings of up to 30, half with one bracket flipped, also with
at most 10 free. All 360 are drawn before any arm answers; 91 of them
can be valid.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string read backwards with `(` and `)` swapped: the same answer |
| P3 | the first free character flipped: the same answer |
| P4 | a locked `()` appended: the same answer |
| P5 | a true answer stays true with the string wrapped in a locked `(` and `)`, and with its first locked position freed |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 strings: checksum 614239360, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
strings by the same enumeration. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-two edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd length let through | P1 71, P6 71 |
| M3 | ★: the forward pass blind to free positions | P1 48, P2 45, P3 49, P6 48 |
| M4 | ★: the forward pass allowed one short | P1 33, P2 55, P6 33 |
| M6 | range: `lo` not clamped | P1 31, P2 70, P6 31 |
| M9 | range: a free position only opens | P1 80, P2 19, P5 4, P6 80 |
| M10 | range: `hi` checked only at the end | P1 39, P2 70, P6 39 |
| M11 | stacks: the order of an open and its partner ignored | P1 27, P2 65, P6 27 |
| M13 | stacks: a close takes a free position first | P1 27, P2 25, P4 53, P5 25, P6 27 |
| M14 | stacks: a close with nothing to match let through | P1 50, P2 93, P5 35, P6 50 |
| M16 | iter: the backward pass dropped | P1 40, P2 95, P6 40 |
| M18 | iter: the balance starts at one | P1 68, P6 68 |
| M20 | iter: a free position counted as closing | P1 87, P5 4, P6 87 |
| M22 | struct: the backward pass fed forward | P1 62, P2 73, P4 3, P5 63, P6 62 |
| M23 | struct: the balance never lowered | P1 124, P6 124 |
| M24 | struct: the free flag read backwards | P1 80, P2 126, P3 63, P5 48, P6 80 |
| M28 | solution: the backward pass counts `(` | P1 74, P2 108, P4 77, P5 77, P6 74 |
| M31 | solution: the backward pass blind to free positions | P1 33, P2 45, P3 14, P6 33 |

P1 and P6 kill all seventeen, P2 thirteen, P5 seven, P3 and P4 three.
P2 sees every edit that treats the two passes unequally, since the
mirror swaps them; it misses only the edits blind to direction (the odd
length, a balance off by one or never lowered, a free position always
closing). P3 sees the edits that read a free position's character,
which no correct arm does (M3, M24, M31). P4 sees the edits that care
what follows the string: a close taking a free position before a
locked open (M13), the backward pass fed in the forward order (M22),
and counting `(` backwards (M28). P5 sees the edits that answer false
for a string a freed or wrapped copy shows to be fine.

Of the thirty-two, fifteen were not kept. Three are equivalent, each
dropping the last step of a pass: the ★ arm's backward pass skipping
position 0, the struct arm's last position never fed, and the Rust
arm's last close never checked. That step can fail only when everything
before it balances exactly and the position is locked against the
pass, which makes the length odd, and the odd length was refused
already. Ten fail as a kept one does: the odd length let through in the
range, stacks (the free positions' parity), iter and Rust arms as M1;
the backward pass dropped in the ★, struct and Rust arms, and the range
arm's end test on `hi`, as M16; the iter arm's backward pass in forward
order as M22; and the Rust arm's forward pass one short as M4. The
stacks arm's locked opens never checked (P1 89, P2 159, P5 59) and the
Rust arm's forward pass from the second position (P1 64, P2 80, P5 29)
are killed with checks of their own but were left out because their
arms keep their share.

## Verification

Every arm prints the same output as `valid.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 s to 2.0 s, the iter arm the
slowest, and the differential 0.7 s; compiled it takes 0.5 s.

`karac fix` carries the template in two rounds of 3 and 2 edits: the two
`||` to `or` and `Solution::can_be_valid` to `Solution.can_be_valid`;
then the two `as_bytes()` to `bytes()`. No compiler gap was met.

## Benchmarks

The bench builds 64 strings of 50000 characters once, each a balanced
random walk, half with one bracket flipped, every other one fully
locked and the rest with a quarter of their positions free; it then
solves each string 40 times, appending a locked `()` before each solve
so no solve repeats the one before, with the ★ arm in all five
languages. Every implementation prints `2560 solves: 1880 can be valid,
checksum 466901817`.

BENCHTAB
