// LeetCode #2716: Minimize String Length -- the bench (minimize.kara in
// Rust): the distinct letters of each string counted by a
// `HashSet<char>`.
use std::collections::HashSet;

fn minimized_string_length(s: &str) -> i64 {
    let seen: HashSet<char> = s.chars().collect();
    seen.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds = 10;
    let mut seed: i64 = 2716;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let letters = next_random(&mut seed) % 26 + 1;
        let mut s = String::new();
        for _ in 0..100 {
            s.push((b'a' + (next_random(&mut seed) % letters) as u8) as char);
        }
        strings.push(s);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in strings.iter() {
            let length = minimized_string_length(s);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    println!("{} strings of 100 letters, {} rounds: lengths sum to {}, checksum {}", count, rounds, sum, check);
}
