# 269. Alien Dictionary

A list of words is sorted according to an unknown alphabet. Recover an order of
the letters consistent with that sorting, or `""` if none exists.

```
[wrt, wrf, er, ett, rftt]  ->  "wertf"
[z, x]                     ->  "zx"
[abc, ab]                  ->  ""       a word cannot precede its own prefix
[ab, adc]                  ->  "abcd"   c is unconstrained but must still appear
[z, x, z]                  ->  ""       a cycle
```

**Constraints:** `1 ≤ words.length ≤ 100`; lowercase English letters only.

## Approaches

| file | direction | order produced |
|---|---|---|
| `alien_dictionary.kara` ★ | Kahn — peel letters nothing depends on | lexicographically **least** |
| `alien_dictionary_dfs.kara` | DFS — record after all successors, reverse | *a* valid order |
| `alien_dictionary_brute.kara` | try every arrangement in order, keep the first valid | lexicographically least |
| `differential.kara` | 1,500 cases, equality **and** property checks | — |

## The input is not a graph

The whole first half of this problem is turning a sorted list into one, and both
rules that do it are places to go wrong.

**Rule 1 — only the first differing character says anything.** From
`["wrt", "wrf"]` the sort tells us `t < f`. It says nothing about later
positions, and nothing about non-adjacent pairs — those follow by transitivity,
and adding them as edges is redundant at best.

**Rule 2 — a word may not be followed by its own prefix.** `["abc", "ab"]` cannot
be sorted under any alphabet: no letter comparison is ever reached, and a shorter
word sorts first when one is a prefix of the other. This yields **no edge**, so a
solver that only ever adds edges accepts it silently and returns a plausible
order for an impossible input. It is the single most missed case here.

## Making the answer testable

The problem accepts *any* valid order, and "any" is not a testable answer — it
makes two correct implementations disagree and a differential meaningless. So the
★ file always takes the **smallest ready letter**, which yields the
lexicographically least valid order. That is unique, so the ★ file, the brute
force, and every mirror must produce the same string.

The DFS deliberately does **not** produce it. Reversed post-order depends on the
visit sequence, not on letter values, so its output is a different — equally
valid — order. The differential therefore checks it by **property**: same verdict
(empty or not), same letter set, and its output satisfies every derived
constraint. Checking a non-unique answer by equality against one implementation
asserts an implementation detail; checking it by property tests the problem.

## How each one breaks

- **Kahn** discovers a cycle by *exhaustion* — letters remain but nothing is
  ready. Its own trap is the in-degree: record a duplicate edge and the successor
  is stranded forever.
- **DFS** must catch a cycle *in the act*, which needs three states rather than a
  visited bit — `0` unvisited, `1` on the current path, `2` finished. Collapsing
  `1` and `2` doesn't merely miss cycles, it reports **success** for them.
- **Brute force** contains no topological argument at all: no frontier, no finish
  order, no notion of a cycle. An unsatisfiable set simply exhausts the
  permutations. That is why it can adjudicate the other two.

## Generator design

Random word lists are almost never sortable under *any* alphabet, so a naive
generator answers `""` nearly always and never exercises the accept path. The
main families work **backwards**: draw a hidden alphabet, generate random words,
and sort them under it. Every such input is satisfiable by construction, and the
solvers must recover an order consistent with a permutation they never see.

The rest attack the two rules directly — swapping an adjacent pair of a sorted
list usually contradicts it, and one family plants a word immediately before its
own prefix.

Over 1,500 cases: **850 solvable** (57%) and **349 rejected by the prefix rule**
(23%), so both paths are well travelled.

## The harness had to be un-refactored

The obvious tidy-up is to derive the constraints once in a shared helper and hand
them to all three solvers. **That is wrong here, and the harness measured how
wrong.** Rules 1 and 2 are the hardest part of the problem, and a shared helper
makes a bug in either break all three solvers *identically*, so the cross-check
goes silent on exactly the code most worth checking:

| injected bug | shared helper | own derivation |
|---|---|---|
| prefix rule dropped | **0 detected** | **292** |
| an edge at every differing position, not the first | **0 detected** | **286** |

Both scored zero until each solver derived its own constraints. The duplication
in `differential.kara` is deliberate and commented, and the two bugs that only
live in the topological half were already caught either way:

| injected bug | detected by |
|---|---|
| DFS collapses on-path and finished into one bit | 301 verdict + 301 invalid orders |
| duplicate edges inflate the in-degree | 107 |

## Benchmark

`bench/` builds a **flat corpus of 20,000 small word lists once**, then punches
the ★ Kahn ordering over all of them **60 times** — 1,200,000 solver calls, each
on a handful of short words. Sink `208478711`, reproduced by all four compiled
mirrors and by Python.

**What it measures is many small fixed-cost passes**, rather than one big one.
Every call clears a 676-slot adjacency array and a 26-slot in-degree vector,
scans a few adjacent word pairs for their first differing byte, and runs a
selection loop that is O(26) per emitted letter. The input is tiny and the
per-call overhead is not — the opposite balance from
[#261](../261-graph-valid-tree/) (one huge structure) or
[#266](../266-palindrome-permutation/) (one long stream), and the shape a lot of
real code actually has.

The corpus is drawn so roughly half the lists are solvable — words generated over
a small alphabet and sorted under a hidden permutation, then some lists have an
adjacent pair swapped. An all-unsolvable corpus would exit early on most calls
and never reach the selection loop.

**Everything is flat and hoisted in every mirror** — three parallel index arrays
plus one byte array, no array of strings, no array of arrays, and the working
structures allocated once and cleared per call. That is a parity decision made
after [#267](../267-palindrome-permutation-ii/), where a per-leaf string became
four different allocation strategies and a 3× phantom result.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 138.2 ± 3.1 ms | 0.69× |
| Rust `-O` | 141.4 ± 4.5 ms | 0.70× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 148.4 ± 5.0 ms | 0.74× |
| **Kāra (codegen)** | **201.4 ± 2.8 ms** | 1.00× |
| Go | 458.6 ± 9.7 ms | 2.28× |

**The ordering is byte-identical to the container**, which is the strongest form
of corroboration this corpus offers: `c < rust < rust_ovf < kara < go` on both
hosts, with the twins tracking their bases and nothing impossible in the table.

**Kāra is 1.46× behind C and 1.36× behind equal-safety Rust** — both slightly
wider than the container's 1.28× and 1.14×. This is a `Map`/adjacency-heavy
workload, and it sits with [#249](../249-group-shifted-strings/) (1.61×) and
[#244](../244-shortest-word-distance-ii/) (1.21×) as the block's map lanes;
Kāra's deficit tracks how much map work each does.

**Go is 3.32× behind C here, the largest Go gap in the block**, up from 2.56× on
the container. Half of it is identified below and the mechanism is unchanged.

### The x86 corroboration run

| lang | mean (ms) | σ |
|---|---|---|
| C (`-march=x86-64-v3`) | 343.6 ± 9.8 | 2.9% |
| C | 345.4 ± 11.8 | 3.4% |
| Rust | 358.3 ± 8.7 | 2.4% |
| Rust (checked + `target-cpu=v3`) | 379.6 ± 10.6 | 2.8% |
| Rust (checked, equal-safety) | 386.3 ± 11.8 | 3.1% |
| **Kāra** | **441.9 ± 10.2** | 2.3% |
| Go | 885.4 ± 25.9 | 2.9% |

**This lane ranks, and the previous two did not.** The twins track their bases
(`c_v3` within 0.5% of `c`; the checked Rust builds slower than plain `rustc -O`,
as they should be), σ is 2.3–3.4%, and nothing in the table is impossible — no
`-march` flag beating its own baseline, no checked build beating an unchecked
one. That is what a trustworthy row set looks like, and it is worth stating
explicitly given how the last two lanes went.

Kāra is **1.28× behind C** and **1.14× behind the equal-safety Rust build** —
its ordinary position in this corpus.

**Go is 2.56× behind C, the largest Go gap here, and half of it is identified.**
Every mirror clears the 676-slot adjacency array with an indexed loop, because
that is what the Kāra kernel does. Go's compiler lowers a *range*-clear to
`memclr` but does not recognise the indexed form; swapping only that loop takes
Go from 880.9 to **604.3 ms** against C's 340.0 — closing **277 ms of the 541 ms
gap, about 51%** — on the same sink. The remaining 264 ms is **not identified**.

The range-clear variant stays a probe rather than replacing the mirror: all five
run the same algorithm, and rewriting one of them to suit its own optimiser while
the others keep the plain form is exactly the parity break that produced #267's
phantom. Method in [`bench/probe/README.md`](bench/probe/README.md).

Kāra's binary is 340.9 KiB against C's 19.7 KiB, Go's 2.17 MB and Rust's 3.87 MB;
peak RSS is 6.5 MiB against C's 4.8 MiB and Go's 8.8 MiB.

`bench/results.container-x86.json` holds this run; it is corroboration only
(BENCHMARKS.md § Hosts).

## Kāra features exercised

- **`Vec[Vec[bool]]` as an adjacency matrix** over a fixed 26-letter space, and
  `Vec[Vec[i64]]` as a word list under construction.
- **Recursion with three `mut ref` accumulators** (`state`, `order`, `ok`) — the
  DFS threads all three and forwards them without re-marking, since they are
  already `mut ref` in scope.
- **Insertion sort with a custom comparator** (`before(a, b, rank)`), used by the
  generator to sort under the hidden alphabet.
- **`(x + 97i64) as u8 as char` inside an f-string** to render letter indices.
- **Early loop exit by assigning the bound** (`k = lim`), the idiom this corpus
  uses in place of `break` inside a `while` with a carried index.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

No compiler bugs found.

## Running

```bash
karac run alien_dictionary.kara
karac run alien_dictionary_dfs.kara      # a different, equally valid order
karac run alien_dictionary_brute.kara

diff <(karac run alien_dictionary.kara) <(python3 alien_dictionary.py) && echo OK
diff <(karac run alien_dictionary.kara) <(karac run alien_dictionary_brute.kara) && echo OK

# 1,500 cases: star==brute by equality, dfs by property
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in alien_dictionary alien_dictionary_dfs alien_dictionary_brute differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

```bash
# cross-language benchmark (needs hyperfine, rustc, clang, go)
BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
