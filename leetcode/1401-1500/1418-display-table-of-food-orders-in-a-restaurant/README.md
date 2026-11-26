# 1418. Display Table of Food Orders in a Restaurant

Given the array `orders`, which represents the orders that customers
have done in a restaurant. More specifically `orders[i] =
[customerName_i, tableNumber_i, foodItem_i]` where `customerName_i` is
the name of the customer, `tableNumber_i` is the table customer sit at,
and `foodItem_i` is the item customer orders. Return the restaurant's
"display table". The "display table" is a table whose row entries denote
how many of each food item each table ordered. The first column is the
table number and the remaining columns correspond to each food item in
alphabetical order. The first row should be a header whose first column
is "Table", followed by the names of the food items. Note that the
customer names are not part of the table. Additionally, the rows should
be sorted in numerically increasing order.

```
orders = [["David","3","Ceviche"],["Corina","10","Beef Burrito"],["David","3","Fried Chicken"],
          ["Carla","5","Water"],["Carla","5","Ceviche"],["Rous","3","Ceviche"]]
  ->  [["Table","Beef Burrito","Ceviche","Fried Chicken","Water"],
       ["3","0","2","1","0"],["5","0","1","0","1"],["10","1","0","0","0"]]
orders = [["James","12","Fried Chicken"],["Ratesh","12","Fried Chicken"],["Amadeus","12","Fried Chicken"],
          ["Adam","1","Canadian Waffles"],["Brianna","1","Canadian Waffles"]]
  ->  [["Table","Canadian Waffles","Fried Chicken"],["1","2","0"],["12","0","3"]]
orders = [["Laura","2","Bean Burrito"],["Jhon","2","Beef Burrito"],["Melissa","2","Soda"]]
  ->  [["Table","Bean Burrito","Beef Burrito","Soda"],["2","1","1","1"]]
```

**Constraints:** `1 <= orders.length <= 5 * 10^4`, `orders[i].length ==
3`, `1 <= customerName_i.length, foodItem_i.length <= 20`,
`customerName_i` and `foodItem_i` consist of lowercase and uppercase
English letters and the space character, `tableNumber_i` is a valid
integer between 1 and 500.

Each arm is `fn display_table(orders: Vec[Vec[String]]) ->
Vec[Vec[String]]`. Alphabetical order is the order of the bytes, as
LeetCode's judge has it: a capital before every small letter, and a
space before both.

## Approaches

| file | mechanism |
|---|---|
| `display_table.kara` ★ | a `SortedMap[i64, SortedMap[String, i64]]` of each table's count of each dish, filled through `entry().or_insert`, and a `SortedSet[String]` of the dishes for the header. O(n log n) |
| `display_table_grid.kara` | the dishes sorted with `sort` and `dedup`, each one's column found through a `Map[String, i64]` built by `collect`, and a grid of counts with a row for every table number from 1 to 500, the rows anyone ordered at kept. O(n log n) |
| `display_table_sorted.kara` | the orders as `(table, dish)` pairs sorted, so each table's orders come together, and each run counted into a row by the dish's place in the sorted dishes, found by `binary_search`. O(n log n) |
| `display_table_hash.kara` | the counts in a `Map[(i64, String), i64]` keyed by table and dish, and the tables and dishes, gathered in `Set`s, sorted afterwards, since a hash map's order is none. O(n log n) |
| `display_table_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `BTreeSet<String>`, a `BTreeMap<i32, HashMap<String, i32>>` filled through `entry().or_default()`, `parse().unwrap()`, `get(food).unwrap_or(&0).to_string()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's three examples and one
more, with a table 500 and a table 1 and dishes apart only by a capital
or a space, each table's rows joined by `|` and each row's cells by `,`
(`Table,Beef Burrito,Ceviche,Fried
Chicken,Water|3,0,2,1,0|5,0,1,0,1|10,1,0,0,0`, `Table,Canadian
Waffles,Fried Chicken|1,2,0|12,0,3`, `Table,Bean Burrito,Beef
Burrito,Soda|2,1,1,1`, `Table,Ab,a b,ab|1,0,1,2|500,1,0,1`); the
constraints' most, 5 * 10^4 orders at 500 tables of 20 drawn dishes (`5
* 10^4 orders: 501 rows of 21 cells, checksum 373420811`); and 2000
random cases of 1 to 40 orders, at up to 5 or 500 tables, of 1 to 8
dishes (`2000 random cases: 26869 rows, checksum 700126093`).
`display_table.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`. The hash arm walks its `Map`
and `Set`s only to collect them, and sorts before anything is printed,
so its output does not depend on their per-process order.

The Mend loop: the ★, grid, sorted and hash arms check clean as first
written. The Rust solution takes one round of 32 fixes by `karac fix`'s
count: the `use std::collections` line deleted, `struct Solution;` to
`struct Solution {}`, `Vec<..>` to `Vec[..]`, `BTreeSet` and `BTreeMap`
to `SortedSet` and `SortedMap` and `HashMap` to `Map`, `::new` and
`Vec::with_capacity` to `.new` and `Vec.with_capacity`, `for order in
&orders` to `for order in ref orders`, `order[1].parse().unwrap()` to
`i32.parse(order[1]).unwrap()`, `or_default()` to
`or_insert(Map.new())`, `vec![..]` to `[..]`, `unwrap_or(&0)` to
`unwrap_or(0)`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the dishes anyone ordered, each one once, put in alphabetical
order by taking the least not yet taken each time; then every table
number from 1 to 500 that some order names, in turn, and for each dish
the orders at that table of that dish, counted by a scan of every order,
while the orders are at most 300. LeetCode's examples, three edge cases
(one order, at table 500; every order at one table; dishes apart only by
a capital, a space or a letter more, with tables 1, 2, 9, 10 and 500, so
that 10 must not sort before 9), 500 orders each at its own table, the
constraints' most twice (5 * 10^4 orders at 500 tables of 20 dishes, and
at 3 tables of one dish), and 1994 random cases, 1 to 40 orders two
times in three and up to 300 otherwise, at up to 5 or 500 tables, of 1
to 8 dishes of up to 1, 3 or 20 characters drawn from `abcAB` and a
space.

The literal reading first tested its `Option` with Python's `if want is
Some(w)`, which `karac check` names as Python's identity test; written
`if let Some(w) = want`, it moves `want` inside the loop over the arms,
and `karac fix` writes `Some(ref w)`, 1 fix.

| | property |
|---|---|
| P1 | the statement read literally, while the orders are at most 300 |
| P2 | a header of "Table" and the dishes, each once and in order, and a row for each table, in numerical order, each as wide as the header |
| P3 | the counts add up to the orders, and each table's to the orders that name it |
| P4 | the orders taken in another order, reversed and then shuffled, give the same table |
| P5 | every order twice over doubles every count and changes nothing else |
| P6 | the ★ arm's answer |

All 60,075 checks pass on every arm: `2003 cases: checksum 269978591,
60075 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by a `Counter`
of `(table, dish)` pairs, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each dish's count started at 1 | P1 2000, P3 2003, P5 2003, P6 8012 |
| M2 | ★: a dish the table never ordered written as 1 | P1 1406, P3 1408, P5 1408, P6 5632 |
| M3 | grid: no table marked as having ordered, so only the header is left | P1 2000, P2 2003, P3 2003, P6 2003 |
| M4 | grid: table 500 left out | P1 114, P2 116, P3 116, P6 116 |
| M5 | sorted: the pairs left unsorted | P1 1928, P2 1930, P3 1440, P4 1930, P5 1955, P6 1930 |
| M6 | sorted: every order counted under the first dish | P1 1638, P6 1640 |
| M7 | hash: the dishes in falling order | P1 1638, P2 1640, P6 1640 |
| M8 | hash: each order counted under its customer's name, not its dish | P1 2000, P3 2003, P6 2003 |
| M9 | solution: the header row left out | P1 2000, P2 2003, P3 2003, P5 2003, P6 2003 |
| M10 | solution: the customers' names taken as the dishes | P1 2000, P2 1746, P3 2003, P6 2003 |

## Benchmarks

The bench draws 30 dishes of 1 to 20 letters and a pool of 2 * 10^5
orders at tables 1 to 500, and runs the ★ arm, taking its window as a
`Slice[Vec[String]]`, on 100 windows of 5 * 10^4 orders, each window's
start drawn. Rust's bench uses `BTreeMap` and `BTreeSet` as the ★ arm
does; C has no ordered map, so its bench keeps the dishes in an
open-addressing hash table, sorted afterwards, and each table's counts
in a row indexed by table number, and Go's and Python's keep the counts
in a hash map and sort the tables and dishes afterwards. Every
implementation prints `100 windows of 5 * 10^4 orders: checksum
237320783`.

BENCHTAB

Measured by hand, Kāra takes 1.5 to 1.7 s against Rust's 1.36 s (1.44 to
1.52 s with overflow checks on), both over B-trees; C takes 0.34 s, Go
0.66 to 0.77 s and Python 1.63 s, all three over hash tables.
