// Benchmark for #413: mirror of arithmetic_slices.kara (slices ending
// here).

fn number_of_arithmetic_slices(nums: &[i64]) -> i64 {
    let mut ending = 0;
    let mut total = 0;
    for i in 2..nums.len() {
        if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2] {
            ending += 1;
            total += ending;
        } else {
            ending = 0;
        }
    }
    total
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(60000);
    let n: i64 = 5000;
    let mut seed: i64 = 413;
    let mut nums: Vec<i64> = vec![0];
    while (nums.len() as i64) < n {
        let mut diff = step(&mut seed) % 7 - 3;
        let run = 1 + step(&mut seed) % 30;
        for _ in 0..run {
            if (nums.len() as i64) < n {
                let last = nums[nums.len() - 1];
                if last + diff > 1000 || last + diff < -1000 {
                    diff = -diff;
                }
                nums.push(last + diff);
            }
        }
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        nums[(r * 7919 % n) as usize] += r % 3 - 1;
        let answer = number_of_arithmetic_slices(&nums);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    println!("{} rounds on {} numbers: total {}, checksum {}", rounds, n, total, checksum);
}
