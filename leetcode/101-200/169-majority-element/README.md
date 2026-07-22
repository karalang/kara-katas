# 169. Majority Element

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Hash Table · Divide and Conquer · Counting · Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/majority-element](https://leetcode.com/problems/majority-element/)

Return the element that appears **more than ⌊n/2⌋ times** (guaranteed to exist).

```
[3,2,3]           ->  3
[2,2,1,1,1,2,2]   ->  2
[7]               ->  7
```

**Constraints:** `1 ≤ n ≤ 5·10⁴`, a majority element always exists. Follow-up: O(n) time, O(1) space.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Boyer-Moore voting** ★ | [`majority_element.kara`](majority_element.kara) ✓ | [`majority_element.py`](majority_element.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The **Boyer-Moore voting** algorithm hits the O(n)/O(1) follow-up target. Keep a running `candidate` and a `count`. Each element equal to the candidate is a vote for it (`+1`); each different element is a vote against (`-1`). When the count reaches 0, adopt the current element as the new candidate. Because the majority element occupies **more than half** the array, its votes can never be fully cancelled by everything else combined — so whoever is left standing at the end is the majority. One pass, two scalars.

## Kāra features exercised

- **O(1)-space scalar carry** — `candidate`/`count` threaded across a `while` scan with a loop-carried dependency (which is exactly why it can't be auto-vectorized — see the benchmark).
- **`Slice[i64]`** input from `Array[i64, N]` literals.

## Benchmarks

> **Machine.** Container-only reference run — a shared **x86-64 Linux cloud container** ([`bench/results.container-x86.json`](bench/results.container-x86.json)); canonical Apple-M5 numbers (`bench/results.json`) are pending a maintainer run. Absolute times are noisy on the shared host; **within-run cross-language ratios are the signal.**

Compute-bound, seq-only kata. **Build-once + punch**: fill `N = 10_000_000` LCG values with a 60% majority, then run the Boyer-Moore scan `K = 20` times, perturbing one element each round so the pure function can't be hoisted. All five mirrors print the same sink (`140`). The scan's candidate/count dependency chain makes it a genuine **sequential arithmetic-and-branch** kernel — the opposite regime from [#164](../164-maximum-gap/)'s allocation-bound bucket sort.

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc, clang, go, karac
./bench/bench.sh
```

### Equal-safety: ahead of `rust_ovf`; the check tax vs wrapping C

Container snapshot, hyperfine `--warmup 5 --runs 30`:

| Run | Mean ± σ | vs kāra |
|---|---|---|
| rust `majority_element` (`-O`, wrapping) | 452.6 ± 47.3 ms | 2.61× ahead |
| c `majority_element` (`clang -O3`) | 480.8 ± 31.8 ms | 2.45× ahead |
| go `majority_element` | 551.9 ± 140 ms | 2.14× ahead |
| **kāra `majority_element` (codegen)** | **1.180 ± 0.029 s** | — |
| rust `majority_element` (`overflow-checks=on`) | 1.278 ± 0.030 s | **kāra 1.08× ahead** |
| python `majority_element` | 13.81 ± 0.70 s | (scale only; 3 runs) |

The honest comparison is at **equal safety**. Kāra bounds-checks every `nums[i]` and overflow-checks the `count ± 1` updates by default; `rustc -O` and `clang -O3` do neither. Matching Kāra's overflow safety with `-C overflow-checks=on` moves Rust to **1.278 s** — and against *that* lane **Kāra is ahead** (1.180 vs 1.278). Against wrapping C/Rust (~470 ms) Kāra pays roughly **2.5×** — the price of bounds + overflow checks on a kernel whose entire body is one compare, one branch, and one add per element, where those checks are a large fraction of the work and the wrapping frontends' loop can be transformed more aggressively.

This is the mirror image of [#164](../164-maximum-gap/), where the same compiler is *fastest* because that kernel is allocation-bound rather than check-bound. Two katas, two regimes, one honest safety story.

## Running

```bash
karac run   majority_element.kara
karac build majority_element.kara && ./majority_element
python3 majority_element.py
diff <(karac run majority_element.kara) <(python3 majority_element.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean.
