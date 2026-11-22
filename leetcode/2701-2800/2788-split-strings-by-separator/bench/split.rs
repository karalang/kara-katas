// LeetCode #2788: Split Strings by Separator -- the bench in Rust: the ★
// arm over 20000 lists of 100 words of 20 characters from a, b, c and the
// six separators, each split by one of them, all drawn first, then each
// answered 10 times.

fn split_words_by_separator(words: &[String], separator: char) -> Vec<String> {
    words
        .iter()
        .flat_map(|w| w.split(separator))
        .filter(|piece| !piece.is_empty())
        .map(|piece| piece.to_string())
        .collect()
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 20000;
    let rounds = 10;
    let letters: Vec<char> = "abc.,|$#@".chars().collect();
    let separators: Vec<char> = ".,|$#@".chars().collect();
    let mut rng = Rng(2788);
    let mut cases = Vec::with_capacity(count);
    for _ in 0..count {
        let words: Vec<String> = (0..100)
            .map(|_| (0..20).map(|_| letters[(rng.next_random() % 9) as usize]).collect())
            .collect();
        let sep = separators[(rng.next_random() % 6) as usize];
        cases.push((words, sep));
    }
    let mut pieces = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (words, separator) in &cases {
            let got = split_words_by_separator(words, *separator);
            pieces += got.len() as i64;
            for p in &got {
                check = (check * 31 + p.len() as i64 + r) % 1000000007;
            }
        }
    }
    println!("{count} lists of 100 words, {rounds} rounds: {pieces} pieces, checksum {check}");
}
