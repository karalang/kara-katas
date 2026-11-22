// LeetCode #2818: Apply Operations to Maximize Score -- the bench's Rust
// mirror of the ★ arm: a sieve of prime scores, one monotonic stack, the
// indices sorted by value, largest first, each power by squaring.

const MOD: i64 = 1_000_000_007;

fn prime_scores(limit: usize) -> Vec<i64> {
    let mut score = vec![0i64; limit + 1];
    for p in 2..=limit {
        if score[p] == 0 {
            let mut q = p;
            while q <= limit {
                score[q] += 1;
                q += p;
            }
        }
    }
    score
}

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

fn maximum_score(nums: &[i64], k: i64) -> i64 {
    let n = nums.len();
    let score = prime_scores(*nums.iter().max().unwrap() as usize);
    let s: Vec<i64> = nums.iter().map(|&v| score[v as usize]).collect();
    let mut left = vec![-1i64; n];
    let mut right = vec![n as i64; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..n {
        while let Some(&t) = stack.last() {
            if s[t] < s[i] {
                right[t] = i as i64;
                stack.pop();
            } else {
                break;
            }
        }
        if let Some(&t) = stack.last() {
            left[i] = t as i64;
        }
        stack.push(i);
    }
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by_key(|&i| -nums[i]);
    let mut rest = k;
    let mut total = 1;
    for &i in &order {
        if rest == 0 {
            break;
        }
        let take = ((i as i64 - left[i]) * (right[i] - i as i64)).min(rest);
        total = total * power(nums[i], take) % MOD;
        rest -= take;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 20;
    let rounds = 3;
    let n = 100000;
    let mut seed = 2818;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 100000 + 1).collect();
        let k = wide(&mut seed) % 1000000000 + 1;
        cases.push((nums, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in &cases {
            let a = maximum_score(nums, *k);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{} arrays of {}, {} rounds: scores sum to {}, checksum {}", count, n, rounds, total, check);
}
