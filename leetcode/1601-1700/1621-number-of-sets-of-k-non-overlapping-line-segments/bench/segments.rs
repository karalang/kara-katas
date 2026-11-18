// LeetCode #1621: Number of Sets of K Non-Overlapping Line Segments -- the
// bench in Rust, mirroring segments.kara: C(n + k - 1, 2k) by factorials
// and Fermat's inverse, the factorials made afresh for every query.

const MOD: i64 = 1000000007;

fn power(base: i64, exp: i64) -> i64 {
    let (mut result, mut b, mut e) = (1, base % MOD, exp);
    while e > 0 {
        if e & 1 == 1 {
            result = result * b % MOD;
        }
        b = b * b % MOD;
        e >>= 1;
    }
    result
}

fn number_of_sets(n: i32, k: i32) -> i32 {
    let top = (n + k - 1) as usize;
    let pick = 2 * k as usize;
    let mut fact = vec![1i64; top + 1];
    for i in 1..=top {
        fact[i] = fact[i - 1] * i as i64 % MOD;
    }
    let below = fact[pick] * fact[top - pick] % MOD;
    (fact[top] * power(below, MOD - 2) % MOD) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1621;
    let mut pairs: Vec<(i32, i32)> = Vec::new();
    for _ in 0..400000 {
        let n = (next_random(&mut seed) % 999 + 2) as i32;
        let k = (next_random(&mut seed) % (n as i64 - 1) + 1) as i32;
        pairs.push((n, k));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for &(n, k) in &pairs {
        let ways = number_of_sets(n, k) as i64;
        total = (total + ways) % MOD;
        check = (check * 31 + ways + 1) % 1000000007;
    }
    println!("400000 random pairs: counts sum to {total} mod 10^9 + 7, checksum {check}");
}
