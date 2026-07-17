// LeetCode #120 — Rust mirror, bottom-up rolling min-path DP.
// Same algorithm + workload as triangle.kara: build one N-row triangle once, then punch the O(N^2)
// min-path DP K=20000 times with a data-dependent seed (base-row perturbation (seed+j)%7). Kara
// checks integer overflow by default, so the like-for-like row is `rustc -O -C overflow-checks=on`.
const MOD: i64 = 1000000007;

fn min_path(tri: &[Vec<i64>], seed: i64) -> i64 {
    let n = tri.len();
    let mut dp = vec![0i64; n];
    for j in 0..n {
        dp[j] = tri[n - 1][j] + ((seed + j as i64) % 7);
    }
    for i in (0..n - 1).rev() {
        for k in 0..=i {
            let a = dp[k];
            let b = dp[k + 1];
            let m = if a < b { a } else { b };
            dp[k] = tri[i][k] + m;
        }
    }
    dp[0]
}

fn main() {
    let nrows: i64 = 200;
    let mut tri: Vec<Vec<i64>> = Vec::new();
    for i in 0..nrows {
        let mut row: Vec<i64> = Vec::new();
        for j in 0..=i {
            row.push((i * 31 + j * 17) % 100);
        }
        tri.push(row);
    }
    let mut acc: i64 = 0;
    for _ in 0..20000 {
        let seed = acc % 97;
        let mp = min_path(&tri, seed);
        acc = (acc * 131 + mp) % MOD;
    }
    println!("{}", acc);
}
