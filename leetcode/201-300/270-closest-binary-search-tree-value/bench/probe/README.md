# Probe — the lane measured nothing for two builds running

This lane was published only on its third workload. Both earlier versions
produced numbers, and both were wrong for reasons that had nothing to do with
the languages. They are recorded here because the second one is the more
instructive mistake I have made in this corpus.

## Fault 1 — hand-writing `abs` in every mirror

The first version defined `abs_f(x) = if x < 0.0 { 0.0 - x } else { x }` in all
five mirrors, on the theory that a shared spelling was the parity-safe choice —
C's `fabs`, Rust's `.abs()` and Go's `math.Abs` being three different things
(intrinsic, method, function).

That reasoning was backwards. **Every one of these languages has an absolute
value, including Kāra (`f64.abs()`)** — so hand-writing it is the *unnatural*
spelling everywhere, not the neutral one. And clang compiled the hand-written
form into a five-instruction branchless select:

```asm
subsd  %xmm2,%xmm5        ; v - target
xorpd  %xmm7,%xmm7
subsd  %xmm6,%xmm7        ; 0 - (v-target)
cmpltsd %xmm1,%xmm5
andpd  %xmm5,%xmm7
andnpd %xmm6,%xmm5
orpd   %xmm7,%xmm5        ; = abs, in six ops
```

sitting inside the pointer-chase dependency chain, where `fabs` is a single
`andpd`. Switching C to `fabs` alone was worth **23%** (1089 → 842 ms).

Parity means the same **algorithm**, not the same keystrokes. The idiomatic call
is what every mirror would really write, and it is what the lane uses now.

## Fault 2 — the generator confined every value to a 32K window

The corrected-`abs` table still had C at 850 ms against Kāra's 386 — 2.2×, which
is not a plausible C result on a float compare. Chasing it turned up something
worse than a slow mirror: **the workload was not the workload.**

```kara
state = (state * 1103515245i64 + 12345i64) & 2147483647i64;
let v = (state / 65536i64) % 1000000i64;      // intended: 0 .. 999,999
```

`state` is masked to 31 bits, so `state / 65536` is the **top 15 bits** and maxes
at **32,767**. The `% 1000000` never fires. So:

- tree values spanned 0–32,767, not 0–999,999 — 30,000 inserts into a 32K space,
  mostly duplicates, all of which go right;
- targets, drawn the same way, came out in **[−50999, −17233]** — *entirely below
  every value in the tree*.

Every descent therefore ran the left spine and returned the tree minimum. The
average descent was 10 nodes rather than the ~20 a random BST gives, and every
query returned the same answer.

**The tell was a probe that couldn't fail.** Two attempts to build a
"predictable direction" variant — targets forced below every value — produced a
sink byte-identical to the original, from two independent toolchains. I first
assumed a broken `sed`; the second attempt asserted its anchors matched, and the
sink was *still* identical. That could only mean the original already did what
the probe was supposed to induce, which is what pointed at the draw.

Combining two draws (`hi * 32768 + lo`) restores the intended range. The lane
went from 0.46 s to 4.6 s at the same round count — a 10× increase, which is the
size of the work that had been missing — and the table changed shape completely:

| | C | Kāra | C / Kāra |
|---|---:|---:|---:|
| hand-written `abs`, 32K window | 1090.2 ms | 465.6 ms | **2.34×** |
| `fabs`, 32K window | 850.0 ms | 385.9 ms | **2.20×** |
| **`fabs`, full range (published)** | **568.2 ms** | **470.5 ms** | **1.21×** |

## What survives — and the cause, now confirmed

The published table is internally consistent — σ 1.8–2.9%, both C builds within
1% of each other, all three Rust builds within 1% — so it ranks.

C is last, 1.21× behind Kāra, and **the cause is the `cmov`**. The disassembly
shows clang if-converting the child selection:

```asm
ucomisd %xmm4,%xmm2
mov     %r14,%rdx
cmova   %r15,%rdx            ; choose left/right branchlessly
mov     (%rdx,%rax,8),%rax   ; ...then load through it
```

which puts the comparison inside the **address** dependency chain. Kāra emits a
branch (`vucomisd` / `jbe`) the processor can speculate past.

### The control

The first draft of this file recorded that as a hypothesis, on the grounds that
the obvious probe — forcing the descent direction predictable — changes the tree
shape as well as the predictability, so it confounds the two.

That was the wrong probe. The right control changes **only the codegen** and
leaves the workload, the algorithm and the source untouched: LLVM has a pass that
converts `cmov` back to a branch, and it can be forced on.

```bash
clang -O3 -mllvm -x86-cmov-converter-force-all=true bst_close.c -o c_forcebr -lm
```

`cmov` in `main` goes 1 → 0. Sink unchanged at `687179070`.

| build | mean | `cmov` in `main` |
|---|---:|---:|
| `clang -O3` (the lane) | 566.7 ms ± 24.5 | 1 |
| `clang -O3`, cmov→branch forced | **434.5 ms ± 17.6** | 0 |
| Kāra | 466.0 ms ± 12.1 | — |
| Rust | 438.3 ms ± 8.8 | — |

**Forcing the branch is worth 23% and moves C from last to first**, level with
Rust — which was already fast because `rustc` chose a branch here. So the entire
C deficit, and a little more, is that one if-conversion decision.

This is [#259](../../259-3sum-smaller/)'s finding in a second setting. There,
plain `rustc -O` if-converted a converging two-pointer loop and paid **65%**;
here `clang -O3` if-converts a BST child selection and pays **23%**. Both are
serial dependency chains where a `cmov` forces the machine to wait for the
comparison, and a branch lets it run ahead. The pass that would have caught it
(`X86CmovConversion`) is on by default and did not fire.

The lane still publishes `clang -O3` as measured — that is the corpus's
methodology, and tuning flags for the one build they embarrass is how a
benchmark suite stops being comparable. But the number now has a cause attached
rather than a guess.

## Reproducing

```bash
# the draw that started it
python3 -c "s=270270
for _ in range(3):
    s=(s*1103515245+12345)&2147483647
    print((s//65536)%1000000)"        # never exceeds 32767
```

Measured on the x86-64 container lane (4-core Xeon @ 2.80 GHz, clang 18.1.3,
rustc 1.94.1, go1.24.7), the same host as `../results.container-x86.json`.
