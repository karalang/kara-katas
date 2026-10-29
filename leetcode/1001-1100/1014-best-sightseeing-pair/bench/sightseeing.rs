// LeetCode #1014: Best Sightseeing Pair -- bench
// Mirrors sightseeing.kara; see ../README.md § Benchmarks.

fn max_score_sightseeing_pair(values: &[i64]) -> i64 {
    let mut best_first = values[0];
    let mut best = 0;
    for j in 1..values.len() {
        best = best.max(best_first + values[j] - j as i64);
        best_first = best_first.max(values[j] + j as i64);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: usize = 50000;
    let rounds = 10000;
    let mut seed = 1014;
    let mut values: Vec<i64> = Vec::new();
    for _ in 0..count {
        values.push(1 + next_random(&mut seed) % 1000);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        let at = ((hi * 32768 + lo) % count as i64) as usize;
        values[at] = 1 + next_random(&mut seed) % 1000;
        let answer = max_score_sightseeing_pair(&values);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    println!("{} rounds over {} values: answers sum to {}, checksum {}", rounds, count, total, check);
}
