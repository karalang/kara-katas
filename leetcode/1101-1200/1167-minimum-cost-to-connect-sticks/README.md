# 1167. Minimum Cost to Connect Sticks

You have some number of sticks with positive integer lengths. These
lengths are given as an array `sticks`, where `sticks[i]` is the length of
the `i`th stick.

You can connect any two sticks of lengths `x` and `y` into one stick by
paying a cost of `x + y`. You must connect all the sticks until there is
only one stick remaining.

Return the minimum cost of connecting all the given sticks into one stick
in this way.

```
sticks = [2,4,3]    ->  14
sticks = [1,8,3,5]  ->  30
sticks = [5]        ->  0
```

**Constraints:** `1 <= sticks.length <= 10^4`; `1 <= sticks[i] <= 10^4`.

The arms are `fn connect_sticks(sticks: Vec[i64]) -> i64`, the ★ arm's
parameter `own`, since its queue takes the sticks.

## Approaches

Joining the two shortest sticks first is always cheapest (Huffman's
argument: the two shortest can be the deepest pair of some best tree); the
arms differ in how the two shortest are found.

| file | mechanism |
|---|---|
| `connect_sticks.kara` ★ | a heap: the sticks in a `PriorityQueue`, smallest first, built in O(n); the two shortest popped, joined at their sum's cost, and the joined stick pushed back. O(n log n) |
| `connect_sticks_queues.kara` | two queues: the sticks sorted, and the joined sticks in a second `Vec` read from a moving head; joined sticks come out no shorter than the ones before them, so the shortest stick is at the head of one queue or the other. O(n log n) for the sort, then O(n) |
| `connect_sticks_counts.kara` | a count of each length in a `SortedMap`: the two shortest taken from its first entry or entries with `pop_first`, the rest of a count put back, and the joined length counted in. O(n log n) |
| `connect_sticks_insert.kara` | a sorted list: the sticks sorted longest first, the two shortest popped from the end, and the joined stick inserted back at the place `partition_point` finds. O(n^2) for the moves |
| `connect_sticks_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `Vec<i32>`, a `BinaryHeap::new()` given every stick as `Reverse(s)`, two pops matched as `Reverse(a)`, an `i32` sum), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's examples (14, 30, 0); two
sticks (`[1,1]`: 2); four equal (`[3,3,3,3]`: 24); the powers of two after
an extra 1, each joined stick the next one's equal (`[1,1,2,4,...,64]`:
254); one stick far longer than the rest (`[10000,1,2,3]`: 10015). Then
300 random piles of 1 to 50 sticks, half of length 1 to 10 so that lengths
tie (`300 random piles: total 85131614, checksum 529531809`), and two piles
of 10^4 sticks, the constraints' most: random (607910780) and all of the
longest (1336160000). `connect_sticks.py` mirrors the ★ arm and its output
is byte-identical; with `lit` it reads the statement literally for the
piles of up to 8 sticks, trying every way of joining, and gives the same
output.

The Mend loop: the ★ arm takes one fix, `sticks: own Vec[i64]`, since
`PriorityQueue.from` takes its vector; the queues arm takes `let (mut i,
mut j)` to `let mut (i, j)`; the counts and insert arms take none. Where
an arm only borrows the sticks, its harness's `.clone()` of them is
dropped as a copy no one needs. The Rust arm takes four rounds (9, 6, 2 and
2 edits): the `use` lines deleted, the generics to brackets, `::` to `.`
and `|&s|` to `|s|`; then `struct Solution {}`, `BinaryHeap.new()` to
`PriorityQueue.new()`, and every `Reverse` dropped, since Kāra's queue
pops the smallest first already; then `ans` annotated `i32` and the
adapter's `as i64` dropped; then the harness's two `.clone()`s. Its output
matches on the first run.

Writing the Rust arm found two gaps. Its first form built the heap the
other common way, `let mut heap: BinaryHeap<Reverse<i32>> =
sticks.into_iter().map(Reverse).collect();`, and `karac fix` renamed the
type to `PriorityQueue[Reverse[i32]]` but, with no constructor to rewrite,
kept the `Reverse`: Kāra's queue then pops the smallest `Reverse`, the
longest stick, and the mended program, once its last error was finished
by hand, answers 16 for `[2,4,3]`. That is kara B-2026-11-15-86, fixed
at `ed156ca6d4`: the collected heap now goes to
`PriorityQueue.max_first_from(..)` and `.map(Reverse)` gets a fix, so
that form mends to 14 too. The arm keeps the constructor form. On the
way, `let Reverse { value: a } = heap.pop().unwrap();` read `a` as moved
after one use, because the binding took the field's declared type, the
parameter `T`.
That is kara B-2026-11-15-79, which kata 2208 found the same day, fixed
at `ee3c8ec9c4`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to join two of the sticks, then two of what is left,
and so on, tried, and the cheapest kept. It checks 1200 piles in four
kinds of 300: 1 to 6 sticks of 1 to 5, so that lengths tie; 1 to 6 of 1
to 10^4; 7 to 100 of 1 to 10; and 7 to 200 of 1 to 10^4. Every random
choice the properties make is drawn before any arm answers: a factor of
2 to 5, an order of the sticks, and a way of joining them.

| | property |
|---|---|
| P1 | the cost is the literal one, for the piles of up to 6 sticks |
| P2 | every stick k times as long costs k times as much |
| P3 | the sticks in another order cost the same |
| P4 | a stick longer than all the others together is joined last, to the whole of them: the cost grows by their total and its length |
| P5 | beside sticks of 2 or more, two sticks of 1 are joined first, into a stick of 2: the cost is 2 more than with that stick of 2 instead |
| P6 | no way of joining costs less: a drawn way of joining costs at least the answer |

All 33,000 checks pass on every arm: `1200 piles: checksum 262623595,
33000 checks over 5 arms: 0 failures`, in 20 s under `karac __mir-run`.
A Python reading of the same draws, with the mirror against the literal
reading, gives the same checksum.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Fourteen are caught and one is
equivalent: the queues arm taking a tie from the joined queue rather than
the sorted one (Q1), since equal lengths cost the same whichever is taken.

| # | mutation | failures by property |
|---|---|---|
| H1 | ★: the longest two joined first | P1 393, P4 1094, P5 1200, P6 949 |
| H2 | ★: a joined stick never put back | P1 395, P4 1094, P5 1198 |
| H3 | ★: a join costing the longer stick only | P1 494, P4 1200, P5 1200 |
| Q2 | queues: the sticks left unsorted | P1 297, P3 863, P5 989, P6 87 |
| Q3 | queues: one join short | P1 494, P4 1200 |
| C1 | counts: the rest of a count put back one longer | P1 199, P2 667, P4 667, P5 1200, P6 448 |
| C2 | counts: a joined stick counted twice | P1 341, P4 1094, P5 1186 |
| C3 | counts: two sticks fewer a join | P1 395, P4 1094, P5 627 |
| I1 | insert: the sticks sorted shortest first | P1 316, P4 1094, P5 627, P6 83 |
| I2 | insert: the joined stick's place searched the wrong way | P1 277, P4 894, P5 1091, P6 722 |
| I3 | insert: the joined stick put first, as the longest | P1 151, P4 995, P5 955, P6 11 |
| X1 | solution: a joined stick one longer | P1 395, P2 995, P4 1094, P5 1200, P6 127 |
| X2 | solution: a join costing the shorter stick only | P1 494, P4 1200, P5 1200 |
| X3 | solution: the last join left out | P1 494, P4 1200 |

P1 catches all fourteen, P4 thirteen, P5 twelve, P6 seven, P2 two and P3
one. P2 sees only the edits that add a fixed length (C1, X1), which does
not scale with the sticks; P3 sees only the unsorted queue (Q2), the one
edit whose answer depends on the order the sticks come in. P6 sees the
edits that join the wrong pair, which a drawn way of joining can beat,
but not those that miscount a right join. Two edits first written for C1
and X3 stopped the run before any property answered, and were replaced:
the rest of a count put back over another count lost sticks and emptied
the map, and a heap pushed the sticks by reference, `for s in
sticks.iter().skip(1)`, which `karac check` refuses but the corpus
backend, which skips that check, stopped on at build.

## Benchmarks

`bench/` times the ★ arm against a binary min-heap in C (a textbook
array heap: built in O(n), each pop a swap down the tree), Rust
(`BinaryHeap` of `Reverse`, from the vector), Go (`container/heap`) and
Python (`heapq`). 16 piles of 10^4 sticks of 1 to 10^4, the constraints'
most, are built once; each of 40 rounds gives one stick of every pile a
new length and joins a copy of the pile. Every program prints `40 rounds
over 16 piles of 10^4 sticks: total 390065148970, checksum 443672652`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `1bdebaaa70`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.394 to 0.487 s | 0.430 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.400 to 0.496 s | 0.440 s |
| Rust (`rustc -O`) | 0.447 to 0.478 s | 0.454 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.432 to 0.466 s | 0.454 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.441 to 0.556 s | 0.456 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.754 to 0.892 s | 0.778 s |
| C (`clang -O3`) | 0.751 to 0.856 s | 0.791 s |
| Go | 1.902 to 2.326 s | 2.115 s |
| Python | 3.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, so the
two Kāra rows are one program timed twice. Kāra takes about 0.97x
overflow-checked Rust's time, the equal-safety comparison. C takes about
1.8x Kāra's: its heap swaps an element down level by level, comparing it
with both children each time, where Rust's `BinaryHeap` and Kāra's
`PriorityQueue` pop by Floyd's method: down to a leaf along the better
child, one comparison a level, then the element carried there back up.
That compares about half as often (read from the two libraries' sources;
the gap is not profiled). Go's `container/heap` calls `Less` and `Swap`
through an interface and takes about 4.8x Kāra's time; Python's `heapq`,
written in C, about 7x.
