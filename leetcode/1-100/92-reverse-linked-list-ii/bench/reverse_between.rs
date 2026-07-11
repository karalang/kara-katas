// Benchmark workload — Reverse Linked List II (LeetCode #92).
// Rust mirror of bench/reverse_between.kara. Uses Rc<RefCell<ListNode>> to mirror
// Kara's shared struct reference semantics — same per-node RC overhead and alloc-per-
// node build + in-place re-link. Each iteration builds a fresh M=200 list, reverses a
// ~100-node window (shifting start), folds the result. Same M/K. Compiled with
// `rustc -O`. See ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn reverse_between(head: Link, left: i64, right: i64) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: 0, next: head }));
    let mut prev = dummy.clone();
    let mut i = 1i64;
    while i < left {
        let n = prev.borrow().next.clone();
        if let Some(node) = n {
            prev = node;
        }
        i += 1;
    }
    let cur_opt = prev.borrow().next.clone();
    if let Some(cur) = cur_opt {
        let mut j = left;
        while j < right {
            let nxt_opt = cur.borrow().next.clone();
            if let Some(nxt) = nxt_opt {
                let after = nxt.borrow().next.clone();
                cur.borrow_mut().next = after;
                nxt.borrow_mut().next = prev.borrow().next.clone();
                prev.borrow_mut().next = Some(nxt);
            }
            j += 1;
        }
    }
    let result = dummy.borrow().next.clone();
    result
}

fn build(m: i64, seed: i64) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: -1, next: None }));
    let mut tail = dummy.clone();
    let mut j = 0i64;
    while j < m {
        let node = Rc::new(RefCell::new(ListNode { val: (j + seed) % 1000, next: None }));
        tail.borrow_mut().next = Some(node.clone());
        tail = node;
        j += 1;
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
    const M: i64 = 200;
    const TOTAL: i64 = 178000;
    const MODULUS: i64 = 1_000_000_007;
    let mut sum: i64 = 0;
    for k in 0..TOTAL {
        let list = build(M, k);
        let left = 1 + (k % 50);
        let right = left + 100;
        let r = reverse_between(list, left, right);
        sum = (sum * 131 + fold(r, k)) % MODULUS;
    }
    println!("{}", sum);
}
