// LeetCode #2163: Minimum Difference in Sums After Removal of Elements --
// the benchmark's Rust mirror of difference.kara: `BinaryHeap` largest
// first for the prefix, of `Reverse` for the suffix.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn minimum_difference(nums: Vec<i64>) -> i64 {
    let n = nums.len() / 3;
    let mut kept: BinaryHeap<i64> = BinaryHeap::new();
    let mut sum = 0i64;
    let mut left: Vec<i64> = Vec::new();
    for i in 0..2 * n {
        kept.push(nums[i]);
        sum += nums[i];
        if kept.len() > n {
            sum -= kept.pop().unwrap();
        }
        if i + 1 >= n {
            left.push(sum);
        }
    }
    let mut kept: BinaryHeap<Reverse<i64>> = BinaryHeap::new();
    let mut sum = 0i64;
    let mut best = i64::MAX;
    for i in (n..3 * n).rev() {
        kept.push(Reverse(nums[i]));
        sum += nums[i];
        if kept.len() > n {
            sum -= kept.pop().unwrap().0;
        }
        if i <= 2 * n {
            best = best.min(left[i - n] - sum);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2163i64;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        lists.push((0..300000).map(|_| wide_random(&mut seed) % 100000 + 1).collect());
    }
    let mut check = 0i64;
    for _ in 0..5 {
        for k in 0..4 {
            let at = (wide_random(&mut seed) % 300000) as usize;
            lists[k][at] = wide_random(&mut seed) % 100000 + 1;
            let d = minimum_difference(lists[k].clone());
            check = (check * 31 + d + 1000000000000) % 1000000007;
        }
    }
    println!("20 solves: checksum {}", check);
}
