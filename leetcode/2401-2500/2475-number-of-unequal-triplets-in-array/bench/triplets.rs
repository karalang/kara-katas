// LeetCode #2475: Number of Unequal Triplets in Array -- the bench, the ★
// arm in Rust: a `HashMap` counts the values, and each value of count `c`
// is the middle of `left * c * right` triplets.
use std::collections::HashMap;

fn unequal_triplets(nums: &[i64]) -> i64 {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for &v in nums {
        *counts.entry(v).or_insert(0) += 1;
    }
    let n = nums.len() as i64;
    let mut left = 0;
    let mut total = 0;
    for &c in counts.values() {
        total += left * c * (n - left - c);
        left += c;
    }
    total
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 2000 lists of 100 values from 1 to 50 built once; then 600 passes,
    // each setting one value of every list from the checksum so far, then
    // answering it, folding the count plus the pass into the checksum
    let mut seed = 2475;
    let mut lists: Vec<Vec<i64>> =
        (0..2000).map(|_| (0..100).map(|_| 1 + next_random(&mut seed) % 50).collect()).collect();
    let mut check = 0i64;
    for p in 0..600i64 {
        for a in 0..lists.len() {
            lists[a][(check as usize + a) % 100] = 1 + check % 50;
            check = (check * 31 + unequal_triplets(&lists[a]) + p) % 1000000007;
        }
    }
    println!("600 passes over 2000 lists of 100: checksum {check}");
}
