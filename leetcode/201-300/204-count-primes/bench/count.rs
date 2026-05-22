// LeetCode 204 — bench mirror in Rust. Idiomatic single-threaded
// implementation; matches kara's bench/count.kara sink (count + sum)
// for N = 10_000_000.

fn is_prime(n: i64) -> bool {
    if n < 2 {
        return false;
    }
    if n == 2 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }
    let mut i: i64 = 3;
    while i * i <= n {
        if n % i == 0 {
            return false;
        }
        i += 2;
    }
    true
}

fn main() {
    let n: i64 = 10_000_000;

    let mut primes: Vec<i64> = Vec::new();
    for k in 0..n {
        if is_prime(k) {
            primes.push(k);
        }
    }

    let sum: i64 = primes.iter().sum();
    println!("{}", primes.len());
    println!("{}", sum);
}
