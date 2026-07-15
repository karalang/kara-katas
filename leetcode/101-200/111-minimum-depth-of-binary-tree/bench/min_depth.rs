// Benchmark workload for LeetCode #111 — minimum depth, Rust mirror (Box + &-borrow).
// The tree is never mutated or shared during traversal, so a single-owner Box walked by
// reference is the honest Rust node. Build 8 balanced 31-node trees once, then K reps of
// recursive min_depth on a data-dependent-selected tree, folding each min depth.
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
fn min_depth(node: &Option<Box<Node>>) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let ld = min_depth(&n.left);
            let rd = min_depth(&n.right);
            if ld == 0 { return 1 + rd; }
            if rd == 0 { return 1 + ld; }
            1 + if ld < rd { ld } else { rd }
        }
    }
}

fn main() {
    let mut pool: Vec<Option<Box<Node>>> = Vec::new();
    for t in 0..8i64 { pool.push(build_balanced(t * 100, t * 100 + 30)); }
    let mut acc: i64 = 1;
    for _ in 0..3000000i64 {
        let idx = (acc % 8) as usize;
        let d = min_depth(&pool[idx]);
        acc = (acc * 131 + d + 1) % MOD;
    }
    println!("{}", acc);
}
