// Benchmark for #645: mirror of set_mismatch.kara (the ★ arm: counting
// each value) on the same workload.

fn find_error_nums(nums: &[i64]) -> [i64; 2] {
    let n = nums.len();
    let mut seen = vec![0i64; n + 1];
    for x in nums.iter() {
        seen[*x as usize] += 1;
    }
    let mut twice = 0;
    let mut missing = 0;
    for v in 1..n + 1 {
        if seen[v] == 2 {
            twice = v as i64;
        } else if seen[v] == 0 {
            missing = v as i64;
        }
    }
    [twice, missing]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mismatched(n: i64, seed: &mut i64) -> Vec<i64> {
    let mut nums: Vec<i64> = (1..n + 1).collect();
    for i in 0..n - 1 {
        let j = i + next_random(seed) % (n - i);
        nums.swap(i as usize, j as usize);
    }
    let from = next_random(seed) % n;
    let mut to = next_random(seed) % (n - 1);
    if to >= from {
        to += 1;
    }
    nums[to as usize] = nums[from as usize];
    nums
}

fn main() {
    let mut seed: i64 = 645;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        arrays.push(mismatched(100000, &mut seed));
    }
    let rounds: i64 = 2000;
    let mut twice_sum: i64 = 0;
    let mut missing_sum: i64 = 0;
    for r in 0..rounds {
        let got = find_error_nums(&arrays[(r % 20) as usize]);
        twice_sum += got[0];
        missing_sum += got[1];
    }
    println!("{} rounds over 20 arrays of 100000 values: copies add to {}, missing values to {}", rounds, twice_sum, missing_sum);
}
