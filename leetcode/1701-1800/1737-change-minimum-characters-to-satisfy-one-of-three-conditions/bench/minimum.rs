// LeetCode #1737: Change Minimum Characters to Satisfy One of Three
// Conditions -- the bench (minimum.kara): letter counts, and every
// boundary tried.

fn min_characters(a: &str, b: &str) -> i64 {
    let mut count_a = [0i64; 26];
    let mut count_b = [0i64; 26];
    for c in a.chars() {
        count_a[(c as i64 - 'a' as i64) as usize] += 1;
    }
    for c in b.chars() {
        count_b[(c as i64 - 'a' as i64) as usize] += 1;
    }
    let (m, n) = (a.len() as i64, b.len() as i64);
    let mut best = m + n;
    for c in 0..26 {
        best = best.min(m + n - count_a[c] - count_b[c]);
    }
    let mut below_a = 0;
    let mut below_b = 0;
    for c in 1..26 {
        below_a += count_a[c - 1];
        below_b += count_b[c - 1];
        best = best.min(m - below_a + below_b);
        best = best.min(n - below_b + below_a);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds: i64 = 200;
    let n = 100000;
    let mut seed: i64 = 1737;
    let mut problems: Vec<(String, String)> = Vec::new();
    for _ in 0..count {
        let a: String = (0..n)
            .map(|_| char::from_u32(97 + (next_random(&mut seed) % 26) as u32).unwrap())
            .collect();
        let b: String = (0..n)
            .map(|_| char::from_u32(97 + (next_random(&mut seed) % 26) as u32).unwrap())
            .collect();
        problems.push((a, b));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (a, b) in problems.iter() {
            let answer = min_characters(a, b);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!(
        "{} pairs of {} letters, {} rounds: changes sum to {}, checksum {}",
        count, n, rounds, sum, check
    );
}
