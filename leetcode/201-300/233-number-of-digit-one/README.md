# 233. Number of Digit One

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Math · Recursion / Digit Counting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/number-of-digit-one](https://leetcode.com/problems/number-of-digit-one/)

Count the total number of times the digit `1` appears across **all** non-negative integers from `0` to `n`.

```
n=13   ->  6     (1, 10, 11, 12, 13 contribute 1+1+2+1+1)
n=0    ->  0
n=100  ->  21
```

**Constraints:** `0 ≤ n ≤ 10⁹`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **per-position counting** ★ | [`number_of_digit_one.kara`](number_of_digit_one.kara) | [`number_of_digit_one.py`](number_of_digit_one.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Enumerating every number is O(n); counting per **digit position** is O(log n). For each place value `pos` (1, 10, 100, …), split `n` into the digits above, at, and below that position:

```
high = n / (pos*10)     cur = (n / pos) % 10     low = n % pos
```

Then the number of `1`s contributed *at this position* over `0..n` is:

- `cur == 0` → `high * pos` — only the fully-completed high cycles put a 1 here;
- `cur == 1` → `high * pos + low + 1` — plus one partial cycle covering `0..low`;
- `cur ≥ 2` → `(high + 1) * pos` — this digit's whole block of 1s is fully covered.

Summing that over every position gives the answer. Place values climb by `×10` until they exceed `n`; `pos*10` reaches at most 10¹⁰, comfortably inside `i64`, so Kāra's overflow-checked arithmetic never trips.

## Kāra features exercised

- **Pure integer digit arithmetic** — `/`, `%`, and a climbing `pos` power of ten, all overflow-checked `i64`; the three-way `cur` branch is the whole kernel.
- **O(log n) loop** — one iteration per decimal position rather than per integer.

## Benchmarks

One call is O(log n) — trivial — so [`bench/`](bench/) turns the kernel into a
**division-throughput** workload: sum `count_digit_one(i)` over `i` in `0..6M`.
Each call runs ~log₁₀(i) iterations of **variable-divisor** integer `/` and `%`
plus a data-dependent 3-way branch (`cur` 0 / 1 / ≥2), so the loop does **not**
vectorize (hardware `idiv`, unpredictable branch) and allocates nothing — a clean
scalar division + branch bench. All five mirrors share the algorithm and agree on
the sink (`15533335400000`).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-02, karac g6697158fa (0.9.0-dev.14057, the v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 55.6 ± 1.9 ms | 0.95× |
| **Kāra (codegen)** | **58.2 ± 3.4 ms** | **1.00×** |
| Rust `-O` | 58.7 ± 1.9 ms | 1.01× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 60.5 ± 8.0 ms | 1.04× |
| Go | 76.7 ± 1.4 ms | 1.32× |
| Python (scale lane) | 8 902 ms | last measured on the x86 container (undated snapshot), not re-run |

On this division-bound scalar kernel Kāra lands **effectively tied with `rustc
-O`** (0.99× of its time) and **ahead of overflow-checked Rust** (0.96×) — the
honest equal-safety comparison, since Kāra checks integer overflow by default. It
trails C by ~5% and beats Go by 1.32×. (Contrast the memory-bound DP in
[#221](../221-maximal-square/), where the field compresses; a pure-ALU division
kernel is where codegen quality shows.)

Against the 2026-07-28 M5 run (karac 0.1.0, legacy backend) the ranking is
unchanged and the language ratios are flat: Kāra/Rust `-O` 1.00× → 0.99×,
Kāra/equal-safety Rust 1.00× → 0.96×, Kāra/C 1.06× → 1.05×, Kāra/Go 0.75× →
0.76×. Every comparator also ran ~16–21% slower in absolute terms this session
(machine state), so compare the ratios, not the milliseconds.

Binary size: C 33,432 B · **Kāra 302,872 B** · Rust 466,280 B · Go 2,492,514 B.
Every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as
[`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

> **History.** An earlier, undated x86 container snapshot put Kāra at 351.5 ms:
> C 318.7 ms (0.91×), Rust `-O` 346.8 ms (0.99×), equal-safety Rust 357.9 ms
> (1.02×), Go 829.3 ms (2.36×), Python 8 902 ms (25.3×); binary size there was
> C 16 KB · Kāra 374 KB · Go 2.2 MB · Rust 4.0 MB. The container feed
> ([`bench/results.container-x86.json`](bench/results.container-x86.json)) has
> since been re-measured (2026-10-30); neither is the M5 result above.

Single-machine snapshot (`bench/results.json`, karac g6697158fa); see
[`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with
`bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   number_of_digit_one.kara
karac build number_of_digit_one.kara && ./number_of_digit_one
python3 number_of_digit_one.py
diff <(karac run number_of_digit_one.kara) <(python3 number_of_digit_one.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Benchmarked: see § Benchmarks.
