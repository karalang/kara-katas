# 2301. Match Substring After Replacement

You are given two strings `s` and `sub`. You are also given a 2D
character array `mappings` where `mappings[i] = [oldi, newi]` indicates
that you may perform the following operation **any** number of times:

- **Replace** a character `oldi` of `sub` with `newi`.

Each character in `sub` **cannot** be replaced more than once.

Return `true` *if it is possible to make* `sub` *a substring of* `s` *by
replacing zero or more characters according to* `mappings`. Otherwise,
return `false`.

A **substring** is a contiguous non-empty sequence of characters within
a string.

```
s = "fool3e7bar", sub = "leet", mappings = [["e","3"],["t","7"],["t","8"]]   ->  true
s = "fooleetbar", sub = "f00l", mappings = [["o","0"]]                       ->  false
s = "Fool33tbaR", sub = "leetd",
    mappings = [["e","3"],["t","7"],["t","8"],["d","b"],["p","b"]]           ->  true
```

**Constraints:** `1 <= sub.length <= s.length <= 5000`; `0 <=
mappings.length <= 1000`; `mappings[i].length == 2`; `oldi != newi`;
`s` and `sub` consist of uppercase and lowercase English letters and
digits; `oldi` and `newi` are either uppercase or lowercase English
letters or digits.

Each letter of `sub` is replaced at most once, so a mapping never
composes with another: a letter may stand for itself or for the new
letter of any mapping from it, and no more. A table of which letter may
stand for which, 128 by 128, answers each comparison at once; then every
start of `sub` in `s` is tried. O(n * k + m).

## Approaches

| file | mechanism |
|---|---|
| `match.kara` ★ | a `Vec[bool]` of 128 * 128 entries, set on the diagonal and for each mapping; every start tried over `bytes()`, the letters of `sub` looked up against the letters opposite them |
| `match_naive.kara` | every start tried over `Vec[char]`s, and for each letter that differs from the one opposite it the list of mappings searched. O(n * k * m) |
| `match_set.kara` | the mappings in a `Set[(char, char)]`; at each start a `while` runs on while each letter is equal to the one opposite or the pair is in the set |
| `match_mask.kara` | each letter's stand-ins as the bits of a `u128`, its own bit set and a mapping ORing in the new letter's; a start matches when `(0..k).all(..)` finds each opposite letter's bit set |
| `match_iter.kara` | the mappings `fold`ed into a `Map[char, Vec[char]]` with `entry(..).or_insert(Vec.new())`, then `s.windows(k)` searched with `any` for a window whose letters `zip`ped with `sub`'s are `all` equal or listed |
| `match_solution.kara` | LeetCode's Rust template: a `vec![vec![false; 128]; 128]` table indexed by `as usize` bytes and an `ok` flag for each start; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; `sub`
the whole of `s`; no mappings, matching only at the end; a chain of two
mappings, which does not compose; a letter mapped to itself; then 2000
random cases of `s` of 1 to 30 letters and `sub` of 1 to 8 but no
longer, both from `abcAB01`, with 0 to 12 mappings between those
letters, with the count that match and a checksum. `match.py` mirrors
the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 11 edits:
`struct Solution;` to `struct Solution {}`; the brackets of
`Vec<Vec<char>>`, whose closing `>>` is one edit; `vec![vec![false;
128]; 128]` to `Vec.filled(128, Vec.filled(128, false))`; `for p in
&mappings` to `for p in ref mappings`; `as_bytes()` to `bytes()` twice;
and `&&` and `!` to `and` and `not`.

The iterator arm was first written with `entry(old).or_default()`, as
Rust spells it. Kāra's `Entry` has `or_insert` and `or_insert_with`
(docs/library/collections.md), and `karac check` names the missing
method and offers `or_insert(Vec.new())`, which the arm writes.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: at each start, each letter of `sub` lists what it may
become, itself first and then the new letter of every mapping whose old
letter it is, and the letter of `s` opposite it must be in that list.
No table, no set, no bits. It checks 300 random cases drawn as the
arms' are, letters from `abcAB01`, up to 12 mappings; then 30 whose
`sub` is a window of `s` with some letters put back, at random, to the
old letter of a mapping that makes them, so that it matches; then 30
of `s` up to 200 letters, `sub` up to 30 and up to 40 mappings. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `s` with letters added at both ends: a match stays a match |
| P3 | the mappings in reverse order, each written twice: the same answer |
| P4 | `sub` a window of `s` from a third of the way in, with the same mappings: a match |
| P5 | a mapping from every letter to `Z`, which is in neither `s` nor `sub`: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 786512533, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and judges them with `all` over a set of pairs.
Of the 360, 102 match, the 30 built to among them. On a failure it
prints the first ten and then the count by property.

P5 as first drafted swapped the case of every letter in `s`, `sub` and
the mappings. No arm treats a capital unlike a small letter, so it
failed for none of the thirty-one mutations, and it was replaced by
mappings to a letter that never appears, which change nothing for an
arm that reads a mapping as the statement does.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the table transposed | P1 52, P6 52 |
| M5 | ★: no start tried after the first that fails | P1 80, P2 14, P4 323, P6 80 |
| M6 | ★: only the first mapping | P1 37, P3 12, P6 37 |
| M7 | naive: either half of a mapping enough | P1 196, P5 62, P6 196 |
| M10 | naive: the rest unchecked after an equal letter | P1 187, P6 187 |
| M11 | naive: every other start | P1 35, P2 27, P4 139, P6 35 |
| M14 | set: an equal letter needing a mapping too | P1 98, P4 350, P6 98 |
| M15 | set: the first start skipped | P1 7, P4 19, P6 7 |
| M16 | set: the first mapping dropped | P1 12, P3 12, P6 12 |
| M17 | mask: no letter standing for itself | P1 65, P4 322, P6 65 |
| M18 | mask: a mapping overwriting the mask | P1 48, P3 9, P4 259, P5 54, P6 48 |
| M21 | mask: the first letter unchecked | P1 49, P6 49 |
| M24 | iter: every window must match | P1 97, P2 5, P4 340, P6 97 |
| M25 | iter: the last mapping for a letter only | P1 19, P3 17, P5 28, P6 19 |
| M26 | iter: the window read backwards | P1 41, P4 230, P6 41 |
| M29 | solution: the last start skipped unless the lengths are equal | P1 6, P4 41, P6 6 |
| M31 | solution: every letter compared with the window's first | P1 53, P4 261, P6 53 |

P1 and P6 kill all seventeen, P4 ten, P3 four, and P2 and P5 three
each. P4, `sub` a window of `s`, fails wherever a match that needs no
mapping at all can be missed: a start skipped or never reached, a
letter not standing for itself, an equal letter asked for a mapping, a
window read backwards or compared with its first letter. P3, the
mappings reversed and each written twice, fails where an arm keeps only
some of them: the first only, the first dropped, the last for a letter
only, or each overwriting the mask. P2, `s` widened at both ends, fails
where an arm gives up on a match it would find farther in: no start
after the first failure, every other start, every window required. P5,
mappings to a `Z` that never appears, fails where a mapping is read by
its new letter alone or overwrites what came before it, and where the
last mapping for a letter hides the rest.

Of the thirty-one, fourteen were not kept. The table or the mappings
read backwards in the naive (M8), set (M12), mask (M19), iter (M23) and
template (M27) arms fail as the ★ arm's table transposed (M1); the ★
arm's letter not standing for itself (M2) as the mask arm's (M17); the
last start skipped in the ★ (M3), naive (M9) and mask (M20) arms and
the iter arm's windows one letter too long (M22) all alike, and none of
them is kept; the ★ arm's last letter of `sub` unchecked (M4) as the set
arm's match one letter short (M13), and neither is kept; the template's
equal letter needing a mapping (M28) as the set arm's (M14); and its
answer after the first start (M30) as the ★ arm's no start tried after
the first that fails (M5).

## Verification

Every arm prints the same output as `match.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the set, mask, naive and iterator arms take 0.4
to 0.6 s; the ★ arm 1.2 s and the template 1.8 s, since each call fills
a table of 16384 entries, 128 rows of 128 for the template, two thousand
times. The differential takes 4.2 s there and 0.7 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 50 cases once: `s` of 20000 letters from `ab`, `sub`
of 40 letters from `abc`, `c` half the time, and 1000 mappings, `c` to
`a` and `c` to `b` among them and the rest from `xyz` to `ab`, so that
a start fails after about four letters and 263 of the 1000 calls
find a match.
Then it makes 20 passes with the ★ arm in all five languages, pass `p`
matching case `c`'s `sub` and mappings against case `c + p`'s `s`.
Every implementation prints `20 passes over 50 cases of 20000 letters:
checksum 145316812`. C keeps the table in a static `bool` array cleared
with `memset` for each call, Rust and Go in a `Vec<bool>` and a
`[]bool` made for each call, and Python in a list.

BENCHTAB
