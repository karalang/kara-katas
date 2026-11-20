// LeetCode #1258 bench, in Rust: the ★ arm (union-find over the pairs'
// words, the groups sorted, every sentence built by a recursive search, the
// sentences sorted) on 100 random cases built once, each 10 pairs of 8
// words and a text of 10 words, 4 of them from the pairs, asked 80 rounds;
// the sentences counted and the middle one of each answer folded into a
// checksum.

use std::collections::HashMap;

fn find(parent: &mut HashMap<String, String>, word: &str) -> String {
    let up = parent[word].clone();
    if up == word {
        return up;
    }
    let root = find(parent, &up);
    parent.insert(word.to_string(), root.clone());
    root
}

fn build(choices: &[Vec<String>], at: usize, current: &mut Vec<String>, out: &mut Vec<String>) {
    if at == choices.len() {
        out.push(current.join(" "));
        return;
    }
    for word in &choices[at] {
        current.push(word.clone());
        build(choices, at + 1, current, out);
        current.pop();
    }
}

fn generate_sentences(synonyms: &[Vec<String>], text: &str) -> Vec<String> {
    let mut parent: HashMap<String, String> = HashMap::new();
    for pair in synonyms {
        for word in pair {
            if !parent.contains_key(word) {
                parent.insert(word.clone(), word.clone());
            }
        }
    }
    for pair in synonyms {
        let a = find(&mut parent, &pair[0]);
        let b = find(&mut parent, &pair[1]);
        if a != b {
            parent.insert(a, b);
        }
    }
    let words: Vec<String> = parent.keys().cloned().collect();
    let mut groups: HashMap<String, Vec<String>> = HashMap::new();
    for word in &words {
        let root = find(&mut parent, word);
        groups.entry(root).or_insert_with(Vec::new).push(word.clone());
    }
    let mut choices: Vec<Vec<String>> = Vec::new();
    for word in text.split(' ') {
        if parent.contains_key(word) {
            let root = find(&mut parent, word);
            let mut group = groups[&root].clone();
            group.sort();
            choices.push(group);
        } else {
            choices.push(vec![word.to_string()]);
        }
    }
    let mut out = Vec::new();
    let mut current = Vec::new();
    build(&choices, 0, &mut current, &mut out);
    out.sort();
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(first: u8, seed: &mut i64) -> String {
    let mut word = String::new();
    let len = next_random(seed) % 3 + 1;
    for _ in 0..len {
        word.push((first + (next_random(seed) % 6) as u8) as char);
    }
    word
}

fn random_words(count: usize, first: u8, seed: &mut i64) -> Vec<String> {
    let mut words: Vec<String> = Vec::new();
    while words.len() < count {
        let word = random_word(first, seed);
        if !words.contains(&word) {
            words.push(word);
        }
    }
    words
}

fn bench_case(seed: &mut i64) -> (Vec<Vec<String>>, String) {
    let pool = random_words(8, b'a', seed);
    let plain = random_words(12, b'p', seed);
    let mut synonyms = Vec::new();
    for _ in 0..10 {
        let i = next_random(seed) % 8;
        let j = (i + 1 + next_random(seed) % 7) % 8;
        synonyms.push(vec![pool[i as usize].clone(), pool[j as usize].clone()]);
    }
    let mut words: Vec<String> = Vec::new();
    for _ in 0..10 {
        words.push(plain[(next_random(seed) % 12) as usize].clone());
    }
    for k in 0..4 {
        words[k * 3] = pool[(next_random(seed) % 8) as usize].clone();
    }
    (synonyms, words.join(" "))
}

fn main() {
    let mut seed = 1258;
    let cases: Vec<(Vec<Vec<String>>, String)> = (0..100).map(|_| bench_case(&mut seed)).collect();
    let mut total = 0;
    let mut check: i64 = 0;
    for _ in 0..80 {
        for (synonyms, text) in &cases {
            let sentences = generate_sentences(synonyms, text);
            total += sentences.len();
            for b in sentences[sentences.len() / 2].bytes() {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
    }
    println!("80 rounds of 100 cases: {total} sentences, checksum {check}");
}
