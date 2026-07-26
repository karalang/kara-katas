// Benchmark harness for LeetCode #264 — Ugly Number II.
// Mirrors ugly_number_ii.kara algorithm-for-algorithm.

fn nth_ugly(n: i64) -> i64 {
    let mut dp: Vec<i64> = Vec::new();
    dp.push(1);

    let mut i2 = 0usize;
    let mut i3 = 0usize;
    let mut i5 = 0usize;

    while (dp.len() as i64) < n {
        let c2 = dp[i2] * 2;
        let c3 = dp[i3] * 3;
        let c5 = dp[i5] * 5;

        let mut next = c2;
        if c3 < next {
            next = c3;
        }
        if c5 < next {
            next = c5;
        }

        dp.push(next);

        if c2 == next {
            i2 += 1;
        }
        if c3 == next {
            i3 += 1;
        }
        if c5 == next {
            i5 += 1;
        }
    }
    dp[(n - 1) as usize]
}

fn main() {
    let iters: i64 = 12000;

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let n = 9000 + (it * 37) % 3001;
        sink = (sink * 31 + nth_ugly(n)) % 1000000007;
        it += 1;
    }
    println!("{}", sink);
}
