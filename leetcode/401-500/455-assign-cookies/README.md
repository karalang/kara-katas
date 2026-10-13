# 455. Assign Cookies

Each child `i` has a greed factor `g[i]`, the smallest cookie size that
will content them, and each cookie `j` has a size `s[j]`. A child gets
at most one cookie, and is content when `s[j] >= g[i]`. Return the
largest number of content children.

```
g = [1,2,3], s = [1,1]    ->  1
g = [1,2],   s = [1,2,3]  ->  2
```

**Constraints:** `1 <= g.length <= 3 * 10^4`;
`0 <= s.length <= 3 * 10^4`; `1 <= g[i], s[j] <= 2^31 - 1`.

## Approaches

Every arm is `fn find_content_children(g: Vec[i64], s: Vec[i64]) -> i64`.

| file | mechanism |
|---|---|
| `assign_cookies.kara` ★ | sort both; walk the cookies from the smallest, giving each to the least greedy child still waiting if it is big enough, and skipping it if not. O(n log n + m log m) |
| `assign_cookies_largest.kara` | sort both; walk the children from the greediest, giving the largest cookie left to each child it satisfies and passing over a child it does not |
| `assign_cookies_ceiling.kara` | keep the cookies in a `SortedMap` of size to count; take the children by greed and give each the smallest cookie that will do, found with `ceiling`, stopping when none is left |
| `assign_cookies_answer.kara` | binary search on the answer: `k` children can be fed exactly when the `k` least greedy, in order, are fed by the `k` largest cookies, in order |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, no
cookies, a cookie too small, the largest greed, children greedier than
most of the cookies, more children than cookies, a shuffled exact fit, and for 300 random cases of 1 to 200 children and 0 to 200 cookies
(greed and sizes from 1 up to 5, 100, 10,000 or 2^31 - 1) the total
content children and a checksum. `assign_cookies.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 5 children and 0 to 5 cookies, greed and sizes 1 to 5, the count is brute force's over every assignment |
| P2 | on 1 to 40 children and 0 to 40 cookies, shuffling both lists keeps the count |
| P3 | one more cookie adds 0 or 1 |
| P4 | one child fewer takes away 0 or 1 |
| P5 | scaling every greed and size by 1 to 5 and adding one constant to all of them keeps the count |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a cookie must be larger than the greed | P1 507 |
| M2 | ★: the children are taken greediest first | P1 655, P4 30 |
| M3 | largest: the greediest child is never considered | P1 487 |
| M4 | largest: a fed child stays to be fed again | P1 451, P4 87 |
| M5 | ceiling: the largest cookie at most the greed is taken | P1 873, P3 44, P4 55 |
| M6 | ceiling: a used-up size stays on offer | P1 418, P3 241 |
| M7 | answer: the `k` smallest cookies are tried | P1 466, P3 45, P4 38 |
| M8 | answer: the search stops one short | P1 858 |

P1, the only property with an independent answer, sees all eight. P2
and P5 see none: every arm sorts both lists, and only ever compares a
size with a greed, so neither the order of the input nor an
order-keeping change of the numbers can reach a mutant. P3 and P4 allow a
change of 0 or 1, so they catch only the mutants that move the count
by more than that or in the wrong direction.

## Verification

All four arms print the same output as `assign_cookies.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends the ★, largest and answer arms match
under `karac run --interp`. LLJIT and `karac build` stop in the legacy
code generator on the harness's index into an array literal ("Index
operator applied to non-array type"). The ceiling arm and the
differential do not type-check on legacy: its `SortedMap.ceiling` hands
out the key by value, so `*size` is rejected. The bench program builds
and matches under legacy `karac build`. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000,000 children and
1,000,000 cookies, greed and sizes from 1 to 10^9, once, then runs 10
rounds; each round sets one greed and one size to new random values
and counts the content children, which copies and sorts both lists.
Every implementation prints `10 rounds on 1000000 children and 1000000
cookies: 9989178 content, checksum 74623912`, the Kāra program under
`karac __mir-run` included (in 27 s).

The mirrors keep the ★ arm's structure: copy, sort both, one pass.
Rust's `sort` is stable like Kāra's; Go's `slices.Sort` and C's `qsort`
are not, which cannot change a sort of plain integers. Spot timings on
a shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 3.2 to 3.3 s |
| Rust (`rustc -O`) | 0.64 to 0.75 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.67 to 0.71 s |
| Go | 2.1 to 2.3 s |
| Python | 8.6 to 10.5 s |
| Kāra (legacy `karac build`) | 0.47 to 0.48 s |
| Kāra (`karac build --mir`) | 0.43 to 0.51 s |

The two sorts are nearly all the work. C's `qsort` calls its comparison
through a function pointer for every step. The v2 compiled backend's
sort took 5.2 to 5.7 s, about 12 times legacy's, until B-2026-10-12-30
(below) was fixed; the row above is re-timed at kara `5f01de4c5c`, and
is now level with legacy. `bench.sh` still uses the default
`karac build`, which is legacy. Under `karac __mir-llvm-run` the
program prints the same line in 19 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-12-30** (MIR runtime, performance; fixed in kara
  `8acdc0bdb5`, which merges the elements in place with one scratch
  buffer): `Vec.sort` on
  the compiled MIR backend sorts an array of indices with a bottom-up
  merge sort, allocating each pass and calling the comparison through
  a function pointer; a probe sorting 1,000,000 numbers 10 times takes
  2.63 s under `karac build --mir` against 0.21 s under legacy
  `karac build`. The output is correct; only the time is off.
- The ceiling arm takes the cookie with `let Some((size, _)) =
  cookies.ceiling(want) else { break; };`, the natural form here; the
  `.expect(...)` form would have hit B-2026-10-12-28 (kata 453).
