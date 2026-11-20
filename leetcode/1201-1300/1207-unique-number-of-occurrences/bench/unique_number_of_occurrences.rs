// LeetCode #1207 bench, in Rust: the ★ arm (each value's count in a
// `HashMap`, and the counts put in a `HashSet`) on 2000 arrays of 1000
// values drawn once, then 10 rounds over the arrays, how many answer true
// folded into a checksum.

use std::collections::{HashMap, HashSet};

fn unique_occurrences(arr: &[i64]) -> bool {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for &v in arr {
        *counts.entry(v).or_insert(0) += 1;
    }
    let distinct: HashSet<i64> = counts.values().copied().collect();
    distinct.len() == counts.len()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1207i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let k = next_random(&mut seed) % 12 + 1;
        let values: Vec<i64> = (0..k).map(|_| next_random(&mut seed) % 2001 - 1000).collect();
        let total = k * (k + 1) / 2;
        let arr: Vec<i64> = (0..1000)
            .map(|_| {
                let mut r = next_random(&mut seed) % total;
                let mut j = 0;
                while r > j {
                    r -= j + 1;
                    j += 1;
                }
                values[j as usize]
            })
            .collect();
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for round in 0..10 {
        let yes = arrays.iter().filter(|a| unique_occurrences(a)).count() as i64;
        check = (check * 131 + yes + round) % 1000000007;
    }
    println!("10 rounds over 2000 arrays of 1000 values: checksum {check}");
}
