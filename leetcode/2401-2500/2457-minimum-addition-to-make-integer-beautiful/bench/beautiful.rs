// LeetCode #2457: Minimum Addition to Make Integer Beautiful -- bench,
// Rust mirror of beautiful.kara: while the digit sum is too large, n + x
// is rounded up to the next multiple of a power of ten one place higher.

fn digit_sum(x: i64) -> i64 {
    let mut rest = x;
    let mut sum = 0;
    while rest > 0 {
        sum += rest % 10;
        rest /= 10;
    }
    sum
}

fn make_integer_beautiful(n: i64, target: i64) -> i64 {
    let mut m = n;
    let mut p = 1;
    while digit_sum(m) > target {
        p *= 10;
        m = (m + p - 1) / p * p;
    }
    m - n
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2457;
    let mut pairs: Vec<(i64, i64)> = Vec::new();
    for _ in 0..100000 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let n = 1 + (a * 1073741824 + b * 32768 + next_random(&mut seed)) % 1000000000000;
        pairs.push((n, next_random(&mut seed) % 150));
    }
    let mut check: i64 = 0;
    for p in 0..36i64 {
        for &(n, t) in pairs.iter() {
            check = (check * 31 + make_integer_beautiful(n, 1 + (t + p) % 150) + p) % 1000000007;
        }
    }
    println!("36 passes over 10^5 pairs: checksum {}", check);
}
