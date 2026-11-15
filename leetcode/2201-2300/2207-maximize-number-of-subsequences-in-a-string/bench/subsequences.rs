// benchmark's Rust mirror of subsequences.kara (LeetCode #2207, the ★
// arm): one pass counting the first letter so far, each second letter
// adding that count, then the more common letter added. The text is read
// by `chars()`, as Kāra's.

fn maximum_subsequence_count(text: &str, pattern: &str) -> i64 {
    let p: Vec<char> = pattern.chars().collect();
    let (first, second) = (p[0], p[1]);
    let (mut firsts, mut seconds, mut pairs) = (0i64, 0i64, 0i64);
    for ch in text.chars() {
        if ch == second {
            pairs += firsts;
            seconds += 1;
        }
        if ch == first {
            firsts += 1;
        }
    }
    pairs + firsts.max(seconds)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(n: usize, letters: i64, seed: &mut i64) -> String {
    let mut w = String::new();
    for _ in 0..n {
        w.push((97 + next_random(seed) % letters) as u8 as char);
    }
    w
}

fn main() {
    let mut seed = 2207;
    let sizes = [2i64, 3, 26];
    let texts: Vec<String> = (0..12).map(|t| random_word(100000, sizes[t % 3], &mut seed)).collect();
    // each pass asks every text about its own pattern
    let mut check: i64 = 0;
    for p in 0..50i64 {
        for t in 0..12usize {
            let letters = sizes[t % 3];
            let mut pattern = String::new();
            pattern.push((97 + p % letters) as u8 as char);
            pattern.push((97 + (p * 7 + t as i64) % letters) as u8 as char);
            check = (check * 31 + maximum_subsequence_count(&texts[t], &pattern)) % 1000000007;
        }
    }
    println!("50 passes over 12 texts: checksum {}", check);
}
