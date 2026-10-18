// LeetCode #691: Stickers to Spell Word -- bench program, Rust mirror of the ★ arm.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(len: i64, alphabet: i64, seed: &mut i64) -> String {
    let mut w = String::new();
    for _ in 0..len {
        w.push((b'a' + (next_random(seed) % alphabet) as u8) as char);
    }
    w
}

fn min_stickers(stickers: &[String], target: &str) -> i64 {
    let t = target.as_bytes();
    let m = t.len();
    let full = (1usize << m) - 1;
    let mut counts: Vec<Vec<i64>> = Vec::new();
    for s in stickers {
        let mut c = vec![0i64; 26];
        for b in s.bytes() {
            c[(b - b'a') as usize] += 1;
        }
        counts.push(c);
    }
    let mut dp = vec![-1i64; full + 1];
    dp[0] = 0;
    let mut left = vec![0i64; 26];
    for mask in 0..full + 1 {
        if dp[mask] < 0 {
            continue;
        }
        for c in &counts {
            for k in 0..26 {
                left[k] = c[k];
            }
            let mut next = mask;
            for i in 0..m {
                let k = (t[i] - b'a') as usize;
                if next & (1 << i) == 0 && left[k] > 0 {
                    left[k] -= 1;
                    next |= 1 << i;
                }
            }
            if next != mask && (dp[next] < 0 || dp[mask] + 1 < dp[next]) {
                dp[next] = dp[mask] + 1;
            }
        }
    }
    dp[full]
}

fn main() {
    let mut seed = 691i64;
    let problems = 160;
    let mut total = 0i64;
    let mut checksum = 0i64;
    for _ in 0..problems {
        let mut stickers: Vec<String> = Vec::new();
        for _ in 0..50 {
            stickers.push(random_word(10, 12, &mut seed));
        }
        let target = random_word(15, 12, &mut seed);
        let r = min_stickers(&stickers, &target);
        total += r;
        checksum = (checksum * 31 + r + 2) % 1000000007;
    }
    println!("{} problems of 50 stickers and a 15-letter target: {} stickers in all, checksum {}", problems, total, checksum);
}
