// LeetCode #2857: Count Pairs of Points With Distance k -- the bench:
// the ★ arm over 10 cases of 50000 points, LeetCode's most, every
// other one in a 256 x 256 square and the rest up to 10^6, with k up
// to 100, all drawn first, then each answered 3 times.

use std::collections::HashMap;

fn count_pairs(coordinates: &[Vec<i64>], k: i64) -> i64 {
    let mut seen: HashMap<(i64, i64), i64> = HashMap::new();
    let mut pairs = 0;
    for p in coordinates.iter() {
        let (x, y) = (p[0], p[1]);
        for a in 0..=k {
            pairs += seen.get(&(x ^ a, y ^ (k - a))).copied().unwrap_or(0);
        }
        *seen.entry((x, y)).or_insert(0) += 1;
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 10;
    let rounds = 3;
    let n = 50000;
    let mut seed = 2857;
    let mut cases: Vec<(Vec<Vec<i64>>, i64)> = Vec::new();
    for c in 0..count {
        let top = if c % 2 == 0 { 256 } else { 1000001 };
        let k = next_random(&mut seed) % 101;
        let mut points: Vec<Vec<i64>> = Vec::new();
        for _ in 0..n {
            let x = wide(&mut seed) % top;
            let y = wide(&mut seed) % top;
            points.push(vec![x, y]);
        }
        cases.push((points, k));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (points, k) in cases.iter() {
            let pairs = count_pairs(points, *k);
            total += pairs;
            check = (check * 31 + pairs + r) % 1000000007;
        }
    }
    println!("{count} cases of {n} points, {rounds} rounds: {total} pairs, checksum {check}");
}
