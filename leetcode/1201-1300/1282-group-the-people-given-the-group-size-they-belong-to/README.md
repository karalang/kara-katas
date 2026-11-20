# 1282. Group the People Given the Group Size They Belong To

There are `n` people, labelled `0` to `n - 1`, each in exactly one group.
`groupSizes[i]` is the size of the group person `i` is in. Return a list
of groups such that each person is in a group of size `groupSizes[i]`.
Any valid answer is accepted, and the input always has one.

```
groupSizes = [3,3,3,3,3,1,3]  ->  [[5],[0,1,2],[3,4,6]]
groupSizes = [2,1,3,3,3,2]    ->  [[1],[0,5],[2,3,4]]
```

**Constraints:** `1 <= n <= 500`, `1 <= groupSizes[i] <= n`.

The arms are `fn group_the_people(group_sizes: Vec[i64]) -> Vec[Vec[i64]]`.
Since any grouping is accepted, the harness prints one form of it: each
group sorted and the groups ordered by their first person, with a check
that the grouping is valid.

## Approaches

| file | mechanism |
|---|---|
| `group_the_people.kara` ★ | by buckets: one open group per size, held in a `Vec` indexed by the size; each person joins the open group of their size, and a group that reaches its size is handed out and a new one opened. O(n) |
| `group_the_people_map.kara` | by a map: every person filed under their size in a `Map` by `entry().or_insert()`, and each size's people then cut into groups of that size by `chunks` |
| `group_the_people_sort.kara` | by sorting: the people ordered by `sort_by_key` on (size, person), so that each size's people stand together, and the order then cut into consecutive slices, each as long as its first person's size. O(n log n) |
| `group_the_people_labels.kara` | by labels, in two passes: the first gives every person a group number, the open group of their size (an `Option` per size) or a new one, closing a group once it is full; the second files every person under their number |
| `group_the_people_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap` of open groups by `entry().or_insert`, a full group handed out by `std::mem::take`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's two examples, everyone
alone (`[1,1,1]`) and everyone together (`[4,4,4,4]`), each with its
validity (`[[0,1,2],[3,4,6],[5]] true`), then 1000 random problems of up
to 500 people (`1000 random problems: 240698 people in 12970 groups, 1000
valid, checksum 777311157`). The map arm walks a `Map`, whose order is
random per process, but the harness's sorted form does not see it.
`group_the_people.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: of the four arms written in Kāra, the ★ arm took 2
`redundant_cast` fixes (`person as i64` and `len() as i64`: an
`enumerate` index and a `len()` are already `i64`), and the sort arm 2
`E0209` fixes (`sort_by_key` hands its closure the element by value, so
`*p` became `p`); the map and labels arms checked clean as first written.
The solution arm takes one round of 20 fixes by `karac fix`'s count: the
`use std::collections::HashMap` line deleted, `HashMap<..>` and `Vec<..>`
became `Map[..]` and `Vec[..]`, `::` paths took `.`, `vec![]` became
`Vec.new()`, the `&s` pattern lost its `&`, `std::mem::take(e)` became
`take(mut e)`, `s as usize` became `s as i64`, and `struct Solution;`
became `struct Solution {}`. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for every person, every group is searched, and the person must
be found exactly once, in a group as long as their size, and the groups
must hold `n` people in all. 2000 random problems of up to 40 people,
with sizes mostly up to 5 so that a size repeats; each property is
checked on every arm. P6 asks more than the statement does, which
accepts any grouping: it holds because every arm puts each size's people
into groups in the order they are numbered.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the number of groups: each size's people over the size, summed |
| P3 | the people in reverse order: the answer, every person renamed back, is valid |
| P4 | a second problem appended: valid, with as many groups as the two apart |
| P5 | every person doubled and every size doubled: valid, with as many groups |
| P6 | the ★ arm's answer, in the sorted form |

All 60,000 checks pass on every arm: `2000 problems: checksum 535937682,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a group handed out one person short | P1 2000, P2 1547, P3 2000, P4 2000, P5 2000, P6 8000 |
| S2 | ★: every person filed under the next number | P1 2000, P3 2000, P4 2000, P5 2000, P6 8000 |
| M1 | map: every size's people cut in twos | P1 1874, P2 1807, P3 1874, P4 1992, P5 1904, P6 1874 |
| M2 | map: each group's first person dropped | P1 2000, P3 2000, P4 2000, P5 2000, P6 2000 |
| T1 | sort: each slice one person short | P1 2000, P3 2000, P4 2000, P5 2000, P6 2000 |
| T2 | sort: each size's even-numbered people before its odd ones | P6 1010 |
| L1 | labels: a group closed only past its size | P1 1471, P2 1029, P3 1471, P4 1928, P5 1471, P6 1471 |
| L2 | labels: a group filled with its own number instead of its people | P1 1904, P3 1904, P4 1987, P5 2000, P6 1904 |
| O1 | solution: a group handed out at two people, whatever its size | P1 1963, P2 1763, P3 1963, P4 1996, P5 1904, P6 1963 |
| O2 | solution: a full group copied out but not emptied (`clone` for `take`) | P1 1471, P2 1471, P3 1471, P4 1928, P5 1471, P6 1471 |

Nine are caught by P1, the statement read literally. P2, the count of
groups, sees only the edits that change how many groups there are (S1,
M1, L1, O1, O2); the rest keep the count and get the people wrong. O2 is
the mistake `std::mem::take` exists to prevent: the open group is never
emptied, so a size's later people pile into it and never fill it again,
which shows on every problem where some size has two groups or more,
1471 of 2000. L1 fails on exactly the same problems, for the same
reason. T2 is a different valid grouping, which the statement accepts
and P1 to P5 pass: only P6, which asks for the ★ arm's grouping, sees
it. It replaced a first T2 that sorted each size's people in reverse
order, which was equivalent: a size's people are cut into the same runs
read from either end.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (one open group per size, handed out when full) on 50 problems of
10000 people, built once, 500 rounds, every group folded into a
checksum. Every program prints `500 rounds of 50 problems of 10000
people: checksum 326738602`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 3.113 to 3.180 s | 3.160 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 3.091 to 3.248 s | 3.130 s |
| Rust (`rustc -O`) | 3.291 to 3.532 s | 3.327 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.370 to 3.523 s | 3.448 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 3.372 to 3.624 s | 3.442 s |
| C (`clang -O3`) | 3.526 to 3.628 s | 3.597 s |
| C (`clang -O3 -march=x86-64-v3`) | 3.574 to 3.702 s | 3.630 s |
| Go | 11.15 to 12.14 s | 11.56 s |
| Python | 58.23 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 9% ahead of Rust with overflow checks on (3.130 s
against 3.448 s). Kāra is about 13% ahead of C (3.130 s against 3.597
s); Go takes about 3.7x Kāra's time. Python takes about 19x Kāra's time.
No profile was taken.
