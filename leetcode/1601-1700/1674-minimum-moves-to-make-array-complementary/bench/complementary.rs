// LeetCode #1674: Minimum Moves to Make Array Complementary -- the bench's
// Rust mirror: the ★ arm on 100 arrays of 100000 values with limits up to
// 100000, all drawn first, each answered 20 times.

fn min_moves(nums: &[i32], limit: i32) -> i32 {
    let n = nums.len();
    let limit = limit as i64;
    let mut delta = vec![0i64; (2 * limit + 2) as usize];
    for i in 0..n / 2 {
        let a = nums[i].min(nums[n - 1 - i]) as i64;
        let b = nums[i].max(nums[n - 1 - i]) as i64;
        delta[2] += 2;
        delta[(a + 1) as usize] -= 1;
        delta[(a + b) as usize] -= 1;
        delta[(a + b + 1) as usize] += 1;
        delta[(b + limit + 1) as usize] += 1;
    }
    let mut best = n as i64;
    let mut moves = 0i64;
    for sum in 2..=2 * limit {
        moves += delta[sum as usize];
        best = best.min(moves);
    }
    best as i32
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays = 100;
    let n = 100000;
    let rounds: i64 = 20;
    let mut seed: i64 = 1674;
    let mut cases: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..arrays {
        let limit = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push(((next_random(&mut seed) * 32768 + next_random(&mut seed)) % limit + 1) as i32);
        }
        cases.push((nums, limit as i32));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, limit) in &cases {
            let moves = min_moves(nums, *limit) as i64;
            total += moves;
            check = (check * 31 + moves + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: {} moves, checksum {}", arrays, n, rounds, total, check);
}
