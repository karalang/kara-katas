# 137. Single Number II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Bit Manipulation · Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/single-number-ii](https://leetcode.com/problems/single-number-ii/)

Every element appears **three times** except one, which appears once. Find it — in `O(n)` time and `O(1)` extra space.

```
[2,2,3,2]                 ->  3
[0,1,0,1,0,1,99]          -> 99
[-2,-2,1,1,-3,1,-3,-3,-2,30] -> 30
```

**Constraints:** `1 ≤ n ≤ 3·10⁴`, `-2³¹ ≤ nums[i] < 2³¹`, exactly one element appears once.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **ones/twos FSM** ★ + **per-bit count mod 3** | [`single_number.kara`](single_number.kara) ✓ | [`single_number.py`](single_number.py) ✓ |

`✓` runs end-to-end today across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), agreeing with the Python mirror. **Both** bit approaches are computed and cross-checked at runtime (they must produce a bit-identical digest); answers are validated against the known LeetCode cases. Zero diagnostics, valgrind-clean.

## The mechanism

Two canonical tricks, both mirrored:

- **ones/twos FSM** (★): a per-bit 2-bit counter mod 3, carried in two 32-bit masks. `ones ^= x & ~twos; twos ^= x & ~ones` — after all elements, a bit set 3k times cancels to `00`, and the bit set once lands in `ones`. Sign-extended from 32 bits.
- **Per-bit count mod 3**: for each of the 32 bit positions, count how many numbers have it set; a residue `≠ 0 mod 3` is a bit of the answer.

Running both and asserting they agree is a self-check that also exercises the full bitwise operator set.

## Kāra features exercised

- **Full bitwise operator set** — `&`, `|`, `^`, `~`, `<<`, `>>` on `i64`, verified interp==build==Python (`12 & 10 = 8`, `~12 = -13`, `12 << 2 = 48`, …). The first corpus kata to lean on bit-twiddling.
- **32-bit two's-complement masking + sign extension** in i64 — `x & 0xFFFFFFFF`, then subtract `2³²` when the top bit is set.
- **`ref Vec[i64]` read-only parameters** — the two helpers borrow the same `nums` (see the note below).

> **Compiler friction surfaced by this kata (open).** Writing the two helpers as `fn helper(nums: Vec[i64])` (owned) and calling both on the same `nums` makes `karac check` hard-error (`value 'nums' moved here, used again here`) — yet `karac build` **and** `karac run` accept that exact program, compile it, and run it correctly and valgrind-clean. The two front-ends disagree on validity; filed as [kara `B-2026-07-19-2`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (check-vs-build ownership false-positive — the reused owned arg is resolved by codegen's RC/copy fallback, which `check` should treat as an rc-fallback rather than a hard error). The idiomatic declaration for a read-only function is `ref Vec[i64]` anyway, which this solver uses.

## Running

```bash
karac run   single_number.kara
karac build single_number.kara && ./single_number
python3 single_number.py
diff <(karac run single_number.kara) <(python3 single_number.py) && echo OK
```

## Notes

Dogfood-first bit-manipulation kata: it verifies the full `i64` bitwise operator set is codegen-correct (interp==build), cross-checks two independent bit tricks at runtime, and surfaced the check-vs-build ownership divergence `B-2026-07-19-2`.
