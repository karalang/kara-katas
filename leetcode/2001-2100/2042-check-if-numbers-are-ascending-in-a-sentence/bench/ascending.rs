// LeetCode #2042: Check if Numbers Are Ascending in a Sentence -- the ★ arm
// in Rust, the same algorithm and workload as ascending.kara: the sentence
// split at its spaces, each token that parses compared with the last.

fn are_numbers_ascending(s: String) -> bool {
    let mut last = 0i64;
    for token in s.split(' ') {
        if let Ok(n) = token.parse::<i64>() {
            if n <= last {
                return false;
            }
            last = n;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn sentence(seed: &mut i64) -> String {
    let words = 1 + next_random(seed) % 30;
    let climb = next_random(seed) % 20 + 1;
    let drift = next_random(seed) % 4;
    let mut last = next_random(seed) % 10 + 1;
    let mut tokens: Vec<String> = Vec::new();
    let mut numbers = 0;
    let mut length = 0;
    for t in 0..words + 2 {
        let token = if t >= words || next_random(seed) % 3 == 0 {
            last = (last + next_random(seed) % (climb + drift + 1) - drift).max(1).min(99);
            numbers += 1;
            format!("{}", last)
        } else {
            let mut word = String::new();
            for _ in 0..next_random(seed) % 6 + 1 {
                word.push(['a', 'b', 'c', 'x', 'y', 'z'][(next_random(seed) % 6) as usize]);
            }
            word
        };
        if length + token.len() + 1 > 200 && numbers >= 2 {
            break;
        }
        length += token.len() + 1;
        tokens.push(token);
    }
    tokens.join(" ")
}

fn main() {
    let mut seed = 2042i64;
    let sentences: Vec<String> = (0..1000).map(|_| sentence(&mut seed)).collect();
    let mut calls = 0i64;
    let mut ascending = 0i64;
    let mut check = 0i64;
    for round in 0..1000i64 {
        for i in 0..sentences.len() {
            let answer = are_numbers_ascending(sentences[i].clone());
            calls += 1;
            if answer {
                ascending += 1;
                check = (check * 31 + round + i as i64) % 1000000007;
            }
        }
    }
    println!("{} calls: {} ascending, checksum {}", calls, ascending, check);
}
