// LeetCode #2427: Number of Common Factors -- the bench, the ★ arm: the
// divisors of gcd(a, b), counted in pairs up to its square root.

fn gcd(a: i64, b: i64) -> i64 {
    let mut a = a;
    let mut b = b;
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn common_factors(a: i64, b: i64) -> i64 {
    let g = gcd(a, b);
    let mut count = 0;
    let mut d = 1;
    while d * d <= g {
        if g % d == 0 {
            count += if d * d == g { 1 } else { 2 };
        }
        d += 1;
    }
    count
}

fn main() {
    let mut check: i64 = 0;
    for p in 0..5i64 {
        for a in 1..1001i64 {
            for b in 1..1001i64 {
                let other = (b + p - 1) % 1000 + 1;
                check = (check * 31 + common_factors(a, other) + p) % 1000000007;
            }
        }
    }
    println!("5 passes over 10^6 pairs: checksum {}", check);
}
