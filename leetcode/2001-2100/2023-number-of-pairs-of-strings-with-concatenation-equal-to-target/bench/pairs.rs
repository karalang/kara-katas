// LeetCode #2023: Number of Pairs of Strings With Concatenation Equal to
// Target -- the ★ arm in Rust, the same algorithm and workload as
// pairs.kara: a HashMap of owned strings, looked up by the target's slices.
use std::collections::HashMap;

fn num_of_pairs(nums: &[String], target: &str) -> i64 {
    let mut count: HashMap<String, i64> = HashMap::new();
    for s in nums {
        *count.entry(s.clone()).or_insert(0) += 1;
    }
    let mut pairs = 0;
    for k in 1..target.len() {
        let a = &target[0..k];
        let b = &target[k..];
        let ca = *count.get(a).unwrap_or(&0);
        if a == b {
            pairs += ca * (ca - 1);
        } else {
            pairs += ca * *count.get(b).unwrap_or(&0);
        }
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2023;
    let mut lists: Vec<Vec<String>> = Vec::new();
    let mut targets: Vec<String> = Vec::new();
    for _ in 0..300 {
        let block_len = next_random(&mut seed) % 3 + 1;
        let mut block = String::new();
        for _ in 0..block_len {
            block.push((b'1' + (next_random(&mut seed) % 2) as u8) as char);
        }
        let nums: Vec<String> = (0..100)
            .map(|_| block.repeat((next_random(&mut seed) % (100 / block_len) + 1) as usize))
            .collect();
        lists.push(nums);
        targets.push(block.repeat((next_random(&mut seed) % (100 / block_len - 1) + 2) as usize));
    }
    let (mut calls, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..20 {
        for p in 0..300 {
            let pairs = num_of_pairs(&lists[p], &targets[p]);
            calls += 1;
            total += pairs;
            check = (check * 31 + pairs) % 1000000007;
        }
    }
    println!("{} calls: {} pairs, checksum {}", calls, total, check);
}
