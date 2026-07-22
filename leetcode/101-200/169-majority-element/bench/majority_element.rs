// LeetCode 169 — Majority Element benchmark kernel (Rust mirror, rustc -O).
//
// Build-once + punch: LCG-filled N values with a 60% majority, Boyer-Moore scan
// run K times with a one-element perturbation each round. Sink = sum of the K
// results. Identical algorithm to the Kāra / C / Go / Python mirrors.

fn majority_element(nums: &[i64]) -> i64 {
    let mut candidate = nums[0];
    let mut count: i64 = 0;
    for &x in nums {
        if count == 0 {
            candidate = x;
        }
        if x == candidate {
            count += 1;
        } else {
            count -= 1;
        }
    }
    candidate
}

fn main() {
    let n: i64 = 10_000_000;
    let k: i64 = 20;
    let majority: i64 = 7;

    let mut nums = vec![0i64; n as usize];
    let mut state: i64 = 12345;
    for slot in nums.iter_mut() {
        state = (state * 1103515245 + 12345) % 2147483648;
        *slot = if state % 100 < 60 {
            majority
        } else {
            state % 1000000 + 1000
        };
    }

    let mut sink: i64 = 0;
    for round in 0..k {
        let idx = ((round * 7919) % n) as usize;
        nums[idx] += 1;
        sink += majority_element(&nums);
    }
    println!("{}", sink);
}
