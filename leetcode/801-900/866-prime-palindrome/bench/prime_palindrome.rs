// LeetCode #866: Prime Palindrome -- Rust mirror of the bench program
// (the ★ arm, the odd-length palindromes in order).

fn odd_palindrome(root: i64) -> i64 {
    let mut y = root;
    let mut rest = root / 10;
    while rest > 0 {
        y = y * 10 + rest % 10;
        rest /= 10;
    }
    y
}

fn is_prime(x: i64) -> bool {
    if x < 2 {
        return false;
    }
    if x % 2 == 0 {
        return x == 2;
    }
    let mut d = 3;
    while d * d <= x {
        if x % d == 0 {
            return false;
        }
        d += 2;
    }
    true
}

fn prime_palindrome(n: i64) -> i64 {
    if (8..=11).contains(&n) {
        return 11;
    }
    let mut root = 1;
    loop {
        let y = odd_palindrome(root);
        if y >= n && is_prime(y) {
            return y;
        }
        root += 1;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_n(seed: &mut i64) -> i64 {
    let digits = 1 + next_random(seed) % 8;
    let mut low = 1;
    for _ in 1..digits {
        low *= 10;
    }
    let hi = next_random(seed);
    let lo = next_random(seed);
    low + (hi * 32768 + lo) % (9 * low)
}

fn main() {
    let queries = 60000;
    let mut seed = 866;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..queries {
        let n = random_n(&mut seed);
        let p = prime_palindrome(n);
        total += p;
        check = (check * 31 + p) % 1000000007;
    }
    println!("{} random n of 1 to 8 digits: answers sum to {}, checksum {}", queries, total, check);
}
