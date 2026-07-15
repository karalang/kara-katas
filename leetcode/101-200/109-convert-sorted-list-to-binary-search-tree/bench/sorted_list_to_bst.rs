// Benchmark workload for LeetCode #109 — sorted list to BST, Rust mirror.
// The input list is a shared, immutable structure read many times, so `Rc<ListNode>` is the
// honest Rust list (reference-counted, kept alive across reps like Kāra's `shared`); the output
// tree is single-owner `Box` (built then dropped). Build 8 lists once, then K reps of the
// array-conversion sorted_list_to_bst on a data-dependent-selected list.
use std::rc::Rc;
const MOD: i64 = 1000000007;

struct LNode { val: i64, next: Option<Rc<LNode>> }
struct TNode { val: i64, left: Option<Box<TNode>>, right: Option<Box<TNode>> }

fn build_list(len: i64, off: i64) -> Option<Rc<LNode>> {
    let mut head: Option<Rc<LNode>> = None;
    for i in (0..len).rev() {
        head = Some(Rc::new(LNode { val: off + 1 + i, next: head.take() }));
    }
    head
}
fn build_from_arr(arr: &[i64], lo: i64, hi: i64) -> Option<Box<TNode>> {
    if lo > hi { return None; }
    let mid = (lo + hi) / 2;
    Some(Box::new(TNode {
        val: arr[mid as usize],
        left: build_from_arr(arr, lo, mid - 1),
        right: build_from_arr(arr, mid + 1, hi),
    }))
}
fn sorted_list_to_bst(head: &Option<Rc<LNode>>) -> Option<Box<TNode>> {
    let mut arr: Vec<i64> = Vec::new();
    let mut cur = head.clone();
    while let Some(n) = cur {
        arr.push(n.val);
        cur = n.next.clone();
    }
    build_from_arr(&arr, 0, arr.len() as i64 - 1)
}
fn ser(node: &Option<Box<TNode>>, acc: i64) -> i64 {
    match node {
        None => (acc * 131 + 1) % MOD,
        Some(n) => {
            let mut a = (acc * 131 + (n.val + 2)) % MOD;
            a = ser(&n.left, a);
            a = ser(&n.right, a);
            a
        }
    }
}

fn main() {
    let mut pool: Vec<Option<Rc<LNode>>> = Vec::new();
    for t in 0..8i64 { pool.push(build_list(15, t * 100)); }
    let mut acc: i64 = 1;
    for _ in 0..1000000i64 {
        let idx = (acc % 8) as usize;
        let root = sorted_list_to_bst(&pool[idx]);
        let s = ser(&root, 0);
        acc = (acc * 131 + s) % MOD;
    }
    println!("{}", acc);
}
