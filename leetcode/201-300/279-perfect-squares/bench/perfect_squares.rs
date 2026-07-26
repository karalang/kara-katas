// Benchmark harness for LeetCode #279 — Perfect Squares.
// Mirrors perfect_squares.kara algorithm-for-algorithm.

fn num_squares(n: i64) -> i64 {
    let mut dp: Vec<i64> = Vec::new();
    dp.push(0);
    let mut i = 1i64;
    while i <= n {
        let mut best = i;
        let mut j = 1i64;
        while j * j <= i {
            let cand = dp[(i - j * j) as usize] + 1;
            if cand < best {
                best = cand;
            }
            j += 1;
        }
        dp.push(best);
        i += 1;
    }
    dp[n as usize]
}

fn main() {
    let iters: i64 = 100;

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let n = 25000 + (it * 37) % 5001;
        sink = (sink * 31 + num_squares(n)) % 1000000007;
        it += 1;
    }
    println!("{}", sink);
}
