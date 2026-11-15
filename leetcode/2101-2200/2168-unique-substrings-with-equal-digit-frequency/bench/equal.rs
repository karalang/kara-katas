// LeetCode #2168: Unique Substrings With Equal Digit Frequency -- the
// benchmark's Rust mirror of equal.kara.

use std::collections::HashSet;

fn equal_digit_frequency(s: &str) -> i64 {
    let digits = s.as_bytes();
    let n = digits.len();
    let mut found: HashSet<String> = HashSet::new();
    for i in 0..n {
        let mut counts = [0i64; 10];
        let mut kinds = 0i64;
        let mut most = 0i64;
        for j in i..n {
            let d = (digits[j] - b'0') as usize;
            if counts[d] == 0 {
                kinds += 1;
            }
            counts[d] += 1;
            most = most.max(counts[d]);
            if most * kinds == (j - i + 1) as i64 {
                found.insert(s[i..=j].to_string());
            }
        }
    }
    found.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2168i64;
    let mut digits: Vec<u8> = (0..1000).map(|_| b'0' + (next_random(&mut seed) % 3) as u8).collect();
    let mut check = 0i64;
    for _ in 0..200 {
        let at = (next_random(&mut seed) % 1000) as usize;
        digits[at] = b'0' + (next_random(&mut seed) % 3) as u8;
        let s = String::from_utf8(digits.clone()).unwrap();
        check = (check * 31 + equal_digit_frequency(&s)) % 1000000007;
    }
    println!("200 solves: checksum {}", check);
}
