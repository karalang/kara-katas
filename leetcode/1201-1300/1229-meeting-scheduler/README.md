# 1229. Meeting Scheduler

Given the availability time slots arrays `slots1` and `slots2` of two
people and a meeting duration `duration`, return the **earliest time
slot** that works for both of them and is of duration `duration`.

If there is no common time slot that satisfies the requirements, return
an **empty array**.

The format of a time slot is an array of two elements `[start, end]`
representing an inclusive time range from `start` to `end`.

It is guaranteed that no two availability slots of the same person
intersect with each other. That is, for any two time slots `[start1,
end1]` and `[start2, end2]` of the same person, either `start1 > end2`
or `start2 > end1`.

```
slots1 = [[10,50],[60,120],[140,210]], slots2 = [[0,15],[60,70]], duration = 8   ->  [60,68]
slots1 = [[10,50],[60,120],[140,210]], slots2 = [[0,15],[60,70]], duration = 12  ->  []
```

**Constraints:** `1 <= slots1.length, slots2.length <= 10^4`;
`slots1[i].length, slots2[i].length == 2`; `slots1[i][0] < slots1[i][1]`;
`slots2[i][0] < slots2[i][1]`; `0 <= slots1[i][j], slots2[i][j] <=
10^9`; `1 <= duration <= 10^6`.

The arms are `fn min_available_duration(slots1: Vec[Vec[i64]], slots2:
Vec[Vec[i64]], duration: i64) -> Vec[i64]`. The two Rust arms keep the
method LeetCode gives Rust users, on `i32`, inside `impl Solution`, and a
short `min_available_duration` converts to and from it.

## Approaches

| file | mechanism |
|---|---|
| `meeting_scheduler.kara` ★ | two pointers over both people's slots sorted by start: the overlap of the two current slots runs from the later start to the earlier end, and when it holds the meeting, the meeting starts at the later start; otherwise the slot that ends first can overlap nothing later, and its pointer moves on. O(n log n + m log m) |
| `meeting_scheduler_heap.kara` | every slot long enough for the meeting in one `PriorityQueue`, earliest start first. A person's own slots never overlap, so two slots popped in turn that overlap are one of each, and the meeting fits when the earlier reaches the later's start plus the duration; when it does not, the later reaches further, and only it is kept. O((n + m) log(n + m)) |
| `meeting_scheduler_merged.kara` | both people's slots in one sorted list of `(start, end, owner)` tuples; walking it, each person's furthest reach so far, and at each slot the other person's reach is the only slot of theirs that can still overlap it from the left |
| `meeting_scheduler_pointers.kara` | a Rust solution as LeetCode's Rust users write it (both lists sorted in place through `mut` parameters by `sort_unstable_by_key(\|s\| s[0])`, then two pointers, `let (mut i, mut j) = (0, 0)`), carried to Kāra by `karac fix` |
| `meeting_scheduler_binheap.kara` | another Rust solution (a `BinaryHeap` of `Reverse((start, end))`: pop a slot, peek the next, and the meeting fits when the popped slot reaches the peeked start plus the duration), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 8 lines: LeetCode's two examples, a meeting
that exactly fills a shared slot (`[5, 9]`), two slots that only touch
(`[]`), a checksum of the answers for 1000 random pairs of schedules of
1 to 30 slots (`60797099`, 117 with no time), and three meetings over
two schedules of `10^4` slots each, up to about `10^9`.
`meeting_scheduler.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★ and merged arms check clean as written. The heap
arm was first written with Rust's `let Some(mut prev) = queue.pop()
else`, and the fix makes it `let mut Some(prev) = ..`. The pointers arm
takes one round of 20 fixes (among them `mut slots1: Vec<Vec<i32>>` to
`slots1: own Vec[Vec[i32]]` with a `let mut slots1 = slots1;` in the
body, `sort_unstable_by_key` to `sort_by_key`, `let (mut i, mut j)` to
`let mut (i, j)`, and `vec![]` to `Vec.new()`) and the binheap arm one
round of 18 (among them `BinaryHeap::new()` of `Reverse` items to a
smallest-first `PriorityQueue.new()` of the bare tuples, and the
`Reverse((..))` patterns to the tuples), and both check clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every slot of the one person against every slot of the other,
the earliest start at which both are free for the duration. 2000 cases:
a third with up to 5 slots each of up to 10, a third with up to 50 of up
to 40, and a third with up to 150 of up to 400, the gaps between a
person's slots as wide; 840 have no time.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | `duration` long and within a slot of each person, or empty |
| P3 | the two people swapped give the same answer |
| P4 | every time shifted by up to 999 gives the answer shifted |
| P5 | a meeting one shorter fits, no later |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 112150720,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python's answers for
the same cases give the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a meeting that exactly fills the overlap refused | P1 149, P6 596 |
| S2 | ★: the slot that ends later moved on | P1 735, P6 2940 |
| H1 | heap: the first slot compared with every later one | P1 647, P5 13, P6 647 |
| H2 | heap: slots too short for the meeting kept | P1 499, P2 499, P6 499 |
| M1 | merged: a slot measured against its own person's reach | P1 1160, P6 1160 |
| M2 | merged: the slot's own end ignored | P1 499, P2 499, P6 499 |
| P1 | pointers: the overlap to the later end | P1 1336, P2 1336, P3 20, P6 1336 |
| P2 | pointers: the first person's last slot never compared | P1 62, P3 99, P6 62 |
| B1 | binheap: the last two slots never compared | P1 30, P6 30 |
| B2 | binheap: any overlap taken for the meeting | P1 729, P2 729, P6 729 |

All ten are caught, and P1 catches every one. A mutation of the ★ arm
fails P6 on the four other arms. Four return a meeting that does not fit,
which P2 catches on every case it breaks: H2 keeps slots too short for
the meeting, M2 ignores where a slot ends, the pointers arm's P1 runs the
overlap to the later end, and B2 takes any overlap at all. The others
miss the earliest meeting and return a later one or none, which only the
statement read literally and the ★ arm see: S1 refuses a meeting that
exactly fills an overlap (on the 149 cases where the earliest does), S2
and M1 move on from the wrong slot, and B1 and the pointers arm's P2
never compare the last slots. P3, the two people swapped, catches the
pointers arm's two, whose first person is treated apart from the second.
P5 catches H1, which compares every slot with the first, on 13 cases: a
meeting one shorter keeps an early slot that the longer one leaves out
as too short, that slot becomes the first, and the shorter meeting is
found later or not at all. Shifting every
time (P4) catches none, as none of the mutations depends on where the
day starts.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, sort and two pointers, over 50 random pairs of schedules of 10^4
slots each, drawn once, each solved for 10 durations; checksum of the
answers. Every program prints `50 pairs of 10^4 slots, 10 durations:
checksum 30183666`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.097 to 1.400 s | 1.163 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.064 to 1.580 s | 1.129 s |
| Rust (`rustc -O`) | 1.013 to 1.221 s | 1.071 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.945 to 1.226 s | 1.066 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.975 to 1.097 s | 1.041 s |
| C (`clang -O3`) | 1.609 to 1.821 s | 1.676 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.620 to 1.882 s | 1.673 s |
| Go | 1.939 to 2.155 s | 2.048 s |
| Python | 7.591 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 6% ahead of Kāra (1.066 s
against 1.129 s), and the two ranges overlap. Kāra is about 33% ahead of
C (1.129 s against 1.676 s); Go takes about 1.8x Kāra's time. Python
takes about 7x Kāra's time. No profile was taken.
