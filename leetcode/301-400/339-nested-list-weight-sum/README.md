# 339. Nested List Weight Sum

A nested list holds integers and further nested lists. An integer's depth is
the number of lists around it, so the outer list's own integers have depth 1.
Return the sum of every integer times its depth.

```
[[1,1],2,[1,1]]  ->  10    four 1s at depth 2, one 2 at depth 1
[1,[4,[6]]]      ->  27    1*1 + 4*2 + 6*3
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `nested_weight_sum.kara` ★ | walk the tree recursively over a `ref Vec[Nested]`, passing each list's depth down to its members | `O(n)`, `O(d)` stack |
| `nested_weight_sum_bfs.kara` | level by level: each level's integers count at that level's depth, and the members of its lists, moved out of them, make the next level | `O(n)`, `O(w)` for the widest level |
| `nested_weight_sum_stack.kara` | an explicit `Vec[(Nested, i64)]` stack of (member, depth) pairs | `O(n)`, `O(n)` at worst |
| `nested_weight_sum_fold.kara` | a `weight(ref self, depth)` method on `Nested`, summing a list's members with `iter().map().sum()` | `O(n)`, `O(d)` stack |
| `nested_weight_sum_scan.kara` | one pass over the text, counting `[` minus `]` for the depth, without building the tree | `O(n)` in the text, `O(1)` |
| `differential.kara` | the five arms, an independent oracle and eight properties | — |
| `bench/nested_weight_sum.kara` | 4,000 parses and walks of 7 KB lists, by the ★ arm | — |

`Nested` is `enum Nested { Int(i64), List(Vec[Nested]) }`. Every tree-building
arm shares one recursive-descent parser (`parse_list`) for LeetCode's text
form, and a seeded generator (`gen_text`) for large inputs.

Every arm prints the same 12 lines: eight hand cases (the two examples, `[]`,
`[[]]`, empty lists mixed with an integer, negatives, a ten-deep list and a
large integer) and a summary (text length and weight sum) of four generated
lists, up to 50,000 members, 450 KB of text and depth 30. The five arms'
output is byte-identical, and `nested_weight_sum.py` mirrors the ★ arm.

## Differential

`differential.kara` compares the five arms with an oracle that, for each
integer in the text, recounts the brackets before it from the start of the
text (quadratic, and sharing no code with any arm). It runs on the eight hand
cases and 300 generated lists (1 to 30 top-level members, depth limit 1 to
6), and checks the properties on each.

| | property |
|---|---|
| P1 | the five arms agree (also on the four large lists the arms print) |
| P2 | they equal the oracle |
| P3 | wrapping the list in one more list adds the plain sum of its integers |
| P4 | joining two lists into one adds their weight sums |
| P5 | negating every integer negates the weight sum |
| P6 | tripling every integer triples it |
| P7 | `n` integers at depth 1 weigh their plain sum, and an integer `v` nested `k` lists deep weighs `v * k` |
| P8 | inserting an empty list as the first member of every list changes nothing |

`308 lists checked (weight sums add up to 1003219), 0 failures`, on every
surface.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each run with every
failure printed rather than the first ten.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: a list passes its own depth to its members | **killed** | P1, P2, P3, P4, P7 |
| M2 | ★: the outer list starts at depth 0 | **killed** | P1, P2, P4, P7 |
| M3 | bfs: each level goes two deeper | **killed** | P1 |
| M4 | bfs: the first level is depth 0 | **killed** | P1 |
| M5 | stack: a list pushes its members at its own depth | **killed** | P1 |
| M6 | stack: the outer members start at depth 0 | **killed** | P1 |
| M7 | fold: an integer ignores its depth | **killed** | P1 |
| M8 | fold: members weigh two deeper | **killed** | P1 |
| M9 | scan: `]` does not close a level | **killed** | P1, P4 |
| M10 | scan: drops the minus sign | **killed** | P1, P4 |
| M11 | parse: drops the minus sign | **killed** | P1, P2, P3, P4, P5, P7 |
| M12 | scan: reads digits in base 16 | **killed** | P1, P4 |

P1 catches every non-★ mutation, because each arm is compared with the ★
arm's answer first. M11 breaks the parser all four tree arms share, so P1
catches it only through the scan arm, which has its own reader; P2, P3 and
P5 catch it independently.

## Verification

All five arms plus the differential print the same standard output under
`karac run` (LLJIT), `karac run --interp`, `karac build` with
`KARAC_AUTO_PAR=0`, and the default auto-parallelising `karac build`, and the
five arms' output is byte-identical to `nested_weight_sum.py`. `karac run`
also prints the copy warnings described under B-2026-10-04-22 to standard
error for the BFS and stack arms and the differential.

At `-O0` with `KARAC_AUTO_PAR=0` and `KARAC_BUF_CACHE=0`, valgrind reports
the ★, BFS, fold and scan arms clean (`All heap blocks were freed`, no
errors). The stack arm and the differential, which carries a copy of it,
leak through B-2026-10-04-24 (open), with the right output.

## Benchmarks

`bench/nested_weight_sum.kara` and its four mirrors time the ★ arm as written:
parse a list's text into the tree, then walk it. Eight pseudo-random lists
(800 members each, depth up to 12, about 7 KB of text each) are generated
once; round `r` parses list `r % 8` and weighs it, for 4,000 rounds. A rolling
hash of every round's weight sum is the sink.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, measured
2026-10-04. karac was built from `main` at `e5c676518` with this thread's
fixes for B-2026-10-04-23 (see Compiler findings) and B-2026-10-02-42 (the
f-string `+` flag, which this kernel does not use). Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O` | 495.7 ms ± 10.1 | 1.00× |
| rust `-C target-cpu=x86-64-v3` (matched) | 500.8 ms ± 11.3 | 1.01× |
| rust `-O -C overflow-checks=on` (equal-safety) | 504.7 ms ± 13.9 | 1.02× |
| **kāra `karac build`** | **518.5 ms ± 14.5** | **1.05×** |
| c `-march=x86-64-v3` (matched-ISA) | 520.3 ms ± 9.8 | 1.05× |
| c `clang -O3` | 531.0 ms ± 13.9 | 1.07× |
| go `go build` | 822.8 ms ± 22.0 | 1.66× |
| python 3 | 4312 ms ± 98 | 8.70× |

Kāra is within 3% of equal-safety Rust and level with C here. All three
spend most of the time allocating: under valgrind the Kāra binary makes
2,741,336 allocations and the overflow-checked Rust one 2,749,339. Before the
B-2026-10-04-23 fix the same Kāra kernel took about 1.15 s, 2.3× Rust, and
made 3.8× Rust's allocations.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 118.6 ms ± 5.6 | 16.1 KiB | 1.7 MiB |
| rust | 207.8 ms ± 6.0 | 3868.4 KiB | 2.2 MiB |
| kāra | 367.6 ms ± 19.3 | 341.6 KiB | 2.5 MiB |
| go | — | 2171.7 KiB | 7.7 MiB |
| python | — | — | 8.1 MiB |

`karac build` is 3.1× clang's cold compile and 1.8× rustc's. Kāra's binary is
21× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

The benchmark kernel's sink matches all four language twins and Python
(`sink 337140885`).

## Compiler findings

- **B-2026-10-04-23 (perf, medium): the ★ walk deep-copied every subtree it
  lent to its own `ref` parameter.** The first bench measured Kāra at 2.3×
  Rust, with 1.08M allocations against Rust's 287k. `for item in
  items.iter() { match item { List(inner) => depth_sum(inner, depth + 1) } }`
  treated the call as a move of `inner`, so codegen took an independent copy
  of each list's payload on every call (`karac_clone_enum_Nested`) and freed
  it after: each subtree was copied once for every level above it. A `ref`
  parameter cannot keep its argument, so the copy was pure cost. Fixed in
  the kara repo: the bench went to 518 ms, within 3% of equal-safety Rust,
  with the same number of allocations.
- **B-2026-10-04-21 (missing feature, low): `char` had no `is_ascii_digit`,
  `is_ascii_alphabetic` or `is_ascii_hexdigit`.** Every parse loop in the kata
  scans a `Vec[char]` with `text[pos].is_ascii_digit()`, which the typechecker
  admitted only on integers. Fixed in the kara repo; the kata uses the call as
  written.
- **B-2026-10-04-20 (miscompile, low): under `--interp` those three
  predicates answered an integer wider than a byte from its low byte**, so an
  `i64` 304 was a digit (0x130 masks to `'0'`) while every compiled surface
  said no. Found probing the predicates across widths for -21. Fixed in the
  kara repo; the kata never calls them on an integer.
- **B-2026-10-04-22 (diagnostics, low): the copy warning (W0299) missed a
  `for` element placed inside a tuple or other literal.** The stack arm's
  `for x in inner { stack.push((x, depth + 1)) }` copies `x` into the tuple
  just as `stack.push(x)` would, but only the bare push warned. Fixed in the
  kara repo: `karac check` now warns once on the stack arm and once on the BFS
  arm, which copies each member into the next level. Both copies are the arms
  as written, since a bare `for` borrows the list (moving the elements out
  with `into_iter()` does not avoid the copy today, B-2026-09-27-76).
- **B-2026-10-04-24 (leak, medium, open): `while let Some(item) = stack.pop()`
  leaks the popped enum's payload buffer when the body does not destructure
  `item`.** Found by valgrind: the stack arm, and the differential that
  carries a copy of it, lose about 4.5 MB at `-O0` on every compiled surface,
  with the right output. Filed for the drop schedule work in the kara repo.
- **B-2026-10-04-25 (miscompile, medium, open): under `--interp`, a
  `match` binding over a borrowed `for` element lent to a `ref` parameter
  runs the payload's `Drop` bodies on every call.** The interpreter's half of
  -23, found while checking whether the compiled fix could change when a
  `Drop` body runs. `Nested` has no `Drop` body, so the kata's output is not
  affected.
