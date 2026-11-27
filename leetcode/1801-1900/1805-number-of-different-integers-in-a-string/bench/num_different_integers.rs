// LeetCode #1805: Number of Different Integers in a String -- the bench in
// Rust: the ★ arm over 64 random words of 1000 characters built once,
// 20000 calls.
use std::collections::HashSet;

fn num_different_integers(word: &str) -> i32 {
    let mut seen: HashSet<String> = HashSet::new();
    let mut run = String::new();
    let mut in_run = false;
    for c in word.chars() {
        if c.is_ascii_digit() {
            in_run = true;
            if !(run.is_empty() && c == '0') {
                run.push(c);
            }
        } else if in_run {
            seen.insert(run.clone());
            run = String::new();
            in_run = false;
        }
    }
    if in_run {
        seen.insert(run);
    }
    seen.len() as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1805;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..64 {
        let mut word = String::new();
        for _ in 0..1000 {
            if next_random(&mut seed) % 2 == 0 {
                word.push(char::from_digit((next_random(&mut seed) % 4) as u32, 10).unwrap());
            } else {
                word.push(char::from_u32(97 + (next_random(&mut seed) % 26) as u32).unwrap());
            }
        }
        words.push(word);
    }
    let mut check: i64 = 0;
    for call in 0..20000i64 {
        let word = &words[((check + call) % 64) as usize];
        check = (check * 31 + num_different_integers(word) as i64) % 1000000007;
    }
    println!("20000 calls over 64 words of 1000 characters: checksum {}", check);
}
