// Benchmark for #532: Rust mirror of the ★ arm (count each number); see
// find_pairs.kara. `HashMap` with its default SipHash-1-3, the hasher
// Kāra's `Map` uses too.
use std::collections::HashMap;

fn find_pairs(nums: &[i64], k: i64) -> i64 {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for &x in nums {
        *counts.entry(x).or_insert(0) += 1;
    }
    let mut pairs = 0;
    for (v, c) in counts.iter() {
        if k == 0 {
            if *c >= 2 {
                pairs += 1;
            }
        } else if counts.contains_key(&(*v + k)) {
            pairs += 1;
        }
    }
    pairs
}

fn main() {
    // 20 arrays of 10,000 numbers made once, the a-th drawn from
    // -1,000(a + 1) to 1,000(a + 1); then each array is answered for 200
    // values of k from 0 to 19.
    let mut seed: i64 = 532;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..20 {
        let half = 1000 * (a + 1);
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..10000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            nums.push(seed / 65536 % (2 * half + 1) - half);
        }
        arrays.push(nums);
    }
    let mut total = 0i64;
    let mut checksum = 0i64;
    for _ in 0..200 {
        for a in 0..arrays.len() {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let answer = find_pairs(&arrays[a], seed / 65536 % 20);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    println!("20 arrays of 10000, 200 values of k each: total {}, checksum {}", total, checksum);
}
