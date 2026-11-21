# 2402. Meeting Rooms III

You are given an integer `n`. There are `n` rooms numbered from `0` to
`n - 1`.

You are given a 2D integer array `meetings` where `meetings[i] =
[start_i, end_i]` means that a meeting will be held during the
**half-closed** time interval `[start_i, end_i)`. All the values of
`start_i` are **unique**.

Meetings are allocated to rooms in the following manner:

1. Each meeting will take place in the unused room with the **lowest**
   number.
2. If there are no available rooms, the meeting will be delayed until a
   room becomes free. The delayed meeting should have the **same**
   duration as the original meeting.
3. When a room becomes unused, meetings that have an earlier original
   **start** time should be given the room.

Return *the **number** of the room that held the most meetings. If
there are multiple rooms, return the room with the **lowest** number.*

```
n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]          ->  0
n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]   ->  1
```

**Constraints:** `1 <= n <= 100`; `1 <= meetings.length <= 10^5`;
`meetings[i].length == 2`; `0 <= start_i < end_i <= 5 * 10^5`; all the
values of `start_i` are unique.

Taken in order of start, each meeting either finds a room free by its
start, and takes the lowest, or waits for the room that frees first,
the lowest of those that free together. A delay can push an end far
past `5 * 10^5`, so ends are kept in 64 bits.

## Approaches

| file | mechanism |
|---|---|
| `rooms.kara` ★ | two heaps: a `PriorityQueue` of free rooms and one of (end, room) for the rooms in use; the rooms that have ended by a meeting's start are freed before it is placed. O(m log m + m log n) |
| `rooms_scan.kara` | each room's free time in a `Vec`, one scan of the rooms per meeting for the lowest free room or else the earliest to free. O(m log m + m n) |
| `rooms_sorted.kara` | two `SortedSet`s, of free rooms and of (end, room), read from their smallest by `min` and `pop_first`. O(m log m + m log n) |
| `rooms_mask.kara` | the free rooms as bits in words of 60, the lowest by `trailing_zeros`; the rooms in use a `PriorityQueue` of (end, room). O(m log m + m log n) |
| `rooms_iter.kara` | iterators: the sorted meetings folded by `fold` over the free times and counts, a room by `position` or else `min_by_key`, the answer by `max_by_key`. O(m log m + m n) |
| `rooms_solution.kara` | LeetCode's Rust template: two `BinaryHeap`s of `Reverse`, rooms as `usize`, `while let Some(&Reverse((t, r))) = busy.peek()`, over `meetings` sorted in place; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one room;
ten meetings at once in three rooms; 100 rooms and `10^5` meetings
starting below `5 * 10^5`, short and then long; 7 rooms and `2 * 10^4`
meetings up to `10^5` long; then 2000 random cases of 1 to 6 rooms and
up to 40 meetings, with a checksum and the total. `rooms.py` mirrors the
★ arm and its output is byte-identical, and the mirror was checked on
5000 random cases of up to 5 rooms and 15 meetings against time run one
unit at a time.

`rooms_mask.kara` was first written with `!` for a bitwise complement,
and `rooms_iter.kara` with `let (mut free_at, mut count) = state`;
`karac fix` wrote `~` in the first, in 1 edit, and moved the `mut`s
before the pattern in the second, in 3.

`check` first reports 9 errors on the template, and `karac fix` carries
it in one call, reporting 42 edits: `use
std::cmp::Reverse;` written `import std.cmp.Reverse;` and the
`BinaryHeap` import deleted; `struct Solution;` given its braces; `mut
meetings` made `meetings: own ..` with a `let mut` rebinding;
`sort_unstable` written `sort`; `BinaryHeap<Reverse<..>>` made
`PriorityQueue[Reverse[..]]`, largest first, so that `Reverse` still
pops the smallest, and `BinaryHeap::new()` `PriorityQueue.max_first()`;
each `Reverse(x)` written `Reverse { value: x }`, in patterns too;
`Some(&Reverse(..)) = busy.peek()` written with `.cloned()`; `usize`
made `i64`; and `vec![0; n as usize]` written `Vec.filled(..)`. The heap
collected from a range, `(0..n as usize).map(Reverse).collect()`, is
written `PriorityQueue.max_first_from((0..n as i64).map(..).collect())`. At
first that call came out opened inside the range's parentheses,
`(PriorityQueue.max_first_from(0..n as i64).map(..).collect())`, which
does not type-check (B-2026-11-21-40, fixed); the template was carried
again after the fix. `while let`, `if let`, `let Reverse { .. } = ..` and `ans as i32`
stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: time run one unit at a time, each room busy until its
meeting's end, and at each unit the rooms that have come free given,
lowest first, to the waiting meetings, earliest original start first.
No heaps. It checks 300 cases of 1 to 5 rooms and 1 to 12 meetings
starting below 40, which the literal reading answers; then 30 of up to
100 rooms and up to 3000 meetings; then 30 of up to 10 rooms and up to
3000 meetings up to 5000 long. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | up to 12 meetings: the answer is the literal reading's |
| P2 | every time moved 7 later: the same answer |
| P3 | the meetings listed in reverse: the same answer |
| P4 | every time doubled: the same answer |
| P5 | every meeting cut to one unit long: room 0 |
| P6 | each arm agrees with at least three of the other five |

P2 and P4 hold because the rules compare times only with each other,
which moving or stretching every time alike keeps, P3 because the rules
read the meetings by start, not by place in the list, and P5 because
meetings of one unit with distinct starts never overlap, so room 0 is
free for each.

The differential prints `360 cases: checksum 690938915, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs time a unit at a time. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a delay adding the whole end | P1 4, P2 10, P6 26 |
| M4 | ★: the highest free room taken | P1 218, P5 297, P6 269 |
| M5 | ★: a tie going to the higher room | P1 36, P6 41 |
| M8 | scan: the later of equal ends waited for | P1 4, P6 12 |
| M9 | scan: a delayed meeting never counted | P1 6, P6 29 |
| M11 | scan: room 1 never the answer | P1 10, P6 29 |
| M12 | sorted: a delay forgotten | P1 3, P6 24 |
| M13 | sorted: a room ending at the start still busy | P1 14, P6 27 |
| M15 | sorted: the least booked room | P1 227, P5 297, P6 284 |
| M18 | mask: a taken room never marked | P1 10, P6 47 |
| M19 | mask: one room freed per meeting | P1 25, P6 48 |
| M20 | mask: each delayed meeting a unit longer | P1 1, P4 14, P6 18 |
| M22 | iter: each delayed meeting a unit shorter | P1 2, P4 15, P6 15 |
| M25 | iter: a delayed end its length alone | P1 5, P2 4, P6 28 |
| M26 | iter: each meeting a unit shorter | P1 5, P4 15, P6 15 |
| M30 | solution: the meetings in the order given | P1 114, P3 140, P5 177, P6 164 |
| M31 | solution: each meeting a unit longer | P1 17, P4 15, P6 47 |

P1 and P6 kill all seventeen, P4 four, P5 three, P2 two and P3 one. P3,
the meetings listed in reverse, fails only the template's meetings in
the order given (M30): every other arm sorts a copy of its own. P2,
every time moved 7 later, fails the two edits that mix a time with a
length, the ★ arm's delay adding the whole end (M3) and the iter arm's
delayed end its length alone (M25). P4, every time doubled, fails the
four edits that add or take a fixed unit (M20, M22, M26, M31), and P5,
every meeting one unit long, the three that can then name a room other
than 0 (M4, M15, M30).

Of the thirty-one, fourteen were not kept. The ★ arm's room ending at
the start still busy and each meeting held a unit longer, the scan
arm's room free at the start passed over and the template's room ending
at the start still busy (M1, M6, M7, M27) fail as the sorted arm's room
ending at the start still busy (M13); the scan arm's last free room
taken, the sorted arm's highest free room taken and the mask arm's
highest free room in a word (M10, M14, M17) as the ★ arm's highest free
room taken (M4); the iter arm's highest of equal ends waited for (M23)
as the scan arm's later of equal ends waited for (M8); the iter arm's
and the template's tie going to the higher room (M24, M29) as the ★
arm's (M5); and the template's delay adding the whole end (M28) as the
★ arm's (M3). The ★ and sorted arms' freed room never returned (M2,
M16) stop on an `unwrap()` of `None` under both backends. The mask
arm's last room never the answer (M21) fails apart from every kept one,
and was left out to keep three to an arm. The scan arm's M9 was first a
delayed meeting not delayed, which failed as the sorted arm's delay
forgotten (M12), and the iter arm's M22 was first a room free at the
start passed over, which failed as M13; they were replaced by a delayed
meeting never counted (M9) and each delayed meeting a unit shorter
(M22).

## Verification

Every arm prints the same output as `rooms.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 4.4 to 11.5 s, except the iter
arm at 21.7 s. The differential takes 45 s there, 5.9 s under `karac
__mir-llvm-asan` and 1.1 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 cases of `10^5` meetings with distinct starts below
`5 * 10^5`, case `i` lasting up to `1 + 500 i`, once from the harness's
generator, then makes 10 passes, answering every case with 100 rooms
and folding each answer plus the pass into the checksum, with the ★ arm
in all five languages. Every implementation prints `10 passes over 10
cases of 10^5 meetings in 100 rooms: checksum 462512969`. Each copies
and sorts the meetings in every call: Kāra with its `sort`, Rust with
`sort`, Python with `sorted`, Go with `sort.Slice` and C with `qsort`,
whose comparison is a call through a pointer. Kāra keeps the heaps in
`PriorityQueue`s, Rust in `BinaryHeap`s of `Reverse`, Python in `heapq`
lists, Go in `container/heap` and C in two arrays of its own heap.

BENCHTAB
