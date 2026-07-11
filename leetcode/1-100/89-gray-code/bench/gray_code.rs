// Benchmark workload — Gray Code (LeetCode #89).
// Rust mirror of bench/gray_code.kara. Folds each gray code i ^ (i >> 1) through a
// rolling polynomial hash (loop-carried, iter-mixed so nothing hoists), N=65536 codes,
// K=2500 iterations. Compiled with `rustc -O`. See ../README.md § Benchmarks.

fn main() {
    const N: i64 = 65536;
    const TOTAL: i64 = 2500;
    const MODULUS: i64 = 1_000_000_007;

    let mut sum: i64 = 0;
    for iter in 0..TOTAL {
        let mut acc = iter;
        let mut i = 0i64;
        while i < N {
            let g = i ^ (i >> 1);
            acc = (acc * 131 + (g ^ iter)) % MODULUS;
            i += 1;
        }
        sum = (sum * 131 + acc) % MODULUS;
    }
    println!("{}", sum);
}
