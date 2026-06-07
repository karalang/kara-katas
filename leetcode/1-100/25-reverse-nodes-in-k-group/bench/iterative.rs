// Benchmark workload — Reverse Nodes in k-Group (LeetCode #25), iterative.
// Rust mirror of bench/iterative.kara. Uses `Rc<RefCell<ListNode>>` to mirror
// Kāra's `shared struct` reference semantics — same per-node RC overhead and
// the same alloc-per-node build + in-place group reversal shape. Same N/K/k
// and full-traversal sink. Compiled with `rustc -O`.
// See ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn reverse_k_group(head: Link, k: i64) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: 0, next: head }));
    let mut group_prev = dummy.clone();
    loop {
        // Probe k nodes ahead; a partial trailing group stays in place.
        let mut probe = group_prev.borrow().next.clone();
        let mut count = 0i64;
        while count < k {
            let Some(node) = probe else { break };
            probe = node.borrow().next.clone();
            count += 1;
        }
        if count < k {
            break;
        }
        let group_head = group_prev.borrow().next.clone().unwrap();
        // Reverse exactly k nodes, prev seeded with the suffix.
        let mut prev = probe;
        let mut cur = group_prev.borrow().next.clone();
        for _ in 0..k {
            let node = cur.unwrap();
            let nxt = node.borrow().next.clone();
            node.borrow_mut().next = prev;
            prev = Some(node);
            cur = nxt;
        }
        group_prev.borrow_mut().next = prev;
        group_prev = group_head;
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
        let reversed = std::hint::black_box(reverse_k_group(list, 5));
        total += sum_list(reversed);
    }
    println!("{}", total);
}
