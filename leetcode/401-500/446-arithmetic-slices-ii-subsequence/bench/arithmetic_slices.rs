// Benchmark for #446: mirror of arithmetic_slices.kara (a map of
// differences per index) on 20 random arrays of 1,000 values from -500
// to 499, built once. `HashMap` with its default SipHash, as Kāra's
// `Map` hashes with SipHash-1-3.
use std::collections::HashMap;

fn number_of_arithmetic_slices(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut ending: Vec<HashMap<i64, i64>> = Vec::new();
    let mut total = 0;
    for i in 0..n {
        let mut here: HashMap<i64, i64> = HashMap::new();
        for j in 0..i {
            let d = nums[i] - nums[j];
            let before = *ending[j].get(&d).unwrap_or(&0);
            total += before;
            *here.entry(d).or_insert(0) += before + 1;
        }
        ending.push(here);
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let n = 1000;
    let mut seed: i64 = 446;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            nums.push(next_random(&mut seed) % 1000 - 500);
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for nums in &arrays {
        let answer = number_of_arithmetic_slices(nums);
        total += answer;
        checksum = (checksum * 31 + answer % 1000000007) % 1000000007;
    }
    println!("{count} arrays of {n}: {total} slices, checksum {checksum}");
}
