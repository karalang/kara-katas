// Benchmark workload for LeetCode #110 — balanced binary tree, Rust mirror (Box + &-borrow).
// The tree is never mutated or shared during the check, so a single-owner Box walked by
// reference is the honest Rust node. Build 8 balanced 31-node trees once, then K reps of
// bottom-up single-pass is_balanced on a data-dependent-selected tree, folding each verdict.
const MOD: i64 = 1000000007;

struct Node { val: i64, left: Option<Box<Node>>, right: Option<Box<Node>> }

fn build_balanced(lo: i64, hi: i64) -> Option<Box<Node>> {
    if lo > hi { return None; }
    let mid = (lo + hi) / 2;
    Some(Box::new(Node {
        val: mid,
        left: build_balanced(lo, mid - 1),
        right: build_balanced(mid + 1, hi),
    }))
}
fn check(node: &Option<Box<Node>>) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let lh = check(&n.left);
            if lh == -1 { return -1; }
            let rh = check(&n.right);
            if rh == -1 { return -1; }
            let diff = lh - rh;
            if (if diff < 0 { -diff } else { diff }) > 1 { return -1; }
            1 + if lh > rh { lh } else { rh }
        }
    }
}
fn is_balanced(root: &Option<Box<Node>>) -> bool { check(root) != -1 }

fn main() {
    let mut pool: Vec<Option<Box<Node>>> = Vec::new();
    for t in 0..8i64 { pool.push(build_balanced(t * 100, t * 100 + 30)); }
    let mut acc: i64 = 1;
    for _ in 0..3000000i64 {
        let idx = (acc % 8) as usize;
        let bal = is_balanced(&pool[idx]);
        acc = (acc * 131 + (if bal { 1 } else { 0 }) + 1) % MOD;
    }
    println!("{}", acc);
}
