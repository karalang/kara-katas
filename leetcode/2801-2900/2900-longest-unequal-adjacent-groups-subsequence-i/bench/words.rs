// LeetCode #2900: Longest Unequal Adjacent Groups Subsequence I -- the
// bench's Rust mirror (words.kara): each chosen word cloned, as the ★
// arm does.

fn get_longest_subsequence(words: &[String], groups: &[i64]) -> Vec<String> {
    let mut chosen: Vec<String> = Vec::new();
    for i in 0..words.len() {
        if i == 0 || groups[i] != groups[i - 1] {
            chosen.push(words[i].clone());
        }
    }
    chosen
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (count, rounds, n) = (10000, 20i64, 100usize);
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 2900i64;
    let mut cases: Vec<(Vec<String>, Vec<i64>)> = Vec::new();
    for _ in 0..count {
        let mut words = Vec::new();
        for i in 0..n {
            let mut word = String::new();
            word.push(letters[(next_random(&mut seed) % 26) as usize]);
            word.push(letters[i % 26]);
            word.push(letters[i / 26]);
            words.push(word);
        }
        let mut groups: Vec<i64> = Vec::new();
        let mut group = next_random(&mut seed) % 2;
        while groups.len() < n {
            let run = next_random(&mut seed) % 5 + 1;
            for _ in 0..run {
                if groups.len() < n {
                    groups.push(group);
                }
            }
            group = 1 - group;
        }
        cases.push((words, groups));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (words, groups) in &cases {
            let chosen = get_longest_subsequence(words, groups);
            total += chosen.len() as i64;
            check = (check * 31 + chosen.len() as i64 + r) % 1000000007;
            for word in &chosen {
                check = (check * 31 + word.len() as i64) % 1000000007;
            }
            check = (check * 31 + chosen[chosen.len() - 1].as_bytes()[0] as i64) % 1000000007;
        }
    }
    println!("{count} cases of {n}, {rounds} rounds: {total} words chosen, checksum {check}");
}
