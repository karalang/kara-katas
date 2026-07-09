// Benchmark workload — Validate Binary Search Tree (LeetCode #98), equal-memory-semantics row.
// Rust mirror using `Rc<Node>` (reference-counted) instead of `Box<Node>` — the
// faithful match to Kāra's `shared struct TreeNode` (which is RC-backed). This is
// the honest like-for-like comparison for Kāra's RC on a build-heavy tree (the
// memory analogue of #69's overflow-checks=on equal-safety row). Compiled with
// `rustc -O`. See ../README.md § Benchmarks.
use std::rc::Rc;
struct Node { val: i64, left: Option<Rc<Node>>, right: Option<Rc<Node>> }
fn build(lo: i64, hi: i64, shift: i64) -> Option<Rc<Node>> {
    if lo > hi { return None; }
    let mid = lo + (hi - lo) / 2;
    Some(Rc::new(Node { val: shift + mid, left: build(lo, mid-1, shift), right: build(mid+1, hi, shift) }))
}
fn is_valid(node: &Option<Rc<Node>>, lo: Option<i64>, hi: Option<i64>) -> bool {
    match node {
        None => true,
        Some(n) => {
            let v = n.val;
            if let Some(l) = lo { if v <= l { return false; } }
            if let Some(h) = hi { if v >= h { return false; } }
            is_valid(&n.left, lo, Some(v)) && is_valid(&n.right, Some(v), hi)
        }
    }
}
fn main() {
    let (total, modulus, size): (i64,i64,i64) = (200_000, 1_000_000_007, 63);
    let mut acc: i64 = 0;
    for k in 0..total {
        let shift = k % 1000;
        let root = build(0, size-1, shift);
        let bit = if std::hint::black_box(is_valid(&root, None, None)) { 1 } else { 0 };
        acc = (acc * 131 + shift + bit) % modulus;
    }
    println!("{}", acc);
}
