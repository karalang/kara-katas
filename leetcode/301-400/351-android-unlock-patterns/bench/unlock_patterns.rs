// Benchmark workload for LeetCode #351 — Rust mirror of unlock_patterns.kara.
// The same search: a skip table, runs from keys 1, 2 and 5 weighted 4, 4, 1.

const ROUNDS: i64 = 48;

fn skip_table() -> Vec<i64> {
    let mut skip = vec![0i64; 100];
    let pairs = [(1, 3, 2), (4, 6, 5), (7, 9, 8), (1, 7, 4), (2, 8, 5), (3, 9, 6), (1, 9, 5), (3, 7, 5)];
    for &(a, b, mid) in pairs.iter() {
        skip[(a * 10 + b) as usize] = mid;
        skip[(b * 10 + a) as usize] = mid;
    }
    skip
}

fn count_from(key: i64, len: i64, m: i64, n: i64, visited: &mut Vec<bool>, skip: &Vec<i64>) -> i64 {
    let mut total = 0;
    if len >= m {
        total += 1;
    }
    if len == n {
        return total;
    }
    visited[key as usize] = true;
    for next in 1..10i64 {
        let mid = skip[(key * 10 + next) as usize];
        if !visited[next as usize] && (mid == 0 || visited[mid as usize]) {
            total += count_from(next, len + 1, m, n, visited, skip);
        }
    }
    visited[key as usize] = false;
    total
}

fn number_of_patterns(m: i64, n: i64) -> i64 {
    if m > n {
        return 0;
    }
    let skip = skip_table();
    let mut visited = vec![false; 10];
    let corner = count_from(1, 1, m, n, &mut visited, &skip);
    let edge = count_from(2, 1, m, n, &mut visited, &skip);
    let center = count_from(5, 1, m, n, &mut visited, &skip);
    4 * corner + 4 * edge + center
}

fn main() {
    let mut sink: i64 = 0;
    for round in 0..ROUNDS {
        for m in 1..10 {
            for n in 1..10 {
                let c = number_of_patterns(m, n);
                sink = (sink * 31 + c + round) % 1000000007;
            }
        }
    }
    println!("sink {}", sink);
}
