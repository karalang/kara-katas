# 465. Optimal Account Balancing

You are given an array of transactions `transactions` where
`transactions[i] = [fromi, toi, amounti]` indicates that the person with
`ID = fromi` gave `amounti $` to the person with `ID = toi`. Return the
minimum number of transactions required to settle the debt.

```
transactions = [[0,1,10],[2,0,5]]                    ->  2
transactions = [[0,1,10],[1,0,1],[1,2,5],[2,0,5]]    ->  1
```

**Constraints:** `1 <= transactions.length <= 8`;
`0 <= fromi, toi < 12`; `fromi != toi`; `1 <= amounti <= 100`.

## Approaches

Every arm is `fn min_transfers(transactions: Vec[(i64, i64, i64)]) ->
i64`. Only each person's net balance matters, and the people already
even drop out. With `k` people left unsettled, `k - 1` transfers always
do (each one settles someone), and a group whose balances add up to
zero can be settled on its own; so the answer is `k` less the most
disjoint zero-sum groups the people split into.

| file | mechanism |
|---|---|
| `min_transfers.kara` ★ | backtracking: the first unsettled person passes their whole balance to someone of the opposite sign; try each such partner, settle the rest, undo, and keep the fewest transfers |
| `min_transfers_groups.kara` | bottom up over every subset of the unsettled people as a bitmask: the most zero-sum groups in a subset is the most in it without one member, plus one if the subset adds up to zero. O(2^k × k) |
| `min_transfers_split.kara` | top down: the lowest person left belongs to some zero-sum group, so try every subset of the people left that holds them and adds up to zero, and split the rest the same way; the best count per set of people left is kept in a `Vec` indexed by its bitmask |
| `min_transfers_bfs.kara` | breadth first over the balances still open, with the ★ arm's move; positions are sorted and kept in a `Set[Vec[i64]]` so the same balances in another order count once. The first level with nothing open is the answer |
| `differential.kara` | the four arms on 1,500 random ledgers, five properties |

Every arm prints the same 10 lines: the two LeetCode examples, one
transfer, a transfer and its reverse, a chain, three separate pairs, a
fan into one person, five transactions that split into two groups, a
loop of 100 beside four pairs of 1, and for 300 random ledgers of 1 to 8
transactions among people 0 to 11 (amounts up to 3, 10 or 100) the
total of the answers and a checksum. `min_transfers.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random ledgers.

| | property |
|---|---|
| P1 | on up to 4 transactions, the answer is brute force's: the unsettled people less the most blocks over every partition of them whose blocks all add up to zero |
| P2 | renaming the people (a random shuffle of 0 to 11) keeps the answer |
| P3 | multiplying every amount by 2 to 5 keeps it, and so does reversing every transaction |
| P4 | adding a transaction and its reverse keeps it, and so does splitting a transaction in two of the same direction |
| P5 | two ledgers among different people, the second with every amount times 1,000, take the sum of their answers |

P5 first said that any two ledgers among different people take the sum
of their answers, and every arm failed it the same way: people from the
two ledgers can form a zero-sum group together (balances `2, -1, -1`
and `1, 1, -2` take 2 transfers each, but 3 together). Multiplying one
ledger's amounts by 1,000, more than any of the other's balances can
add up to, keeps their groups apart.

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tried transfer is not undone | P1 292, P2 462, P5 921 |
| M2 | ★: the most transfers is kept | P1 291, P2 13, P5 1496 |
| M3 | groups: a zero-sum subset adds no group | P1 1482 |
| M4 | groups: a subset looks only at itself without its last member | P1 244, P2 198 |
| M5 | split: a group need only add up to zero or more | P1 168, P2 264, P3 316, P5 337 |
| M6 | split: the first person's balance is left out of every sum | P1 93, P2 168, P5 1496 |
| M7 | bfs: the first balance always goes to the second | P1 348, P5 1496 |
| M8 | bfs: the first balance only goes to the largest | P1 17 |

P1, the only property with an independent answer, sees all eight. P4
sees none, and P3 sees only M5: their changes leave the balances as
they were, or scaled, or negated, and these mutants' wrong answers
follow the balances. P2 renames the people, which reorders the
balances, so it sees the mutants whose answer depends on that order.
M8, settling always with the largest creditor, is caught by P1's
brute force alone.

Letting the ★ arm or the breadth-first arm pass a balance to someone of
the same sign was not used as a mutant: it only adds ways to settle,
none of them shorter, so it cannot change the answer.

## Verification

All four arms print the same output as `min_transfers.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`. LLJIT and `karac build` stop in the legacy code
generator on the harness's index into an array literal ("Index operator
applied to non-array type"), in every arm. The legacy type checker
rejects the differential, which reads loop items through `*x` where v2
lends them by reference. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm on 20,000 random ledgers of 8
transactions among people 0 to 11, with amounts 1 to 3 so that
zero-sum groups are common, each settled from scratch. Every
implementation prints `20000 ledgers of 8 transactions: 104931
transfers in all, checksum 193047123`, the Kāra program under
`karac __mir-run` included (in 148 s).

Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.54 to 0.67 s |
| Rust (`rustc -O`) | 0.63 to 0.64 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.64 to 0.69 s |
| Go | 0.71 to 0.79 s |
| Python | 20.1 to 20.8 s |
| Kāra (legacy `karac build`) | 0.60 to 0.62 s |
| Kāra (`karac build --mir`) | 0.75 to 0.85 s |

`bench.sh` builds with legacy `karac build`. The `--mir` row is timed at
kara `5f01de4c5c`. Under `karac __mir-llvm-run` the program prints the
same line in 2.1 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
