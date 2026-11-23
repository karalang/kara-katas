// LeetCode #2530: Maximal Score After Applying K Operations -- Rust mirror
// of the benchmark (score.kara): the same numbers, passes, order and
// checksum.
use std::collections::BinaryHeap;

fn max_kelements(nums: &[i64], k: i64) -> i64 {
    let mut heap: BinaryHeap<i64> = BinaryHeap::new();
    for &x in nums.iter() {
        heap.push(x);
    }
    let mut score = 0;
    for _ in 0..k {
        let top = heap.pop().unwrap();
        score += top;
        heap.push((top + 2) / 3);
    }
    score
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2530;
    let nums: Vec<i64> = (0..100000).map(|_| wide_random(&mut seed) % 1000000000 + 1).collect();
    let passes = 170;
    let mut check: i64 = 0;
    for p in 0..passes {
        let k = 50000 + check % 50001;
        check = (check * 31 + max_kelements(&nums, k) % 1000000007 + p) % 1000000007;
    }
    println!("{passes} passes over 100000 numbers: checksum {check}");
}
