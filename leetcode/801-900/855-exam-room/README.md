# 855. Exam Room

An exam room has `n` seats in one row, numbered `0` to `n - 1`. A
student who enters sits in the seat that is farthest from the closest
other student; among several such seats, the one with the lowest number;
in an empty room, seat `0`. Implement `ExamRoom(n)`, `seat()`, which
seats a student and returns the seat, and `leave(p)`, after which the
student at seat `p` leaves.

```
ExamRoom(10)
seat() -> 0, seat() -> 9, seat() -> 4, seat() -> 2, leave(4), seat() -> 5
```

**Constraints:** `1 <= n <= 10^9`, `leave(p)` is only called for a seat
with a student in it, and there are at most `10^4` calls to `seat` and
`leave` in all.

## Approaches

| file | mechanism |
|---|---|
| `exam_room.kara` ★ | the taken seats in a sorted set, walked in order for the widest gap: the gap before the first student is worth its whole width (the new student sits at seat 0), a gap between two students half its width (the student sits in the middle), the gap after the last its whole width again (seat `n - 1`). The first gap worth the most wins, which is also the lowest seat. O(k) a seat and O(log k) a leave, for `k` students |
| `exam_room_list.kara` | the same scan over a sorted vector, the gaps between neighbours through `windows(2)`; the new seat goes where a binary search says it belongs, and a leave finds the seat with `binary_search` and removes it. O(k) for both |
| `exam_room_heap.kara` | every gap is an entry in a priority queue keyed by its worth, negated, and then by the seat it offers, so the first entry is the widest gap and the lowest seat among equals; the ends are the imaginary seats -1 and `n`, and maps hold each student's neighbours. A leave joins the neighbours and pushes their gap without touching the queue, so a seat pops entries until one still joins two neighbours. O(log) amortised |
| `exam_room_intervals.kara` | the same gaps and keys in an ordered set, kept exact: a seat takes the smallest key and replaces its gap by the two around the new student, and a leave replaces the two gaps around the seat by the one that joins its neighbours. O(log k) for both |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's example; ten more (a room
of one seat, entered, left and entered again, rooms of two to five seats
filled in turn, a leave at either end that brings the next student back
to the same end, a room whose two end students leave, and four students
in a room of 10^9 seats); a room of 10^9 seats through 2,000 random
calls, with the sum of the seats given and a checksum; and 300 random
rooms of up to 30 seats and 60 calls, with the same. A random call is a
seat in an empty room, a leave in a full one, and otherwise a seat two
times in three and a leave of a random student the third. `exam_room.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each seat tries every free seat, measures its distance to the
closest student, and takes the farthest, the lowest among equals. Its
1,600 rooms come in four kinds of 400: rooms of 1 to 6 seats, rooms of 7
to 30 seats that mostly fill, rooms of 7 to 30 with as many leaves as
seats, and rooms of 7 to 30 filled before their calls start. Each has 1
to 40 random calls, made against the statement so that every leave names
a taken seat; they hold 26,050 seats in all. Each case also seats 1 to
30 students in a room of 10^9 seats, too large for the statement, where
the arms are held to each other.

| | property |
|---|---|
| P1 | the statement's seats |
| P2 | every seat given is in the room and free |
| P3 | after each seat, the student leaving and another entering gets the same seat back |
| P4 | between two leaves, no student sits farther from the closest other student than the one before |
| P5 | the student entering an empty room sits at seat 0 |
| P6 | in the room of 10^9 seats, at least two of the other three arms give the arm's seats |

An arm that goes wrong can be told to free a seat it never gave, or to
seat a student in a room it has filled; the differential skips both, so
that a wrong arm fails properties instead of stopping the run.

It prints `1600 rooms and 1600 rooms of 10^9 seats, 26050 seat calls,
38400 checks over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the gap before the first student worth half its width | P1 467, P2 31, P4 61 |
| M2 | ★: a tie going to the later seat | P1 1063, P2 91, P6 1308 |
| M3 | ★: the gap after the last student worth half its width | P1 609, P2 345, P4 159 |
| M4 | list: a middle gap's half taken from one seat less | P1 1267, P2 796, P6 1424 |
| M5 | list: a middle seat counted from the right | P1 1063, P2 75, P6 1487 |
| M6 | list: the last gap measured from the first student | P1 1318, P2 1318, P6 1487 |
| M7 | heap: a stale gap taken | P1 935, P2 931, P3 1203, P4 7 |
| M8 | heap: the gap before the first student worth one seat less | P1 419, P2 29 |
| M9 | heap: a middle gap's seat counted from its right end | P1 1063, P2 75, P6 1487 |
| M10 | intervals: the gap a student sits in left in the set | P1 1465, P2 1465, P6 1546 |
| M11 | intervals: a leave keeping the gap on its right | P1 249, P2 183, P4 50 |
| M12 | intervals: the first gap's seat taken next to its student | P1 1524, P2 294, P4 6, P5 1524, P6 1600 |

P1 kills all twelve. M5 and M9 are one mistake in two arms, a middle
seat counted from the right end of its gap, and fail the same cases. P3
sees only M7, the heap arm taking a stale gap. P5 sees only M12, which
seats the first student at the far end. P2 counts both a seat already
taken and a room an arm has filled early: the leaves name the
statement's seats, so an arm that gave other seats is skipped on some of
them and can run out of room before the statement does.

## Verification

Every arm prints the same output as `exam_room.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `8439d277a6`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 0.4 to 0.8 s
and the differential 13.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends refuse every arm and the differential: a loop
over `calls.iter()` binds `ref i64`, which v2's `*c` reads, and legacy
types the binding as `i64` and refuses the `*` ("a 'i64' is copied, so
drop the `*`"); the ★ arm's walk of its sorted set and the ordered-gaps
arm's `*self.gaps.min().unwrap()` meet the same refusal. Legacy also
stops at the bench program's `windows` ("not yet supported in codegen").
Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the sorted-vector arm, the one whose data
structure is the same in all five languages: C has no ordered set, and a
sorted array with a binary search is a few lines in any of them. Each of
300 rounds is a room of 10^9 seats and 4,000 random calls, drawn as in
the harness. Every implementation prints `300 rooms of 4000 calls: seats
sum to 388677380086695, checksum 389099515`, the Kāra program under
`karac __mir-run` included, in 546 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.56 to 0.68 s |
| Rust (`rustc -O`) | 0.64 to 0.79 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.60 to 0.78 s |
| Go | 0.81 to 0.97 s |
| Python | 34.3 to 36.0 s |
| Kāra (`karac build --mir`) | 1.01 to 1.20 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

Nearly all the time is the walk of the taken seats on every seat call.
At the medians of the interleaved runs v2 takes 1.18 s, against Rust's
0.65 (0.63 under overflow checks), C's 0.60 and Go's 0.88: 1.87 times
Rust's time under overflow checks, 1.97 times C's and 1.34 times Go's.
Under valgrind's cachegrind Rust runs 9.74 billion instructions and 0.72
billion branches, with 7.0 million mispredicted; v2 runs 12.88 billion,
2.42 billion and 13.5 million, and C 8.41 billion, 0.44 billion and 9.3
million. v2 takes three times Rust's branches; most likely its
`windows(2)`, which the library gives as a `Vec` of slices, is built on
each call and its slices bounds-checked, where Rust's is a lazy iterator
(not traced). Built for `x86-64-v3`, the target `karac build` uses, C
takes 0.50 to 0.64 s and Rust with overflow checks 0.65 to 0.80 s,
against v2's 1.05 to 1.32 s in the same five interleaved runs. Python
takes 35 s, about 58 times C's time. The comparison with C and Rust
waits until after M4.
