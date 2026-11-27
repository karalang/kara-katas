// LeetCode #1787: Make the XOR of All Segments Equal to Zero -- the bench in
// Rust, mirroring min_changes.kara: a DP over the k groups of positions.
use std::collections::HashMap;

fn min_changes(nums: &[i32], k: i32) -> i32 {
    let mut best: Vec<i32> = vec![i32::MAX / 2; 1024];
    best[0] = 0;
    for g in 0..k as usize {
        let mut count: HashMap<i32, i32> = HashMap::new();
        let mut size: i32 = 0;
        let mut i = g;
        while i < nums.len() {
            *count.entry(nums[i]).or_insert(0) += 1;
            size += 1;
            i += k as usize;
        }
        let floor = best.iter().min().unwrap() + size;
        let mut next: Vec<i32> = vec![floor; 1024];
        for x in 0..1024usize {
            for (&v, &c) in count.iter() {
                let here = best[x ^ v as usize] + size - c;
                if here < next[x] {
                    next[x] = here;
                }
            }
        }
        best = next;
    }
    best[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1787;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..100 {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..600 {
            nums.push((next_random(&mut seed) % 1024) as i32);
        }
        lists.push(nums);
    }
    let mut check: i64 = 0;
    for call in 0..300i64 {
        let nums = &lists[((check + call) % 100) as usize];
        let k = 1 + (check * 7 + call) % 600;
        check = (check * 31 + min_changes(nums, k as i32) as i64) % 1000000007;
    }
    println!("300 calls over 100 lists: checksum {}", check);
}
