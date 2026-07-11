# 93. Restore IP Addresses

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String · Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/restore-ip-addresses](https://leetcode.com/problems/restore-ip-addresses/)

Given a string `s` of digits, return **all possible valid IP addresses** that can be formed by inserting three dots into `s`. You may not reorder or remove any digits. A **valid** IP address is four integers (each `0`–`255`) separated by single dots, where **no** integer has a leading zero (so `0` is allowed but `01`, `00` are not).

```
s = "25525511135"  ->  ["255.255.11.135", "255.255.111.35"]
s = "0000"         ->  ["0.0.0.0"]
s = "101023"       ->  ["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]
```

**Constraints:** `1 ≤ s.length ≤ 20`; `s` consists of digits only.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Segment-at-a-time backtracking** ★ | [`restore_ip.kara`](restore_ip.kara) ✓ via `karac run` / `karac build` | [`restore_ip.py`](restore_ip.py) ✓ |
| **Three explicit dot-position loops** | [`restore_ip_loops.kara`](restore_ip_loops.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all nine test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other **and** with the Python mirror. The ★ carries one note-level `N0503` RC-fallback diagnostic (the recursively threaded `path: String`); the loops variant compiles with **zero diagnostics**.

## Four segments, one validity rule

An address is four segments that together consume the whole string, each passing the same test: **1–3 digits, no leading zero unless the segment is exactly `"0"`, value ≤ 255**. Both solvers enumerate the same candidates in the same order — they differ only in *how* the three cut points are placed.

**Segment-at-a-time backtracking** ([`restore_ip.kara`](restore_ip.kara), the ★) places one segment at a time from position `start`, trying each length 1/2/3, validating, and recursing for the next part:

```
backtrack(start, part, path):
    if part == 4:
        if start == n: emit(path)          # four parts AND fully consumed
        return
    for len in 1..3:
        if start + len > n: break
        seg = s[start .. start+len]
        if (len == 1 or seg[0] != '0') and value(seg) <= 255:
            backtrack(start+len, part+1, part == 0 ? seg : path + "." + seg)
```

The dots are woven into `path` as it grows (`f"{path}.{seg}"` for every part after the first), so a complete address needs no post-join. The segment value is folded and its string built in the **same pass** over the `Vec[u8]` digit bytes — no substring copies.

**Three explicit dot-position loops** ([`restore_ip_loops.kara`](restore_ip_loops.kara)) drops the recursion: a candidate is fixed by three cut points `a < b < c`, giving segments `s[0,a)`, `s[a,b)`, `s[b,c)`, `s[c,n)`. Each cut advances at most 3 past the previous (a segment is 1–3 digits), and all four segments run through a shared `valid_seg` / `seg_str` helper pair:

```
for a in 1..min(3,n-1):
  for b in a+1..min(a+3,n-1):
    for c in b+1..min(b+3,n-1):
      if valid_seg(0,a) and valid_seg(a,b-a) and valid_seg(b,c-b) and valid_seg(c,n-c):
        emit(seg(0,a) + "." + seg(a,b-a) + "." + seg(b,c-b) + "." + seg(c,n-c))
```

It walks the **identical candidate order** as the ★'s DFS (part-1 length 1, then 2, then 3, and so on), so the two produce byte-identical lists — a distinct surface (flat nested loops + a reusable validate/emit helper pair) proving the same enumeration two ways.

## Kāra features exercised

- **Recursion threading `path: String` + `mut ref Vec[String]`** — the ★ carries the growing address down the DFS and pushes finished addresses into the accumulator (`mut out` at the root, unmarked forwarding inside — the call-site-marker rule shared with [#39](../39-combination-sum/)/[#78](../78-subsets/)).
- **`if`-expression for the dot weave** — `let newpath = if part == 0i64 { seg } else { f"{path}.{seg}" };` — a value-producing `if` feeding the recursive call directly.
- **Single-pass value-fold + string-build** — each segment's numeric value (`val * 10 + digit`) and its text (`seg.push_str`) are produced in one walk over the `Vec[u8]` bytes, no substring allocation.
- **Byte-level digit handling** — `s[start] != 48u8` (the leading-zero guard) and `(s[start+i] as i64) - 48i64` (the digit decode) work directly on the `u8` bytes of `str.bytes()`.
- **Triple-nested `while` with data-dependent bounds** — the loops variant's `a`/`b`/`c` cuts (`while a <= 3 and a < n { … }`) enumerate the three dot positions with no recursion.

**v1 note.** `s.length ≤ 20` (the LeetCode cap; a valid restore needs 4–12 digits), so the candidate space stays small; the per-case sink folds the address count and every emitted address's bytes into a running hash, both count- and content-sensitive. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`, and both agree with the Python mirror on every case.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   restore_ip.kara
karac build restore_ip.kara && ./restore_ip

# The three-loop variant (identical output):
karac run restore_ip_loops.kara

# Python
python3 restore_ip.py

# Verify they all agree
diff <(karac run restore_ip.kara) <(python3 restore_ip.py)               && echo OK
diff <(karac run restore_ip.kara) <(karac run restore_ip_loops.kara)     && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`restore_ip.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** Canonical numbers measured on the corpus's **Apple M5 Pro** (6P+12E, Darwin 25.5.0; `karac 0.1.0` from `main` `a84a8624`, `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). A shared x86-64 Linux cloud-container reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. The cross-language *ordering* itself differs between the two — see the note below the table.

**Workload.** The kata's engine is the **segment enumeration + validity test** (which three cut points give four valid 0–255 segments). Building the address strings would make this an allocation bench, so instead the bench **folds** the segment values of every valid quadruple through a rolling polynomial hash — no strings. Digits are computed inline from the iteration index so nothing hoists, and the three-dot triple loop with the leading-zero / ≤255 test runs over them, **K = 6,500,000** times (acc seeded by the loop index). All five compiled mirrors must agree on `467547481` before timing.

**Data-dependent length — the honest-bench lever.** The input length **varies per iteration** (`n = 4 + iter%9`, i.e. 4–12, the real range for a restorable string). This is not cosmetic: a **fixed** `n = 12` lets clang/rustc statically unroll and *vectorize* the fixed-shape 12-element enumeration, erasing the checked scalar work — under that degenerate shape unchecked C/Rust ran **4–5× ahead purely on SIMD** while equal-safety `rustc -O -C overflow-checks=on` and Go landed *behind* kāra, a pure measurement artifact (CLAUDE.md's "vectorizable loop distorts benches" pitfall). Data-dependent bounds make the trip counts unknowable at compile time, so **every engine does honest scalar work** and the field levels out.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded (the loop-carried hash is not a reduction the auto-par pass can split; the default build is verified equal to `KARAC_AUTO_PAR=0`). **Apple M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| rust restore_ip (rustc -O)                          | 141.1 ± 1.5 ms |
| **kāra restore_ip**                                 | **144.4 ± 0.9 ms** |
| c    restore_ip (clang -O3)                          | 153.7 ± 2.1 ms |
| rust restore_ip (rustc -O, overflow-checks=on)      | 182.8 ± 3.3 ms |
| go   restore_ip                                     | 345.6 ± 7.1 ms |

**The equal-safety headline holds and sharpens.** Kāra checks integer overflow by default, and at matched safety it is **1.27× ahead of `rustc -O -C overflow-checks=on`** and **1.06× ahead of clang C** — while landing within **~2 %** of *un*checked `rustc -O` (a statistical dead heat: 144.4 ± 0.9 vs 141.1 ± 1.5, overlapping ranges), and **2.39× ahead of Go**. The tell is the cost of the overflow guards themselves: adding them costs **Rust ~30 %** (141 → 183 ms) but kāra only a few percent, so kāra-*with*-checks nearly matches Rust-*without* and clears Rust-*with* by a wide margin. The enumeration is branch-heavy (the leading-zero and ≤255 guards, plus the three data-dependent loop bounds), so it is **latency-bound on branch resolution** rather than throughput-bound — the same favourable regime as the recursion-bound backtracking siblings [#77](../77-combinations/)/[#78](../78-subsets/)/[#90](../90-subsets-ii/), where kāra's higher IPC absorbs its extra bounds/overflow-check instructions (fully vs C and equal-safety Rust; to within noise vs unchecked Rust). Binary **33.1 KiB** (C parity at 32.7 KiB, ~73× smaller than Go's 2.4 MiB), peak RSS **1.0 MiB** (identical to C). Python (K = 200,000, a fraction of the native iterations) is timed separately at 827 ms.

**What changed from the container.** On the shared x86 container kāra was outright *fastest of five* (592 ms, ahead of C and both Rust builds); on the M5's wider out-of-order core the whole native field compresses to 141–154 ms and plain `rustc -O` nudges ~2 % ahead, dropping kāra to a near-tied **2nd**. The ordering shift is the cross-host variation the machine note warns about — the *equal-safety* comparison (kāra ahead of C and of overflow-checked Rust) is stable across both hosts; only the gap to overflow-*wrapping* Rust flips sign, and only by a hair.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap. C calibrates the metal floor, Go is the other native data point, Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
