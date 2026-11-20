// LeetCode #1735: Count Ways to Make Array With Product -- the bench
// (ways.kara): the product over k's primes of C(n + e - 1, e), read off
// factorials and their inverses.

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

fn ways_to_fill_array(queries: &[Vec<i32>]) -> Vec<i32> {
    let top = queries.iter().map(|q| q[0] as i64).max().unwrap() + 14;
    let mut fact: Vec<i64> = vec![1; top as usize + 1];
    for i in 1..top + 1 {
        fact[i as usize] = fact[i as usize - 1] * i % MOD;
    }
    let mut inverse: Vec<i64> = vec![1; top as usize + 1];
    inverse[top as usize] = power(fact[top as usize], MOD - 2);
    for i in (1..top + 1).rev() {
        inverse[i as usize - 1] = inverse[i as usize] * i % MOD;
    }
    let choose = |m: i64, r: i64| {
        fact[m as usize] * inverse[r as usize] % MOD * inverse[(m - r) as usize] % MOD
    };
    let mut answers: Vec<i32> = Vec::new();
    for q in queries.iter() {
        let n = q[0] as i64;
        let mut k = q[1] as i64;
        let mut ways = 1;
        let mut p = 2;
        while p * p <= k {
            let mut e = 0;
            while k % p == 0 {
                k /= p;
                e += 1;
            }
            ways = ways * choose(n + e - 1, e) % MOD;
            p += 1;
        }
        if k > 1 {
            ways = ways * n % MOD;
        }
        answers.push(ways as i32);
    }
    answers
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let rounds: i64 = 60;
    let q: usize = 10000;
    let mut seed: i64 = 1735;
    let mut problems: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..count {
        let mut queries: Vec<Vec<i32>> = Vec::new();
        for _ in 0..q {
            let n = (next_random(&mut seed) % 10000 + 1) as i32;
            let k = (next_random(&mut seed) % 10000 + 1) as i32;
            queries.push(vec![n, k]);
        }
        problems.push(queries);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for queries in problems.iter() {
            let answers = ways_to_fill_array(queries);
            sum += answers[0] as i64;
            check = (check * 31
                + answers[0] as i64
                + answers[q / 2] as i64
                + answers[q - 1] as i64
                + r)
                % 1000000007;
        }
    }
    println!(
        "{} lists of {} queries, {} rounds: first answers sum to {}, checksum {}",
        count, q, rounds, sum, check
    );
}
