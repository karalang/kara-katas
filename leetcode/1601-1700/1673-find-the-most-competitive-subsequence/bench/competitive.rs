// LeetCode #1673: Find the Most Competitive Subsequence -- the bench's Rust
// mirror: the ★ arm on 50 arrays of 100000 values up to 10^9, each with a
// random k, all drawn first, each answered 20 times.

fn most_competitive(nums: &[i32], k: i32) -> Vec<i32> {
    let n = nums.len() as i64;
    let k = k as i64;
    let mut stack: Vec<i32> = Vec::new();
    for i in 0..n {
        let x = nums[i as usize];
        while let Some(&top) = stack.last() {
            if top > x && stack.len() as i64 - 1 + n - i >= k {
                stack.pop();
            } else {
                break;
            }
        }
        if (stack.len() as i64) < k {
            stack.push(x);
        }
    }
    stack
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays = 50;
    let n: i64 = 100000;
    let rounds: i64 = 20;
    let mut seed: i64 = 1673;
    let mut cases: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..arrays {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push(((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000) as i32);
        }
        let k = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % n + 1) as i32;
        cases.push((nums, k));
    }
    let mut chosen: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in &cases {
            let answer = most_competitive(nums, *k);
            chosen += answer.len() as i64;
            check = (check * 31 + answer[0] as i64 + answer[answer.len() - 1] as i64 + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: {} chosen, checksum {}", arrays, n, rounds, chosen, check);
}
