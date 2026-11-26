// LeetCode #1799: Maximize Score After N Operations -- the bench in Rust:
// the ★ arm over 100 random lists of 14 numbers built once, 100 calls.

fn gcd(a: i32, b: i32) -> i32 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn max_score(nums: &[i32]) -> i32 {
    let m = nums.len() as i64;
    let full: i64 = 1 << m;
    let mut best: Vec<i32> = vec![0; full as usize];
    for mask in 0..full {
        let taken = mask.count_ones() as i64;
        if taken % 2 == 1 {
            continue;
        }
        let op = (taken / 2 + 1) as i32;
        for i in 0..m {
            if mask >> i & 1 == 1 {
                continue;
            }
            for j in i + 1..m {
                if mask >> j & 1 == 1 {
                    continue;
                }
                let next = (mask | 1 << i | 1 << j) as usize;
                best[next] = best[next].max(best[mask as usize] + op * gcd(nums[i as usize], nums[j as usize]));
            }
        }
    }
    best[(full - 1) as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1799;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..100 {
        let nums: Vec<i32> = (0..14).map(|_| (1 + next_random(&mut seed) % 1000000) as i32).collect();
        lists.push(nums);
    }
    let mut check: i64 = 0;
    for call in 0..100i64 {
        let nums = &lists[((check + call) % 100) as usize];
        check = (check * 31 + max_score(nums) as i64) % 1000000007;
    }
    println!("100 calls over 100 lists of 14 numbers: checksum {}", check);
}
