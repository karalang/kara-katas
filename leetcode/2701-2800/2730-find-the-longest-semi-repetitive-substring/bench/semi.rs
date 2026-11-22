// LeetCode #2730: Find the Longest Semi-Repetitive Substring -- the bench
// (semi.kara in Rust): a sliding window over the bytes holding at most
// one adjacent equal pair.

fn longest_semi_repetitive_substring(s: &str) -> i64 {
    let b = s.as_bytes();
    let mut left = 0;
    let mut pairs = 0;
    let mut best: i64 = 1;
    for right in 1..b.len() {
        if b[right] == b[right - 1] {
            pairs += 1;
        }
        while pairs > 1 {
            if b[left] == b[left + 1] {
                pairs -= 1;
            }
            left += 1;
        }
        best = best.max((right - left + 1) as i64);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 200000;
    let rounds = 20;
    let mut seed: i64 = 2730;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let digits = next_random(&mut seed) % 9 + 2;
        let mut s = String::new();
        for _ in 0..50 {
            s.push((b'0' + (next_random(&mut seed) % digits) as u8) as char);
        }
        strings.push(s);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in strings.iter() {
            let length = longest_semi_repetitive_substring(s);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    println!("{} strings of 50 digits, {} rounds: lengths sum to {}, checksum {}", count, rounds, sum, check);
}
