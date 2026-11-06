# 364. Nested List Weight Sum II

You are given a nested list of integers: each element is an integer or a
list whose elements may also be integers or lists. The depth of an integer
is the number of lists it is inside. Let `maxDepth` be the largest depth of
any integer. The weight of an integer is `maxDepth - depth + 1`, so the most
deeply nested integers weigh 1. Return the sum of every integer times its
weight.

```
[[1,1],2,[1,1]]   -> 8    (four 1s at depth 2 weigh 1; the 2 at depth 1 weighs 2)
[1,[4,[6]]]       -> 17   (1*3 + 4*2 + 6*1)
```

**Constraints:** `1 <= nestedList.length <= 50`; integers in `[-100, 100]`;
`maxDepth <= 50`.

## Approaches

The list is `enum Nested { Int(i64), List(Vec[Nested]) }`, parsed from the
LeetCode text form by a small recursive-descent parser over the string's
bytes that every arm shares.

| file | mechanism |
|---|---|
| `weight_sum.kara` ★ | two recursive passes: the first finds `maxDepth`, the second adds each integer times `maxDepth - depth + 1` |
| `weight_sum_levels.kara` | level by level: sum the integers on each level, then add the running sum of the levels so far once per level, which counts an integer at depth `d` once for each level from `d` to the deepest |
| `weight_sum_one_pass.kara` | one walk gathering the plain sum, the depth-weighted sum and `maxDepth`; the answer is `(maxDepth + 1) * plain - weighted` |
| `differential.kara` | the three arms against an oracle that lists every integer with its depth, 45,000 checks, five properties |

`maxDepth` is the depth of the deepest *integer*. Lists with nothing but
empty lists below them make the nesting deeper without making `maxDepth`
larger, so `[1,[[]]]` is 1, not 3. The textbook level-by-level solution
counts those trailing levels and gets this wrong; the level arm here stops
at the last level that holds an integer.

Every arm prints the same 12 lines: the two LeetCode examples, nine edge
cases (an empty list, only empty lists, one integer, empty lists below the
deepest integer, a level with no integers, the deep integer first, negative
integers, one integer five lists down, a staircase), and a checksum over 500
random lists up to six levels deep. `weight_sum.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the three arms, plus an oracle that
flattens the list into (value, depth) pairs and applies the definition. The
test draws 3,000 random lists up to six levels deep, empty lists included,
half of them with integers in `[-3, 3]` and half in `[-100, 100]`.

| | property |
|---|---|
| P1 | each arm gives the oracle's answer |
| P2 | wrapping the whole list in one more list changes no answer |
| P3 | reversing every list changes no answer |
| P4 | the answer plus the depth-weighted sum (problem 339) is `(maxDepth + 1)` times the plain sum |
| P5 | appending `[[],[[[]]]]`, a list of empty lists, changes no answer |

It prints `3000 cases, 45000 checks, 0 failures` under `karac __mir-run`
and `karac run --interp`.

## Mutation testing

Nine edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All nine are killed.

| # | mutation | how |
|---|---|---|
| M1 | two-pass: an empty list counts toward `maxDepth` | P1, P4 and P5, 2668 failures |
| M2 | two-pass: weight is `maxDepth - depth` | P1 and P4, 4492 failures |
| M3 | two-pass: depths counted from 0 | P1 and P4, 4492 failures |
| M4 | levels: trailing empty levels counted | P1, P4 and P5, 1896 failures |
| M5 | levels: the running total is added before the level's sum | P1 and P4, 4492 failures |
| M6 | levels: a level holding lists counts as holding an integer | P1, P4 and P5, 1896 failures |
| M7 | one pass: `maxDepth` times the plain sum, not `maxDepth + 1` | P1 and P4, 4492 failures |
| M8 | one pass: `maxDepth` taken from lists, not integers | P1, P4 and P5, 2668 failures |
| M9 | oracle: weights by depth, which is problem 339 | P1, 3531 failures |

M2, M3, M5 and M7 fail identically because each one takes the plain sum
off the right answer once.

## Verification

All three arms print the same output as `weight_sum.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program builds ten random nested lists once, up to 14 levels
deep, and runs the ★ arm's two-pass sum 20 times on each. The Kāra build
and the C, Rust, Go and Python mirrors all print `checksum 853514947`.
`karac __mir-run` prints the same checksum, in 222 seconds against Python's 4.4.

### Apple M5 Pro, 2026-11-06

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14606+g162ee7a0e`
(g162ee7a0e, the v2/MIR backend), measured 2026-11-06, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| rust `-O` | 18.4 ms ± 0.5 | 4.17× |
| c `clang -O3` | 20.3 ms ± 0.4 | 3.77× |
| **kāra `karac build`, seq** | **76.7 ms ± 0.9** | **—** |
| rust `-O -C overflow-checks=on` (equal-safety) | 83.3 ms ± 1.2 | 0.92× |
| go `go build` | 108.6 ms ± 2.3 | 0.71× |

Kāra is 4.17× `rustc -O` but 0.92× equal-safety Rust: the gap to `rustc -O`
is the cost of overflow checks, which take Rust from 18.4 ms to 83.3 ms when
turned on. Kāra is 3.77× C and 0.71× Go; the C gap was not investigated on
this host. Against the legacy backend (exact counts, dd86e3955, `KARAC_AUTO_PAR=0`) Kāra executes 1.12× the instructions in
0.90× the cycles.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 51.6 ms ± 1.5 | 32.9 KiB | 14.3 MiB |
| rust | 96.8 ms ± 2.6 | 456.2 KiB | 12.5 MiB |
| kāra | 119.9 ms ± 2.1 | 66.9 KiB | 11.9 MiB |
| go | — | 2450.6 KiB | 41.3 MiB |

`karac build` is 2.3× clang's cold compile and 1.2× rustc's. Kāra's
68,520-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`checksum 853514947`).

## Compiler findings

None. Every arm passed `karac check` after `karac fix` added the call-site
`mut` markers, and after the parser's parameter changed from `ref Vec[u8]`
to `Slice[u8]`, the type `String.bytes()` returns.
