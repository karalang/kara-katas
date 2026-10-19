// LeetCode 805 -- Split Array With Same Average: the bench, mirroring
// split_array.kara with the same sums by size.
use std::collections::HashSet;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn split_array_same_average(nums: &[i64]) -> bool {
    let n = nums.len() as i64;
    let total: i64 = nums.iter().sum();
    let half = (n / 2) as usize;
    let mut sums: Vec<HashSet<i64>> = Vec::new();
    for _ in 0..half + 1 {
        sums.push(HashSet::new());
    }
    sums[0].insert(0);
    for &x in nums.iter() {
        let mut k = half;
        while k >= 1 {
            let before: Vec<i64> = sums[k - 1].iter().copied().collect();
            for s in before.iter() {
                sums[k].insert(s + x);
            }
            k -= 1;
        }
    }
    for k in 1..half as i64 + 1 {
        if total * k % n == 0 && sums[k as usize].contains(&(total * k / n)) {
            return true;
        }
    }
    false
}

fn main() {
    let mut seed: i64 = 805;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..16 {
        let mut nums: Vec<i64> = Vec::new();
        let mut sum = 0;
        for _ in 0..29 {
            let x = next_random(&mut seed) % 300;
            nums.push(x);
            sum += x;
        }
        let last = if a % 2 == 0 {
            next_random(&mut seed) % 300
        } else {
            (31 - sum % 30) % 30 + 30 * (next_random(&mut seed) % 9)
        };
        nums.push(last);
        arrays.push(nums);
    }
    let rounds: i64 = 400;
    let mut yes = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let can = split_array_same_average(&arrays[(r % 16) as usize]);
        if can {
            yes += 1;
        }
        check = (check * 131 + if can { 1 } else { 2 }) % 1000000007;
    }
    println!("{} rounds of 30 numbers: {} can be split, checksum {}", rounds, yes, check);
}
