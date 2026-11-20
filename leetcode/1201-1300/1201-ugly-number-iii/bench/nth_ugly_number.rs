// LeetCode #1201 bench: the ★ arm in Rust, over the same 50000 queries and
// 10 rounds as the Kāra bench.

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn lcm(a: i64, b: i64) -> i64 {
    a / gcd(a, b) * b
}

fn nth_ugly_number(n: i64, a: i64, b: i64, c: i64) -> i64 {
    let ab = lcm(a, b);
    let bc = lcm(b, c);
    let ac = lcm(a, c);
    let abc = lcm(ab, c);
    let count = |x: i64| x / a + x / b + x / c - x / ab - x / bc - x / ac + x / abc;
    let mut low = 1;
    let mut high = n * a.min(b).min(c);
    while low < high {
        let mid = low + (high - low) / 2;
        if count(mid) >= n {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    low
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let tops = [1000000i64, 1000, 30];
    let mut seed = 1201i64;
    let mut queries: Vec<(i64, i64, i64, i64)> = Vec::new();
    for k in 0..50000 {
        let top = tops[k % 3];
        let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % top + 1;
        let b = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % top + 1;
        let c = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % top + 1;
        let most = (2000000000 / a.min(b).min(c)).min(1000000000);
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % most + 1;
        queries.push((n, a, b, c));
    }
    let mut check = 0i64;
    for _ in 0..10 {
        for &(n, a, b, c) in queries.iter() {
            check = (check * 131 + nth_ugly_number(n, a, b, c)) % 1000000007;
        }
    }
    println!("10 rounds of 50000 queries: checksum {}", check);
}
