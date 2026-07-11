// Benchmark workload — Combinations (LeetCode #77).
// Rust mirror of bench/combinations.kara. Start-indexed pruned backtracking that
// ENUMERATES all C(16,8)=12870 combinations and folds each leaf's values into a
// threaded accumulator (no Vec-of-Vec storage), K=1500 iterations seeded by the
// iteration index. The DFS recursion is the measured work. See ../README.md.

fn enumerate(n: i64, k: i64, start: i64, path: &mut Vec<i64>, acc: i64) -> i64 {
    if path.len() as i64 == k {
        let mut a = acc;
        for &x in path.iter() {
            a = (a * 131 + x) % 1_000_000_007;
        }
        return a;
    }
    let need = k - path.len() as i64;
    let limit = n - need + 1;
    let mut a = acc;
    let mut i = start;
    while i <= limit {
        path.push(i);
        a = enumerate(n, k, i + 1, path, a);
        path.pop();
        i += 1;
    }
    a
}

fn main() {
    const N: i64 = 16;
    const K: i64 = 8;
    const TOTAL: i64 = 1500;
    const MODULUS: i64 = 1_000_000_007;

    let mut path: Vec<i64> = Vec::new();
    let mut sum: i64 = 0;
    for iter in 0..TOTAL {
        let r = enumerate(N, K, 1, &mut path, iter);
        sum = (sum + r) % MODULUS;
    }
    println!("{}", sum);
}
