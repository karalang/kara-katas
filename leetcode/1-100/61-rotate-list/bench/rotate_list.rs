// Benchmark workload — Rotate List (LeetCode #61).
// Rust mirror of bench/rotate_list.kara. Uses `Rc<RefCell<ListNode>>` to
// mirror Kāra's `shared struct` reference semantics — same per-node RC
// overhead and the same alloc-per-node build + close-the-ring + cut shape.
// Same N/K, append list-builder, rotation sweep `r = k % (2*N)`, and sink.
// The transient ring is severed before returning, so no reference cycle
// survives to leak. Compiled with `rustc -O`. See ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn rotate_right(head: Link, k: i64) -> Link {
    // Measure the length and hold onto the tail.
    let mut len: i64 = 0;
    let mut cur = head.clone();
    let mut tail: Link = None;
    while let Some(node) = cur {
        len += 1;
        tail = Some(node.clone());
        cur = node.borrow().next.clone();
    }

    if len == 0 {
        return None;
    }
    let shift = k % len;
    if shift == 0 {
        return head;
    }

    // Close the ring: old tail -> old head.
    if let Some(t) = &tail {
        t.borrow_mut().next = head.clone();
    }

    // Walk to the new tail, (len - shift - 1) steps from the old head.
    let steps = len - shift - 1;
    let mut new_tail = head.clone();
    let mut i = 0;
    while i < steps {
        let next = new_tail.as_ref().and_then(|n| n.borrow().next.clone());
        new_tail = next;
        i += 1;
    }

    // Sever the ring just after the new tail.
    let mut result = head;
    if let Some(nt) = new_tail {
        result = nt.borrow().next.clone();
        nt.borrow_mut().next = None;
    }
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
    let span: i64 = 200; // 2*N
    let k_iters: i64 = 500_000;

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let list = build_list(n_values);
        let r = k % span;
        let out = rotate_right(list, r);
        if let Some(node) = std::hint::black_box(out) {
            sum += node.borrow().val;
        }
    }
    println!("{}", sum);
}
