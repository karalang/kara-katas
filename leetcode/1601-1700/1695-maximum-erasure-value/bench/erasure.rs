// LeetCode #1695: Maximum Erasure Value -- the bench's Rust mirror: the ★
// arm on 50 random arrays of 100000 values up to 10^4, all drawn first,
// each answered 60 times.

fn maximum_unique_subarray(nums: &[i32]) -> i32 {
    let mut last: Vec<i64> = vec![-1; 10001];
    let mut prefix: Vec<i32> = vec![0; nums.len() + 1];
    let mut start: i64 = 0;
    let mut best = 0;
    for (i, &v) in nums.iter().enumerate() {
        prefix[i + 1] = prefix[i] + v;
        start = start.max(last[v as usize] + 1);
        last[v as usize] = i as i64;
        best = best.max(prefix[i + 1] - prefix[start as usize]);
    }
    best
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds = 60;
    let n = 100000;
    let mut seed = 1695;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push((next_random(&mut seed) % 10000 + 1) as i32);
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let answer = maximum_unique_subarray(nums) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n} values, {rounds} rounds: answers sum to {total}, checksum {check}");
}
