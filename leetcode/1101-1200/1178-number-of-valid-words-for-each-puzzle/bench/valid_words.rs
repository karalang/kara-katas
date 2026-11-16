// LeetCode #1178: Number of Valid Words for Each Puzzle -- the ★ arm's
// bench in Rust: each word's letter set counted in a `HashMap`, each
// puzzle's subsets of its other six letters walked with
// `sub = (sub - 1) & rest`. The same words, the same puzzles and the same
// 20 calls.

use std::collections::HashMap;

fn find_num_of_valid_words(words: &[String], puzzles: &[String]) -> Vec<i64> {
    let mut count: HashMap<i64, i64> = HashMap::new();
    for w in words {
        let mut mask: i64 = 0;
        for c in w.bytes() {
            mask |= 1 << (c - b'a');
        }
        *count.entry(mask).or_insert(0) += 1;
    }
    let mut answer = Vec::new();
    for p in puzzles {
        let bytes = p.as_bytes();
        let first: i64 = 1 << (bytes[0] - b'a');
        let mut rest: i64 = 0;
        for &c in bytes.iter().skip(1) {
            rest |= 1 << (c - b'a');
        }
        let mut total = 0;
        let mut sub = rest;
        loop {
            total += count.get(&(sub | first)).copied().unwrap_or(0);
            if sub == 0 {
                break;
            }
            sub = (sub - 1) & rest;
        }
        answer.push(total);
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn distinct(seed: &mut i64, m: i64, k: i64) -> Vec<u8> {
    let mut letters: Vec<u8> = (0..m).map(|i| b'a' + i as u8).collect();
    for i in 0..k {
        let j = i + next_random(seed) % (m - i);
        letters.swap(i as usize, j as usize);
    }
    letters.truncate(k as usize);
    letters
}

fn main() {
    let mut seed = 1178;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..100000 {
        let k = 1 + next_random(&mut seed) % 7;
        let set = distinct(&mut seed, 14, k);
        let len = 4 + next_random(&mut seed) % 47;
        let w: Vec<u8> = (0..len).map(|_| set[(next_random(&mut seed) % set.len() as i64) as usize]).collect();
        words.push(String::from_utf8(w).unwrap());
    }
    let puzzles: Vec<String> = (0..10000).map(|_| String::from_utf8(distinct(&mut seed, 14, 7)).unwrap()).collect();
    let calls = 20;
    let mut check: i64 = 0;
    for _ in 0..calls {
        for &a in find_num_of_valid_words(&words, &puzzles).iter() {
            check = (check * 131 + a + 1) % 1000000007;
        }
    }
    println!("{} calls: checksum {}", calls, check);
}
