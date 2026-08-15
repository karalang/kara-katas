# 247. Strobogrammatic Number II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Recursion · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/strobogrammatic-number-ii](https://leetcode.com/problems/strobogrammatic-number-ii/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Return **every** strobogrammatic number of length `n` — the generation problem behind [#246](../246-strobogrammatic-number/)'s recognition problem.

```
n = 1  ->  0 1 8
n = 2  ->  11 69 88 96
n = 3  ->  101 609 808 906 111 619 818 916 181 689 888 986
```

**Constraints:** `1 ≤ n ≤ 14`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| recursive build from the middle outward ★ | O(output) | [`strobogrammatic_ii.kara`](strobogrammatic_ii.kara) ✓ | [`strobogrammatic_ii.py`](strobogrammatic_ii.py) ✓ |

`✓` marks agreement under **interpreter**, **JIT**, and **codegen** — default auto-par build and `KARAC_AUTO_PAR=0` alike.

## The mechanism

**Build from the middle outward, not left to right.** A strobogrammatic number of length `k` is a legal outer pair wrapped around a strobogrammatic number of length `k-2`, so the recursion bottoms out **twice**:

```
k == 0  ->  [""]            even lengths
k == 1  ->  ["0","1","8"]   odd lengths — the digits that survive rotating IN PLACE
```

That second base case is the same fact #246 leans on from the other side: an odd-length number's centre pairs with *itself*, so only `0`, `1` and `8` may sit there. Recognition and generation are two views of one constraint.

Every other level wraps each inner result in each of the five pairs `0/0 1/1 6/9 8/8 9/6`.

**The leading zero is the whole wrinkle.** `"0"` wrapped in a `0/0` pair gives `"000"`, which is not a number of length 3. So the **outermost** layer — and only that one — refuses the `0/0` pair, which is why `n` is threaded through the recursion beside `k`: the recursion has to know whether it is at the outside. `n == 1` is exempt, because `"0"` alone *is* a valid answer, and that falls out for free since the `k == 1` base case never consults `n`.

Counts run **3, 4, 12, 20, 60, 100, 300** for n=1..7 — each added pair multiplies by 5 at inner layers, by 4 at the outermost where `0/0` is barred.

## What it found

**No compiler bugs.** Two independent checks, not one:

- **`valid == count` at every n**, in both mirrors. Every generated number is re-tested with #246's two-pointer predicate, which re-derives the property from the string instead of trusting how it was built. A generator that emitted something illegal would show `valid < count`.
- **Generator == brute force** for n≤5 — `python3 strobogrammatic_ii.py --verify` enumerates all n-digit candidates, filters them through the same predicate, and compares as sets. Construction versus enumerate-and-filter are genuinely different algorithms, and this catches the errors the first check cannot: a generator that *omits* valid numbers, or admits a leading zero. It is Python-only because brute force needs zero-padded integer formatting; the `valid` check is the half both languages run.

This is the third clean kata in a row, which is the honest headline. The shapes here — recursion returning `Vec[String]`, `String` concatenation via `push_str`, nested `while` over a `Vec[String]` — are well covered by the corpus.

## Kāra features exercised

- **Recursion returning `Vec[String]`** — each level allocates a fresh vector and consumes the level below, the main new surface relative to #246.
- **Two base cases in one function**, dispatching on `k == 0` and `k == 1`, with early `return` of a locally built `Vec`.
- **A parameter threaded purely for context** (`n` alongside `k`) to make the outermost layer distinguishable — no accumulator, no mutable state.
- **`String` building by `push_str`** of a borrowed `Vec[String]` element, plus `push(char)` for the separator in `join_all`.
- **`num.bytes()[i]` byte indexing** in the validity re-check, carried over from #246, where Kāra refuses `s[i]` outright.

## Reading the benchmark table

Two caveats attach to the generated table below. It is regenerated from
`bench/results.json` by `scripts/inject-bench-readme.py`, so notes belong here,
outside its span, rather than inside it.

**The Go row is not a sequential measurement.** Go runs this kata at **126% CPU**
— 370 ms of user time against 315 ms of wall — because its garbage collector is
concurrent. Every other lane sits at 99%. Go's wall-clock row therefore buys its
position with a second core and is not comparable within the sequential lane; on
user-CPU it is the slowest of the four compiled lanes, not the third fastest.

**Kāra is last here, and the gap is real.** 337.6 ms against C's 255.7 ms is
**1.32×**, essentially unchanged from the container's 1.35× — this is a
per-allocation kata (312,500 strings built per round) and it does not compress on
the M5 the way the per-access katas next door do. The x86 corroboration run is in
[`bench/results.container-x86.json`](bench/results.container-x86.json); it ranks
the five languages `c < rust < rust_ovf < kara < go`, which differs from the M5
order only by Go's GC-assisted move past Kāra.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`404314354`). Workload: generate every strobogrammatic number of length 16 (312,500 strings) and re-verify each by the two-pointer rotation check, 12 rounds; sink = checksum over every generated string.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-08-15 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 255.7 ms | 0.76× |
| Rust `-O` | 309.0 ms | 0.92× |
| Go | 315.4 ms | 0.93× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 321.7 ms | 0.95× |
| **Kāra (codegen)** | 337.6 ms | 1.00× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac 28878bc2f2ae); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   strobogrammatic_ii.kara
karac build strobogrammatic_ii.kara && ./strobogrammatic_ii
python3 strobogrammatic_ii.py

diff <(karac run strobogrammatic_ii.kara) <(python3 strobogrammatic_ii.py) && echo OK
python3 strobogrammatic_ii.py --verify     # generator vs brute force, n<=5
```

## Notes

Verified byte-identical under `karac run --interp`, `karac run`, and `karac build` — including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

**Benchmark: `bench/`.** Generates every strobogrammatic number of length 16 (312,500 strings), re-verifies each by the two-pointer rotation check, 12 rounds. Sink `404314354`, reproduced exactly by the C, Rust, Go and Python mirrors.

This lane previously read "no benchmark", on the grounds that the runtime is dominated by allocating and concatenating output and so would measure each language's string allocator rather than the algorithm. **That objection is correct and the lane is kept anyway**, because string building *is* what this algorithm does — the middle-outward recursion has no other cost — and measuring it on identical work across five languages is a legitimate comparison, not a confound. What the section must not do is imply the number says something about the strobogrammatic construction specifically; it says something about string throughput under that construction.

Which turned out to be the point. On the x86 corroboration host Kāra runs **793 ms against `rustc -O`'s 681 and equal-safety Rust's 716** — 1.17× and 1.11×. That independently reproduces the residual the compiler README already tracks ("a few string-building loops, ~1.2×"), on a workload chosen for a different reason. A lane that surfaces a known gap earns its place; recognition ([#246](../246-strobogrammatic-number/)) still carries the two-pointer-scan measurement for the pair.

**The M5 lane reproduces it a third time**: 337.6 ms against `rustc -O`'s 309.0 and equal-safety Rust's 321.7 — **1.09× and 1.05×**, narrower than x86's 1.17×/1.11× but the same sign on a different ISA and allocator. Two hosts agreeing on a ~1.1× string-building residual is worth more than either measurement alone. `bench/results.container-x86.json` holds the x86 run; it is corroboration only (BENCHMARKS.md § Hosts).
