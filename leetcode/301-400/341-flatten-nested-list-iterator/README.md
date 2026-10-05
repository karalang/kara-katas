# 341. Flatten Nested List Iterator

Given a nested list of integers, where each member is an integer or a further
nested list, implement an iterator over its integers in order: `has_next()`
says whether one remains and `next()` returns it.

```
[[1,1],2,[1,1]]  ->  1 1 2 1 1
[1,[4,[6]]]      ->  1 4 6
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `flatten_iterator.kara` ★ | a stack of the members still to visit, the next on top; `has_next` pops lists and pushes their members in reverse until an integer is on top | `O(n)` over the whole iteration, `O(n)` |
| `flatten_iterator_eager.kara` | the constructor walks the tree once into a `Vec[i64]`; `next` reads it back through a cursor | `O(n)` to build, `O(1)` a call, `O(n)` |
| `flatten_iterator_path.kara` | the iterator keeps the whole list and a path of indices from the root to the next member, and re-walks the path from the root on every step | `O(n d)` for depth `d`, `O(d)` beyond the list |
| `flatten_iterator_peek.kara` | a one-integer lookahead: `has_next` checks it, `next` hands it out and finds the one after | `O(n)`, `O(n)` |
| `flatten_iterator_trait.kara` | the ★ stack behind the standard `Iterator` trait, so the caller writes `for v in NestedIter.new(items)` | `O(n)`, `O(n)` |
| `differential.kara` | the five arms, an oracle that reads the integers straight out of the text, and seven properties | — |
| `bench/flatten_iterator.kara` | 80 nested lists of 20,000 top-level members built and drained by the ★ arm | — |

Every arm prints the same 12 lines: eight hand cases (the two examples, an
empty list, lists of empty lists, negatives, a ten-deep nest and a large
value) and a summary of four generated lists, up to 50,000 top-level members
nested 30 deep. The arms parse LeetCode's text form themselves. The five arms'
output is byte-identical, and `flatten_iterator.py` mirrors the ★ arm.

| arm | `run --interp` | `run` (JIT) | `build` | `build`, `KARAC_AUTO_PAR=0` |
|---|---|---|---|---|
| ★ stack | ✓ | ✓ | ✓ | ✓ |
| eager | ✓ | ✓ | ✓ | ✓ |
| path | ✓ | ✓ | ✓ | ✓ |
| peek | ✓ | ✓ | ✓ | ✓ |
| trait | ✓ | codegen gap | codegen gap | codegen gap |

✓ is the same 12 lines as `flatten_iterator.py`. The trait arm's `for` loop
over a user `Iterator` does not lower in codegen yet (B-2026-10-05-17), so
JIT and both builds refuse it with that message; under `--interp` it needed
B-2026-10-05-16, fixed for this kata. Valgrind on the four compiled arms at
`-O0` reports no errors and nothing lost. The 3 to 4 blocks still reachable
at exit (5 to 6 MB) are the runtime's large-buffer recycling cache
(`karac_free_buf`), which keeps a freed `Vec` buffer for reuse: a one-function
program that fills a 200,000-element `Vec` shows the same single block.

## Differential

`differential.kara` compares the five arms with an oracle that never builds
the tree: it takes every run of digits in the text, with a `-` just before it
as its sign, in the order written. It runs on the eight hand cases and 300
generated lists (0 to 6 top-level members, depth 1 to 6), and checks the
properties on each.

| | property |
|---|---|
| P1 | the five arms agree (also on the four large lists the arms print) |
| P2 | they equal the oracle |
| P3 | wrapping the whole list in one more list keeps the answer |
| P4 | flattening is idempotent: the answer, read back as a list, flattens to itself |
| P5 | joining two lists' members into one list joins their answers |
| P6 | reversing every list at every depth reverses the answer |
| P7 | asking `has_next` three times before each `next`, and again at the end, changes nothing (the stack and path arms move in `has_next`) |

`308 cases checked (143048 integers flattened), 0 failures` under
`karac run --interp`. The differential does not build, because it carries
the trait arm, whose `for` loop over a user `Iterator` codegen cannot lower
yet (B-2026-10-05-17, see Compiler findings).

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each run under
`--interp` without the four large lists, with every failure counted.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: `has_next` pops the integer instead of putting it back | **killed** | panics (`next() past the end`) |
| M2 | ★: pushes a list's members in forward order | **killed** | P1, P2, P4 |
| M3 | eager: skips nested lists | **killed** | P1 |
| M4 | eager: `has_next` is true one past the end | **killed** | panics (index out of bounds) |
| M5 | eager: `next` advances by two | **killed** | P1 |
| M6 | path: descends to a list's second member | **killed** | P1, P7, then panics |
| M7 | path: every list looks one member short | **killed** | P1, P7, then panics |
| M8 | peek: the constructor does not look ahead | **killed** | P1, P7 |
| M9 | peek: pushes a list's members in forward order | **killed** | P1, P7 |
| M10 | trait: drops zeros | **killed** | P1 |
| M11 | trait: pushes a list's members in forward order | **killed** | P1 |
| M12 | ★: drops one-member lists | **killed** | P1, P2, P7 |

P1 catches every mutation that does not panic first, because each arm is
compared with the ★ arm. The two ★ mutations that survive into the
comparison are caught by the oracle as well (P2), so the ★ arm is not
checked only against itself. M10 fails 27 cases, the generated lists that
happen to hold a zero.

## Benchmarks

`bench/flatten_iterator.kara` and its four mirrors time the ★ arm as
written. Each of 80 rounds builds a pseudo-random nested list of 20,000
top-level members (a member is a list of 0 to 4 members one time in three
while the depth is below 12, otherwise an integer from -100 to 100), then
drains it through the stack iterator. A rolling hash of every integer, in the
order the iterator hands them out, is the sink. Rust uses `enum Nested {
Int(i64), List(Vec<Nested>) }`, Go a struct with a slice, C a tagged struct
that frees each list's array once its members are on the stack, and Python
ints and lists.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, measured
2026-10-05, karac built from `d456e8f1f` (B-2026-10-05-16's fix before it
was rebased onto `main` as `3a7995069`). Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O -C overflow-checks=on` (equal-safety) | 223.7 ms ± 9.0 | 1.00× |
| rust `-O` | 232.3 ms ± 10.0 | 1.04× |
| rust `-C target-cpu=x86-64-v3` (matched) | 239.3 ms ± 8.1 | 1.07× |
| c `-march=x86-64-v3` (matched-ISA) | 254.1 ms ± 14.4 | 1.14× |
| c `clang -O3` | 258.0 ms ± 13.5 | 1.15× |
| **kāra `karac build`** | **561.0 ms ± 20.0** | **2.51×** |
| go `go build` | 874.8 ms ± 27.7 | 3.91× |
| python 3 | 4423 ms ± 185 | 19.8× |

Kāra is 2.5× equal-safety Rust, for two reasons found with callgrind over 8
rounds (Kāra 310.7M instructions, Rust 136.9M). The ★ arm's `push_reversed`
rebinds its by-value `Vec` parameter (`let mut rest = items;`), and codegen
deep-copies it there, so each list's subtree is copied once per list above
it (B-2026-10-05-19). Writing the same loop inline, where the list is a
`match` binding, takes the kernel from 0.55 s to 0.34 s and 214M
instructions. The rest is `pop()`: `Nested` is four words, one more than
`Option`'s inline area, so every `pop` boxes the element on the heap and the
`while let` frees the box again (B-2026-10-05-20). The kernel makes 487,028
such allocations over 8 rounds on top of the 125,747 list buffers that Rust
also allocates.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 118.8 ms ± 5.9 | 16.0 KiB | 5.6 MiB |
| rust | 158.7 ms ± 5.1 | 3867.3 KiB | 4.7 MiB |
| kāra | 339.3 ms ± 12.3 | 341.6 KiB | 8.4 MiB |
| go | — | 2167.3 KiB | 31.0 MiB |
| python | — | — | 11.0 MiB |

`karac build` is 2.9× clang's cold compile and 2.1× rustc's. Raw numbers are
in `bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

The benchmark kernel's sink matches all four language twins and Python
(`sink 131040260`), under `karac build` with and without auto-par.

## Compiler findings

- **B-2026-10-05-16 (miscompile, high): under `--interp`, a `for` loop over a value
  of a user type that implements `Iterator` ran its body once, with the
  iterator itself as the loop variable.** The trait arm's `for v in
  NestedIter.new(items)` failed with an `Add` on an integer and a struct,
  and design.md's own `CountUp` example printed the struct. `karac check`
  passed it, typing the variable as the `Item`. Fixed in the kara repo: the
  loop now pulls the value through its own `next` until `None`.
- **B-2026-10-05-17 (codegen gap, medium, open): `karac build` cannot lower the same
  loop.** It fails `for-loop over this iterable is not lowered`, so the
  trait arm runs only under `--interp` until this is fixed; `while let
  Some(v) = it.next()` over the same value builds. Filed for the codegen
  thread.
- **B-2026-10-05-18 (missing feature, medium, open): the iterator adaptors are not
  available on a user `Iterator`.** `NestedIter.new(items).collect()` and
  `.sum()` fail `no method 'collect' on type 'NestedIter'`, where design.md
  defines them on every `Iterator`. The trait arm collects with a `for` loop.
- **B-2026-10-05-14 (perf, medium): `--interp` copied the whole `String` on every
  `push`.** The arms' input generator builds a 450 KB text one character at a
  time, and the ★ arm took 42 s under `--interp`. Fixed in the kara repo: a
  push on a named `String` appends in place, and 200,000 pushes went from
  2.99 s to 0.10 s. The generator appends through a `mut ref String`
  parameter, which still copies the string per call (B-2026-10-05-15, open).
- **B-2026-10-05-19 (perf, medium, open): `let mut rest = items;` over a by-value
  `Vec` parameter deep-copies it, elements included.** The ★ arm's
  `push_reversed` copies each list's whole subtree once for every list above
  it. The bench runs 0.55 s as written and 0.34 s with the same loop written
  inline, where the list is a `match` binding and no copy is made. Filed for
  the by-value parameter thread.
- **B-2026-10-05-20 (perf, medium, open): `pop()` on a `Vec` whose element is
  wider than three words heap-allocates a box for the `Some` payload.**
  `Nested` is four words, and the stack arm pops about twice per node, so the
  bench makes about four times as many allocations as Rust's twin.
