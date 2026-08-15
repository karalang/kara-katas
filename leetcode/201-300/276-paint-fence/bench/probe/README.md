# probe — what the par lane would be worth

`paint_enum_guarded.kara` is `../paint_enum.kara` with one change: the push is
wrapped in `if pre >= 0i64 { ... }`, a guard that is always true.

It exists to **size `B-2026-08-15-23`**, not to answer it. The collect-*tabulate*
lowering — selected for a body that pushes exactly once, unconditionally — never
dispatches to the worker pool while reporting that it did. A tautological guard
moves the loop out of the tabulate shape and into the collect shape, which does
dispatch:

|  | time | cpu |
|---|---:|---:|
| `../paint_enum.kara` (as written) | 457.9 ms ± 6.7 | 100% |
| `paint_enum_guarded.kara` | 130.4 ms ± 4.7 | **391%** |
|  | **3.51× ± 0.14** | |

Same logic, same sink (36884484), one always-true guard between them. The guarded
build beats sequential `clang -O3` (362.3 ms) by 2.8×.

**This is not the kata's answer to the gap.** The shipped lane stays in its
natural unconditional form and publishes 1.02×, because a kata twisted to dodge a
compiler bug has stopped doing its job. The probe turns "does not fan out" into a
number, which is what makes the ledger row actionable.
