# 246. Strobogrammatic Number

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Hash Table · Two Pointers · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/strobogrammatic-number](https://leetcode.com/problems/strobogrammatic-number/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

A number is **strobogrammatic** if it reads the same after rotating the page 180°.

```
"69"   ->  true      rotate: 6 becomes 9, 9 becomes 6, order flips  ->  "69"
"88"   ->  true
"962"  ->  false     2 is not legible upside down
```

**Constraints:** `1 ≤ num.length ≤ 50`; digits only; `num` has no leading zeros except `"0"` itself.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| two pointers, `rot(num[lo]) == num[hi]` ★ | O(n) time, O(1) space | [`strobogrammatic.kara`](strobogrammatic.kara) ✓ | [`strobogrammatic.py`](strobogrammatic.py) ✓ |
| build the rotated string, compare | O(n) time, O(n) space | [`strobogrammatic_rotate.kara`](strobogrammatic_rotate.kara) ✓ | — |

`✓` marks agreement with the Python mirror under **interpreter** (`karac run --interp`), **JIT** (`karac run`), and **codegen** (`karac build`), under the default auto-parallelising build and `KARAC_AUTO_PAR=0` alike — on the 26 spec cases below *and* on 6,000 randomized cases (see § What it found).

## The mechanism

**Rotation does two things at once, and the whole problem is remembering the second.** Each digit turns into another digit, *and* the string reverses. Only five digits survive the first half:

```
0 -> 0     1 -> 1     8 -> 8     6 -> 9     9 -> 6
```

`2 3 4 5 7` become nothing legible, so one occurrence anywhere is fatal — no pairing argument needed, the answer is `false` on sight.

Get the reversal wrong and you have written a *different, easier* problem: "are all digits individually rotatable?". That version accepts `"6996"`, which is wrong — rotating it gives `"6996"` → map → `"9669"` → reverse → `"9669"` ≠ `"6996"`. Both `"6996"` (false) and `"6009"` (true) are in the test set precisely because they differ only in that check.

The **two-pointer** form closes in from the ends and asks `rot(num[lo]) == num[hi]`. The loop condition is `lo <= hi`, not `lo < hi`, and that single character carries real weight: on an odd-length number the centre pairs with **itself**, which is exactly what forbids 6 and 9 in the middle — `rot('6')` is `'9'`, and `'9' != '6'`. A `lo < hi` loop skips the centre and wrongly accepts `"696"`. `"689"` (true, centre 8) and `"69896"` (false, would pass a centre-skipping check) are the cases that separate the two.

The **build-and-compare** form performs the rotation instead of testing it — `reverse(map(num)) == num` — which makes the reversal impossible to forget because you have to write it down. It costs O(n) space and two passes, so it is the slower way to answer, but it is an independent implementation and a distinct compiler surface: `Vec[char]` construction, `.reverse()`, and element-wise comparison rather than index-pair arithmetic.

## What it found

**No compiler bugs**, and this time the claim is built on a differential from the start rather than bolted on afterwards.

[`differential.kara`](differential.kara) and its twin [`differential.py`](differential.py) run 6,000 shared-LCG cases through **both** algorithms, which must agree with each other and with Python:

```
algorithms disagree on 0 of 6000 cases
accepted 1938 of 6000 (3018 constructed, 1488 then corrupted)
439356090
```

The same three lines come back from `karac run --interp`, `karac run`, `karac build` (auto-par, the default) and `KARAC_AUTO_PAR=0 karac build`.

**How the cases are drawn matters more than how many there are.** A uniform draw over ten digits makes nearly every string of length > 3 a reject, so the accepting path would only ever be tested on very short inputs — 6,000 cases that all exit on the first forbidden digit test almost nothing. So half the cases are **constructed** strobogrammatic strings (pairs from the rotatable set, an odd centre from `0/1/8`), and half of *those* are then **corrupted at one random position**. That puts near-misses — strings one character away from legal — at every length from 1 to 8, which is where a pairing or centre-handling bug would actually live. The accept rate went from 7% under a uniform draw to 32% with this shape, and 1,488 of the cases are single-character corruptions. The other half stays uniform over 5 rotatable + 2 forbidden digits, because construction never produces a forbidden digit and that reject path needs covering too.

This is the second kata in a row to come back clean, and that is worth stating rather than glossing: the shapes here — `chars().collect()`, `Vec[char]` indexing, `.reverse()`, `Option[char]` returns, `char` equality — are well-trodden by the corpus. A clean result on a differential designed to be adversarial is evidence; a clean result on hand-picked inputs would not have been.

## Kāra features exercised

- **`num.chars().collect()` into `Vec[char]`** — the corpus's standard string-to-characters idiom (as in [#205](../205-isomorphic-strings/)), here on both a borrowed parameter and a locally built `String`.
- **`Option[char]` as a total rotation map** — `rotate_digit` returns `None` for a digit that does not survive, so "illegible" is a value rather than a sentinel character, and the caller's `match` makes the reject path explicit.
- **`char` literals and equality** (`c == '6'`, `r != cs[hi]`) — comparison on a primitive `char`, distinct from the `String` equality the #243–245 family leans on.
- **`Vec[char].reverse()`** — in-place reversal (rotate variant), then element-wise comparison against the original.
- **`String.push(char)`** — building a `String` one character at a time in the differential, the inverse of `chars().collect()`.
- **Index-assign into `Vec[char]`** (`chars[lo] = a`) including the two-ended write `chars[lo] = a; chars[hi] = b` that constructs a strobogrammatic string.
- **`lo <= hi` two-pointer convergence** where the inclusive bound is load-bearing for correctness, not a style choice.

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go
./bench/bench.sh
```

[`bench/`](bench/) carries a scaled cross-language variant — same algorithm, same LCG, all five agreeing on the sink (`325454619`). Build-once + punch: 20,000 length-32 numbers built **once**, then 100 passes of the two-pointer check over all of them — 2,000,000 calls, ~30M pair-checks.

**The corpus is deliberately mostly accepting.** A uniform digit draw would make almost every number reject on its *first* character, so the benchmark would measure loop entry and early return rather than the scan. Every number is therefore constructed strobogrammatic, with 1 in 8 corrupted at one random position — which rejects, but on average halfway through, so a reject still does real work and no branch predictor learns a fixed answer.

**All five lanes index bytes in place.** Kāra refuses `s[i]` outright, with a diagnostic that names both alternatives and their cost — *"`s[i]` would hide an O(n) scan … use `s.char_at(i)` (O(n)) or `s.bytes()[i]` (O(1))"*. The input is ASCII digits, so `bytes()` is correct and is exactly what C, Go (`num[i]`) and Rust (`as_bytes()[i]`) do naturally. An earlier draft had Kāra materialising a `Vec[char]` per call while C indexed in place; that would have made the Kāra lane do strictly more work and reported the difference as codegen quality.

### Runtime — sequential lane

Container x86-64, 2026-08-04, hyperfine 30 runs, `KARAC_AUTO_PAR=0`, all lanes 99–101% CPU.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| Rust `-O` | 24.1 ± 0.7 ms | 0.45× |
| Rust overflow-checked | 24.4 ± 2.9 ms | 0.45× |
| Rust @ x86-64-v3, overflow-checked | 25.5 ± 1.2 ms | 0.47× |
| C `clang -O3` @ x86-64-v3 | 38.6 ± 4.0 ms | 0.72× |
| C `clang -O3` | 40.8 ± 8.3 ms | 0.76× |
| **Kāra (codegen)** | **53.9 ± 1.9 ms** | 1.00× |
| Go | 308.8 ± 7.0 ms | 5.72× |

**Do not read the Go row as a Kāra win. It is a Go compiler artifact, and it was chased down rather than published.**

A 5.72× lead over Go on a byte-scanning loop is not credible on its face — C, Rust and Kāra cluster within 2.2× of each other and Go sits 6–13× away, which is the signature of a mirror problem, not a language fact. Three hypotheses were tested and **rejected**: constant-modulo strength reduction (removing the `% 1000000007` changes nothing, 0.30 s either way), inlining (`go build -gcflags=-m` confirms `rotateByte` and `isStrobogrammatic` are both inlined), and bounds checks (passing a `*[32]byte` with static bounds instead of a slice changes nothing).

The cause is the **5-way `switch` on a byte**. LLVM turns it into a table or a branchless sequence; Go's compiler emits a compare chain and evaluates it ~30M times:

| Go `rotateByte` shape | Time |
|---|---|
| 5-way `switch` (as published, matching every other lane's source) | 0.31 s |
| explicit `[256]byte` lookup table | **0.03 s** |

So with a lookup table Go runs at ~30 ms and **leads Kāra**, and the honest summary of this kata's Go lane is: *Go's codegen for a small value switch is ~10× worse than LLVM's here, and that single difference dominates the measurement.* The switch is kept in all five mirrors because it is the source-level algorithm they share and it is what anyone would write — but the resulting number says nothing about Kāra versus Go.

**What the C and Rust rows do say.** Kāra is **1.40× behind ISA-matched C** and **2.11× behind equal-safety Rust** — and this is the first kata in the recent run where Rust is clearly ahead rather than level or behind. Overflow checks cost Rust nothing (24.1 vs 24.4 ms, inside σ), matching [#243](../243-shortest-word-distance/) and [#245](../245-shortest-word-distance-iii/) and unlike [#244](../244-shortest-word-distance-ii/)'s 2.28×: there is no arithmetic in this loop worth checking. Kāra's gap here is against the same 5-way map that costs Go so dearly, which makes it the natural next thing to look at — whether `karac` table-izes a small `if`-chain over `u8` the way LLVM does for C.

### Caveats

Container-x86 lane, ~1.15× noise floor per [`BENCHMARKS.md`](../../../BENCHMARKS.md) — the two C rows are a tie with each other, as are the three Rust rows. The 1.40× C gap and 2.11× Rust gap clear the floor. The Go row is excluded from any comparative claim for the reason above.

The **M5 Pro host lane (`results.json`) has not been measured**, so this kata stays out of the consolidated feed and graphs until an Apple-silicon run is done.

## Running

```bash
# Kāra — both variants, all backends, same output.
karac run   strobogrammatic.kara
karac run   strobogrammatic_rotate.kara
karac build strobogrammatic.kara && ./strobogrammatic

# Python
python3 strobogrammatic.py

# Verify they agree
for v in strobogrammatic strobogrammatic_rotate; do
    diff <(karac run $v.kara) <(python3 strobogrammatic.py) && echo "$v OK"
done

# Randomized differential: 6,000 cases, two algorithms, must match Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"
```

## Notes

Verified byte-identical under `karac run --interp` (tree-walk), `karac run` (JIT), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — with both Kāra variants agreeing with the Python mirror on the spec cases and the differential.

**Why the test set looks the way it does.** Every entry earns its place against a specific wrong implementation: `"6"` and `"9"` alone catch "is this digit rotatable" (both rotate, neither is strobogrammatic); `"6996"` vs `"6009"` catch a missing reversal; `"689"` and `"69896"` catch a `lo < hi` loop that skips the odd centre; `"10501"` catches a forbidden digit hidden between legal pairs; `"18"` catches assuming self-mapping digits pair with each other. That is 26 cases chosen as counterexamples rather than as coverage — the breadth comes from the differential.
