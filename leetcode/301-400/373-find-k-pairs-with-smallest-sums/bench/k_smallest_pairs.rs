// Benchmark for #373 -- mirror of k_smallest_pairs.kara.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn k_smallest_pairs(nums1: &[i64], nums2: &[i64], k: usize) -> Vec<(i64, i64)> {
    let mut out = Vec::new();
    if nums1.is_empty() || nums2.is_empty() {
        return out;
    }
    let mut fronts = BinaryHeap::new();
    for i in 0..nums1.len().min(k) {
        fronts.push(Reverse((nums1[i] + nums2[0], i, 0usize)));
    }
    while out.len() < k {
        match fronts.pop() {
            Some(Reverse((_, i, j))) => {
                out.push((nums1[i], nums2[j]));
                if j + 1 < nums2.len() {
                    fronts.push(Reverse((nums1[i] + nums2[j + 1], i, j + 1)));
                }
            }
            None => break,
        }
    }
    out
}

fn main() {
    let mut seed: i64 = 373;
    let mut checksum: i64 = 0;
    let mut nums1 = vec![0i64; 100000];
    let mut nums2 = vec![0i64; 100000];
    for _ in 0..20 {
        let mut v: i64 = -1000000000;
        for x in nums1.iter_mut() {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            v += (seed / 65536) % 20000;
            *x = v;
        }
        v = -1000000000;
        for x in nums2.iter_mut() {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            v += (seed / 65536) % 20000;
            *x = v;
        }
        for (u, w) in k_smallest_pairs(&nums1, &nums2, 10000) {
            checksum = (checksum * 31 + (u + w) % 1000000007 + 2000000000) % 1000000007;
        }
    }
    println!("checksum {}", checksum);
}
