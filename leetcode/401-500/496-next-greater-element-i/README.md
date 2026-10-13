# 496. Next Greater Element I

The next greater element of some element `x` in an array is the first
greater element that is to the right of `x` in the same array.

You are given two distinct 0-indexed integer arrays `nums1` and
`nums2`, where `nums1` is a subset of `nums2`.

For each `0 <= i < nums1.length`, find the index `j` such that
`nums1[i] == nums2[j]` and determine the next greater element of
`nums2[j]` in `nums2`. If there is no next greater element, then the
answer for this query is `-1`.

Return an array `ans` of length `nums1.length` such that `ans[i]` is
the next greater element as described above.

```
nums1 = [4,1,2], nums2 = [1,3,4,2]  ->  [-1,3,-1]
nums1 = [2,4],   nums2 = [1,2,3,4]  ->  [3,-1]
```

**Constraints:** `1 <= nums1.length <= nums2.length <= 1000`;
`0 <= nums1[i], nums2[i] <= 10^4`; all integers in `nums1` and `nums2`
are unique; all the integers of `nums1` also appear in `nums2`.

## Approaches

Every arm is `fn next_greater_element(nums1: Vec[i64], nums2:
Vec[i64]) -> Vec[i64]`.

| file | mechanism |
|---|---|
| `next_greater_element.kara` ★ | a stack and a map: walk `nums2` keeping a stack of numbers still waiting for something greater; each new number answers every smaller one on top, then waits itself. Each question is then one `Map` lookup. O(n) expected time |
| `next_greater_element_brute.kara` | for each question, find the number in `nums2` and scan right for the first greater one. O(n·m) |
| `next_greater_element_backward.kara` | from the right: a stack of the numbers that could still answer someone, nearest on top; each number drops the candidates no greater than itself, and the top is its answer. `(0..len).rev()`, then `iter().map(...).collect()` over the map |
| `next_greater_element_table.kara` | the ★ walk with a `vec![-1; 10001]` indexed by the number in place of the map, and a stack of positions in `nums2` rather than numbers |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, one
number, `nums2` falling, `nums2` rising, a valley, every number asked
in a shuffled order, the problem's largest values, and for 300 random
cases (`nums2` of 1 to 30 distinct numbers below 100, `nums1` of 1 to
all of them in a random order) the count asked, the count with a
greater number and a checksum. `next_greater_element.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases: `nums2` of 1 to 25 distinct numbers below 30, 100
or 200 in turn, and `nums1` of 1 to all of them in a random order.
There is no reference arm; P1 checks each answer against the
definition directly.

| | property |
|---|---|
| P1 | each answer fits the definition: `-1` when nothing after the number is greater, else the first greater number after it |
| P2 | each answer is the one it gets when all of `nums2` is asked |
| P3 | a number above all of them on the end of `nums2` answers every `-1` and changes nothing else |
| P4 | a number above all of them in front of `nums2` changes nothing |
| P5 | every number moved up by the same amount moves every answer but `-1` up by it |

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a new number answers only the top of the stack | P1 1027, P3 1250 |
| M2 | ★: a number never answered gets 0, not -1 | P1 1213, P3 1213, P5 1209 |
| M3 | brute: the scan skips the number right after | P1 1245, P3 869 |
| M4 | brute: the scan keeps going past the first greater | P1 1203, P3 1313 |
| M5 | backward: the answer is the bottom of the stack, not the top | P1 1085, P3 1313 |
| M6 | backward: the stack drops the greater candidates | P1 1384, P3 1217 |
| M7 | table: the answer is the number before the one that pops | P1 1313, P3 1213 |
| M8 | table: the bottom of the stack is never answered | P1 702, P3 859, P4 702 |

P2 catches none of them: each mutant answers a number the same way
whatever else is asked, so it agrees with itself. It stays as a guard
against an arm whose answers depend on `nums1`, which none of these
edits introduce.

Three more edits are equivalent, and all three hang on the numbers
being distinct: stopping the ★ arm's popping at an equal top rather
than only a greater one, starting the brute scan at the number itself
rather than the one after (the number is never greater than itself),
and keeping an equal candidate on the backward arm's stack. Each gives
0 failures, as it must on distinct numbers.

## Verification

The four arms print the same output as `next_greater_element.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included.
The differential prints `30000 checks, 0 failures` on both. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on the brute, backward and table
arms: `karac run --interp`, LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build print the same output. They refuse the ★ arm
at type checking, on `Some(g) => out.push(*g)`: "unary '*' requires
'ref T' ... found 'i64'". Legacy reads what `Map.get` returns as a
value, where v2 reads it as a borrow. The differential carries a copy
of the ★ arm and is refused the same way, as is the bench program.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10,000 cases once:
`nums2` is 1,000 distinct numbers from 0 to 10,000 (the problem's
most), drawn by shuffling the front of a pool of all of them, and
`nums1` is every other one of them from the end. Then it solves each
once. Every implementation prints `10000 cases of 1000 and 500:
4959092 with a greater number, checksum 812723056`, the Kāra program
under `karac __mir-run` included (in 50 s).

The mirrors keep the ★ arm's structure: a fresh hash map for each case
and a stack. Rust's `HashMap` hashes with SipHash, as Kāra's `Map`
does; Go uses its built-in map; C uses the small open-addressing table
of #447 (linear probing, a 64-bit mixing hash). Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.62 to 0.68 s |
| Rust (`rustc -O`) | 0.64 to 0.70 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.70 s |
| Go | 1.07 to 1.18 s |
| Python | 6.9 to 7.4 s |
| Kāra (`karac build --mir`) | 0.84 to 1.09 s |

The legacy `karac build` refuses this program, on the ★ arm's `*g` (see
Verification) and on `next_greater_element(all1[c], all2[c])`, where
it reads `all1[c]` as a move out of the index and v2 reads a borrow. So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`d9a7136c58`. Under `karac __mir-llvm-run` the program prints the same
line in 6.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends. The first drafts used `&&` and `!`, which Kāra
spells `and` and `not`; `karac fix` rewrote them.
