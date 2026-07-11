// Benchmark workload — Remove Duplicates from Sorted Array II (LeetCode #80).
// Rust mirror of bench/remove_duplicates_ii.kara. The generalized run-scan computes
// the at-most-2 dedup and folds each kept value through a rolling polynomial hash —
// the loop-carried hash serialises the scan, and a fixed heap Vec built once avoids
// per-iteration allocation. N=3000 sorted array with mixed run lengths, scanned
// K=67000 times, seeded by the iteration index. See ../README.md.

fn build(n: i64) -> Vec<i64> {
    let mut arr: Vec<i64> = Vec::new();
    let mut val: i64 = 0;
    let mut pos: i64 = 0;
    while pos < n {
        let runlen = (val % 3) + 1;
        let mut r = 0;
        while r < runlen && pos < n {
            arr.push(val);
            pos += 1;
            r += 1;
        }
        val += 1;
    }
    arr
}

fn scan_fold(arr: &[i64], n: i64, seed: i64) -> i64 {
    let mut acc = seed;
    let mut i: i64 = 0;
    while i < n {
        let v = arr[i as usize];
        let mut run = 0;
        while i < n && arr[i as usize] == v {
            if run < 2 {
                acc = (acc * 131 + (v + 1)) % 1_000_000_007;
            }
            run += 1;
            i += 1;
        }
    }
    acc
}

fn main() {
    const N: i64 = 3000;
    const TOTAL: i64 = 67000;
    const MODULUS: i64 = 1_000_000_007;

    let arr = build(N);
    let mut sum: i64 = 0;
    for iter in 0..TOTAL {
        let r = scan_fold(&arr, N, iter);
        sum = (sum + r) % MODULUS;
    }
    println!("{}", sum);
}
