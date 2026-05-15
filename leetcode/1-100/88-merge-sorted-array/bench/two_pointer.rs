//! Benchmark workload — two-pointer-from-back O(m + n) Merge Sorted Array.
//!
//! Algorithmic mirror of bench/two_pointer.kara and bench/two_pointer.py. See
//! ../README.md § Benchmarks for the choice of m, n, K and the
//! maximally-alternating input.

fn merge(nums1: &mut [i64], m: i64, nums2: &[i64], n: i64) {
    let mut i = m - 1;
    let mut j = n - 1;
    let mut k = m + n - 1;
    while j >= 0 {
        if i >= 0 && nums1[i as usize] > nums2[j as usize] {
            nums1[k as usize] = nums1[i as usize];
            i -= 1;
        } else {
            nums1[k as usize] = nums2[j as usize];
            j -= 1;
        }
        k -= 1;
    }
}

fn main() {
    const M: usize = 1_000_000;
    const N: usize = 1_000_000;
    const TOTAL: usize = M + N;

    let prefix_a: Vec<i64> = (0..M as i64).map(|i| 2 * i).collect();
    let b: Vec<i64> = (0..N as i64).map(|i| 2 * i + 1).collect();

    let mut workspace: Vec<i64> = vec![0; TOTAL];

    let mut sum: i64 = 0;
    for _ in 0..10 {
        for p in 0..M {
            workspace[p] = prefix_a[p];
        }
        merge(&mut workspace, M as i64, &b, N as i64);
        sum += workspace[TOTAL - 1];
    }
    println!("{}", sum);
}
