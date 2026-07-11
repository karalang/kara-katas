// Benchmark workload — Remove Duplicates from Sorted List II (LeetCode #82).
// Rust mirror of bench/remove_duplicates_ii_list.kara. Uses `Rc<RefCell<ListNode>>`
// to mirror Kāra's `shared struct` reference semantics — same per-node RC overhead
// and the same alloc-per-node build + in-place re-link shape. Each iteration builds a
// fresh list, runs delete_duplicates, and folds the survivors through a rolling
// polynomial hash. Same M/K and even-duplicated/odd-single pattern. Compiled with
// `rustc -O`. See ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn delete_duplicates(head: Link) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: 0, next: head }));
    let mut prev = dummy.clone();
    let mut cur = dummy.borrow().next.clone();
    loop {
        let cur_node = cur.clone();
        match cur_node {
            Some(node) => {
                let is_dup = match node.borrow().next.clone() {
                    Some(nxt) => node.borrow().val == nxt.borrow().val,
                    None => false,
                };
                if is_dup {
                    let v = node.borrow().val;
                    let mut runner = cur.clone();
                    loop {
                        let rn_opt = runner.clone();
                        match rn_opt {
                            Some(rn) => {
                                if rn.borrow().val == v {
                                    let next = rn.borrow().next.clone();
                                    runner = next;
                                } else {
                                    break;
                                }
                            }
                            None => break,
                        }
                    }
                    prev.borrow_mut().next = runner.clone();
                    cur = runner;
                } else {
                    let next = node.borrow().next.clone();
                    prev = node;
                    cur = next;
                }
            }
            None => break,
        }
    }
    let result = dummy.borrow().next.clone();
    result
}

fn build(m: i64) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: -1, next: None }));
    let mut tail = dummy.clone();
    let mut v = 0i64;
    while v < m {
        let node = Rc::new(RefCell::new(ListNode { val: v, next: None }));
        tail.borrow_mut().next = Some(node.clone());
        tail = node;
        if v % 2 == 0 {
            let d = Rc::new(RefCell::new(ListNode { val: v, next: None }));
            tail.borrow_mut().next = Some(d.clone());
            tail = d;
        }
        v += 1;
    }
    let result = dummy.borrow().next.clone();
    result
}

fn fold(list: Link, seed: i64) -> i64 {
    let mut a = seed;
    let mut c = list;
    while let Some(n) = c {
        a = (a * 131 + (n.borrow().val + 1000)) % 1_000_000_007;
        c = n.borrow().next.clone();
    }
    a
}

fn main() {
    const M: i64 = 300;
    const TOTAL: i64 = 61000;
    const MODULUS: i64 = 1_000_000_007;

    let mut sum: i64 = 0;
    for k in 0..TOTAL {
        let list = build(M);
        let dedup = std::hint::black_box(delete_duplicates(list));
        sum = (sum * 131 + fold(dedup, k)) % MODULUS;
    }
    println!("{}", sum);
}
