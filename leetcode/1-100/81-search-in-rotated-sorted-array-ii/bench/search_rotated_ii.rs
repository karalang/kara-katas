// Benchmark workload — Search in Rotated Sorted Array II (LeetCode #81).
// Rust mirror of bench/search_rotated_ii.kara. Build-once + punch: one rotated sorted
// array with duplicates (each value 0..M appears twice, M=1000, rotated) built once,
// then searched K=17,000,000 times for targets sweeping present/absent values, each
// boolean folded through a rolling polynomial hash. The duplicate-aware rotated
// binary search's branch loop is the measured work. See ../README.md.

fn search(nums: &[i64], len: i64, target: i64) -> bool {
    let mut lo: i64 = 0;
    let mut hi: i64 = len - 1;
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        if nums[mid as usize] == target {
            return true;
        }
        if nums[lo as usize] == nums[mid as usize] && nums[mid as usize] == nums[hi as usize] {
            lo += 1;
            hi -= 1;
        } else if nums[lo as usize] <= nums[mid as usize] {
            if nums[lo as usize] <= target && target < nums[mid as usize] {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else if nums[mid as usize] < target && target <= nums[hi as usize] {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    false
}

fn build(m: i64, dup: i64, rot: i64) -> Vec<i64> {
    let n = m * dup;
    let mut base: Vec<i64> = Vec::with_capacity(n as usize);
    for v in 0..m {
        for _ in 0..dup {
            base.push(v);
        }
    }
    let mut arr: Vec<i64> = Vec::with_capacity(n as usize);
    for i in 0..n {
        arr.push(base[((i + rot) % n) as usize]);
    }
    arr
}

fn main() {
    const M: i64 = 1000;
    const DUP: i64 = 2;
    const TOTAL: i64 = 17_000_000;
    const MODULUS: i64 = 1_000_000_007;

    let arr = build(M, DUP, (M * DUP) / 3);
    let n = arr.len() as i64;
    let span = M + 50;
    let mut sum: i64 = 0;
    for iter in 0..TOTAL {
        let target = iter % span;
        let found = search(&arr, n, target);
        let bit = if found { 1 } else { 0 };
        sum = (sum * 131 + bit + 1) % MODULUS;
    }
    println!("{}", sum);
}
