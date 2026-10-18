# 752. Open the Lock

A lock has four wheels, each showing a digit from 0 to 9, and starts at
`0000`. One turn moves one wheel one step up or down, and 9 and 0 are
next to each other. The lock jams at any setting in `deadends`. Return
the fewest turns that reach `target` without passing through a dead end,
or -1 if there is no way.

```
deadends = ["0201", "0101", "0102", "1212", "2002"]
target = "0202"                                     ->   6
deadends = ["8888"], target = "0009"                ->   1
deadends = ["8887", "8889", "8878", "8898",
            "8788", "8988", "7888", "9888"]
target = "8888"                                     ->  -1
```

**Constraints:** 1 to 500 dead ends; every setting is four digits; the
target is not a dead end.

## Approaches

The settings and turns form a graph of 10,000 nodes with eight edges
each, so the answer is a shortest path; the arms differ in the search
and in how they hold the settings.

| file | mechanism |
|---|---|
| `open_lock.kara` ★ | breadth-first search over the settings as numbers 0 to 9999, with a `Vec[bool]` of dead ends, a `Vec` of turns so far and a `VecDeque`; O(10^4 x 8) |
| `open_lock_strings.kara` | the textbook search: settings stay strings, dead ends and settings reached are `Set[String]`s, and the search goes a level at a time |
| `open_lock_bidir.kara` | breadth-first from both ends at once, always growing the smaller frontier, until the frontiers meet; frontiers are `Set[i64]`s |
| `open_lock_astar.kara` | A* from a `PriorityQueue`, estimating the turns left as the sum of each wheel's circular distance to the target digit |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: the three LeetCode examples; a dead
0000; no dead ends with target 0000 and with 5555; the neighbours of
0000 dead but one, and all of them dead; and 40 random locks of up to
478 dead ends, with how many cannot be opened, the total turns of the
rest and a checksum. `open_lock.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which grows the set of settings reached a turn at a time, as strings,
until the target is in it or the set stops growing. 400 random locks are
checked. Each target has every wheel at 9, 0 or 1, and each of the other
80 such settings is a dead end with one chance from 0 to 70 in
100 picked per lock (0000 with 5 in 100), so that dead ends crowd the
way to the target; up to 10 more dead ends fall anywhere. 20 of the
locks cannot be opened and the rest take 1,139 turns in all.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | every wheel negated, in the target and the dead ends, gives the same answer: turning up becomes turning down |
| P3 | the wheels read in reverse order, in the target and the dead ends, give the same answer |
| P4 | when the lock opens, one more dead end farther from 0000 than the answer, even with no dead ends at all, leaves the answer as it was |

It prints `400 locks (20 cannot open, the rest 1139 turns in all),
4 arms, 6320 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a dead 0000 not noticed | P1 18 |
| M2 | ★: a wheel turned down by two, not one | P1 295, P2 301 |
| M3 | ★: dead ends walked through | P1 50 |
| M4 | strings: a digit wrapped at 9, not 10 | P1 304, P2 140 |
| M5 | strings: the wheels only turned up | P1 304, P2 325 |
| M6 | strings: the target not seen at the start | P1 3 |
| M7 | bidir: a wheel turned down wrapping at 9 | P1 256, P2 273 |
| M8 | bidir: a meeting after one turn missed | P1 42 |
| M9 | bidir: no answer of 0 for the target 0000 | P1 3 |
| M10 | astar: a wheel's estimate not taken the short way round | P1 39, P2 52, P3 8 |
| M11 | astar: aims at the setting with the first wheel dropped | P1 264, P3 241 |
| M12 | astar: ordered by the estimate alone | P1 1, P2 3, P3 2 |
| E1 | ★: one more unused slot | 0 |
| E2 | bidir: the larger frontier grown | 0 |
| E3 | astar: stale entries not skipped | 0 |

P1 kills all twelve. P2 sees the edits that treat a turn up and a turn
down differently, M2, M4, M5, M7 and M10, and also M12; P3 sees the
edits that treat one wheel differently from another, M10 and M11, and
also M12. P4 kills none: it is there for an arm that lets a dead end off
every shortest way change the answer, and none of these edits does that.
M1, M3, M6, M8 and M9 are seen by the definition alone, since they get
one kind of lock wrong in a way that negating or reversing the wheels
does not change. E1 keeps one more slot that nothing uses; E2 grows the
larger frontier, which only costs time; E3 stops skipping stale queue
entries, which A* then expands again to no effect. An earlier M11 let A*
ignore a shorter way to a setting it had already found, and it survived
because the edit changes nothing: the estimate changes by at most one
per turn and every turn flips the parity of the digit sum, so a second
way to a setting could only be two turns shorter if it left the queue at
the same total with fewer turns, and the queue orders by turns after the
total, which puts it first. It was replaced by an A* that aims at the
target with its first wheel dropped.

## Verification

Every arm prints the same output as `open_lock.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1a5c083e3a`, whose last compiler change is `4655692faa`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★ and A* arms and the bench
program: both arms print the same output under the legacy interpreter,
`karac run`, `karac build` and an auto-par build. They refuse the
strings and two-ended arms and the differential at type checking, at a
`*` over a set's `iter()` (`*s`, `*x`), since legacy gives those by
value where v2 gives references. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws
500 random dead ends, then for each of 3,000 locks replaces 5 of them at
random and opens the lock at a random target, counting the locks that
cannot be opened and adding up the turns of the rest. Every
implementation prints `3000 locks with 500 dead ends: 162 cannot open,
the rest take 27854 turns in all`, the Kāra program under `karac
__mir-run` included (in 129 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.38 to 0.44 s |
| Rust (`rustc -O`) | 0.31 to 0.43 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.53 s |
| Go | 0.84 to 0.94 s |
| Python | 15.4 to 15.9 s |
| Kāra (`karac build --mir`) | 1.49 to 1.59 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
5.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 1.54 s,
against C's 0.42, Rust's 0.31 (0.52 under overflow checks) and Go's
0.87, and the legacy build of the same program 0.58 to 0.69 s, a median
of 0.60 s: v2 is about 2.6 times legacy, over M2's limit of twice
legacy. Under valgrind's cachegrind v2 runs 19.7 billion instructions
against C's 3.1 billion and Rust's 3.2 billion, and callgrind puts most
of the difference in the allocator: the ★ arm turns each wheel with `for
step in [1, 9]`, and under `karac build --mir` that literal is a new
heap `Vec` each time, some 58 million of them, where legacy keeps it on
the stack. Written `Array[1, 9]` the same program runs 0.80 to 0.85 s on
v2, about 1.3 times legacy. The kata keeps the natural spelling and the
gap is filed as B-2026-10-18-52 (below); new katas' benches are outside
M2's frozen set in any case. The comparison with C and Rust waits until
after M4.

## Compiler findings

B-2026-10-18-52 (kara ledger, open): a bare list literal that is only
walked or read, such as `for step in [1, 9]`, heap-allocates a `Vec`
every time it is evaluated under `karac build --mir`,
1,000,008 allocations for a million evaluations against legacy's 9. It
makes this bench 2.5 to 2.6 times legacy. design.md makes `[a, b]` a
`Vec`, so the allocation is what the literal means and keeping it on the
stack is an optimisation, which legacy already does
(B-2026-10-02-70). Nothing in the kata works around it; once the row is
fixed the bench should run near the `Array` spelling's 0.8 s (inferred,
not measured).
