// LeetCode #2845: Count of Interesting Subarrays -- the bench, mirrored
// from interesting.kara: a map from each prefix count mod modulo to how
// often it has come up, read before each new prefix is added.
use std::collections::HashMap;

fn count_interesting_subarrays(nums: &[i64], modulo: i64, k: i64) -> i64 {
    let mut seen: HashMap<i64, i64> = HashMap::new();
    seen.insert(0, 1);
    let mut prefix = 0;
    let mut count = 0;
    for &x in nums.iter() {
        if x % modulo == k {
            prefix = (prefix + 1) % modulo;
        }
        let want = (prefix - k + modulo) % modulo;
        count += seen.get(&want).copied().unwrap_or(0);
        *seen.entry(prefix).or_insert(0) += 1;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let n = 100000;
    let rounds = 20;
    let mut seed = 2845;
    let mut cases: Vec<(Vec<i64>, i64, i64)> = Vec::new();
    for c in 0..count {
        let nums: Vec<i64> = (0..n)
            .map(|_| (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000 + 1)
            .collect();
        let modulo = next_random(&mut seed) % if c % 2 == 0 { 10 } else { 100000 } + 1;
        let k = next_random(&mut seed) % modulo;
        cases.push((nums, modulo, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, modulo, k) in cases.iter() {
            let got = count_interesting_subarrays(nums, *modulo, *k);
            total += got;
            check = (check * 31 + got % 1000000007 + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: {total} subarrays, checksum {check}");
}
