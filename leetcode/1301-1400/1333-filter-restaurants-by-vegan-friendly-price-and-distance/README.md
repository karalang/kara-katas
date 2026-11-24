# 1333. Filter Restaurants by Vegan-Friendly, Price and Distance

Given the array `restaurants` where `restaurants[i] = [id_i, rating_i,
veganFriendly_i, price_i, distance_i]`, you have to filter the
restaurants using three filters. The `veganFriendly` filter will be
either true (meaning you should only include restaurants with
`veganFriendly_i` set to true) or false (meaning you can include any
restaurant). In addition, you have the filters `maxPrice` and
`maxDistance`, which are the maximum value for price and distance of
restaurants you should consider respectively. Return the array of
restaurant ids after filtering, ordered by rating from highest to lowest.
For restaurants with the same rating, order them by id from highest to
lowest.

```
restaurants = [[1,4,1,40,10],[2,8,0,50,5],[3,8,1,30,4],[4,10,0,10,3],[5,1,1,15,1]]
veganFriendly = 1, maxPrice = 50, maxDistance = 10  ->  [3,1,5]
veganFriendly = 0, maxPrice = 50, maxDistance = 10  ->  [4,3,2,1,5]
veganFriendly = 0, maxPrice = 30, maxDistance = 3   ->  [4,5]
```

**Constraints:** `1 <= restaurants.length <= 10^4`, `1 <= id_i,
rating_i, price_i, distance_i <= 10^5`, `1 <= maxPrice, maxDistance <=
10^5`, `veganFriendly_i` and `veganFriendly` are 0 or 1, and all `id_i`
are distinct.

The arms are `fn filter_restaurants(restaurants: Vec[Vec[i32]],
vegan_friendly: i32, max_price: i32, max_distance: i32) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `filter_restaurants.kara` ★ | the restaurants that pass the three filters kept as (rating, id) pairs and sorted with `sort_by`, rating and then id, both highest first, chained with `Ordering.then`. O(n log n) |
| `filter_restaurants_reverse.kara` | the passing restaurants found by an iterator `filter`, with the vegan filter written `vegan_friendly <= r[2]`, kept as (rating, id) tuples, sorted in the tuples' own order, lowest first, and read backwards. O(n log n) |
| `filter_restaurants_heap.kara` | every passing restaurant pushed into a `PriorityQueue.max_first()` of (rating, id), and popped until it is empty. O(n log n) |
| `filter_restaurants_tree.kara` | the passing ids gathered by rating in a `SortedMap`, whose keys are walked from the highest down, each rating's ids sorted highest first. O(n log n) |
| `filter_restaurants_solution.kara` | a Rust solution as LeetCode's Rust users write it (the passing rows collected as `Vec<&Vec<i32>>` by a `filter` with `\|\|` and `&&`, sorted with `sort_by(\|a, b\| b[1].cmp(&a[1]).then(b[0].cmp(&a[0])))`, and each row's id mapped out), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; nothing
passing, and one restaurant exactly on both limits (`[] [7]`); 10^4
restaurants, the constraints' most, every one passing and then the vegan
ones under two limits (`10^4 restaurants: 10000 first 99873, 4952 vegan
first 99873, checksum 999767419`); and 600 random lists of 1 to 2000
restaurants, most of them short, with ratings from 1 to 3 or to 10^5 and
prices, distances and limits from 1 to 10 or to 10^5 (`600 random lists:
9976 kept, checksum 471070661`). `filter_restaurants.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean. The heap arm was first
written with `PriorityQueue.new()`, Rust's `BinaryHeap::new()` habit, and
gave every list lowest first: a Kāra `PriorityQueue` pops its smallest
first unless built with `max_first()`, as `docs/library/collections.md`
says, so the oracle caught a mistake in the arm, not in the compiler. The
Rust arm takes one round of 21 fixes by `karac fix`'s count, from 13
errors: `struct Solution;` to `struct Solution {}`, each `Vec<..>` to
`Vec[..]`, `Vec<&Vec<i32>>` to `Vec[ref Vec[i32]]`, `||` to `or` and
`&&` to `and`, `cmp(&a[1])` to `cmp(a[1])`, and `Solution::` to
`Solution.`. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a restaurant passes when the vegan filter is off or it is
vegan-friendly, and its price and distance are at most the limits; the
passing restaurant with k others ahead of it, by a higher rating or the
same rating and a higher id, is the k-th answer. 2000 lists of 1 to 8
restaurants with distinct ids up to 30, in four kinds, 500 each: ratings
from 1 to 3 and prices and distances from 1 to 5; ratings, prices and
distances up to 10^5; every rating the same; and limits taken from the
list's own prices and distances, so some restaurants sit on them
exactly. Every list, filter and amount is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the list read backwards: the same answer |
| P3 | the vegan filter on: the answer with it off, the restaurants that are not vegan-friendly left out |
| P4 | every rating raised by one amount up to 1000: the same answer |
| P5 | every id turned over, 100001 less it: the answer's ids turned over, each run of one rating read backwards |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 lists: checksum 618597809,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, sorting by rating and id, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: ties left in the order they came | P1 239, P2 380, P5 380, P6 956 |
| M2 | ★: a price on the limit refused | P1 637, P6 2548 |
| M3 | reverse: the vegan filter turned around | P1 1018, P3 1427, P6 1018 |
| M4 | reverse: the sorted tuples read forwards | P1 610, P6 610 |
| M5 | heap: the distance never checked | P1 838, P6 838 |
| M6 | heap: the vegan-friendly ones turned away | P1 728, P3 1427, P6 728 |
| M7 | tree: the ratings walked from the lowest | P1 390, P6 390 |
| M8 | tree: each rating's ids lowest first | P1 380, P6 380 |
| M9 | solution: the distance held to the price limit | P1 770, P6 770 |
| M10 | solution: ties broken by the vegan flag | P1 239, P2 317, P5 380, P6 239 |

P1 and P6 kill all ten, P2, P3 and P5 two each, and P4 none. P2 to P5
each compare an arm with itself, so an edit that is wrong the same way
on both sides passes them. Reading the list backwards (P2) and turning
the ids over (P5) catch only the two edits that let the input's order
decide a tie (M1, M10); ids sorted the wrong way within a rating (M8) are
wrong consistently, and P5's turned answer reads the same. Only the two
edits to the vegan filter fail P3, which is about that filter alone (M3,
M6). Raising every rating (P4) catches none: no edit here depends on how
large a rating is, only on how ratings compare.

## Benchmarks

The bench builds 20 lists of 10^4 restaurants, the constraints' most,
with ratings, prices and distances up to 10^5, once; then makes 100
passes, each setting one rating of every list from the checksum so far
and drawing the filters from it too, so no answer carries over, answering
every list with the ★ arm and folding the answer's length, two of its
ids and the pass into the checksum. Every language reads the lists in
place. C sorts with `qsort` and Go with `slices.SortFunc`, the kata
convention, and both trail: on a shared Linux container with two
compiler gates running, C took 2.1 s, Go 2.8 s, Rust 0.70 s and Kāra
0.57 s. `qsort` and `slices.SortFunc` call their comparator through a
pointer or a closure for every comparison, where Rust's and Kāra's sorts
inline it. Every implementation prints `100 passes over 20 lists of
10^4: checksum 101851909`.

BENCHTAB
