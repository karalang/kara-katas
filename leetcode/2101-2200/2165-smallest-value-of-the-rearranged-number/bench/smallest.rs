// LeetCode #2165: Smallest Value of the Rearranged Number -- the
// benchmark's Rust mirror of smallest.kara.

fn smallest_number(num: i64) -> i64 {
    let mut digits: Vec<i64> = num.abs().to_string().chars().map(|c| c.to_digit(10).unwrap() as i64).collect();
    if num < 0 {
        digits.sort_by(|a, b| b.cmp(a));
    } else {
        digits.sort();
        if let Some(first) = digits.iter().position(|&d| d != 0) {
            digits.swap(0, first);
        }
    }
    let size = digits.iter().fold(0i64, |n, d| n * 10 + d);
    if num < 0 { -size } else { size }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2165i64;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..1000 {
        let length = next_random(&mut seed) % 14 + 1;
        let mut num = 0i64;
        for _ in 0..length {
            num = num * 10 + next_random(&mut seed) % 10;
        }
        if next_random(&mut seed) % 2 == 1 {
            num = -num;
        }
        nums.push(num);
    }
    let mut check = 0i64;
    for _ in 0..1000 {
        for k in 0..1000 {
            nums[k] = nums[k] + next_random(&mut seed) % 2001 - 1000;
            let s = smallest_number(nums[k]);
            check = (check * 31 + s % 1000000007 + 1000000007) % 1000000007;
        }
    }
    println!("1000000 solves: checksum {}", check);
}
