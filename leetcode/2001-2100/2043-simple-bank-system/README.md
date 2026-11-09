# 2043. Simple Bank System

You have been tasked with writing a program for a popular bank that will
automate all its incoming transactions (transfer, deposit, and withdraw).
The bank has `n` accounts numbered from `1` to `n`. The initial balance of
each account is stored in a 0-indexed integer array `balance`, with the
`(i + 1)`-th account having an initial balance of `balance[i]`.

Execute all the valid transactions. A transaction is valid if the given
account number(s) are between `1` and `n`, and the amount of money
withdrawn or transferred from is less than or equal to the balance of the
account. Implement the `Bank` class: `Bank(long[] balance)` initializes the
object with the 0-indexed integer array `balance`; `boolean transfer(int
account1, int account2, long money)` transfers `money` dollars from the
account numbered `account1` to the account numbered `account2`;
`boolean deposit(int account, long money)` deposits `money` dollars into
the account numbered `account`; `boolean withdraw(int account, long money)`
withdraws `money` dollars from the account numbered `account`. Each returns
`true` if the transaction was successful, `false` otherwise.

```
Bank([10, 100, 20, 50, 30])
withdraw(3, 10)      ->  true     (account 3 has 20; 10 left)
transfer(5, 1, 20)   ->  true     (account 5 has 30; 10 left, account 1 30)
deposit(5, 20)       ->  true     (account 5 has 30)
transfer(3, 4, 15)   ->  false    (account 3 has only 10)
withdraw(10, 50)     ->  false    (there is no account 10)
```

**Constraints:** `n == balance.length`; `1 <= n, account, account1,
account2 <= 10^5`; `0 <= balance[i], money <= 10^12`; at most `10^4`
calls in total to `transfer`, `deposit` and `withdraw`.

A call is checked whole before anything changes: its accounts must exist,
and an account it takes money from must hold at least that much. Nothing
else about the bank's past matters, so each call is O(1).

## Approaches

| file | mechanism |
|---|---|
| `bank.kara` ★ | `struct Bank { balance: Vec[i64] }`, an `exists` helper, `mut ref self` methods that check and then write `balance[account - 1]`. O(1) a call |
| `bank_map.kara` | a `Map[i64, i64]` from account number to balance, an account existing when the map has its key; `match self.accounts.get(account) { Some(have) if have >= money => .. }` and the balance written back by index. O(1) expected a call |
| `bank_result.kara` | refusals as values: `account` and `take` return `Result[.., Refusal]` (`enum Refusal { NoSuchAccount(i64), TooLittle { have, want } }`), a transfer chains them with `?`, and the API's `bool` is `.is_ok()`. O(1) a call |
| `bank_ops.kara` | each call built as an `enum Op` with struct variants and handed to one `apply`, a `match` whose guards say which accounts must exist and how much must be there, with an `exists` closure over the account count. O(1) a call |
| `bank_option.kara` | `Option` chaining: `index` gives `Some(position)` or `None`, a withdrawal keeps it through `filter`, a transfer pairs both positions with `zip` first, a deposit is `map(..).is_some()`. O(1) a call |
| `bank_solution.kara` | LeetCode's Rust template (`Vec<i64>`, `fn new(..) -> Self`, `&self` and `&mut self`, `i32` accounts cast `as usize`, `&&`, `\|\|`, `!`), carried by `karac fix` in two rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: the answers for LeetCode's example and
two more call sequences; then how many calls succeed, with a checksum of
the answers in order, for 2000 banks of 1 to 8 accounts and 1 to 30 calls
(amounts up to 1 to 100), and for 4 banks of 100000 accounts and 10000
calls, the most the constraints allow (amounts up to 10^12, 10^6, 100 and
1). Now and then a call names account 0 or `n + 1`. `bank.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a log of the calls that went through, each kept as `(from, to,
money)` with 0 for the world outside the bank, and an account's balance
summed from its first value and the log whenever a call asks for it. It
checks 1500 banks of 1 to 6 accounts and 1 to 20 calls (amounts up to 1 to
30), each with a relabelling of the accounts and a place to cut the calls.
Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | the accounts relabelled, with their balances, leave the answers |
| P3 | every balance and amount doubled leaves the answers |
| P4 | a deposit of 0 into account 1 put first answers `true` and leaves the rest |
| P5 | the calls cut short answer the same up to the cut |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 banks: checksum 681014109, 54000 checks over
6 arms: 0 failures` under every lane in Verification; 6106 of the 16152
calls succeed, and the checksum is also computed by a few lines of Python.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. All thirty are killed, each
fails the same way under both backends, none by a crash, and no two kept
ones fail the same checks. An edit that lets a call through to an account
that does not exist would index outside the balances and crash, so none
does: the unchecked accounts here land on accounts that exist.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last account refused (`<` for `<=`) | P1 1016, P2 724, P4 258, P6 1016 |
| M2 | ★: a transfer of the whole balance refused | P1 169, P6 169 |
| M3 | ★: a transfer's money never arriving | P1 113, P6 113 |
| M4 | map: the accounts numbered from 0 | P1 1349, P2 859, P4 258, P6 1349 |
| M5 | map: a deposit taken out | P1 558, P6 558 |
| M6 | map: a transfer checked against the receiving account | P1 790, P6 790 |
| M7 | result: a transfer to no account kept by the sender | P1 536, P6 536 |
| M8 | result: a deposit to no account answered true | P1 1057, P6 1057 |
| M9 | result: half a transfer arriving (`money / 2`) | P1 67, P3 1, P6 67 |
| M10 | ops: a deposit of nothing refused | P1 263, P4 1500, P6 263 |
| M11 | ops: the accounts past the fourth refused | P1 318, P2 320, P6 318 |
| M12 | ops: every refusal answered true | P1 1453, P6 1453 |
| M13 | option: the receiver taken as the sender | P1 616, P6 616 |
| M14 | option: a deposit answered the other way (`is_none`) | P1 1372, P4 1500, P6 1372 |
| M15 | option: an unknown account taken as the first | P1 1322, P2 496, P6 1322 |
| M16 | solution: account 1 refused | P1 1023, P2 717, P4 1500, P6 1023 |
| M17 | solution: a deposit setting the balance | P1 347, P4 358, P6 347 |

P1 and P6 kill all seventeen, P4 six, P2 five, P3 one and P5 none. P2
sees the edits that depend on which number an account has: the last
account, account 1 or the accounts past the fourth refused (M1, M16, M11),
the accounts numbered from 0 (M4), and an unknown account taken as the
first (M15). P4 sees the edits that a deposit of nothing into account 1
exposes: account 1 refused, outright or when it is the last (M16, M1) or
missing from accounts numbered from 0 (M4); a deposit of nothing refused
or answered the other way (M10, M14); and a deposit that sets the balance,
which empties the account (M17). P3 doubles every amount, which keeps
every comparison between amounts, so it sees only M9, whose halving rounds
an odd transfer down and an even one exactly. P5 sees none: no arm's
answer to a call depends on the calls after it. It is there for an arm
that reads ahead or keeps state across banks.

The other thirteen fail as a kept one does, or with a signature of their
own that adds nothing. A transfer of the whole balance refused fails alike
in the ★, map and Rust arms (P1 169, kept as the ★ arm's M2), and a
transfer's money never arriving alike in the ★ and Rust arms (kept as M3).
A withdrawal never checked fails alike in the result, option and Rust arms,
with a count of its own. The ★ arm's deposit counted twice and withdrawal
never taken out, the map arm's transfer's money put back, the result
arm's whole balance never taken, the ops arm's withdrawal of nothing
answered false and transfer checked against the receiver's balance, and
the option arm's every withdrawal answered true fail with counts of their
own.

## Verification

Every arm prints the same output as `bank.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.9 s (result) to 2.7 s (map) and the
differential 2.4 s, on kara 991c45adcd.

The five Kāra arms met no compiler gap. `karac fix` made `Bank.new`'s
parameter `own Vec[i64]`, since a bare parameter borrows and the struct
keeps the balances, and turned the option arm's `map(|i| self.balance[i]
+= money)` into a block body, since an assignment is a statement and not a
closure's value. Its style pass also dropped the `ref` on the harness's
parameters, which borrow already.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds (fifteen edits, then seven) to a clean check: `Vec<i64>`
to `Vec[i64]`, `&self` to `self` and `&mut self` to `mut ref self`, `&&`,
`||` and `!` to `and`, `or` and `not`; then `balance` taken `own`, and
each `as usize` to `as i64`, since sizes and indices are `i64` in Kāra.
`fn new(..) -> Self` carries as it is.

## Benchmarks

The bench builds a bank of 100000 accounts and a list of 1000000 calls once
in all five languages, and for 40 rounds opens the bank afresh and makes
every call: 40000000 calls. Every implementation prints `40000000 calls:
30521200 succeed, checksum 992861305`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.514 to 0.568 s | 0.527 s |
| C (`clang -O3`) | 0.538 to 0.593 s | 0.570 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.546 to 0.620 s | 0.571 s |
| Kāra (`karac build`) | 0.555 to 0.674 s | 0.579 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.564 to 0.668 s | 0.591 s |
| Go | 0.625 to 0.762 s | 0.671 s |
| Python | 23.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.558 s) is not above its real time (0.579 s).

The sequential Kāra program is 0.97x Rust under overflow checks and 1.00x
C.
