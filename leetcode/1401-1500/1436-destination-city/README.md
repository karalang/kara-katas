# 1436. Destination City

You are given the array `paths`, where `paths[i] = [cityAi, cityBi]`
means there exists a direct path going from `cityAi` to `cityBi`. Return
the destination city, that is, the city without any path outgoing to
another city. It is guaranteed that the graph of paths forms a line
without any loop, therefore, there will be exactly one destination city.

```
paths = [["London","New York"],["New York","Lima"],["Lima","Sao Paulo"]]   ->  "Sao Paulo"
paths = [["B","C"],["D","B"],["C","A"]]                                     ->  "A"
paths = [["A","Z"]]                                                         ->  "Z"
```

**Constraints:** `1 <= paths.length <= 100`, `paths[i].length == 2`, `1
<= cityAi.length, cityBi.length <= 10`, `cityAi != cityBi`, all strings
consist of lowercase and uppercase English letters and the space
character.

Each arm is `fn dest_city(paths: Vec[Vec[String]]) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `dest_city.kara` ★ | every city a path leaves from in a `Set[String]`, and the first city a path reaches that is not in it, by `find`. O(n) |
| `dest_city_follow.kara` | each city's next city in a `Map[String, String]`, and the trip followed from the first path's city by `while let Some(after) = next.get(city)` until a city has no next. O(n) |
| `dest_city_brute.kara` | each path's end tried against every path's start, the first end no path starts from. O(n²) |
| `dest_city_sorted.kara` | the cities reached and the cities left, each a `SortedSet[String]` collected from the paths, and the one city in the `difference`. O(n log n) |
| `dest_city_solution.kara` | a Rust solution as LeetCode's Rust users write it (`use std::collections::HashSet`, the starts gathered into a `HashSet<&String>` by `map(\|p\| &p[0])`, each end looked up by `contains(&p[1])`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and one
more, a name that begins another (`Sao Paulo,A,Z,pq`); the constraints'
most, 100 paths through cities of up to 10 letters, and through cities
of up to 10 of two letters (`100 paths: HT BBABBBB`); and 2000 random
trips of 1 to 100 paths, the names of 1 to 10 letters of the first 2 to
26 of the alphabet, the paths in a drawn order (`2000 random trips: 7106
letters, checksum 371087762`). `dest_city.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, follow and brute arms check clean as first
written. The sorted arm took the first city of the `difference` by
`.next()`, which `karac check` refuses, saying Kāra's `difference` gives
a `SortedSet`, not Rust's iterator, and `karac fix` writes
`.into_iter().next()`, 1 fix. The Rust solution takes one round of 17
fixes by `karac fix`'s count: the `use` line deleted, `Set` being in the
prelude, `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]` and `HashSet<&String>` to `Set[ref String]`, `&p[0]` to `ref
p[0]`, `!` to `not`, `contains(&p[1])` to `contains(p[1])`,
`String::new` to `String.new`, and `Solution::` to `Solution.`. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every city named in a path, at either end, and the one with
no path out of it to another city. LeetCode's examples, five edge cases
(one path, one name the start of another, names that differ only in
case, a name with spaces in it, and a trip given end first), the
constraints' most two ways (100 paths through cities of up to 10
letters, and of up to 10 of two letters), and 1992 random trips drawn as
the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the paths in the other order give the same city |
| P3 | a path on from the answer to a new city gives the new city |
| P4 | some path's end, and no path's start |
| P5 | every name with a dash after it gives the answer with one |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 cases: checksum 916160885,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by the ends less
the starts as sets, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the first path's start left out of the starts | P1 845, P2 1478, P3 1840, P4 845, P6 3380 |
| M2 | ★: a one-letter city taken as the answer whatever its paths | P1 1478, P2 1846, P3 1895, P4 1478, P5 1478, P6 5912 |
| M3 | follow: the trip followed one step only | P1 1815, P2 1954, P3 2003, P4 1815, P6 1815 |
| M4 | follow: the trip followed backwards, to where it began | P1 2003, P3 2003, P4 2003, P6 2003 |
| M5 | brute: each end matched against the ends, not the starts | P1 2003, P3 2003, P4 2003, P5 2003, P6 2003 |
| M6 | brute: the first path's start never tried | P1 845, P2 1478, P3 1840, P4 845, P6 845 |
| M7 | sorted: the city left and never reached, where the trip began | P1 2003, P3 2003, P4 2003, P6 2003 |
| M8 | sorted: the first path's start left out of the cities left | P1 954, P2 1297, P4 954, P5 1, P6 954 |
| M9 | solution: the first end that some path starts from | P1 2003, P2 1907, P3 2003, P4 2003, P5 49, P6 2003 |
| M10 | solution: the path's start given for its end | P1 2003, P3 2003, P4 2003, P6 2003 |

## Benchmarks

The bench draws 1000 trips of 100 paths through cities of 10 letters,
each trip's paths turned round by a drawn place, and asks each trip's
destination 100 times, folding the answers to a checksum. Each
implementation copies the starts into a fresh hash set, as the ★ arm
clones each into a `Set[String]`, except Go's, whose `map[string]bool`
keeps the strings it is given; the C bench copies them into a set of its
own, open addressing over 256 slots. Every implementation prints `10^5
trips of 100 paths: checksum 88072598`.

BENCHTAB

Measured by hand, Kāra takes 1.01 to 1.03 s against Rust's 0.93 s (0.93
to 0.94 s with overflow checks on), C's 0.60 to 0.61 s and Go's 0.58 to
0.63 s; Python takes 1.2 s.
