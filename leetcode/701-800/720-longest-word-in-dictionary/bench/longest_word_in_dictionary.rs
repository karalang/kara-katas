// LeetCode #720: Longest Word in Dictionary -- a trie, walked through
// word ends only. Benchmark mirror of the Kara trie arm: every word put
// in a trie with one array of 26 children per node, then a depth-first
// walk that steps only onto nodes where a word ends.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn deepest(next: &[Vec<i64>], word_at: &[i64], node: usize, depth: i64) -> (i64, i64) {
    let mut best = (depth, word_at[node]);
    for c in 0..26 {
        let child = next[node][c] as usize;
        if child != 0 && word_at[child] >= 0 {
            let got = deepest(next, word_at, child, depth + 1);
            if got.0 > best.0 {
                best = got;
            }
        }
    }
    best
}

fn longest_word(words: &[String]) -> String {
    let mut next: Vec<Vec<i64>> = Vec::new();
    let mut word_at: Vec<i64> = Vec::new();
    next.push(vec![0; 26]);
    word_at.push(-1);
    for (i, w) in words.iter().enumerate() {
        let mut node = 0usize;
        for b in w.bytes() {
            let c = (b - b'a') as usize;
            if next[node][c] == 0 {
                next[node][c] = next.len() as i64;
                next.push(vec![0; 26]);
                word_at.push(-1);
            }
            node = next[node][c] as usize;
        }
        word_at[node] = i as i64;
    }
    let found = deepest(&next, &word_at, 0, 0);
    if found.1 < 0 { String::new() } else { words[found.1 as usize].clone() }
}

fn main() {
    let mut seed: i64 = 720;
    let mut dicts: Vec<Vec<String>> = Vec::new();
    for _ in 0..40 {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..1000 {
            if !words.is_empty() && next_random(&mut seed) % 4 != 0 {
                let k = (next_random(&mut seed) % words.len() as i64) as usize;
                let mut w = words[k].clone();
                if w.len() < 30 {
                    w.push((97 + next_random(&mut seed) % 4) as u8 as char);
                }
                words.push(w);
            } else {
                let mut w = String::new();
                for _ in 0..1 + next_random(&mut seed) % 3 {
                    w.push((97 + next_random(&mut seed) % 4) as u8 as char);
                }
                words.push(w);
            }
        }
        dicts.push(words);
    }
    let mut sum = 0;
    for round in 0..300i64 {
        for d in 0..40i64 {
            let i = ((round * 7919 + d * 104729) % 1000) as usize;
            let w = &mut dicts[d as usize][i];
            if w.len() < 30 {
                w.push((97 + round % 4) as u8 as char);
            }
            sum += longest_word(&dicts[d as usize]).len();
        }
    }
    println!("300 rounds of 40 dictionaries of 1000 words: sum {}", sum);
}
