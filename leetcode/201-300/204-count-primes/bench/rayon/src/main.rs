// Rayon-parallel mirror of the LeetCode 204 bench. The natural
// rayon-idiomatic shape: `.into_par_iter().filter(...).collect()`
// — same shape Kara's `#[par_unordered] for ... acc.push(...)`
// lowers to: workers each accumulate a private Vec<i64>, merged at
// the end into one final Vec<i64>.
//
// Same sink (count, sum) as the other three bench mirrors:
// (664579, 3203324994356) at N = 10_000_000.

use rayon::prelude::*;

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

    let primes: Vec<i64> = (0..n).into_par_iter().filter(|&k| is_prime(k)).collect();

    let sum: i64 = primes.iter().sum();
    println!("{}", primes.len());
    println!("{}", sum);
}
