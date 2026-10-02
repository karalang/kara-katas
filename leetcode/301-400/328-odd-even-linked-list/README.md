# 328. Odd Even Linked List

Given the head of a singly linked list, group the nodes at odd positions (1st,
3rd, 5th, ...) followed by the nodes at even positions, keeping the relative
order inside each group, and return the new head. Use `O(1)` extra space.

```
[1, 2, 3, 4, 5]       ->  [1, 3, 5, 2, 4]
[2, 1, 3, 5, 6, 4, 7] ->  [2, 3, 6, 7, 1, 5, 4]
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `odd_even_list.kara` ★ | `shared struct` nodes; two tails, `odd` and `even`, take turns unlinking the next node, then the even group is hung after the last odd node | `O(n)` time, `O(1)` space |
| `odd_even_list_arena.kara` | the same relinking over an index arena: `vals[i]` and `next[i]`, `-1` for the end | `O(n)` time, `O(1)` space beyond the arena |
| `odd_even_list_enum.kara` | a persistent `shared enum` list, never relinked: every other node copied into a new list twice, and the two appended | `O(n)` time, `O(n)` new nodes and `O(n)` stack |
| `odd_even_list_vec.kara` | no nodes: the values at even indices, then those at odd indices | `O(n)` time, `O(n)` space |
| `differential.kara` | the four arms on 608 inputs, six properties | — |
| `bench/odd_even_list.kara` | a million-node list regrouped and walked ten times by the ★ arm | — |

Every arm prints the same 16 lines: the two examples, six edge cases, five
lists of `1..n` for `n` in 10, 11, 1,000, 1,001 and 10,000 reported by a
position-weighted hash, and three small random lists. The four arms' output is
byte-identical, and `odd_even_list.py` mirrors the ★ arm.

## Why the relinking loop stops where it does

`even` is always the last node of the even group so far, so the node after it
is the next odd one. Each step moves that node onto `odd` and gives `even` the
node after it. The loop ends when either is missing: no node after `even`
means the list had an even count and `even` is its last node; no node after
the one just moved means an odd count, and `even.next` was already set to
nothing by the move. In both cases `even`'s group is properly terminated, so
hanging the group's head after `odd` finishes the list.

The persistent arm gives up `O(1)` space for a list nothing can relink. A
`shared enum` value is immutable, so the only way to regroup it is to build
new nodes. The input survives, which is what P5 below checks.

## Differential

`differential.kara` runs the four arms on eight hand-picked lists (the empty
list, one, two, three and five values, both examples, and the 64-bit limits)
and 600 pseudo-random lists of 0 to 39 values in `[0, 9]`, so most lists repeat
values.

| | property |
|---|---|
| P1 | all four results agree |
| P2 | the result has as many values as the input |
| P3 | the result is a permutation of the input |
| P4 | position `k` holds input position `2k` for `k < ceil(n/2)`, and position `ceil(n/2) + k` holds input position `2k + 1` |
| P5 | the persistent arm leaves its input list as it was |
| P6 | splitting the input after an even number of values splits the result: `f(a ++ b) = odd(a) ++ odd(b) ++ even(a) ++ even(b)` |

`rounds 608, values 12221, failures 0`, and all properties hold, on every
surface.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | relink: never hang the even group back on | **killed** | P1, P2, P3, P4, P6, from `[1, 2, 3]` |
| M2 | relink: hang the even group after the first node, not the last odd one | **killed** | P1, P2, P3, P4, P6, from `[1, 2, 3]` |
| M3 | relink: skip unlinking the next odd node from `even` | **killed** | never finishes; the process was killed by signal 9 |
| M4 | persist: keep every node of the odd half (`true` for `false`) | **killed** | P1, from `[1, 2]` |
| M5 | persist: `append` onto an empty list drops the second list | **killed** | P1, from `[1, 2]` |
| M6 | persist: the even half first | **killed** | P1, from `[1, 2]` |
| M7 | arena: no early return for a one-node list | silent (equivalent) | — |
| M8 | arena: loop while `even` exists, not its successor | **killed** | `vec index out of bounds` panic in `arena` |
| M9 | arena: end the odd group instead of hanging the even group | **killed** | P1, from `[1, 2]` |
| M10 | vec: the even group starts at index 2 | **killed** | P1, from `[1, 2]` |
| M11 | vec: the odd group steps by 1 | **killed** | P1, from `[1, 2]` |
| M12 | relink: advance `even` to the node just moved, not the one after it | **killed** | P1, P2, P3, P4, P6 |

M7 is equivalent. On a one-node list `next[head]` is `-1`, so `even_head` is
`-1`, the loop never runs, and the final `next[odd] = even_head` writes the
`-1` that was already there.

M3 leaves `even.next` pointing at the node that just became `odd`'s
successor, so the list turns into a cycle. Why the process then died by
signal 9 rather than by the 30-second timeout was not investigated; running out
of memory while copying a cyclic list into a `Vec` is the likely cause, but it
is inferred, not measured.

The persistent, arena and Vec mutants are caught only by P1. P2 to P6 read the
★ arm's result, so the other arms are checked only against it.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac build` with `KARAC_AUTO_PAR=0`, and the default
auto-parallelising `karac build`. Under `karac run --interp`, the ★, arena and
Vec arms and the differential are byte-identical too. The persistent arm is
not: the interpreter copies its whole list on every alias and overflows its
stack at 8,000 nodes, short of the arm's 10,000-node case. That is
B-2026-10-02-58 (below). The four arms' output is byte-identical to
`odd_even_list.py`. All five programs are valgrind-clean at `-O0`.

`scripts/surface-sweep.py --filter 328- --timeout 30` reports `5 programs · 4
clean · 0 DIVERGENCES · 1 timeouts`; the timeout is the persistent arm under
`--interp`, which the sweep uses as its oracle. The budget is 30 s rather than
the usual 400 because that run's memory grows with its time, to 2.7 GB by
4,000 nodes.

The benchmark kernel's sink matches all four language twins and Python
(`sink 933734468`).

## Benchmarks

`bench/odd_even_list.kara` and its four mirrors time the ★ arm as written. A
list of 1,000,000 nodes with values in `[0, 999999]` is built once. Each of
10 punches regroups the whole list in place, then walks it once, folding
every value into a rolling hash weighted by its position and replacing the
value at one random position. The hash is the sink. Regrouping over and over
scatters the nodes through memory, so the workload is bound by the latency of
following `next`. The Rust twin is `Rc<RefCell<Node>>`, because a Kāra
`shared struct` is a reference-counted node whose `mut` fields carry a borrow
flag. The C and Rust twins never free the list, since the process exits right
after; Rust's own drop of a million-node `Rc` chain would recurse once per
node.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10208+g9b394d94c` with the fixes for B-2026-10-02-57 and -60
applied, measured 2026-10-02. Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| go `go build` | 466.3 ms ± 17.6 | 1.00× |
| **kāra `karac build`** | **709.7 ms ± 79.5** | **1.52×** |
| rust `-O` | 747.3 ms ± 129.7 | 1.60× |
| rust `-O -C overflow-checks=on` (equal-safety) | 759.3 ms ± 89.9 | 1.63× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 809.0 ms ± 115.3 | 1.74× |
| c `clang -O3` | 890.2 ms ± 102.2 | 1.91× |
| c `-march=x86-64-v3` (matched-ISA) | 920.2 ms ± 100.5 | 1.97× |
| python 3 | 5097 ms ± 96 | 10.9× |

**Go is fastest by a third, and the other three compiled lanes overlap.**
Kāra, Rust and C land between 710 and 920 ms with standard deviations of 80
to 130 ms, so their order here is not a ranking. Kāra measured ahead of C, but
an earlier run on the same container while it was busy with a build had C
ahead, so read the two as a tie. The peak memory below suggests why Go leads:
a million Go nodes take 18 MiB against 32 to 33 MiB for C and Kāra and 48 MiB
for Rust, and a denser list puts more nodes in each cache line a walk pulls
in. That reading is inferred from the memory numbers, not measured.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 99.8 ms ± 5.8 | 15.7 KiB | 32.2 MiB |
| rust | 172.2 ms ± 6.1 | 3865.7 KiB | 48.0 MiB |
| kāra | 515.3 ms ± 14.7 | 396.3 KiB | 32.9 MiB |
| go | — | 2179.0 KiB | 18.1 MiB |
| python | — | — | 84.3 MiB |

`karac build` is 5.2× clang's cold compile and 3× rustc's. Kāra's binary is
25× clang's and 9.8× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**No wrong answers from the kata's own programs.** Four findings, two of them
fixed; the first is a wrong answer the kata's recursion led to:

- **B-2026-10-02-57 (miscompile, high, fixed in kara `f868e4639`): `--interp`
  scoped names dynamically.** A call pushed its frame as one more scope on a
  single stack, and a name lookup searched every scope outward, so a name the
  callee did not bind was looked up in its CALLERS' scopes before the
  globals. A callee's call to a free function `helper` ran a caller's local
  closure named `helper` instead, and a caller's local `LIMIT` hid a constant.
  The same walk made every global lookup cost the call depth, so recursion was
  quadratic: depth 16,000 took 25.3 s, and now takes 0.56 s. A frame's lookup
  now stops at its own frame and goes straight to the globals. The persistent
  arm's recursion was the first deep recursion in the kata set.
- **B-2026-10-02-60 (codegen gap, medium, fixed in kara `9b322b2ca`): a local closure
  broke `karac build` of later functions.** After any function bound a local
  closure `helper`, every function compiled after it that called the free
  function `helper` failed with `Undefined variable 'helper'`: the record of
  closure names was not scoped to the function that bound it. Found while
  writing B-2026-10-02-57's test.
- **B-2026-10-02-58 (perf, medium, open): `--interp` deep-copies a `shared
  enum` on every alias.** Building the persistent arm's list is quadratic in
  time and memory under the interpreter: 4,000 nodes take 9.8 s and 2.7 GB,
  and a recursive walk of them 45 s and 10.7 GB, against 0.17 s under the JIT.
  At 8,000 nodes the interpreter overflows its stack.
- **B-2026-10-02-59 (diagnostics, low, open): a `shared enum` is not treated
  as an RC handle by the move checker.** `append(alternate(head, true),
  alternate(head, false))`, the persistent arm's natural spelling, passes
  `head` twice and draws an E0500 "moved here, used again" warning that a
  `shared struct` would not; `.clone()` on a `shared enum` is an error. The
  program is correct on every surface; the warning is advisory, and the arm
  keeps the natural spelling.

`karac check` flagged six `mut` markers on arguments that were already
`mut ref` in the differential (E0219), and `karac fix` removed them. That says
little about the diagnostics: the author already knows the language, which is
why authoring like this never counts toward the machine-fix rate.
