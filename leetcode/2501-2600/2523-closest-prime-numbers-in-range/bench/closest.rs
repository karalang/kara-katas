// LeetCode #2523: Closest Prime Numbers in Range -- Rust mirror of the
// benchmark (closest.kara): the same queries, each answered by a fresh
// sieve, and the same checksum.

fn closest_primes(left: i64, right: i64) -> (i64, i64) {
    let mut composite = vec![false; right as usize + 1];
    let mut p = 2;
    while p * p <= right {
        if !composite[p as usize] {
            let mut m = p * p;
            while m <= right {
                composite[m as usize] = true;
                m += p;
            }
        }
        p += 1;
    }
    let mut best = (-1, -1);
    let mut last = -1;
    for x in left.max(2)..right + 1 {
        if !composite[x as usize] {
            if last != -1 && (best.0 == -1 || x - last < best.1 - best.0) {
                best = (last, x);
            }
            last = x;
        }
    }
    best
}

fn main() {
    let queries = 150;
    let mut check: i64 = 0;
    for q in 0..queries {
        let right = check % 500000 + 500001;
        let (a, b) = closest_primes(right - 10000, right);
        check = (check * 31 + a + q) % 1000000007;
        check = (check * 31 + b) % 1000000007;
    }
    println!("{queries} queries to 10^6: checksum {check}");
}
