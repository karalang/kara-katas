# 336. Palindrome Pairs

Given a list of distinct words, return every ordered pair of indices
`(i, j)`, `i != j`, such that `words[i] + words[j]` is a palindrome.

```
["abcd", "dcba", "lls", "s", "sssll"]  ->  (0, 1) (1, 0) (2, 4) (3, 2)
["bat", "tab", "cat"]                  ->  (0, 1) (1, 0)
["a", ""]                              ->  (0, 1) (1, 0)
```

## Approaches

Split a word `w` at every position into a prefix and a suffix. If the suffix
is a palindrome and some word is the reverse of the prefix, that word goes
after `w`. If the prefix is a palindrome and some word is the reverse of the
suffix, that word goes before `w`. Three arms answer "is some word the
reverse of this piece" in different ways, and one tries every pair.

| file | mechanism | cost |
|---|---|---|
| `palindrome_pairs.kara` ★ | a `Map` from each reversed word to its index, looked up with the piece as a slice of `w`. The empty prefix is tried by the first rule only, so two words that are each other's reverse are not reported twice | `O(n · L²)` |
| `palindrome_pairs_trie.kara` | a trie of the reversed words, kept as a pool of `Node` structs. Each node holds the word that ends there and every word whose part not yet inserted is a palindrome. Each word walks forwards down the trie | `O(n · L²)` time, `O(n · L)` nodes |
| `palindrome_pairs_lengths.kara` | the two rules again, but a split is tried only when it leaves a piece whose length is the length of some word. The words are in a `SortedMap`, the lengths in a `Set`, and each candidate is an owned reversed copy | `O(n · L · m)` for `m` distinct lengths |
| `palindrome_pairs_brute.kara` | every ordered pair, checked by walking inwards from both ends of the virtual concatenation, so nothing is concatenated | `O(n² · L)` |
| `differential.kara` | the four arms, a concatenate-and-reverse oracle and eight properties on 11,701 lists | — |
| `bench/palindrome_pairs.kara` | 50 solves of a 20,000-word list, by the ★ arm | — |

Every arm sorts its pairs and prints the same 19 lines: the three examples,
nine edge cases (the empty list, one empty word, no pairs, the empty word
beside palindromes, prefix and suffix pairs, words that are reverses of
each other at several lengths), six random lists of 4 to 9 words, and a
1,000-word list over `{a, b}` whose 4,107 pairs are printed as a count and
a hash. The four arms' output is byte-identical, and `palindrome_pairs.py`
mirrors the ★ arm.

## Differential

`differential.kara` checks every list of at most three distinct words drawn
from the 40 words of length 0 to 3 over `{a, b, c}` (10,701 lists), then
1,000 random lists of up to 30 distinct words of 0 to 8 letters over 2 to 4
letters. The oracle concatenates each ordered pair and compares the result
with its reverse.

| | property |
|---|---|
| P1 | the four arms agree |
| P2 | they equal the oracle |
| P3 | listing the words backwards maps `(i, j)` to `(n-1-i, n-1-j)` |
| P4 | reversing every word swaps each pair, since the reverse of `a + b` is `reverse(b) + reverse(a)` |
| P5 | the pairs are strictly increasing, so distinct, and never pair a word with itself |
| P6 | swapping the letters `a` and `b` keeps the pairs |
| P7 | the empty word pairs both ways with exactly the non-empty palindromes |
| P8 | appending the reverse of the first word, when it is new, adds the pairs `(0, n)` and `(n, 0)` |

`10701 exhaustive lists (5616 pairs), 1000 random lists (15752 pairs), 0
failures`, on every surface.

## Mutation testing

Fourteen edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: the empty prefix is tried by both rules | **killed** | P1, P2, P5 |
| M2 | ★: the split that takes the whole word is never tried | **killed** | P1, P2, P4, P7, P8 |
| M3 | ★: the second rule puts the partner after `w` | **killed** | P1, P2, P4, P5 |
| M4 | ★: a word may pair with itself | **killed** | P1, P2, P5, P7 |
| M5 | ★: the palindrome check also compares the middle byte with itself | silent (equivalent) | — |
| M6 | trie: "palindrome below" tests the piece from its second byte | **killed** | P1 |
| M7 | trie: a word is not listed below its own end node | **killed** | P1 |
| M8 | trie: drop `ends != i` while walking | silent (equivalent) | — |
| M9 | lengths: test for a word one longer than the prefix | **killed** | P1 |
| M10 | lengths: the empty suffix is tried by the second rule too | **killed** | P1 |
| M11 | brute: the right end starts one byte early | **killed** | P1 |
| M12 | brute: a word may pair with itself | **killed** | P1 |
| M13 | oracle: a word may pair with itself | **killed** | P2 |
| M14 | oracle: every concatenation is a palindrome | **killed** | P2 |

Both silent mutations are equivalent. M5 compares the middle byte of an
odd-length piece with itself, which always matches. M8: walking word `i`
down the trie checks the word ending at depth `k` only while `k` is shorter
than word `i`, and word `i` itself ends at depth `len(w)`, so `ends == i`
cannot happen there. P1 catches everything the non-★ mutations do, because
each arm is compared against the ★ arm's answer first.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and all five programs are
valgrind-clean at `-O0` with `KARAC_AUTO_PAR=0` and `KARAC_BUF_CACHE=0`
(`All heap blocks were freed`, no errors). The four arms' output is
byte-identical to `palindrome_pairs.py`. The ★ arm keeps its words in a
`Map`, but every arm sorts its pairs before printing, so the output does not
depend on the hash order.

The interpreter is slow on the arms that make many small calls. With a
release karac, the brute-force arm takes 63.6 s under `--interp` against
0.32 s on the JIT, and the differential 80.6 s against 1.2 s. The other three
arms take 0.5 to 3.2 s. Nearly all of that time is per-call bookkeeping in
the interpreter rather than the arms' own work, filed as B-2026-10-03-21.

## Benchmarks

`bench/palindrome_pairs.kara` and its four mirrors time the ★ arm as
written. 20,000 distinct words over `{a, b, c}`, 1 to 10 letters long, are
built once. Each of 50 punches appends a `d` to one random word, which no
other word contains, so that word loses most of its pairs. The whole list is
solved, and the `d` is removed again. The sink is a rolling hash of each
solve's pair count and pairs.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, karac built
from `main` at `b87830f19` with the three fixes listed under Compiler
findings, measured 2026-10-03. Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-C target-cpu=x86-64-v3` (matched) | 627.9 ms ± 32.4 | 1.00× |
| rust `-O -C overflow-checks=on` (equal-safety) | 635.1 ms ± 22.5 | 1.01× |
| rust `-O` | 643.4 ms ± 39.1 | 1.02× |
| **kāra `karac build`** | **741.1 ms ± 19.1** | **1.18×** |
| c `clang -O3` | 808.2 ms ± 26.7 | 1.29× |
| c `-march=x86-64-v3` (matched-ISA) | 819.1 ms ± 25.9 | 1.30× |
| go `go build` | 1451.4 ms ± 43.9 | 2.31× |
| python 3 | 4588.9 ms ± 177.4 | 7.31× |

**Kāra is 17% behind equal-safety Rust, and ahead of C and Go.** Before the
fix for B-2026-10-03-25 the Kāra row was 867 ms, 38% behind: `pairs.sort()`
called its tuple comparator through a function pointer on every comparison.
C sorts with `qsort` and a comparator function, which is the same shape, and
that is probably why C trails here, though that is inferred rather than
measured. Where the remaining 17% against Rust goes was not investigated.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 167.3 ms ± 6.2 | 20.1 KiB | 8.8 MiB |
| rust | 313.8 ms ± 9.8 | 3903.9 KiB | 9.2 MiB |
| kāra | 491.5 ms ± 23.8 | 362.2 KiB | 12.0 MiB |
| go | — | 2198.2 KiB | 10.7 MiB |
| python | — | — | 25.7 MiB |

`karac build` is 2.9× clang's cold compile and 1.6× rustc's. Kāra's binary is
18× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

The benchmark kernel's sink matches all four language twins and Python
(`sink 832271229`).

## Compiler findings

- **B-2026-10-03-25 (perf, low, fixed): a bare `sort()` over tuples called
  its comparator through a function pointer**, so it was slower than the
  `sort_by(|a, b| a.cmp(b))` spelling of the same order. The bench went from
  867 ms to 741 ms once the comparator was inlined.
- **B-2026-10-03-23 (miscompile, high, fixed): a tuple literal stored into a
  container with narrower integer fields was laid out at `i64` widths.**
  `v.push((1, 2))` on a `Vec[(i32, i32)]` wrote past its slot and every read
  got the wrong fields. Found while probing the sort fix with other element
  types; the kata itself uses `(i64, i64)` and was never affected.
- **B-2026-10-03-24 (miscompile, medium, fixed): `--interp` ordered a `u64`
  inside a tuple as signed**, so `sort()` and `<` disagreed with the compiled
  backends. Found by the same probe. Sorted-collection keys and `min`/`max`
  over such tuples are still left over.
- **B-2026-10-03-21 (perf, low, open): the interpreter spends about 5 µs on
  every call to a small function**, almost all of it in ownership
  bookkeeping. Details are under Verification.

`karac check` reported no diagnostics on any arm. That says little about the
diagnostics overall: the author already knows the language, which is why
authoring like this never counts toward the machine-fix rate.
