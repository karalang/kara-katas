// LeetCode #1748: Sum of Unique Elements -- the bench (unique.kara in
// Rust): one pass with a state per value.

fn sum_of_unique(nums: &[i32]) -> i32 {
    let mut seen = [0; 101];
    let mut sum: i32 = 0;
    for &x in nums.iter() {
        let i = x as usize;
        if seen[i] == 0 {
            sum += x;
        } else if seen[i] == 1 {
            sum -= x;
        }
        seen[i] = (seen[i] + 1).min(2);
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50000;
    let rounds: i64 = 10;
    let n = 100;
    let mut seed: i64 = 1748;
    let arrays: Vec<Vec<i32>> = (0..count).map(|_| (0..n).map(|_| (next_random(&mut seed) % 100 + 1) as i32).collect()).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let answer = sum_of_unique(nums) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: unique sums add to {}, checksum {}", count, n, rounds, sum, check);
}
