# 1172. Dinner Plate Stacks

You have an infinite number of stacks arranged in a row and numbered (left
to right) from `0`, each of the stacks has the same maximum capacity.

Implement the `DinnerPlates` class:

- `DinnerPlates(int capacity)` Initializes the object with the maximum
  capacity of the stacks `capacity`.
- `void push(int val)` Pushes the given integer `val` into the leftmost
  stack with a size less than `capacity`.
- `int pop()` Returns the value at the top of the rightmost non-empty
  stack and removes it from that stack, and returns `-1` if all the stacks
  are empty.
- `int popAtStack(int index)` Returns the value at the top of the stack
  with the given index `index` and removes it from that stack or returns
  `-1` if the stack with that given index is empty.

```
["DinnerPlates","push","push","push","push","push","popAtStack","push","push","popAtStack","popAtStack","pop","pop","pop","pop","pop"]
[[2],[1],[2],[3],[4],[5],[0],[20],[21],[0],[2],[],[],[],[],[]]
->  [null,null,null,null,null,null,2,null,null,20,21,5,4,3,1,-1]
```

**Constraints:** `1 <= capacity <= 2 * 10^4`; `1 <= val <= 2 * 10^4`;
`0 <= index <= 10^5`; at most `2 * 10^5` calls will be made to `push`,
`pop`, and `popAtStack`.

The Kāra arms are `struct DinnerPlates` with `new(capacity: i64)`,
`push(mut ref self, val: i64)`, `pop(mut ref self) -> i64` and
`pop_at_stack(mut ref self, index: i64) -> i64`. The two Rust arms keep
the signatures LeetCode gives Rust users, `i32` throughout.

## Approaches

Every arm keeps the stacks in a vector; they differ in how a push finds
the leftmost stack with room and how `pop` finds the rightmost plate.

| file | mechanism |
|---|---|
| `dinner_plates.kara` ★ | a `PriorityQueue` of the indices that may have room, smallest first: `popAtStack` adds its index, and a push drops the indices on top whose stack is full or gone, then takes the top. Empty stacks at the right end are dropped as they empty, so `pop` is `popAtStack` on the last stack. O(log n) a call, amortized |
| `dinner_plates_sorted.kara` | the indices of the stacks with room in a `SortedSet`, kept exact, so a push takes its smallest; empty stacks at the right end dropped as they empty. O(log n) a call |
| `dinner_plates_cursor.kara` | the index `left`, below which every stack is full: a push walks it right past the full stacks, a `popAtStack` below it moves it back. O(1) a call but for the walk, which can cover every stack |
| `dinner_plates_tree.kara` | a segment tree over the stacks' sizes, each node the smallest and largest size under it: a push walks down to the leftmost stack below capacity, `pop` to the rightmost above 0, and the leaves double when every one is full. Empty stacks stay. O(log n) a call, amortized |
| `dinner_plates_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Vec<Vec<i32>>` and a `BinaryHeap<Reverse<usize>>` of the stacks with room, read through `while let Some(&Reverse(i)) = self.available.peek()`, stale indices popped off its top), carried to Kāra by `karac fix` |
| `dinner_plates_btree.kara` | another Rust solution (`Vec<Vec<i32>>` and a `BTreeSet<usize>` of the stacks with room, its first element taken with `iter().next()`, empty stacks at the right end dropped in `pop_at_stack`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five properties |

Every arm prints the same 10 lines: LeetCode's example; pops with
nothing to pop; a stack past the last; capacity 1; holes refilled before
a new stack opens; the left stacks emptied first; 300 random streams of
1 to 60 calls at capacity 1 to 4 (`300 random streams: 4540 pops,
checksum 947906389`); and streams of 200000 calls, the constraints' most,
at capacity 7 and 20000, and of 50000 at capacity 1, every index up to
100000 (`200000 calls, capacity 7: 80185 pops, 33321 empty, checksum
643796424`). The capacity-1 stream is cut to 50000 calls for the cursor
arm, whose walk at capacity 1 covers every stack: at 200000 calls it
took 2.5 minutes under `karac run`, about 0.4 µs a step of the walk.
`dinner_plates.py` mirrors the ★ arm with `heapq` and its output is
byte-identical; with `lit` it reads the statement literally, a push
scanning from the left for the first stack below capacity and `pop` from
the right for the first plate, no stack ever dropped, and gives the same
output. Every arm gives the same output under `karac run` and `karac
build`.

The Mend loop: the four Kāra arms take no fixes. The Rust arms take one
round each, 34 edits and 29: the generics to brackets, `::` to `.`,
`&mut self` to `mut ref self`, `&&`, `||` and `!` to `and`, `or` and
`not`, `vec![..]` to `[..]`, `usize` to `i64` (and `as usize` to `as
i64`), the `use` lines dropped, `BinaryHeap<Reverse<usize>>` to
`PriorityQueue[i64]` with `Reverse(..)` taken off every push and
`Some(&Reverse(i)) = self.available.peek()` to `Some(i) =
self.available.peek().cloned()`, `BTreeSet<usize>` to `SortedSet[i64]`,
`Some(&i) = self.open.iter().next()` to `Some(i) =
self.open.iter().next().cloned()`, and `remove(&i)` to `remove(i)`. In
the harness, `out.push(d.pop() as i64)` to `out.push(d.pop())`, since
`i32` widens to `i64`. Both arms' outputs match on the first run.

One compiler gap came up on the way, fixed in kara `3091098c58`:

- `karac fix` carried the `BinaryHeap<Reverse<usize>>` arm to a heap
  that popped the LARGEST index, a silent wrong answer (kara B-2026-11-16-185). It
  took two rounds. The first did not see `Some(&Reverse(i))` as a read of
  the heap's `Reverse` values, so it kept `Reverse` and wrote `import
  std.cmp.Reverse;`; the second, seeing `Reverse` now as Kāra's own,
  read the heap as smallest-first and wrote `PriorityQueue.new()`, a
  smallest-first queue of `Reverse` values, which pops the largest. A
  reduction printed 3 where Rust prints 2. `Some(&Reverse(..))` is now
  read as the heap's own pattern, so the arm takes the one round above;
  and a heap whose `Reverse` is imported from `std.cmp` is now carried
  to `PriorityQueue.max_first()`, so that a later round can no longer
  turn it around.

The differential takes one round of 4 edits, the same `as i64` casts in
its copies of the two Rust arms' calls.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally (a push scanning from the left, `pop` from the right, no stack
dropped). It runs 600 streams in four kinds of 150: 1 to 20 calls at
capacity 1 to 3 with indices below 6; 1 to 80 at capacity 1 to 5 below
20; 100 to 400 at capacity 1 to 50 below 100; and 1 to 100 at capacity 2
with half the calls `popAtStack` below 10, so that holes open and fill all
the time. Every random choice the properties make is drawn before any arm
answers.

| | property |
|---|---|
| P1 | every pop returns what the statement read literally returns |
| P2 | every value shifted shifts every plate popped |
| P3 | a capacity no stack can fill gives one stack: capacity `pushes + 1` and `2 * (pushes + 1) + 7` return the same |
| P4 | as many `pop` calls again as pushes, appended, return every plate pushed and then `-1` |
| P5 | a `popAtStack` past every stack, put in anywhere, returns `-1` and changes nothing else |

All 18,000 checks pass on every arm: `600 streams: checksum 125619428,
18000 checks over 6 arms: 0 failures`, in 7 s under `karac __mir-run`,
and the same under `karac __mir-llvm-run` and `karac build`.

## Mutation testing

Eighteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All eighteen are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: a popped stack's index not offered again, so holes are never refilled | P1 292 |
| A2 | ★: an index past the trimmed stacks kept | a crash: `index out of bounds` |
| A3 | ★: only one trailing empty stack trimmed | P1 8, P4 16 |
| S1 | sorted: a trimmed stack's index left in the set | a crash: `index out of bounds` |
| S2 | sorted: a full stack left open | P1 373 |
| S3 | sorted: the rightmost open stack filled | P1 187 |
| C1 | cursor: the cursor not moved back to a hole | P1 251 |
| C2 | cursor: only one trailing empty stack trimmed | P1 8, P4 16 |
| C3 | cursor: the cursor stops at a full stack | P1 389 |
| T1 | tree: pop takes the leftmost plate | P1 459, P4 513 |
| T2 | tree: a grown tree forgets the stacks' sizes | P1 371 |
| T3 | tree: never grows when every leaf is exactly full | P1 337 |
| X1 | solution: a popped stack's index not offered again | P1 318 |
| X2 | solution: pop takes from the first stack | P1 457, P4 508 |
| X3 | solution: a full stack counts as open | P1 228 |
| B1 | btree: the rightmost open stack filled | P1 187 |
| B2 | btree: a popped stack's index not offered again | P1 292 |
| B3 | btree: a capacity-1 stack left open after its one plate | P1 59 |

A2 and S1 are caught as crashes rather than by a property: an index past
the last stack reaches `stacks[i]`.

A first C2 removed the cursor arm's clamp of `left` to the number of
stacks after a trim, and nothing failed. The clamp was dead: every stack
below `left` is full, so never empty, and the trim, which drops only
empty stacks from the right, never passes `left`. The arm no longer has
it, and C2 now weakens the trim instead.

## Benchmarks

`bench/` times the ★ arm against the same lazy min-heap in C, Rust, Go
and Python. 60 streams of 200000 calls, the constraints' most, run at
capacity 1, 7, 100 and 20000 in turn, each on a new `DinnerPlates`: a
push with weight 6, a pop with weight 2 and a `popAtStack` with weight 2,
at an index below `20000 / capacity + 1`, about as many stacks as a
stream ever holds. Every pop's value is folded into a checksum. The heap
is Kāra's `PriorityQueue`, Rust's `BinaryHeap<Reverse<usize>>`, Go's
`container/heap` over an `[]int`, Python's `heapq`, and in C a binary
heap written out over a growable array. Every program prints `60 streams
of 200000 calls: 4801455 pops, 362606 empty, checksum 797723517`.

Timings on a 4-core container (Intel Xeon, 2.3 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac
`3091098c58` on LLVM 22. karac builds for the x86-64-v3 baseline, so the
C and overflow-checked Rust programs are also built at
`-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.202 to 0.242 s | 0.208 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.200 to 0.241 s | 0.210 s |
| Rust (`rustc -O`) | 0.199 to 0.248 s | 0.207 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.202 to 0.283 s | 0.217 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.201 to 0.253 s | 0.211 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.173 to 0.253 s | 0.185 s |
| C (`clang -O3`) | 0.171 to 0.228 s | 0.181 s |
| Go | 0.545 to 0.642 s | 0.595 s |
| Python | 8.7 to 8.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time equals wall time for both Kāra rows, so
both ran on one core. Kāra takes about 0.97x overflow-checked Rust's
time, the equal-safety comparison, a tie within the runs' spread, and
C takes about 0.86x Kāra's: all three keep the same vector of vectors and
the same binary heap of indices, and the work is the heap's sifting and
the vectors' growth, not arithmetic. Go takes about 2.8x Kāra's time:
`container/heap` calls `Less`, `Swap`, `Push` and `Pop` through an
interface, and each `heap.Push` boxes its index into an `any`. Python
takes about 42x, every call a method call on objects. These causes are
read from the programs, not profiled.
