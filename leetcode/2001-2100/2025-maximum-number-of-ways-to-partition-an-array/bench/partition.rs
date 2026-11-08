// LeetCode #2025: Maximum Number of Ways to Partition an Array -- the ★ arm
// in Rust, the same algorithm and workload as partition.kara: two HashMaps
// of the pivots' differences, swept.
use std::collections::HashMap;

fn ways_to_partition(nums: &[i64], k: i64) -> i64 {
    let n = nums.len();
    let total: i64 = nums.iter().sum();
    let mut d: Vec<i64> = Vec::new();
    let mut left = 0;
    for p in 1..n {
        left += nums[p - 1];
        d.push(left - (total - left));
    }
    let mut right: HashMap<i64, i64> = HashMap::new();
    for &x in &d {
        *right.entry(x).or_insert(0) += 1;
    }
    let mut best = *right.get(&0).unwrap_or(&0);
    let mut seen: HashMap<i64, i64> = HashMap::new();
    for i in 0..n {
        if i >= 1 {
            let x = d[i - 1];
            *right.entry(x).or_insert(0) -= 1;
            *seen.entry(x).or_insert(0) += 1;
        }
        let delta = k - nums[i];
        let ways = *right.get(&-delta).unwrap_or(&0) + *seen.get(&delta).unwrap_or(&0);
        best = best.max(ways);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2025;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut ks: Vec<i64> = Vec::new();
    for a in 0..20 {
        let r = [1, 2, 3, 10, 100, 1000, 10000, 100000][a % 8];
        arrays.push((0..50000).map(|_| next_random(&mut seed) % (2 * r + 1) - r).collect());
        ks.push(next_random(&mut seed) % (2 * r + 1) - r);
    }
    let (mut calls, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..10 {
        for a in 0..20 {
            let best = ways_to_partition(&arrays[a], ks[a]);
            calls += 1;
            total += best;
            check = (check * 31 + best) % 1000000007;
        }
    }
    println!("{} calls: total {}, checksum {}", calls, total, check);
}
