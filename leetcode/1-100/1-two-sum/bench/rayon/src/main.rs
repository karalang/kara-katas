// LeetCode #1 — rayon-parallel Rust mirror (par lane, brute_force).
// Same O(n²) two_sum as ../brute_force.rs; the 100-call reduction runs across a
// rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par. Sink = -200.
use rayon::prelude::*;

fn two_sum(nums: &[i64], target: i64) -> Option<(usize, usize)> {
    let n = nums.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if nums[i] + nums[j] == target {
                return Some((i, j));
            }
        }
    }
    None
}

fn main() {
    const N: usize = 5000;
    let data: [i64; N] = std::array::from_fn(|i| ((i as i64) * 7) % 1000);
    let target: i64 = -1;
    let sum: i64 = (0..100)
        .into_par_iter()
        .map(|_| match two_sum(&data, target) {
            Some((i, j)) => i as i64 + j as i64,
            None => -2,
        })
        .sum();
    println!("{}", sum);
}
