// Benchmark workload for LeetCode #263 — Ugly Number (Rust mirror).
// Mirrors ugly_sweep.kara algorithm-for-algorithm.

fn gcd(a: i64, b: i64) -> i64 {
    let mut x = a;
    let mut y = b;
    while y != 0 {
        let t = x % y;
        x = y;
        y = t;
    }
    x
}

fn is_ugly(n: i64) -> bool {
    if n <= 0 {
        return false;
    }
    let mut m = n;
    let mut g = gcd(m, 30);
    while g > 1 {
        m /= g;
        g = gcd(m, 30);
    }
    m == 1
}

fn main() {
    let n: i64 = 10000000;
    let limit: i64 = i64::MAX;

    let mut ring: Vec<i64> = Vec::with_capacity(64);
    let mut rs: i64 = 7717;
    for _ in 0..64 {
        let mut v: i64 = 1;
        let mut steps: i64 = 0;
        while steps < 40 {
            rs = (rs * 1103515245 + 12345) & 2147483647;
            let pick = (rs / 65536) % 3;
            let f: i64 = if pick == 1 { 3 } else if pick == 2 { 5 } else { 2 };
            if v <= limit / f {
                v *= f;
            } else {
                steps = 40;
            }
            steps += 1;
        }
        ring.push(v);
    }

    let mut state: i64 = 263263;
    let mut uglies: i64 = 0;
    let mut digest: i64 = 0;
    for i in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let hi = state;
        state = (state * 1103515245 + 12345) & 2147483647;
        let mut probe = hi * 2147483648 + state;
        if i % 512 == 0 {
            probe = ring[((i / 512) % 64) as usize];
        }
        let mut bit: i64 = 0;
        if is_ugly(probe) {
            uglies += 1;
            bit = 1;
        }
        digest = (digest * 131 + bit * 7 + probe % 1000003) % 1000000007;
    }

    println!("{}", uglies);
    println!("{}", digest);
}
