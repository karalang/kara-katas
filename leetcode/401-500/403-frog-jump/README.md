# 403. Frog Jump

A frog crosses a river on stones. `stones` lists their positions in
increasing order, and the first is 0. The frog starts on the first stone
and its first jump is 1 unit. If its last jump was `k` units, the next
must be `k - 1`, `k` or `k + 1`, always forward, and it must land on a
stone. Return whether it can reach the last stone.

```
stones = [0,1,3,5,6,8,12,17]  -> true   (jumps 1, 2, 2, 3, 4, 5)
stones = [0,1,2,3,4,8,9,11]   -> false  (the gap from 4 to 8 is too wide)
```

**Constraints:** `2 <= stones.length <= 2000`; `0 <= stones[i] <=
2^31 - 1`; `stones[0] == 0`, and the positions increase.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `frog_jump.kara` ★ | the jump sizes that reach each stone: a `Map` from a stone's position to a `Set` of jump sizes; walking the stones in order, each size `k` on stone `s` adds `k - 1`, `k` and `k + 1` to the stones they land on | O(n^2) | O(n^2) |
| `frog_jump_memo.kara` | depth-first search over states (stone, last jump), trying the three jumps in turn, with a `Set` of states known to be dead ends | O(n^2) | O(n^2) |
| `frog_jump_table.kara` | a table `reached[i][k]`: stone `i` is reached with jump `k = stones[i] - stones[j]` from an earlier stone `j` reached with `k - 1`, `k` or `k + 1`; the jump leaving stone `j` is at most `j + 1`, which bounds the table | O(n^2) | O(n^2) |
| `frog_jump_bfs.kara` | breadth-first search over the same states, each visited once | O(n^2) | O(n^2) |
| `differential.kara` | the four arms on 3,000 random cases whose answers are known by construction, five properties | — | — |

Every arm prints the same 11 lines: the two LeetCode examples, eight
edge cases (two stones, a first gap of 2, jumps that grow by one each
time, three rivers of mixed gaps, a stone too far away, every position
from 0 to 19), and for 2,000 random rivers of 2 to
60 stones, with gaps from 1 to 4 after the first stone, how many are
crossed and a checksum of which. `frog_jump.py` mirrors the ★ arm and
its output is byte-identical.

The ★ arm copies a stone's jump sizes into a `Vec` before using them,
with `for k in jumps[*s].iter() { sizes.push(k); }`. The items of
`Set.iter()` are references, so the spec form is `sizes.push(*k)`.
`karac check` accepts that, but `karac __mir-run` refuses it as `found
'i64'` (kara `B-2026-10-12-9`, extended by this kata). Revert to `*k`
once it is fixed.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
cases builds five rivers whose answers are known without solving them:

| | property |
|---|---|
| P1 | a river of stones 0, 1, 2, ..., n - 1 is crossed |
| P2 | a river with a gap after stone `i` wider than `i + 1` is not crossed: the jump leaving stone `i` is at most `i + 1` |
| P3 | a river laid along a random legal path of jumps, with extra stones added off the path, is crossed |
| P4 | for up to 12 stones, the answer is that of a search that tries every sequence of jumps, with no memo |
| P5 | a crossed river stays crossed when stones are added before its last stone |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | sets: the jump `k + 1` is never tried | P1 3000, P3 3000, P4 1670 |
| M2 | sets: the first stone is reached with a jump of 1, so the first jump may be 2 | P2 80, P4 276 |
| M3 | memo: the jump `k - 1` is never tried | P3 927, P4 413 |
| M4 | memo: a dead end is recorded under the next jump size | P3 174, P4 155, P5 100 |
| M5 | table: a stone reached with jump `k + 1` cannot jump `k` | P3 927, P4 413 |
| M6 | table: the answer is read from the last stone but one | P2 205, P3 91, P4 228, P5 5 |
| M7 | bfs: a stone is visited once, whatever the jump that reached it | P3 179, P4 41, P5 32 |
| M8 | bfs: the river is crossed at the last stone but one | P2 205, P3 91, P4 228, P5 5 |

M3 and M5 are one mistake in two arms, the frog never slowing down, and
fail the same checks; so do M6 and M8. M2 lets every jump be one unit
longer than allowed, so P2 sees it only where the too-wide gap is
exactly one unit too wide.

## Verification

All four arms print the same output as `frog_jump.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints `60000
checks, 0 failures` under both. The table arm also matches under
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`. The frozen legacy typechecker refuses the other three and the
differential: it refuses `*s` on the items of `stones.iter()` and
`*next` on the result of `Map.get`, as in katas 382 to 401. Not filed.

## Benchmarks

The bench program uses the ★ arm on 600 random rivers of 2,000 stones
(the problem's limit), with gaps from 1 to 3 after the first stone,
built from an LCG; about half are crossed. It counts the rivers crossed
and folds their numbers into a checksum. Every implementation prints
`600 rivers of 2000 stones: 312 crossed, checksum 225473500`; a 6-river
cut of the Kāra program under `karac __mir-run` prints the same as the
C program cut the same way. C has no map or set type, so its mirror
carries an open-addressing table from position to stone and a growable
open-addressing set of jump sizes per stone; the others use their own
hash maps and sets. Spot timings on a shared 4-core container
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.4 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.9 s |
| Rust (`rustc -O`) | 1.9 s |
| Go | 3.4 s |
| Python | 5.2 s |

The Kāra program prints the same line under `karac __mir-llvm-run` in
52 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark. The legacy `karac build` refuses it,
as above.

## Compiler findings

- **`Set.iter()` items are values under `karac __mir-run`** (kara
  `B-2026-10-12-9`, extended): `for k in s.iter() { t += *k; }` passes
  `karac check` and is refused by the MIR builder as `found 'i64'`. The
  row covered destructured tuple items of `Vec` and `Map`; a plain
  `Set[i64]` item has the same split.
