// LeetCode #2781: Length of the Longest Valid Substring -- the bench in
// Rust: the ★ arm over 10 words of 10^5 letters from a to e, each
// against 10^5 forbidden words of 8 to 10 letters, all drawn first, then
// each answered 5 times, every answer building its own `HashSet`.
use std::collections::HashSet;

fn longest_valid_substring(word: &str, forbidden: &[String]) -> i64 {
    let banned: HashSet<String> = forbidden.iter().cloned().collect();
    let n = word.len() as i64;
    let mut start = 0i64;
    let mut best = 0i64;
    for j in 0..n {
        let mut i = j;
        while i >= start && i + 10 > j {
            if banned.contains(&word[i as usize..(j + 1) as usize]) {
                start = i + 1;
                break;
            }
            i -= 1;
        }
        best = best.max(j + 1 - start);
    }
    best
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
    fn word(&mut self, n: i64, letters: i64) -> String {
        (0..n).map(|_| (b'a' + (self.next_random() % letters) as u8) as char).collect()
    }
    fn words(&mut self, count: i64, shortest: i64, longest: i64, letters: i64) -> Vec<String> {
        (0..count)
            .map(|_| {
                let n = shortest + self.next_random() % (longest - shortest + 1);
                self.word(n, letters)
            })
            .collect()
    }
}

fn main() {
    let count = 10;
    let rounds = 5;
    let mut rng = Rng(2781);
    let mut cases = Vec::new();
    for _ in 0..count {
        let word = rng.word(100000, 5);
        let forbidden = rng.words(100000, 8, 10, 5);
        cases.push((word, forbidden));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (word, forbidden) in &cases {
            let a = longest_valid_substring(word, forbidden);
            total += a;
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    println!("{count} words of 10^5, {rounds} rounds: lengths sum to {total}, checksum {check}");
}
