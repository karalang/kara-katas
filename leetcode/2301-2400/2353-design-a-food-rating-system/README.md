# 2353. Design a Food Rating System

Design a food rating system that can do the following:

- **Modify** the rating of a food item listed in the system.
- Return the highest-rated food item for a type of cuisine in the system.

Implement the `FoodRatings` class:

- `FoodRatings(String[] foods, String[] cuisines, int[] ratings)`
  Initializes the system. The food items are described by `foods`,
  `cuisines` and `ratings`, all of which have a length of `n`.
  `foods[i]` is the name of the `i`th food, `cuisines[i]` is the type of
  cuisine of the `i`th food, and `ratings[i]` is the initial rating of
  the `i`th food.
- `void changeRating(String food, int newRating)` Changes the rating of
  the food item with the name `food`.
- `String highestRated(String cuisine)` Returns the name of the food
  item that has the highest rating for the given type of `cuisine`. If
  there is a tie, return the item with the **lexicographically smaller**
  name.

```
["FoodRatings", "highestRated", "highestRated", "changeRating", "highestRated", "changeRating", "highestRated"]
[[["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"],
  ["korean", "japanese", "japanese", "greek", "japanese", "korean"],
  [9, 12, 8, 15, 14, 7]],
 ["korean"], ["japanese"], ["sushi", 16], ["japanese"], ["ramen", 16], ["japanese"]]
->  [null, "kimchi", "ramen", null, "sushi", null, "ramen"]
```

**Constraints:** `1 <= n <= 2 * 10^4`; `1 <= foods[i].length,
cuisines[i].length <= 10`, lowercase letters; `1 <= ratings[i] <= 10^8`;
the foods are distinct; `food` is a food in the system and `cuisine` a
cuisine with at least one food; at most `2 * 10^4` calls in total.

A food keeps its cuisine for life, so each cuisine is its own ranking,
ordered by rating from the highest and then by name. Keying that
ranking on `(-rating, food)` makes the answer its least element. A
change must take the food's old key out, or the lazy way leaves it in:
every key a food was ever given stays in a min-heap, and a query throws
away the tops whose rating is no longer the food's. Each key is pushed
once per change and popped at most once, so the work is `O(log n)` per
call, amortized.

## Approaches

| file | mechanism |
|---|---|
| `ratings.kara` ★ | lazy heaps: a map from each food to its rating and its cuisine, and for each cuisine a min-first `PriorityQueue` of `(-rating, food)` holding every key a food was ever given; a change only pushes, and a query pops the tops whose rating is no longer the food's. O(log n) amortized |
| `ratings_set.kara` | sorted sets: a map from each food to its cuisine and rating, and for each cuisine a `SortedSet` of `(-rating, food)`; a change takes the old key out and puts the new one in, and a query reads the set's least. O(log n) |
| `ratings_naive.kara` | no index: the three lists kept as they came, with a map from each food to its place; a change writes one rating, and a query walks every food for the best of the cuisine. O(n) per query |
| `ratings_buckets.kara` | buckets: for each cuisine a `SortedMap` from a rating to the `SortedSet` of foods that hold it; a change moves the food between buckets, dropping one left empty, and a query takes the last bucket's least food. O(log n) |
| `ratings_iter.kara` | iterators: a map from each food to its cuisine and rating, built by `collect`; a query `filter`s it to the cuisine and takes `min_by_key` on `(-rating, food)`. O(n) per query |
| `ratings_solution.kara` | LeetCode's Rust template: a `HashMap` from each food to its cuisine and rating, a `BTreeSet<(i32, String)>` per cuisine through `entry(..).or_default()`, and the change written through `get_mut`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's example; three foods tied,
the least name answered as the ratings move; a food raised past another
and lowered back, at the constraints' largest rating; 500 foods over 20
cuisines and then `2 * 10^4` calls, two changes to every query, as a
checksum of the answers and their letters; then 2000 random scripts of
1 to 8 foods of 1 to 3 letters from `a` to `c` over cuisines `x`, `y`
and `z`, rated 1 to 4, and 1 to 40 calls, as a checksum, the letters,
and how often the first food was the answer. `ratings.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on
20000 random scripts against the statement read literally.

`check` first reports 14 errors on the template, and `karac fix`
carries it in one call, reporting 32 edits: the
`use std::collections::{BTreeSet, HashMap};` line deleted, since both
are in the prelude, with `HashMap` written `Map` and `BTreeSet`
`SortedSet` wherever they are named; the brackets of every `HashMap<..>`
and `Vec<..>`; `HashMap::new` written `.` twice; `or_default()` written
`or_insert(SortedSet.new())`; `&mut self` to `mut ref self` and `&self`
to `self`; the `&` of the arguments `&food`, `&(..)` and `&cuisine`
dropped; and both `*`s of `*old` dropped, the pattern's `old` being the
rating in the map. `entry`, `get_mut` and `iter().next()` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: no table is kept at all, only the calls so far. A query takes
each food of the cuisine, reads its rating back as that of the latest
change that names it or else its first, and keeps the highest, the
least name among equals. It checks 300 random scripts of 1 to 8 foods
of 1 to 3 letters from `a` to `c` over cuisines `x`, `y` and `z`, rated
1 to 4, then 1 to 20 calls, three changes to every two queries; then 30
of up to 60 foods of 1 to 6 letters rated up to `10^8` and up to 300
calls; then 30 of up to 30 foods rated 1 or 2 and up to 300 calls. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 20 calls, the answers are the literal reading's |
| P2 | one answer to each query, each a food of the cuisine asked for |
| P3 | every rating `r` made `2 r + 5`, at the start and in the changes: the same answers |
| P4 | every food's name given a leading `q`: every answer given it too |
| P5 | every query made twice in a row: each answer twice |
| P6 | each arm agrees with at least three of the other five |

P3 holds because `2 r + 5` keeps the ratings' order and their ties; P4
because a common first letter keeps the names' order; P5 because a
query changes nothing the statement can see, though the ★ arm's query
does pop its heaps.

The differential builds each changed script as a tuple of four lists,
two of them `collect`ed in place: `(foods.clone(), cuisines.clone(),
ratings.iter().map(..).collect(), calls.iter().map(..).collect())`,
handed to a function taking `(Vec[String], Vec[String], Vec[i64],
Vec[(i64, String, i64)])`. `check` first refused it, giving both
`collect`s one type, `(?T, ?T)`, where each is its own; a single
`collect` in a tuple checked and then stopped at lowering
(B-2026-11-21-45, fixed). `check` also refused the doubled answers,
`flat_map(|a| [a.clone(), a.clone()])`, since Kāra's `flat_map` takes an
`Iterator` and a list is a collection; `karac fix` writes the
`.into_iter()` it names, in one edit.

The differential prints `360 cases: checksum 561252966, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same scripts and reads every rating back from the calls. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a second stale top returned | P1 32, P5 78, P6 76 |
| M5 | ★: ratings compared halved | P1 8, P3 8, P6 8 |
| M6 | ★: every change also entered under cuisine x | P1 64, P2 106, P6 106 |
| M8 | set: the lowest rating taken | P1 206, P6 260 |
| M9 | set: the new rating never stored | P1 33, P6 77 |
| M11 | set: the cuisine made fresh for every food | P1 108, P6 158 |
| M13 | naive: names compared by their first letter | P1 16, P4 77, P6 41 |
| M14 | naive: the first food of the cuisine kept | P1 148, P6 202 |
| M16 | naive: a tie kept by the earlier food | P1 64, P6 92 |
| M17 | buckets: the lowest bucket read | P1 199, P6 253 |
| M18 | buckets: the greatest name in the bucket | P1 107, P6 136 |
| M19 | buckets: the old entry never removed | P1 74, P6 124 |
| M22 | iter: the cuisines up to the one asked read | P1 135, P2 187, P6 187 |
| M24 | iter: every cuisine read | P1 194, P2 248, P6 248 |
| M25 | iter: the change never stored | P1 100, P6 153 |
| M30 | solution: the change entered unnegated | P1 135, P6 187 |
| M31 | solution: the starting ratings entered unnegated | P1 139, P6 191 |

P1 and P6 kill all seventeen, P2 three, and P3, P4 and P5 one each.
P3 maps every rating `r` to `2 r + 5`, which keeps every comparison of
ratings, so only the ★ arm's ratings compared halved (M5) fails it: 4
and 5 halve to one value, 13 and 15 do not. P4 puts a `q` in front of
every name, which keeps every comparison of names, so only the naive
arm's names compared by their first letter (M13) fails it, every name
then starting with the same one. P5 asks each query twice, which
changes nothing but the ★ arm's heaps, so only the ★ arm's second stale
top returned (M3) fails it: the first query pops one stale top and
answers the next unchecked, and the second checks that one.

Of the thirty-one, fourteen were not kept. Eleven fail the same checks
as a kept one: a stale rating returned and a stale top answered as found
in the ★ arm (M1, M4) and the old entry never removed in the set arm and
the template (M7, M27), all as the buckets arm's old entry never removed
(M19), since each lets a food answer at a rating it no longer has; the
change never recorded or made in the ★ and naive arms (M2, M12) as the
iter arm's change never stored (M25); the set arm's change entered
unnegated (M10) as the template's (M30); the naive arm's every cuisine
read (M15) as the iter arm's (M24); the iter arm's greatest name among
equals (M23) as the buckets arm's (M18); the template's stored rating
never updated (M28) as the set arm's new rating never stored (M9),
which shows that the template's `old = new_rating` writes the map's own
rating; and the template's lowest rating taken (M29) as the set arm's
(M8). The iter arm's change given one more (M26) fails apart from every
kept one, and was left out because that arm keeps three already. Two
end in a panic, not a wrong answer, under both backends: the buckets
arm's new rating never put (M20) and emptied bucket kept (M21) leave a
cuisine whose last bucket is missing or empty, and the query unwraps
nothing.

Five were replaced before this count. The ★ arm's lowest rating taken,
new rating never pushed and starting ratings negated twice each left a
cuisine's lazy heap with no true entry, and the query's
`peek().unwrap()` panicked; they became M3, M5 and M6. The naive arm's
greatest name among equals became M13, since no mutant killed P4, and
the iter arm's lowest rating taken became M22, since it failed as the
buckets arm's lowest bucket read (M17) and left the iter and naive arms
one distinct signature short between them.

## Verification

Every arm prints the same output as `ratings.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 to 8.7 s, the iter arm the
slowest, since each of its queries walks the whole map. The
differential takes 6.2 s there, 2.2 s under `karac __mir-llvm-asan` and
1.2 s under `karac run`.

## Benchmarks

The bench builds `10^4` foods once from its own generator, four-letter
names over 100 cuisines rated up to `10^8`, and `10^5` calls, two
changes to every query. It then makes 100 passes, each through a fresh
system, folding every answer's letters and the pass into the checksum.
The bench uses the ★ arm, lazy heaps keyed on `(-rating, food)`, in all
five languages. Every implementation prints `100 passes over 10^4 foods
and 10^5 calls: checksum 842171869`. Kāra, Rust, Go and Python use
their own hash maps and heaps: `Map` and `PriorityQueue`; `HashMap` and
a `BinaryHeap` of `Reverse`; `map` and a hand-written heap; `dict` and
`heapq`. C has neither, and uses an open-addressing hash map over FNV-1a
of the name with a hand-written heap. Every name is a heap-allocated
string compared byte by byte; Kāra and Rust copy a food's name into
each heap entry, and Go, C and Python share it.

BENCHTAB
