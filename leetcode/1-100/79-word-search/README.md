# 79. Word Search

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Backtracking · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/word-search](https://leetcode.com/problems/word-search/)

Given an `m × n` grid of characters `board` and a string `word`, return **true** if `word` can be spelled out along a path of **orthogonally adjacent** cells (up/down/left/right), where each cell is used **at most once**.

```
board = ABCE          word = "ABCCED" -> true
        SFCS          word = "SEE"    -> true
        ADEE          word = "ABCB"   -> false   (would reuse the 'B')
```

**Constraints:** `1 ≤ m, n ≤ 6`; `1 ≤ word.length ≤ 15`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **DFS backtracking, in-place cell marking** ★ | [`word_search.kara`](word_search.kara) ✓ via `karac run` / `karac build` | [`word_search.py`](word_search.py) ✓ |
| **DFS backtracking, separate `visited` grid** | [`word_search_visited.kara`](word_search_visited.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all nine test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## Two ways to forbid cell reuse

The search itself is the same for both: from **every** cell that matches `word[0]`, run a depth-first search that at step `k` requires the current cell to equal `word[k]`, then recurses into the four neighbours for `word[k+1]`. The whole word is found when `k` reaches `word.length`. Bounds and the letter-match are checked at the **top** of each call, so an out-of-range neighbour (including `r - 1 = -1`) falls straight out — the recursion is driven blindly into all four directions and the guard does the filtering.

The only thing the two variants differ on is **how a cell is marked used so the path can't cross itself**:

**In-place cell marking** ([`word_search.kara`](word_search.kara), the ★) temporarily overwrites the current cell with a sentinel byte (`0`, which no board letter equals), recurses, then restores it on the way out:

```
dfs(r, c, k):
    if k == len(word):            return true
    if out of bounds:             return false
    if board[r][c] != word[k]:    return false
    saved = board[r][c]; board[r][c] = 0        # mark used
    found = dfs(r+1,c,k+1) or dfs(r-1,c,k+1) or dfs(r,c+1,k+1) or dfs(r,c-1,k+1)
    board[r][c] = saved                          # restore
    return found
```

The board is threaded `mut ref Vec[Vec[u8]]`, and the mark/restore is a **nested 2D index assignment** — `board[r][c] = 0`. `or` short-circuits, so the first neighbour that completes the word ends the search immediately, and the restore still runs (the result is computed, *then* the cell is put back).

**Separate `visited` grid** ([`word_search_visited.kara`](word_search_visited.kara)) leaves the board immutable (`ref`, not `mut ref`) and carries a parallel `Vec[Vec[bool]]` of visited flags instead — set `true` before recursing, reset to `false` on the way out. It's the same DFS with the backtracking state moved out of the board and into a bool grid: a distinct surface (a `Vec[Vec[bool]]` threaded `mut ref`, nested bool index-assignment) that must agree with the in-place variant byte-for-byte.

## Kāra features exercised

- **Nested 2D index read + assignment** — `board[r][c]` and `board[r][c] = 0u8` compile a double GEP with a bounds check at each level; the mark/restore is the ★'s whole backtracking mechanism. (The u8 index path is the same one hardened by kāra ledger `B-2026-07-11-2` — narrow indices zero-extend to i64 before the bounds `icmp`.)
- **Signed neighbour probing** — the DFS calls `dfs(r - 1, …)` etc. unconditionally and lets the `r < 0` guard reject the negative coordinate; `r`/`c` are `i64`, so the `< 0` compare is a signed one.
- **`String.bytes()` → `Vec[u8]` board build** — each row string is walked byte-by-byte into a `Vec[u8]` row, and the rows into a `Vec[Vec[u8]]` board; the word is turned into a `Vec[u8]` the same way and compared byte-against-byte (`board[r][c] != word[k]`).
- **`mut ref` recursion threading** — the board (★) or the visited grid (variant) is passed `mut ref` down the recursion; the call-site-marker rule (`mut board` / `mut visited` at the root; unmarked forwarding inside) is the same one katas [#39](../39-combination-sum/)/[#77](../77-combinations/)/[#78](../78-subsets/) exercise.
- **`Vec[Vec[bool]]` grid** — the variant allocates a fresh all-`false` visited grid per start cell and flips flags in place, a bool-typed sibling of the u8 board.

**v1 note.** Boards and words are small (`m, n ≤ 6`, `word ≤ 15`); all coordinates and the fold fit i64. The per-case sink folds each case's boolean outcome (`1`/`0`) into a running polynomial hash so the sink is outcome-sensitive across the nine cases. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   word_search.kara
karac build word_search.kara && ./word_search

# The separate-visited-grid variant (identical output):
karac run word_search_visited.kara

# Python
python3 word_search.py

# Verify they all agree
diff <(karac run word_search.kara) <(python3 word_search.py)                  && echo OK
diff <(karac run word_search.kara) <(karac run word_search_visited.kara)      && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`word_search.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-10).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **The M5 reorders this one and corrects an earlier claim:** the container had kāra *ahead* of both Rust builds, but on the M5 Rust pulls ahead and kāra lands **4th of five** — behind C and both Rust builds, just ahead of Go. It is a throughput-bound loop where kāra's diffuse instruction-density gap (`B-2026-07-10-5`) shows directly in wall-time. `bench/results.json` records the M5 host.

**Workload.** The 4-neighbour visited-marking DFS (the kata's engine) run as an **enumerate-and-fold**: the recursion visits **every self-avoiding walk of up to 25 steps** from every start cell of a fixed all-`'A'` **5×5** board and folds each visited cell into a threaded accumulator (no per-node storage — so the measured work is the **DFS recursion + nested 2D-index access**, not allocation). A matched letter is replaced by "any unvisited cell, up to depth", so every branch is taken and the work is uniform and heavy. Run for **K = 12** iterations seeded by the loop index so nothing hoists. All five compiled mirrors must agree on `314439491` before timing.

**Equal data structure — the honest comparison.** Every mirror uses a **nested heap board** — kāra `Vec[Vec[u8]]`, Rust `Vec<Vec<u8>>`, C `uint8_t **`, Go `[][]uint8` — the same pointer-chased, per-level-bounds-checked layout, **not** a fixed 2D stack array. Handing the native mirrors a `[5][5]` stack array would measure *layout*, not *codegen*; the nested-heap match keeps it codegen-vs-codegen (kata [#72](../72-edit-distance/)'s fairness lesson).

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99 % CPU (verified equal to `KARAC_AUTO_PAR=0`; `karac build --concurrency-report` finds no parallelizable region). **M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| c    word_search (clang -O3)                     | **165.6 ± 2.7 ms** |
| rust word_search (rustc -O)                      | 195.5 ± 1.4 ms |
| rust word_search (rustc -O, overflow-checks=on)  | 199.4 ± 0.8 ms |
| **kāra word_search**                             | **211.6 ± 1.6 ms** |
| go   word_search                                 | 217.5 ± 1.2 ms |

On the M5 kāra is **4th of five** — 1.28× behind the C floor, 1.06× behind equal-safety `rustc -O -C overflow-checks=on`, just ahead of Go (1.03×). This **reverses the container's `Vec<Vec>`-indexing claim**: kāra does **not** elide an inner bounds check Rust keeps — instruction counts show kāra doing *more* work, not less (kāra **6.07 G** instructions vs rust_ovf 5.84 G, 1.04×; vs C 4.14 G, 1.47×). This is a **throughput-bound** loop (IPC ~6.3), so kāra's diffuse instruction-density gap (`B-2026-07-10-5`) shows directly in wall-time — the same regime as kata [#76](../76-minimum-window-substring/). Two honest reads: (1) vs **equal-safety Rust** kāra is only ~4 % more instructions — a small codegen-density sliver; (2) the larger 1.28× gap vs **C** is mostly the *cost of safety* both kāra and Rust pay (rust_ovf is itself 1.41× C's instruction count — C's raw `**` does zero bounds/overflow checking). Overflow checks are free here (branch/pointer-bound), so equal-safety and wrapping Rust are indistinguishable. Python (K=2, ~1.39 s, a fraction of the native iteration count) is timed separately.

Compile-cold on the M5: clang 39.5 ms < **karac 81.8 ms** < rustc 87.1 ms (karac ~1.06× faster than rustc, ~2.07× clang). Binary 33.4 KiB (C parity), runtime RSS 1.04 MiB (C parity). Full records in [`bench/results.json`](bench/results.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and on this index-bound nested-`Vec` backtracking, with the data structure held equal, kāra trails equal-safety Rust by 1.06× on the M5 (only ~4 % more instructions, but a throughput-bound loop so it shows). C calibrates the metal floor and Go is the other native data point. Python (run at a fraction of the iteration count, timed separately) is the ergonomic foil. This kata is exactly why Rust stays in the harness — it turned the container's rosy "kāra ahead of Rust" reading into a precise, honest 1.06× gap once measured on the reference machine.
