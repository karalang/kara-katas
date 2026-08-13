# Intra-Kāra probe: where the prefix copying goes

Not a benchmark lane — a two-program measurement of the claim in the kata's
README, kept because the claim was wrong the first time it was written.

Both programs build the **same pure left spine** (depth n, exactly one leaf) and
produce its single root-to-leaf path. They differ only in how the path is
carried.

| n = 12,000, one round | time | peak RSS |
|---|---|---|
| `string_walk.kara` — String extended at every node | 0.29 s | **355 MB** |
| `join_walk.kara` — `Vec[i64]`, rendered once at the leaf | 0.00 s | **4.7 MB** |

**The dominant cost is memory, not copying.** Every recursion frame keeps its own
prefix alive for the duration of the call below it, so on a spine the string walk
holds O(depth²) bytes *simultaneously* — 12,000 frames averaging ~6,000 chars.
The join walk holds one `Vec[i64]`: O(depth).

That is also why the workload does not scale the way the copying argument alone
predicts. At n = 24,000 the string walk needs ~1.4 GB and takes **67 s**, against
the ~1.2 s an n² extrapolation from n = 12,000 would suggest — it is thrashing,
not computing.

## What was wrong the first time

The kata README originally said the join form is O(leaves · depth) and therefore
O(n) "on a path-shaped tree". True only for a tree with ONE leaf. The first
generator here branched 4% of the time, which yields ~0.04n leaves — so
`leaves · depth` is 0.04n · n, quadratic, and **both** walks measured n²:

```
n=3000   string 0.02s   join 0.01s
n=6000   string 0.08s   join 0.07s
n=12000  string 0.31s   join 0.27s
```

Four percent branching was enough to erase the entire distinction the kata is
about. The generator is now a pure spine, and the numbers separate by ~75× on
memory.

```bash
karac build string_walk.kara && /usr/bin/time -v ./string_walk
karac build join_walk.kara   && /usr/bin/time -v ./join_walk
```
