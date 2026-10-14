# 621. Task Scheduler

A CPU runs a list of tasks, each named by a capital letter, one in every
time slot, in any order. Two tasks with the same letter must be at least
`n` slots apart, and a slot may be left idle. Return the fewest slots
that run every task.

```
tasks = ["A","A","A","B","B","B"], n = 2  ->  8    A B _ A B _ A B
tasks = ["A","C","A","B","D","B"], n = 1  ->  6    A B C A D B
tasks = ["A","A","A","B","B","B"], n = 3  ->  10   A B _ _ A B _ _ A B
```

**Constraints:** 1 to 10,000 tasks; each a letter from A to Z; `n` from
0 to 100.

## Approaches

Every arm is `fn least_interval(tasks: Slice[char], n: i64) -> i64` and
starts by counting each letter's tasks.

| file | mechanism |
|---|---|
| `least_interval.kara` ★ | the letters that occur most, `most` times each, need `most - 1` gaps of `n` slots between their runs, so the answer is `(most - 1) * (n + 1)` plus one for each letter tied at `most`, or the number of tasks if that is larger; O(tasks) |
| `least_interval_heap.kara` | the schedule a slot at a time: a max-first `PriorityQueue` of the counts that may run now and a `VecDeque` of the letters cooling down, each slot running the letter with the most left and sending it to cool for `n` slots; O(answer * log 26) |
| `least_interval_rounds.kara` | rounds of `n + 1` slots, each running one task of each of the `n + 1` letters with the most left after sorting the counts again, padded with idle slots unless it is the last; O(answer / (n + 1) * 26 log 26) |
| `least_interval_idle.kara` | the most frequent letter laid out with `(most - 1) * n` idle slots between its runs, each other letter then filling as many as it has tasks but at most one in each gap, and whatever is left idle added to the number of tasks; O(tasks + 26 log 26) |
| `least_interval_scan.kara` | the schedule a slot at a time, each slot scanning all 26 letters for the one with the most left among those whose cooling is over; O(answer * 26) |
| `differential.kara` | the five arms against the definition, five properties |

Every arm prints the same 13 lines: the three LeetCode examples; seven
more (one task, no cooling, one letter only, every letter once with a
cooling of 100, ties at the most, other letters filling every gap
exactly, and two letters more than that); a total and checksum over
300 random lists of 1 to 60 tasks from the first 1 to 26 letters, drawn
evenly or skewed, with a cooling of 0 to 12; and the answers for
10,000 tasks with a cooling of 100, from all 26 letters skewed and from
three letters evenly. `least_interval.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the definition:
the fewest slots of any schedule, found by a breadth first search a slot
at a time over states that hold, for each letter, the tasks it has left
and the slots it must still wait, where each slot either runs a letter
that has tasks left and need not wait or is idle. Each of 1,000 random
cases is 1 to 10 tasks from the first 1 to 4 letters with a cooling of
0 to 3.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | the letters renamed and the list reversed give the same count |
| P3 | with no cooling, the count is the number of tasks |
| P4 | one more task makes it no shorter, and no more than `n + 1` slots longer |
| P5 | cooling one slot longer makes it no shorter, and fewer than the number of tasks longer |

It prints `1000 cases (8547 slots), 5 arms, 25000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Fifteen edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All ten that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one slot for the letters tied at the most | P1 42 |
| M2 | ★: the frame's rows `n` long, not `n + 1` | P1 493 |
| M3 | heap: a letter's last two tasks run as one | P1 828, P3 828 |
| M4 | heap: the letter with the fewest left run first | P1 346, P5 5 |
| M5 | rounds: the last round padded too | P1 687, P5 407 |
| M6 | rounds: a round padded only when a letter has two left | P1 493 |
| M7 | idle: a letter filling more than one slot in a gap | P1 42 |
| M8 | idle: the idle count allowed below zero | P1 7, P4 2, P5 2 |
| M9 | scan: the letter with the fewest left run first | P1 346, P5 5 |
| M10 | scan: a letter barred one slot too few | P1 493 |
| E1 | ★: the larger taken the other way round | 0 |
| E2 | heap: the test as `left >= 2` | 0 |
| E3 | rounds: the round's bound as `ran < n + 1` | 0 |
| E4 | idle: the loop run on past zero | 0 |
| E5 | scan: a tie going to the later letter | 0 |

Only the definition kills every mutant; the other properties are bounds
and invariances that a wrong count can still meet. P3 sees M3, which
drops a letter's last task, so even without cooling its count is short.
P5 sees M5 on 407 cases and M4, M8 and M9 on a few. M8 is the thinnest
kill, at 7 cases, and the only one P4 sees: its idle count goes below
zero only when one letter's share is larger than the idle slots still
left, which is rare with at most ten tasks. P2 kills nothing, since
every arm counts the letters first and so cannot see their names or
their order.

## Verification

Every arm prints the same output as `least_interval.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `4bf1e8e2f7` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They type
the items of a `Vec`'s `iter()` by value, so the `*t` that reads a task
and the `*c` that reads a count are errors, and they still hold the old
rule that an argument which is already a `mut ref`, as `seed` is inside
`random_tasks`, drops its call-site `mut` marker. Legacy is frozen, so
these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 100 lists of 10,000 tasks,
the problem's most, from the first 1 to 26 letters, evenly or skewed,
once; then 30,000 times answers one of them, picked by the round, with a
cooling of 0 to 100, adding up the answers and putting each into a
checksum. Every implementation prints `100 lists, 30000 rounds: total
3358321806, checksum 610868401`, the Kāra program under `karac
__mir-run` included (in 473 s).

Each implementation counts the letters into an array of 26 and computes
the frame as the ★ arm does: Rust over a `Vec<char>`, Go over a
`[]rune`, C over a `char` array, and Python over a list of one-character
strings. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.22 to 0.24 s |
| Rust (`rustc -O`) | 0.32 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.29 to 0.38 s |
| Go | 0.30 to 0.35 s |
| Python | 15.7 s |
| Kāra (`karac build --mir`) | 0.36 to 0.47 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses it for the
same reasons; that edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

The Kāra row is about 1.2 times Rust's and 1.8 times C's. It is not
profiled here.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
