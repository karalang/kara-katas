// Benchmark workload for LeetCode #96 — Catalan DP-table, Rust mirror.
// K reps of the O(n^2) DP at a data-dependent size (m = 2 + acc%18), folding each
// count into a rolling hash. A fresh Vec per call, matching Kara's Vec.new.
const MOD: i64 = 1_000_000_007;

fn num_trees(n: i64) -> i64 {
    let mut dp: Vec<i64> = Vec::new();
    dp.push(1);
    for k in 1..=n {
        let mut total = 0i64;
        for r in 1..=k {
            total += dp[(r - 1) as usize] * dp[(k - r) as usize];
        }
        dp.push(total);
    }
    dp[n as usize]
}

fn main() {
    let mut acc: i64 = 1;
    for _ in 0..5_000_000 {
        let m = 2 + (acc % 18);
        let c = num_trees(m);
        acc = (acc * 1000003 + c) % MOD;
    }
    println!("{}", acc);
}
