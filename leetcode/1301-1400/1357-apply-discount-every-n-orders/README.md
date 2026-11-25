# 1357. Apply Discount Every n Orders

There is a supermarket that is frequented by many customers. The
products sold at the supermarket are represented as two parallel integer
arrays `products` and `prices`, where the `i`-th product has an ID of
`products[i]` and a price of `prices[i]`.

When a customer is paying, their bill is represented as two parallel
integer arrays `product` and `amount`, where the `j`-th product they
purchased has an ID of `product[j]`, and `amount[j]` is how much of the
product they bought. Their subtotal is calculated as the sum of each
`amount[j] * (price of the j-th product)`.

The supermarket decided to have a sale. Every `n`-th customer paying for
their groceries will be given a percentage discount. The discount
amount is given by `discount`, where they will be given `discount`
percent off their subtotal. More formally, if their subtotal is `bill`,
then they would actually pay `bill * ((100 - discount) / 100)`.

Implement the `Cashier` class:

- `Cashier(int n, int discount, int[] products, int[] prices)`
  initializes the object with `n`, the `discount`, and the `products`
  and their `prices`.
- `double getBill(int[] product, int[] amount)` returns the final total
  of the bill with the discount applied (if any). Answers within `10^-5`
  of the actual value will be accepted.

```
Cashier(3, 50, [1,2,3,4,5,6,7], [100,200,300,400,300,200,100])
getBill([1,2], [1,2])                                      ->  500.0
getBill([3,7], [10,10])                                    ->  4000.0
getBill([1,2,3,4,5,6,7], [1,1,1,1,1,1,1])                  ->  800.0    (1600, the 3rd customer, 50% off)
getBill([4], [10])                                         ->  4000.0
getBill([7,3], [10,10])                                    ->  4000.0
getBill([7,5,3,1,6,4,2], [10,10,10,9,9,9,7])               ->  7350.0   (14700, the 6th customer)
getBill([2,3,5], [5,3,2])                                  ->  2500.0
```

**Constraints:** `1 <= n <= 10^4`, `0 <= discount <= 100`, `1 <=
products.length <= 200`, `prices.length == products.length`, `1 <=
products[i] <= 200`, `1 <= prices[i] <= 1000`, the elements in
`products` are unique, `1 <= product.length <= products.length`,
`amount.length == product.length`, `product[j]` exists in `products`,
`1 <= amount[j] <= 1000`, the elements of `product` are unique, at most
1000 calls will be made to `getBill`.

Each arm is a `struct Cashier` with `fn new(n: i32, discount: i32,
products: Vec[i32], prices: Vec[i32]) -> Cashier` and `fn get_bill(mut
ref self, product: Vec[i32], amount: Vec[i32]) -> f64`. Every harness
prints a bill in cents, rounded.

## Approaches

| file | mechanism |
|---|---|
| `cashier.kara` ★ | the prices in a `Map` from product to price, and a count of the customers so far; every n-th customer's bill is cut by the discount. O(k) for a bill of k products |
| `cashier_array.kara` | the prices in a list indexed by product, the products being 1 to 200, and the customers counted down from n, the discount given at 0 and the count started again. O(k) |
| `cashier_scan.kara` | the products and prices kept as given, each product found by a scan of the products; the bill summed in whole units, and cut on every n-th customer by the discount in hundredths. O(k p) for a bill of k products among p |
| `cashier_sorted.kara` | the (product, price) pairs sorted by product, each product found by a binary search, `partition_point`. O(k log p) |
| `cashier_solution.kara` | a Rust solution as LeetCode's Rust users write it (the pairs made by `products.into_iter().zip(prices).collect()` and sorted, each product found by `binary_search_by_key(p, \|&(id, _)\| id).unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's example, in cents
(`[50000, 400000, 80000, 400000, 400000, 735000, 250000]`); one
customer of a cashier that discounts everyone by 100% and one by 0%,
one of a cashier with n = 10^4, and the largest bill, 200 products of
price 1000 bought 1000 times each, at 99% off (`0 2100 2100
200000000`); and 300 random cashiers of 1 to 200 products at prices
from 1 to 1000, n from 1 to 10 and a discount from 0 to 100, each
serving 1 to 40 customers who buy 1 to 20 of the products 1 to 1000
times (`300 random cashiers: 1158985846230 cents billed, checksum
623633239`). `cashier.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the array and sorted arms check clean. The ★ arm's
harness passed `ids.clone()` twice and `products.clone()` to parameters
that only borrow; `karac check` warns of each copy (W0300,
`redundant_clone`), and `karac fix` drops all three. The harness was
first written to print the example's bills through Rust's turbofish,
`.collect::[Vec[i64]]()`, inside the f-string; `karac check` refuses it
(E0001) and says to annotate a binding instead, which needs a binding
the f-string does not have, so the binding was written by hand. The
scan arm was written `(bill * (100 - self.discount) as i64) as f64`;
the `as i64` is unnecessary, an `i32` operand widening to `i64` beside
the `i64` bill (W0310, `lossless_cast`), and `karac fix` drops it. The
Rust solution takes one round of 18 fixes by `karac fix`'s count:
among them each `Vec<..>` to `Vec[..]`, `&mut self` to `mut ref self`,
`sort_unstable()` to `sort()`, the `&` dropped from the pattern
`|&(id, _)|`, and two that came with rows filed from this kata.
`products.into_iter().zip(prices)` over two borrowed parameters becomes
`products.clone().into_iter().zip(prices.iter())`, the borrowed
collection at `zip` iterated by its view (B-2026-11-21-62, fixed);
and `self.items.binary_search_by_key(p, ..).unwrap()` becomes two
`partition_point`s, the last equal element as Rust's `Ok` gives it, and
a panic where there is none, as Rust's `unwrap` gives
(B-2026-11-21-61, fixed). Before those rows each of the two got only a
bare trait or method error and no fix. Every arm matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, in cents: each customer's products looked up among the
products in turn, the price times the amount summed, and every n-th
customer's bill x made `x - (discount * x) / 100`. 2000 sessions in four
kinds, 500 each, by discount: 0, 100, 50, and from 0 to 100. Each sells
1 to 8 of the products 1 to 200 at prices from 1 to 1000, with n from 1
to 5, and serves 1 to 10 customers, each buying 1 to 8 of them 1 to
1000 times. Every session is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the products and prices listed in the opposite order: the same bills |
| P3 | every price doubled: every bill doubled |
| P4 | no discount: every bill the sum of price times amount, and no bill with the discount above that sum |
| P5 | every customer discounted, n = 1: each bill the undiscounted one cut by the discount |
| P6 | the ★ arm's bills |

All 60,000 checks pass on every arm: `2000 sessions: checksum
888275176, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`. Python, in whole
cents, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the discount given to the customer after each n-th | P1 1497, P5 1497, P6 5988 |
| M2 | ★: the discount charged instead of taken off | P1 1207, P4 1592, P5 1777, P6 4828 |
| M3 | array: the count never started again | P1 728, P5 1362, P6 728 |
| M4 | array: every product at the first price | P1 1612, P2 1642, P4 1704, P6 1612 |
| M5 | scan: the amount left out | P1 1895, P4 2000, P6 1895 |
| M6 | scan: a discounted bill rounded down to a whole unit | P1 584, P3 477, P5 838, P6 584 |
| M7 | sorted: the prices paired in the opposite order | P1 1638, P4 1731, P6 1638 |
| M8 | sorted: each customer counted twice | P1 578, P6 578 |
| M9 | solution: the first n-th customer not discounted | P1 1183, P5 1497, P6 1183 |
| M10 | solution: only the last product billed | P1 1496, P4 1591, P6 1496 |

P1 and P6 kill all ten, P4 and P5 five each, and P2 and P3 one each.
Discounting every customer (P5) catches the edits that pick the wrong
customers or the wrong cut (M1, M2, M3, M6, M9); with n = 1 every
customer is the n-th, so counting each customer twice (M8) is still
right there. No discount (P4) checks each bill against the plain sum,
and catches the edits that get the sum wrong (M4, M5, M7, M10), and the
cut charged instead of taken off (M2), which leaves a bill of 0 percent
off at nothing. Listing the products backwards (P2) catches only the
first price used for every product (M4), since the first price changes
with the order; pairing the prices in the opposite order (M7) makes the
same wrong pairs either way. Doubling the prices (P3) doubles every
right bill and every bill an edit gets wrong by a factor, so it catches
only the bill rounded down to a whole unit (M6), whose lost fraction
doubles into a whole unit or does not.

## Benchmarks

The bench builds 20 cashiers, each selling the products 1 to 200 at
prices from 1 to 1000, with n from 1 to 10 and a discount from 0 to
100, once; then makes 10^6 bills, each of 1 to 20 products bought 1 to
1000 times, all drawn from the checksum so far, so no answer carries
over, billed by the ★ arm and folded into the checksum in cents. Every
implementation prints `1000000 bills over 20 cashiers: checksum
563753405`. C keeps the prices in a hash table written out (open
addressing, linear probing), Rust in a `HashMap`, Go in a `map` and
Python in a `dict`.

BENCHTAB
