// LeetCode #2520: Count the Digits That Divide a Number -- Rust mirror of
// the benchmark (digits.kara): the same numbers, passes, order and checksum.

fn count_digits(num: i64) -> i64 {
    let mut rest = num;
    let mut count = 0;
    while rest > 0 {
        if num % (rest % 10) == 0 {
            count += 1;
        }
        rest /= 10;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2520;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let length = next_random(&mut seed) % 9 + 1;
        let mut num = 0;
        for _ in 0..length {
            num = num * 10 + next_random(&mut seed) % 9 + 1;
        }
        nums.push(num);
    }
    let passes = 150;
    let mut check: i64 = 0;
    for p in 0..passes {
        let start = check % 100000;
        for i in 0..100000 {
            check = (check * 31 + count_digits(nums[((start + i) % 100000) as usize]) + p) % 1000000007;
        }
    }
    println!("{passes} passes over 100000 numbers: checksum {check}");
}
