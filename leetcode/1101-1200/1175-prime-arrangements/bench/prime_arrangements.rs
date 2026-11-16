// LeetCode #1175: Prime Arrangements -- the ★ arm's bench in Rust: a sieve
// of Eratosthenes over a `Vec<bool>` counts the primes up to n, and the
// answer is p! * (n - p)! modulo 10^9 + 7. The same million calls.
const MOD: i64 = 1_000_000_007;

fn factorial(k: i64) -> i64 {
    let mut f = 1;
    for i in 2..=k {
        f = f * i % MOD;
    }
    f
}

fn num_prime_arrangements(n: i64) -> i64 {
    let mut composite = vec![false; n as usize + 1];
    let mut primes = 0;
    for i in 2..=n {
        if !composite[i as usize] {
            primes += 1;
            let mut j = i * i;
            while j <= n {
                composite[j as usize] = true;
                j += i;
            }
        }
    }
    factorial(primes) * factorial(n - primes) % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let calls = 1000000;
    let mut seed = 1175i64;
    let mut check = 0i64;
    for _ in 0..calls {
        let n = 1 + next_random(&mut seed) % 100;
        check = (check * 131 + num_prime_arrangements(n)) % 1000000007;
    }
    println!("{calls} calls: checksum {check}");
}
