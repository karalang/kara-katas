# 331. Verify Preorder Serialization of a Binary Tree

A binary tree is serialized by a preorder walk that writes each node's value,
and a `#` for each absent child, separated by commas. Given such a string,
decide whether it is the serialization of some binary tree, without
rebuilding the tree.

```
"9,3,4,#,#,1,#,#,2,#,6,#,#"  ->  true
"1,#"                        ->  false   (the root's right child is missing)
"9,#,#,1"                    ->  false   (a node after the tree has ended)
```

## Approaches

The serializer emits the grammar `tree := '#' | value tree tree`, so the
question is whether the string is exactly one `tree`. The four arms decide it
four ways.

| file | mechanism | cost |
|---|---|---|
| `verify_preorder.kara` ★ | count open slots over `split(",")`. The empty tree has one slot, each token fills one, and a value opens two more. Valid when no token arrives with no slot open and none is left open at the end | `O(len)` time, `O(1)` space beyond the split |
| `verify_preorder_stack.kara` | leaf folding: push tokens, and whenever the top three are a value and two `#`, replace them with one `#`. Valid when the stack folds to a single `#` | `O(len)` time and stack |
| `verify_preorder_recursive.kara` | recursive descent over the grammar with one cursor (`pos: mut ref i64`) shared by the whole recursion. Valid when one tree parses and the cursor ends at the last token | `O(len)` time, `O(depth)` stack |
| `verify_preorder_bytes.kara` | the slot count over the bytes, with no split. A token starts at the first byte and after each comma, and is a `#` exactly when its first byte is one | `O(len)` time, `O(1)` space |
| `differential.kara` | the four arms, an exhaustive oracle and eight properties on 36,963 cases | — |
| `bench/verify_preorder.kara` | 160 checks against 16 strings of about 200,000 tokens, by the ★ arm | — |

Every arm prints the same 19 lines: the three examples, nine edge cases (`#`,
`#,#`, a lone value, `1,#,#` and one `#` too many, a leading `#`, three-digit
values, a left spine and the same spine one `#` short), six random trees with
their last token dropped, and a tree of 10,001 tokens with one `#` appended.
The four arms' output is byte-identical, and `verify_preorder.py` mirrors the
★ arm.

The byte arm needs one rule the split gives for free: a string ending in a
comma has an empty last token. `split` yields `""`, which is not `"#"` and so
counts as a value, and the byte arm counts the same token after its loop.

## Differential

`differential.kara` checks every string over `{1, #}` of 1 to 13 tokens
(16,382 strings) against the serializations of every tree shape with at most
6 nodes, which covers every valid string that short: a valid string of 13
tokens has 6 values. It then runs eight properties on 400 random trees with
values in `[0, 100]`, and on mutations of them.

| | property |
|---|---|
| P1 | the four arms agree |
| P2 | an exhaustive string is valid exactly when it is in the shape set |
| P3 | a serialization produced by a walk is valid |
| P4 | dropping any one token from a valid string makes it invalid |
| P5 | appending any token to a valid string makes it invalid |
| P6 | a valid string has one more `#` than values |
| P7 | replacing any `#` with `v,#,#` keeps a valid string valid |
| P8 | when `A` is valid, `v,A,B` is valid exactly when `B` is |

P2 is the oracle. 197 of the exhaustive strings are valid, the sum of the
Catalan numbers C₀ to C₆, one per shape. P8 is stated one way on purpose: a
valid string has no valid proper prefix, so the left subtree's parse ends
exactly where a valid `A` does, but when `A` is invalid the split between `A`
and `B` is not unique and nothing follows.

`16382 exhaustive strings (197 valid), 20581 random cases (228 for P8), 0
failures`, on every surface.

## Mutation testing

Fourteen edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: start with 0 open slots | **killed** | P1, P2, P3, P7 |
| M2 | ★: no early exit when no slot is open | **killed** | P1, P2 |
| M3 | ★: accept `slots <= 0` at the end | silent (equivalent) | — |
| M4 | ★: a value opens two slots net | **killed** | P1, P2, P3, P4, P5, P7, P8 |
| M5 | folding: fold any three-token top ending in two `#` | **killed** | P1 |
| M6 | folding: fold at most once per token | **killed** | P1 |
| M7 | folding: accept any single-token stack | **killed** | P1 |
| M8 | recursive: ignore tokens left after the tree | **killed** | P1 |
| M9 | recursive: one child parse is enough | **killed** | P1 |
| M10 | recursive: running out of tokens counts as a `#` | **killed** | P1 |
| M11 | bytes: no early exit when no slot is open | **killed** | P1 |
| M12 | bytes: no count for a trailing empty token | **killed** | P1 (5 cases) |
| M13 | all four arms: accept a leftover open slot | **killed** | P2, P4, P8 |
| M14 | oracle: shapes of up to 5 nodes only | **killed** | P2 |

M3 is equivalent: a token that would take `slots` below zero is refused by
the early exit first, so `slots` is never negative. M12 is the trailing-comma
rule above, and only five strings exercise it. M13 breaks every arm the same
way, so it is the one that shows the properties have teeth without P1; M14
shows the oracle is not vacuous.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. The four arms are valgrind-clean
(`All heap blocks were freed`) at `-O0` with `KARAC_AUTO_PAR=0`. The
differential is too, apart from one 48-byte block that the `Map`/`Set` hash seed
leaves behind (B-2026-10-03-11, below). The four arms' output is
byte-identical to `verify_preorder.py`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 445967011`).

## Benchmarks

`bench/verify_preorder.kara` and its four mirrors time the ★ arm as written.
One random tree of 100,000 values is serialized once, and 16 strings are
built from it: the tree itself, one with a token dropped, one with a `#` grown
into `7,#,#`, and one with a `#` inserted. Each of 160 punches checks one of
them, so the work is the split and the count over about 200,000 tokens. The
sink is a rolling hash of each answer and the string it came from.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, karac built from
`main` at `bc22c5fe2` with this thread's three unpushed commits (none touches
`split`), measured 2026-10-03. Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| c `-march=x86-64-v3` (matched-ISA) | 249.8 ms ± 8.1 | 1.00× |
| c `clang -O3` | 262.1 ms ± 14.1 | 1.05× |
| rust `-O -C overflow-checks=on` (equal-safety) | 432.4 ms ± 23.5 | 1.73× |
| rust `-O` | 434.2 ms ± 18.0 | 1.74× |
| rust `-C target-cpu=x86-64-v3` (matched) | 435.7 ms ± 23.1 | 1.74× |
| go `go build` | 575.8 ms ± 36.1 | 2.30× |
| python 3 | 1909.4 ms ± 35.3 | 7.64× |
| **kāra `karac build`** | **2313.8 ms ± 51.4** | **9.26×** |

**Kāra is 5.4× equal-safety Rust and slower than CPython.** This is not the
slot count, which is a compare and an add per token. Kāra's `split` heap
allocates every token: `karac_runtime_string_split` mallocs and copies each
piece, and each one is freed when the temporary `Vec` dies at the end of the
loop. callgrind puts that at about 350 of the roughly 520 instructions spent
per token, and 400 ms of the 2.3 s is system time. Rust's `split` yields
borrowed `&str`, Go's `strings.Split` makes string headers that share the
input's bytes, and C scans in place. Overflow checks cost Rust nothing here.
This is filed as B-2026-10-03-10.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 101.1 ms ± 2.3 | 15.8 KiB | 10.0 MiB |
| rust | 168.9 ms ± 6.0 | 3868.4 KiB | 30.9 MiB |
| kāra | 344.5 ms ± 11.7 | 362.4 KiB | 41.1 MiB |
| go | — | 2188.0 KiB | 31.6 MiB |
| python | — | — | 31.4 MiB |

`karac build` is 3.4× clang's cold compile and 2.0× rustc's. Kāra's binary is
23× clang's and 11× smaller than rustc's. Its higher peak RSS is the same
cause: the split's result holds a separate allocation for each of about
200,000 tokens. Raw numbers are in `bench/results.container-x86.json`.
Methodology and caveats are in [`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**No wrong answers**, and every arm was byte-identical on every surface from
the first run. Verifying the kata found one slowdown and one leak report:

- **B-2026-10-03-10 (perf, medium, open): `for tok in s.split(",")` heap
  allocates and frees every token, even when the loop only compares it.** It
  is the whole gap in the benchmark above. The runtime already has a
  non-owning string header that the element drop skips, so a split whose
  result cannot outlive its source, and whose tokens do not escape the loop
  body, could hand out views into the source instead. A one-byte separator
  could also be found with `memchr`.
- **B-2026-10-03-11 (leak, low, open): any compiled program that hashes a
  `Map` or `Set` key leaves a 48-byte "possibly lost" block under valgrind.** The
  random seed mixes in the current thread's id, and `std::thread::current()`
  allocates a handle for the main thread that is never freed. The id is also
  `ThreadId(1)` on every main thread, so it adds no entropy there. With
  `KARAC_HASH_SEED` pinned the block is gone, which is why the differential
  (which keeps its shape set in a `Set`) is the only program here that shows
  it.

`karac check` reported nothing on any of the five programs. That says little
about the diagnostics: the author already knows the language, which is why
authoring like this never counts toward the machine-fix rate.
