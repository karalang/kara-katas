// LeetCode #2047 -- the ★ arm as a benchmark; mirror of valid.kara: each
// token's chars collected into a Vec, as the Kāra arm does.

fn is_valid(token: &str) -> bool {
    let cs: Vec<char> = token.chars().collect();
    let n = cs.len();
    let mut hyphens = 0;
    for i in 0..n {
        let c = cs[i];
        if c.is_ascii_digit() {
            return false;
        }
        if c == '-' {
            hyphens += 1;
            if hyphens > 1 || i == 0 || i == n - 1 {
                return false;
            }
            if !cs[i - 1].is_ascii_lowercase() || !cs[i + 1].is_ascii_lowercase() {
                return false;
            }
        }
        if (c == '!' || c == '.' || c == ',') && i != n - 1 {
            return false;
        }
    }
    true
}

fn count_valid_words(sentence: &str) -> i64 {
    let mut count = 0;
    for token in sentence.split_whitespace() {
        if is_valid(token) {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let symbols: Vec<char> = "abcdefgh--!.,9".chars().collect();
    let mut seed: i64 = 2047;
    let mut sentences: Vec<String> = Vec::new();
    for _ in 0..2000 {
        let mut s = String::new();
        for _ in 0..1000 {
            let r = next_random(&mut seed) % 100;
            if r < 70 {
                s.push(symbols[(next_random(&mut seed) % 8) as usize]);
            } else if r < 85 {
                s.push(' ');
            } else {
                s.push(symbols[(next_random(&mut seed) % symbols.len() as i64) as usize]);
            }
        }
        sentences.push(s);
    }
    let (mut calls, mut words, mut check) = (0i64, 0i64, 0i64);
    for r in 0..100usize {
        for s in &sentences {
            let n = count_valid_words(&s[r % 7..]);
            calls += 1;
            words += n;
            check = (check * 31 + n) % 1_000_000_007;
        }
    }
    println!("{} calls: {} valid words, checksum {}", calls, words, check);
}
