// Benchmark workload — Minimum Path Sum (LeetCode #64).
// Rust mirror of bench/minimum_path_sum.kara. `Vec<i64>` rolling-DP array
// allocated and filled per call, sized to the real column count n (costs break
// #62's axis symmetry — no swap) — the same heap traffic as Kāra's per-call
// `Vec[i64]`. Same K/span sweep, the same `dp[c] = cost + min(dp[c], dp[c-1])`
// recurrence (`min` via `i64::min`, Rust's stdlib counterpart to Kāra's
// `std.cmp::min`), the same inline cost predicate ((i*7 + c*3 + k) % 13 + 1),
// and the same rolling polynomial-hash sink. Compiled with `rustc -O`.
// See ../README.md § Benchmarks.

fn min_path_sum(m: i64, n: i64, k: i64) -> i64 {
    let cols = n;

    let mut dp: Vec<i64> = vec![0; cols as usize];
    for j in 0..cols {
        let cost = ((j * 3 + k) % 13) + 1; // i == 0
        dp[j as usize] = if j == 0 { cost } else { dp[j as usize - 1] + cost };
    }

    for i in 1..m {
        dp[0] += ((i * 7 + k) % 13) + 1;
        for c in 1..cols {
            let cost = ((i * 7 + c * 3 + k) % 13) + 1;
            dp[c as usize] = cost + dp[c as usize].min(dp[c as usize - 1]);
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
        let ans = std::hint::black_box(min_path_sum(m, n, k));
        acc = (acc * 131 + ans) % modulus;
    }
    println!("{}", acc);
}
