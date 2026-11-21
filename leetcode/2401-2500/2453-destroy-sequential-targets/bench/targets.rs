// LeetCode #2453: Destroy Sequential Targets -- bench, Rust mirror of
// targets.kara: a HashMap counts each residue class, and a second pass
// keeps the least value of a largest class.

use std::collections::HashMap;

fn destroy_targets(nums: &[i64], space: i64) -> i64 {
    let mut count: HashMap<i64, i64> = HashMap::new();
    for &x in nums {
        *count.entry(x % space).or_insert(0) += 1;
    }
    let mut best = 0;
    let mut answer = 0;
    for &x in nums {
        let c = count[&(x % space)];
        if c > best || (c == best && x < answer) {
            best = c;
            answer = x;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100000;
    let mut seed: i64 = 2453;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            let hi = next_random(&mut seed);
            nums.push(1 + (hi * 32768 + next_random(&mut seed)) % 1000000000);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..50i64 {
        for a in 0..10i64 {
            arrays[a as usize][((p * 7919 + a) % n) as usize] = 1 + check % 1000000000;
            let space = 1 + (p * 7919 + a * 104729) % 100000;
            check = (check * 31 + destroy_targets(&arrays[a as usize], space) + p) % 1000000007;
        }
    }
    println!("50 passes over 10 arrays of 10^5 values: checksum {}", check);
}
