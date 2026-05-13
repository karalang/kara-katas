//! Benchmark workload — BFS + sieve solution to LeetCode #3629.
//!
//! Algorithmic mirror of bench/bfs_sieve.kara and bench/bfs_sieve.py.
//! See ../README.md § Benchmarks for the choice of N / K and the
//! deterministic seeding scheme.

use std::collections::{HashMap, VecDeque};

fn build_factors(cap: i64) -> Vec<Vec<i64>> {
    let cap_u = cap as usize;
    let mut factors: Vec<Vec<i64>> = (0..=cap_u).map(|_| Vec::new()).collect();
    for i in 2..=cap {
        if factors[i as usize].is_empty() {
            let mut j = i;
            while j <= cap {
                factors[j as usize].push(i);
                j += i;
            }
        }
    }
    factors
}

fn min_jumps(nums: &[i64]) -> i64 {
    let n = nums.len();
    if n <= 1 {
        return 0;
    }

    let cap = *nums.iter().max().unwrap_or(&1).max(&1);
    let factors = build_factors(cap);

    let mut bucket: HashMap<i64, Vec<i64>> = HashMap::new();
    for (j, &v) in nums.iter().enumerate() {
        if v >= 2 {
            for &p in &factors[v as usize] {
                bucket.entry(p).or_insert_with(Vec::new).push(j as i64);
            }
        }
    }

    let mut visited = vec![false; n];
    visited[0] = true;

    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    queue.push_back((0, 0));

    while let Some((i, d)) = queue.pop_front() {
        if i as usize == n - 1 {
            return d;
        }
        if i > 0 && !visited[(i - 1) as usize] {
            visited[(i - 1) as usize] = true;
            queue.push_back((i - 1, d + 1));
        }
        if (i + 1) < n as i64 && !visited[(i + 1) as usize] {
            visited[(i + 1) as usize] = true;
            queue.push_back((i + 1, d + 1));
        }
        let v = nums[i as usize];
        if v >= 2 && factors[v as usize][0] == v {
            if let Some(indices) = bucket.remove(&v) {
                for j in indices.into_iter() {
                    if !visited[j as usize] {
                        visited[j as usize] = true;
                        queue.push_back((j, d + 1));
                    }
                }
            }
        }
    }

    -1
}

fn main() {
    const N: usize = 50_000;
    let data: Vec<i64> = (0..N as i64).map(|i| (i * 7919 + 13) % 999983 + 2).collect();

    let mut sum: i64 = 0;
    for _ in 0..3 {
        sum += min_jumps(&data);
    }
    println!("{}", sum);
}
