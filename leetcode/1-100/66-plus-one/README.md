# 66. Plus One

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Math &nbsp;·&nbsp; **Source:** [leetcode.com/problems/plus-one](https://leetcode.com/problems/plus-one/)

A non-negative integer is given as its decimal **digits**, most-significant first (`[1, 2, 3]` is 123), with no leading zeros except the single `[0]`. Add one and return the digit array of the result.

```
[1, 2, 3]     →  [1, 2, 4]        123 + 1 = 124
[4, 3, 2, 1]  →  [4, 3, 2, 2]     4321 + 1 = 4322
[9]           →  [1, 0]           9 + 1 = 10   (grows by one place)
[9, 9, 9]     →  [1, 0, 0, 0]     999 + 1 = 1000
```

**Constraints:** `1 ≤ digits.length ≤ 100`; `0 ≤ digits[i] ≤ 9`; no leading zeros except `[0]`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Reverse scan, early return** ★ — bump the first digit below 9 and stop; a 9 becomes 0 and the carry ripples left | O(n) time, O(1) extra | [`plus_one.kara`](plus_one.kara) ✓ via `karac run` / `karac build` | [`plus_one.py`](plus_one.py) ✓ |
| **Explicit carry propagation** — seed a carry of 1 and ripple it through every column, LSB-first, then reverse | O(n) time, O(n) space | [`plus_one_carry.kara`](plus_one_carry.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all twelve test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The carry, and the one case the length changes

Adding one only disturbs the tail: the carry dies the instant it meets a digit that is not 9. So the whole problem is a reverse scan with an early exit —

```
digit < 9   →  increment it, done — nothing to the left changes
digit == 9  →  it becomes 0 and the carry ripples one place left
```

The **reverse scan** ([`plus_one.kara`](plus_one.kara)) is the ★. On the common path (a trailing digit below 9) it touches exactly **one** cell and returns. The only case that scans the whole array is **all nines** (`[9, 9, 9]`): the carry falls off the left end and the result is one place **wider** — a leading 1 followed by `n` zeros (`[1, 0, 0, 0]`). That grow-by-one is the kata's entire subtlety and the reason a plain in-place bump is insufficient — the answer array is sometimes longer than the input. The ★ handles it by allocating the widened result only on that path.

The **carry-propagation** form ([`plus_one_carry.kara`](plus_one_carry.kara)) is the general-adder phrasing: seed `carry = 1` and ripple it through every column exactly as kata [#67](../67-add-binary/) adds two binary strings, here in base 10 —

```
sum = digits[i] + carry ;  out = sum % 10 ;  carry = sum / 10
```

A leftover `carry == 1` after the scan *is* the widening, pushed as the new leading digit. It always walks the whole array and builds a fresh result — strictly more work than the ★'s early return — but it is the phrasing that **generalises**: swap the seed `1` for any addend, or `% 10` for another base, and the same loop adds arbitrary values. The digits accumulate least-significant-first and are flipped to most-significant-first at the end, the same LSB-first-then-reverse discipline as [#67](../67-add-binary/) and kata [#2](../2-add-two-numbers/).

## Kāra features exercised

- **`ref Vec[i64]` input + owned `Vec[i64]` result** — the solver borrows the digit array (`digits: ref Vec[i64]`) and builds a fresh `Vec.new()` output; the ★ mid-loop `return out` when the carry stops is the idiomatic early exit, the same shape kata [#55](../55-jump-game/) and [#67](../67-add-binary/) use.
- **Length-changing output** — the all-nines path constructs a `Vec[i64]` one element longer than the input (`push(1)` then `n` zeros), the case that makes this more than an in-place mutation.
- **`% 10` / `/ 10` column arithmetic + LSB-first reverse** — the carry form's `sum % 10` / `sum / 10` and the trailing MSB-first flip, the base-10 sibling of kata [#67](../67-add-binary/)'s base-2 `% 2` / `/ 2`.
- **Nested array literals as test input** — `report([9, 9, 9], mut s)` builds the `Vec[i64]` digit arrays inline; the harness prints each result as a bracketed list plus a positional checksum `Σ (k+1)·out[k]` folded into `sums:`, the byte-for-byte diff anchor shared with katas [#54](../54-spiral-matrix/) and [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/).

**v1 note.** Digits stay in `[0, 9]` and the array length ≤ 100, so every value and every checksum fits i64 comfortably; the arithmetic is i64 for uniformity with the rest of the corpus. The ★ returns from inside the reverse-scan loop the moment the carry is absorbed — a mid-function `return` in a `while`, lowered identically under `karac run` and `karac build`.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   plus_one.kara
karac build plus_one.kara && ./plus_one

# The carry-propagation approach (identical output):
karac run plus_one_carry.kara

# Python
python3 plus_one.py

# Verify they all agree
diff <(karac run plus_one.kara) <(python3 plus_one.py)          && echo OK
diff <(karac run plus_one.kara) <(karac run plus_one_carry.kara) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`plus_one.{kara,rs,c,py}`, `go-seq/main.go`).

> ⚠️ **Machine caveat — read before comparing.** Like katas [#63](../63-unique-paths-ii/#benchmarks)/[#64](../64-minimum-path-sum/#benchmarks)'s first pass (and unlike the M5 Pro tables elsewhere in the corpus), the numbers below were measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.10 GHz, 4 vCPU, Linux 6.18.5). **Do not compare these absolute times/sizes/RSS against sibling katas' M5 tables** — different ISA, toolchains, and a noisier host; `bench/results.json` records the real host in `env.host`/`env.note`. The **within-kata cross-language ratio** is the signal, and here it lands exactly where #62/#63 did (kāra at C parity), so — unlike #64's provisional kāra-lead — there is no anomaly to confirm. Re-run `bench/bench.sh` on the M5 to fold comparable numbers into the corpus tables.

**Workload.** A single `plus_one` is O(1) amortised (the ★ returns at the first digit below 9), so one call is far too cheap to time. The honest heavy workload is the operation the kata *is*: increment a number over and over. So a fixed-width **W = 9** decimal digit buffer is driven as a base-10 **counter**, applying the ★'s reverse-scan carry **in place** K = 80,000,000 times — a build-once + punch workload (BENCHMARKS.md's preferred shape). Keeping the carry in one reused buffer (rather than the kata's per-call fresh `Vec`) measures the **carry-scan codegen** itself, not allocator throughput. `K < 10⁹`, so the counter never overflows 9 digits and the array-widening path (`[9,9,9] → [1,0,0,0]`, a once-per-power-of-ten rarity) does not fire in steady state. The sink is a rolling polynomial hash `acc = (acc*131 + digits[k % W]) % 1_000_000_007`; the **rotating** index `k % W` reads every digit over its cycle, so the carry propagation cannot be dead-code-eliminated down to `units = k % 10`. All four compiled mirrors must agree on `496509690` before timing.

**Seq-only kata**: the hash sink is a **loop-carried dependency**, so the K-loop is not a reduction karac's auto-par pass can split — the default `karac build` stays single-threaded, directly comparable to `rustc -O` / `clang -O3` / `go build` on a per-core basis.

### Runtime — seq lane

`--warmup 5 --runs 30 --shell=none`. All four single-threaded. **Cloud-container numbers — ratios, not absolutes** (see caveat).

| Implementation | Wall time |
|---|---|
| go   plus_one                       | 378.1 ± 8.6 ms |
| c    plus_one (clang -O3)           | 390.4 ± 4.6 ms |
| **kāra plus_one**                   | **392.2 ± 2.5 ms** |
| rust plus_one (rustc -O)            | 435.5 ± 12.0 ms |

**Kāra sits dead even with C** on this in-place carry scan — **within 0.5 %** (392.2 vs 390.4 ms), ~1.04× behind Go, and ~1.11× *ahead* of Rust, with the tightest variance of the four (±2.5 ms). This is the expected C-parity result and the reassuring one: it matches #62/#63's finding on the same RMW-scan family and, unlike #64's surprising container lead, needs no M5 asterisk. Kāra also pays for its default overflow checks on the `digit + 1` / `acc*131 + …` arithmetic that `rustc -O`/`clang -O3` skip, so reaching C's time here is an equal-*result* at a stricter safety posture. (Go edges ahead on this particular fixed-array counter loop, which its compiler handles well; the four are within ~15 % end to end.)

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py plus_one` (K=8M) | 930.5 ± 39.9 ms |

Python at K=8M is ~0.93 s; projecting to the compiled mirrors' K=80M (~9.3 s) puts it **~24× slower than kāra seq** — a narrower Python gap than #62's ~16.7× → #64's ~108× range would suggest, because the per-iteration body here is a very short reverse scan (usually one step) rather than an inner grid loop.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 plus_one.c          | **58.6 ± 1.5 ms** |
| rustc -O plus_one.rs          | 79.6 ± 4.0 ms |
| **karac build plus_one.kara** | **197.9 ± 46.6 ms** |

On this container karac compiles slower than both (and with high variance on the shared host); consistent with #63/#64's container runs and the reverse of #62's M5 snapshot. Small-single-file compile time is dominated by process/LLVM-init overhead that differs across the toolchain sets.

### Binary size

| Implementation | Size |
|---|---|
| c    plus_one                | 15.6 KiB |
| **kāra plus_one**            | **324.5 KiB** |
| go   plus_one                | 2.11 MiB |
| rust plus_one                | 3.77 MiB |

Kāra's seq binary is **far below Rust's 3.8 MiB and Go's 2.1 MiB**, above C's 15.6 KiB — the same 332,272 B floor as #62–64 built on this toolchain (the M5 build strips further; see #63's note).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra plus_one**            | **7.03 MiB** |
| c    plus_one                | 7.03 MiB |
| rust plus_one                | 7.03 MiB |
| go   plus_one                | 7.03 MiB |

All four sit at the same ~7.03 MiB floor on this container — the working set is a nine-element array, so peak RSS is dominated by the process/runtime base, identical across the compiled mirrors.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **karac build plus_one.kara** | **83.8 MiB** |
| clang -O3 plus_one.c          | 95.4 MiB |
| rustc -O plus_one.rs          | 100.3 MiB |

On this container karac has the lowest compile-memory footprint of the three.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, Python is the ergonomic foil. On this in-place carry scan kāra matches C and leads Rust — the clean C-parity result the RMW-scan family (#62/#63) established, reproduced here without #64's provisional asterisk. The load-bearing claim is the five-language sink agreement and that kāra reaches C's time at its stricter (overflow-checked) safety posture.
