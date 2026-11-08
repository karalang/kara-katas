// LeetCode #2014: Longest Subsequence Repeated k Times -- the ★ arm's
// benchmark, a mirror of longest.kara.
use std::collections::VecDeque;

fn repeats(s: &[u8], t: &[u8], k: i64) -> bool {
    let (mut i, mut found) = (0, 0);
    for &c in s {
        if c == t[i] {
            i += 1;
            if i == t.len() {
                found += 1;
                if found == k {
                    return true;
                }
                i = 0;
            }
        }
    }
    false
}

fn longest_subsequence_repeated_k(s: &[u8], k: i64) -> Vec<u8> {
    let mut counts = [0i64; 26];
    for &c in s {
        counts[(c - b'a') as usize] += 1;
    }
    let letters: Vec<u8> = (0..26u8).filter(|&i| counts[i as usize] >= k).map(|i| b'a' + i).collect();
    let mut queue: VecDeque<Vec<u8>> = VecDeque::new();
    queue.push_back(Vec::new());
    let mut best = Vec::new();
    while let Some(t) = queue.pop_front() {
        for &c in &letters {
            let mut next = t.clone();
            next.push(c);
            if repeats(s, &next, k) {
                best = next.clone();
                queue.push_back(next);
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(n: usize, letters: i64, seed: &mut i64) -> Vec<u8> {
    let mut pattern = Vec::new();
    for _ in 0..next_random(seed) % 7 + 1 {
        pattern.push(b'a' + (next_random(seed) % letters) as u8);
    }
    let mut text = Vec::new();
    let mut at = 0;
    while text.len() < n {
        if next_random(seed) % 10 < 9 {
            text.push(pattern[at]);
        }
        if text.len() < n && next_random(seed) % 10 < 1 {
            text.push(b'a' + (next_random(seed) % letters) as u8);
        }
        at = (at + 1) % pattern.len();
    }
    text
}

fn main() {
    let mut seed = 2014i64;
    let mut cases: Vec<(Vec<u8>, i64)> = Vec::new();
    for c in 0..200i64 {
        let k = 251 + next_random(&mut seed) % 50;
        cases.push((random_text(2000, c % 8 + 2, &mut seed), k));
    }
    let (mut calls, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..5 {
        for (s, k) in &cases {
            let answer = longest_subsequence_repeated_k(s, *k);
            calls += 1;
            total += answer.len() as i64;
            for &c in &answer {
                check = (check * 31 + c as i64) % 1000000007;
            }
            check = (check * 31 + answer.len() as i64) % 1000000007;
        }
    }
    println!("{calls} calls: total length {total}, checksum {check}");
}
