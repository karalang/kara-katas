// LeetCode #1124: Longest Well-Performing Interval -- the bench in Rust,
// the ★ arm with a `HashMap<i64, i64>` from score to first index (SipHash,
// as Kāra's `Map`), the same 16 schedules and 300 rounds.
use std::collections::HashMap;

fn longest_wpi(hours: &[i32]) -> i64 {
    let mut first: HashMap<i64, i64> = HashMap::new();
    let mut score: i64 = 0;
    let mut best: i64 = 0;
    for (i, &h) in hours.iter().enumerate() {
        let i = i as i64;
        score += if h > 8 { 1 } else { -1 };
        if score > 0 {
            best = i + 1;
        } else {
            if let Some(&j) = first.get(&(score - 1)) {
                best = best.max(i - j);
            }
            first.entry(score).or_insert(i);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1124;
    let mut schedules: Vec<Vec<i32>> = Vec::new();
    for _ in 0..16 {
        let hours: Vec<i32> = (0..10000).map(|_| (next_random(&mut seed) % 17) as i32).collect();
        schedules.push(hours);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..300i64 {
        for (j, hours) in schedules.iter_mut().enumerate() {
            let at = ((round * 7919 + j as i64 * 104729) % 10000) as usize;
            let h = hours[at];
            hours[at] = if h > 8 { h - 9 } else { 9 + h % 8 };
            let answer = longest_wpi(hours);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("300 rounds over 16 schedules of 10^4 days: answers total {total}, checksum {check}");
}
