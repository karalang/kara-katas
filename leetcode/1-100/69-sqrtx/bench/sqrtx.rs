// Benchmark workload — Sqrt(x) (LeetCode #69).
// Rust mirror of bench/sqrtx.kara. The ★'s binary search for floor(sqrt(x)) run
// K=3_000_000 times over a Knuth-multiplicative sweep of x across [0, 2^31),
// folding results into a rolling polynomial hash. No allocation — a pure
// compute/branch benchmark of the search loop. Compiled with `rustc -O`.
// See ../README.md § Benchmarks.

fn my_sqrt(x: i64) -> i64 {
    let mut lo = 0i64;
    let mut hi = x;
    let mut ans = 0i64;
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        if mid * mid <= x {
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    ans
}

fn main() {
    let total: i64 = 3_000_000;
    let modulus: i64 = 1_000_000_007;
    let range: i64 = 2_147_483_648; // 2^31

    let mut acc: i64 = 0;
    for k in 0..total {
        let x = (k * 2_654_435_761) % range;
        let r = std::hint::black_box(my_sqrt(x));
        acc = (acc * 131 + r) % modulus;
    }
    println!("{}", acc);
}
