# 735. Asteroid Collision

An array `asteroids` gives a row of asteroids. For each, the absolute
value is its size and the sign its direction, positive moving right and
negative moving left, all at the same speed. When two meet, the smaller
explodes, and both explode if they are the same size; two moving the
same way never meet. Return the asteroids left after every collision, in
their order.

```
asteroids = [5, 10, -5]      ->  [5, 10]
asteroids = [8, -8]          ->  []
asteroids = [10, 2, -5]      ->  [10]
```

**Constraints:** 2 <= `asteroids.length` <= 10^4; -1000 <=
`asteroids[i]` <= 1000; `asteroids[i]` != 0.

## Approaches

Only a left-mover with a right-mover somewhere to its left can collide,
and the order collisions happen in does not change who is left, so every
arm may settle them in whatever order suits it.

| file | mechanism |
|---|---|
| `asteroid_collision.kara` ★ | a stack of the survivors so far: each left-mover destroys the smaller right-movers on top, then is destroyed by a larger one, dies with one of its own size, or goes onto the stack; O(n) time |
| `asteroid_collision_simulate.kara` | one collision at a time: find the first right-mover followed directly by a left-mover, settle that one collision with `Vec.remove`, and start again until there is none; O(n^2) time |
| `asteroid_collision_inplace.kara` | the ★ arm's stack kept in the front of a copy of the row, with a count of the survivors, the row cut to that count at the end; O(n) time, no second list |
| `asteroid_collision_fromright.kara` | the mirror walk from the end, where a right-mover destroys the smaller left-movers on the stack, then the stack reversed; O(n) time |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: the three LeetCode examples;
left-movers already left of right-movers, which never meet; a
right-mover destroyed by the first of three larger left-movers; a
left-mover that destroys three right-movers and never meets the one
after it; a row where pairs of the same size go together and only the
first left-mover survives; three pairs of the same sizes nested inside
each other, which leave nothing; 10,000 random asteroids, the problem's
longest row, of sizes up to 1,000; 9,999 right-movers and one left-mover
larger than all of them; 5,000 pairs of the same size side by side;
5,000 right-movers met by their mirror image, which destroy each other
from the middle out; and 300 random rows of 2 to 13 asteroids of sizes
up to 5. The long rows and the random ones print how many asteroids are
left and a checksum. `asteroid_collision.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which moves the asteroids: the i-th starts at position 2i, and at each
step every asteroid moves one place its own way. The gap between a
right-mover and a left-mover after it starts even and closes by 2 a
step, so two asteroids meet only at the same place at the same time;
wherever two meet the smaller is removed, and both if they are the same
size, until no right-mover is left of a left-mover. 3,000 random rows
are checked, each of 2 to 10 asteroids of sizes 1 to 4 moving either
way, so that asteroids of the same size meet often; 10,558 asteroids are
left in all.

| | property |
|---|---|
| P1 | the survivors are the definition's |
| P2 | the row reversed, with every asteroid turned round, leaves the survivors reversed and turned round |
| P3 | the survivors are some of the asteroids in their order, and no right-mover among them is left of a left-mover |
| P4 | settling the two sides of a random cut first, and then the two sides' survivors together, leaves the same survivors |

It prints `3000 rows (10558 survivors), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: same sizes, only the left-mover exploding | P1 1093, P2 1235 |
| M2 | ★: a left-mover meeting left-movers too | P1 1475, P2 2417, P4 148 |
| M3 | ★: same sizes, only the right-mover exploding (the left-mover goes on) | P1 1100, P2 1235 |
| M4 | simulate: any asteroid after a right-mover meeting it | P1 1575, P2 2573, P4 106 |
| M5 | simulate: same sizes, only the left-mover exploding | P1 1093, P2 1235 |
| M6 | simulate: the last two never checked | P1 1061, P2 1562, P3 1061 |
| M7 | inplace: one asteroid past the survivors kept | P1 2363, P2 2342, P3 1797, P4 971 |
| M8 | inplace: the first survivor never hit | P1 1023, P2 1562, P3 1023 |
| M9 | inplace: a survivor left where it was, not put on the stack | P1 1918, P2 2313, P3 1284, P4 1351 |
| M10 | fromright: the stack never reversed | P1 2410, P3 2352, P4 2330 |
| M11 | fromright: same sizes, only the left-mover exploding (the right-mover goes on) | P1 1093, P2 1235 |
| M12 | fromright: same sizes, only the right-mover exploding | P1 1100, P2 1235 |
| E1 | ★: a nonempty stack as len() >= 1 | 0 |
| E2 | simulate: a pair of the same size removed at the same place twice | 0 |
| E3 | inplace: each asteroid read from the input, not the row | 0 |

P1 kills all twelve. M1, M5 and M11 are one mistake in three arms, a
pair of the same size where only the left-mover explodes, and fail the
same rows; M3 and M12 are the opposite mistake, only the right-mover
exploding, in two arms. P2 sees all of those, since turning the row
round swaps which of the two survives, and P3 and P4 see none of them:
the survivors are still some of the asteroids in their order with no
collision left, and the mistake is made the same way on each side of a
cut. P3 sees the edits that leave a collision to come or survivors out
of the row's order: M6 and M8 skip a meeting, M7 keeps an asteroid past
the survivors, M9 leaves a survivor where it was and M10 gives the
survivors last first. P2 misses only M10, whose reversal turning the row
round undoes. E1 writes a nonempty stack as `len() >= 1`; E2 removes a
pair of the same size at the same place twice, which removes the same
two; E3 reads each asteroid from the input rather than the row, which
the in-place stack never overwrites ahead of where it reads.

## Verification

Every arm prints the same output as `asteroid_collision.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`969445f00a`, whose last compiler change is `b830c8f243`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at a `*` over a vector's `iter()`
(`*a` over the asteroids in the ★ arm and over the survivors in the
harness), since legacy gives those by value where v2 gives references.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes 20 rows
of 10,000 random asteroids of sizes up to 1,000 once, the problem's
largest, and in each of 500 rounds turns one random asteroid of each row
round and collides the row, summing how many are left and a checksum of
them. The C program grows its stack with `realloc`, as the others grow a
vector, and frees it after each row. Every implementation prints
`500 rounds of 20 rows of 10000 asteroids: 2427285 left, checksum
252413425`, the Kāra program under `karac __mir-run` included (in
3.4 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.77 to 0.86 s |
| Rust (`rustc -O`) | 0.82 to 0.87 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.99 s |
| Go | 0.89 to 1.06 s |
| Python | 11.4 to 11.8 s |
| Kāra (`karac build --mir`) | 0.92 to 1.12 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.6 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is a fifth behind C and Rust at the medians of the
interleaved runs (1.00 s against 0.83 and 0.84), a fifth behind Rust
under overflow checks (0.82), and a thirteenth behind Go (0.93). Under
valgrind's cachegrind it runs 3.0 billion instructions against 2.2 for C
and for Rust, and 0.95 billion branches against 0.50 and 0.55; all three
mispredict 86 to 89 million of them, most likely the tests of each
asteroid's direction and size, which are random here. The legacy `karac
build` refuses the program (above), so there is no legacy time to
compare. Where the extra branches go was not traced. The comparison with
C and Rust waits until after M4.

## Compiler findings

None new.
