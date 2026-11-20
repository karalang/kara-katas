// LeetCode #2386: Find the K-Sum of an Array -- the bench, the ★ arm in
// Rust: the largest sum less the (k-1)-th smallest nonempty sum of the
// sorted sizes, walked from the smallest by a heap of (sum, last place).

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn k_sum(nums: &[i64], k: i64) -> i64 {
    let mut largest = 0i64;
    let mut sizes: Vec<i64> = Vec::new();
    for &v in nums {
        if v > 0 {
            largest += v;
        }
        sizes.push(v.abs());
    }
    sizes.sort();
    let mut heap = BinaryHeap::new();
    heap.push(Reverse((sizes[0], 0usize)));
    let mut lost = 0i64;
    for _ in 1..k {
        let Reverse((sum, last)) = heap.pop().unwrap();
        lost = sum;
        if last + 1 < sizes.len() {
            heap.push(Reverse((sum + sizes[last + 1], last + 1)));
            heap.push(Reverse((sum - sizes[last] + sizes[last + 1], last + 1)));
        }
    }
    largest - lost
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    // 10 arrays of 10^5 values from -10^9 to 10^9; pass p asks array a for
    // k = 2000 - (7 p + a) % 100
    let mut seed = 2386i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        arrays.push((0..100000).map(|_| wide(&mut seed) % 2000000001 - 1000000000).collect());
    }
    let mut check = 0i64;
    for p in 0..60i64 {
        for a in 0..10i64 {
            let answer = k_sum(&arrays[a as usize], 2000 - (7 * p + a) % 100);
            check = (check * 31 + answer % 1000000007 + 1000000007 + p) % 1000000007;
        }
    }
    println!("60 passes over 10 arrays of 10^5 values: checksum {}", check);
}
