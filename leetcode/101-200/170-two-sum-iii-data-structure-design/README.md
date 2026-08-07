# 170. Two Sum III - Data structure design

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Hash Table · Two Pointers · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/two-sum-iii-data-structure-design](https://leetcode.com/problems/two-sum-iii-data-structure-design/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Design a structure with two operations: `add(number)` inserts a number, and `find(value)` returns `true` iff **some pair** of the added numbers sums to `value`. Numbers may repeat; a value pairs with itself only if it was added at least twice.

```
add(1); add(3); add(5);
find(4) -> true   (1 + 3)
find(7) -> false
add(3);            // two 3s now
find(6) -> true   (3 + 3)
```

**Constraints:** `-10⁵ ≤ number, value ≤ 10⁵`; up to `10⁴` calls to `add` and `find`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **count map + complement scan** ★ | [`two_sum_iii.kara`](two_sum_iii.kara) ✓ | [`two_sum_iii.py`](two_sum_iii.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Store a `Map[number → count]`. `add` bumps the count (O(1)). `find(value)` scans the **distinct keys**: for key `k` the complement is `value - k`. If the complement differs from `k`, it just has to be present; if it **equals** `k` (a self-pair like `3 + 3`), the count must be at least 2. This makes `add` fast and `find` O(distinct) — the standard trade for a workload with many more adds than finds. (The mirror trade — sorted list + two pointers, O(1)-ish find, O(n) add — is the other classic answer.)

## Kāra features exercised

- **Struct + free functions, no impl blocks** — the corpus idiom: a `TwoSum { counts: Map[i64,i64] }` with `add(ds: mut ref TwoSum, …)` and `find(ds: ref TwoSum, …)`. This exercises a `Map`-field struct threaded through `mut ref` / `ref` receivers.
- **`Map` iteration** — `for k in ds.counts.keys()`, with `.get` → `Option` matched inside the loop. The `find` result is a boolean, so hash-iteration order does not affect output (deterministic across run/build).
- **Self-pair count check** — the `complement == k` branch requires `count >= 2`.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`762965`). Workload: build a 170-add sparse multiset over [0,6K) keys (~168 distinct), then 1.2M full-scan find(target) queries; sink=count of trues. NOTE: Kara/Rust/Go/Python use a hash map; C hand-rolls a direct-address count table + distinct-key list (same membership semantics)..

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-08-04 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 295.3 ms | 0.30× |
| Rust `-O` | 746.9 ms | 0.75× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 761.1 ms | 0.76× |
| **Kāra (codegen)** | 997.1 ms | 1.00× |
| Go | 1.16 s | 1.17× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac 9e8558e68059); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

> **The Kāra row above is a 2026-08-04 measurement and is now stale on the slow side.** Part of the `B-2026-08-05-5` regression it captured has since been fixed in `karac` (see the note below): the same binary measures 858–870 ms on the same host after the fix, against 986–1026 ms before it. The table is left at the recorded value deliberately — these numbers come from the `bench.sh` → `results.json` pipeline and are never hand-edited, and the remaining residual is still open, so the kata is due one re-bench once that lands rather than two.

## Running

```bash
karac run   two_sum_iii.kara
karac build two_sum_iii.kara && ./two_sum_iii
python3 two_sum_iii.py
diff <(karac run two_sum_iii.kara) <(python3 two_sum_iii.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.

**A `Map.keys()` materialisation cost — now fixed in `karac`.** [`B-2026-07-24-2`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): `for k in map.keys()` (and `.values()` / `.entries()`) eagerly built a fresh heap `Vec` of the whole key set on **every evaluation**. This kata's `find` does `for k in ds.counts.keys()` and runs 1.2M times over a ~170-entry map — 1.2M malloc + full-set-copy + free cycles — which put the Kāra row at ~1.74× the equal-safety Rust mirror, whose `keys()` is a zero-allocation inlined bucket walk. A benchmark gap rather than a correctness one, and the kind that only shows up when the iteration sits inside a hot loop rather than at the top level.

**`B-2026-08-05-5` (open, partially fixed) — Kāra's row regressed 1.29× (771.2 ms → 997.1 ms) between the 2026-07-28 and 2026-08-04 measurements**, source unchanged and sink still `762965`. The cause was found: `58412d9f` began folding a 7-bit hash tag into the map probe's occupancy test (`status == ctrl` instead of `status >= 0x80`), which lets a probe reject a bucket *without loading its key*. That trade is worth exactly what the skipped key compare would have cost — and for this kata's `Map[i64, i64]` over a ~168-entry, L1-resident table, it costs nothing to skip. Measured with a compiler flag that isolates the tag compare alone: the tag executes **12.8% fewer instructions yet burns 18.5% more cycles** (IPC 3.04 → 2.24) on Apple silicon. Fewer instructions, slower program — an instruction count is a misleading proxy here.

`karac` now drops that compare for primitive keys on arm64 and keeps it for `String` keys, where the skipped compare is a `{ptr,len,cap}` load plus a cold heap dereference and the tag genuinely pays (kata [#127](../127-word-ladder/) measures 1.07× *faster* with it). That recovers 1.14× of the 1.29×. **A ~1.10× residual remains open**, attributable to the rest of the same commit and not yet isolated.

Two methodology notes this kata paid for. Isolating any of it needs a **matched compiler+archive pair per step**: codegen and the runtime map co-evolve on a shared bucket-layout contract, so a mismatched pair silently miscompiles — during this investigation one such pair returned sink `287184` while timing "2.67× faster", which is skipped work wearing a speedup's clothes. Sink-check every candidate binary before timing it. And a *commit-to-commit* comparison is the wrong instrument for sizing a one-line codegen choice: `58412d9f` also restructured the probe emitter, so measuring the tag that way disagreed with the isolated flag by a factor of three.

The same window moved kata [#127](../127-word-ladder/) 1.24× in the *opposite* direction — which turned out to be the same mechanism with its sign flipped by key type, not a second cause.
