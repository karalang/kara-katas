// Benchmark for #447: mirror of number_of_boomerangs.kara (a map of
// distances per point) on 10 random sets of 1,000 distinct points on a
// 300 x 300 grid, built once. `HashMap` with its default SipHash, as
// Kāra's `Map` hashes with SipHash-1-3.
use std::collections::{HashMap, HashSet};

fn number_of_boomerangs(points: &[(i64, i64)]) -> i64 {
    let mut total = 0;
    for p in points {
        let mut counts: HashMap<i64, i64> = HashMap::new();
        for q in points {
            let dx = p.0 - q.0;
            let dy = p.1 - q.1;
            *counts.entry(dx * dx + dy * dy).or_insert(0) += 1;
        }
        for c in counts.values() {
            total += c * (c - 1);
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let n = 1000;
    let mut seed: i64 = 447;
    let mut sets: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..count {
        let mut seen: HashSet<(i64, i64)> = HashSet::new();
        let mut points: Vec<(i64, i64)> = Vec::new();
        while points.len() < n {
            let x = next_random(&mut seed) % 300;
            let y = next_random(&mut seed) % 300;
            if seen.insert((x, y)) {
                points.push((x, y));
            }
        }
        sets.push(points);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for points in &sets {
        let answer = number_of_boomerangs(points);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{count} sets of {n} points: {total} boomerangs, checksum {checksum}");
}
