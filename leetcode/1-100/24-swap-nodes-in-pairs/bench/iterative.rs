// Benchmark workload — Swap Nodes in Pairs (LeetCode #24), iterative.
// Rust mirror of bench/iterative.kara. Uses `Rc<RefCell<ListNode>>` to mirror
// Kāra's `shared struct` reference semantics — same per-node RC overhead and
// the same alloc-per-node build + in-place pair re-link shape. Same N/K and
// full-traversal sink. Compiled with `rustc -O`.
// See ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn swap_pairs(head: Link) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: 0, next: head }));
    let mut prev = dummy.clone();
    loop {
        let first = prev.borrow().next.clone();
        let Some(first) = first else { break };
        let second = first.borrow().next.clone();
        let Some(second) = second else { break };
        // Re-link prev → second → first → rest.
        first.borrow_mut().next = second.borrow().next.clone();
        second.borrow_mut().next = Some(first.clone());
        prev.borrow_mut().next = Some(second);
        prev = first;
    }
    let result = dummy.borrow().next.clone();
    result
}

fn build_list(count: i64) -> Link {
    if count <= 0 {
        return None;
    }
    let head = Rc::new(RefCell::new(ListNode { val: 1, next: None }));
    let mut tail = head.clone();
    for v in 2..=count {
        let node = Rc::new(RefCell::new(ListNode { val: v, next: None }));
        tail.borrow_mut().next = Some(node.clone());
        tail = node;
    }
    Some(head)
}

fn sum_list(list: Link) -> i64 {
    let mut s = 0i64;
    let mut c = list;
    while let Some(n) = c {
        s += n.borrow().val;
        c = n.borrow().next.clone();
    }
    s
}

fn main() {
    let n_values: i64 = 100;
    let k_iters: i64 = 500_000;

    let mut total: i64 = 0;
    for _ in 0..k_iters {
        let list = build_list(n_values);
        let swapped = std::hint::black_box(swap_pairs(list));
        total += sum_list(swapped);
    }
    println!("{}", total);
}
