# 528. Random Pick with Weight

You are given a 0-indexed array of positive integers `w` where `w[i]`
describes the weight of the `i`th index. Implement the function
`pickIndex()`, which randomly picks an index in the range `[0,
w.length - 1]` and returns it. The probability of picking an index `i`
is `w[i] / sum(w)`.

```
Solution([1])     pickIndex() -> 0
Solution([1, 3])  pickIndex() -> 1 with probability 3/4, 0 with 1/4
```

**Constraints:** `1 <= w.length <= 10^4`; `1 <= w[i] <= 10^5`;
`pickIndex` will be called at most `10^4` times.

## Approaches

Every arm is a `Solution` with `fn new(w: Vec[i64], seed: i64) ->
Solution` and `fn pick_index(mut ref self) -> i64`. Laid end to end,
index `i` owns the run `[p_i, p_i + w_i)` of `[0, total)`, `p_i` being
the sum of the weights before it. Every arm draws one point of `[0,
total)` from a seeded generator of its own (`Draw`, as in katas 497
and 519: 15 bits a step, two steps to a uniform draw below `n`, with
rejection so it is exactly uniform) and returns the index whose run
holds it. The arms differ only in how they find that run, so from the
same seed they all make the same picks.

| file | mechanism | finding the run |
|---|---|---|
| `random_pick_with_weight.kara` ★ | prefix sums, binary search for the first run that ends past the point | log n |
| `random_pick_with_weight_linear.kara` | walk the weights, taking each off the point until it falls inside one | n |
| `random_pick_with_weight_floor.kara` | a `SortedMap` from each run's start to its index; `floor` finds the run | log n |
| `random_pick_with_weight_fenwick.kara` | a Fenwick tree of the weights, descended from the highest power of two | log n |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 8 lines: the picks for five lists (the two
examples, a heavy last weight, a heavy first weight, six equal
weights), the counts of 100,000 picks from `[1, 2, 3, 4]` and whether
each is within 5 standard deviations of its share, then for 300 random
lists of 1 to 50 weights up to 100 whether 200 picks each are in range
and a checksum over them, and last the largest case: 10,000 weights
up to 100,000 and 10,000 picks (the problem's most calls), counted in
10 bands of indices and checked against the bands' shares.
`random_pick_with_weight.py` mirrors the ★ arm with the same
generator, makes the same picks, and its output is byte-identical.

## Differential

`differential.kara` holds the generator, copies of the four arms and
the definition: every index written out as many times as its weight,
and the drawn point read off that list. Each arm is held to the
properties below on 300 cases: a short list of 1 to 10 weights up to
20 for P1, a longer one of 1 to 30 weights up to 100 for P2 and P4,
and a single weight up to 100,000 for P3.

| | property |
|---|---|
| P1 | from the same seed, the 100 picks are the definition's |
| P2 | every one of 3,000 picks is an index of the list |
| P3 | a single weight is always picked |
| P4 | over those 3,000 picks every index gets its share, within 5 standard deviations |
| P5 | the same seed twice gives the same 50 picks |

It prints `300 cases, 4 arms, 6000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
picks, and four that do not, each run under `karac __mir-run`. All
eight that change picks are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run that ends exactly at the point taken (`>=`) | P1 269, P4 1 |
| M2 | ★: the point drawn below the first weight, not the total | P1 269, P4 289 |
| M3 | linear: a point at the end of a run counted in it (`<=`) | P1 269, P4 1 |
| M4 | linear: one taken off the point per weight passed, not the weight | P1 244, P4 278 |
| M5 | floor: each index keyed by the end of its run, not the start | P1 269, P4 289 |
| M6 | floor: `ceiling` for `floor` | P1 269, P4 289 |
| M7 | fenwick: a block that sums to the point exactly not stepped over (`<`) | P1 269, P4 1 |
| M8 | fenwick: each weight added to every later slot, not the Fenwick ones | P1 219, P4 269 |
| E1 | ★: the middle taken as `low + (high - low) / 2` | 0 |
| E2 | linear: the fallback after the walk returns 0 | 0 |
| E3 | floor: the missing-floor case returns -1 | 0 |
| E4 | fenwick: the highest power of two kept below n, not up to it | 0 |

M1, M3 and M7 are one mistake in three arms: a point on the boundary
between two runs goes to the earlier one. Each run then loses one
point and the one before it gains one, so the picks are wrong (P1) but
the shares hardly move, and P4 notices once in 300 cases. M2, M5 and
M6 move whole runs and fail P4 on almost every case.

E4 was first written as a mutant that should be killed. With n a power
of two the descent then starts at n/2, so it can reach at most n - 1
weights, but n - 1 is also the most it ever needs: the point is below
the total, so the last weight's run is never stepped over. It is
equivalent, and the Fenwick arm's mutant M8 replaced it.

## Verification

Every arm prints the same output as `random_pick_with_weight.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints `6000 checks, 0 failures` on the first
two and runs clean under the third. `karac check` passes on every arm,
the differential and the bench program.

The frozen legacy backends refuse every file at type checking,
"unary '*' requires 'ref T' ... found 'i64'": legacy types the items of
a `Vec`'s `iter()` by value, so it refuses the `*x` that sums the
weights and the harness's `fair`. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 lists of 10,000 weights
(the problem's longest) from 1 to 100,000 once; then in each of 50
rounds every list gets a fresh solution, seeded by round and list, and
10,000 picks (the problem's most calls). Every implementation uses the
same generator and prints `20 lists of 10000, 50 rounds of 10000 picks:
total 50025388919, checksum 683557184`, the Kāra program under `karac
__mir-run` included (in 79 s). Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.00 s |
| Rust (`rustc -O`) | 0.91 to 1.02 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.98 to 1.04 s |
| Go | 1.25 to 1.34 s |
| Python | 19.1 to 19.3 s |
| Kāra (`karac build --mir`) | 0.99 to 1.02 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`df61cbfff6`. Under `karac __mir-llvm-run` the program prints the same
line in 2.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
