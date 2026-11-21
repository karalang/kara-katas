// LeetCode #2506: Count Pairs Of Similar Strings -- Rust mirror of the
// benchmark (similar.kara): the same lists, passes and checksum; the
// masks counted in a std `HashMap`.
use std::collections::HashMap;

fn similar_pairs(words: &[String]) -> i64 {
    let mut seen: HashMap<i64, i64> = HashMap::new();
    let mut pairs = 0;
    for word in words {
        let mut mask = 0i64;
        for ch in word.chars() {
            mask |= 1 << (ch as i64 - 'a' as i64);
        }
        pairs += seen.get(&mask).copied().unwrap_or(0);
        *seen.entry(mask).or_insert(0) += 1;
    }
    pairs
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn random_word(rng: &mut Rng) -> String {
    let length = rng.next() % 100 + 1;
    let letters = rng.next() % 4 + 3;
    (0..length).map(|_| (b'a' + (rng.next() % letters) as u8) as char).collect()
}

fn main() {
    let passes = 24;
    let mut rng = Rng(2506);
    let mut lists: Vec<Vec<String>> = (0..1000).map(|_| (0..100).map(|_| random_word(&mut rng)).collect()).collect();
    let mut check: i64 = 0;
    for p in 0..passes {
        for l in 0..1000 {
            let at = (check % 100) as usize;
            let was = lists[l][at].clone();
            lists[l][at] = lists[l][((check / 100 + p) % 100) as usize].clone();
            check = (check * 31 + similar_pairs(&lists[l]) + p) % 1000000007;
            lists[l][at] = was;
        }
    }
    println!("{} passes over 1000 lists of 100 words: checksum {}", passes, check);
}
