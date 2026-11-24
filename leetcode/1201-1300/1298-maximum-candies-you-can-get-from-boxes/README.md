# 1298. Maximum Candies You Can Get from Boxes

You have `n` boxes labeled from `0` to `n - 1`. You are given four arrays:
`status`, `candies`, `keys`, and `containedBoxes` where:

- `status[i]` is `1` if the `i`th box is open and `0` if the `i`th box is
  closed,
- `candies[i]` is the number of candies in the `i`th box,
- `keys[i]` is a list of the labels of the boxes you can open after
  opening the `i`th box,
- `containedBoxes[i]` is a list of the boxes you found inside the `i`th
  box.

You are given an integer array `initialBoxes` that contains the labels of
the boxes you initially have. You can take all the candies in **any open
box** and you can use the keys in it to open new boxes and you also can
use the boxes you find in it.

Return the maximum number of candies you can get following the rules
above.

```
status = [1,0,1,0], candies = [7,5,4,100], keys = [[],[],[1],[]],
containedBoxes = [[1,2],[3],[],[]], initialBoxes = [0]                  ->  16
status = [1,0,0,0,0,0], candies = [1,1,1,1,1,1], keys = [[1,2,3,4,5],[],[],[],[],[]],
containedBoxes = [[1,2,3,4,5],[],[],[],[],[]], initialBoxes = [0]       ->  6
```

**Constraints:** `1 <= n <= 1000`, `status[i]` is `0` or `1`,
`1 <= candies[i] <= 1000`, the values of each `keys[i]` and each
`containedBoxes[i]` are distinct labels below `n`, each box is contained
in one box at most, and `initialBoxes` holds labels below `n`.

The arms are `fn max_candies(status: Vec[i64], candies: Vec[i64], keys:
Vec[Vec[i64]], contained_boxes: Vec[Vec[i64]], initial_boxes: Vec[i64]) ->
i64`.

## Approaches

Opening a box only ever adds keys and boxes, never takes one away, so
every order of opening that goes on while it can reaches the same boxes;
every arm opens what it can and stops.

| file | mechanism |
|---|---|
| `max_candies.kara` ★ | a breadth-first walk in a `VecDeque`: a box goes in the queue once, at the moment it is both held and open, whichever of the two came last, when it is found inside another box or when its key is found. O(n + keys + boxes inside) |
| `max_candies_sweep.kara` | every box looked at in turn, again and again, each held, open box not yet opened opened on the spot, until a whole sweep opens nothing. O(n (n + keys + boxes inside)) |
| `max_candies_dfs.kara` | depth first: opening a box is a recursive call that returns at once unless the box is held, open and not yet opened; a box opened tries again each box its keys fit and each box found inside it. O(n + keys + boxes inside) |
| `max_candies_waiting.kara` | a waiting room: the keys found in a `Set`, the boxes held but still locked in another `Set`, and the boxes ready to open on a `Vec` used as a stack; a key found frees its box from the waiting room. O(n + keys + boxes inside) |
| `max_candies_solution.kara` | a Rust solution as LeetCode's Rust users write it (the held boxes in a `VecDeque<usize>`, a locked one sent to the back, the walk given up once a whole round of the queue finds every box locked, and the keys written into `status` itself, taken as `mut status`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, nothing held
at the start, a key found before its box, and a box whose key is inside it
(`16 6 0 111 1`); then 3002 random cases, 3000 of 1 to 60 boxes with every
mix of open boxes, boxes held at the start, nesting and up to 5 keys a
box, and two of 1000 boxes, the constraints' largest (`3002 random cases:
candies total 11850388, checksum 156316829`). `max_candies.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms checked clean as first written. The
Rust arm takes one round of 37 fixes by `karac fix`'s count, from 20
errors: the `use std::collections::VecDeque;` line deleted, since
`VecDeque` is in Kāra's prelude, `struct Solution;` to `struct Solution
{}`, the parameter `mut status: Vec<i32>` to `status: own Vec[i32]` with
`let mut status = status;` as the body's first line, `Vec<..>` and
`VecDeque<..>` to `Vec[..]` and `VecDeque[..]`, `|&b|` to `|b|`, `for &k
in &keys[b]` to `for k in ref keys[b]`, `let mut ans = 0` to `let mut
ans: i32 = 0`, `::` to `.`, and in the wrapper the closure `|v:
&Vec<i64>| -> Vec<i32> { .. }` to `let narrow: Fn(ref Vec[i64]) ->
Vec[i32] = |v: ref Vec[i64]| { .. }`, its calls' `&` dropped, and the
`as i64` dropped as a widening. Its output matches on the first run. The
bench's `let c = cases[t];` moved a `Case` out of the vector, and
`E_INDEX_MOVE_NON_COPY` said to borrow it, which `karac fix` did (1 fix):
`let c = ref cases[t];`. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every held, open box not yet emptied is tried as the next one
to empty, in every order, and the answer is the most candies of any
order. What is held and what is open follow from which boxes have been
emptied, so the best from each set of emptied boxes is remembered as a
bit mask. 2000 cases of 1 to 9 boxes in four kinds, 500 each: any mix;
deep nesting with few boxes open, so that most boxes wait on a key found
elsewhere; every box held at the start and most of them locked, so that
the keys decide; and up to n keys a box. Past the first kind the first
box held at the start is open, so that the walk gets going. Every case
and renumbering is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | every box renumbered: the same answer |
| P3 | every list of keys, of boxes inside and of boxes held at the start read back to front: the same answer |
| P4 | every box open: no fewer candies |
| P5 | the boxes held at the start put inside one more open box of 1 candy, held alone: one more |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 891736417,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Twelve edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out: the ★ arm
queueing a box again each time its key turns up never stops on a box that
holds its own key, and times out rather than failing, and the waiting
arm forgetting a key found before its box fails exactly as the same arm
making a box found inside wait with its key in hand does. The ten kept,
two to each arm, are each killed, fail the same way under both backends
and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a held box whose key turns up later never opened | P1 550, P3 26, P6 2200 |
| M2 | ★: a locked box held at the start opened anyway | P1 717, P5 717, P6 2868 |
| M3 | sweep: one sweep only | P1 603, P2 536, P5 1624, P6 603 |
| M4 | sweep: a box found locked dropped | P1 104, P2 18, P5 486, P6 104 |
| M5 | depth first: a box opened when its key is found, held or not | P1 387, P6 387 |
| M6 | depth first: a box found inside opened only when its key turns up | P1 412, P3 88, P4 2, P5 1624, P6 412 |
| M7 | waiting: a key found before its box forgotten | P1 217, P3 49, P6 217 |
| M8 | waiting: a locked box held at the start forgotten | P1 488, P5 488, P6 488 |
| M9 | solution: the walk given up one box early | P1 250, P3 706, P6 250 |
| M10 | solution: a key opening the box it came from | P1 681, P6 681 |

P1 and P6 kill all ten, P5 five, P3 four, P2 two and P4 one. Wrapping
the boxes held at the start in one more box (P5) turns them into boxes
found inside, so it sees every edit that treats the two differently (M2,
M8) or that mishandles a box found inside (M4, M6), and the one sweep of
M3, which reaches the new box, numbered last, and nothing past it. Only
the sweep arm depends on how the boxes are numbered, so only its edits
fail P2. Reading the lists back to front (P3) changes which comes first,
a box or its key, and so catches the edits that go wrong only in one of
those orders (M1, M6, M7) and the Rust arm giving up one box early (M9),
whose queue order the lists decide. Every box open (P4) makes the keys
irrelevant, and only M6, which opens a box found inside only through its
key, comes out ahead of it, twice.

## Benchmarks

The bench builds 100 cases of 1000 boxes, the constraints' largest, with
from 10 to 49 boxes in 100 open, 5 to 24 in 100 held at the start, 60 to
99 in 100 nested, and up to 1 to 4 keys a box, once from its own
generator; then makes 5000 passes, each flipping one box of every case
between open and locked, chosen from the checksum so far, so no answer
carries over, answering it with the ★ arm and folding the candies plus
the pass into the checksum. The queue is the language's own: `VecDeque`
in Kāra and Rust and `collections.deque` in Python; Go reads a slice from
a moving head, and C an array of n, since each box is queued at most
once. Every implementation prints `5000 passes over 100 cases of 1000
boxes: checksum 106713413`.

BENCHTAB
