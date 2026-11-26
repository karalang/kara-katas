# 1481. Least Number of Unique Integers after K Removals

Given an array of integers `arr` and an integer `k`. Find the least
number of unique integers after removing exactly `k` elements.

```
arr = [5,5,4],           k = 1   ->  1
arr = [4,3,1,1,3,3,2],   k = 3   ->  2
```

**Constraints:** `1 <= arr.length <= 10^5`, `1 <= arr[i] <= 10^9` and `0
<= k <= arr.length`.

The arms are `fn find_least_num_of_unique_ints(arr: Vec[i32], k: i32) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `find_least_num_of_unique_ints.kara` ★ | each value counted in a `Map[i32, i64]`; the counts sorted, and the removals spent on the rarest values first, each one gone once all its copies are. O(n log n) |
| `find_least_num_of_unique_ints_bucket.kara` | the values counted, then bucketed by their count, so the rarest come first without a sort: from count 1 up, each bucket finished off while the removals last, and of the first they cannot finish, as many values as they still cover. O(n) |
| `find_least_num_of_unique_ints_heap.kara` | the counts in a `PriorityQueue[i64]`, which pops the smallest first, and the removals spent on whatever is on top while it fits. O(n log n) |
| `find_least_num_of_unique_ints_sorted.kara` | no map: the values sorted, so each value's copies stand together and its count is the length of its run; the run lengths sorted in turn and spent rarest first. O(n log n) |
| `find_least_num_of_unique_ints_solution.kara` | a Rust solution as LeetCode's Rust users write it (`HashMap<i32, i32>`, `*map.entry(x).or_insert(0) += 1`, `map.into_values()`, `sort_unstable`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; five edges,
no removals, every value removed, one value many times, all values
different, and removals that cannot finish a value off; the constraints'
most, 100000 values from 1 to 10^9, all but a few different, and from 1
to 1000, for 0, 1000, 50000 and 100000 removals (`100000 values: 99994
98994 49994 0 | 1000 987 461 0`); and 3000 random arrays of 1 to 60
values from 1 to top, top from 1 to 30, and 0 removals to all of them,
each answer folded into a checksum (`3000 random arrays: checksum
978810728`). `find_least_num_of_unique_ints.py` mirrors the ★ arm, and
its output is byte-identical. The map is walked only to collect its
counts, which are sorted or bucketed before anything is read in order,
so no output depends on the map's walk. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the bucket and sorted arms check clean as first written.
The ★ arm was first written `let mut left = k;`, an `i32` from `k`, and
check refused `left -= c` with a count `c: i64` as a narrowing; the
budget was widened, `let mut left: i64 = k;`. The heap arm was first
written with Rust's habit for a heap that pops the smallest,
`PriorityQueue[Reverse[i64]]` and `rarest.push(Reverse(c))`; `karac fix`
added `import std.cmp.Reverse;` and wrote `Reverse { value: c }`, 5
fixes, and the arm then checked and printed wrong answers, since Kāra's
`PriorityQueue.new()` already pops the smallest first and `Reverse`
turned it to the largest, as collections.md says. The oracle caught it,
and the `Reverse` was dropped. The Rust solution takes one round of 12
fixes by `karac fix`'s count, and its diff is: `use
std::collections::HashMap;` deleted, since `Map` is in the prelude,
`struct Solution;` to `struct Solution {}`, each `Vec<i32>` to
`Vec[i32]`, `HashMap<i32, i32>` and `HashMap::new()` to `Map[i32, i32]`
and `Map.new()`, and `sort_unstable` to `sort`. Rust's
`*map.entry(x).or_insert(0) += 1` and `into_values` stay. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to remove exactly `k` of the places, and of those,
the fewest distinct values left. LeetCode's examples, the edges, and
1993 random arrays, half of 1 to 10 values from 1 to 4, so values repeat
often, and half of 1 to 14 values from 1 to top, top from 1 to 10, each
with 0 removals to all of them. Each arm meets six properties on each
case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed has the same answer |
| P3 | no removals leave every distinct value, and removing all leaves none |
| P4 | one removal more leaves the same number or one fewer |
| P5 | every value twice over, with twice the removals, has the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 893222428,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, removing the
places by `itertools.combinations`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a value whose copies use up the last removals is kept | P1 935, P3 2000, P6 3740 |
| M2 | ★: the commonest values spent first | P1 727, P6 2908 |
| M3 | bucket: the last value of a bucket never finished off | P1 1237, P3 2000, P6 1237 |
| M4 | bucket: a value finished off costs one removal, not its count | P1 182, P4 5, P5 196, P6 182 |
| M5 | heap: a value finished off costs nothing | P1 938, P4 227, P6 938 |
| M6 | heap: a value one copy over the removals left finished off | P1 880, P3 1508, P5 880, P6 880 |
| M7 | sorted: each run counted one longer | P1 1231, P3 2000, P5 332, P6 1231 |
| M8 | sorted: the runs taken from the largest value down, not by length | P1 417, P6 417 |
| M9 | solution: a value whose copies use up the last removals is kept | P1 935, P3 2000, P6 935 |
| M10 | solution: each value finished off counts as two | P1 1492, P3 2000, P4 880, P6 1492 |

## Benchmarks

The bench makes one array of 100000 values from 1 to 30000 once; then
makes 100 passes, each punching one value and asking the ★ arm for 0 to
99999 removals, both chosen from the checksum so far. Kāra's `Map` and
Rust's `HashMap` both hash by SipHash-1-3, and Go's map by its own hash;
C has no map, so its mirror counts in an open-addressing table with a
multiplicative hash, grown at half full, which is cheaper per insert
than SipHash. Every implementation prints `100 passes over 100000
values: checksum 704565113`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.34 s against Rust's 0.32 s (0.32 s with overflow checks
on), C's 0.35 s and Go's 0.60 s; Python takes 1.4 s.
