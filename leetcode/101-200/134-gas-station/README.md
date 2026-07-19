# 134. Gas Station

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Greedy &nbsp;·&nbsp; **Source:** [leetcode.com/problems/gas-station](https://leetcode.com/problems/gas-station/)

`n` stations in a circle; `gas[i]` fills the tank, `cost[i]` is the gas to reach `i+1`. Return the starting index from which you can complete the loop once (unique if it exists), else `-1`.

```
gas=[1,2,3,4,5], cost=[3,4,5,1,2]  ->  3
gas=[2,3,4],     cost=[3,4,3]      -> -1
```

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ gas[i], cost[i] ≤ 10⁴`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Greedy single pass** ★ | O(n) time, O(1) space | [`gas_station.kara`](gas_station.kara) ✓ | [`gas_station.py`](gas_station.py) ✓ |

`✓` runs end-to-end today: interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`) all agree with the Python mirror. Validated against known cases (3, -1, single-station 0) plus deterministic-LCG inputs. Zero diagnostics, valgrind-clean.

## The mechanism

Two running sums in one pass. `total` accumulates `gas[i] - cost[i]` over the whole ring — the trip is feasible iff `total ≥ 0`. `tank` is the running balance from the current candidate start; the moment it dips below zero, **no** station from the candidate up to `i` can be the true start (each was reached with non-negative tank, so dropping the prefix only helps), so the candidate jumps to `i + 1` and `tank` resets. The last surviving candidate is the unique answer. O(n), O(1).

## Kāra features exercised

- **Two owned `Vec[i64]` inputs** consumed by value into the greedy scan (`gas[i] - cost[i]`).
- **`mut ref i64` sink accumulator** threaded into a `report` helper (`report(g, c, mut sink)` — the fresh-binding call-site `mut` marker).
- **Overflow-checked running sums** — `total` / `tank` under kāra's default trap.

## Running

```bash
karac run   gas_station.kara
karac build gas_station.kara && ./gas_station
python3 gas_station.py
diff <(karac run gas_station.kara) <(python3 gas_station.py) && echo OK
```

## Notes

Dogfood-first greedy kata; the O(n) single-pass shape over two `Vec[i64]` inputs is verified across every surface.
