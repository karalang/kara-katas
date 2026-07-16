// Benchmark workload for LeetCode #112 — path sum, Rust mirror (Box + &-borrow).
// The tree is never mutated or shared during the check, so a single-owner Box walked by
// reference is the honest Rust node. Build 8 balanced 31-node trees once, then K reps of
// has_path_sum against an unachievable target (full traversal) on a data-dependent-selected tree.
const MOD: i64 = 1000000007;
struct Node { val: i64, left: Option<Box<Node>>, right: Option<Box<Node>> }
fn build(lo: i64, hi: i64) -> Option<Box<Node>> {
    if lo > hi { return None; }
    let mid = (lo + hi) / 2;
    Some(Box::new(Node { val: mid, left: build(lo, mid - 1), right: build(mid + 1, hi) }))
}
fn has_path_sum(node: &Option<Box<Node>>, target: i64) -> bool {
    match node {
        None => false,
        Some(n) => {
            let rem = target - n.val;
            if n.left.is_none() && n.right.is_none() { rem == 0 }
            else { has_path_sum(&n.left, rem) || has_path_sum(&n.right, rem) }
        }
    }
}
fn main() {
    let mut pool: Vec<Option<Box<Node>>> = Vec::new();
    for t in 0..8i64 { pool.push(build(t * 100, t * 100 + 30)); }
    let mut acc: i64 = 1;
    for _ in 0..6000000i64 {
        let idx = (acc % 8) as usize;
        let hit = has_path_sum(&pool[idx], 1000000000);
        acc = (acc * 131 + (if hit { 1 } else { 0 }) + 1) % MOD;
    }
    println!("{}", acc);
}
