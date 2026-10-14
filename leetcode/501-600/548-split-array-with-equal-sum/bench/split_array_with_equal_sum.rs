// Benchmark for #548: Rust mirror of the ★ arm (a set of left sums per
// middle cut); see split_array_with_equal_sum.kara.
use std::collections::HashSet;

fn split_array(nums: &[i64]) -> bool {
    let n = nums.len();
    if n < 7 {
        return false;
    }
    let mut prefix = vec![0i64; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    for j in 3..n - 3 {
        let mut sums: HashSet<i64> = HashSet::new();
        for i in 1..j - 1 {
            if prefix[i] == prefix[j] - prefix[i + 1] {
                sums.insert(prefix[i]);
            }
        }
        for k in j + 2..n - 1 {
            let third = prefix[k] - prefix[j + 1];
            if third == prefix[n] - prefix[k + 1] && sums.contains(&third) {
                return true;
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let n = 2000;
    let mut seed: i64 = 548;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for g in 0..count {
        let spread = 1 + (g % 5 * 25) as i64;
        let mut a = Vec::new();
        for _ in 0..n {
            a.push(next_random(&mut seed) % (2 * spread + 1) - spread);
        }
        all.push(a);
    }
    let mut yes: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..20 {
        for g in 0..count {
            let i = (round * 31 + g * 7) % n;
            all[g][i] = -all[g][i];
            let bit = if split_array(&all[g]) { 1 } else { 0 };
            yes += bit;
            checksum = (checksum * 31 + bit + 7 * g as i64) % 1000000007;
        }
    }
    println!("{} arrays, 20 rounds each: {} can be split, checksum {}", count, yes, checksum);
}
