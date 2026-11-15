# 1575. Count All Possible Routes

You are given an array of distinct positive integers `locations` where
`locations[i]` represents the position of city `i`, and integers
`start`, `finish` and `fuel`. At each step, if you are at city `i`, you
can pick any city `j` such that `j != i` and move to it, which reduces
your fuel by `|locations[i] - locations[j]|`. Fuel cannot become
negative at any point. You may visit any city more than once, including
`start` and `finish`. Return the count of all possible routes from
`start` to `finish`, modulo `10^9 + 7`.

```
locations = [2,3,6,8,4], start = 1, finish = 3, fuel = 5   ->  4
locations = [4,3,1],     start = 1, finish = 0, fuel = 6   ->  5
locations = [5,2,1],     start = 0, finish = 2, fuel = 3   ->  0
```

**Constraints:** `2 <= locations.length <= 100`; `1 <= locations[i] <= 10^9`;
all `locations` distinct; `0 <= start, finish < locations.length`;
`1 <= fuel <= 200`.

## Approaches

| file | mechanism |
|---|---|
| `routes.kara` ★ | `ways[f][c]`, the routes from city `c` with `f` fuel left that end at the finish: 1 for standing at the finish, plus the routes after each move it can afford, filled from no fuel up. O(fuel · n²) |
| `routes_memo.kara` | the same count read top down: a recursive walk from the start that remembers each finished state in a `Map[(i64, i64), i64]` keyed by city and fuel. O(fuel · n²) |
| `routes_forward.kara` | forward from the start: `reach[f][c]`, the ways to stand at city `c` with `f` fuel left, filled from a full tank down, each state pushing its moves on; the answer adds every way to stand at the finish. O(fuel · n²) |
| `routes_solution.kara` | LeetCode's Rust template (`count_routes(..) -> i32` with a nested `fn dfs` over `usize`, a memo of `-1`s and a `const MOD` in the method body), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples, then
`[1, 2]` from city 0 back to it with 1 and 2 fuel, and `[1, 2, 3]` from
city 1 back to it with 200 fuel, which the modulus reduces; then the sum
of the answers and a checksum for 3000 random problems of up to 5
locations below 10, 300 of up to 20 below 100, 10 of up to 100 below
10^9 (where almost nothing is affordable), and 10 of up to 100 below
200. `routes.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every route walked out from the start, one city to another
while the fuel lasts, counted each time it stands at the finish. It
checks 3000 problems of 2 to 4 distinct locations below 8 and a fuel of
1 to 6, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every location moved by the same amount leaves the answer |
| P3 | every location `x` made `7 - x` leaves the answer |
| P4 | one more unit of fuel never lowers the answer |
| P5 | the start and the finish swapped leave the answer (a route read backwards costs the same) |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 318902244, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

Two first tries in the memo arm were replaced. Looking the memo up under
one unit less fuel was equivalent: the fuel left at a city always has the
same parity (a move's cost has the parity of the distance between the two
positions), so that key is never in the map. Letting a city move to
itself made a move of cost 0, and the walk recursed until the stack ran
out: killed by a crash rather than by a property.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: standing at the finish with no fuel left not counted | P1 952, P6 952 |
| M2 | ★: a move that spends the last of the fuel refused | P1 952, P6 952 |
| M3 | ★: the routes after a move read at the city left | P1 2119, P6 2119 |
| M4 | memo: each state stored one more than its count | P1 987, P5 518, P6 987 |
| M5 | memo: a move allowed only at twice its cost | P1 1336, P5 153, P6 1336 |
| M6 | forward: the finish counted only after fuel has been spent | P1 1074, P6 1074 |
| M7 | forward: each move carries one way, not the ways that reached it | P1 366, P5 134, P6 366 |
| M8 | forward: the states with no fuel left never visited | P1 952, P6 952 |
| M9 | template: every state counted as standing at the finish | P1 2760, P5 1021, P6 2760 |
| M10 | template: every move one unit dearer | P1 1422, P6 1422 |

## Benchmarks

The bench draws 100 problems of 60 distinct locations below 300 and a
fuel of 200 first, then answers them by the ★ arm, in all five
languages. Every implementation prints `100 problems of 60 locations and
fuel 200: routes total 42385903080, checksum 735696291`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.177 s |
| Rust (`rustc -O`) | 0.183 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.198 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.203 s |
| Kāra (`karac build`) | 0.237 s |
| Go | 0.256 s |
| Python | 7.4 s |

Kāra is 1.03x Rust under overflow checks by median.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.202 s and 0.203 s on one run).

## Verification

All four arms print the same output as `routes.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `76e5a13ad`.

## Writing it

The ★, memo and forward arms were written in Kāra and checked as
written.

The Rust template took five rounds of `karac fix`: 6 changed lines,
then the nested `fn` moved with its `const` (17 lines), then 8, 6 and
1:

1. the `Vec<..>` types to `[..]`, `&Vec<i32>` and `&mut Vec<..>` to
   `ref Vec[i32]` and `mut ref Vec[..]`, `&&` to `and`, `&locations` and
   `&mut memo` to `locations` and `mut memo`, the wrapper's `|&x|` to
   `|x|`, and `Solution::` to `Solution.`;
2. the nested `fn dfs` moved above the `impl`, and the `const MOD` it
   names moved with it;
3. `usize` to `i64` throughout `dfs` and its call, `-1i64` to `-1`,
   `memo` to `mut memo` at the recursive call, and the wrapper's
   `as i64` dropped;
4. `ref Vec[i32]` to `Vec[i32]`, the `as i64` casts on `fuel`, `start`
   and `finish` dropped, and the inner `vec![-1; ..]` to `Vec.filled`;
5. the outer `vec![..; n]` to `Vec.filled(n, ..)`.

At kara `572956a03` the second round moved `fn dfs` and left `const MOD`
in the method body, so the moved `fn` named an undefined `MOD`, with no
fix: a Rust nested `fn` sees the items of the block around it, and the
move did not carry them. Filed as B-2026-11-15-9 and fixed in `76e5a13ad`:
the move now carries every one-line `const` of the body above the `fn`
that it names, and the template checks and agrees with no hand edit.
