// LeetCode #2272: Substring With Largest Variance -- the bench, the ★ arm.

fn largest_variance(s: &str) -> i64 {
    let bytes = s.as_bytes();
    let mut seen = [false; 26];
    for &c in bytes {
        seen[(c - b'a') as usize] = true;
    }
    let mut best = 0;
    for a in b'a'..=b'z' {
        for b in b'a'..=b'z' {
            if a == b || !seen[(a - b'a') as usize] || !seen[(b - b'a') as usize] {
                continue;
            }
            let mut diff: i64 = 0;
            let mut with_b = i64::MIN / 2;
            for &c in bytes {
                if c == a {
                    diff += 1;
                    with_b += 1;
                } else if c == b {
                    with_b = diff - 1;
                    diff = (diff - 1).max(0);
                }
                best = best.max(with_b);
            }
        }
    }
    best
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2272;
    let mut check = 0;
    for t in 0..40 {
        let k = [3, 5, 10, 26][t % 4];
        let mut s = String::new();
        for _ in 0..10000 {
            s.push((b'a' + (next_random(&mut seed) % k) as u8) as char);
        }
        check = (check * 31 + largest_variance(&s)) % 1000000007;
    }
    println!("40 strings of 10^4: checksum {check}");
}
