# 190. Reverse Bits

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Divide and Conquer · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-bits](https://leetcode.com/problems/reverse-bits/)

Reverse the bits of a 32-bit **unsigned** integer.

```
43261596   (00000010100101000001111010011100)
  -> 964176192 (00111001011110000010100101000000)
1          ->  2147483648   (bit 0 → bit 31)
4294967295 ->  4294967295   (all ones)
```

**Constraints:** the input is a 32-bit unsigned integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **shift-and-peel** ★ | [`reverse_bits.kara`](reverse_bits.kara) | [`reverse_bits.py`](reverse_bits.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Shift the answer left one bit at a time while peeling the input's **low** bit off the right: `result = (result << 1) | (x & 1)`, then `x >>= 1`. After 32 steps, the input's bit 0 has migrated to the answer's bit 31, bit 1 to bit 30, and so on — a full mirror. O(32) = O(1).

## Kāra features exercised

- **Bitwise operators on `i64`** — `<<`, `>>`, `&`, `|` — the whole kernel. Values live in Kāra's signed `i64` but are masked to 32-bit behaviour; the intermediate `result << 1` peaks at 2³², well inside `i64`, so the default checked arithmetic never trips.
- **Fixed 32-iteration loop** — the constant-width shift-register idiom.

## Running

```bash
karac run   reverse_bits.kara
karac build reverse_bits.kara && ./reverse_bits
python3 reverse_bits.py
diff <(karac run reverse_bits.kara) <(python3 reverse_bits.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
