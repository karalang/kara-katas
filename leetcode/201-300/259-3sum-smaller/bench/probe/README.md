# Probe — why plain `rustc -O` and `clang -O3` lose this lane

The first bench run produced a table with an impossibility in it:

```
rust_ovf   447.7 ms ± 5.9   (rustc -O -C overflow-checks=on)
rust       739.7 ms ± 3.4   (rustc -O)
```

Overflow-*checked* Rust cannot be 1.65× faster than unchecked Rust, at σ of
1.3% and 0.5%, by doing strictly more work. Something other than the checks was
being measured. This is that investigation.

The numbers reproduce exactly on re-measurement, and the binaries differ (three
distinct hashes, all three printing the same sink `540236372`), so it is not a
stale artifact or a harness join error. It is a real, stable property of the
code `rustc -O` emits.

## What the compilers actually emitted

The kernel is the converging two-pointer scan:

```rust
if s[a] + s[lo] + s[hi] < target { count += hi - lo; lo += 1; } else { hi -= 1; }
```

`rustc -O` if-converts the entire body to branchless code
(`three_sum_smaller::main`, one `cmov` in the kernel, no branch on the
comparison):

```asm
mov    (%r12,%rdi,8),%rsi     ; s[lo]
add    (%r12,%rcx,8),%rsi     ; + s[a]
add    (%r12,%rdx,8),%rsi     ; + s[hi]
mov    %rdx,%r8
sub    %rdi,%r8               ; hi - lo
cmp    %r15,%rsi
setge  %r9b
setl   %r10b
cmovge %rbx,%r8               ; count contribution: (hi-lo) or 0
add    %r10,%rdi              ; lo += (sum < target)
sub    %r9,%rdx               ; hi -= (sum >= target)
add    %r8,%rbp               ; count += contribution
```

`clang -O3` emits the same shape, instruction for instruction
(`setge`/`setl`/`cmovge`, one `cmov` in `main`).

`-C overflow-checks=on` emits a **branchy** loop instead — zero `cmov` in the
kernel, a real `jge` on the comparison, and `jo` edges after each checked add:

```asm
mov    (%r15,%rsi,8),%r8
add    %rdx,%r8
jo     <panic>
add    (%r15,%rdi,8),%r8
jo     <panic>
cmp    %r12,%r8
jge    <else: hi-->           ; a branch, not a cmov
```

The `jo` edges are what block the if-conversion: LLVM will not fold a body with
a side exit into a select chain.

## Why branchless is the slower shape here

Branchless makes the loop a pure serial dependency chain — the address of the
next load depends on the `cmov` result, so each iteration pays full load-to-use
latency with nothing else in flight. Branchy lets the predictor run ahead and
keeps several iterations' loads outstanding.

The decisive test: the inner loop's trip count is **exactly `hi - lo` regardless
of the target**, because every iteration advances `lo` or retreats `hi` by one.
So changing the target changes branch *predictability* and nothing else — same
instructions, same iterations, same memory traffic.

Re-run everything with `target = max_sum + 1` (every triple satisfies `<`, so
the branch is perfectly predicted):

| build | mid-band target | `max_sum + 1` | shape |
|---|---:|---:|---|
| kāra (checked by default) | 460.7 ms | **208.9 ms** | branchy |
| `rustc -O -C overflow-checks=on` | 448.6 ms | **233.7 ms** | branchy |
| `rustc -O` | 740.0 ms | 746.8 ms | cmov |
| `clang -O3` | 729.3 ms | 722.2 ms | cmov |

The branchy builds more than halve. The branchless builds do not move at all —
which is exactly what "immune to branch prediction" predicts, and confirms the
mechanism rather than merely being consistent with it.

## It is not the sort

C sorts with `qsort` and a function-pointer comparator, which cannot inline —
the explanation that fit #252 and #253. It does not fit here. Compiling the C
mirror with the counting loop disabled, leaving only the 26 `qsort` calls:

```
sort-only C   10.4 ms ± 0.7
full C       729.3 ms ± 8.8
```

The sort is **1.4%** of the lane. At n = 4,000 the O(n²) scan (208M inner
iterations) buries the O(n log n) sort by two orders of magnitude, as the kernel
comment claims. The `qsort` caveat does not apply to this lane and is not
carried into the README.

## What this means for the published table

The plain `rust` and `c` rows are real and reproducible, but they measure an
LLVM if-conversion pessimisation on this loop, not the cost of unchecked
arithmetic. Reading them as "C is 1.6× slower than Kāra at counting triples"
would be wrong.

The honest comparator is the equal-safety twin the harness already designates —
`rust_ovf` / `rust_v3` — and it lands within 3% of kāra.

The direction is worth stating plainly because it is the opposite of the usual
framing: kāra's **default overflow checking**, normally the thing that costs it
against `rustc -O`, is what keeps this loop branchy and therefore fast. The same
property that makes the equal-safety twin the fair comparator is the property
doing the work.

## Reproducing

```bash
# predictable-target variants (same trip count, predictable branch)
sed 's|let target = (min_sum + max_sum) / 2;|let target = max_sum + 1;|' \
    ../three_sum_smaller.rs > pred.rs
rustc -O pred.rs -o pred_plain
rustc -O -C overflow-checks=on pred.rs -o pred_ovf
hyperfine --warmup 3 -N ./pred_plain ./pred_ovf

# the emitted kernels
objdump -d --no-show-raw-insn ../target/three_sum_smaller |
    awk '/three_sum_smaller4main/{p=1} p&&/^$/{exit} p' | grep -c cmov   # 1
objdump -d --no-show-raw-insn ../target/three_sum_smaller_ovf |
    awk '/three_sum_smaller4main/{p=1} p&&/^$/{exit} p' | grep -c cmov   # 0

# qsort's share
sed 's|for (long a = 0; a + 2 < n; a++) {|for (long a = 0; a + 2 < n \&\& 0; a++) {|' \
    ../three_sum_smaller.c > sortonly.c
clang -O3 sortonly.c -o sortonly_c && hyperfine --warmup 3 -N ./sortonly_c
```

Measured on the x86-64 container lane (4-core Xeon @ 2.80 GHz, rustc 1.94.1,
clang 18.1.3), the same host as `../results.container-x86.json`.
