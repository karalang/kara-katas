// LeetCode #2513: Minimize the Maximum of Two Arrays -- Rust mirror of the
// benchmark (minimize.kara): the same cases, passes and checksum.

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn minimize_set(divisor1: i64, divisor2: i64, unique_cnt1: i64, unique_cnt2: i64) -> i64 {
    let lcm = divisor1 / gcd(divisor1, divisor2) * divisor2;
    let enough = |x: i64| x - x / divisor1 >= unique_cnt1 && x - x / divisor2 >= unique_cnt2 && x - x / lcm >= unique_cnt1 + unique_cnt2;
    let mut lo = 1;
    let mut hi = 2 * (unique_cnt1 + unique_cnt2);
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if enough(mid) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn below(top: i64, seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    (hi * 32768 + next_random(seed)) % top
}

fn main() {
    let mut seed = 2513;
    let mut cases = Vec::new();
    for _ in 0..100000 {
        let d1 = below(99999, &mut seed) + 2;
        let d2 = below(99999, &mut seed) + 2;
        let c1 = below(999998999, &mut seed) + 1;
        let c2 = below(999999000 - c1, &mut seed) + 1;
        cases.push((d1, d2, c1, c2));
    }
    let passes = 10;
    let mut check: i64 = 0;
    for p in 0..passes {
        for &(d1, d2, c1, c2) in &cases {
            check = (check * 31 + minimize_set(d1, d2, c1 + check % 1000, c2) + p) % 1000000007;
        }
    }
    println!("{} passes over 10^5 cases: checksum {}", passes, check);
}
