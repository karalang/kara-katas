# 2111. Minimum Operations to Make the Array K-Increasing

You are given a 0-indexed array `arr` of `n` positive integers, and a
positive integer `k`.

The array `arr` is called K-increasing if `arr[i - k] <= arr[i]` holds
for every index `i`, where `k <= i <= n - 1`. For example, `arr = [4,
1, 5, 2, 6, 2]` is K-increasing for `k = 2`, but not for `k = 1`
(`arr[0] > arr[1]`) or `k = 3` (`arr[0] > arr[3]`).

In one operation, you can choose an index `i` and change `arr[i]` into
any positive integer. Return the minimum number of operations required
to make the array K-increasing for the given `k`.

```
arr = [5,4,3,2,1],   k = 1  ->  4
arr = [4,1,5,2,6,2], k = 2  ->  0
arr = [4,1,5,2,6,2], k = 3  ->  2
```

**Constraints:** `1 <= arr.length <= 10^5`; `1 <= arr[i], k <=
arr.length`.

The condition only ever ties places `k` apart, so the array is `k`
separate chains, `r, r + k, r + 2k, ...`, each of which must become
non-decreasing, and the chains do not constrain each other. Within a
chain, the values left alone must already be non-decreasing in order,
and any such set can stay: each changed value can be set to the kept
value before it (or 1). So a chain keeps its longest non-decreasing
subsequence and changes the rest, and the answer is `n` less the sum of
those lengths.

## Approaches

| file | mechanism |
|---|---|
| `increasing.kara` ★ | patience piles per chain: `tails[j]` the smallest last value of a non-decreasing subsequence of length `j + 1`, each value replacing the first tail above it, found with `partition_point(\|t\| t <= x)`; the chain walked with a `while` stepping by `k`. O(n log n) |
| `increasing_search.kara` | the same piles, each chain gathered first with `iter().skip(r).step_by(k).collect()`, the first tail above each value found by a binary search written out, `lo` and `hi` in a `while` |
| `increasing_fenwick.kara` | a Fenwick tree over the values 1 to 10^5: the longest subsequence ending at `x` is one more than the longest ending at any value up to `x`, a prefix maximum; after each chain its writes are undone. O(n log V) |
| `increasing_struct.kara` | a `struct Piles` with a `place` method (`mut ref self`), first written with Rust's `match tops.binary_search(x) { Ok(i) => i, Err(i) => i }`, which `karac fix` turned into a `partition_point` block; equal tops then stepped past |
| `increasing_fold.kara` | one expression: `(0..k).map(..).sum()`, each chain's places a `step_by` range collected into a `Vec`, `fold`ed into its tails |
| `increasing_solution.kara` | LeetCode's Rust template (`Vec<i32>, i32` to `i32`): each chain walked with `(i..arr.len()).step_by(k)`, the tails placed with `partition_point(\|&t\| t <= x)`, carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and four
more (one element, equal elements, every chain one long, two falling
chains), each with its answer; then the total for 3000 random arrays of
1 to 40 values from 1 to 10 with `k` from 1 to the length, and a
checksum of the answers; then the constraints' largest, 10^5 values:
falling with `k = 1`, random with `k = 7`, and random with `k = n`.
`increasing.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the most values that can stay, each kept value no smaller
than the kept value before it in its chain, found by trying every
earlier place of the chain (quadratic, with no piles and no search),
the rest changed. It checks 300 random arrays of 1 to 10 values from 1
to 4 with `k` from 1 to the length; then 30 of up to 120 values from 1
to 30 with `k` from 1 to 5; then 30 of up to 120 that mostly rise (place
`i` holds `i` plus 1 to 8), with `k` from 1 to 3, so that long chains
keep most of their values. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least 0 and at most `n - k` |
| P3 | every value raised by 7: the same answer |
| P4 | `k` values above them all appended, one to the end of each chain: the same answer |
| P5 | every value raised by 7 and a 1 appended: the answer plus one |
| P6 | each arm agrees with at least three of the other five |

P2's bound holds because each chain keeps at least its first value. P5
holds because a 1 below every other value ends no non-decreasing
subsequence of length two, so its chain keeps as many as before and
has one more place.

The differential prints `360 arrays: checksum 790163854, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
arrays with `bisect_right` piles. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-four edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: strictly increasing chains | P1 161, P6 161 |
| M4 | ★: the last chain skipped | P1 143, P5 145, P6 143 |
| M31 | ★: chains over ten long cut short | P1 53, P5 56, P6 53 |
| M7 | search: the search one short at the top | P1 228, P4 360, P6 228 |
| M8 | search: every chain from the start | P1 130, P2 31, P5 266, P6 130 |
| M32 | search: values above 20 dropped | P1 57, P2 1, P3 56, P4 58, P5 57, P6 57 |
| M11 | fenwick: the tree never cleared between chains | P1 256, P2 186, P4 135, P5 60, P6 256 |
| M14 | fenwick: the last length kept, not the longest | P1 51, P4 51, P5 147, P6 51 |
| M33 | fenwick: values capped at 50 | P1 24, P3 25, P4 25, P5 25, P6 24 |
| M16 | struct: equals stepped past twice | P1 68, P6 68 |
| M19 | struct: a new pile always started | P1 203, P5 360, P6 203 |
| M20 | struct: the step one more than `k` | P1 172, P5 167, P6 172 |
| M21 | fold: each chain's length counted one less past two | P1 150, P2 19, P4 131, P5 60, P6 150 |
| M23 | fold: the place pushed, not its value | P1 174, P3 110, P4 111, P5 262, P6 174 |
| M25 | fold: the tails emptied whenever they pass three | P1 72, P4 35, P5 17, P6 72 |
| M27 | solution: the values halved | P1 81, P3 125, P5 125, P6 81 |
| M28 | solution: each chain's length one too long | P1 360, P2 213, P6 360 |

P1 and P6 kill all seventeen, P5 thirteen, P4 eight, P2 five and P3
four. P5 misses only the edits that change how equal values are
treated (M1, M16), the search one short at the top (M7), which never
starts a second pile and so fails every array P4 extends instead,
and the Rust arm's chain length one too long (M28), which is off by
the same `k` before and after the 1 is appended. P3 sees the edits
that read a value against a constant or as a place: values above 20 or
50 (M32, M33), the place pushed (M23), the values halved (M27). P2 sees
the edits that can answer more than `n - k`: a chain read from another
chain's places (M8, M11), a chain's length miscounted (M21, M28), and
once the search arm's dropped values (M32). The two caps (M31, M33) and the
strict piles (M1) show only on arrays that have long chains, large
values or repeated ones.

Of the thirty-four, seventeen were not kept. Five give strict piles in
some form and fail as M1, P1 161, P6 161: the search arm's equal values
starting a new pile, the Fenwick arm's own length looked up below the
value, the struct arm's equals not stepped past, and the fold and Rust
arms' strict tails. The ★ and Rust arms' value never replacing a tail
fail alike (P1 83, P6 83), as do their chains one apart (P1 233, P2
195, P5 266, P6 233). Five more are killed with checks of their own but
were left out because their arm keeps its share: the ★ arm's kept values
counted as changes, the search arm's first value of each chain dropped,
the Fenwick arm's parent step taken going down and its raise stopping
at its first node, and the fold arm's first chain only. Two were not
kept for how they end: the search arm's middle rounded up loops forever
(a timeout under both backends), and the fold arm's tails capped at
five indexes past the end. One survives and is equivalent: the struct
arm's piles shared across chains, with the tops cleared at each chain,
does what a new `Piles` per chain does.

## Verification

Every arm prints the same output as `increasing.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.9 s to 3.8 s, and the Fenwick
arm 12 s, its tree of 10^5 + 1 entries walked per value; the
differential takes 4.8 s, and compiled 0.6 s.

`karac fix` carries the template in three rounds of 6, 3 and 1 edits:
Rust's spellings (`Vec<i32>` to `Vec[i32]` twice, `Vec::new()` to
`Vec.new()`, `|&t|` to `|t|`); then `k as usize` to `k as i64`, `ans`
declared `i32` beside the `i32` answer, and the adapter's `as i64`
dropped, since the `i32` result widens without one; then `len`
declared `i32` too, which the round before had made the type
`ans += len - ..` needs.

Two compiler gaps came up, each fixed in karac with a test named for
this kata (karac SKIPSHA):

- The search arm, `arr.iter().skip(r).step_by(k)`, ran for minutes at
  `k = n = 10^5`. `skip` already jumped its skipped items, but
  `step_by` advanced the `skip` itself, which walked each step one item
  at a time; it now passes the advance through to the `Vec`'s
  iterator, and the arm takes 0.35 s compiled.
- The fold arm first wrote `places.clone().count()` on the `step_by`
  range, and the message offered "did you mean 'cloned'?", whose rename
  maps the items. No library iterator is `Clone`; the message now says
  so and what a second walk takes, and the arm collects its places
  once.

## Benchmarks

The bench builds 10 arrays of 10^5 random values from 1 to 10^5 once;
it then solves each 10 times, with `k` from 1 to 10, moving one value
up by one (or from 10^5 to 1) before each solve so no solve repeats the
one before, with the ★ arm in all five languages: patience piles per
chain, a binary search for each value's pile. Every implementation
prints `100 solves: 9862479 operations, checksum 982606240`.

BENCHTAB
