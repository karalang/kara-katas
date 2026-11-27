// LeetCode #1807: Evaluate the Bracket Pairs of a String -- the bench in
// Rust: the ★ arm over 40 strings of 10^5 characters and 40 knowledge lists
// of 2 * 10^4 pairs built once, 200 calls.
use std::collections::{HashMap, HashSet};

fn evaluate(s: &str, knowledge: &[Vec<String>]) -> String {
    let mut values: HashMap<String, String> = HashMap::new();
    for pair in knowledge.iter() {
        values.insert(pair[0].clone(), pair[1].clone());
    }
    let mut out = String::new();
    let mut key = String::new();
    let mut inside = false;
    for c in s.chars() {
        if c == '(' {
            inside = true;
        } else if c == ')' {
            match values.get(&key) {
                Some(v) => out.push_str(v),
                None => out.push('?'),
            }
            key = String::new();
            inside = false;
        } else if inside {
            key.push(c);
        } else {
            out.push(c);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(seed: &mut i64, most: i64, letters: i64) -> String {
    let n = 1 + next_random(seed) % most;
    let mut w = String::new();
    for _ in 0..n {
        w.push(char::from_u32(97 + (next_random(seed) % letters) as u32).unwrap());
    }
    w
}

fn main() {
    let mut seed = 1807;
    let mut texts: Vec<String> = Vec::new();
    let mut lists: Vec<Vec<Vec<String>>> = Vec::new();
    for _ in 0..40 {
        let mut s = String::new();
        while s.len() < 99980 {
            if next_random(&mut seed) % 2 == 0 {
                s.push_str(&word(&mut seed, 3, 26));
            } else {
                s.push('(');
                s.push_str(&word(&mut seed, 8, 4));
                s.push(')');
            }
        }
        texts.push(s);
        let mut knowledge: Vec<Vec<String>> = Vec::new();
        let mut seen: HashSet<String> = HashSet::new();
        while knowledge.len() < 20000 {
            let k = word(&mut seed, 8, 4);
            if seen.insert(k.clone()) {
                knowledge.push(vec![k, word(&mut seed, 10, 26)]);
            }
        }
        lists.push(knowledge);
    }
    let mut check: i64 = 0;
    for call in 0..200i64 {
        let s = &texts[((check + call) % 40) as usize];
        let knowledge = &lists[((check * 7 + call) % 40) as usize];
        let out = evaluate(s, knowledge);
        check = (check * 31 + out.len() as i64 + out.as_bytes()[out.len() / 2] as i64) % 1000000007;
    }
    println!("200 calls over 40 strings of 10^5 characters: checksum {}", check);
}
