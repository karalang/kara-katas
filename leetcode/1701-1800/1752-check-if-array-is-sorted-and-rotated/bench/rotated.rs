// LeetCode #1752: Check if Array Is Sorted and Rotated -- the bench
// (rotated.kara in Rust): count the drops.

fn check_rotated(nums: &[i32]) -> bool {
    let drops = nums.windows(2).filter(|w| w[0] > w[1]).count();
    let wrap = if nums[nums.len() - 1] > nums[0] { 1 } else { 0 };
    drops + wrap <= 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds: i64 = 5;
    let n = 100;
    let mut seed: i64 = 1752;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i32> = (0..n).map(|_| (next_random(&mut seed) % 100 + 1) as i32).collect();
        if next_random(&mut seed) % 2 == 0 {
            nums.sort();
            let k = (next_random(&mut seed) % n) as usize;
            nums.rotate_left(k);
        }
        arrays.push(nums);
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let answer = check_rotated(nums);
            if answer {
                yes += 1;
            }
            check = (check * 31 + if answer { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: {} sorted and rotated, checksum {}", count, n, rounds, yes, check);
}
