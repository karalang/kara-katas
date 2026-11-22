// LeetCode #2746: Decremental String Concatenation -- the bench
// (decremental.kara in Rust): the shortest string for each pair of first
// and last letters in a 26 by 26 array, rolled word by word.

const NONE: i64 = 1000000000;

fn minimize_concatenated_length(words: &[String]) -> i64 {
    let first_of = |w: &str| (w.as_bytes()[0] - b'a') as usize;
    let last_of = |w: &str| (w.as_bytes()[w.len() - 1] - b'a') as usize;
    let mut best = [[NONE; 26]; 26];
    best[first_of(&words[0])][last_of(&words[0])] = words[0].len() as i64;
    for w in words.iter().skip(1) {
        let (a, b) = (first_of(w), last_of(w));
        let n = w.len() as i64;
        let mut next = [[NONE; 26]; 26];
        for f in 0..26 {
            for l in 0..26 {
                let length = best[f][l];
                if length == NONE {
                    continue;
                }
                let after = length + n - if l == a { 1 } else { 0 };
                next[f][b] = next[f][b].min(after);
                let before = length + n - if b == f { 1 } else { 0 };
                next[a][l] = next[a][l].min(before);
            }
        }
        best = next;
    }
    best.iter().flatten().copied().min().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let rounds = 5;
    let mut seed = 2746;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..count {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..1000 {
            let len = next_random(&mut seed) % 10 + 1;
            let mut w = String::new();
            for _ in 0..len {
                w.push((b'a' + (next_random(&mut seed) % 26) as u8) as char);
            }
            words.push(w);
        }
        lists.push(words);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for words in lists.iter() {
            let length = minimize_concatenated_length(words);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    println!("{count} lists of 1000 words, {rounds} rounds: lengths sum to {sum}, checksum {check}");
}
