// LeetCode #647: Palindromic Substrings -- Rust mirror of the Kāra
// bench.
//
// The ★ arm over the same texts and rounds: from each of the 2n - 1
// centers, the window widened while its two ends match, over the
// string's bytes.

fn count_substrings(s: &str) -> i64 {
    let bytes = s.as_bytes();
    let n = bytes.len() as i64;
    let mut count = 0;
    for center in 0..2 * n - 1 {
        let mut lo = center / 2;
        let mut hi = lo + center % 2;
        while lo >= 0 && hi < n && bytes[lo as usize] == bytes[hi as usize] {
            count += 1;
            lo -= 1;
            hi += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let inputs = 20;
    let rounds = 300;
    let mut seed: i64 = 647;
    let mut texts: Vec<String> = Vec::new();
    for _ in 0..inputs {
        let letters = 1 + next_random(&mut seed) % 3;
        let mut s = String::new();
        for _ in 0..2000 {
            s.push((97 + next_random(&mut seed) % letters) as u8 as char);
        }
        texts.push(s);
    }
    let mut sum: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let c = count_substrings(&texts[(r * 7) % inputs]);
        sum += c;
        checksum = (checksum * 31 + c) % 1000000007;
    }
    println!("{} inputs, {} rounds: total {}, checksum {}", inputs, rounds, sum, checksum);
}
