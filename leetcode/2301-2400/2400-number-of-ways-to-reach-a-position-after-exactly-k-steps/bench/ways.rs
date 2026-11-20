// LeetCode #2400: Number of Ways to Reach a Position After Exactly k
// Steps -- the bench, the ★ arm in Rust: C(k, (k + d) / 2) from factorials
// modulo 10^9 + 7 and Fermat's inverse.

const MOD: i64 = 1_000_000_007;

fn power(base: i64, exponent: i64) -> i64 {
    let mut result = 1;
    let mut b = base % MOD;
    let mut e = exponent;
    while e > 0 {
        if e % 2 == 1 {
            result = result * b % MOD;
        }
        b = b * b % MOD;
        e /= 2;
    }
    result
}

fn number_of_ways(start_pos: i64, end_pos: i64, k: i64) -> i64 {
    let d = (end_pos - start_pos).abs();
    if d > k || (k - d) % 2 == 1 {
        return 0;
    }
    let toward = ((k + d) / 2) as usize;
    let k = k as usize;
    let mut factorial = vec![1i64; k + 1];
    for i in 1..=k {
        factorial[i] = factorial[i - 1] * i as i64 % MOD;
    }
    factorial[k] * power(factorial[toward], MOD - 2) % MOD * power(factorial[k - toward], MOD - 2) % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2400;
    let mut check = 0;
    let mut zeros = 0;
    for _ in 0..300000 {
        let k = 1 + next_random(&mut seed) % 1000;
        let start = 1 + next_random(&mut seed) % 1000;
        let end = (start - k + 2 * (next_random(&mut seed) % (k + 1))).clamp(1, 1000);
        let w = number_of_ways(start, end, k);
        if w == 0 {
            zeros += 1;
        }
        check = (check * 31 + w) % MOD;
    }
    println!("300000 queries of k up to 1000: checksum {}, {} zeros", check, zeros);
}
