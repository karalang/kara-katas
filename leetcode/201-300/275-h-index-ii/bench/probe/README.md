# Probe — Rust is 1.63× behind on the canonical case, and it is one `cmov`

Every lane in this corpus has Rust within noise of C. Here it is **749.1 ms
against C's 447.5** on the same algorithm, with Kāra and Go both around 460. A
gap that size on an identical binary search is not a language difference, so it
was measured before it was published.

## The disassembly names it

`rustc -O` if-converts the search loop into two conditional moves:

```
14959:  cmp    %r10,(%rbx,%rdi,8)     ; citations[mid]  vs  n - mid
1495d:  cmovge %rdi,%r9               ; hi = mid
14961:  lea    0x1(%rdi),%rdi
14965:  cmovl  %rdi,%rdx              ; lo = mid + 1
```

`clang -O3` emits **zero** `cmov` in `main`; Kāra's search loop is branchy too.
So Rust alone is running the branchless form.

## Forcing the branch back closes the whole gap

Changing only the codegen — same source, same sink `217993832`:

| build | mean | `cmov` in `main` |
|---|---:|---:|
| `rustc -O` (the lane) | 758.0 ± 25.9 ms | 2 |
| `rustc -O -C llvm-args=-x86-cmov-converter-force-all=true` | **480.6 ± 4.6 ms** | 0 |
| `karac build` (for reference) | 459.0 ± 3.0 ms | — |

**1.58× from one if-conversion decision.** Branchless binary search puts the
comparison *inside* the address dependency chain: the next load cannot issue
until the current one has returned and been compared. The branchy form lets the
predictor speculate down one side and start the next load immediately, and it is
right often enough that the occasional flush costs less than the serialization.

## The third instance of the same mechanism

This corpus has now measured it three times, and the pattern is stable enough to
state as a rule: **`cmov` inside a serial dependency chain loses to a branch,
even when the branch is genuinely unpredictable.**

| kata | who if-converted | what it cost |
|---|---|---|
| [#259](../../259-3sum-smaller/) | `rustc -O`, a two-pointer loop | 65% |
| [#270](../../270-closest-binary-search-tree-value/) | `clang -O3`, BST child selection | 23% |
| **#275** | `rustc -O`, binary search | **58%** |

Binary search is the textbook case *for* branchless code — the branch is
maximally unpredictable, which is exactly the argument for `cmov`. It loses
anyway, because unpredictable-but-speculatable still beats serialized. Neither
compiler is wrong in general; both are wrong here, and which one guesses wrong
varies by kata.

## Reproducing

```bash
rustc -O hsearch.rs -o /tmp/r_cmov
rustc -O -C llvm-args=-x86-cmov-converter-force-all=true hsearch.rs -o /tmp/r_branch
/tmp/r_cmov && /tmp/r_branch          # same sink
hyperfine -w 3 -r 15 /tmp/r_cmov /tmp/r_branch ./target/hsearch_kara

objdump -d target/hsearch | awk '/<main>:/,/^$/' | grep -c cmov
```
