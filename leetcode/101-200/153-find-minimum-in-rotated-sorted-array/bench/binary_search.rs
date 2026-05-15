//! Benchmark workload — binary search find-min on a rotated sorted array.
//!
//! Algorithmic mirror of bench/binary_search.kara and bench/binary_search.py.
//! See ../README.md § Benchmarks for the choice of N / K and the
//! rotated-sorted generator.
//!
//! `black_box(&data)` keeps LLVM from hoisting the pure find_min call out
//! of the K=2_000_000 outer loop — without it the inner work collapses to
//! a single call and the bench measures startup, not algorithm time.

use std::hint::black_box;

fn find_min(nums: &[i64]) -> i64 {
    let mut lo: usize = 0;
    let mut hi: usize = nums.len() - 1;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if nums[mid] > nums[hi] {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    nums[lo]
}

fn main() {
    const N: usize = 2_000_000;
    const R: usize = 666_666;
    let mut data: Vec<i64> = Vec::with_capacity(N);
    for i in 0..N {
        data.push((((i + R) % N) + 1) as i64);
    }

    let mut sum: i64 = 0;
    for _ in 0..2_000_000 {
        sum += find_min(black_box(&data));
    }
    println!("{}", sum);
}
