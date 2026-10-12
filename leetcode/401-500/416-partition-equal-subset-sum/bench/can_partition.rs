// LeetCode #416: Partition Equal Subset Sum -- Rust mirror of
// can_partition.kara (sums up to half).

fn can_partition(nums: &[i64]) -> bool {
    let mut total = 0;
    for &x in nums {
        total += x;
    }
    if total % 2 != 0 {
        return false;
    }
    let half = total / 2;
    let mut reach = vec![false; (half + 1) as usize];
    reach[0] = true;
    for &x in nums {
        let mut s = half;
        while s >= x {
            if reach[(s - x) as usize] {
                reach[s as usize] = true;
            }
            s -= 1;
        }
    }
    reach[half as usize]
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 200;
    let rounds: i64 = 2000;
    let mut seed: i64 = 416;
    let mut nums: Vec<i64> = Vec::new();
    let mut total = 0;
    for _ in 0..n {
        let x = 1 + step(&mut seed) % 100;
        nums.push(x);
        total += x;
    }
    if total % 2 != 0 {
        nums[0] += if nums[0] < 100 { 1 } else { -1 };
    }
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let i = (step(&mut seed) % n) as usize;
        let j = (step(&mut seed) % n) as usize;
        if nums[i] < 100 && nums[j] > 1 {
            nums[i] += 1;
            nums[j] -= 1;
        }
        let answer = can_partition(&nums);
        if answer {
            yes += 1;
        }
        checksum = (checksum * 31 + nums[i] + if answer { r } else { 0 }) % 1000000007;
    }
    println!("{rounds} rounds on {n} numbers: {yes} can be split, checksum {checksum}");
}
