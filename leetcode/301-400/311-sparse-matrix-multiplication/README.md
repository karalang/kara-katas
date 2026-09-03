# 311. Sparse Matrix Multiplication

Multiply two matrices that are mostly zeros. The product is defined exactly as
always —

```
C[i][j] = SUM over k of A[i][k] * B[k][j]
```

— so the problem is not *what* to compute but *how much of it to skip*.

```
A = [[ 1, 0, 0],        B = [[7, 0, 0],
     [-1, 0, 3]]             [0, 0, 0],       ->  [[ 7, 0, 0],
                             [0, 0, 1]]            [-7, 0, 3]]
```

## Approaches

| file | mechanism | skips A's zeros | skips B's zeros |
|---|---|---|---|
| `sparse_matrix_multiply.kara` ★ | loops reordered `(i,k,j)`, zero test hoisted out of `j` | ✅ by testing | — |
| `sparse_matrix_multiply_csr.kara` | A compressed to CSR, B dense | ✅ structurally | — |
| `sparse_matrix_multiply_both.kara` | both operands compressed | ✅ | ✅ |
| `sparse_matrix_multiply_naive.kara` | the definition, `(i,j,k)` | — | — |
| `differential.kara` | 3,000 cases across every shape and density, seven properties | — | — |
| `bench/spmm.kara` | two 320×320 matrices at 4% density × 620 multiplications | — | — |

## The mechanism

The naive triple loop asks "is this term zero?" once per `(i, j, k)` — `m·n·k`
questions. But `A[i][k]` does not depend on `j`, so a single zero in A kills an
**entire inner loop**. Reordering `(i,j,k)` → `(i,k,j)` lets the test move up a
level:

```kara
for i in 0..m {
    for k in 0..k_dim {
        let av = a[i][k];
        if av != 0 {                     // tested m*k times, not m*n*k
            for j in 0..n {
                c[i][j] += av * b[k][j];
            }
        }
    }
}
```

The arithmetic is identical and the answer is identical; only the order of
accumulation into `C[i][j]` changes, and addition does not care.

**The reordering pays twice**, and the second time is easy to miss. The obvious
win is skipping work proportional to A's zeros. The subtler one is that the
inner loop now walks `B[k]` along a **row** — consecutive memory — where the
naive order strides down a column. On a fully dense input, where nothing is
skipped at all, the reordered arm is still faster for that reason alone.

## The optimisation is invisible to every correctness test

This is the unusual thing about this kata, and it is worth stating before the
properties.

Delete the `if av != 0` guard entirely and **every answer is byte-identical**.
All four arms still agree; all seven properties still pass; the differential
reports OK across 3,000 cases. Revert the loop order from `(i,k,j)` back to
`(i,j,k)` — the change that makes the test useless — and the output is again
identical.

Both were run as mutations. Both survive. They are in the table below as
controls, because a mutation battery that flagged them would be flagging
*edits*, not faults.

What does detect the optimisation is the clock. On a 4%-dense 260×260 pair, with
byte-identical output either way:

| | mean |
|---|---:|
| zero test present | **6.0 ms ± 0.5** |
| zero test removed | 64.2 ms ± 2.1 |

**10.7× ± 1.0.** So for this kata the benchmark is not a report *on* the
implementation — it is the only test *of* the thing being implemented.

## Properties, not just agreement

| # | property | what it pins down |
|---|---|---|
| P1 | four arms, one answer | the algorithm, from four directions |
| P2 | `A × I = A` and `I × A = A` | the identity |
| P3 | `A × 0 = 0` and `0 × A = 0` | annihilation |
| P4 | `A(B + C) = AB + AC` | **distributivity — no arm computes this** |
| P5 | `(AB)C = A(BC)` | **associativity — no arm computes this** |
| P6 | `(sA)B = s(AB)` | scaling passes through |
| P7 | `(AB)ᵀ = BᵀAᵀ` | **the transpose law — no arm computes this** |

```
cases 3000
P1..P7 all 0
DIFFERENTIAL OK
```

Matrix multiplication is not merely a function to be checked pointwise — it
satisfies an **algebra**, and none of these arms knows that. P4, P5 and P7 each
relate *separate invocations* to one another, so they catch a fault symmetric
across every arm, which is the failure mode four-way agreement is blind to.
**Associativity is the strongest**: it constrains two entirely different
bracketings of three matrices, and nothing in any arm is trying to make them
equal.

**Arm D is the one that skips nothing**, which is why it earns its `O(m·n·k)`.
The other three all rest on the same claim — omitting terms where a factor is
zero cannot change the sum. The claim is true, but all three depend on it the
same way, so a misapplication could make them wrong *together* and still agree.

### One case deliberately excluded

Every dimension in the differential is at least 1. A zero **inner** dimension
makes the product's shape unrecoverable from the operands: a `2×0` times a `0×3`
is mathematically a `2×3` of zeros, but an empty B is literally `0×0` and
carries no record that `n = 3`. Verified directly rather than assumed. It is
excluded as ill-posed rather than papered over with a convention the statement
never states.

## Mutation-tested, because a differential that cannot fail is decoration

| # | mutation | caught by |
|---|---|---|
| M2 | B indexed transposed, `b[j][k]` | **bounds panic** (silently wrong if square) |
| M3 | accumulates into `c[j][i]` | **bounds panic** |
| M4 | CSR row end reads `offsets[i]`, not `[i+1]` | P1 |
| M5 | output column taken from A's index, not B's | **bounds panic** |
| M6 | naive term transposed | **bounds panic** |
| M1 | **control** — the zero test removed entirely | *(correctly survives — 10.7× slower, identical output)* |
| — | **control** — loop order reverted to `(i,j,k)` | *(correctly survives — identical output)* |

**The panics are the non-square shapes doing the work.** Verified directly: on
*square* matrices a transposed index stays in bounds and is silently wrong
(summing 282 where 276 was right at n=3, 1170 where 1080 at n=5). The
differential varies `m`, `k` and `n` independently from 1 to 5, so most cases
are non-square and the fault becomes a crash instead of a plausible number.
Same lesson [#308](../308-range-sum-query-2d-mutable/) recorded, arrived at from
the other direction.

## Benchmarks

Build two 320×320 matrices at ~4% density once in flat row-major; then punch
620 zero-skipping multiplications, `build-once + punch`
([BENCHMARKS.md](../../../BENCHMARKS.md)). All five languages print
`checksum 1073595789`.

**Each pass perturbs one entry of A from the running checksum** — the product is
a pure function of its operands, so 620 identical multiplications of unchanging
inputs are exactly what an optimiser may hoist and run once.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 346.4 ms | 0.56× |
| c (`-O3`) | 514.5 ms | 0.83× |
| rust (`-O`) | 592.7 ms | 0.96× |
| **kara** (codegen, seq) | **616.4 ms** | **1.00×** |
| rust (equal safety + matched ISA) | 720.9 ms | 1.17× |
| go | 786.5 ms | 1.28× |
| rust (`-O -C overflow-checks=on`, equal safety) | 852.1 ms | 1.38× |
| python | 56.222 s | 91.2× |

Kāra ties plain `rustc -O` (within 4%) and is comfortably ahead of Go (1.28×)
and of **both** equal-safety Rust builds — 1.38× against `-C overflow-checks=on`,
its largest such margin in this range.

**The interesting column is the ISA one.** `c -O3` to `c -O3 -march=x86-64-v3`
is a **1.49× jump** — far larger than the 1–3% that flag usually buys in this
corpus. That is not noise and it is not mysterious: the inner loop is a textbook
AXPY,

```
c[arow + j] += av * b[brow + j]
```

a unit-stride multiply-accumulate over contiguous `i64`, which is the single
most vectorisable shape a loop can have. Given AVX2, clang takes it.

Kāra shows no comparable gain, so on this workload it is leaving a real
vectorisation win on the table — and the gap to matched-ISA C (1.78×) is
substantially wider than the gap to plain C (1.20×). The obvious suspect is the
pair of bounds checks in that loop body blocking the vectoriser, but **that is a
suspect and not a finding**: this lane has no kāra-side ISA variant to compare
against and no way to disable the checks, so nothing here distinguishes "cannot
vectorise" from "vectorises but is limited by something else." Recorded as
measured, on the same footing as
[#310](../310-minimum-height-trees/)'s unexplained *win* over clang.

The flat row-major layout is a mirror-parity requirement rather than the kata's
preference; [#308](../308-range-sum-query-2d-mutable/) measured nested
`Vec[Vec[i64]]` beating flat by 1.59× in kāra on a different workload, and the
same caveat applies.

## Compiler findings

The arms are clean — zero `karac check` diagnostics across all six sources, all
byte-identical under `karac run`, `karac build` and the default
auto-parallelising build.

**No compiler defect surfaced.** Probed before shipping, targeting the sparse
representations these four arms happen not to use:

- **`Map[(i64, i64), i64]` — a tuple-keyed coordinate map**, the third classical
  sparse form after dense and CSR, and one the corpus had not touched. Clean:
  insert, overwrite, keyed lookup on a tuple key, `contains_key` on an absent
  key, and `len` all behave. (Never walked, so no iteration-order exposure.)
- **Struct-of-arrays CSR as a `struct`** with `ref self` accessors, rather than
  the three loose `Vec`s arm B uses — clean.
- **Returning two `Vec`s as a tuple** — what `compress` would do idiomatically
  instead of arm C's trick of packing three rows into one `Vec[Vec[i64]]`.
  Clean.

The third of those is worth noting as a code-quality remark rather than a
compiler one: arm C packs `offsets`, `cols` and `vals` into a
`Vec[Vec[i64]]` and indexes them as `ca[0]`, `ca[1]`, `ca[2]`. A tuple return
compiles fine and would read better. The arm keeps its shape because that is
what it was written as and it is exercised by the differential as written, but
the probe records that the nicer spelling was available.

## Running it

```bash
karac run sparse_matrix_multiply.kara        # ★ reordered loops, zero test hoisted
karac run sparse_matrix_multiply_csr.kara    # A compressed to CSR
karac run sparse_matrix_multiply_both.kara   # both operands compressed
karac run sparse_matrix_multiply_naive.kara  # the definition
karac run differential.kara                  # 3,000 cases, seven properties

bash bench/bench.sh                          # cross-language lane
```
