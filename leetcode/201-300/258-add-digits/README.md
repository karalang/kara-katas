# 258. Add Digits

Repeatedly sum a number's digits until one digit is left.

```
38 -> 3+8 = 11 -> 1+1 = 2
0  -> 0
9  -> 9
```

**Constraints:** `0 ≤ num ≤ 2³¹ - 1`.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `add_digits.kara` ★ | `% 10` / `/ 10` simulation | O(log n) per pass, ≤ 3 passes |
| `add_digits_formula.kara` | `1 + (num - 1) % 9` | **O(1)** |
| `add_digits_bytes.kara` | render to text, sum the bytes | O(log n) + a `String` per pass |
| `differential.kara` | exhaustive sweep 0..300,000, all three agree | — |

## The mechanism

**`10 ≡ 1 (mod 9)`**, so every power of ten is congruent to 1 and a number is
congruent to the sum of its digits mod 9. Repeating the digit sum preserves that
congruence all the way down, so the single-digit result is the unique value in
`1..=9` congruent to `num` — with `0` as its own case, being the only input whose
answer falls outside that range.

**`num % 9` is the tempting spelling and it is wrong**, for every multiple of
nine: `9 % 9 == 0`, but the digital root of 9 is 9. `1 + (num - 1) % 9` shifts
the range so multiples of nine land on 9 rather than 0.

**The zero branch is explicit on purpose.** `num = 0` would evaluate
`1 + (-1) % 9`, and Kāra's `%` keeps the dividend's sign (as C and Rust do,
unlike Python), so `(-1) % 9` is `-1` and the expression yields `0` — accidentally
correct. Writing it as a branch means the reader never has to reason about the
sign rule to trust the answer.

## Why the third file shares no arithmetic

`add_digits.kara` and a recursive twin would both rest on the same `% 10` loop:
agreement between them is one computation checked against itself, and says
almost nothing about whether the congruence in `add_digits_formula.kara` is
right.

`add_digits_bytes.kara` goes through the text representation instead — render,
then subtract `'0'` from each byte. It shares no arithmetic with either sibling,
so three-way agreement is a real check of the derivation rather than a
restatement of it. It is also much the slowest, allocating a `String` per pass;
`bench/` measures that.

## Why the sweep is exhaustive rather than sampled

The closed form's failure mode is not a random wrong answer — it is being wrong
on a **regular subset**. The likeliest such subset is the multiples of nine, and
a uniform draw would find that. A subtler off-by-one — wrong only at `9k+1`, say
— could slip through sampling. Sweeping every value in a contiguous range cannot
miss a residue class.

Over `0..300,000`: **33,333 inputs answer 9** (exactly one ninth) and **exactly
one answers 0**, which is `num = 0` itself. Plus 500 high-range values stepping
down from `i64.MAX` by a prime stride, where the simulation needs three passes
and the closed form still needs one.

**The harness was tested against the bug it exists to find.** Replacing the
closed form with `num % 9` makes it report **33,333 mismatches** — precisely the
count of inputs whose answer is 9, confirming the bug hits exactly that residue
class and nothing else — plus 56 in the high range.

## Benchmark

`bench/` sweeps **10,000,000 LCG-drawn values** through the ★ `% 10` simulation.
Nothing is built once — the input is generated on the fly and the work is the
arithmetic. Sink `50005138`, reproduced by all four mirrors.

Values are drawn across the **full i64 magnitude range** rather than uniformly
small, because the pass count depends on magnitude: a 19-digit value needs three
passes where a 3-digit value needs one or two. Drawing only small values would
measure a single pass and hide the loop's shape.

This is a **pure integer-division lane** — no allocation whatsoever — which
complements the allocation-heavy ([#254](../254-factor-combinations/)), push/pop
([#255](../255-verify-preorder-sequence-in-bst/)) and string-building
([#257](../257-binary-tree-paths/)) lanes.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | σ% | vs Kāra |
|---|---|---|---|
| **Kāra (codegen)** | **209.1 ± 0.9 ms** | 0.4% | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 209.2 ± 0.6 ms | 0.3% | 1.00× |
| Rust `-O` | 211.0 ± 0.9 ms | 0.4% | 1.01× |
| C `clang -O3` | 213.4 ± 0.3 ms | 0.1% | 1.02× |
| Go | 235.8 ± 1.9 ms | 0.8% | 1.13× |

**Kāra, both Rust builds and C land inside a 2.1% band, and this is the tightest
lane in the corpus on either host** — σ of 0.1–0.4%. Kāra is nominally first and
0.1 ms ahead of equal-safety Rust, which is not a claim; what the lane does
establish is that a pure-arithmetic loop with no allocation and no memory traffic
runs at C speed in Kāra, and that its default overflow checking costs nothing
detectable here (equal-safety Rust and wrapping Rust are 0.9 ms apart).

**Go is 13% behind and I could not establish why.** The obvious hypothesis — that
Go emits real division where LLVM strength-reduces `/ 10` and `% 10` into a
multiply-and-shift — is **refuted**: disassembly shows zero `DIVQ` in Go's
`addDigits`, same as C and Kāra. Something else accounts for it, and this lane
does not identify what. The margin was 28% on the container and 13% here, so
whatever it is, it is partly a property of that host.

### The x86 corroboration run

Container x86-64, `bench/results.container-x86.json` — corroboration only
(BENCHMARKS.md § Hosts). It found the same three-way tie in a different order.

| lang | mean (ms) | σ |
|---|---|---|
| C | 458.0 ± 8.0 | 1.7% |
| Rust (checked) | 463.9 ± 6.8 | 1.5% |
| **Kāra** | **464.5 ± 8.2** | 1.8% |
| Rust | 465.7 ± 4.4 | 0.9% |
| Go | 597.7 ± 13.6 | 2.3% |

**Go is 28% behind and I could not establish why.** The obvious hypothesis —
that Go emits real division where LLVM strength-reduces `/ 10` and `% 10` into a
multiply-and-shift — is **refuted**: disassembly shows zero `DIVQ` in Go's
`addDigits`, same as C and Kāra. Something else accounts for it, and this lane
does not identify what.

**Kāra's binary is 15.3 KiB — smaller than C's 15.6 KiB.** First time in this
corpus. The program allocates nothing and touches no runtime surface, so the lean
archive links essentially nothing; against Rust's 3.86 MB and Go's 2.16 MB the
gap is three orders of magnitude larger than the runtime difference.

## Kāra features exercised

- **Sign-preserving `%`** on a potentially negative intermediate, and an explicit
  branch chosen over relying on it.
- **`f"{n}"` integer rendering** and **`String.bytes()`** with an ASCII offset —
  the byte-sum path.
- **`i64.MAX` as a literal** and as a loop bound, where the simulation needs
  three passes.
- **Nested `while` with a carried accumulator** — the digit-peeling inner loop
  inside the repeat-until-single-digit outer loop.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the two with
mirrors match Python.

No compiler bugs found — every construct here is well-trodden ground.

## Running

```bash
karac run add_digits.kara
karac run add_digits_formula.kara
karac run add_digits_bytes.kara

diff <(karac run add_digits.kara) <(python3 add_digits.py) && echo OK
diff <(karac run add_digits.kara) <(karac run add_digits_formula.kara) && echo OK
diff <(karac run add_digits.kara) <(karac run add_digits_bytes.kara) && echo OK

# exhaustive sweep 0..300,000 plus a high-range stride, three forms cross-checked
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in add_digits add_digits_formula add_digits_bytes differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
