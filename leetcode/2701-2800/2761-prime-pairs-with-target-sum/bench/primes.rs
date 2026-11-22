// LeetCode #2761: Prime Pairs With Target Sum -- the bench (primes.kara in
// Rust): a sieve of Eratosthenes up to n, then each x up to n / 2 with x
// and n - x both prime.

fn find_prime_pairs(n: i64) -> Vec<Vec<i64>> {
    let mut prime: Vec<bool> = vec![true; (n + 1) as usize];
    prime[0] = false;
    if n >= 1 {
        prime[1] = false;
    }
    let mut p = 2;
    while p * p <= n {
        if prime[p as usize] {
            let mut m = p * p;
            while m <= n {
                prime[m as usize] = false;
                m += p;
            }
        }
        p += 1;
    }
    let mut pairs: Vec<Vec<i64>> = Vec::new();
    for x in 2..=n / 2 {
        if prime[x as usize] && prime[(n - x) as usize] {
            pairs.push(vec![x, n - x]);
        }
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds = 3;
    let mut seed = 2761;
    let targets: Vec<i64> = (0..count)
        .map(|_| {
            let hi = next_random(&mut seed);
            (hi * 32768 + next_random(&mut seed)) % 100000 + 900001
        })
        .collect();
    let mut pairs_seen: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &n in targets.iter() {
            let pairs = find_prime_pairs(n);
            pairs_seen += pairs.len() as i64;
            check = (check * 31 + pairs.len() as i64 + r) % 1000000007;
            for pair in pairs.iter() {
                check = (check * 31 + pair[0]) % 1000000007;
            }
        }
    }
    println!("{count} n near 10^6, {rounds} rounds: {pairs_seen} pairs, checksum {check}");
}
