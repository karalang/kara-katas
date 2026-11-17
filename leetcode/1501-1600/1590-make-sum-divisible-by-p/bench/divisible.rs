// LeetCode #1590: Make Sum Divisible by P -- the bench in Rust, mirroring
// divisible.kara: the latest prefix with each remainder in a `HashMap`
// (SipHash, as Kāra's `Map`).

use std::collections::HashMap;

fn min_subarray(nums: &[i32], p: i32) -> i32 {
    let p = p as i64;
    let need = nums.iter().map(|&v| v as i64).sum::<i64>() % p;
    if need == 0 {
        return 0;
    }
    let mut last: HashMap<i64, i64> = HashMap::new();
    last.insert(0, -1);
    let mut prefix = 0i64;
    let n = nums.len() as i64;
    let mut best = n;
    for (j, &v) in nums.iter().enumerate() {
        let j = j as i64;
        prefix = (prefix + v as i64) % p;
        if let Some(&i) = last.get(&((prefix - need + p) % p)) {
            best = best.min(j - i);
        }
        last.insert(prefix, j);
    }
    if best == n { -1 } else { best as i32 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 1590;
    let mut problems = Vec::new();
    for _ in 0..40 {
        let nums: Vec<i32> = (0..100000).map(|_| (wide(&mut seed) % 1000000000 + 1) as i32).collect();
        let p = (wide(&mut seed) % 100000 + 1) as i32;
        problems.push((nums, p));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (nums, p) in &problems {
        let answer = min_subarray(nums, *p) as i64;
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    println!("40 problems of 100000 values: lengths {}, checksum {}", total, check);
}
