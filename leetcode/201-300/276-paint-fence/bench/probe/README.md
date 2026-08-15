# probe — regression witness for `B-2026-08-15-23`

`paint_enum_guarded.kara` is `../paint_enum.kara` with one change: the push is
wrapped in `if pre >= 0i64 { ... }`, a guard that is always true.

## What it was for

It sized `B-2026-08-15-23` while that bug was open. A `#[par_order_free]` loop
whose body pushes *unconditionally* takes the collect-**tabulate** lowering,
which sets the `order_free` flag and routes dispatch through the runtime's
dynamic pull loop. That loop's chunk floor was

    chunk = iter_total.div_ceil(target_chunks)
                      .max(MIN_DYNAMIC_CHUNK.min(iter_total))   // 1024

so for any range under 1024 — this kata's loop has **16** iterations — the chunk
was the whole range: one chunk, one worker doing everything, three exiting. The
tautological guard moved the loop out of the tabulate shape and onto the static
split, which worked. That is why it was 3.5× faster:

|  | time | cpu |
|---|---:|---:|
| `../paint_enum.kara` (as written) | 457.9 ms ± 6.7 | 100% |
| `paint_enum_guarded.kara` | 130.4 ms ± 4.7 | 391% |

**The guard was never the kata's answer to the gap.** The shipped lane stayed in
its natural unconditional form and published 1.02×, because a kata twisted to
dodge a compiler bug has stopped doing its job. The probe turned "does not fan
out" into a number, which is what made the ledger row actionable.

## What it is for now

The bug is fixed (`c04bc65`: the floor is capped at the static-split size, so it
can never reduce the chunk *count* below the number of workers waiting to pull
one). Re-measured after the fix:

|  | time |
|---|---:|
| `../paint_enum.kara` (as written) | 121.1 ms ± 8.8 |
| `paint_enum_guarded.kara` | 137.9 ms ± 19.2 |

The natural shape is now **1.14× faster** than the guarded one, which is the
expected ordering — the dynamic pull loop should beat a static split on 16
uneven branches.

Keep it as a regression witness: **if the guarded variant ever pulls materially
ahead of the natural shape again, the chunker floor has regressed.**
