// LeetCode #2521: Distinct Prime Factors of Product of Array -- Rust mirror
// of the benchmark (primes.kara): the same lists, passes, order and
// checksum.
use std::collections::HashSet;

fn distinct_prime_factors(nums: &[i64]) -> i64 {
    let mut primes: HashSet<i64> = HashSet::new();
    for &x in nums {
        let mut rest = x;
        let mut d = 2;
        while d * d <= rest {
            if rest % d == 0 {
                primes.insert(d);
                while rest % d == 0 {
                    rest /= d;
                }
            }
            d += 1;
        }
        if rest > 1 {
            primes.insert(rest);
        }
    }
    primes.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2521;
    let lists: Vec<Vec<i64>> = (0..200)
        .map(|_| (0..1000).map(|_| next_random(&mut seed) % 999 + 2).collect())
        .collect();
    let passes = 110;
    let mut check: i64 = 0;
    for p in 0..passes {
        for nums in &lists {
            let n = (check % 1000 + 1) as usize;
            let part: Vec<i64> = nums.iter().take(n).cloned().collect();
            check = (check * 31 + distinct_prime_factors(&part) + p) % 1000000007;
        }
    }
    println!("{passes} passes over 200 lists of 1000 numbers: checksum {check}");
}
