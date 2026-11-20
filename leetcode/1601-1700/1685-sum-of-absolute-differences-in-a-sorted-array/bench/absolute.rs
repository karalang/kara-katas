// LeetCode #1685: Sum of Absolute Differences in a Sorted Array -- the
// bench's Rust mirror: the ★ arm on 50 random sorted arrays of 100000
// values, all drawn first, each answered 20 times.

fn sum_differences(nums: &[i32]) -> Vec<i32> {
    let n = nums.len() as i64;
    let total: i32 = nums.iter().sum();
    let mut before: i32 = 0;
    let mut result = Vec::with_capacity(nums.len());
    for i in 0..n {
        let x = nums[i as usize];
        let after = (total - before - x) as i64;
        let x = x as i64;
        result.push((x * i - before as i64 + after - x * (n - 1 - i)) as i32);
        before += x as i32;
    }
    result
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let size = 100000;
    let rounds = 20;
    let mut seed = 1685;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i32> = (0..size).map(|_| (next_random(&mut seed) % 10000 + 1) as i32).collect();
        nums.sort();
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let answer = sum_differences(nums);
            let first = answer[0] as i64;
            let middle = answer[size / 2] as i64;
            let last = answer[size - 1] as i64;
            total += middle;
            check = (check * 31 + first + middle + last + r) % 1000000007;
        }
    }
    println!("{count} arrays of {size} values, {rounds} rounds: middles sum to {total}, checksum {check}");
}
