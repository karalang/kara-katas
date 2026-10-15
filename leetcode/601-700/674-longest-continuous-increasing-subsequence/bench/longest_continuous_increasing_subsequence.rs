// Benchmark for #674: one pass with a running length, as the Kara ★
// arm.

fn find_length_of_lcis(nums: &[i64]) -> i64 {
    let mut best = 0;
    let mut run = 0;
    for i in 0..nums.len() {
        if i > 0 && nums[i - 1] < nums[i] {
            run += 1;
        } else {
            run = 1;
        }
        best = best.max(run);
    }
    best
}

fn main() {
    let arrays: i64 = 100;
    let size: i64 = 10000;
    let rounds: i64 = 20000;
    let mut seed: i64 = 674;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..arrays {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..size {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            nums.push(seed / 65536 % 1000);
        }
        all.push(nums);
    }
    let mut sum: i64 = 0;
    for r in 0..rounds {
        let a = (r % arrays) as usize;
        all[a][(r * 7919 % size) as usize] = r % 1000;
        sum = (sum * 31 + find_length_of_lcis(&all[a])) % 1000000007;
    }
    println!("{} rounds over {} arrays of {}: checksum {}", rounds, arrays, size, sum);
}
