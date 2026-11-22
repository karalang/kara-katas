// LeetCode #2740: Find the Value of the Partition -- the bench
// (partition.kara in Rust): sort a copy, and the least gap between
// neighbours.

fn find_value_of_partition(mut nums: Vec<i64>) -> i64 {
    nums.sort();
    let mut best = i64::MAX;
    for i in 1..nums.len() {
        best = best.min(nums[i] - nums[i - 1]);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let n = 100000;
    let rounds: i64 = 10;
    let mut seed = 2740;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            nums.push((hi * 32768 + lo) % 1000000000 + 1);
        }
        arrays.push(nums);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let value = find_value_of_partition(nums.clone());
            sum += value;
            check = (check * 31 + value + r) % 1000000007;
        }
    }
    println!("{} arrays of {} numbers, {} rounds: values sum to {}, checksum {}", count, n, rounds, sum, check);
}
