// Benchmark workload — Remove Duplicates from Sorted List (LeetCode #83).
// Rust mirror of bench/remove_duplicates_list.kara. Uses `Rc<RefCell<ListNode>>` to
// mirror Kāra's `shared struct` reference semantics — same per-node RC overhead and
// alloc-per-node build + in-place re-link shape. Each iteration builds a fresh list
// (M=300, every value duplicated), runs the keep-one dedup, and folds the survivors
// through a rolling polynomial hash. Compiled with `rustc -O`. See ../README.md.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn delete_duplicates(head: Link) -> Link {
    let mut cur = head.clone();
    loop {
        let cur_node = cur.clone();
        match cur_node {
            Some(node) => {
                let nxt_opt = node.borrow().next.clone();
                match nxt_opt {
                    Some(nxt) => {
                        if node.borrow().val == nxt.borrow().val {
                            let after = nxt.borrow().next.clone();
                            node.borrow_mut().next = after;
                        } else {
                            cur = node.borrow().next.clone();
                        }
                    }
                    None => break,
                }
            }
            None => break,
        }
    }
    head
}

fn build(m: i64, dup: i64) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: -1, next: None }));
    let mut tail = dummy.clone();
    let mut v = 0i64;
    while v < m {
        let mut d = 0i64;
        while d < dup {
            let node = Rc::new(RefCell::new(ListNode { val: v, next: None }));
            tail.borrow_mut().next = Some(node.clone());
            tail = node;
            d += 1;
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
    const DUP: i64 = 2;
    const TOTAL: i64 = 70000;
    const MODULUS: i64 = 1_000_000_007;

    let mut sum: i64 = 0;
    for k in 0..TOTAL {
        let list = build(M, DUP);
        let dd = std::hint::black_box(delete_duplicates(list));
        sum = (sum * 131 + fold(dd, k)) % MODULUS;
    }
    println!("{}", sum);
}
