# Probe — where Go's 19% goes on this lane

The lane result had Go at 549.2 ms against a 463–477 ms cluster containing Kāra,
C and every Rust build. σ was 0.7–1.6% throughout, so the gap is real rather than
noise. This is where it went.

## The disassembly

The kernel is Euclid, so `x % y` has a **variable** divisor and cannot be
strength-reduced — every backend has to emit a real divide. Counting divide
instructions inside each `main`:

| binary | divides in `main` | shape |
|---|---:|---|
| C (`clang -O3`) | 7 | `div %r15` **paired with** `div %r15d` |
| Kāra | 7 | `div %r10` / `div %r15` paired with `div %r15d` |
| Go | 2 | `idiv %r9` + a `runtime.panicdivide` edge |

The pairing is the point. LLVM emits a **32-bit narrowing fast path**: before
each 64-bit `div`, it checks whether both operands fit in 32 bits and, if so,
runs the much cheaper `div r32` instead. That check pays off constantly here —
`gcd(m, 30)` collapses to operands below 30 after a single step, so almost every
division in the loop is small. The 64-bit path runs essentially once per call,
for the first `n % 30` on a wide `n`.

Go emits a single signed `idiv r64` with no narrowing, and takes it every time.

## Confirming it rather than inferring it

The disassembly is suggestive, not conclusive — Go also inlined `gcd` differently
and carries a `panicdivide` edge, either of which could account for the gap. So
the fast path was added to the Go source by hand and re-measured:

```go
if uint64(x) <= 0xffffffff && uint64(y) <= 0xffffffff {
    xs, ys := uint32(x), uint32(y)
    for ys != 0 { ts := xs % ys; xs = ys; ys = ts }
    return int64(xs)
}
```

| build | mean |
|---|---:|
| Go, stock | 557.7 ms ± 12.4 |
| Go, hand-written 32-bit narrowing | **501.3 ms ± 7.5** |
| C | 476.6 ms ± 6.4 |

Same sink (`19532` / `258327156`), so it is the same work. The narrowing closes
**56 ms of the 81 ms gap — about 70% of it**.

The remaining ~25 ms (5%) is *not* identified. It may be the `panicdivide`
check, the inlining difference, or something else entirely; this probe does not
say, and neither does the README.

## What this does NOT explain

[#258](../../258-add-digits/) also put Go ~28% behind, and it is tempting to
carry this result over. It does not transfer. That lane divides by the literal
`10`, which LLVM *and* Go both strength-reduce to a multiply-and-shift —
disassembly there showed **zero** divide instructions in any of the four
binaries. Whatever costs Go 28% on #258 cannot be a divide fast path, because
there is no divide.

What the two lanes together do establish is narrower and still worth having:
Go trails by a similar margin whether the division is strength-reduced away
(#258, 28%) or fully present (#263, 19%), and only in the second case is most of
the gap attributable to how the division is emitted.

## Note on status

The narrowing variant is a **probe, not a corpus lane**. It deliberately breaks
the cross-language parity rule — it is no longer the same algorithm as the other
mirrors — which is exactly why it can isolate the effect, and exactly why its
number never enters `results.container-x86.json`.

## Reproducing

```bash
# divide instructions in each kernel
objdump -d --no-show-raw-insn ../target/ugly_sweep_c |
    awk '/<main>:/{p=1} p&&/^$/{exit} p' | grep -E 'i?div'
objdump -d --no-show-raw-insn ../target/ugly_sweep_go_seq |
    awk '/<main\.main>:/{p=1} p&&/^$/{exit} p' | grep -E 'i?div'
```

Measured on the x86-64 container lane (4-core Xeon @ 2.80 GHz, go1.24.7,
clang 18.1.3), the same host as `../results.container-x86.json`.
