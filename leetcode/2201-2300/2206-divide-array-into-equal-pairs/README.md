# 2206. Divide Array Into Equal Pairs

You are given an integer array `nums` consisting of `2 * n` integers.

You need to divide `nums` into `n` pairs such that:

- Each element belongs to **exactly one** pair.
- The elements present in a pair are **equal**.

Return `true` *if nums can be divided into* `n` *pairs, otherwise
return* `false`.

```
nums = [3,2,3,2,2,2]  ->  true
nums = [1,2,3,4]      ->  false
```

**Constraints:** `nums.length == 2 * n`; `1 <= n <= 500`;
`1 <= nums[i] <= 500`.

The array divides into pairs of equals exactly when every number appears
an even number of times, so a count per value and one pass over the
counts answer it. O(n + 500).

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | a count table of 501 by `Vec.filled`, then the first odd count answers `false` |
| `pairs_sort.kara` | a sorted copy read two at a time; the array divides exactly when each two are equal. O(n log n) |
| `pairs_toggle.kara` | a `Set` of the numbers still waiting for their pair, each number taken out if it is there and put in if not; the array divides exactly when none is left waiting |
| `pairs_struct.kara` | a `struct Tally` of how often each number appears, in a `Map`, asked whether every count is even |
| `pairs_iter.kara` | a sorted copy cut by `chunks(2)`, and `all` of them a pair of equals |
| `pairs_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `bool` out, the counts in a `HashMap` by `entry(x).or_insert(0)`, and `values().all` of them even; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one pair, one number four times, three of one and one of another, and
both ends of the range), each with its answer; then how many of 3000
random arrays of 2 to 20 numbers divide, and a checksum; then the
constraints' largest, 1000 numbers in pairs, and the same with its last
number changed. `pairs.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in two rounds of 8 and 1 edits: first
Rust's spellings (`Vec<i32>` to `Vec[i32]`, `HashMap::new()` to
`HashMap.new()`, `for &x in &nums` to `for x in ref nums`, `|&c|` to
`|c|`, `struct Solution;` to `struct Solution {}`, and the `use`
dropped); then `HashMap` to Kāra's `Map`.

The iter arm's first draft called `all` on `chunks(2)` directly, which
returns a `Vec` of slices rather than an iterator; `karac fix` writes
the `.into_iter()`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the first number not yet paired tried with every later
unpaired number equal to it, and the rest paired the same way, backing
up when none is left; no count. It checks 300 random arrays of 2 to 12
numbers up to 2, 5 and 500 in turn; then 30 built of pairs and shuffled;
then 30 of 40 to 60 numbers up to 500 built of pairs, with one number
changed in every other one. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array followed by itself: it divides |
| P3 | the array reversed: the same answer |
| P4 | every number x made 501 - x: the same answer |
| P5 | two more of the first number appended: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 402184617, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that counts
with `collections.Counter`. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-six edits to the differential, six to the ★ arm, five to the sort
arm and to the template arm, six to the iter arm, and seven to the
toggle and struct arms, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a count of 3 or more taken as even | P1 27, P5 9, P6 27 |
| M5 | ★: the last number left uncounted | P1 110, P2 360, P6 110 |
| M6 | ★: the answer turned round | P1 360, P2 360, P6 360 |
| M7 | sort: the copy left unsorted | P1 77, P2 327, P6 77 |
| M8 | sort: the pairs read one apart | P1 91, P2 341, P6 91 |
| M9 | sort: the first pair skipped | P1 57, P4 37, P5 24, P6 57 |
| M12 | toggle: a number seen again kept waiting | P1 100, P2 342, P4 21, P6 100 |
| M15 | toggle: the waiting checked by the first number only | P1 45, P3 45, P6 45 |
| M33 | toggle: a number above 250 never waiting | P1 13, P4 160, P6 13 |
| M17 | struct: every count starting at 1 | P1 269, P2 360, P6 269 |
| M18 | struct: a count of 2 taken as odd | P1 83, P2 223, P5 23, P6 83 |
| M36 | struct: a count of 4 or more taken as odd | P1 73, P2 240, P5 37, P6 73 |
| M24 | iter: any pair, not all | P1 123, P5 127, P6 123 |
| M25 | iter: a pair's first compared with itself | P1 250, P6 250 |
| M26 | iter: the last pair skipped | P1 58, P4 37, P5 25, P6 58 |
| M27 | solution: the counts by parity of the number | P1 94, P6 94 |
| M28 | solution: any count even | P1 91, P6 91 |

P1 and P6 kill all seventeen, P2 eight, P5 six, P4 four and P3 one. P2
doubles the array, so every count is even and the answer must be
`true`; it kills the eight that can say `false` to an array of pairs
(M5, M6, M7, M8, M12, M17, M18, M36). P3 reverses the array and kills
only the toggle arm's check by the first number (M15), the one answer
that depends on order once the sort arms sort. P4 turns every number
round and kills the four that treat a number by its size or its place in
the sorted copy (M9, M12, M26, M33). P5 adds two of the first number and
kills the six that answer a count of 3 or 4, or a pair at the edge of
the sorted copy, wrongly (M2, M9, M18, M24, M26, M36).

Of the thirty-six, nineteen were not kept. Two are equivalent by parity:
the ★ arm's counts read from 2 (M4) and the toggle arm's one left
waiting allowed (M14), since the counts of an array of even length sum
to an even number, so a single odd count cannot happen. Two survive and
are not equivalent: the struct arm's counts by the number mod 100 (M34)
and the template adapter's numbers mod 256 (M30) answer wrongly only
when two numbers that far apart both appear an odd number of times and
every other number pairs, which none of the 360 cases draws. Two crash
on an index out of bounds: the ★ arm's count table of 500 (M1) and the
iter arm's chunks of 3 (M23). One differs between the two backends: the
struct arm's first count alone deciding (M21), since the first count is
the first entry of a `Map`, whose order is random per process. Eleven
fail as a kept one does: the ★ arm's numbers counted twice and the iter
arm's pairs taken as sorted (M3, M35) as M25; the toggle arm's every
number put in, its last number never toggled and its set started with
the first number, the struct arm's tally without its first number, and
the adapter dropping the first number (M13, M16, M32, M20, M31) as M5;
the sort arm's pair compared with the next one's first and its sort
reversed and shifted (M10, M11) as M8; the iter arm's copy left unsorted
(M22) as M7; and the struct arm's odd count of 3 or more passed (M19) as
M2. The template's counts by the number over 2 (M29) fails its own way
and is left out for the count of two. M32 to M36 were added when the
first thirty-one crowded the toggle, struct and iter arms onto shared
signatures.

## Verification

Every arm prints the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 s to 0.4 s and the
differential 0.53 s.

## Benchmarks

The bench builds 200 arrays of 1000 numbers once, three in four of them
pairs shuffled and the rest drawn freely, up to 2, 5 and 500 in turn,
then answers each 1500 times over with the ★ arm in all five languages,
every odd pass with one number changed before the count and put back
after. Every implementation prints `1500 passes over 200 arrays:
checksum 659994446`.

BENCHTAB
