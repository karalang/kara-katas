// LeetCode #1297 bench: the ★ arm (one window of minSize letters slid along
// the string, each with few enough distinct letters counted in a `HashMap` by
// its text) over 10 strings of 10^5 letters over the first 2 to 6 letters,
// built once; then 20 passes, each setting one letter of every string and its
// limits from the checksum so far, answering it, and folding the answer into
// the checksum.
use std::collections::HashMap;

fn max_freq(s: &str, max_letters: i64, min_size: i64, _max_size: i64) -> i64 {
    let bytes = s.as_bytes();
    let n = bytes.len();
    let min_size = min_size as usize;
    let mut letters = vec![0i64; 26];
    let mut distinct = 0;
    let mut seen: HashMap<&str, i64> = HashMap::new();
    let mut best = 0;
    for i in 0..n {
        let add = (bytes[i] - 97) as usize;
        if letters[add] == 0 {
            distinct += 1;
        }
        letters[add] += 1;
        if i >= min_size {
            let gone = (bytes[i - min_size] - 97) as usize;
            letters[gone] -= 1;
            if letters[gone] == 0 {
                distinct -= 1;
            }
        }
        if i + 1 >= min_size && distinct <= max_letters {
            let window = &s[i + 1 - min_size..i + 1];
            let times = seen.get(window).cloned().unwrap_or(0) + 1;
            seen.insert(window, times);
            if times > best {
                best = times;
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1297;
    let mut texts: Vec<Vec<u8>> = Vec::new();
    for t in 0..10i64 {
        let alphabet = 2 + t % 5;
        let mut text: Vec<u8> = Vec::new();
        for _ in 0..100000 {
            text.push((97 + next_random(&mut seed) % alphabet) as u8);
        }
        texts.push(text);
    }
    let mut check: i64 = 0;
    for p in 0..20 {
        for t in 0..texts.len() {
            texts[t][(check % 100000) as usize] = (97 + check % (2 + t as i64 % 5)) as u8;
            let s = String::from_utf8(texts[t].clone()).unwrap();
            let min_size = 1 + check % 26;
            let max_letters = 1 + (check / 26) % 26;
            check = (check * 31 + max_freq(&s, max_letters, min_size, min_size) + p) % 1000000007;
        }
    }
    println!("20 passes over 10 strings of 10^5: checksum {}", check);
}
