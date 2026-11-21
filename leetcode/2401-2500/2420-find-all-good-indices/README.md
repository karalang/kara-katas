# 2420. Find All Good Indices

You are given a **0-indexed** integer array `nums` of size `n` and a
positive integer `k`.

We call an index `i` in the range `k <= i < n - k` **good** if the
following conditions are satisfied:

- The `k` elements that are just **before** the index `i` are in
  **non-increasing** order.
- The `k` elements that are just **after** the index `i` are in
  **non-decreasing** order.

Return *an array of all good indices sorted in **increasing** order*.

```
nums = [2,1,1,1,3,4,1], k = 2  ->  [2,3]
nums = [2,1,1,2], k = 2        ->  []
```

**Constraints:** `n == nums.length`; `3 <= n <= 10^5`;
`1 <= nums[i] <= 10^6`; `1 <= k <= n / 2`.

The `k` values before `i` never rise exactly when the run of values
that never rise, ending at `i - 1`, is at least `k` long, and likewise
after `i` for the run that never falls starting at `i + 1`. Both runs
come from one pass each, so every index is tested in constant time.

## Approaches

| file | mechanism |
|---|---|
| `good.kara` ★ | two run lengths: how many values end at each index without rising, from the left, and how many start at each index without falling, from the right; `i` is good when the first at `i - 1` and the second at `i + 1` both reach `k`. O(n) |
| `good_naive.kara` | the statement checked directly: for each index, the `k` values before it walked for a rise and the `k` after it for a fall. O(n k) |
| `good_breaks.kara` | counted breaks: prefix counts of the steps up and of the steps down, and each side tested by two lookups, no step up among the `k` before and no step down among the `k` after. O(n) |
| `good_runs.kara` | runs: the array cut into its longest stretches that never rise and, apart, those that never fall, as `(start, end)` pairs; the stretch holding `i - 1` found by binary search must start by `i - k`, and the one holding `i + 1` end by `i + k`. O(n log n) |
| `good_iter.kara` | iterators: the two run lengths by `scan`, the rising one over the indices reversed and then turned back, and the good indices by `filter` and `collect`. O(n) |
| `good_solution.kara` | LeetCode's Rust template: `vec![1; n]` run lengths `left` and `right`, compared with `k as usize`, and the indices pushed as `i as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples; all the
same values; `k` at its largest, `n / 2`; one valley; strictly up and
strictly down with `k = 1`; the constraints' largest, `10^5` values up
to `10^6` in slopes about 60 long, with `k` of 2, 5 and 50, and `10^5`
of 1 to 3 turning often with `k = 3`, each by the count of good indices,
a digest and their sum; then 3000 random arrays of 3 to 30 values up to
1 to 8 with `k` from 1 to `n / 2`, as a checksum and the count. `good.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 20000 random arrays of up to 12 values against the two
conditions tested pair by pair.

`check` first reports 5 errors on the template, and `karac fix` carries
it in one call, reporting 10 edits: both `Vec<i32>` given brackets;
`Vec::new` written `.`; `&&` written `and`; `struct Solution;` given its
braces; `vec![1; n]` written `Vec.filled(n, 1)` twice; and `k as usize`
written `k as i64`, since Kāra counts lengths and indices in `i64`
and the run lengths it is compared with are `i64`. `i as i32` stands.

Two arms were first written with Rust habits, and `check` refused both
with the rewrite named. The runs arm found the stretch by
`binary_search_by`, returning `Ordering`, and matched `Ok(r)` and
`Err(_)`: Kāra has no `binary_search_by`, and `karac fix` writes the
search as two `partition_point` calls over the same comparison, the
`Ok` case being the one where the first point lies below the second, in
one edit. The iter arm's `scan` closures wrote their state through
`*run`, as Rust's do: Kāra's `scan` takes the state by value and
returns `Some((next_state, item))`, and `karac fix` rewrites both
closures, in two edits. It wrote the first on one line and the second
across lines; the first is laid out here as `karac fmt` prints it.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every index from `k` to `n - k - 1`, the `k` values before
it compared with their own copy sorted from the largest, and the `k`
after with theirs sorted from the smallest. No run lengths, no counts.
It checks 300 random arrays of 3 to 14 values up to 1 to 8 in slopes
that turn with probability 1 in 1 to 6, with `k` from 1 to `n / 2`; then
30 of up to 400 values up to `10^6` in slopes about 30 long, `k` up to
20; then 30 of up to 400 values of 1 to 3 turning often, `k` up to 5.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the indices rise, each at least `k` and below `n - k` |
| P3 | the array reversed: each index `i` answered as `n - 1 - i`, in order |
| P4 | every value `v` made `2 v + 1`: the same answer |
| P5 | `k` made one less: an answer holding every index of this one; at `k = 1`, every index from 1 to `n - 2` |
| P6 | each arm agrees with at least three of the other five |

P3 holds because reversing turns the `k` values before `i` that never
rise into the `k` after `n - 1 - i` that never fall, and the other way
round. P4 holds because `2 v + 1` keeps every comparison, P5 because a
run long enough for `k` is long enough for `k - 1`, and at `k = 1` each
side is one value, always in order.

P5's `k = 1` side compares the answer with `(1..n - 1).collect()`, which
`check` refused: a comparison does not fix what `collect` builds, and it
names the collection to build. `karac fix` writes
`(Vec[i64].from_iter(1..n - 1))`, keeping the parentheses that held the
range, in one edit.

The differential prints `360 cases: checksum 777497912, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and sorts both sides of every index. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the run before read at i | P1 83, P3 96, P6 83 |
| M4 | ★: one value short allowed after | P1 59, P3 80, P6 59 |
| M5 | ★: the run before never broken | P1 68, P3 87, P6 68 |
| M7 | naive: the first pair before never checked | P1 54, P3 80, P6 54 |
| M8 | naive: a rise allowed before | P1 53, P3 76, P4 53, P6 53 |
| M9 | naive: the pair across i checked after | P1 109, P3 127, P5 37, P6 109 |
| M14 | breaks: the falls read one pair short | P1 96, P3 130, P5 68, P6 96 |
| M15 | breaks: the falls never counted | P1 83, P3 105, P6 83 |
| M16 | breaks: rises and falls swapped after | P1 95, P3 115, P6 95 |
| M17 | runs: a strict fall needed in the stretch | P1 143, P3 52, P6 143 |
| M18 | runs: the stretch before ending at i - 1 required | P1 205, P3 198, P5 223, P6 205 |
| M20 | runs: the last stretch never closed | P1 117, P3 108, P6 117 |
| M22 | iter: the falling run never reset | P1 270, P3 222, P5 112, P6 270 |
| M23 | iter: the rising run never reversed | P1 87, P3 97, P6 87 |
| M26 | iter: either run enough | P1 105, P6 105 |
| M28 | solution: the right run read at i | P1 81, P3 96, P6 81 |
| M30 | solution: the indices one past | P1 276, P2 229, P3 276, P5 112, P6 276 |

P1 and P6 kill all seventeen, P3 sixteen, P5 five, and P2 and P4 one
each. P2 asks only that the indices rise within `k` to `n - k - 1`,
which every mutant that tests the wrong values still keeps, so only the
template's indices one past (M30) fails it, its last index reaching
`n - k`. P4 maps every value `v` to `2 v + 1`, which keeps every
comparison of two values, so only the naive arm's rise allowed before
(M8) fails it: it lets a value one more than the one before it pass,
and after the map no two values are one apart. P3 misses only the iter
arm's either run enough (M26), which is wrong the same way on both
sides of an index.

Of the thirty-one, fourteen were not kept. Eight fail the same checks as
a kept one: a fall needed before `i`, not a run that never rises, in
the ★ arm and an equal pair counted as a rise in the breaks arm (M1,
M13) as the runs arm's strict fall needed in the stretch (M17), since
all three refuse a run of equal values before `i`; the ★ arm's run
after read at `i` (M3) as the template's (M28); a fall checked after
where a rise should be and the rising run compared the wrong way in the
naive and iter arms (M10, M25) as the breaks arm's rises and falls
swapped after (M16); the runs arm's stretch after one short (M19) as
the ★ arm's one value short allowed after (M4); the runs arm's stretch
after looked up at `i` (M21) as the naive arm's pair across `i` checked
after (M9); and the template's value one more allowed before (M29) as
the naive arm's (M8). Four fail apart from every kept one and were
left out because those arms keep their share already: the ★ arm's last
index tried (M6), the naive arm's first index never tried (M11), and
the iter arm's runs started at 0 and the template's left run counted
from 0 (M24, M27), which fail alike.
Two end in an index out of bounds, not a wrong answer, under both
backends: the breaks arm's rises counted one pair long (M12) reads
`rises[i - k - 1]` at `i = k`, and the template's `k` read as one less
(M31) reads `left[i - 1]` at `i = 0` once `k` is 0.

## Verification

Every arm prints the same output as `good.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 to 3.5 s, but for the runs
arm, which takes 29 s there and 0.5 s under `karac run`: each of its
lookups runs two `partition_point` searches, each step a closure call,
and the interpreter makes millions of them. The differential
takes 3.6 s under `karac __mir-run`, 1.3 s under `karac
__mir-llvm-asan` and 0.6 s under `karac run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values up to `10^6` once from its
own generator, in slopes about 60 long with steps of up to 40. It then
makes 100 passes, pass `p` answering array `a` with `k = 1 + (p + a) %
40` and folding the count of good indices and their sum into the
checksum. The bench uses the ★ arm, the two run lengths, in all five
languages. Every implementation prints `100 passes over 10 arrays of
10^5 values: checksum 475405937`. Each allocates its two run arrays and
its answer afresh for every call, but C, which writes the answer into
one buffer allocated once.

BENCHTAB
