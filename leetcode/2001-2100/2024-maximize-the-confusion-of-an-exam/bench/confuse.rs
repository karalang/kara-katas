// LeetCode #2024: Maximize the Confusion of an Exam -- the ★ arm in Rust,
// the same algorithm and workload as confuse.kara: a sliding window for each
// answer, the longer of the two.

fn longest_run(key: &[u8], c: u8, k: i64) -> i64 {
    let (mut best, mut left, mut other) = (0i64, 0usize, 0i64);
    for right in 0..key.len() {
        if key[right] != c {
            other += 1;
        }
        while other > k {
            if key[left] != c {
                other -= 1;
            }
            left += 1;
        }
        best = best.max((right - left + 1) as i64);
    }
    best
}

fn max_consecutive_answers(answer_key: &str, k: i64) -> i64 {
    let key = answer_key.as_bytes();
    longest_run(key, b'T', k).max(longest_run(key, b'F', k))
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2024;
    let mut keys: Vec<String> = Vec::new();
    let mut ks: Vec<i64> = Vec::new();
    for a in 0..20 {
        let pct = [50, 70, 90, 97, 99][a % 5];
        let mut key = String::new();
        for _ in 0..100000 {
            key.push(if next_random(&mut seed) % 100 < pct { 'T' } else { 'F' });
        }
        keys.push(key);
        ks.push([1, 10, 100, 1000, 10000][a / 4]);
    }
    let (mut calls, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..5 {
        for a in 0..20 {
            let best = max_consecutive_answers(&keys[a], ks[a]);
            calls += 1;
            total += best;
            check = (check * 31 + best) % 1000000007;
        }
    }
    println!("{} calls: total {}, checksum {}", calls, total, check);
}
