// Benchmark for #525: Rust mirror of the ★ arm (first index of each
// balance); see find_max_length.kara. `HashMap` with its default hasher,
// a fresh one for every call, as the ★ arm's `Map`.
use std::collections::HashMap;

fn find_max_length(nums: &[i64]) -> i64 {
    let mut first: HashMap<i64, i64> = HashMap::new();
    first.insert(0, -1);
    let mut balance = 0;
    let mut best = 0;
    for i in 0..nums.len() as i64 {
        balance += if nums[i as usize] == 1 { 1 } else { -1 };
        match first.get(&balance) {
            Some(j) => best = best.max(i - *j),
            None => {
                first.insert(balance, i);
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 525;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..20 {
        let q = 2 + a % 3;
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            nums.push(if next_random(&mut seed) % q == 0 { 1 } else { 0 });
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..20 {
        for a in 0..arrays.len() {
            let answer = find_max_length(&arrays[a]);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    println!("20 arrays of 100000, 20 rounds: total {}, checksum {}", total, checksum);
}
