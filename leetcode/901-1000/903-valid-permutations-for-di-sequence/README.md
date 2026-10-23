# 903. Valid Permutations for DI Sequence

You are given a string `s` of length `n` where `s[i]` is either `'D'`
(decreasing) or `'I'` (increasing).

A permutation `perm` of `n + 1` integers of all the integers in the
range `[0, n]` is called a valid permutation if for all valid `i`: if
`s[i] == 'D'`, then `perm[i] > perm[i + 1]`, and if `s[i] == 'I'`, then
`perm[i] < perm[i + 1]`.

Return the number of valid permutations `perm`. Since the answer may be
large, return it modulo `10^9 + 7`.

```
s = "DID"  ->  5    (1032, 1302, 2031, 2130, 3021)
s = "D"    ->  1
```

**Constraints:** `1 <= n <= 200`, and `s[i]` is either `'I'` or `'D'`.

## Approaches

Only the order of the numbers placed so far matters, not their values,
so four arms build the permutation from the left and keep, for each
rank the last number can have among those so far, the number of orders
that fit the letters; the fifth places the largest number first.

| file | mechanism |
|---|---|
| `num_perms_di_sequence.kara` ★ | ranks of the last number, with running sums: a new number after an `'I'` takes rank `j` when the old last ranked below `j`, after a `'D'` when it ranked `j` or above, and a running sum over the old row gives each in O(1). O(n^2) |
| `num_perms_di_sequence_cubic.kara` | the same table with every entry summed over the old row afresh. O(n^3) |
| `num_perms_di_sequence_rolling.kara` | one row, rewritten in place: running sums from the left after an `'I'`, from the right after a `'D'`, the row growing by one place a letter. O(n^2) time, O(n) space |
| `num_perms_di_sequence_memo.kara` | the ranks asked for recursively from the end, each entry the one beside it plus one term of the row above, remembered. O(n^2) |
| `num_perms_di_sequence_interval.kara` | where the largest number goes: it sits after an `'I'` (or first) and before a `'D'` (or last), the two sides then fit their own letters, and which numbers go left is free, a binomial. O(n^3) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and eight
more (`I`, `III`, `DDD`, `ID`, `DI`, `IDID`, `DDIDI` and `IIDDII`); for
120 random cases of up to 200 letters, with `'D'` from none to every
letter, a checksum of the counts; and two of LeetCode's largest, 200
random letters and 200 alternating. `num_perms_di_sequence.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every permutation of `0` to `n` built from the numbers not
yet used, and each whole one checked against every letter. It checks
3,200 random cases: 3,000 of up to 5 letters against the statement and
200 of up to 40 letters against the other properties, with `'D'` from
none to every letter; 12,858 letters in all.

| | property |
|---|---|
| P1 | the statement's count, on the small cases |
| P2 | the same count with every letter flipped, as `n - perm[i]` turns each fitting permutation into one for the flipped letters |
| P3 | the same count with the letters reversed |
| P4 | the counts with an `'I'` and with a `'D'` at one place sum to `C(n + 1, at + 1)` times the counts of the two sides, since together they allow every order between the sides |
| P5 | a letter of either kind after the rest, or before it, gives `n + 2` times the count |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 12858
letters, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the running sums missing the old top rank | P1 3000, P4 644, P6 3200 |
| M2 | ★: the first number counted twice | P1 3000, P4 3200, P6 3200 |
| M3 | ★: the last letter never read | P1 1165, P3 823, P4 2402, P5 3200, P6 1304 |
| M4 | cubic: after an `I`, the old last at rank `j` allowed | P1 2070, P2 3020, P3 630, P4 3159, P5 3200, P6 2238 |
| M5 | cubic: after a `D`, the old last at rank `j` not allowed | P1 2095, P2 2852, P3 691, P4 2069, P5 2244, P6 2266 |
| M6 | cubic: the new number never the largest | P1 2070, P2 3200, P3 924, P4 2302, P5 3200, P6 2238 |
| M7 | rolling: after an `I`, the zero put at the top | P1 2070, P2 3020, P3 630, P4 3159, P5 3200, P6 2238 |
| M8 | rolling: after a `D`, the zero put at the bottom | P1 2095, P2 3020, P3 593, P4 3163, P5 3200, P6 2266 |
| M9 | rolling: after a `D`, the bottom place never summed | P1 848, P2 1304, P3 1079, P4 1925, P5 3200, P6 984 |
| M10 | memo: the top rank never counted | P1 3000, P6 3200 |
| M11 | memo: after an `I`, the old last taken at rank `j` | P1 2070, P2 3020, P3 630, P4 3159, P5 3200, P6 2238 |
| M12 | memo: after a `D`, a rank skipped in the sum | P1 848, P2 1304, P3 1079, P4 1938, P5 3200, P6 984 |
| M13 | interval: the largest after a `D`, not an `I` | P1 3000, P2 1896, P6 3200 |
| M14 | interval: which numbers go left never chosen | P1 848, P2 1079, P3 1079, P4 1938, P5 3200, P6 984 |
| M15 | interval: the right side counted as one way | P1 492, P2 936, P3 573, P4 1201, P5 1936, P6 621 |

P1 and P6 kill all fifteen. M10 counts nothing at all, since the first
number's only rank is the top one, and a count of 0 everywhere keeps
every relation P2 to P5 states, so only the statement and the agreement
see it. M2 doubles every count, which keeps P2, P3 and P5, all linear in
the count, but not P4, whose right side multiplies two counts. Three
mutants in three arms fail exactly the same cases (M4, M7, M11): each
lets the number after an `'I'` take the old last's own rank, summing
the old row up to `j` rather than below it. P5 kills eleven, all but M1, M2,
M10 and M13.

Two mutants were replaced. The first M8 and M9 started the rolling
arm's running sums one place in from the new zero, and so were
equivalent: the zero just put in adds nothing to the place beside it.

## Verification

Every arm prints the same output as `num_perms_di_sequence.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.6 to 23 s
each (the two O(n^3) arms, cubic and interval, take 23 and 20 s, the
others 3 s or less) and the differential 15 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy lanes split. The memo and interval arms print the same
output under the legacy interpreter; the legacy JIT and both legacy
builds, with and without auto-par, stop at codegen with `no handler for
method 'to_string' on variable 's' in show`, the harness function that
prints each example. Every legacy lane refuses the ★, cubic and rolling
arms, the differential and the bench program: `*w` (or `*c`) on an
element of `.iter()` is rejected, because legacy's iterator gives the
value itself. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on one string of 4,000 random letters,
twenty times LeetCode's largest so that each count takes long enough to
time, built once. Each round counts its valid permutations, folds the
count into a checksum and flips one letter; 12 rounds. Every
implementation allocates two new rows a letter, as the arm does. Every
implementation prints `12 rounds over 4000 letters: checksum
133543825`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.45 to 0.50 s | 0.48 s |
| Rust (`rustc -O`) | 0.45 to 0.51 s | 0.47 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.47 to 0.50 s | 0.49 s |
| Go | 1.05 to 1.19 s | 1.12 s |
| Python | 17.0 s | |
| Kāra (`karac build --mir`) | 0.65 to 0.70 s | 0.69 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 1.41 times Rust's median time under overflow checks and 1.44
times C's. Under valgrind's cachegrind C runs 3.81 billion instructions
and 1.96 billion branches, Rust with overflow checks 4.37 billion and
2.23 billion, and v2 4.49 billion and 1.97 billion; none mispredicts
more than a million. So v2 runs 3% more instructions than Rust with
overflow checks but takes 41% longer; which instructions cost the
difference was not profiled. The comparison with C and Rust waits until
after M4.
