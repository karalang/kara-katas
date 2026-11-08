# 2015. Average Height of Buildings in Each Segment

A perfectly straight street is a number line. `buildings[i] = [start, end,
height]` is a building of that height over the half-closed stretch
`[start, end)`. Describe the street with the fewest segments `[left,
right, average]`, where the average is the integer division of the sum of
the heights over `[left, right)` by the number of buildings there. A
stretch with no building is left out, and two segments that meet with the
same average are one.

```
buildings = [[1,4,2],[3,9,4]]               ->  [[1,3,2],[3,4,3],[4,9,4]]
buildings = [[1,3,2],[2,5,3],[2,8,3]]       ->  [[1,3,2],[3,8,3]]
buildings = [[1,2,1],[5,6,1]]               ->  [[1,2,1],[5,6,1]]
```

**Constraints:** `1 <= buildings.length <= 10^5`; `0 <= start < end <=
10^8`; `1 <= height <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `average.kara` ★ | each building two events, (start, height, 1) and (end, -height, -1), sorted; a sweep applies every event at a position, then describes the stretch to the next position by the running sum over the running count, joined to the last segment when it continues it. O(n log n) |
| `average_map.kara` | a `SortedMap` from each position to its change in sum and count; a walk in order describes the stretch from the last position before applying this one's change, joining through `pop` and a guarded `match`. O(n log n) |
| `average_diff.kara` | the starts and ends sorted and `dedup`ped, each building's change put at its positions' indices by `binary_search` into two difference arrays, whose prefix sums describe each stretch. O(n log n) |
| `average_brute.kara` | the positions cut the street into stretches no building begins or ends inside; each stretch scans every building for those over it, and a second pass joins. O(n^2) |
| `average_heap.kara` | the buildings sorted by start, a `PriorityQueue` of (end, height) for those standing; the walk moves to the next start or the earliest end, whichever comes first. O(n log n) |
| `average_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, a `BTreeMap<i32, (i64, i32)>` of changes through `entry().or_insert()`, `ans.last_mut()` in a guarded `match`, `Vec<Vec<i32>>`, a `&Vec` wrapper), carried by `karac fix` to two remaining errors: blocked by B-2026-11-08-46 and B-2026-11-08-21 |
| `differential.kara` | the five arms that check against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the number of segments and a checksum for
2000 streets of 1 to 12 buildings on up to 40 positions, and for 4 streets
of 2000 buildings over 1000 to 99000000 positions. `average.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms that check and the
statement read literally: each unit stretch `[x, x + 1)` from 0 to 200
given the average of the buildings over it, stretches with none left out,
and neighbours with the same average joined. It checks 1500 problems of 1
to 10 buildings starting below 1 to 30, up to 10 long and 6 high. Every
random choice of a problem (the buildings, a shuffle, a shift) is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the buildings shuffled leave the answer |
| P3 | every position moved along by the same amount moves every segment |
| P4 | the street read the other way, position `p` turned into `100 - p`, turns the answer round |
| P5 | every building listed twice leaves the answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1500 problems: checksum 363489651, 45000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust-template arm
joins it, as a sixth, once it checks.

## Mutation testing

Twenty-five edits to the differential, five to each of its arms, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three
to each arm. All twenty-five are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an end's height not taken off | P1 1313, P4 1325, P6 1313 |
| M2 | ★: one event per position applied | P1 401, P5 164, P6 401 |
| M3 | ★: the average rounded up | P1 790, P6 790 |
| M4 | map: the stretch described after the change | P1 1346, P3 1463, P4 1500, P6 1346 |
| M5 | map: a start's change replacing the one there | P1 915, P2 630, P4 1056, P5 1096, P6 915 |
| M6 | map: joined whatever the average | P1 834, P4 703, P6 834 |
| M7 | diff: the counts never taken off | P1 1317, P4 1326, P6 1317 |
| M8 | diff: a stretch with nothing on it kept | P1 754, P6 754 |
| M9 | diff: the first position's change never applied | P1 1500, P4 930, P6 1500 |
| M10 | brute: a stretch under one building left out | P1 1423, P5 1423, P6 1423 |
| M11 | brute: a building ending inside the stretch counted | P1 1103, P4 966, P6 1103 |
| M12 | brute: the heights summed without the count | P1 1152, P5 1500, P6 1152 |
| M13 | heap: the next start always taken first | P1 970, P4 516, P6 970 |
| M14 | heap: the buildings never sorted | P1 1116, P2 1105, P4 1251, P5 1273, P6 1116 |
| M15 | heap: the average over the heap and one more | P1 1491, P5 761, P6 1491 |

P1 and P6 kill all fifteen, P4 nine, P5 six, P2 two and P3 one. P4 reads
the street from the other end, which turns each building's start into an
end, so it sees every edit that treats the two ends of a building, or the
two sides of a position, unevenly: an end that takes nothing off (M1, M7),
a stretch described from the wrong side of its change (M4), a building
counted past its end (M11), the walk taking a start before an end (M13),
and the first position skipped (M9). It misses the edits that are their
own mirror image: an average rounded up (M3), an empty stretch kept (M8),
and the edits to the count alone (M2, M10, M12, M15). P5 lists every
building twice, which leaves every average alone but doubles every count
and sum, so it sees the edits that read a count or a sum by its size
rather than as a ratio: the sum without the count (M12), a stretch under
one building (M10), one more than the heap holds (M15), a change replaced
rather than added to (M5), and one event applied per position (M2). P2
sees only the two edits that let the input's order through: a change
replaced, which keeps whichever building came last (M5), and the heap arm
unsorted (M14). P3 moves the street along, and sees only the walk that
starts its first stretch at position 0 rather than at the first change
(M4).

The other ten fail as a kept one does, or with counts of their own. An
end's height not taken off fails alike in the ★ and heap arms (M1); the
map arm's joined segment keeping its old end and the diff arm's joined
segment ending at the old stretch fail alike (P1 1035, P4 759), and a
stretch never joined (★) fails P1 1035 alone; joining across a gap
fails alike in the ★ and brute arms, P1 412; the diff arm's end marked one
position late fails as M11; the map arm dropping the last segment when a
new one starts and the heap arm letting a building go one position early
fail with counts of their own. Five drafts were replaced. The diff arm
never deduplicating its positions, the brute arm counting a building that
covers only a stretch's start, and the heap arm letting only one ending
building go per step never fail: a stretch of no length adds nothing, no
building ends inside a stretch, and the next step lets the rest go. The
brute arm's last stretch dropped by `windows(2).take(..)` was refused by
the checker (`take` is an iterator method, and `windows` returns a `Vec`),
and was rewritten as a bound on the stretch's right end.

## Verification

Every arm but the Rust template prints the same output as `average.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports nothing
on any of them. Under `karac __mir-run` the arms take 0.38 s (★) to 5.2 s
(brute) and the differential 5.0 s.

The five arms were written in Kāra. The brute arm's
`flat_map(|(start, end, _)| [start, end])` drew one fix: Kāra's `flat_map`
takes a closure that returns an `Iterator`, and the array literal became
`[start, end].into_iter()`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds (32, 2 and 6 edits: the `use`, the struct, the
`Vec<..>` and `BTreeMap<..>` types, `BTreeMap` to `SortedMap`, the `::`
paths, `vec![..]`, `&&`, the `&` patterns and the `&Vec` parameter, the
tuple `let (mut sum, mut cnt)`, and the casts an `i32` no longer needs)
to two errors it has no fix for. `match ans.last_mut() { Some(last) if
last[1] == prev && last[2] == avg => last[1] = pos, _ => ans.push(..) }`
is refused, since a `Vec` has no `last_mut`; the message says to write
through an index, with no machine fix (B-2026-11-08-46). And `let mut prev =
0; .. prev = pos;` leaves `prev` an `i64` where Rust types it `i32` from
the assignment, so `ans.push([prev, pos, avg])` mixes the two
(B-2026-11-08-21: an assignment now fixes a literal's type, but `prev` is
first read as an element of a collection literal, which settles it before
the `Vec[i32]` slot is reached). With
`prev: i32` and the `match` written through an index by hand, the arm
checks clean and prints the mirror's output.

## Benchmarks

The bench builds 60 streets of 10000 buildings once in all five languages,
positions up to 1000000, the buildings longer and the heights higher on
each street, and runs the ★ arm on each for 5 rounds: 300 calls, each
sorting 20000 events. Every implementation prints `300 calls: 2994430
segments, checksum 457485271`. Every language builds and sorts the events
per call, as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.373 to 0.431 s | 0.385 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.374 to 0.442 s | 0.407 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.799 to 0.895 s | 0.841 s |
| Kāra (`karac build`) | 0.819 to 0.875 s | 0.841 s |
| C (`clang -O3`) | 1.024 to 1.147 s | 1.055 s |
| Go | 1.352 to 1.456 s | 1.412 s |
| Python | 5.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.818 s) is not above its real time (0.841 s).

The sequential Kāra program is 2.07x Rust under overflow checks and 0.80x
C. Rust is about twice as fast here because of the sort: Kāra sends a Vec
of tuples to the runtime's generic merge sort, which calls the comparison
through a pointer, where Rust monomorphizes its stable sort. That is
B-2026-11-08-85; a `Vec[i64]` sort keeps pace with Rust.