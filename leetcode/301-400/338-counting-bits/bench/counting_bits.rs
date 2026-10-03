// Benchmark workload for LeetCode #338 — Rust mirror of counting_bits.kara.

const TOP_N: i64 = 1000000;
const ROUNDS: i64 = 300;
const MODULUS: i64 = 1073741789;

fn count_bits(n: i64) -> Vec<i64> {
    let mut ans = vec![0i64; (n + 1) as usize];
    for i in 1..=n {
        ans[i as usize] = ans[(i >> 1) as usize] + (i & 1);
    }
    ans
}

fn main() {
    let mut sink = 0;
    for r in 0..ROUNDS {
        let n = TOP_N - r;
        let ans = count_bits(n);
        let picked = ans[n as usize] * 10000 + ans[(n / 3) as usize] * 100 + ans[((n * 7) / 11) as usize];
        sink = (sink * 1000003 + picked + ans.len() as i64) % MODULUS;
    }
    println!("{}", sink);
}
