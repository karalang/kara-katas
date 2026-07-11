// Benchmark workload — Partition List (LeetCode #86), SEQ lane.
// Rust mirror of bench/partition_list.kara. Uses `Rc<RefCell<ListNode>>` to mirror
// Kāra's `shared struct` reference semantics — same per-node RC overhead and
// alloc-per-node build + in-place re-link. Each iteration builds a fresh M=200 list,
// stably partitions around x=50, and adds the fold into an associative sum. Same M/K.
// Compiled with `rustc -O`. The rayon/ sibling parallelises the same reduction.
// See ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn partition(head: Link, x: i64) -> Link {
    let less_dummy = Rc::new(RefCell::new(ListNode { val: 0, next: None }));
    let greater_dummy = Rc::new(RefCell::new(ListNode { val: 0, next: None }));
    let mut less_tail = less_dummy.clone();
    let mut greater_tail = greater_dummy.clone();
    let mut cur = head;
    while let Some(node) = cur {
        let nxt = node.borrow().next.clone();
        node.borrow_mut().next = None;
        if node.borrow().val < x {
            less_tail.borrow_mut().next = Some(node.clone());
            less_tail = node;
        } else {
            greater_tail.borrow_mut().next = Some(node.clone());
            greater_tail = node;
        }
        cur = nxt;
    }
    let g = greater_dummy.borrow().next.clone();
    less_tail.borrow_mut().next = g;
    let result = less_dummy.borrow().next.clone();
    result
}

fn build(m: i64, seed: i64) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: -1, next: None }));
    let mut tail = dummy.clone();
    let mut j = 0i64;
    while j < m {
        let node = Rc::new(RefCell::new(ListNode {
            val: (j * 7 + seed) % 100,
            next: None,
        }));
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
    const TOTAL: i64 = 170000;
    let mut sum: i64 = 0;
    for k in 0..TOTAL {
        let list = build(M, k);
        let p = partition(list, 50);
        sum += fold(p, k);
    }
    println!("{}", sum);
}
