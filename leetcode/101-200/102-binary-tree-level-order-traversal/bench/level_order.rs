// Benchmark workload for LeetCode #102 — level order, Rust mirror (Box + &-borrow).
// The tree is never mutated or shared during traversal, so a single-owner Box walked
// by reference is the honest Rust node. Build 8 BSTs once, then K reps of DFS-with-depth
// level_order on a data-dependent-selected tree, folding the whole Vec<Vec<i64>> result
// into a rolling hash. Each rep allocates a fresh Vec<Vec<i64>> and drops it.
const MOD: i64 = 1000000007;

struct Node { val: i64, left: Option<Box<Node>>, right: Option<Box<Node>> }

fn insert(root: Option<Box<Node>>, v: i64) -> Option<Box<Node>> {
    match root {
        None => Some(Box::new(Node { val: v, left: None, right: None })),
        Some(mut n) => {
            if v < n.val { n.left = insert(n.left.take(), v); }
            else { n.right = insert(n.right.take(), v); }
            Some(n)
        }
    }
}

fn dfs(node: &Option<Box<Node>>, depth: usize, result: &mut Vec<Vec<i64>>) {
    if let Some(n) = node {
        if depth == result.len() { result.push(Vec::new()); }
        result[depth].push(n.val);
        dfs(&n.left, depth + 1, result);
        dfs(&n.right, depth + 1, result);
    }
}

fn level_order(root: &Option<Box<Node>>) -> Vec<Vec<i64>> {
    let mut result: Vec<Vec<i64>> = Vec::new();
    dfs(root, 0, &mut result);
    result
}

fn main() {
    let base: [i64; 15] = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30];
    let bn = base.len();
    let mut pool: Vec<Option<Box<Node>>> = Vec::new();
    for t in 0..8 {
        let mut root: Option<Box<Node>> = None;
        for k in 0..bn { root = insert(root, base[(k + t) % bn]); }
        pool.push(root);
    }
    let mut acc: i64 = 1;
    for _ in 0..1500000i64 {
        let idx = (acc % 8) as usize;
        let levels = level_order(&pool[idx]);
        acc = (acc * 131 + levels.len() as i64) % MOD;
        for lvl in &levels {
            acc = (acc * 131 + lvl.len() as i64) % MOD;
            for &v in lvl {
                acc = (acc * 131 + v) % MOD;
            }
        }
    }
    println!("{}", acc);
}
