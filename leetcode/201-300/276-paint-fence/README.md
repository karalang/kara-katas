# 276. Paint Fence

`n` posts, `k` colours. **No three consecutive posts may share a colour** — two
in a row is fine. Return how many ways the fence can be painted.

```
n=1 k=5  ->  5
n=2 k=2  ->  4        every two-post painting is legal
n=3 k=2  ->  6        the two all-same paintings are out
n=4 k=3  ->  66
n=10 k=3 ->  27408
n=20 k=2 ->  21892    at k=2 the sequence is Fibonacci doubled
```

**Constraints:** `1 ≤ n ≤ 50`, `1 ≤ k ≤ 10⁵`, and — the part LeetCode states and
this kata does not paper over — the testcases are chosen so the answer fits in 32
bits.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `paint_fence.kara` ★ | two rolling states, `same` and `diff` | O(n), O(1) space |
| `paint_fence_recurrence.kara` | the same recurrence with a variable eliminated | O(n), O(1) space |
| `paint_fence_brute.kara` | enumerate every painting, reject three-in-a-row | O(k·kⁿ) |
| `differential.kara` | 474 `(n, k)` pairs, 75 checked against the definition | — |
| `bench/paint_enum.kara` | the enumerator at n=13, k=4, split 16 ways | benchmark lane |

## One bit of history is enough

The rule looks at a window of three, but carrying the last two colours is
unnecessary — all that matters about the previous post is **whether it matched
the one before it**. That bit splits every valid painting into two classes:

```kara
same[i] = diff[i-1]                          // repeating is only legal after a change
diff[i] = (same[i-1] + diff[i-1]) * (k - 1)  // any painting, extended differently
```

and the three-in-a-row rule is never re-checked — it is enforced entirely by
`same[i] = diff[i-1]` refusing to chain.

**The base cases are where this goes wrong.** `same[2] = k` and
`diff[2] = k·(k−1)`, which sum to `k²`: every painting of two posts is legal,
because the rule needs three. A solver that starts the roll at 2, or seeds
`same[1] = k`, is right for `n = 1` and wrong from `n = 3` on.

## Eliminating the states moves the mistakes

Add the two classes together once and they disappear:

```
total[i] = diff[i-1] + total[i-1]·(k-1)
         = (total[i-1] + total[i-2])·(k-1)
```

A two-term linear recurrence — Fibonacci's shape, scaled by `k−1`. The second
solver is not a rewrite of the first; it is the first with a variable eliminated,
and **eliminating it moves where the mistakes live**. The ★ version can seed
`same` and `diff` wrongly while the loop is right; this one has no states to
seed but must get `total[2] = k²` — not `k·(k−1)` — and must start at 3. Two
different off-by-one surfaces, one answer.

## Which is exactly why the third solver is the definition

Both DP solvers are the same derivation at different stages. They share the
`total[2] = k²` fact and the "the rule needs three posts" reading, so a
misunderstanding of the **rule** — as opposed to an off-by-one in a loop — would
leave them agreeing confidently on a wrong count.

`paint_fence_brute.kara` walks all `kⁿ` assignments and rejects three-in-a-row.
Hopeless past a dozen posts, and that is fine: it is the problem statement,
compiled.

## What the injected bugs did

| injection | mismatches | brute-force disagreements |
|---|---:|---:|
| two-state: `same[i] = same[i-1]` (lets three chain) | 431 | 51 |
| recurrence: `total[2] = k(k−1)` instead of `k²` | 255 | 0 |
| two-state: swap the `same`/`diff` seeds | 139 | 42 |
| two-state: start the roll at 2 | *overflow trap* | — |
| recurrence: multiply by `k` instead of `k−1` | *overflow trap* | — |
| brute force: reject only **four** in a row | 0 | 52 |
| **both DP solvers misread the rule** | **0** | **63** |

The last row is the one this kata exists for. The two DP solvers agree
**perfectly** — cross-checking reports nothing — and the definition catches all
63. That is [#272](../272-closest-binary-search-tree-value-ii/)'s finding and
[#275](../275-h-index-ii/)'s in a third setting.

Row six is the same argument run backwards: break the *oracle* instead, and the
two DP solvers catch it. Neither side is privileged; they are independent.

**Two injections trap instead of answering**, which is worth its own note. Both
make the recurrence grow faster than the real one, so they leave `i64` inside an
envelope the generator computed for the *correct* recurrence — and Kāra's
default overflow checking turns what would be a silently wrapped wrong answer in
C or Rust into a located panic. A wrong algorithm caught by arithmetic rather
than by the oracle.

## The generator has to know where the arithmetic stops fitting

The answer grows like `(k−1)ⁿ`, so at `k = 100000` it leaves `i64` **before
n = 5**. Kāra traps; C and Rust wrap and print garbage without complaint.

So the harness computes its own envelope — `max_safe_n` walks the same recurrence
with a guard *before* each multiply, because checking afterwards is checking a
value that has already trapped — and draws every case inside it:

```
cases 474
of which checked against the DEFINITION (brute force) 75
largest n reached, all k (k=1 never grows, so it runs to the walk cap) 200
envelope at k=2 89, at k=100000 3
brute-force disagreements 0
digest 338090785
mismatches 0
```

`n = 89` at `k = 2` against `n = 3` at `k = 100000` is the whole story of this
problem's arithmetic in two numbers. LeetCode's `n ≤ 50` sits inside the envelope
for every `k` it allows, which is what its 32-bit promise is really saying.

The Python mirror cannot reproduce the envelope by overflowing — its integers are
arbitrary-precision — so it computes the same bound the same way, against the
same explicit limit. The envelope is arithmetic the harness performs, not a
property of the host's integer type, which is what lets the two agree exactly.

## Two compiler bugs this kata found

`B-2026-08-15-20` — **the interpreter blames an integer overflow on a
sub-expression that cannot overflow.** In `let c = (a + b) * m` with `a + b == 3`,
the trap is reported at the column of `a`; the compiled backends point elsewhere
on the same line. The message text is right everywhere and all four surfaces exit
1 — but `karac run` and `karac build` give two different answers to *where*, and
the interpreter's is provably not the culprit. Filed low: no wrong answer, and
the fault is detected. It still costs the first thing anyone does with a panic.

`B-2026-08-15-23` — **the collect-tabulate lowering reports `fanned_out: true,
"dispatched across the worker pool"` and runs entirely on one thread.** Every
`#[par_order_free]` loop whose body pushes *unconditionally* — the natural
parallel-map idiom — is sequential. Wrapping the identical push in a tautological
`if` restores a 3.5× speedup, and both surfaces report the fan-out identically
either way. Found by this kata's par lane measuring 1.02× against its own
sequential twin. Filed **high**: see § Benchmarks for what it costs.

## Kāra features exercised

- **`Vec[Vec[i64]]` literals** as a case table, indexed twice (`cases[i][0i64]`).
- **Default integer-overflow checking**, as a load-bearing part of the kata
  rather than a footnote — see the two trapping injections.
- **A `while` odometer with carry** over base-`k` digits — the brute-force
  enumerator, mutating its array in place.
- **`i64` bounds arithmetic** — `9223372036854775807i64` as a literal, and
  division-before-multiply guards.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

## Running

```bash
karac run paint_fence.kara
karac run paint_fence_recurrence.kara
karac run paint_fence_brute.kara

diff <(karac run paint_fence.kara) <(python3 paint_fence.py) && echo OK

# 474 (n, k) pairs, 75 of them against brute-force enumeration
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in paint_fence paint_fence_recurrence paint_fence_brute differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

## Benchmarks

The **DP is not the workload.** It is O(n) and `n` cannot exceed 89 before the
answer leaves `i64` — ninety iterations of four arithmetic ops. Benching it would
have meant inventing a modular variant, which is a different problem wearing this
kata's name.

The **enumerator** is a real one: `n = 13, k = 4` is 67 million paintings and
~800 million comparisons, branch-heavy and entirely data-dependent. And the sink
is the answer, so the bench verifies itself — the printed total must equal
`num_ways(13, 4) = 36884484`, which every lane produces. A lane that optimized
away half the search would say so immediately.

4-core x86 container, hyperfine, 10 runs. Full caveats in
[BENCHMARKS.md](../../../BENCHMARKS.md).

| lane | time | vs C |
|---|---:|---:|
| `clang -O3` | 362.3 ms ± 8.6 | 1.00× |
| `clang -O3 -march=x86-64-v3` | 371.8 ms ± 17.9 | 1.03× |
| `rustc -O` | 397.0 ms ± 9.6 | 1.10× |
| **`rustc -O -C overflow-checks=on`** (equal safety) | **421.6 ms ± 15.4** | **1.16×** |
| **`karac build`** | **459.7 ms ± 11.6** | **1.27×** |
| `go build` | 1045 ms ± 13 | 2.89× |

Against the equal-safety comparator — Rust with overflow checks on, matching
Kāra's default-checked arithmetic — Kāra is **1.09×**. Against Go, 2.3× faster.

### The parallel lane, and what it is currently worth

The enumeration splits on the first two posts into 16 wholly independent
branches. The lane is recognized: `parallel_reduction { op: collect }`, and
`karac query concurrency` reports `fanned_out: true`.

It does not fan out.

| | time | cpu |
|---|---:|---:|
| `paint_enum_seq.kara` (no attribute) | 470.0 ms ± 6.0 | 100% |
| `paint_enum.kara` (`#[par_order_free]`) | 459.5 ms ± 7.2 | 100% |
| | **1.02× ± 0.02** | |

The cause is `B-2026-08-15-23`: the collect-*tabulate* lowering — selected for a
body that pushes exactly once, unconditionally — never dispatches, while
reporting that it did. `bench/probe/paint_enum_guarded.kara` measures the gap by
wrapping the identical push in an always-true guard:

| | time | cpu |
|---|---:|---:|
| par as written (unconditional push) | 457.9 ms ± 6.7 | 100% |
| par + tautological `if pre >= 0i64` | 130.4 ms ± 4.7 | **391%** |
| | **3.51× ± 0.14** | |

Same logic, same sink, one always-true guard between them. **The guarded build
beats sequential `clang -O3` by 2.8×** — that is what the bug is holding back.

The shipped lane stays in its natural unconditional form and publishes 1.02×.
Adopting the guard would manufacture a good row by routing around a compiler gap,
which is the one thing a kata must not do; the probe exists to size the gap, not
to hide it.
