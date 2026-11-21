// LeetCode #2478: Number of Beautiful Partitions -- bench, Rust mirror of
// beauty.kara.

const MOD: i64 = 1000000007;

fn is_prime_digit(c: i64) -> bool {
    c == 2 || c == 3 || c == 5 || c == 7
}

fn beautiful_partitions(digits: &[i64], k: i64, min_length: i64) -> i64 {
    let n = digits.len();
    if !is_prime_digit(digits[0]) || is_prime_digit(digits[n - 1]) {
        return 0;
    }
    let cut: Vec<bool> = (0..=n).map(|i| i == n || (i > 0 && !is_prime_digit(digits[i - 1]) && is_prime_digit(digits[i]))).collect();
    let m = min_length as usize;
    let mut ways = vec![0i64; n + 1];
    ways[0] = 1;
    for _ in 0..k {
        let mut next = vec![0i64; n + 1];
        let mut running = 0;
        for i in m..=n {
            let start = i - m;
            if start == 0 || (cut[start] && start < n) {
                running = (running + ways[start]) % MOD;
            }
            if cut[i] && i > 0 {
                next[i] = running;
            }
        }
        ways = next;
    }
    ways[n]
}

fn main() {
    let mut seed: i64 = 2478;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let strings: Vec<Vec<i64>> = (0..20)
        .map(|_| {
            let mut d = vec![2i64];
            for _ in 0..998 {
                d.push(1 + next_random() % 9);
            }
            d.push(1);
            d
        })
        .collect();
    let mut check: i64 = 0;
    for p in 0..90 {
        for s in &strings {
            let k = 1 + check % 100;
            let m = 1 + check % 5;
            check = (check * 31 + beautiful_partitions(s, k, m) + p) % MOD;
        }
    }
    println!("90 passes over 20 strings of 1000: checksum {}", check);
}
