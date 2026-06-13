// LeetCode #153 — rayon-parallel Rust mirror (par lane, binary_search).
// Same O(log n) find_min as ../binary_search.rs; the K=2_000_000-call
// reduction runs across a rayon pool. Hand-tuned-parallel comparator for
// Kāra's auto-par (which parallelizes the same K-loop from zero parallel
// source). Sink = 2000000 (K × min value 1).
use rayon::prelude::*;
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
    const K: i64 = 2_000_000;

    let mut data = vec![0i64; N];
    for i in 0..N {
        data[i] = (((i + R) % N) + 1) as i64;
    }

    // black_box(&data) per call mirrors the seq lane — without it LLVM hoists
    // the loop-invariant pure find_min out of the K-loop (2M calls → 1).
    let sum: i64 = (0..K)
        .into_par_iter()
        .map(|_| find_min(black_box(&data)))
        .sum();
    println!("{}", sum);
}
