// Benchmark workload — Subsets (LeetCode #78).
// Rust mirror of bench/subsets.kara. Emit-at-every-node backtracking that ENUMERATES
// the power set of [1..16] (2^16 subsets) and folds each node's path into a threaded
// accumulator (no storage), K=300 iterations seeded by the iteration index. The DFS
// recursion is the measured work. See ../README.md.

fn enumerate(nums: &[i64], start: i64, path: &mut Vec<i64>, acc: i64) -> i64 {
    let mut a = acc;
    a = (a * 131 + (path.len() as i64 + 1)) % 1_000_000_007;
    for &x in path.iter() {
        a = (a * 131 + x) % 1_000_000_007;
    }
    let n = nums.len() as i64;
    let mut i = start;
    while i < n {
        path.push(nums[i as usize]);
        a = enumerate(nums, i + 1, path, a);
        path.pop();
        i += 1;
    }
    a
}

fn main() {
    const N: i64 = 16;
    const TOTAL: i64 = 300;
    const MODULUS: i64 = 1_000_000_007;

    let nums: Vec<i64> = (1..=N).collect();
    let mut path: Vec<i64> = Vec::new();
    let mut sum: i64 = 0;
    for iter in 0..TOTAL {
        let r = enumerate(&nums, 0, &mut path, iter);
        sum = (sum + r) % MODULUS;
    }
    println!("{}", sum);
}
