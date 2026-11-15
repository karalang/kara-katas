# 1169. Invalid Transactions

A transaction is possibly invalid if:

- the amount exceeds `$1000`, or;
- if it occurs within (and including) `60` minutes of another transaction
  with the same name in a different city.

You are given an array of strings `transaction` where `transactions[i]`
consists of comma-separated values representing the name, time (in
minutes), amount, and city of the transaction.

Return a list of `transactions` that are possibly invalid. You may return
the answer in any order.

```
["alice,20,800,mtv","alice,50,100,beijing"]  ->  ["alice,20,800,mtv","alice,50,100,beijing"]
["alice,20,800,mtv","alice,50,1200,mtv"]     ->  ["alice,50,1200,mtv"]
["alice,20,800,mtv","bob,50,1200,mtv"]       ->  ["bob,50,1200,mtv"]
```

**Constraints:** `transactions.length <= 1000`; each `transactions[i]` takes
the form `"{name},{time},{amount},{city}"`; each `{name}` and `{city}`
consists of lowercase English letters and has a length between 1 and 10;
each `{time}` consists of digits and represents an integer between 0 and
1000; each `{amount}` consists of digits and represents an integer between
0 and 2000.

The arms are `fn invalid_transactions(transactions: Vec[String]) ->
Vec[String]`. The answer may come in any order, so the harness sorts it
before printing.

## Approaches

A transaction is invalid on its own when its amount is over 1000; otherwise
it needs another of its name, in another city, at most 60 minutes away.
The arms differ in how they find that other one.

| file | mechanism |
|---|---|
| `invalid_transactions.kara` ★ | by name: each transaction parsed into a `struct Txn`, the places of each name's transactions gathered in a `Map[String, Vec[i64]]`, and every transaction compared with the others of its name only. O(n + the sum of each name's count squared) |
| `invalid_transactions_pairs.kara` | every pair: each transaction split into a `(Str, i64, i64, Str)` of views into it, and compared with every other one, whatever its name. O(n^2) |
| `invalid_transactions_window.kara` | a sliding window: the transactions sorted by name and time, and for each one the window of its name's transactions within 60 minutes either side, its two ends only moving forward, with a `Map` counting the window's transactions in each city; a transaction is invalid when the window holds more than its own city's count. O(n log n) |
| `invalid_transactions_minutes.kara` | counts by the minute: for each name, and for each name and city, the transactions in each of the 1001 minutes summed into running totals, so a window's count is two totals' difference; a transaction is invalid when its name's count in the window is more than its city's. O(n + 1001 for each name and city) |
| `invalid_transactions_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, each transaction parsed into a `(String, i32, i32, String)` with `parse::<i32>()`, a `let (ref name, time, amount, ref city) = parsed[i]` destructure, every pair compared), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's examples; 60 minutes apart
counting and 61 not (`ann,0` and `ann,60` invalid, `ann,121` not); an
amount of 1000 allowed and 1001 not; the same transaction twice, both
invalid; a transaction alone. Then 300 random lists of 1 to 40
transactions by three names in three cities, half within 200 minutes so
that times crowd (`300 random lists: 4532 invalid, checksum 352250502`),
and two lists of 1000 transactions, the constraints' most: by 100 names in
two cities (498 invalid), and 999 by one name in one city with one in
another in the middle (122 invalid, the one and the 121 within 60 minutes
of it). `invalid_transactions.py` mirrors the ★ arm and its output is
byte-identical; with `lit` it reads the statement literally, comparing
every transaction with every other, and gives the same output.

The Mend loop: the harness takes five fixes in every arm: `b as i64` on a
byte dropped, since a `u8` widens to `i64` by itself; three `let name =
names[..]` (and `city`) to `ref names[..]`, since the list's elements are
`String`s and the binding only reads; and `.to_string()` dropped from a
literal pushed onto a `Vec[String]`. Beside them, the ★ arm takes
`f[1].parse().unwrap()` to `i64.parse(f[1]).unwrap()`, twice, since
`.parse()` takes its target from an expected `Option[T]` and the struct
field's type reaches it only through `unwrap`; the pairs arm `let mut out
= []` to `Vec.new()`; the window arm `let (mut lo, mut hi)` to `let mut
(lo, hi)` and `.copied()` to `.cloned()`; the minutes arm none. The Rust
arm takes four rounds (22, 1, 6 and 1 edits): the generics to brackets,
`&str` to `Str`, `parse::<i32>()` to `i32.parse(..)`, `::` to `.` and
`&&` to `and`; then `struct Solution {}`; then the `','` given to `split`
to `","` and the destructure's `= parsed[i]` to `= ref parsed[i]`, which
its `ref` bindings need; with the harness's fixes in the last two. Its
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each transaction compared with every other, invalid when its
amount exceeds 1000 or another of its name in a different city is at most
60 minutes from it. It checks 600 lists in four kinds of 150: 1 to 8
transactions by two names in two cities within 130 minutes; 1 to 30 by
three names in three cities within 300; 30 to 100 by five names in four
cities within the whole 1000; and 1 to 20 at whole half hours within 240
minutes, so that two are often exactly 60 apart, of 995 to 1005. Every
random choice the properties make is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the transactions in another order give the same answer |
| P3 | every name and city renamed alike renames the answer alike |
| P4 | every time moved by the same minutes, kept within 0 to 1000, moves the answer alike |
| P5 | a transaction over 1000 by a new name is added to the answer and changes nothing else |
| P6 | one more transaction leaves every invalid one invalid, and every answer is one of the transactions given |

All 18,000 checks pass on every arm: `600 lists: checksum 615253556, 18000
checks over 5 arms: 0 failures`, in 30 s under `karac __mir-run`, about
half of it in the minutes arm, which fills 1001 minutes for each name
and each name and city on every call. A Python reading of the same
draws, with the mirror against the literal reading, gives the same
checksum.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. All fifteen are caught.

| # | mutation | failures by property |
|---|---|---|
| B1 | ★: an amount of 1000 taken as too much | P1 34 |
| B2 | ★: exactly 60 minutes apart not counted | P1 111 |
| B3 | ★: names compared where cities should be | P1 483 |
| P1 | pairs: names ignored | P1 431, P5 5 |
| P2 | pairs: every earlier transaction counted as near | P1 325 |
| P3 | pairs: amounts ignored | P1 328, P5 600 |
| W1 | window: a transaction 60 minutes later left out | P1 77 |
| W2 | window: a transaction 60 minutes earlier left out | P1 63 |
| W3 | window: each name's transactions left unsorted by time | P1 384, P2 358 |
| M1 | minutes: the window's last minute left out | P1 78, P4 2 |
| M2 | minutes: one other city's transaction let pass | P1 464 |
| M3 | minutes: the window's first minute left out | P1 63 |
| X1 | solution: an amount of 1001 let pass | P1 27, P5 600 |
| X2 | solution: the same city taken for a different one | P1 499 |
| X3 | solution: a transaction pushed once for every match | P1 397, P6 397 |

P1 catches all fifteen, and each other property three at most: the
edits are wrong answers that every reordering, renaming and shift
reproduces alike. P5 sees the edits that let a transaction over 1000
through (P3, X1), and the one that ignores names (P1), where the new
name's transaction makes another of its time invalid. P2 sees only W3,
whose answer depends on the order the transactions come in; P6 only X3,
whose answer holds a transaction more often than it was given; and P4
only M1, in 2 checks. P3 sees none, since no edit treats one name or
city differently from another.

## Benchmarks

`bench/` times the ★ arm against the same grouping in C (an
open-addressing hash table, FNV-1a), Rust (`HashMap`), Go (`map`) and
Python (`dict`). 16 lists of 1000 transactions, the constraints' most, by
200 names in two cities, are built once; each of 300 rounds gives one
transaction of every list a new name, time, amount and city and finds
the invalid ones. Every program prints `300 rounds over 16 lists of 1000
transactions: 1523014 invalid, checksum 381314853`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `1bdebaaa70`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.286 to 1.367 s | 1.314 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.256 to 1.440 s | 1.319 s |
| Rust (`rustc -O`) | 1.048 to 1.147 s | 1.111 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.115 to 1.201 s | 1.158 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.142 to 1.202 s | 1.171 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.431 to 0.585 s | 0.440 s |
| C (`clang -O3`) | 0.424 to 0.502 s | 0.467 s |
| Go | 1.018 to 1.269 s | 1.131 s |
| Python | 4.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, so the
two Kāra rows are one program timed twice. Kāra takes about 1.14x
overflow-checked Rust's time, the equal-safety comparison. C takes about
a third of it: it copies each name and city into fixed arrays inside its
`Txn`, hashes with FNV-1a, and returns pointers into the input, where
Kāra and Rust allocate a `String` for each name and city and a copy of
each invalid transaction, and hash with SipHash. Go's fields are slices
of the input and its answer shares the input's strings, and it takes
about 0.86x Kāra's time. These causes are read from the programs, not
profiled. Python takes about 3.4x.
