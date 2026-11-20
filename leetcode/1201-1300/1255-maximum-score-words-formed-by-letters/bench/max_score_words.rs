// LeetCode #1255 bench, in Rust: the ★ arm (backtracking, every word in
// turn left out or, when the letters on hand cover it, taken) on 100
// random cases built once, each 14 words of 1 to 15 letters and 100
// letters to spend from the first 6 letters of the alphabet; each asked
// 3 times, every best score folded into a checksum.

fn best(i: usize, words: &[Vec<i64>], left: &mut Vec<i64>, score: &[i64]) -> i64 {
    if i == words.len() {
        return 0;
    }
    let mut top = best(i + 1, words, left, score);
    let need = words[i].clone();
    if (0..26).all(|c| need[c] <= left[c]) {
        for c in 0..26 {
            left[c] -= need[c];
        }
        let gain: i64 = (0..26).map(|c| need[c] * score[c]).sum();
        top = top.max(gain + best(i + 1, words, left, score));
        for c in 0..26 {
            left[c] += need[c];
        }
    }
    top
}

fn max_score_words(words: &[String], letters: &[char], score: &[i64]) -> i64 {
    let counts: Vec<Vec<i64>> = words
        .iter()
        .map(|w| {
            let mut n = vec![0i64; 26];
            for ch in w.chars() {
                n[ch as usize - 'a' as usize] += 1;
            }
            n
        })
        .collect();
    let mut left = vec![0i64; 26];
    for &ch in letters {
        left[ch as usize - 'a' as usize] += 1;
    }
    best(0, &counts, &mut left, score)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1255;
    let mut cases: Vec<(Vec<String>, Vec<char>, Vec<i64>)> = Vec::new();
    for _ in 0..100 {
        let mut words = Vec::new();
        for _ in 0..14 {
            let n = next_random(&mut seed) % 15 + 1;
            let mut w = String::new();
            for _ in 0..n {
                w.push((b'a' + (next_random(&mut seed) % 6) as u8) as char);
            }
            words.push(w);
        }
        let mut letters = Vec::new();
        for _ in 0..100 {
            letters.push((b'a' + (next_random(&mut seed) % 6) as u8) as char);
        }
        let score: Vec<i64> = (0..26).map(|_| next_random(&mut seed) % 11).collect();
        cases.push((words, letters, score));
    }
    let mut check: i64 = 0;
    for _ in 0..3 {
        for (words, letters, score) in &cases {
            check = (check * 131 + max_score_words(words, letters, score)) % 1000000007;
        }
    }
    println!("3 rounds of 100 cases of 14 words: checksum {check}");
}
