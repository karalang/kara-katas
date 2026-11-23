// LeetCode #2512: Reward Top K Students -- Rust mirror of the benchmark
// (reward.kara): the same cases, passes and checksum, the words in two
// `HashSet<String>` and each report's words looked up as they are split.
use std::collections::HashSet;

fn top_students(positive: &[String], negative: &[String], report: &[String], student_id: &[i64], k: i64) -> Vec<i64> {
    let good: HashSet<String> = positive.iter().cloned().collect();
    let bad: HashSet<String> = negative.iter().cloned().collect();
    let mut ranked: Vec<(i64, i64)> = Vec::new();
    for i in 0..report.len() {
        let mut score = 0;
        for word in report[i].split(' ') {
            if good.contains(word) {
                score += 3;
            } else if bad.contains(word) {
                score -= 1;
            }
        }
        ranked.push((-score, student_id[i]));
    }
    ranked.sort();
    ranked.iter().take(k as usize).map(|&(_, id)| id).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(w: i64) -> String {
    let mut digits = Vec::new();
    let mut v = w + 5;
    while v > 0 {
        digits.push(v % 5);
        v /= 5;
    }
    digits.iter().rev().map(|&d| (b'a' + d as u8) as char).collect()
}

fn main() {
    let mut seed = 2512;
    let mut cases: Vec<(Vec<String>, Vec<String>, Vec<String>, Vec<i64>, i64)> = Vec::new();
    for c in 0..100 {
        let p = next_random(&mut seed) % 200 + 1;
        let q = next_random(&mut seed) % 200 + 1;
        let positive: Vec<String> = (0..p).map(word).collect();
        let negative: Vec<String> = (p..p + q).map(word).collect();
        let mut report = Vec::new();
        for _ in 0..1000 {
            let length = next_random(&mut seed) % 20 + 1;
            let words: Vec<String> = (0..length).map(|_| word(next_random(&mut seed) % 600)).collect();
            report.push(words.join(" "));
        }
        let ids: Vec<i64> = (0..1000).map(|r| (r * 7919 + c) % 1000003 + 1).collect();
        cases.push((positive, negative, report, ids, c * 10 + 1));
    }
    let passes = 50;
    let mut check: i64 = 0;
    for p in 0..passes {
        for case in cases.iter_mut() {
            let at = (check % 1000) as usize;
            let kept = case.2[at].clone();
            case.2[at] = case.2[((check / 1000 + p) % 1000) as usize].clone();
            for i in top_students(&case.0, &case.1, &case.2, &case.3, case.4) {
                check = (check * 31 + i + p) % 1000000007;
            }
            case.2[at] = kept;
        }
    }
    println!("{} passes over 100 cases of 1000 reports: checksum {}", passes, check);
}
