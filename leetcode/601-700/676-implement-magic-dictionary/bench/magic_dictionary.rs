// Benchmark for #676: every word of the same length compared, as the
// Kara ★ arm.

struct MagicDictionary {
    words: Vec<String>,
}

impl MagicDictionary {
    fn new() -> MagicDictionary {
        MagicDictionary { words: Vec::new() }
    }

    fn build_dict(&mut self, dictionary: &[String]) {
        self.words = dictionary.to_vec();
    }

    fn search(&self, search_word: &str) -> bool {
        let b = search_word.as_bytes();
        for w in self.words.iter() {
            let a = w.as_bytes();
            if a.len() == b.len() {
                let mut diff = 0;
                for i in 0..a.len() {
                    if a[i] != b[i] {
                        diff += 1;
                    }
                }
                if diff == 1 {
                    return true;
                }
            }
        }
        false
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, length: i64) -> String {
    let mut s = String::new();
    for _ in 0..length {
        s.push((97 + next_random(seed) % 2) as u8 as char);
    }
    s
}

fn main() {
    let rounds: i64 = 1000;
    let mut seed: i64 = 676;
    let mut sum: i64 = 0;
    let mut found = 0;
    for _ in 0..rounds {
        let mut dictionary: Vec<String> = Vec::new();
        for _ in 0..100 {
            dictionary.push(random_word(&mut seed, 50));
        }
        let mut d = MagicDictionary::new();
        d.build_dict(&dictionary);
        for k in 0..100 {
            let word = if k % 2 == 0 {
                let w = &dictionary[(next_random(&mut seed) % 100) as usize];
                let at = (next_random(&mut seed) % 50) as usize;
                let c = if &w[at..at + 1] == "a" { "b" } else { "a" };
                format!("{}{}{}", &w[..at], c, &w[at + 1..])
            } else {
                random_word(&mut seed, 50)
            };
            if d.search(&word) {
                found += 1;
                sum = (sum * 3 + 1) % 1000000007;
            } else {
                sum = sum * 3 % 1000000007;
            }
        }
    }
    println!(
        "{} dictionaries of 100 words, {} searches, {} found: checksum {}",
        rounds,
        rounds * 100,
        found,
        sum
    );
}
