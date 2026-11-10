# 1101. The Earliest Moment When Everyone Become Friends

There are `n` people in a social group labeled from `0` to `n - 1`. You
are given an array `logs` where `logs[i] = [timestamp_i, x_i, y_i]`
indicates that `x_i` and `y_i` will be friends at the time
`timestamp_i`.

Friendship is symmetric: if `a` is friends with `b`, then `b` is
friends with `a`. Also, person `a` is acquainted with a person `b` if
`a` is friends with `b`, or `a` is a friend of someone acquainted with
`b`.

Return the earliest time for which every person became acquainted with
every other person. If there is no such earliest time, return `-1`.

```
logs = [[20190101,0,1],[20190104,3,4],[20190107,2,3],[20190211,1,5],
        [20190224,2,4],[20190301,0,3],[20190312,1,2],[20190322,4,5]],
n = 6                                                    ->  20190301
logs = [[0,2,0],[1,0,1],[3,0,3],[4,1,2],[7,3,1]], n = 4  ->  3
```

**Constraints:** `2 <= n <= 100`; `1 <= logs.length <= 10^4`;
`logs[i].length == 3`; `0 <= timestamp_i <= 10^9`; `0 <= x_i, y_i <= n -
1`; `x_i != y_i`; all the values `timestamp_i` are unique; all the pairs
`(x_i, y_i)` occur at most one time in the input.

The arms are `fn earliest_acq(logs: Vec[Vec[i64]], n: i64) -> i64`. The
logs come in no order, so every arm puts them in time order first, or
takes them out of a heap in that order. With every pair at most once,
100 people have at most 4950 logs.

## Approaches

| file | mechanism |
|---|---|
| `earliest_acq.kara` ★ | union-find over the logs in time order: each log joins two groups, the parents halving the path as they are followed and the smaller group hung under the larger, and the moment the groups come to one is the answer. `sort_by_key`, then a `while` loop for `find` over a `mut ref Vec[i64]` |
| `earliest_acq_rank.kara` | a disjoint-set `struct` with methods on `mut ref self`: `find` recursive, every node on the path pointed at the root, and `union` by rank, returning whether two groups joined. The logs sorted with `sort_by` and `cmp` |
| `earliest_acq_search.kara` | binary search over the moments: with the logs sorted, whether everyone is acquainted after the first `i` logs only ever turns from false to true, so a binary search finds the first `i`, each probe a breadth-first search from person 0 over a `VecDeque` |
| `earliest_acq_relabel.kara` | every person labelled with their group, and each group's members in a list: two groups join by relabelling the members of the smaller and moving them to the larger with `swap` and `take`, so each person moves at most log n times |
| `earliest_acq_heap.kara` | the logs never sorted: a `PriorityQueue[(i64, i64, i64)]` collected from them hands them out earliest first, and a plain union-find, its parents shortened by recursion, counts the groups down to one |
| `earliest_acq_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `mut logs: Vec<Vec<i32>>`, `sort_unstable_by_key`, a `fn find(p: &mut Vec<usize>, x: usize)` nested in the method), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the answers for LeetCode's two
examples and seven more (two people and one log, three people and one,
two logs out of order, two pairs that never meet, a later log inside a
group already joined, a moment of 10^9, four logs given latest first,
three of them meeting at one person), then over 2000 random groups of 2 to 30 people with up
to 60 logs how many came to one (`1211 come to one, checksum
934234363`), and two of LeetCode's largest: 100 people with every pair
of them in a random order, and 100 people in a chain whose links are
given last first. `earliest_acq.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the moments in order, and at each a depth-first search from
person 0 over the logs at or before it, until it reaches everyone. It
checks 2000 problems in four kinds of 500, every log at a distinct
random moment below 10^6 and its pair written either way round: 2 to 12
people with up to 30 random pairs; 2 to 6 people with every pair; 2 to
20 people joined by a random tree and up to 5 more pairs; and two
groups of 2 to 8 people each joined by a tree, with one pair between
them or, a quarter of the time, none. Every random choice is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | -1 only when everyone is never acquainted; otherwise a moment of the logs at which everyone is, and one before which they are not, both judged by a second reading: every person given the smallest label among their friends until nothing changes |
| P3 | the logs in another order, reversed and rotated, with each pair written the other way round, give the same answer |
| P4 | the people renamed by a random permutation give the same answer |
| P5 | every moment `t` moved to `3t + 7` moves the answer the same way |
| P6 | one more person, befriended by one of the group at a moment of their own, is acquainted at the later of that moment and the answer; and without the log at the answer's moment, everyone is acquainted only later, if at all |

All 72,000 checks pass on every arm: `2000 problems: checksum
718878081, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, by a union-find at each moment, gives the same
checksum.

P1 builds the answer and P2 judges it by another reading; P3 to P6
compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a pair already in one group counted as a join | P1 575, P2 575, P6 775 |
| M2 | ★: the logs never sorted | P1 1338, P2 1338, P3 1265, P6 1218 |
| M3 | ★: one step taken toward the root | P1 3, P2 3, P3 10, P6 5 |
| M4 | ★: the last moment answered when never acquainted | stops: index out of bounds |
| M5 | rank: the second friend's root not found | P1 545, P2 545, P3 79, P6 745 |
| M6 | rank: any join answered | P1 1801, P2 1801, P6 2000 |
| M7 | search: friendships one way only | P1 1561, P2 1561, P3 775, P4 407, P6 559 |
| M8 | search: each probe one log short | P1 1775, P2 1775, P6 331 |
| M9 | relabel: the moved members lost | P1 1775, P2 1775 |
| M10 | relabel: everyone counted twice | P1 1847, P2 1847, P6 1295 |
| M11 | heap: a node under the root taken for it | stops: stack overflow |
| M12 | heap: the last log never read | P1 855, P2 855, P6 101 |
| M13 | solution: the logs sorted by the first friend | P1 1366, P2 1366, P3 1376, P4 1220, P6 1203 |
| M14 | solution: answered one moment late | P1 1775, P2 1775, P5 1775, P6 581 |
| M15 | solution: any log of person 0 a join | P1 146, P2 146, P3 251, P4 213, P6 276 |

Of the thirteen that run to the end, P1 and P2 catch all thirteen, P6
twelve, P3 six, P4 three and P5 one. P1 and P2 fail on the same
problems every time: an answer that is a moment of the logs, reached
then and not before, is the literal one. M3 is the narrow one: union by
size keeps the trees shallow, and a `find` that stops after one step
goes wrong only on a path of three or more, which 3 problems in 2000
build and 10 more build once the logs come in another order. P4 sees
the three edits that treat one person or one side of a pair apart from
the other (M7, M13, M15), and P5 only the answer one moment late (M14),
the one edit that changes the moment rather than which log gives it.
P3 to P6, which compare the arm only with itself, catch all but M9: an
arm that loses the members it moves never sees everyone in one group,
answers -1 to every problem, and agrees with itself on every changed
one. The two that stop do so on a problem P6 builds: M4 indexes the
last log of a group whose only log has been taken away, and M11's
`find`, stopping short of the root, joins a group to itself and ends
in a cycle of parents that its recursion never leaves.

Of the fifteen not kept, three fail as a kept edit: the heap arm
counting one group too many and reading the second friend as the first
answer -1 to everything, as M9 does, and the search arm never taking
the first log as the answer stops on an index out of bounds, as M4
does. The other twelve fail in ways of their own but were not needed:
the ★ arm answering one join early, the rank arm counting a pair
already joined, sorting latest first and taking the parent for the
root, the search arm passing the bound by one and answering the log
after the moment, the relabel arm keeping the moved members' labels,
answering one person short and taking the friend's own number for
their label, the heap arm joining the friends rather than their groups,
and the solution arm answering one join early and taking the parent
for the root.

## Verification

Every arm prints the same output as `earliest_acq.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found no compiler gap. The ★ arm was written as Kāra, and the
other five as Rust writes them; `karac fix` carried every Rust spelling
to a clean check:

- The rank arm in three rounds: `&mut self` to `mut ref self`, `vec![0;
  n as usize]` to `Vec.filled(n, 0)`, `DisjointSet::new` to
  `DisjointSet.new`, `cmp(&b[0])` to `cmp(b[0])`, `for log in &logs` to
  `for log in ref logs`, and `&&` to `and`.
- The search arm in three: `vec![..; n as usize]` to `Vec.filled`,
  `VecDeque::new()` to `VecDeque.new()`, `!` to `not`, `let (mut lo,
  mut hi)` to `let mut (lo, hi)`, and the `as usize` and `as i64` casts
  on indices and lengths dropped.
- The relabel arm in two: `vec![p]` to `[p]`, `std::mem::swap(&mut a,
  &mut b)` and `std::mem::take(&mut members[b])` to `swap(mut a, mut b)`
  and `take(mut members[b])`.
- The heap arm in two: `&mut Vec<i64>` to `mut ref Vec[i64]` and the
  calls' `&mut parent` to `mut parent`.
- The Rust solution in four: the `find` nested in the method moved out
  to the top level, `mut logs: Vec<Vec<i32>>` to `logs: own
  Vec[Vec[i32]]` and a `let mut logs = logs;`, `&mut p` to `mut p`,
  `struct Solution {}`, and `sort_unstable_by_key` to `sort_by_key`.

## Benchmarks

The bench builds 64 groups of 100 people once, LeetCode's most, each
with every pair of them at a moment from a shuffle of 0 to 4949 (times
1000): 4950 logs, the most LeetCode's pairs allow. Each of 20 rounds
swaps the moments of two logs in every group and finds its earliest
moment with the ★ arm, which copies the logs, sorts the copy and runs
the union-find: 1280 calls over 6.3 million logs. Every implementation
prints `20 rounds over 64 groups of 100 people: moments sum to
323606000, checksum 517156166`. Each log is its own heap array in every
language: C `malloc`s each copy and sorts the pointers with `qsort`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.467 to 0.577 s | 0.482 s |
| Kāra (`karac build`) | 0.467 to 0.570 s | 0.500 s |
| Rust (`rustc -O`) | 0.537 to 0.724 s | 0.558 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.537 to 0.634 s | 0.578 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.538 to 0.663 s | 0.583 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.847 to 1.003 s | 0.883 s |
| C (`clang -O3`) | 0.858 to 0.943 s | 0.899 s |
| Go | 1.427 to 1.637 s | 1.536 s |
| Python | 2.360 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is the fastest, Rust about 1.17x its time, C about 1.8x and
Go about 3x. Each call sorts 4950 logs: C sorts its pointers with
`qsort` and Go with `sort.Slice`, the kata convention, and neither can
inline the comparison. Python takes about 5x Kāra's time.
