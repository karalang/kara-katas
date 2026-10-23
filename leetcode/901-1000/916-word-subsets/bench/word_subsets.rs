// LeetCode #916: Word Subsets -- bench: Rust mirror of every word of
// words2 folded into one need in word_subsets.kara.

fn counts(word: &str) -> [i64; 26] {
    let mut count = [0i64; 26];
    for b in word.bytes() {
        count[(b - b'a') as usize] += 1;
    }
    count
}

fn word_subsets(words1: &[String], words2: &[String]) -> Vec<String> {
    let mut need = [0i64; 26];
    for b in words2 {
        let count = counts(b);
        for c in 0..26 {
            need[c] = need[c].max(count[c]);
        }
    }
    let mut universal = Vec::new();
    for a in words1 {
        let count = counts(a);
        let mut all = true;
        for c in 0..26 {
            if count[c] < need[c] {
                all = false;
            }
        }
        if all {
            universal.push(a.clone());
        }
    }
    universal
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, len: i64, letters: i64) -> String {
    let mut w = String::new();
    for _ in 0..len {
        w.push((97 + next_random(seed) % letters) as u8 as char);
    }
    w
}

fn main() {
    let rounds = 200;
    let n = 50000;
    let mut seed = 916;
    let mut words1: Vec<String> = Vec::new();
    for _ in 0..n {
        words1.push(random_word(&mut seed, 10, 8));
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut words2: Vec<String> = Vec::new();
        for _ in 0..3 {
            let len = 1 + next_random(&mut seed) % 3;
            words2.push(random_word(&mut seed, len, 8));
        }
        let universal = word_subsets(&words1, &words2);
        total += universal.len();
        for w in &universal {
            for b in w.bytes() {
                check = (check * 31 + b as i64) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over {n} words: {total} universal, checksum {check}");
}
