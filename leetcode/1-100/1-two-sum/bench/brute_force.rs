//! Benchmark workload — brute-force O(n²) Two Sum.
//!
//! Algorithmic mirror of bench/brute_force.kara and bench/brute_force.py.
//! See ../README.md § Benchmarks for the choice of N / K and the
//! no-short-circuit target sentinel.

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

    let mut sum: i64 = 0;
    for _ in 0..10 {
        sum += match two_sum(&data, target) {
            Some((i, j)) => i as i64 + j as i64,
            None => -2,
        };
    }
    println!("{}", sum);
}
