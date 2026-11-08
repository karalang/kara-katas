// LeetCode #1065: Index Pairs of a String -- the benchmark, the same
// every-start-against-every-word search as index_pairs.kara.

fn index_pairs(text: &str, words: &[String]) -> Vec<(i64, i64)> {
    let mut pairs: Vec<(i64, i64)> = Vec::new();
    for i in 0..text.len() {
        for w in words.iter() {
            if text[i..].starts_with(w.as_str()) {
                pairs.push((i as i64, (i + w.len() - 1) as i64));
            }
        }
    }
    pairs.sort();
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(n: i64, k: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    for _ in 0..n {
        s.push((b'a' + (next_random(seed) % k) as u8) as char);
    }
    s
}

// Up to `count` distinct words of 1 to `longest` letters over `k`: each
// drawn at random or, every other one, cut from the text.
fn random_words(text: &str, count: i64, longest: i64, k: i64, seed: &mut i64) -> Vec<String> {
    let mut words: Vec<String> = Vec::new();
    for w in 0..count {
        let n = next_random(seed) % longest + 1;
        let word = if w % 2 == 1 && n as usize <= text.len() {
            let at = (next_random(seed) % (text.len() as i64 - n + 1)) as usize;
            text[at..at + n as usize].to_string()
        } else {
            random_word(n, k, seed)
        };
        if !words.contains(&word) {
            words.push(word);
        }
    }
    words
}

fn main() {
    // 40 texts of 20000 letters over 2 to 4, each with up to 100 words of 1
    // to 12 letters, built once, then each answered
    let mut seed = 1065;
    let mut texts: Vec<String> = Vec::new();
    let mut lists: Vec<Vec<String>> = Vec::new();
    for t in 0..40 {
        let k = 2 + t % 3;
        let text = random_word(20000, k, &mut seed);
        lists.push(random_words(&text, 100, 12, k, &mut seed));
        texts.push(text);
    }
    let mut calls = 0;
    let mut count = 0;
    let mut check: i64 = 0;
    for t in 0..40 {
        let pairs = index_pairs(&texts[t], &lists[t]);
        count += pairs.len();
        for &(i, j) in pairs.iter() {
            check = (check * 31 + i * 101 + j + 1) % 1000000007;
        }
        calls += 1;
    }
    println!("{} calls: {} pairs, checksum {}", calls, count, check);
}
