// LeetCode #86 — rayon-parallel Rust mirror (par lane).
// Same batch of K=170000 independent partitions as ../partition_list.rs; the
// associative sum reduction runs across a rayon pool. Each task builds its own
// Rc<RefCell<>> lists locally (Rc stays thread-local, never shared), so the per-node
// RC overhead matches the seq mirror. Hand-tuned-parallel comparator for Kāra's
// auto-par. Sink matches the seq mirrors.
use rayon::prelude::*;
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

const M: i64 = 200;

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

fn build(seed: i64) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: -1, next: None }));
    let mut tail = dummy.clone();
    let mut j = 0i64;
    while j < M {
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

fn compute(seed: i64) -> i64 {
    fold(partition(build(seed), 50), seed)
}

fn main() {
    let sum: i64 = (0..170000_i64).into_par_iter().map(compute).sum();
    println!("{}", sum);
}
