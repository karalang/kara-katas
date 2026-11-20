# 2261. K Divisible Elements Subarrays

Given an integer array `nums` and two integers `k` and `p`, return *the
number of **distinct subarrays**, which have **at most** `k` elements
that are divisible by* `p`.

Two arrays `nums1` and `nums2` are said to be **distinct** if they are
of different lengths, or there exists **at least** one index `i` where
`nums1[i] != nums2[i]`. A **subarray** is defined as a **non-empty**
contiguous sequence of elements in an array.

```
nums = [2,3,3,2,2], k = 2, p = 2  ->  11
nums = [1,2,3,4],   k = 4, p = 1  ->  10
```

**Constraints:** `1 <= nums.length <= 200`; `1 <= nums[i], p <= 200`;
`1 <= k <= nums.length`.

The divisible count of a subarray only grows as it is extended, so from
each start the subarrays that qualify are a prefix of the ones that
begin there, and the work is to count the distinct ones among about
n^2 / 2 subarrays. A set of the subarrays themselves does it in
O(n^3); a trie of all of them, one node per distinct subarray, does it
in O(n^2) steps.

## Approaches

| file | mechanism |
|---|---|
| `divisible.kara` ★ | from every start a `run` grows one element at a time, the divisible ones counted, stopping by `break` past `k`; every `run.clone()` goes into a `Set[Vec[i64]]` |
| `divisible_sort.kara` | no hashing: every qualifying `nums[start..end + 1].to_vec()` in one `Vec[Vec[i64]]`, then `sort`, which orders `Vec`s element by element, and `dedup` |
| `divisible_trie.kara` | a trie in a `Map[(i64, i64), i64]` from (node, value) to child, node 0 the root; each start walks down and makes the children it lacks, and the nodes made are the answer |
| `divisible_struct.kara` | `struct Trie` of one `Map[i64, i64]` of children per node; `step` (`mut ref self`) returns the child and whether it was new; the walk spends a budget of `k` divisible elements |
| `divisible_iter.kara` | chains: `flat_map` over the starts of a `scan` that carries the running count as Kāra's `Some((count, (end, count)))`, `take_while` up to `k`, each subarray written as its elements `join`ed by commas, all `collect`ed into a `Set[String]` |
| `divisible_solution.kara` | LeetCode's Rust template: `Vec<i32>` and two `i32`s in, `i32` out; a `HashSet` of `nums[i..=j].to_vec()` while a count of divisible elements stays at most `k`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (one element, divisible, with k = 1; all one value; nothing
divisible; every element divisible with k = 1), each with its count;
then 2000 arrays of 1 to 20 elements from 1 to 10 with `k` from 1 to
the length and `p` from 1 to 10, with the total and a checksum; then
four of the constraints' longest, 200 elements: all 1 with `p = 1` and
`k = 50` (50); random from 1 to 200 with `p = 7` and `k = 200`
(20030); 1 to 200 in order with `p = 2` and `k = 10` (3900); and
random from 1 to 3 with `p = 3` and `k = 20` (10171).
`divisible.py` mirrors the ★ arm and its output is byte-identical.

The iterator arm was first written as Rust writes `scan`, lending the
count: `|count, end| { *count += ..; Some((end, *count)) }`. `karac
fix` took the pair in the tail for Kāra's own `(next_state, item)` and
offered only to drop the two `*`s, which leaves `end` as the state and
the count as the item (B-2026-11-18-79). The arm is written in Kāra's
shape.

`karac fix` carries the template in one round of 6 edits: the `use
std::collections::HashSet;` line deleted, `Vec<i32>` to `Vec[i32]`,
`HashSet::new()` to `Set.new()`, and `struct Solution;` to `struct
Solution {}`. `nums[i..=j]` stays as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray `nums[i..=j]` in turn, its divisible elements
counted, and when it has at most `k` it is compared element by element
with every one kept so far, and kept if it differs from all. No
hashing, no sorting, no trie. It checks 300 random arrays of 1 to 12
elements from 1 to 6 or 1 to 12 in turn, with `k` from 1 to the length
and `p` from 1 to 6; then 30 of one value repeated; then 30 with `p =
1`, every element divisible. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the array reversed: the same count |
| P3 | `k` one larger: no smaller a count |
| P4 | `p` added to every element: the same count |
| P5 | 1009 put on the end: the count plus the suffixes, the empty one with them, that still have room for it |
| P6 | each arm agrees with at least three of the other five |

P5 holds because 1009 appears nowhere else, so every subarray that
ends with it is new, and those are the suffixes with 1009 appended,
counted when their divisible elements, with 1009's own when `p = 1`,
stay within `k`.

The differential prints `360 cases: checksum 477863970, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that puts
the qualifying slices into a set of tuples. On a failure it prints the
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
| M1 | ★: the limit at k - 1 | P1 153, P5 153, P6 153 |
| M3 | ★: the start element never counted | P1 84, P2 17, P5 107, P6 84 |
| M6 | ★: the divisible test on the value plus one | P1 59, P5 74, P6 59 |
| M8 | sort: dedup without the sort | P1 253, P6 253 |
| M9 | sort: the subarray one longer | P1 287, P2 17, P5 282, P6 287 |
| M10 | sort: the stop checked before counting | P1 84, P2 17, P5 78, P6 84 |
| M13 | trie: children keyed by value only | P1 247, P2 94, P6 247 |
| M14 | trie: the root shared with node 1 | P1 313, P2 164, P5 293, P6 313 |
| M15 | trie: a non-divisible element stopping the walk | P1 101, P2 51, P5 153, P6 101 |
| M19 | struct: the node not moved | P1 199, P2 188, P5 249, P6 199 |
| M20 | struct: a new child hung on the root | P1 300, P2 2, P5 336, P6 300 |
| M21 | struct: the budget spent on the others | P1 202, P5 292, P6 202 |
| M22 | iter: the key without its last element | P1 298, P2 127, P5 360, P6 298 |
| M23 | iter: no separator | P1 9, P2 5, P4 9, P6 9 |
| M25 | iter: no subarray from the first element | P1 346, P2 138, P5 253, P6 346 |
| M28 | solution: the subarray from 0 | P1 301, P5 336, P6 301 |
| M31 | solution: the values cut to 4 | P1 249, P4 244, P5 325, P6 249 |

P1 and P6 kill all seventeen, P5 fourteen, P2 eleven, P4 two, and P3
none. P5 catches nearly every miscount, since appending a value seen
nowhere else adds a number of subarrays the harness counts itself. P2
catches the edits that favour one end: a key without its last element,
a stop checked before counting, a start never counted. P4 catches the
template's values cut to 4 and the iter arm's keys with no separator,
where adding `p` makes values of two digits that run together. P3
holds under every edit: none of them makes the count fall as `k`
grows.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Twelve fail as a kept one does or as a group:
the ★ arm's divisible count never reset as the template's count kept
across starts (M2, M29); the ★ arm's last element dropped from the key
and the template's end excluded (M4, M30) as the iter arm's key
without its last element (M22); every subarray counted with its
repeats in the ★, sort, trie and struct arms (M5, M7, M12, M18) all
alike; the iter arm's limit below `k` (M24) as the ★ arm's (M1); and
the struct arm's budget at `k + 1`, the iter arm's count not carried
and the template's limit one higher (M17, M26, M27) all alike. Two fail
in ways of their own and are left out because their arms keep enough:
the sort arm's last start never taken (M11) and the trie arm's walk
from the wrong root (M16).

Three edits of the first draft were replaced or answered. Two were
equivalent, since a count that only grows stays past `k` once it gets
there: the ★ arm's `break` made `continue`, and the iter arm's
`take_while` made `filter`; they are now M3 and M25. The third, the
iter arm's keys joined with no separator (M23), survived while every
value had one digit; the random arrays now take values to 12 in every
other case, and P1, P2 and P4 kill it.

## Verification

Every arm prints the same output as `divisible.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the struct arm takes 0.7 s, the ★ arm and the
template 0.8 s, the trie arm 0.9 s, the sort arm 1.3 s, the
differential 2.5 s, and the iter arm 10.9 s. The iter arm builds a
`String` for every subarray, `to_string` on each element and a
`join`, about 2 * 10^6 element strings over the four long arrays.

## Benchmarks

The bench answers 40 arrays of the constraints' longest, 200 elements
from 1 to 200, with `p` from 2 to 9 and `k` from 5 to 200, with the ★
arm in all five languages. Every implementation prints `40 arrays of
200: checksum 320836881`. Rust keys a `HashSet<Vec<i64>>` and Python a
set of tuples, as the ★ arm keys its `Set[Vec[i64]]`. Go's maps cannot
key on a slice, so its mirror keys on the elements' bytes in a
`string`; C has no set, so its mirror is an open-addressing table that
hashes each subarray whole, compares on a hash match and stores a copy
of each new one.

BENCHTAB
