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
