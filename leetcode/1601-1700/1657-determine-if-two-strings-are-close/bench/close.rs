// LeetCode #1657: Determine if Two Strings Are Close -- the bench's Rust
// mirror: the ★ arm on 400 random pairs of words of 100000 letters, each
// pair from the first 1 to 26 of the alphabet, half of the second words
// made close by construction, all drawn first.

fn close_strings(word1: &str, word2: &str) -> bool {
    let mut count1 = [0i64; 26];
    let mut count2 = [0i64; 26];
    for b in word1.bytes() {
        count1[(b - b'a') as usize] += 1;
    }
    for b in word2.bytes() {
        count2[(b - b'a') as usize] += 1;
    }
    for i in 0..26 {
        if (count1[i] == 0) != (count2[i] == 0) {
            return false;
        }
    }
    count1.sort();
    count2.sort();
    count1 == count2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(n: i64, letters: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    for _ in 0..n {
        s.push((b'a' + (next_random(seed) % letters) as u8) as char);
    }
    s
}

fn main() {
    let mut seed: i64 = 1657;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..400 {
        let alphabet = next_random(&mut seed) % 26 + 1;
        let word1 = random_word(100000, alphabet, &mut seed);
        let word2 = if next_random(&mut seed) % 2 == 0 {
            random_word(100000, alphabet, &mut seed)
        } else {
            let a = (b'a' + (next_random(&mut seed) % alphabet) as u8) as char;
            let b = (b'a' + (next_random(&mut seed) % alphabet) as u8) as char;
            word1.chars().rev().map(|c| if c == a { b } else if c == b { a } else { c }).collect()
        };
        pairs.push((word1, word2));
    }
    let mut check: i64 = 0;
    let mut close = 0;
    for (word1, word2) in &pairs {
        let answer = close_strings(word1, word2);
        if answer {
            close += 1;
        }
        check = (check * 31 + if answer { 2 } else { 1 }) % 1000000007;
    }
    println!("400 pairs of 100000 letters: {} close, checksum {}", close, check);
}
