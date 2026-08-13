// Benchmark workload for LeetCode #258 — Add Digits (Rust mirror).
// Mirrors add_digits.kara algorithm-for-algorithm.

fn add_digits(num: i64) -> i64 {
    let mut n = num;
    while n >= 10 {
        let mut sum = 0i64;
        while n > 0 {
            sum += n % 10;
            n /= 10;
        }
        n = sum;
    }
    n
}

fn main() {
    let iters: i64 = 10000000;
    let mut state: i64 = 258258;
    let mut sink: i64 = 0;
    for _ in 0..iters {
        state = (state * 1103515245 + 12345) & 2147483647;
        let shift = (state / 65536) % 33;
        let v = (state / 8) * (1i64 << shift) % 9223372036854775807;
        sink = (sink + add_digits(v)) % 1000000007;
    }
    println!("{}", sink);
}
