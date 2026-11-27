# 1815. Maximum Number of Groups Getting Fresh Donuts

A donut shop bakes donuts in batches of `batchSize`, and must serve all
of a batch before it serves any donut of the next. Given `batchSize` and
an array `groups`, where `groups[i]` is the number of customers in the
`i`th group to visit the shop, each customer getting exactly one donut,
all customers of a group are served before the next group's. A group is
happy if its first customer gets a fresh donut, that is, if the group
before it left no donut of its batch. The groups may be rearranged.
Return the maximum possible number of happy groups.

```
batchSize = 3, groups = [1, 2, 3, 4, 5, 6]        ->  4
batchSize = 4, groups = [1, 3, 2, 5, 2, 2, 1, 6]  ->  4
```

**Constraints:** `1 <= batchSize <= 9`, `1 <= groups.length <= 30`, `1
<= groups[i] <= 10^9`.

The arms are `fn max_happy_groups(batch_size: i64, groups: Vec[i64]) ->
i64`.

## Approaches

| file | mechanism |
|---|---|
| `max_happy_groups.kara` ★ | only each group's size modulo the batch matters. Groups of remainder 0 are always happy; a group of remainder `r` and one of `b - r` make one happy group and then end a batch together, so those pairs are taken first, and two groups of half a batch likewise; what is left is a search over how many groups of each remainder remain, memoized in a `Map` by those counts written as one number in base 31, which also fixes the donuts left over. O(b * the product of (count + 1)) |
| `max_happy_groups_plain.kara` | the search with no pairing first: groups of remainder 0 counted happy, every other group placed in turn, memoized in a `Map` keyed by the `Vec` of counts left, as a Python solution keys by a tuple, and the next group happy when the groups left sum to all of them, modulo the batch |
| `max_happy_groups_table.kara` | bottom up: every choice of how many groups of each remainder go first is a number in a mixed radix, one digit per remainder, and adding a group adds its remainder's place value, so the table is filled in increasing order, `best[s]` the most happy groups among those of `s` served first |
| `max_happy_groups_dense.kara` | the ★ arm's pairing, then its search memoized in a dense `Vec` indexed by the counts as a mixed-radix number, -1 for a state not reached, in place of a `Map` |
| `max_happy_groups_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn dfs` nested in the method over `&mut Vec<usize>` counts, memoized in a `HashMap<Vec<usize>, i32>`, read with `if let Some(&v) = memo.get(cnt)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`4 4`); five
edges, a batch of one, one group, every group a whole batch, ten groups
of one at a batch of nine, and the largest groups (`3 1 3 2 1`); the
constraints' most, 30 groups at a batch of 9 covering every remainder
and 30 at a batch of 8 (`the most: 17 15`); and 300 random cases of a
batch of 1 to 9 and 1 to 30 groups (`300 random cases: checksum
10189455`). `max_happy_groups.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: every arm and the harness check clean as first written.
The plain arm was first written to call the next group happy when the
groups left sum to whole batches; that is the groups served, not those
left, and it printed `4 3` for LeetCode's examples. The mistake was
mine, and it now compares the groups left with all of them, modulo the
batch. The Rust solution takes 44 fixes by `karac fix`'s count, and its
diff is: `use std::collections::HashMap;` deleted and `struct Solution
{}` added; the nested `fn dfs` moved above the `impl`, as Kāra has no
nested items and it captures nothing; `&mut Vec<usize>` and `&mut
HashMap<Vec<usize>, i32>` to `mut ref Vec[i64]` and `mut ref
Map[Vec[i64], i32]`, and `&mut` to `mut` at the calls; `usize` to `i64`
throughout, so `batch_size as usize` becomes `batch_size as i64`,
`vec![0usize; b]` becomes `Vec.filled(b, 0)` and `g as usize % b`
becomes `g % b`; `if let Some(&v) = memo.get(cnt)` to `if let Some(v) =
memo.get(cnt).cloned()`; `let mut res = 0` to `let mut res: i32 = 0`;
`HashMap::new()` to `Map.new()`; `Solution::` to `Solution.` at the
harness's 10 calls; and the harness's `as i64` on the `i32` result taken
off. The solution takes an `i32` batch and `Vec[i32]` groups, so its
harness builds them so. Every other arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, for at most 7 groups: every order of the groups served, the
donuts left from the last batch carried from group to group, and a group
counted happy when none are left as it arrives. It runs 1500 random
cases of 1 to 7 groups of 1 to 20 customers and 300 of 8 to 30 groups up
to `10^9`, each at a batch of 1 to 9. Each arm meets six properties on
each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, for at most 7 groups |
| P2 | the groups listed backwards give the same answer |
| P3 | one more group of a whole batch adds one happy group |
| P4 | every group of whole batches is happy, and so is the first of the rest, and no more groups are happy than there are |
| P5 | a whole batch more in every group changes nothing |
| P6 | the ★ arm's answer |

It checks clean as first written. All 52,500 checks pass on every arm:
`1800 cases: checksum 640291734, 52500 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, running the ★ arm's mirror over the same cases
and checking it against every order for the small ones, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the counts written in base 2, so different states share a key | P6 28 |
| M2 | ★: every group of half a batch counted happy | P1 408, P4 130, P6 2168 |
| M3 | plain: the next group happy when what is left is whole batches | P1 1028, P4 467, P6 1226 |
| M4 | plain: the groups of whole batches left out | P1 830, P3 1800, P4 702, P6 1115 |
| M5 | table: a group happy one donut short of a fresh batch | P1 846, P4 419, P6 994 |
| M6 | table: each state given its last way in, not its best | P1 445, P6 674 |
| M7 | dense: an odd group of half a batch dropped | P1 160, P4 70, P6 194 |
| M8 | dense: the memo indexed by half of each count | P1 72, P6 116 |
| M9 | solution: the happy group added once per remainder tried | P1 843, P4 481, P6 1077 |
| M10 | solution: the groups of whole batches left out | P1 830, P3 1800, P4 702, P6 1115 |

## Benchmarks

The bench makes 3000 calls of the ★ arm, each on 30 groups at a batch of
7 to 9 whose remainders are drawn from the batch's lower half, so that
no two groups pair off and the search meets the most states. The C
mirror memoizes in an open-addressing hash table keyed by the counts in
base 31. It checks clean as first written. Every implementation prints
`3000 cases: checksum 865485860`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.66 s against Rust's 0.78 s (0.81 s with
overflow checks on), C's 0.26 s and Go's 1.2 s; Python takes 9.0 s.
