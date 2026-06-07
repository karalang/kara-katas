// Benchmark workload — Merge k Sorted Lists (LeetCode #23), divide and
// conquer. Rust mirror of bench/divide_and_conquer.kara. Uses
// `Rc<RefCell<ListNode>>` to mirror Kāra's `shared struct` reference
// semantics — same per-node RC overhead, same alloc-per-node build +
// in-place pairwise re-link shape. Same k/N/K, stride-k interleaving, and
// full-traversal sink. Compiled with `rustc -O`.
// See ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn merge_two_lists(l1: Link, l2: Link) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: 0, next: None }));
    let mut tail = dummy.clone();
    let mut a = l1;
    let mut b = l2;
    loop {
        let a_node = a.clone();
        let b_node = b.clone();
        match (a_node, b_node) {
            (Some(na), Some(nb)) => {
                if na.borrow().val <= nb.borrow().val {
                    tail.borrow_mut().next = Some(na.clone());
                    let next = na.borrow().next.clone();
                    tail = na;
                    a = next;
                } else {
                    tail.borrow_mut().next = Some(nb.clone());
                    let next = nb.borrow().next.clone();
                    tail = nb;
                    b = next;
                }
            }
            (Some(_), None) => {
                tail.borrow_mut().next = a;
                break;
            }
            (None, _) => {
                tail.borrow_mut().next = b;
                break;
            }
        }
    }
    let result = dummy.borrow().next.clone();
    result
}

fn merge_k_lists(mut lists: Vec<Link>) -> Link {
    let k = lists.len();
    if k == 0 {
        return None;
    }
    let mut interval = 1;
    while interval < k {
        let mut i = 0;
        while i + interval < k {
            lists[i] = merge_two_lists(lists[i].clone(), lists[i + interval].clone());
            i += 2 * interval;
        }
        interval *= 2;
    }
    lists[0].clone()
}

fn build_list(start: i64, step: i64, count: i64) -> Link {
    if count <= 0 {
        return None;
    }
    let head = Rc::new(RefCell::new(ListNode {
        val: start,
        next: None,
    }));
    let mut tail = head.clone();
    let mut v = start;
    for _ in 1..count {
        v += step;
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
    let k_lists: i64 = 8;
    let n_values: i64 = 128;
    let k_iters: i64 = 100_000;

    let mut total: i64 = 0;
    for _ in 0..k_iters {
        let mut lists: Vec<Link> = Vec::new();
        for j in 0..k_lists {
            lists.push(build_list(j, k_lists, n_values));
        }
        let merged = std::hint::black_box(merge_k_lists(lists));
        total += sum_list(merged);
    }
    println!("{}", total);
}
