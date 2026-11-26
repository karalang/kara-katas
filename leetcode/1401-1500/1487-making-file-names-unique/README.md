# 1487. Making File Names Unique

Given an array of strings `names` of size `n`. You will create `n`
folders in your file system such that, at the `i`th minute, you will
create a folder with the name `names[i]`. Since two files cannot have
the same name, if you enter a folder name that was previously used, the
system will have a suffix addition to its name in the form of `(k)`,
where `k` is the smallest positive integer such that the obtained name
remains unique. Return an array of strings of length `n` where `ans[i]`
is the actual name the system will assign to the `i`th folder when you
create it.

```
["pes","fifa","gta","pes(2019)"]                              ->  ["pes","fifa","gta","pes(2019)"]
["gta","gta(1)","gta","avalon"]                               ->  ["gta","gta(1)","gta(2)","avalon"]
["onepiece","onepiece(1)","onepiece(2)","onepiece(3)","onepiece"]  ->  [.., "onepiece(4)"]
["wano","wano","wano","wano"]                                 ->  ["wano","wano(1)","wano(2)","wano(3)"]
["kaido","kaido(1)","kaido","kaido(1)"]                       ->  ["kaido","kaido(1)","kaido(2)","kaido(1)(1)"]
```

**Constraints:** `1 <= names.length <= 5 * 10^4`, `1 <= names[i].length
<= 20`, and `names[i]` consists of lowercase English letters, digits
and/or round brackets.

The arms are `fn get_folder_names(names: Vec[String]) -> Vec[String]`.

## Approaches

| file | mechanism |
|---|---|
| `get_folder_names.kara` ★ | one `Map` from each name taken to the next suffix worth trying for it: a new name is taken as it is; a taken one tries `name(k)` from its remembered k up, takes the first free one, and remembers where it stopped. O(total length) amortized |
| `get_folder_names_set.kara` | the names taken kept in a `Set`, and apart from it a `Map` of where each name's suffix search last stopped, filled only for names that needed one |
| `get_folder_names_sorted.kara` | the one-map approach over a `SortedMap`, so the names taken are also held in order; each suffix candidate built by `push_str` onto a copy of the name |
| `get_folder_names_entry.kara` | every name's counter reached through `entry(..).or_insert(0)` inside a `map` closure: a name's first use takes it as it is, and every later one walks its counter past the made names already taken |
| `get_folder_names_solution.kara` | a Rust solution as LeetCode's Rust users write it (`HashMap<String, i32>`, `if let Some(&k) = map.get(&name)`, `format!("{}({})", name, k)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 8 lines: LeetCode's five examples, one to a
line; four edges, one name, a name that already looks made, twice, a
made name taken before the system makes it, and a suffix past 9 (`a |
a(1),a(1)(1) | a,a(1),a(1)(1) | b,b(1),..,b(10),b(10)(1),b(11)`); the
constraints' most, 50000 copies of one name and 50000 names drawn from
300 base names with up to two suffixes, the folders' text hashed in
order (`50000 names: last x(49999), checksum 335600114 | checksum
632753204`); and 2000 random lists of 1 to 30 names from 1 to 6 base
names (`2000 random lists: checksum 775616894`). `get_folder_names.py`
mirrors the ★ arm, and its output is byte-identical. The maps are only
looked up, never walked, so no output depends on their order. Every arm
gives the same output under `karac __mir-run`, `karac run`, `karac
build` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 26 fixes by `karac fix`'s count, and its
diff is: `use std::collections::HashMap;` deleted, since `Map` is in the
prelude, `struct Solution;` to `struct Solution {}`, each `Vec<String>`
to `Vec[String]`, the parameter to `names: own Vec[String]`, since `for
name in names` consumes it, and that loop to `names.into_iter()`,
`HashMap<String, i32>` and `HashMap::new()` to `Map[String, i32]` and
`Map.new()`, `Vec::with_capacity` to `Vec.with_capacity`, `if let
Some(&k) = map.get(&name)` to `if let Some(k) = map.get(name).cloned()`,
each `format!("{}({})", name, k)` to `f"{name}({k})"`, `&new_name` to
`new_name` and `Solution::` to `Solution.`. Every arm's output matches
on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each name taken as it is when no folder made so far has it,
else with the smallest `k` from 1 up that makes it new, searched over a
`Vec` of the folders. LeetCode's examples, the edges, and 1991 random
lists of 1 to 12 names from 1 to 4 base names, each with up to two
suffixes, so the names drawn collide with the ones made. Each arm meets
six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | one folder for each name, all of them different |
| P3 | each folder is its name, or its name with a suffix `(k)`, k from 1 and written without a leading 0 |
| P4 | the first names alone, a random count of them, get the same folders |
| P5 | a name keeps its own text exactly when no earlier folder has it |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 824482774,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, searching a list
of the folders made, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a made name never remembered as taken | P1 371, P2 371, P5 371, P6 1484 |
| M2 | ★: the search starts one past where it stopped | P1 1340, P6 5360 |
| M3 | set: a name's first suffix tried is 2 | P1 1323, P6 1323 |
| M4 | set: the name asked for recorded, not the one made | P1 371, P2 371, P5 371, P6 371 |
| M5 | sorted: the suffix closed with `]` | P1 1406, P3 1406, P6 1406 |
| M6 | sorted: the search starts one past where it stopped | P1 1340, P6 1340 |
| M7 | entry: a name's second use takes it as it is | P1 1406, P2 1406, P5 1406, P6 1406 |
| M8 | entry: a made name never remembered as taken | P1 371, P2 371, P5 371, P6 371 |
| M9 | solution: the search steps two suffixes at a time | P1 513, P6 513 |
| M10 | solution: a made name's own next suffix starts at 2 | P1 361, P6 361 |

## Benchmarks

The bench draws 50000 names once from 3000 base names, a third of them
with a suffix `(1)` to `(3)`; then makes 20 passes, each punching one
name and making every folder with the ★ arm, both chosen from the
checksum so far. Kāra's `Map` and Rust's `HashMap` both hash by
SipHash-1-3, and Go's map by its own hash; C has no map, so its mirror
keeps the names in an open-addressing table keyed by FNV-1a, grown at
half full, and builds each candidate with `snprintf`. Every
implementation prints `20 passes over 50000 names: checksum 384689460`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.39 s against Rust's 0.43 s (0.53 s with
overflow checks on), C's 0.52 s and Go's 0.74 s; Python takes 1.1 s.
