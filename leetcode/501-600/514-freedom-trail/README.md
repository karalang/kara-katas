# 514. Freedom Trail

In the video game Fallout 4, the quest "Road to Freedom" requires
players to reach a metal dial called the "Freedom Trail Ring" and use
the dial to spell a specific keyword to open the door.

Given a string `ring` that represents the code engraved on the outer
ring and another string `key` that represents the keyword that needs
to be spelled, return the minimum number of steps to spell all the
characters in the keyword.

Initially, the first character of the ring is aligned at the "12:00"
direction. You should spell all the characters in `key` one by one by
rotating `ring` clockwise or anticlockwise to make each character of
the string `key` aligned at the "12:00" direction and then by pressing
the center button.

At the stage of rotating the ring to spell the key character
`key[i]`:

1. You can rotate the ring clockwise or anticlockwise by one place,
   which counts as one step. The final purpose of the rotation is to
   align one of `ring`'s characters at the "12:00" direction, where
   this character must equal `key[i]`.
2. If the character `key[i]` has been aligned at the "12:00"
   direction, press the center button to spell, which also counts as
   one step. After the pressing, you could begin to spell the next
   character in the key (next stage). Otherwise, you have finished all
   the spelling.

```
ring = "godding", key = "gd"       ->  4
ring = "godding", key = "godding"  ->  13
```

In the first example, "g" is already at 12:00, so pressing it is one
step; turning the ring anticlockwise by two places brings "d" to 12:00
in two steps, and pressing it is one more.

**Constraints:** `1 <= ring.length, key.length <= 100`; `ring` and
`key` consist of only lowercase English letters; it is guaranteed that
`key` can always be spelled by rotating `ring`.

## Approaches

Every arm is `fn find_rotate_steps(ring: Str, key: Str) -> i64` and
reads both strings through `.bytes()`, a `Slice[u8]`.

| file | mechanism |
|---|---|
| `find_rotate_steps.kara` ★ | bottom-up over the key: for each letter, the fewest turns ending at each position holding it, from the previous letter's positions and costs, taking the shorter way round, `d.min(n - d)`. The positions of each letter are listed once in a `Vec[Vec[i64]]`. The presses are added at the end. O(m k^2), k the most positions a letter has |
| `find_rotate_steps_memo.kara` | top-down: the fewest turns to spell `key[i..]` from position p, trying every position holding `key[i]`, kept in a table of `-1` for not yet known that goes down the recursion as `mut ref Vec[Vec[i64]]`. O(m n^2) |
| `find_rotate_steps_dijkstra.kara` | shortest path over the states (letters spelled, position): a smallest-first `PriorityQueue[(i64, i64, i64)]` of (steps, i, p), edges to every position holding the next letter, each costing its turns and the press; the first state out with the whole key spelled gives the answer |
| `find_rotate_steps_nearest.kara` | only the nearest `key[i]` clockwise and the nearest anticlockwise need trying, since passing a copy of the letter to reach a farther one the same way never pays; the fewest steps from each (i, p) kept in a `Map[(i64, i64), i64]`. O(m n) states, O(n) to find the two |
| `differential.kara` | the four arms on 1,000 random rings and keys, five properties |

Every arm prints the same 7 lines: the two LeetCode examples, four
more cases, and for 300 random rings and keys of 1 to 60 letters the
total and a checksum. `find_rotate_steps.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,000 random rings of 1 to 24 letters from the first 2, 5 or 26 in
turn, each with a key of 1 to 12 letters drawn from the ring.

| | property |
|---|---|
| P1 | the answer is the reference's: the distance between every two positions found by walking the ring a step at a time, then a table over every position, not only those holding the letter, filled from the end of the key back |
| P2 | the ring read the other way round from the same 12:00 letter needs as many steps |
| P3 | renaming the letters, a for z, b for y and so on, in ring and key changes nothing |
| P4 | one more key letter, drawn from the ring, costs at least 1 more and at most 1 + n / 2 more |
| P5 | pressing the key's last letter again costs exactly 1 more |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the ring turned only the way the indexes run, `d` for `d.min(n - d)` | P1 459, P2 709, P4 41 |
| M2 | ★: the presses left out | P1 1000, P4 361, P5 1000 |
| M3 | memo: the next letter looked for from the old position, not the one just reached | P1 700, P5 617 |
| M4 | memo: the way back round one step short, `n - d - 1` | P1 636, P2 703 |
| M5 | dijkstra: always the long way round, `n - d` | P1 952, P2 763, P4 350, P5 1000 |
| M6 | dijkstra: any position counts as the letter | P1 872 |
| M7 | nearest: the anticlockwise search walks clockwise | P1 592, P2 692, P4 41 |
| M8 | nearest: the worse of the two ways kept, `.max` | P1 822, P4 263 |
| E1 | memo: not yet known written `-7`, not `-1` | 0 |
| E2 | dijkstra: states already finished pushed again | 0 |
| E3 | ★: the running best starts at 10^9, not `i64.MAX` | 0 |
| E4 | dijkstra: a finished state taken off the queue is expanded again | 0 |

E1 holds because the table is read with `>= 0` and every real count is
at least 0. E2 and E4 only add work: a state already finished comes
back out of the queue at a cost no lower than the first time, so the
first full spelling out of the queue is still the cheapest. E3 holds
because no answer comes near 10^9.

P3, the renaming, kills nothing: no arm reads a letter as anything but
a label to compare, and none of the edits change that. It stays as a
check that none ever does. M6 is seen only by the reference: with any
position counting as the letter, the dial never turns and the answer
is the key's length, which every other property allows. M3 measures
every turn from the start, which reads the same either way round the
ring, so P2 misses it; P5 sees it, since pressing the last letter
again is then charged the turn from the start to it. M1, M4 and M7
each get the anticlockwise distance wrong, and P2 sees them, since
reading the ring the other way round swaps the two directions.

Two first tries at the memo mutants never finished. Keeping the
distance signed (`(p - q)` for `(p - q).abs()`) lets a negative count
into the table, which `>= 0` then reads as unknown, and `> 0` for
`>= 0` reads every count of 0 as unknown. Either makes the recursion
exponential, and both runs passed the runner's ten-minute limit. They
are left out of the table.

## Verification

Every arm prints the same output as `find_rotate_steps.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

The frozen legacy backends run only the memo arm, under `karac run
--interp`, where it prints the same output. Its type checker types
the items of a `Vec`'s and a `Map`'s `iter()` and of a `for` over
`.bytes()` by value, so it refuses the `*q`, `*c`, `*v` and `*b` reads
in the ★ and nearest arms, the differential and the bench program.
Its codegen has no `.bytes()` on a `Str` ("no handler for method
'bytes'"), so LLJIT and `karac build` refuse the memo and Dijkstra
arms. The Dijkstra arm prints the six fixed cases under `karac run
--interp` and does not finish the 300 random ones inside five minutes.

## Benchmarks

The bench program uses the ★ arm. It builds 400 random rings of 300
letters from all 26, each with a key of 2,000 letters drawn from the
ring, and solves each once. Every implementation prints `400 rings of
300 letters, keys of 2000: 7385290 steps in all, checksum 426531922`,
the Kāra program under `karac __mir-run` included (in 135 s).

Every mirror copies the letter's positions and builds a fresh cost
list for every key letter, as the ★ arm does with `.clone()` and
`Vec.new()`: Rust `Vec`s, Go slices, Python lists, and C arrays it
grows by doubling with `realloc`. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.49 to 0.54 s |
| Rust (`rustc -O`) | 0.40 to 0.43 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.46 to 0.64 s |
| Go | 0.79 to 0.82 s |
| Python | 29.1 to 29.3 s |
| Kāra (`karac build --mir`) | 0.27 to 0.29 s |

The legacy `karac build` refuses this program (its type checker reads
`*q` and `*c` as derefs of an `i64`, see Verification). So `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend. That edit is by hand, on top of the `scripts/new-bench.sh`
output. The `--mir` row is timed at kara `e85c10e377`. Under `karac
__mir-llvm-run` the program prints the same line in 2.2 s, compile
included; that JITs the MIR's IR without optimization passes, so it
is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
