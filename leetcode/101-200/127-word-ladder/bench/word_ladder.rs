// Benchmark harness for LeetCode #127 — Word Ladder.
// Mirrors word_ladder.kara algorithm-for-algorithm.
//
// This lane uses Rust's DEFAULT HashMap hasher (SipHash-1-3), which is
// DoS-resistant and slower than the FxHash Kara's Map[String, _] uses. The
// equal-hash sibling is word_ladder_fasthash.rs — see ../README.md § Benchmarks.

use std::collections::HashMap;

fn nth_letter(n: i64) -> char {
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let target = n % 26;
    let mut i = 0i64;
    for ch in alphabet.chars() {
        if i == target {
            return ch;
        }
        i += 1;
    }
    'a'
}

fn replace_char(word: &str, pos: i64, new_ch: char) -> String {
    let mut out = String::new();
    let mut i = 0i64;
    for ch in word.chars() {
        if i == pos {
            out.push(new_ch);
        } else {
            out.push(ch);
        }
        i += 1;
    }
    out
}

fn neighbors(word: &str, word_set: &HashMap<String, i64>) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    let bytes = word.as_bytes();
    let n = bytes.len() as i64;
    let mut i = 0i64;
    while i < n {
        let orig = bytes[i as usize];
        let mut c = 0i64;
        while c < 26 {
            if (c + 97) != (orig as i64) {
                let cand = replace_char(word, i, nth_letter(c));
                if word_set.contains_key(&cand) {
                    out.push(cand);
                }
            }
            c += 1;
        }
        i += 1;
    }
    out
}

fn ladder_length(begin: String, end: String, words: &Vec<String>) -> i64 {
    let mut word_set: HashMap<String, i64> = HashMap::new();
    let mut wi = 0usize;
    while wi < words.len() {
        word_set.insert(words[wi].clone(), 1);
        wi += 1;
    }
    if !word_set.contains_key(&end) {
        return 0;
    }

    let mut visited: HashMap<String, i64> = HashMap::new();
    visited.insert(begin.clone(), 1);
    let mut cur: Vec<String> = Vec::new();
    cur.push(begin);
    let mut steps = 1i64;

    while !cur.is_empty() {
        let mut nxt: Vec<String> = Vec::new();
        let mut i = 0usize;
        while i < cur.len() {
            let word = cur[i].clone();
            if word == end {
                return steps;
            }
            let nbs = neighbors(&word, &word_set);
            let mut j = 0usize;
            while j < nbs.len() {
                let nb = nbs[j].clone();
                if !visited.contains_key(&nb) {
                    visited.insert(nb.clone(), 1);
                    nxt.push(nb);
                }
                j += 1;
            }
            i += 1;
        }
        cur = nxt;
        steps += 1;
    }
    0
}

fn main() {
    let alpha: i64 = 5;
    let wlen: i64 = 5;
    let iters: i64 = 17;

    let mut words: Vec<String> = Vec::new();
    let total: i64 = 3125;
    let mut idx = 0i64;
    while idx < total {
        let mut w = String::new();
        let mut d = 0i64;
        let mut rem = idx;
        let mut div = 625i64;
        while d < wlen {
            let digit = rem / div;
            w.push(nth_letter(digit));
            rem -= digit * div;
            div /= alpha;
            d += 1;
        }
        words.push(w);
        idx += 1;
    }

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let b = ((it * 257) % total) as usize;
        let e = ((it * 613 + 1234) % total) as usize;
        let r = ladder_length(words[b].clone(), words[e].clone(), &words);
        sink = (sink * 31 + r) % 1000000007;
        it += 1;
    }
    println!("{}", sink);
}
