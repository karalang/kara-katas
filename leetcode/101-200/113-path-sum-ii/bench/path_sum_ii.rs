// Benchmark workload for LeetCode #113 — path sum II, Rust mirror (Box + &mut accumulator).
const MOD: i64 = 1000000007;
struct Node { val: i64, left: Option<Box<Node>>, right: Option<Box<Node>> }
fn build_perfect(depth: i64, val: i64) -> Option<Box<Node>> {
    if depth <= 0 { return None; }
    Some(Box::new(Node { val, left: build_perfect(depth-1, val), right: build_perfect(depth-1, val) }))
}
fn dfs(node: &Option<Box<Node>>, target: i64, path: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    if let Some(n) = node {
        path.push(n.val);
        let rem = target - n.val;
        if n.left.is_none() && n.right.is_none() {
            if rem == 0 { out.push(path.clone()); }
        } else {
            dfs(&n.left, rem, path, out);
            dfs(&n.right, rem, path, out);
        }
        path.pop();
    }
}
fn main() {
    let pool: Vec<Option<Box<Node>>> = (0..8i64).map(|t| build_perfect(5, t + 1)).collect();
    let mut acc: i64 = 1;
    for _ in 0..300000i64 {
        let idx = (acc % 8) as usize;
        let mut out: Vec<Vec<i64>> = Vec::new();
        let mut path: Vec<i64> = Vec::new();
        dfs(&pool[idx], 5 * (idx as i64 + 1), &mut path, &mut out);
        let mut h: i64 = out.len() as i64;
        for p in &out { for &v in p { h = (h * 131 + v) % MOD; } }
        acc = (acc * 1000003 + h + 1) % MOD;
    }
    println!("{}", acc);
}
