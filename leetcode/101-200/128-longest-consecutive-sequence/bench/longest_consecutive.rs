// Benchmark harness for LeetCode #128 — Longest Consecutive Sequence.
// Mirrors longest_consecutive.kara algorithm-for-algorithm.

use std::collections::HashSet;

fn longest_consecutive(nums: &[i64]) -> i64 {
    let mut s: HashSet<i64> = HashSet::new();
    for &v in nums {
        s.insert(v);
    }
    let mut best: i64 = 0;
    for &v in nums {
        if !s.contains(&(v - 1)) {
            let mut length: i64 = 1;
            let mut cur = v;
            while s.contains(&(cur + 1)) {
                cur += 1;
                length += 1;
            }
            if length > best {
                best = length;
            }
        }
    }
    best
}

fn lcg(seed: i64, n: i64, cap: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut x = seed;
    for _ in 0..n {
        x = (x * 1103515245 + 12345) % 2147483648;
        out.push(x % cap);
    }
    out
}

fn main() {
    let np: i64 = 8;
    let n: i64 = 20000;
    let cap: i64 = 25000;
    let iters: i64 = 150;

    let arrays: Vec<Vec<i64>> = (0..np).map(|j| lcg(j + 1, n, cap)).collect();

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        sink += longest_consecutive(&arrays[idx]);
    }
    println!("{}", sink);
}
