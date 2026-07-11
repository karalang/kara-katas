// Benchmark workload — Subsets II (LeetCode #90).
// Rust mirror of bench/subsets_ii.kara. Enumerate-and-fold over the emit-at-node dedup
// backtracking of a sorted multiset (8 distinct values x2 => 3^8 unique subsets); each
// node's path is folded into a threaded accumulator, K=2700 iterations seeded by the
// index. Compiled with `rustc -O`. See ../README.md § Benchmarks.

fn enumerate(nums: &[i64], start: i64, path: &mut Vec<i64>, acc: i64) -> i64 {
    let plen = path.len() as i64;
    let mut a = (acc * 131 + (plen + 1)) % 1_000_000_007;
    for &x in path.iter() {
        a = (a * 131 + (x + 1)) % 1_000_000_007;
    }
    let n = nums.len() as i64;
    let mut i = start;
    while i < n {
        if i == start || nums[i as usize] != nums[(i - 1) as usize] {
            path.push(nums[i as usize]);
            a = enumerate(nums, i + 1, path, a);
            path.pop();
        }
        i += 1;
    }
    a
}

fn main() {
    const D: i64 = 8;
    const R: i64 = 2;
    const TOTAL: i64 = 2700;
    const MODULUS: i64 = 1_000_000_007;

    let mut nums: Vec<i64> = Vec::new();
    for v in 0..D {
        for _ in 0..R {
            nums.push(v);
        }
    }

    let mut sum: i64 = 0;
    for iter in 0..TOTAL {
        let mut path: Vec<i64> = Vec::new();
        let rr = enumerate(&nums, 0, &mut path, iter);
        sum = (sum * 131 + rr) % MODULUS;
    }
    println!("{}", sum);
}
