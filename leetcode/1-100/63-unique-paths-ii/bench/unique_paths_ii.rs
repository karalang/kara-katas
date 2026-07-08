// Benchmark workload — Unique Paths II (LeetCode #63).
// Rust mirror of bench/unique_paths_ii.kara. `Vec<i64>` rolling-DP array
// allocated and filled per call, sized to the real column count n (obstacles
// break #62's axis symmetry — no swap to the smaller side) — the same heap
// traffic as Kāra's per-call `Vec[i64]`. Same K/span sweep, the same
// `dp[c] += dp[c-1]` recurrence, the same inline obstacle predicate
// ((i*7 + c*3 + k) % 13 == 0), and the same rolling polynomial-hash sink.
// Compiled with `rustc -O`. See ../README.md § Benchmarks.

fn unique_paths_with_obstacles(m: i64, n: i64, k: i64) -> i64 {
    let cols = n;

    let mut dp: Vec<i64> = vec![0; cols as usize];
    dp[0] = 1;

    for i in 0..m {
        for c in 0..cols {
            if (i * 7 + c * 3 + k) % 13 == 0 {
                dp[c as usize] = 0;
            } else if c > 0 {
                dp[c as usize] += dp[c as usize - 1];
            }
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
        let ans = std::hint::black_box(unique_paths_with_obstacles(m, n, k));
        acc = (acc * 131 + ans) % modulus;
    }
    println!("{}", acc);
}
