# 40. Combination Sum II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/combination-sum-ii](https://leetcode.com/problems/combination-sum-ii/)

Given a collection of candidates that **may contain duplicates** and a `target`, return
every unique combination summing to `target` where each array element is used **at most
once**. The result must contain **no duplicate combinations** — even when the input repeats
a value.

```
candidates = [10,1,2,7,6,1,5], target = 8  →  [[1,1,6], [1,2,5], [1,7], [2,6]]
candidates = [2,5,2,1,2],      target = 5  →  [[1,2,2], [5]]
```

**Constraints:** `1 ≤ candidates.length ≤ 100`, `1 ≤ candidates[i] ≤ 50`, `1 ≤ target ≤ 30`.
Note `[1,1,6]` legitimately uses two `1`s — the input *has* two — but the combination set
must not list `[1,1,6]` twice just because the two `1`s sit at different indices.

## Why this kata — the dedup twin of #39

This is the once-each, **duplicate-input** flip of [#39](../39-combination-sum/). #39 had
**distinct** candidates with **unlimited reuse**, and got uniqueness for free from "recurse
at `i`, never look left." #40 inverts both knobs — each element is used **once** (recurse at
`i+1`), and the input itself **repeats values**, so the index walk alone no longer dedups:
two equal candidates at different indices would each start the same combination. The kata is
about *how you suppress those duplicate branches* — and the two textbook answers (skip
repeats at each tree level, or collapse the multiset into value-with-count groups) plus the
mutable-vs-immutable path axis give three genuinely distinct factorings.

| Lens | Idea |
|---|---|
| **Sorted + same-level skip** ★ | sort, recurse at `i+1`; at each level skip `candidates[i] == candidates[i-1]` when `i > start` — only the first of a run of equal values may start a combination at that level |
| **Counted / grouped** | sort, then collapse to distinct `(value, count)` groups; DFS the distinct values once each, choosing *how many* copies (`count` … 0) of the current value — duplicates are impossible by construction, no adjacent skip needed |
| **Immutable-snapshot** | the same sorted same-level-skip DFS, but the path is carried as an owned `Vec[i64]` snapshot (`clone` + `push` per descent, no pop) — the functional shape |

The `i > start` guard is the whole trick in the ★ form: the **first** occurrence of a value
at a level recurses normally; later equal values at the **same** level are skipped because
any combination they could start is already enumerated by that first occurrence's subtree.
Deeper levels still see the duplicates — `[1,1,6]` uses two `1`s because the second is
reached with `start` past the first, where it becomes *that* level's first pick.

## Approaches

Three styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`. All sort first, so all emit combinations in the same lexicographic
order.

| Approach | File | Shape |
|---|---|---|
| **Sorted + same-level skip** ★ | [`combination_sum_ii.kara`](combination_sum_ii.kara) | `if i > start and c == candidates[i-1] { continue }`, recurse at `i+1`, suffix-`break` |
| Counted / grouped | [`combination_sum_ii_counted.kara`](combination_sum_ii_counted.kara) | run-group into `vals`/`cnts`, then take `k = count … 0` copies of each distinct value |
| Immutable-snapshot | [`combination_sum_ii_snapshot.kara`](combination_sum_ii_snapshot.kara) | same sorted skip DFS, `let next = path.clone(); next.push(c)` per descent, no pop |

The ★ form is the tightest; the counted form makes the dedup *structural* (the choice is "how
many", so no duplicate branch can exist) and run-groups the sorted multiset exactly as kata
[#38](../38-count-and-say/)'s indexed style reads runs; the snapshot form trades the
per-descent copy for zero pop bookkeeping. All three are O(answer size) to emit and agree on
every combination.

## What this kata surfaced

**Nothing new — and that is the result.** #40 leans on exactly the idioms kata #39 drove two
karac fixes for: the leaf snapshot `out.push(path.clone())` through a `mut ref Vec[i64]`
receiver ([`B-2026-06-18-9`](../../../../kara/docs/bug-ledger.jsonl)) and
`sort_by(|a, b| a.cmp(b))` in a function the auto-par pass parallelizes
([`B-2026-06-18-10`](../../../../kara/docs/bug-ledger.jsonl)). All three solvers — including
the counted form, which builds two parallel `Vec[i64]`s and the snapshot form, which clones
an owned path — **build and run clean**, byte-for-byte matching the interpreter and the
Python oracle on every case. A stress run over a 16-element duplicate multiset confirmed
`karac run`, the auto-par default `karac build`, and the `KARAC_AUTO_PAR=0` seq twin all
produce the identical checksum (auto-par *does* fire on that shape and stays correct). So #40
is a **regression witness** for the #39 fixes across a richer dedup workload and a new
counted factoring, rather than a new bug-finder — the corpus's other job.

## Benchmarks

Workload: enumerate once-each combinations for a per-iteration target. **`TOTAL = 30000`**
times, with a fixed duplicate-heavy multiset `[1,1,2,2,3,3,4,5,6,7]` (sorted once), set
`target = 10 + (k % 13)` (a per-iteration target, so nothing hoists), solve with the ★
sorted same-level-dedup backtracker, and fold a **position-weighted** signature of every
combination — `sum element*(i+1)` per combo, combos folded by a rolling `*31`, plus the
count — into a rolling checksum (sink `71775739`). The target varies with the loop index (no
comparator can hoist the work out) and the checksum carries a loop-borne dependency, so this
is a single-lane (seq) bench by construction. Like #39 this is a **heap-allocating**
`Vec[Vec[i64]]` workload — each solve grows a fresh result and clones a path at every leaf —
so it isolates nested-collection allocation + the duplicate-skip backtracking codegen. Apple
M5 Pro; `bench/bench.sh` (`hyperfine`). Figures below are the 2026-10-31 re-bench
(results.json `measured_at` 2026-11-01T02:02Z), measured with **karac
0.9.0-dev.14057+g6697158fa** — the v2/MIR backend (the legacy backend was deleted
2026-10-23).

### Seq lane — runtime (single-threaded sorted same-level-dedup backtracking)

| | C | Rust (`-O`) | Rust (`overflow-checks=on`) | **Kāra** | Go | Python |
|---|---|---|---|---|---|---|
| time | 35.5 ± 0.8 ms | 35.6 ± 1.7 ms | 35.7 ± 1.5 ms | **38.1 ± 0.9 ms** | 42.4 ± 1.0 ms | 600 ms (last measured 2026-06-19, not re-run) |
| vs Kāra | 1.07× faster | 1.07× faster | **1.07× faster (= safety)** | — | 1.11× slower | 12.9× slower than the 2026-06-19 Kāra figure |

**Kāra now trails the C-class by ~1.07× and leads Go by 1.11×.** In language ratios against
the previous feed (legacy karac 0.1.0, 2026-06-19): Kāra/Rust 1.41× → 1.07×, Kāra/C 1.40× →
1.07×, Kāra/Go 1.23× → 0.90× — a ~1.3× relative gain, while every comparator ran 7–13 %
slower in absolute ms this session.

**The June standing (history), and what is left.** On the legacy build Kāra trailed by ~1.4×
and the gap was put down to allocation, the same as #39: the duplicate-skip walk prunes the
tree harder than #39's reuse walk, so each `solve` returns fewer combinations, both Kāra and
Rust dropped proportionally versus #39, and the *ratio* was essentially unchanged. On the
MIR backend the two katas no longer move together — #39 is now a tie with Rust (0.98×) while
#40 keeps a 1.07× gap — so the remaining residual is specific to this walk; it was not
isolated in this pass. The per-leaf `Vec[Vec[i64]]` growth + path `clone()` churn —
`malloc`/`realloc`/`free` that C/Rust/Go drive through the same allocator with tighter
per-object overhead — is still the candidate, and the builder-buffer / arena-reuse headroom
identified in #38/#39 is still **not** implemented in the kata; no perf change was made
here.

- **The overflow tax is ~zero.** `rustc -O` (35.6 ms) and `-C overflow-checks=on` (35.7 ms)
  are within noise — the hot path is pointer-chasing and `i64` adds well inside range, no
  arithmetic to check — so **equal-safety** Rust is 1.07× ahead, the same as unchecked. C
  (35.5 ms) and Rust (35.6 ms) are within noise; Go (42.4 ms) is now the slowest compiled
  mirror.

**No par lane — by construction.** The per-iteration solve is pure, but the checksum
reduction carries a loop-borne dependency, so karac's auto-par-on-reduction pass does not
fire: verified in the emitted IR (`KARAC_MIR_LL`) on the 2026-10-31 MIR build — neither the
default nor the `KARAC_AUTO_PAR=0` build carries a call of `karac_mir_task_spawn` (the
detector fires on a known auto-par program), and both run single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.14 MiB** | 1.17 MiB | 1.16 MiB | 9.52 MiB |
| binary size (seq) | 295.8 KiB | 456.0 KiB | **33.1 KiB** | 2452.1 KiB |
| compile elapsed | 132.4 ms | 110.9 ms | **50.4 ms** |
| compile peak RSS | 58.0 MiB | 33.2 MiB | **2.6 MiB** |

The result vectors are freed each iteration, so steady-state RSS is allocator-bound and
tight: Kāra (**1.14 MiB**) is still the lowest, with C (1.16) and Rust (1.17) within
rounding, while Go's runtime pays 9.52 MiB and Python's interpreter paid 6.8 MiB (last
measured 2026-06-19, not re-run). Every MIR Kāra binary is ~300–390 KB where the legacy
backend's were ~34 KB (kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md));
this one is **295.8 KiB** (302,896 B, was 34,112 B on legacy), 1.54× under Rust and 8.9×
over C (Go's static runtime is 2.4 MiB). On the MIR backend compile no longer favours Kāra:
karac is 1.19× slower than `rustc -O` (132.4 vs 110.9 ms) and peaks at 1.7× its compiler
RSS (58.0 vs 33.2 MiB); the legacy build was 76.4 ms / 14.4 MiB, ahead of rustc on both.
clang's 50.4 ms / 2.6 MiB is the toolchain floor.

## Kāra features exercised

- **`sort_by(|a, b| a.cmp(b))` + duplicate-skip backtracking** — sorting makes equal values
  adjacent so the `i > start and c == candidates[i-1]` dedup is one backward look; the same
  `sort_by` whose auto-par codegen kata #39 fixed ([`B-2026-06-18-10`](../../../../kara/docs/bug-ledger.jsonl)).
- **`Vec[Vec[i64]]` built by path snapshots** — `out.push(path.clone())` at each solution
  leaf, the `mut ref Vec` clone whose deep-copy kata #39 fixed ([`B-2026-06-18-9`](../../../../kara/docs/bug-ledger.jsonl)).
- **Run-grouping a sorted multiset into parallel `Vec[i64]`s** — the counted solver collapses
  `[1,1,2,2,…]` into `vals`/`cnts` with a two-pointer run walk, then a "take `k` copies" DFS.
- **`Vec.push` / `Vec.pop` backtracking + `mut ref` accumulator threading** — the ★ and
  counted solvers bracket each choice with push/pop; `path` and `out` thread as `mut ref`,
  the root call writing the call-site markers and interior calls forwarding unmarked.
- **`Vec.clone()` across owned and borrowed receivers** — the snapshot solver clones an owned
  `path`, the ★ and counted solvers clone a `mut ref` one.
- **Three factorings of one dedup backtracker** — same-level skip, counted/grouped, and
  immutable-snapshot, all agreeing across the LeetCode examples under both `karac run` and
  `karac build`.

---

**Bug ledger:** none filed — #40 builds and runs clean on the idioms kata #39 fixed
([`B-2026-06-18-9`](../../../../kara/docs/bug-ledger.jsonl),
[`B-2026-06-18-10`](../../../../kara/docs/bug-ledger.jsonl), both fixed `c0432862`),
serving as a regression witness for those fixes across a duplicate-dedup workload. See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).
