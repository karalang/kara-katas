// LeetCode #1134: Armstrong Number -- the bench in Rust, the same algorithm
// and workload as is_armstrong.kara: every number from 1 to 15000000 asked
// in turn.

fn is_armstrong(n: i64) -> bool {
    let mut k = 0;
    let mut m = n;
    while m > 0 {
        k += 1;
        m /= 10;
    }
    let mut total = 0;
    m = n;
    while m > 0 {
        let d = m % 10;
        let mut p = 1;
        for _ in 0..k {
            p *= d;
        }
        total += p;
        m /= 10;
    }
    total == n
}

fn main() {
    let mut count: i64 = 0;
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for n in 1..15000001i64 {
        if is_armstrong(n) {
            count += 1;
            sum += n;
            check = (check * 31 + n) % 1000000007;
        }
    }
    println!("1 to 15000000: {} Armstrong numbers, summing to {}, checksum {}", count, sum, check);
}
