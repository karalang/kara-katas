// LeetCode #1181: Before and After Puzzle -- the ★ arm in Rust: the
// phrases' indices grouped by first word in a `HashMap`, each phrase's last
// word looking up the phrases that start with it, the puzzles gathered in a
// `BTreeSet`.
use std::collections::{BTreeSet, HashMap};

fn before_and_after_puzzles(phrases: &[String]) -> Vec<String> {
    let mut starting: HashMap<&str, Vec<usize>> = HashMap::new();
    for (i, p) in phrases.iter().enumerate() {
        let first = match p.split_once(' ') {
            Some((w, _)) => w,
            None => p.as_str(),
        };
        starting.entry(first).or_default().push(i);
    }
    let mut puzzles: BTreeSet<String> = BTreeSet::new();
    for (i, p) in phrases.iter().enumerate() {
        let last = match p.rsplit_once(' ') {
            Some((_, w)) => w,
            None => p.as_str(),
        };
        if let Some(js) = starting.get(last) {
            for &j in js {
                if j != i {
                    let rest = match phrases[j].split_once(' ') {
                        Some((_, r)) => format!(" {r}"),
                        None => String::new(),
                    };
                    puzzles.insert(format!("{p}{rest}"));
                }
            }
        }
    }
    puzzles.into_iter().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let vocabulary = ["a", "be", "cat", "dog", "eel", "fig", "go", "hat"];
    let mut seed: i64 = 1181;
    let mut problems: Vec<Vec<String>> = Vec::new();
    for _ in 0..100 {
        let m = 2 + next_random(&mut seed) % 7;
        let mut phrases = Vec::new();
        for _ in 0..100 {
            let n = 1 + next_random(&mut seed) % 25;
            let words: Vec<&str> = (0..n).map(|_| vocabulary[(next_random(&mut seed) % m) as usize]).collect();
            phrases.push(words.join(" "));
        }
        problems.push(phrases);
    }
    let rounds = 5;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for phrases in problems.iter() {
            let puzzles = before_and_after_puzzles(phrases);
            check = (check * 131 + puzzles.len() as i64) % 1000000007;
            for p in puzzles.iter() {
                check = (check * 31 + p.len() as i64) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds of 100 problems: checksum {check}");
}
