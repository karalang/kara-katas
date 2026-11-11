# 2115. Find All Possible Recipes from Given Supplies

You have information about `n` different recipes. You are given a
string array `recipes` and a 2D string array `ingredients`. The `i`th
recipe has the name `recipes[i]`, and you can create it if you have all
the needed ingredients from `ingredients[i]`. A recipe can also be an
ingredient for other recipes, i.e., `ingredients[i]` may contain a
string that is in `recipes`.

You are also given a string array `supplies` containing all the
ingredients that you initially have, and you have an infinite supply of
all of them.

Return a list of all the recipes that you can create. You may return
the answer in any order.

Note that two recipes may contain each other in their ingredients.

```
recipes = ["bread"], ingredients = [["yeast","flour"]],
supplies = ["yeast","flour","corn"]                          ->  ["bread"]
recipes = ["bread","sandwich"], ingredients = [["yeast","flour"],["bread","meat"]],
supplies = ["yeast","flour","meat"]                          ->  ["bread","sandwich"]
recipes = ["bread","sandwich","burger"],
ingredients = [["yeast","flour"],["bread","meat"],["sandwich","meat","bread"]],
supplies = ["yeast","flour","meat"]                          ->  ["bread","sandwich","burger"]
```

**Constraints:** `n == recipes.length == ingredients.length`; `1 <= n
<= 100`; `1 <= ingredients[i].length, supplies.length <= 100`; `1 <=
recipes[i].length, ingredients[i][j].length, supplies[k].length <= 10`;
lowercase English letters only; all the values of `recipes` and
`supplies` combined are unique; each `ingredients[i]` has no duplicate
values.

The recipes and their ingredients form a graph, and a recipe can be made
exactly when every ingredient is a supply or a recipe that can itself be
made. Kahn's topological order finds those: start from the supplies,
and each item had lowers the count of what every recipe needing it still
lacks; a recipe whose count reaches zero is made and becomes an item
too. Recipes on a cycle, or below an item nobody has, are never reached.
The answer may come in any order, so every harness sorts it before
printing.

## Approaches

| file | mechanism |
|---|---|
| `recipes.kara` ★ | Kahn's order over names: a `Map[String, Vec[i64]]` from each ingredient to the recipes needing it, built with `entry(..).or_insert(Vec.new())`, a count of what each recipe lacks, and a `VecDeque` starting with the supplies. O(n + total ingredients) |
| `recipes_fixpoint.kara` | a `Set` of what is on hand, and passes over the recipes adding every one whose ingredients are `all` on hand, until a pass adds nothing. O(n^2 k) |
| `recipes_dfs.kara` | a depth-first search with an `enum State { Unseen, Visiting, Made, Failed }` per recipe; meeting a recipe still `Visiting` is a cycle, which fails |
| `recipes_struct.kara` | a `struct Kitchen` of a `Set` on hand and a `Map` from each recipe to the `Set` it still lacks; its `stock` method (`mut ref self`) puts an item on hand, walks the map with `iter_mut` and returns the recipes it completes, stocked in turn from a `Vec` used as a stack |
| `recipes_levels.kara` | Kahn's order over indices: every name numbered through a `Map`, the edges a `Vec[Vec[i64]]`, and a frontier of item numbers worked off level by level with `flat_map` and a `filter` that lowers each count |
| `recipes_solution.kara` | LeetCode's Rust template: Kahn's order over `&str` keys, `HashMap`s of in-degrees and edges, `entry(..).or_default()`, a `VecDeque` of supplies and `get_mut` on each in-degree, carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (two recipes needing each other, a recipe needing one that cannot
be made, a chain given last recipe first), each with the recipes made,
sorted; then the number made over 2000 random kitchens of 1 to 8
recipes and 1 to 6 of 8 possible supplies, each recipe needing 1 to 4
items among the supplies and the other recipes, and a checksum of the
recipes made; then the constraints' largest, a chain of 100 recipes
each needing the one before and 99 supplies, given last first, with
every supply and with `s0` missing. `recipes.py` mirrors the ★ arm and
its output is byte-identical.

The ★ arm was first written with Rust's `entry(..).or_default()`;
`karac fix` turned it into `or_insert(Vec.new())`, since Kāra's `Entry`
takes the value it puts in.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a recipe can be made within `d` steps when each of its
ingredients is a supply or a recipe that can be made within `d - 1`,
and can be made at all when it can within `n` steps, the number of
recipes, computed a round at a time over every recipe and every
ingredient. It checks 300 random kitchens of 1 to 6 recipes and 1 to 4
of 6 possible supplies, each recipe needing 1 to 3 items; then 30 of up
to 30 recipes and up to 10 of 12 supplies, needing 1 to 4; then 30
chains of up to 30 recipes listed in a shuffled order, each needing the
one before and a supply, one in three closed into a cycle. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the recipes made are the statement read literally |
| P2 | each is a recipe, none twice, and each one's ingredients are all supplies or recipes made |
| P3 | every name given an `x` in front: the same recipes with theirs |
| P4 | the recipes listed in reverse: the same recipes |
| P5 | a recipe needing only a supply appended, and one needing it and an item nobody has: the recipes made and the first of the two |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 kitchens: checksum 120798031, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
kitchens by passes over a set. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-two edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a recipe made when one ingredient is had | P1 259, P2 259, P5 360, P6 259 |
| M2 | ★: a made recipe not queued | P1 62, P6 62 |
| M5 | ★: the queue stopped after 20 items | P1 11, P5 13, P6 11 |
| M7 | fixpoint: any ingredient enough | P1 226, P2 207, P5 360, P6 226 |
| M8 | fixpoint: made recipes not put on hand | P1 169, P2 169, P5 360, P6 169 |
| M10 | fixpoint: passes stop after the second | P1 20, P4 21, P6 20 |
| M11 | dfs: a cycle taken as made | P1 40, P2 12, P4 22, P6 40 |
| M13 | dfs: the first ingredient decides | P1 144, P2 128, P5 360, P6 144 |
| M14 | dfs: a missing item taken as had | P1 275, P2 275, P5 360, P6 275 |
| M19 | struct: the supplies but the last stocked | P1 93, P5 82, P6 93 |
| M20 | struct: a recipe needing more than two items never done | P1 8, P6 8 |
| M31 | struct: an item whose name starts with `x` never stocked | P3 169 |
| M23 | levels: the first supply dropped | P1 113, P5 360, P6 113 |
| M24 | levels: the edges to the first recipe dropped | P1 87, P4 117, P6 87 |
| M25 | levels: the levels stop after five | P1 16, P6 16 |
| M27 | solution: the in-degree one short | P1 264, P2 185, P5 360, P6 264 |
| M30 | solution: the last recipe never listed | P1 108, P4 117, P5 108, P6 108 |

P1 and P6 kill sixteen, P5 ten, P2 seven, P4 four and P3 one. P5 fails
on every array for the edits that make a recipe from less than all its
ingredients (M1, M7, M8, M13, M14, M27), since its second appended
recipe needs an item nobody has and is then made, and for the edits
that drop the first supply (M23), which the first appended recipe needs.
P2 sees a recipe made without its ingredients: the same edits but M23,
and the DFS arm's cycle taken as made (M11). P4 sees the edits whose
answer depends on where a recipe sits in the list: a bounded number of
passes (M10), a cycle met first from one side (M11), the first recipe's
edges (M24), the last recipe dropped (M30). P3 sees only the struct
arm's names starting with `x` (M31), an edit added for it, which
nothing else reads; it is the one kept edit P1 does not see, since no
name in the drawn kitchens starts with `x`. The caps (M5, M10, M20,
M25) show only on the long chains and the larger kitchens.

Of the thirty-two, fifteen were not kept. Two are equivalent: the DFS
arm's failure forgotten, which only searches again and fails again, and
the struct arm's item stocked twice, which completes nothing the second
time. Two loop until the timeout, a recipe made again at every level
past its last ingredient: the levels arm's and the Rust arm's done at a
count of one. Eight fail as a kept one does: the ★ arm's first supply
ignored and the Rust arm's as M23; the ★ arm's recipe needing one item
less as M27; the fixpoint arm's last recipe never tried as M30; the
struct arm's done at its first item as M1; and the struct, levels and
Rust arms' made recipes not passed on as M2. The fixpoint arm's one
pass only and the DFS arm's recipe ingredient never searched fail alike
(P1 45, P4 62, P6 45), and the struct arm's first three supplies only is
killed with checks of its own (P1 32, P6 32) but was left out because
its arm keeps its share.

## Verification

Every arm prints the same output as `recipes.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 s to 1.2 s, and the
differential 2.4 s; compiled it takes 0.9 s.

`karac fix` carries the template in three rounds of 27, 4 and 2 edits:
Rust's spellings (the `use std::collections` line deleted, `<..>` to
brackets, `&str` to `Str`, `::` to `.`, the `&` dropped from `for &r`,
`struct Solution;` to `struct Solution {}`); then `HashMap` to `Map`;
then the in-degree's `usize` to `i64` and `or_default()` to
`or_insert(Vec.new())`.

It then met a compiler gap, fixed in karac with a test named for this
kata (karac BORROWSHA, `tests/kata_2115_ref_key_not_stored.rs`):
`indeg.get_mut(r)` inside `for r in next` was refused with "cannot
write to `r` while `indeg` still holds a borrow of it". The borrow
checker takes a call with a `mut ref` argument to store every other
argument's borrows in it, so the reference to `r` passed as the key was
kept in the map, and the loop's next `r` was a write to a borrowed
place. A reference argument that the receiver's type has no slot for can
only leave there what its referent holds, here the `Str`'s own origin,
which is still tracked; a view a callee does store still keeps its
owner borrowed.

## Benchmarks

The bench builds 40 kitchens of 100 recipes once, each recipe needing 1
to 8 items among 60 possible supplies, of which 56 are had, and the
recipes before it; it then solves each kitchen 10 times, renaming one
ingredient of one recipe before each solve so no solve repeats the one
before, with the ★ arm in all five languages: Kahn's order over names
in a hash map. Every implementation prints `400 solves: 16230 recipes
made, checksum 632881912`.

BENCHTAB
