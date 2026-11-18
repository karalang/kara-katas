// LeetCode #2306: Naming a Company -- the bench, the ★ arm in Rust. Group
// the suffixes by first letter, and for each pair of letters multiply the
// suffixes each group does not share with the other, twice.

use std::collections::HashSet;

fn distinct_names(ideas: &[String]) -> i64 {
    let mut groups: Vec<HashSet<String>> = (0..26).map(|_| HashSet::new()).collect();
    for idea in ideas {
        let first = (idea.as_bytes()[0] - b'a') as usize;
        groups[first].insert(idea[1..].to_string());
    }
    let mut names = 0i64;
    for a in 0..26 {
        for b in a + 1..26 {
            let mut shared = 0i64;
            for suffix in &groups[a] {
                if groups[b].contains(suffix) {
                    shared += 1;
                }
            }
            names += 2 * (groups[a].len() as i64 - shared) * (groups[b].len() as i64 - shared);
        }
    }
    names
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 2306;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..10 {
        let mut seen: HashSet<String> = HashSet::new();
        let mut ideas: Vec<String> = Vec::new();
        while ideas.len() < 50000 {
            let mut idea = String::new();
            idea.push(letters[(next_random(&mut seed) % 26) as usize]);
            for _ in 0..next_random(&mut seed) % 7 {
                idea.push(letters[(next_random(&mut seed) % 6) as usize]);
            }
            if !seen.contains(&idea) {
                seen.insert(idea.clone());
                ideas.push(idea);
            }
        }
        lists.push(ideas);
    }
    let mut check: i64 = 0;
    for _ in 0..4 {
        for ideas in &lists {
            check = (check * 31 + distinct_names(ideas)) % 1000000007;
        }
    }
    println!("4 passes over 10 lists of 5 * 10^4 ideas: checksum {}", check);
}
