// Benchmark workload — Unique Paths (LeetCode #62).
// Rust mirror of bench/unique_paths.kara. `Vec<i64>` rolling-DP array allocated
// and filled per call, sized to the smaller axis — the same heap traffic as
// Kāra's per-call `Vec[i64]`. Same K/span sweep, the same `dp[c] += dp[c-1]`
// recurrence, and the same rolling polynomial-hash sink. Compiled with
// `rustc -O`. See ../README.md § Benchmarks.

fn unique_paths(m: i64, n: i64) -> i64 {
    let (mut rows, mut cols) = (m, n);
    if cols > rows {
        std::mem::swap(&mut rows, &mut cols);
    }

    let mut dp: Vec<i64> = vec![1; cols as usize];
    for _ in 1..rows {
        for c in 1..cols as usize {
            dp[c] += dp[c - 1];
        }
    }
    dp[cols as usize - 1]
}

fn main() {
    let total: i64 = 1_000_000;
    let modulus: i64 = 1_000_000_007;
    let span: i64 = 32;

    let mut acc: i64 = 0;
    for k in 0..total {
        let m = 2 + (k % span);
        let n = 2 + ((k / span) % span);
        let ans = std::hint::black_box(unique_paths(m, n));
        acc = (acc * 131 + ans) % modulus;
    }
    println!("{}", acc);
}
