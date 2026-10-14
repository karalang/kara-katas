# 599. Minimum Index Sum of Two Lists

Given two arrays of strings `list1` and `list2`, find the common strings
with the least index sum. A common string is a string that appeared in
both `list1` and `list2`. A common string with the least index sum is a
common string such that if it appeared at `list1[i]` and `list2[j]` then
`i + j` should be the minimum value among all the other common strings.
Return all the common strings with the least index sum. Return the
answer in any order.

```
list1 = ["Shogun","Tapioca Express","Burger King","KFC"],
list2 = ["Piatti","The Grill at Torrey Pines","Hungry Hunter Steakhouse","Shogun"]  ->  ["Shogun"]
list1 = ["Shogun","Tapioca Express","Burger King","KFC"],
list2 = ["KFC","Shogun","Burger King"]  ->  ["Shogun"]
list1 = ["happy","sad","good"], list2 = ["sad","happy","good"]  ->  ["sad","happy"]
```

**Constraints:** `1 <= list1.length, list2.length <= 1000`; `1 <=
list1[i].length, list2[i].length <= 30`; `list1[i]` and `list2[i]`
consist of spaces `' '` and English letters; all the strings of
`list1` are unique; all the strings of `list2` are unique; there is at
least a common string between `list1` and `list2`.

## Approaches

Every arm is `fn find_restaurant(list1: Vec[String], list2: Vec[String])
-> Vec[String]`. The parameters are bare, so the lists are borrowed;
every string in the answer is a clone.

| file | mechanism |
|---|---|
| `find_restaurant.kara` ★ | a `Map[String, i64]` from each string of `list1` to its index, then one walk of `list2`: a string found there with a smaller sum starts the answer over, and one with an equal sum joins it; O(n + m) expected, times the strings' length |
| `find_restaurant_pairs.kara` | every string of `list1` against every string of `list2`, the least sum kept the same way; O(n * m) comparisons |
| `find_restaurant_bysum.kara` | the sums tried in increasing order, 0, 1, 2 and on: for a sum s, every i with j = s - i inside `list2`; the first sum with a match gives the whole answer; O((n + m) * n) at worst |
| `find_restaurant_merge.kara` | each list paired with its indexes and sorted by string, then one merge walk that meets the common strings in order; O((n + m) log(n + m)) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the problem's three examples; five
cases at the edges (one string each, a list against its reverse, where
every string ties, the one common string last in both, strings that
differ only by case, and a string first in `list1` that loses to two
nearer the middle of both); two at the problem's longest, 1,000 names
each sharing only the last, and 1,000 against the same in reverse, where
all 1,000 tie; and a count and checksum over 300 random cases. The
answer may come in any order, so the harness sorts it before printing.
Every name is letters and spaces, as the constraints say, numbers
spelled in letters. `find_restaurant.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read word by word: the common strings are those of
`list1` that `list2` also holds; each one's index sum is where it stands
in `list1` plus where it stands in `list2`, both found by search; the
answer is the common strings whose sum is the least of them. It uses no
map, no sort of the lists and no walk by sums. Every answer is sorted
before it is compared. Each of 1,000 random cases has 1 to 8 names in
each list out of ten that differ by case, by length and by order (`a`,
`b`, `ab`, `ba`, `abc`, `A`, `B`, `aa`, `c`, `ca`), one name of
`list1` put into `list2` when they share none; 103 of them have a tie.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the two lists swapped give the same strings |
| P3 | one more string, the last of both lists, changes nothing |
| P4 | one more string, the first of both lists, is the whole answer |
| P5 | one more string at the front of `list1` only raises every sum by one and changes nothing |

It prints `1000 cases (103 with a tie), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie starts the answer over | P1 103, P2 103 |
| M2 | ★: a smaller sum keeps the answer so far | P1 158, P2 292 |
| M3 | pairs: the last string of `list2` never compared | P1 257, P2 359, P3 257 |
| M4 | pairs: the least sum starts at `list1`'s length | P1 131, P2 234, P3 52 |
| M5 | bysum: the sums stop below the longer list's length | P1 48, P3 37, P5 50 |
| M6 | bysum: index 0 of `list2` skipped | P1 460, P2 588, P3 231, P4 1000 |
| M7 | merge: the larger side advanced | P1 565, P2 548, P4 799 |
| M8 | merge: the lists not sorted | P1 613, P3 442, P5 558 |
| E1 | ★: the map filled by `insert` | 0 |
| E2 | pairs: the string pushed from `list2` | 0 |
| E3 | bysum: one sum more than the largest | 0 |
| E4 | merge: only `list1`'s side advanced on a match | 0 |

M1 keeps only the last of the strings that tie, so it fails exactly the
103 cases with a tie, against the definition and again when the lists
are swapped, which changes which tied string comes last. P3, P4 and
P5 compare an arm with itself, so they see a mutant only when its
mistake moves with the edit: P4 puts the new string at index 0 of both
lists, the one place M6 never looks, and so fails it on every case;
P5 raises every sum by one, which pushes some answers past the limit
M5 stops at. E2 is safe because a match pushes two equal strings;
E3 because no pair reaches the extra sum; E4 because the strings of
`list1` are unique, so after a match the next step advances `list2`'s
side anyway.

## Verification

Every arm prints the same output as `find_restaurant.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`286748264f`.

The frozen legacy backends do not all agree. Every arm prints the same
output under `karac run --interp`, but `karac run` and `karac build`
stop with a panic in legacy's code generation
(`src/codegen/method_call.rs`) on every arm. The arms build inside the
differential, so the panic is in code only the test harness has. The
differential prints its line under `karac run --interp`; built by `karac
build` it stops with `free(): double free detected` before printing. The
bench program builds and prints the same line. Legacy is frozen, so
these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes a pool of 3,000 names of up
to 25 letters and spaces once, and from it 100 pairs of lists of
1,000 different names each, the problem's longest, 299 to 373 of them
shared in each pair, about a third; then 100 times over it solves every
pair. Every implementation prints `100 pairs, 100 rounds: total
10300, checksum 633889845`, the Kāra program under `karac __mir-run`
included (77 s).

Each implementation is the same algorithm over a hash table: Rust a
`HashMap<String, usize>` with its default SipHash-1-3, the same hash as
Kāra's `Map`, its keys and answer cloned as the Kāra arm's are; Go a
built-in `map[string]int`, whose strings share their bytes and are not
copied; C an open-addressing table hashed by FNV-1a, its keys and answer
`malloc`'d copies freed at the end of each call; Python a `dict`. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.53 to 1.67 s |
| Rust (`rustc -O`) | 1.85 to 1.92 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.73 to 1.82 s |
| Go | 1.36 to 1.56 s |
| Python | 1.45 to 1.62 s |
| Kāra (`karac build`, legacy) | 2.19 to 2.32 s |
| Kāra (`karac build --mir`) | 1.69 to 1.73 s |

Both Kāra rows are at kara `286748264f`; the v2 compiled backend is
about 1.3 times faster than legacy here. Under `karac __mir-llvm-run`
the program prints the same line in 15.4 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark.

Every row is within a few tenths of a second of the others, Python's
included. Each call builds a fresh table of 1,000 strings and looks
1,000 up; in a callgrind profile of the C program at 10 rounds, 45% of
its instructions are in `malloc` and `free`, building the lists
included. A copy of the C program whose lists share the pool's
3,000 strings, as Go's and Python's do, runs in the same 1.52 to 1.56 s,
so the copies held in the lists are not what costs. Python keeping up is
likely because a Python string keeps its hash once computed, so a lookup
with one of the pool's strings does not hash it again; that is not
measured.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
