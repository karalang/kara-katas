// Benchmark workload — Remove Nth Node From End (LeetCode #19).
// Rust mirror of bench/remove_nth.kara. Uses `Rc<RefCell<ListNode>>` to
// mirror Kāra's `shared struct` reference semantics — same per-node RC
// overhead and the same alloc-per-node build + in-place splice shape.
// Same N/K, append list-builder, rotating removal position, and sink.
// Compiled with `rustc -O`. See ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn remove_nth_from_end(head: Link, n: i64) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode {
        val: 0,
        next: head.clone(),
    }));

    // Lead `fast` n nodes into the list from the head.
    let mut fast = head;
    let mut i = 0;
    while i < n {
        let next = fast.as_ref().and_then(|node| node.borrow().next.clone());
        fast = next;
        i += 1;
    }

    // Walk `slow` (from the dummy) and `fast` in lockstep until `fast` runs
    // off the end. `slow` then rests just before the target.
    let mut slow = dummy.clone();
    while fast.is_some() {
        let fnext = fast.as_ref().and_then(|node| node.borrow().next.clone());
        fast = fnext;
        let snext = slow.borrow().next.clone();
        if let Some(s) = snext {
            slow = s;
        }
    }

    // Splice out `slow.next` (the n-th node from the end).
    let new_next = {
        let slow_ref = slow.borrow();
        match &slow_ref.next {
            Some(target) => target.borrow().next.clone(),
            None => None,
        }
    };
    if slow.borrow().next.is_some() {
        slow.borrow_mut().next = new_next;
    }

    let result = dummy.borrow().next.clone();
    result
}

// Build a fresh `count`-node list valued 1..count, append via a tail cursor.
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

fn main() {
    let n_values: i64 = 100;
    let k_iters: i64 = 500_000;

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let list = build_list(n_values);
        let n = (k % n_values) + 1;
        let out = remove_nth_from_end(list, n);
        if let Some(node) = std::hint::black_box(out) {
            sum += node.borrow().val;
        }
    }
    println!("{}", sum);
}
