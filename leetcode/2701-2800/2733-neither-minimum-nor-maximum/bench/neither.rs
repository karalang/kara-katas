// LeetCode #2733: Neither Minimum nor Maximum -- the bench (neither.kara
// in Rust): the least and the greatest in one pass, then the first number
// that is neither.

fn find_non_min_or_max(nums: &[i64]) -> i64 {
    let mut low = nums[0];
    let mut high = nums[0];
    for &x in nums.iter() {
        low = low.min(x);
        high = high.max(x);
    }
    for &x in nums.iter() {
        if x != low && x != high {
            return x;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 2000;
    let rounds = 3000;
    let mut seed: i64 = 2733;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let n = next_random(&mut seed) % 100 + 1;
        let mut all: Vec<i64> = (1..=100).collect();
        for i in (1..100i64).rev() {
            let j = next_random(&mut seed) % (i + 1);
            all.swap(i as usize, j as usize);
        }
        all.truncate(n as usize);
        arrays.push(all);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let answer = find_non_min_or_max(nums);
            sum += answer;
            check = (check * 31 + answer + 1 + r) % 1000000007;
        }
    }
    println!("{} arrays, {} rounds: answers sum to {}, checksum {}", count, rounds, sum, check);
}
