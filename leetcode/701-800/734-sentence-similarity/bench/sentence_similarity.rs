// LeetCode #734: Sentence Similarity -- a set of pairs.
// Benchmark mirror of the Kara star arm: put every pair in a hash set
// both ways round, then check the words place by place.
use std::collections::HashSet;

fn are_sentences_similar(sentence1: &[String], sentence2: &[String], pairs: &[(String, String)]) -> bool {
    if sentence1.len() != sentence2.len() {
        return false;
    }
    let mut similar: HashSet<(String, String)> = HashSet::new();
    for p in pairs.iter() {
        similar.insert((p.0.clone(), p.1.clone()));
        similar.insert((p.1.clone(), p.0.clone()));
    }
    for i in 0..sentence1.len() {
        let a = sentence1[i].clone();
        let b = sentence2[i].clone();
        if a != b && !similar.contains(&(a, b)) {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 734;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..1000 {
        let a = next_random(&mut seed) % 5000;
        let b = next_random(&mut seed) % 5000;
        pairs.push((format!("w{}", a), format!("w{}", b)));
    }
    let mut s1: Vec<String> = Vec::new();
    let mut s2: Vec<String> = Vec::new();
    for _ in 0..1000 {
        let p = (next_random(&mut seed) % 1000) as usize;
        if next_random(&mut seed) % 2 == 0 {
            s1.push(pairs[p].0.clone());
            s2.push(pairs[p].1.clone());
        } else {
            s1.push(pairs[p].1.clone());
            s2.push(pairs[p].0.clone());
        }
    }
    let mut similar = 0;
    for _ in 0..1000 {
        let j = (next_random(&mut seed) % 1000) as usize;
        let x = next_random(&mut seed) % 5000;
        let saved = s2[j].clone();
        s2[j] = format!("w{}", x);
        if are_sentences_similar(&s1, &s2, &pairs) {
            similar += 1;
        }
        s2[j] = saved;
        if are_sentences_similar(&s1, &s2, &pairs) {
            similar += 1;
        }
    }
    println!("1000 rounds of 2 checks of 1000 words with 1000 pairs: {} similar", similar);
}
