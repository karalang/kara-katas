// LeetCode #2507: Smallest Value After Replacing With Sum of Prime
// Factors -- Rust mirror of the benchmark (smallest.kara): the same
// passes, order and checksum.

fn smallest_value(mut n: i64) -> i64 {
    loop {
        let mut rest = n;
        let mut total = 0;
        let mut p = 2;
        while p * p <= rest {
            while rest % p == 0 {
                rest /= p;
                total += p;
            }
            p += 1;
        }
        if rest > 1 {
            total += rest;
        }
        if total == n {
            return n;
        }
        n = total;
    }
}

fn main() {
    let passes = 14;
    let mut check: i64 = 0;
    for p in 0..passes {
        let start = check % 99999;
        for k in 0..99999 {
            let n = (start + k) % 99999 + 2;
            check = (check * 31 + smallest_value(n) + p) % 1000000007;
        }
    }
    println!("{} passes over 2 to 10^5: checksum {}", passes, check);
}
