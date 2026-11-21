// LeetCode #2488: Count Subarrays With Median K -- Rust mirror of the ★
// arm's benchmark (median.kara): the same 20 orders and passes, the
// balances of the starts counted in a `HashMap`.
use std::collections::HashMap;

fn count_subarrays(nums: &[i64], k: i64) -> i64 {
    let n = nums.len();
    let at = nums.iter().position(|&v| v == k).unwrap();
    let mut starts: HashMap<i64, i64> = HashMap::new();
    starts.insert(0, 1);
    let mut balance = 0i64;
    for i in (0..at).rev() {
        balance += if nums[i] > k { 1 } else { -1 };
        *starts.entry(balance).or_insert(0) += 1;
    }
    let mut count = 0;
    balance = 0;
    for j in at..n {
        if j > at {
            balance += if nums[j] > k { 1 } else { -1 };
        }
        count += starts.get(&-balance).unwrap_or(&0) + starts.get(&(1 - balance)).unwrap_or(&0);
    }
    count
}

fn main() {
    let n: i64 = 10000;
    let passes: i64 = 400;
    let mut seed: i64 = 2488;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut orders: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums: Vec<i64> = (1..n + 1).collect();
        for i in (1..n).rev() {
            let j = next_random() % (i + 1);
            nums.swap(i as usize, j as usize);
        }
        orders.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for o in 0..20i64 {
            let nums = &mut orders[o as usize];
            nums.swap((check % n) as usize, ((check / n + p) % n) as usize);
            let k = (check + o) % n + 1;
            check = (check * 31 + count_subarrays(nums, k) + p) % 1_000_000_007;
        }
    }
    println!("{} passes over 20 orders of 10^4: checksum {}", passes, check);
}
