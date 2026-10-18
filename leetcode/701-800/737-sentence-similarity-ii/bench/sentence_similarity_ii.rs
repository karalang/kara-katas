// LeetCode #737: Sentence Similarity II -- union-find.
// Benchmark mirror of the Kara star arm: number every word in a pair,
// join the two words of each pair in a union-find with union by size
// and path compression, and compare the roots of the two words at each
// place.
use std::collections::HashMap;

fn find(parent: &mut Vec<i64>, x: i64) -> i64 {
    let mut root = x;
    while parent[root as usize] != root {
        root = parent[root as usize];
    }
    let mut y = x;
    while parent[y as usize] != root {
        let next = parent[y as usize];
        parent[y as usize] = root;
        y = next;
    }
    root
}

fn number(ids: &mut HashMap<String, i64>, parent: &mut Vec<i64>, size: &mut Vec<i64>, w: &str) -> i64 {
    if let Some(i) = ids.get(w) {
        return *i;
    }
    let i = parent.len() as i64;
    ids.insert(w.to_string(), i);
    parent.push(i);
    size.push(1);
    i
}

fn are_sentences_similar_two(sentence1: &[String], sentence2: &[String], pairs: &[(String, String)]) -> bool {
    if sentence1.len() != sentence2.len() {
        return false;
    }
    let mut ids: HashMap<String, i64> = HashMap::new();
    let mut parent: Vec<i64> = Vec::new();
    let mut size: Vec<i64> = Vec::new();
    for p in pairs.iter() {
        let a = number(&mut ids, &mut parent, &mut size, &p.0);
        let b = number(&mut ids, &mut parent, &mut size, &p.1);
        let ra = find(&mut parent, a);
        let rb = find(&mut parent, b);
        if ra != rb {
            if size[ra as usize] < size[rb as usize] {
                parent[ra as usize] = rb;
                size[rb as usize] += size[ra as usize];
            } else {
                parent[rb as usize] = ra;
                size[ra as usize] += size[rb as usize];
            }
        }
    }
    for i in 0..sentence1.len() {
        if sentence1[i] == sentence2[i] {
            continue;
        }
        let a = match ids.get(&sentence1[i]) {
            Some(k) => *k,
            None => return false,
        };
        let b = match ids.get(&sentence2[i]) {
            Some(k) => *k,
            None => return false,
        };
        if find(&mut parent, a) != find(&mut parent, b) {
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
    let mut seed: i64 = 737;
    let mut pairs: Vec<(String, String)> = Vec::new();
    let mut near: Vec<Vec<i64>> = vec![Vec::new(); 3000];
    for _ in 0..2000 {
        let a = next_random(&mut seed) % 3000;
        let b = next_random(&mut seed) % 3000;
        pairs.push((format!("w{}", a), format!("w{}", b)));
        near[a as usize].push(b);
        near[b as usize].push(a);
    }
    let mut s1: Vec<String> = Vec::new();
    let mut s2: Vec<String> = Vec::new();
    for _ in 0..1000 {
        let start = next_random(&mut seed) % 3000;
        let mut at = start;
        for _ in 0..next_random(&mut seed) % 6 {
            if !near[at as usize].is_empty() {
                at = near[at as usize][(next_random(&mut seed) % near[at as usize].len() as i64) as usize];
            }
        }
        s1.push(format!("w{}", start));
        s2.push(format!("w{}", at));
    }
    let mut similar = 0;
    for _ in 0..1000 {
        let j = (next_random(&mut seed) % 1000) as usize;
        let x = next_random(&mut seed) % 3000;
        let saved = s2[j].clone();
        s2[j] = format!("w{}", x);
        if are_sentences_similar_two(&s1, &s2, &pairs) {
            similar += 1;
        }
        s2[j] = saved;
        if are_sentences_similar_two(&s1, &s2, &pairs) {
            similar += 1;
        }
    }
    println!("1000 rounds of 2 checks of 1000 words with 2000 pairs: {} similar", similar);
}
