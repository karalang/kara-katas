// Benchmark workload for LeetCode #108 — sorted array to BST, Rust mirror (Box).
// The tree is single-owner (built then dropped, never shared), so Box is the honest Rust
// node. Build 8 sorted arrays once, then K reps of recursive middle-pick sorted_to_bst on a
// data-dependent-selected array, folding the built tree's serialization into a rolling hash.
const MOD: i64 = 1000000007;

struct Node { val: i64, left: Option<Box<Node>>, right: Option<Box<Node>> }

fn build(arr: &[i64], lo: i64, hi: i64) -> Option<Box<Node>> {
    if lo > hi { return None; }
    let mid = (lo + hi) / 2;
    Some(Box::new(Node {
        val: arr[mid as usize],
        left: build(arr, lo, mid - 1),
        right: build(arr, mid + 1, hi),
    }))
}
fn ser(node: &Option<Box<Node>>, acc: i64) -> i64 {
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
    let mut arrs: Vec<[i64; 15]> = Vec::new();
    for t in 0..8i64 {
        let mut a = [0i64; 15];
        for i in 0..15i64 { a[i as usize] = t * 100 + i; }
        arrs.push(a);
    }
    let mut acc: i64 = 1;
    for _ in 0..1200000i64 {
        let idx = (acc % 8) as usize;
        let root = build(&arrs[idx], 0, 14);
        let s = ser(&root, 0);
        acc = (acc * 131 + s) % MOD;
    }
    println!("{}", acc);
}
