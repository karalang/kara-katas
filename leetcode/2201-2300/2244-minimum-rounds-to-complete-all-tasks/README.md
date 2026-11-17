# 2244. Minimum Rounds to Complete All Tasks

You are given a **0-indexed** integer array `tasks`, where `tasks[i]`
represents the difficulty level of a task. In each round, you can
complete either 2 or 3 tasks of the **same difficulty level**.

Return *the **minimum** rounds required to complete all the tasks, or
`-1` if it is not possible to complete all the tasks.*

```
tasks = [2,2,3,3,2,4,4,4,4,4]  ->  4
tasks = [2,3,3]                ->  -1
```

**Constraints:** `1 <= tasks.length <= 10^5`; `1 <= tasks[i] <= 10^9`.

Each difficulty is done on its own. One task alone can never be done;
any other count `c` takes `ceil(c / 3)` rounds: threes, with one two in
place of the last three when `c % 3 == 2`, and two twos in place of the
last four when `c % 3 == 1`. O(n).

## Approaches

| file | mechanism |
|---|---|
| `rounds.kara` ★ | the counts in a `Map`, then `-1` at a count of one and `(c + 2) / 3` summed over the rest; the sum does not depend on the map's order |
| `rounds_sort.kara` | no map: the tasks sorted, so each difficulty is a run, and each run's length treated as above. O(n log n) |
| `rounds_dp.kara` | no formula: the fewest rounds for every count up to the largest by dynamic programming over steps of two and three, a `Vec[Option[i64]]` with `None` where a count cannot be made and a `match` on the pair of predecessors; the counts in a `SortedMap`. O(n + largest count) |
| `rounds_enum.kara` | an `enum Plan` of `Impossible` and `Rounds(i64)`, `Plan.for_count` choosing threes and then the twos the remainder needs, and `then` (`ref self`) adding two plans, `Impossible` absorbing |
| `rounds_iter.kara` | iterator chains: the counts gathered by a `fold` into a `Map`, each count `map`ped to `Some` rounds or `None`, the whole `collect`ed into an `Option[Vec[i64]]` and `map`ped to its `sum`, `unwrap_or(-1)` |
| `rounds_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out, a `HashMap<i32, i32>` filled by `*map.entry(t).or_insert(0) += 1` over `for &t in &tasks`, then `for &c in map.values()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four
more (one task, two alike, four alike as two rounds of two, and seven
alike beside a pair of the largest difficulty), each with its answer;
then how many of 3000 lists of 1 to 60 tasks of 1 to 20 difficulties
can be done, with a checksum of the answers; then the constraints'
longest, 10^5 tasks of difficulties up to 10^9 drawn in pairs and
triples so that every count is at least two; then the same list with
its last task changed to a fresh difficulty, which is alone. `rounds.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 20 edits: `Vec<..>` and
`HashMap<..>` to `Vec[..]` and `Map[..]`, `HashMap::new()` to
`Map.new()`, the `use std::collections::HashMap` removed, `for &t in
&tasks` to `for t in ref tasks`, the `&` pattern dropped from `for &c`
and from the adapter's closure, `let mut ans = 0` typed `i32`, `struct
Solution;` to `struct Solution {}`, `Solution::` to `Solution.`, and the
adapter's `as i64` removed as lossless.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each difficulty every number of rounds of three and of
two tried, kept when they finish exactly its tasks, and the fewest
taken; `-1` when a difficulty has none; no formula. It checks 300
random lists of 1 to 30 tasks of 1 to 8 difficulties; then 30 built of
pairs and triples, so that every difficulty can be done; then 30 of
those with one lone task added. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the fewest rounds, read literally, or -1 |
| P2 | the tasks in reverse order: the same answer |
| P3 | every difficulty renamed `d -> 7d + 3`: the same answer |
| P4 | three tasks of a new difficulty: one round more, or -1 again |
| P5 | -1 exactly when some difficulty has one task; otherwise at least a third and at most a half of the tasks |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 940205384, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
counts with `collections.Counter` and finds each count's fewest rounds
by breadth-first search over the tasks left.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: every count started at one | P1 285, P4 360, P5 193, P6 285 |
| M4 | ★: rounds of two only | P1 142, P6 142 |
| M5 | ★: a lone task answered 0 | P1 163, P4 163, P5 163, P6 163 |
| M7 | sort: a run cut at three | P1 106, P5 106, P6 106 |
| M9 | sort: reversed, not sorted | P1 131, P5 130, P6 131 |
| M10 | sort: a task skipped after each run | P1 141, P5 105, P6 141 |
| M12 | dp: a step of one for two | P1 147, P5 70, P6 147 |
| M14 | dp: nothing counted as a round | P1 197, P4 197, P5 123, P6 197 |
| M16 | dp: two never made | P1 88, P5 88, P6 88 |
| M17 | enum: a round too many for a multiple of three | P1 122, P4 197, P5 30, P6 122 |
| M19 | enum: twos only for a remainder of two | P1 72, P6 72 |
| M21 | enum: the plan begun at one round | P1 197, P5 30, P6 197 |
| M22 | iter: a lone task counted as none | P1 163, P5 163, P6 163 |
| M24 | iter: each task counted twice | P1 360, P4 360, P5 360, P6 360 |
| M26 | iter: a pair called impossible | P1 64, P5 64, P6 64 |
| M27 | solution: a pair called impossible | P1 133, P5 133, P6 133 |
| M31 | solution: the difficulties folded to two | P1 167, P4 27, P5 115, P6 167 |

P1 and P6 kill all seventeen, P5 fifteen and P4 six. P2 and P3 kill
none: every arm counts, and a count changes neither with the order of
the tasks nor with the names of the difficulties. They stay as checks
that no arm reads either, which the only mutant they catch shows (M20,
below). P5 misses only the edits that still answer `-1` exactly when it
should and stay within a third and a half of the tasks (M4, M19); P4
catches the edits that miscount three, or answer a lone task with
something other than `-1`.

Of the thirty-one, fourteen were not kept, and none crashes or survives.
One differs between the backends, and is left out for that: the enum
arm's `then` answering no rounds where an `Impossible` plan meets a
possible one (M20) lets a later difficulty wipe out an impossible one,
so the answer depends on which difficulty the `Map` hands over first, and the map's
order is random per process, so its failures (P2 among them) change
from run to run. Eight fail as a kept one does: the ★ arm's pair
called impossible (M1) as the template's (M27); the ★ arm's lone task
skipped and the dp arm's impossible count passed over (M6, M15) as the
iter arm's lone task counted as none (M22); the sort arm's runs one
longer (M8) as the ★ arm's counts started at one (M2); the dp arm's
slower of the two ways (M13) as the ★ arm's rounds of two only (M4);
the iter arm's impossible answered 0 (M25) as the ★ arm's (M5); the
template's answer begun at one (M29) as the enum arm's plan begun at
one round (M21); and the template's tasks counted twice (M30) as the
iter arm's (M24). Three fail alike in a group of their own: ceil
rounded down for a remainder of one in the ★, enum and iter arms (M3,
M18, M23). Two fail their own way and are left out for the count of
three: the sort arm's rounds rounded down (M11) and the template's
rounds of two only (M28).

## Verification

Every arm prints the same output as `rounds.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the sort arm takes 0.5 s, the ★ arm 0.65 s, the
enum arm 0.8 s, the template 0.9 s, the iter arm 1.0 s, the dp arm
2.2 s, and the differential 0.6 s.

## Benchmarks

The bench answers 40 lists of 10^5 tasks with the ★ arm in all five
languages: 3 * 10^4 difficulties up to 10^9 per list, the tasks drawn
from them in pairs so that no task is alone and every difficulty is
counted to the end. C counts in an open-addressing hash table with
linear probing; Rust uses `HashMap`, Go `map` and Python `dict`. Every
implementation prints `40 lists of 100000 tasks: checksum 914741058`.

BENCHTAB
