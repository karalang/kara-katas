# 2816. Double a Number Represented as a Linked List

You are given the `head` of a **non-empty** linked list representing a
non-negative integer without leading zeroes.

Return *the* `head` *of the linked list after **doubling** it.*

```
head = [1,8,9]  ->  [3,7,8]
head = [9,9,9]  ->  [1,9,9,8]
```

**Constraints:** the number of nodes in the list is in the range
`[1, 10^4]`; `0 <= Node.val <= 9`; the input is generated such that the
list represents a number that does not have leading zeros, except the
number `0` itself.

## Approaches

| file | mechanism |
|---|---|
| `double.kara` ★ | one walk, in place, looking one node ahead: a 0 node put in front when the first digit is 5 or more, since only then does the number grow; then each digit its double's last digit, plus the one the next digit carries when it is 5 or more |
| `double_prev.kara` | one walk looking one node back, behind a 0 node put before the head: each digit doubled in place and a carry added to the node behind, whose even last digit never carries further; the front node kept only if it took a carry |
| `double_reverse.kara` | by reversing: the list turned round in place, doubled from the last digit with a carry as on paper, turned back, and a node for a carry left over put in front |
| `double_stack.kara` | by a stack: the digits read into a `Vec`, doubled from its end with a carry into a second `Vec`, and a new list built from that one |
| `double_solution.kara` | a Rust solution as LeetCode's Rust users write it, LeetCode's `Option<Box<ListNode>>` with `i32` values and a nested recursive `fn carry` over `&mut Option<Box<ListNode>>` that doubles each node on the way back and returns the carry, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The four own arms use a `shared struct ListNode` with `mut` fields, so a
node can be changed through any handle to it. The solution keeps
LeetCode's plain struct, and its harness converts the `i64` digits to
`i32` at `build` and back at `values_of`.

Every arm prints the same 7 lines: LeetCode's two examples; zero; 10^4
nodes, LeetCode's most, all 9, and all 4, which carries nothing, as a
length and a digest; 3000 random numbers of 1 to 12 digits; and 50 of up
to 10^4, the last two with how many grew a digit and a checksum.
`double.py` mirrors the ★ arm and its output is byte-identical.

```
[3, 7, 8]
[1, 9, 9, 8]
[0]
10001 172401662
10000 297692184
3000 short numbers: 1692 grew a digit, checksum 539782755
50 long numbers: 24 grew a digit, checksum 311921552
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the digits read as one number, that number times 2, and its
digits written out again by an f-string; no carry and no list. It draws
2000 random numbers of 1 to 12 digits, then 50 of up to 3000, all before
any arm answers; the literal reading is asked only of the first 2000.
The four own arms share one `shared` list; the solution's plain one is
renamed `BoxNode` there.

| | property |
|---|---|
| P1 | up to 12 digits, the digits are the literal reading's |
| P2 | digits from 0 to 9, no leading 0 but for 0 itself, and one digit more just when the first was 5 or more |
| P3 | halved by long division: the number given |
| P4 | the last digit the given last digit's double, modulo 10 |
| P5 | the number with a 0 after it: the answer with a 0 after it |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 198206391, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a 0 put in front from 6 up, not 5 | P1 226, P2 230, P3 230, P6 230 |
| M2 | ★: the next digit's carry taken from 6 up | P1 954, P2 230, P3 1004, P6 1004 |
| M3 | prev: the carry added to the digit itself | P1 1850, P2 1152, P3 1900, P4 1060, P6 1900 |
| M4 | prev: the front node always kept | P1 875, P2 898, P6 898 |
| M5 | reverse: the list never turned back | P1 1770, P2 176, P3 1820, P4 1692, P5 2014, P6 1820 |
| M6 | reverse: the carry left over dropped | P1 1125, P2 1152, P3 1152, P6 1152 |
| M7 | stack: the carry never added in | P1 1663, P3 1713, P6 1713 |
| M8 | stack: the list built front to back | P1 1899, P2 416, P3 1949, P4 1896, P5 2036, P6 1949 |
| M9 | solution: the carry read as the remainder | P1 1850, P2 1152, P3 1900, P6 1900 |
| M10 | solution: the front node's carry doubled | P1 1125, P3 1152, P6 1152 |

## Benchmarks

The bench draws 200 numbers of 10^4 digits, LeetCode's most, all of
them first, then builds each as a list and doubles it 20 times by the ★
arm in all five languages, reading the list back after each: Kāra's
nodes are `shared`, counted references; Rust's are LeetCode's boxes, C's
`malloc`ed and freed node by node, Go's collected. Every implementation
prints `200 numbers of 10000 digits, 20 rounds: digits sum to
179948620, checksum 682272508`.

BENCHTAB

## Verification

All five arms print the same output as `double.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written.

LeetCode's Rust template took 35 `karac fix` edits in one run, the
wrapper included: `Option<Box<ListNode>>` became `Option[ListNode]`
everywhere and `Box::new(..)` went, Kāra's struct being a value that
can hold itself in an `Option`; the nested `fn carry` was hoisted to
the top level; `&mut Option<..>` became `mut ref Option[..]` and
`carry(&mut n.next)` `carry(mut n.next)`; `head` taken by value became
`own`, in the method and the wrapper; `struct Solution {}` was added
and `Solution::` took `.`. LeetCode's `#[derive(PartialEq, Eq, Clone,
Debug)]` and `#[inline]` lines and the `match node { None => 0, Some(n)
=> { .. } }` over the `mut ref` are Kāra as written.
