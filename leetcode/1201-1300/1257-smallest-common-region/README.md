# 1257. Smallest Common Region

You are given some lists of `regions` where the first region of each
list includes all other regions in that list.

Naturally, if a region `x` contains another region `y` then `x` is
bigger than `y`. Also, by definition, a region `x` contains itself.

Given two regions: `region1` and `region2`, return *the smallest region
that contains both of them*.

If you are given regions `r1`, `r2`, and `r3` such that `r1` includes
`r3`, it is guaranteed there is no `r2` such that `r2` includes `r3`.

It is guaranteed the smallest region exists.

```
regions = [["Earth","North America","South America"],
           ["North America","United States","Canada"],
           ["United States","New York","Boston"],
           ["Canada","Ontario","Quebec"],
           ["South America","Brazil"]]
region1 = "Quebec", region2 = "New York"     ->  "North America"
region1 = "Canada", region2 = "South America" ->  "Earth"
```

**Constraints:** `2 <= regions.length <= 10^4`; `2 <= regions[i].length <= 20`;
`1 <= regions[i][j].length, region1.length, region2.length <= 20`;
`region1 != region2`; names are English letters; the input
is generated so that a region holding both exists.

The arms are `fn find_smallest_region(regions: Vec[Vec[String]], region1: Str, region2: Str) -> String`.

## Approaches

The lists make a tree: each region but the outermost is inside exactly
one other. The answer is the lowest common ancestor of the two regions.

| file | mechanism |
|---|---|
| `smallest_common_region.kara` ★ | by parents: each region's parent in a `Map[String, String]`, the regions holding `region1` (itself included) collected into a `Set[String]` by walking up, then a walk up from `region2` until it meets one of them |
| `smallest_common_region_depth.kara` | by depth: the regions numbered as they are met (`Map[String, i64]`), parents and names in `Vec`s, each region's depth counted by a closure, the deeper region walked up to the other's depth, then both together until they meet |
| `smallest_common_region_paths.kara` | by paths: a `fn path_down` that walks up with `while let Some(up) = parent.get(..)` and reverses, and the last region two paths share, found by `zip`, `take_while` and `count` |
| `smallest_common_region_switch.kara` | two walkers, as for the meeting point of two linked lists: each walks up and, past the outermost region, starts again from the other region; both have gone the same distance when they meet |
| `smallest_common_region_solution.kara` | a Rust solution as LeetCode's Rust users write it (`HashMap<&str, &str>` borrowing the input's names, `while let Some(&p)`, `parent[cur]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples; the total of
the regions found and a checksum of them for 4000 random pairs in 200
random trees of 2 to 2000 regions, nested broadly or deeply (`total
954268, checksum 211326608`); and three pairs at the constraints' top, in
a chain of 10000 regions each inside the one before and in two chains of
5000 from the root. `smallest_common_region.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, depth and paths arms checked clean as first
written. The switch arm was first written with a closure return type,
`|at: Str, restart: Str| -> String`, which Kāra does not take; `karac
fix` removes it. The solution arm takes one round of fixes, 20 by `karac
fix`'s count: the `use std::collections` line deleted, `struct
Solution;` to `struct Solution {}`, `Vec<..>` and `HashMap<..>` to
brackets, `HashMap` and `HashSet` to the prelude's `Map` and `Set`,
`&str` to `Str`, `::new` to `.new`, `for r in &regions` to `for r in ref
regions`, `&r[1..]` to `r[1..]`, `Some(&p)` to `Some(p)` with
`.cloned()` on the lookup, `!` to `not`, and the harness's
`regions.clone()` to `regions`, which the call only borrows. All five
check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike. The solution arm keeps the borrowed names of the Rust
original: its map is a `Map[Str, Str]` of views into `regions`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a region holds itself and the regions listed inside it and
inside those, found by recursion over the lists, and of the regions
holding both, the answer is the one holding the fewest. 2000 random
trees of 2 to 12 regions, a third with every region inside the one
before, a third inside one of the two before and a third inside any
earlier one, the lists shuffled, and a random pair of regions, possibly
the same region twice.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the two regions swapped give the same region |
| P3 | the lists in reverse order give the same region |
| P4 | the region found and `region1` give the region found |
| P5 | every name given a prefix gives the same region with it |
| P6 | the ★ arm's region |

All 60,000 checks pass on every arm: `2000 trees: checksum 124506460,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the holding regions collected from `region2` | P1 971, P2 1633, P4 1633, P6 3884 |
| S2 | ★: one step up from `region2` at most (`while` to `if`) | P1 492, P2 957, P4 957, P6 1968 |
| D1 | depth: the deeper `region2` never walked up to `region1`'s depth | runtime error: index out of bounds |
| D2 | depth: one step together at most (`while` to `if`) | P1 62, P2 62, P6 62 |
| A1 | paths: regions compared by the length of their names | P1 351, P2 351, P6 351 |
| A2 | paths: the paths left outermost last | runtime error: index out of bounds |
| W1 | two walkers: past the outermost region, a walker stays there | P1 783, P4 55, P6 783 |
| W2 | two walkers: walking while the names differ in length | P1 1020, P2 1629, P4 39, P6 1020 |
| L1 | solution: the second walk from `region1` | P1 1021, P2 1633, P6 1021 |
| L2 | solution: `region1` itself not counted as holding it | runtime error: key not found |

All ten are caught: seven by P1, the statement read literally, and P6,
and three by a runtime error, D1 and A2 by an index past the end of a
`Vec` and L2 by `parent[cur]` asked of the outermost region, which has
no parent. P2, the two regions swapped, catches the six that treat the
two regions differently (S1, S2, D2, A1, W2, L1). P4, the region found
asked with `region1`, catches the four whose answer, asked again, moves:
S1 and S2 answer with a region at or below `region2` that need not hold
`region1`; W1's walkers meet right only when the two regions are at one
depth, and W2's stop at the first two names of one length, so a pair
answered right can be followed by one answered wrong. P3, the lists
in reverse order, catches none: every arm reads the lists into a map of
parents before walking, so their order is never seen. P5, every name
given a prefix, catches none either, though A1 and W2 compare the
lengths of names: a prefix adds one to every length, so lengths equal
before are equal after.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (each region's parent in a `Map`, the regions holding `region1` in a
`Set`, then a walk up from `region2` until it meets one of them) on 20
random trees of 10000 regions built once, each nested broadly or deeply,
with 250 random pairs asked of each; every region found folded into a
checksum. Every program prints `20 trees of 10000 regions, 250 pairs
each: checksum 968443197`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 7.021 to 7.929 s | 7.414 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 7.188 to 7.841 s | 7.582 s |
| Rust (`rustc -O`) | 8.602 to 9.193 s | 8.898 s |
| Rust (`rustc -O -C overflow-checks=on`) | 8.628 to 9.357 s | 8.786 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 8.515 to 9.094 s | 8.827 s |
| C (`clang -O3`) | 11.46 to 12.41 s | 11.78 s |
| C (`clang -O3 -march=x86-64-v3`) | 11.50 to 12.19 s | 11.86 s |
| Go | 6.154 to 7.488 s | 6.613 s |
| Python | 6.940 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 14% ahead of Rust with overflow checks on (7.582 s
against 8.786 s). C takes about 1.6x Kāra's time; Go is about 13% ahead
of Kāra (6.613 s against 7.582 s). Python is about 8% ahead of Kāra
(6.940 s against 7.582 s). No profile was taken.
