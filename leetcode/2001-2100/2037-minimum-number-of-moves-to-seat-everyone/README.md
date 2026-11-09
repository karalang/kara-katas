# 2037. Minimum Number of Moves to Seat Everyone

There are `n` available seats and `n` students standing in a room. You are
given an array `seats` of length `n`, where `seats[i]` is the position of
the `i`-th seat, and an array `students` of length `n`, where `students[j]`
is the position of the `j`-th student. You may increase or decrease the
position of a student by 1 any number of times, each one move. Return the
minimum number of moves required to move each student to a seat such that
no two students are in the same seat. Several seats or students may start
at the same position.

```
seats = [3,1,5], students = [2,7,4]          ->  4
seats = [4,1,5,9], students = [1,3,2,6]      ->  7
seats = [2,2,6,6], students = [1,3,2,6]      ->  4
```

**Constraints:** `n == seats.length == students.length`; `1 <= n <= 100`;
`1 <= seats[i], students[j] <= 100`.

A student who walks to a seat makes as many moves as the distance, so the
answer is the cheapest matching of students to seats by total distance.
Pairing the `k`-th smallest seat with the `k`-th smallest student is
cheapest: two pairs that cross can always be uncrossed without making the
total longer. Counted another way, the sorted matching moves exactly
`|seats at or below p - students at or below p|` students across the gap
between places `p` and `p + 1`, and each crossing is one move.

## Approaches

| file | mechanism |
|---|---|
| `seats.kara` ★ | both lists taken `own`, sorted in place, and the distances of `zip`ped pairs summed. O(n log n) |
| `seats_crossings.kara` | the students crossing each gap: seats counted up and students down into a fixed `[0; 102]` array, then a running balance over the places, its absolute value summed. O(n + 100) |
| `seats_heaps.kara` | two min-first `PriorityQueue`s popped in step by `while let (Some(seat), Some(student)) = (free.pop(), waiting.pop())`. O(n log n) |
| `seats_runs.kara` | each side counted into a `SortedMap` of place to how many, then the two lists of `(place, count)` runs walked together, the front runs pairing off as many as the smaller count. O(n log n) |
| `seats_insertion.kara` | each side built sorted by `insert` at its `partition_point`, then the moves folded over the paired indices. O(n^2), which `n <= 100` allows |
| `seats_solution.kara` | LeetCode's Rust template (`impl Solution`, `mut` parameters of `Vec<i32>`, `sort_unstable`, `iter().zip(..).map(..).sum()`), carried by `karac fix` in two rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: the answers for LeetCode's three
examples and four more, then the sum and a checksum of the answers for 2000
rooms of 1 to 100 seats at places up to 1 to 100. `seats.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to give each student a free seat, by recursion over a
bit mask of the seats taken, and the fewest moves. It checks 1500 rooms of
1 to 6 seats at places up to 1 to 60, each with a shift and a place to add.
Every random choice of a problem (the places, a shuffle of each list, the
shift, the added place) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | either list shuffled leaves the answer |
| P3 | the seats and the students swapped leave the answer |
| P4 | every place moved by the same amount (0 to 39) leaves the answer |
| P5 | a seat and a student added at the same place leave the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 rooms: checksum 521673991, 54000 checks over
6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. All thirty are killed, each
fails the same way under both backends, none by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the students never sorted | P1 849, P2 807, P3 800, P5 200, P6 849 |
| M2 | ★: the distances signed (`a - b` for `(a - b).abs()`) | P1 1012, P3 1418, P6 1012 |
| M3 | ★: the first pair skipped | P1 1411, P3 1178, P5 1269, P6 1411 |
| M4 | crossings: the students counted as seats | P1 1500, P4 1460, P5 1500, P6 1500 |
| M5 | crossings: the balance never carried (`=` for `+=`) | P1 1378, P6 1378 |
| M6 | crossings: the gaps above 50 left out | P1 120, P4 588, P6 120 |
| M7 | heaps: one seat taken by every student (`peek` for `pop`) | P1 1172, P3 1175, P5 1477, P6 1172 |
| M8 | heaps: each move capped at one place | P1 1344, P5 216, P6 1344 |
| M9 | heaps: each distance halved | P1 1444, P5 66, P6 1444 |
| M10 | runs: a run pairing the larger count | P1 429, P5 467, P6 429 |
| M11 | runs: a run's count never multiplied in | P1 54, P5 1, P6 54 |
| M12 | runs: every count one too many | P1 1421, P5 351, P6 1421 |
| M13 | insertion: each place inserted at the front | P1 838, P2 989, P6 838 |
| M14 | insertion: each distance one place off | P1 1337, P3 1306, P5 1500, P6 1337 |
| M15 | insertion: the fold seeded at one | P1 1500, P6 1500 |
| M16 | solution: each distance one too long | P1 1500, P5 1500, P6 1500 |
| M17 | solution: the adapter dropping the first student | P1 1346, P2 771, P3 1040, P5 1192, P6 1346 |

P1 and P6 kill all seventeen, P5 twelve, P3 six, P2 three and P4 two. P2
sees only the edits that read the lists in the order given: the students
never sorted (M1), each place inserted at the front, which builds the list
reversed (M13), and the adapter's first student dropped (M17). P4 sees the
edits tied to where the places are rather than how far apart: the
crossings arm's gaps cut off at 50 (M6), and its students counted as seats,
whose balance then grows with the places themselves (M4). P3 sees the edits
that treat the two sides differently, a signed distance (M2) or one side
left unsorted or cut (M1, M3, M17), and those whose error depends on the
pairing order rather than the distances (M7, M14). P5 misses the edits
that an extra pair at no distance cannot change: a signed distance (M2)
gains 0 from it, the front insertion (M13) puts the two side by side at
the front and pairs them, a balance never carried (M5) or a constant added
to the answer (M15) stays as wrong, and an answer read from beyond place 50
(M6) is unchanged by a pair below it.

The other thirteen fail as a kept one does, or with a signature of their
own that adds nothing. The students paired in reverse fail alike in the ★,
heaps (the waiting popped from the largest), runs (the students' runs
walked from the largest) and Rust arms, and so does the Rust arm's seats
sorted from the largest. The ★ arm's distances squared fail exactly as the
heaps arm's moves capped at one place: both are wrong only where a distance
is 2 or more. Four edits fail exactly where the answer is not 0 (P1 1444):
the crossings arm counting each crossing twice, and the heaps, runs and
insertion arms each building both sides from one list, which answers 0. The
Rust arm's students never sorted fails as M1. The crossings arm's balance
taken signed and the insertion arm's last pair left out fail with counts of
their own. One first draft survived and was replaced: the insertion arm's
`partition_point(|q| q >= p)` builds each list in descending order, and
pairing two descending lists is the same matching.

## Verification

Every arm prints the same output as `seats.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.8 s (crossings) to 3.4 s (heaps)
and the differential 4.1 s, on kara 991c45adcd.

The five Kāra arms met no compiler gap. `karac fix` moved the runs arm's
`let (mut i, mut j)` to `let mut (i, j)`. The harness first printed
`f"{seats} {students} -> {min_moves_to_seat(seats, students)}"`, which
reads both lists and gives them to the call in one string. It is refused:
the string's reading borrows `seats` while the call moves it (core
semantics §5.6), as Rust's `format!` refuses the same line. The harness
now builds the room's text first, and the fix for the moves from a `for`
element (`.into_iter()`) came from `karac fix`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds (seven edits, then three) to a clean check. Rust's `mut
seats: Vec<i32>` parameter becomes `seats: own Vec[i32]` with `let mut
seats = seats;` at the body's start, `sort_unstable` becomes `sort` (a
stable sort is also an unstable one), and the adapter's `as i64` on an
`i32` answer is dropped, since an `i32` widens to `i64` where one is
wanted.

## Benchmarks

The bench builds 2000 rooms of 100 seats and 100 students once in all five
languages, and runs the ★ arm for 25 rounds, one seat of every room moved
before each call, which answers on copies: 50000 calls. Every
implementation prints `50000 calls: sum 21787683, checksum 510827097`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.097 to 0.134 s | 0.099 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.097 to 0.113 s | 0.101 s |
| Rust (`rustc -O`) | 0.133 to 0.156 s | 0.135 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.143 to 0.185 s | 0.159 s |
| C (`clang -O3`) | 0.343 to 0.400 s | 0.350 s |
| Go | 0.389 to 0.446 s | 0.400 s |
| Python | 1.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.096 s) is not above its real time (0.099 s).

The sequential Kāra program is 0.63x Rust under overflow checks and 0.29x
C.
