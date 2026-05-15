//! Benchmark workload — linear scan find-min on a rotated sorted array.
//!
//! Algorithmic mirror of bench/linear_scan.kara and bench/linear_scan.py.
//! See ../README.md § Benchmarks for the choice of N / K and the
//! rotated-sorted generator.

use std::hint::black_box;

fn find_min(nums: &[i64]) -> i64 {
    let mut m = nums[0];
    for &x in &nums[1..] {
        if x < m {
            m = x;
        }
    }
    m
}

fn main() {
    const N: usize = 2_000_000;
    const R: usize = 666_666;
    let mut data: Vec<i64> = Vec::with_capacity(N);
    for i in 0..N {
        data.push((((i + R) % N) + 1) as i64);
    }

    let mut sum: i64 = 0;
    for _ in 0..10 {
        sum += find_min(black_box(&data));
    }
    println!("{}", sum);
}
