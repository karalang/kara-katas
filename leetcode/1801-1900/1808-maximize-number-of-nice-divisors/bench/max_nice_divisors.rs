// LeetCode #1808: Maximize Number of Nice Divisors -- the bench in Rust: the
// ★ arm over 2 * 10^6 calls, each count of prime factors drawn from the
// checksum so far.

const MOD: i64 = 1000000007;

fn power(base: i64, exp: i64) -> i64 {
    let mut result = 1;
    let mut b = base % MOD;
    let mut e = exp;
    while e > 0 {
        if e % 2 == 1 {
            result = result * b % MOD;
        }
        b = b * b % MOD;
        e /= 2;
    }
    result
}

fn max_nice_divisors(prime_factors: i32) -> i32 {
    let n = prime_factors as i64;
    if n <= 3 {
        return prime_factors;
    }
    let answer = match n % 3 {
        0 => power(3, n / 3),
        1 => power(3, n / 3 - 1) * 4 % MOD,
        _ => power(3, n / 3) * 2 % MOD,
    };
    answer as i32
}

fn main() {
    let mut check: i64 = 0;
    for call in 0..2000000i64 {
        let n = 1 + (check * 7919 + call) % 1000000000;
        check = (check * 31 + max_nice_divisors(n as i32) as i64) % 1000000007;
    }
    println!("2000000 calls: checksum {}", check);
}
