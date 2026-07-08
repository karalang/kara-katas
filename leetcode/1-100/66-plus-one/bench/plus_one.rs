// Benchmark workload — Plus One (LeetCode #66).
// Rust mirror of bench/plus_one.kara. A fixed-width (W=9) decimal digit buffer
// driven as a base-10 counter: the ★'s reverse-scan carry applied in place K
// times, folding a rotating digit into a rolling polynomial-hash sink. In place,
// no per-iter allocation. K < 10^9 so the counter never overflows 9 digits.
// Compiled with `rustc -O`. See ../README.md § Benchmarks.

fn main() {
    let total: i64 = 80_000_000;
    let modulus: i64 = 1_000_000_007;
    const W: usize = 9;

    let mut digits: [i64; W] = [0; W];

    let mut acc: i64 = 0;
    for k in 0..total {
        let mut i: isize = W as isize - 1;
        while i >= 0 {
            if digits[i as usize] < 9 {
                digits[i as usize] += 1;
                break; // carry absorbed
            }
            digits[i as usize] = 0;
            i -= 1;
        }
        acc = std::hint::black_box((acc * 131 + digits[(k as usize) % W]) % modulus);
    }

    println!("{}", acc);
}
