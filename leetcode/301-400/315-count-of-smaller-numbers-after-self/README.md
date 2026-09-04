# 315. Count of Smaller Numbers After Self

For every position `i`, count the elements to its **right** that are
**strictly smaller** than `nums[i]`.

```
nums = [5, 2, 6, 1]  ->  [2, 1, 1, 0]

5: {2, 1} are smaller and to the right     2
2: {1}                                     1
6: {1}                                     1
1: nothing to the right                    0
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `count_smaller.kara` ★ | Fenwick tree over compressed ranks, right to left | `O(n log n)` |
| `count_smaller_mergesort.kara` | merge sort on indices, counting during the merge | `O(n log n)` |
| `count_smaller_insertion.kara` | sorted `Vec` grown by binary-search insertion | `O(n^2)` worst, memmove-cheap |
| `count_smaller_brute.kara` | the definition: scan everything to the right | `O(n^2)` |
| `differential.kara` | four arms, seven properties, 4,824 cases | — |
| `bench/count_smaller.kara` | 200,000 elements × 24 passes | — |

## Three ways to see the right-hand side before you get there

Every fast answer is the same observation: walking **right to left**, the
elements already visited are exactly "the elements to the right", so the
question at `i` is "how many of what I have seen so far is below `nums[i]`?" —
an order-statistic query on a growing set. The arms differ in the structure that
answers it.

**★ A Fenwick tree over ranks.** Compress the values to their rank among the
distinct values (one sort, one binary search per element), keep a frequency
table indexed by rank, and the query is a prefix sum over ranks `[0, r)` — the
ranks strictly below. A Fenwick tree makes the prefix query and the point update
each `O(log m)`. The tree is 1-indexed exactly as in
[#307](../307-range-sum-query-mutable/): `lowbit(0) == 0`, so rank `r` lives at
slot `r + 1`, and `prefix(r)` sums slots `1..r` — precisely the strictly-smaller
ranks, with no off-by-one to reason about at the query site.

**Merge sort, counting as it merges.** Sort a permutation of the *indices* by
value and watch each merge: when it takes from the LEFT half, every element
already taken from the right half is both smaller and originally to its right,
so the running count of right-half takes is added to that index's answer. No
compression, no extra structure; the recursion is the data structure.

**Insertion into a sorted list.** Keep the seen values in a sorted `Vec`; the
answer is the insertion point (`lower_bound`) and then the value is inserted
there. The shift is `O(n)`, so the whole thing is quadratic in the worst case —
but the shift is a memmove and the constant is tiny, which is why this is the
answer most people actually submit. It is here as a third mechanism, and because
`Vec.insert` in a hot loop is a codegen surface worth walking.

## The tie is the whole problem, and every arm answers it in a different place

"Strictly smaller" means an equal value to the right must **not** be counted.
Each arm enforces that at one specific comparison, and each is the natural place
to get it wrong:

- ★ queries `prefix(r)`, not `prefix(r + 1)` — the ranks *below* `r`.
- The merge takes from the right only when the right element is **strictly**
  smaller (`left <= right` keeps the left); flip it and every duplicate is
  over-counted.
- The insertion arm uses `lower_bound`, not `upper_bound`.
- Brute force compares with `<`, not `<=`.

That is four different comparisons, in four different idioms, all encoding one
rule. If they all drifted the same way at once, arm agreement would never notice
— which is exactly the failure class the properties below are built for.

## The differential: an oracle for every case, and properties that relate two runs

The brute-force arm is `O(n^2)` and the bands are sized for the tree-walk
interpreter, so unlike [#313](../313-super-ugly-number/)'s trial division it is
a **complete oracle for every case**. Be exact about what that means: wherever an
arm equals the brute answer, any property that is a function of *that one
answer* is implied. P2 (bounds) and P6 (closed forms) can only localise a fault
the oracle has already detected; they are kept because a differential that only
says "A ≠ D" has not said where.

The properties that stand on their own are the ones that relate **two
invocations** — the axis a one-answer oracle never varies, and where a fault
shared by all four arms (the tie rule above) shows up:

- **P3, reversal.** An element's smaller-*after* count plus its smaller-*before*
  count (the after-count of the reversed array, read at the mirrored index) is
  the number of strictly smaller values in the whole array — an external answer
  from the sorted copy.
- **P4, negation.** Smaller-after plus *greater*-after (the after-count of the
  negated array) plus equal-after is everything to the right, `n - 1 - i`.
  Equal-after is a direct scan, so a `<` that drifted to `<=` is caught here
  regardless of which arm computed it.
- **P5, order-preserving maps.** Shifting every value by a constant, or scaling
  by a positive one, changes nothing. A rank compression that leaked the *value*
  rather than the *rank* would fail.
- **P7, tie-breaking.** Map `a[i]` to `a[i] * n + i`: equal values become
  strictly ordered with the *later* one larger, so it must still not be counted
  and the answer is unchanged. **Each arm is compared with itself** on the two
  inputs, not with arm A — an arm with the wrong tie rule is wrong on `a` and
  right on the mapped array, and that self-disagreement *names the arm*.
  Comparing with A would only repeat P1 on a second input, which is what the
  first draft of this property did (below).

Four value alphabets cover the shapes that matter: two symbols (almost all
ties), five, a thousand (few ties), and a wide negative range; plus strictly
ascending, strictly descending and all-equal closed forms. `cases 4824`.

## Mutation-tested, and the harness caught a flaw in my own property

Each arm's tie comparison and mechanism was mutated and the harness checked which
property fires (content-anchored to named function bodies, run under
`karac run`). Two semantics-preserving controls must stay silent, and do.

| mutation | fires | killed |
|---|---|---|
| ★ prefix query counts `<=` (`x = r + 1`) | P1, P3, P4, P5, P6, P7 | ✓ |
| ★ rank table left unsorted | P1, P3, P4, P5, P6, P7 | ✓ |
| ★ update skips the covering climb | P1, P3, P4, P5, P6, P7 | ✓ |
| merge: ties taken from the right | P1, P5, **P7** | ✓ |
| merge: count added once, not accumulated | P1, P5 | ✓ |
| insertion: `upper_bound` for `lower_bound` | P1, **P7** | ✓ |
| **X7: every arm counts `<=` at once** | **P3, P4, P6, P7** — P1 silent | ✓ |

**X7 is the probe the property set exists for.** Flip the strictness in all four
arms and they agree with each other perfectly; the oracle is one of them, so it
agrees too. P3, P4 and P7 catch it anyway, because they relate the answer to a
*second* invocation and to an external count — 49,231 P4 hits and 9,856 P7 hits
(4 arms × the 2,464 tie-bearing cases).

**The first draft of P7 could not do that.** It compared each arm's tie-broken
answer against *arm A's* answer, so a merge that took ties from the right —
wrong on the original, right on the tie-broken input — matched A on the
tie-broken input and P7 stayed silent; only P1 fired, and P1 cannot say which
arm. Rewriting P7 as each arm against *itself* made it fire on exactly the 2,464
cases that contain a tie, for exactly the mutated arm. The mutation harness is
what surfaced that; a differential that was never mutated would have shipped the
weaker property and reported the same green.

## Benchmarks

`build-once + punch` ([BENCHMARKS.md](../../../BENCHMARKS.md)): generate the
200,000-element array **once**, then punch 24 complete answers through it. Each
pass first swaps two elements at positions drawn from the running checksum — so
no pass is a repeat and none can be hoisted — and undoes the swap after. The ★
Fenwick arm is mirrored in all five languages: a sort and dedup for the ranks,
then per element a binary search, a prefix query and a point update. The
per-pass allocations (rank table, tree, answer) are part of the algorithm and
every mirror makes the same ones. All five print `checksum 399910461`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each. **Noisy**: σ is 8–10% on every lane in this run, wider than #314's,
so read the compiled lanes as one band — canonical Apple-silicon numbers await
an idle run ([#313's methodology note](../313-super-ugly-number/#a-methodology-note-because-the-first-version-of-this-table-was-wrong)).

| | mean | vs kara |
|---|---:|---:|
| rust (`-O`) | 724 ms ± 61 | 0.96× |
| **kara** (codegen, seq) | **751 ms ± 72** | **1.00×** |
| rust (`-O -C overflow-checks=on`, equal safety) | 770 ms ± 66 | 1.03× |
| rust (equal safety + matched ISA) | 801 ms ± 57 | 1.07× |
| c (`-O3 -march=x86-64-v3`) | 1145 ms ± 76 | 1.52× |
| c (`-O3`) | 1168 ms ± 72 | 1.56× |
| go | 1394 ms ± 55 | 1.86× |

**Kāra sits inside the Rust band** — 4% behind unchecked `rustc -O`, 3% ahead of
the equal-safety build, all within one σ. The workload is a sort of 200,000
values plus 200,000 binary searches and `O(log m)` tree walks per pass, so it is
dominated by the sort and by cache-missing gathers into `ranks` and `tree`.

**C is last among the compiled lanes, and that is C's `qsort`, not the
compiler.** The C mirror sorts with `qsort` and a comparator callback — the only
standard sort C has — which runs ~2× slower than Rust's monomorphised `sort` and
Kāra's `Vec.sort` on the same data. It is the faithful mirror (the same
algorithm, the language's own sort), and the honest reading is that this kata's
comparison is partly a comparison of sorts. Go's `sort.Slice` pays a similar
callback cost plus GC.

## Compiler findings

The arms are clean — zero `karac check` diagnostics across all six sources, all
byte-identical under `karac run`, `karac build`, the default auto-parallelising
build and `--interp`. Nothing to file: this kata's surfaces (`Vec.sort`/`dedup`,
`Vec.insert` in a hot loop, `x & -x`, index-mediated `mut ref` recursion) all
held. Two front-end rules bit the first draft and were the compiler being right:
`distinct` is a reserved word, and a single-letter `const N` is Type-class by
the naming rules, so a const needs a longer name (`LEN`).
