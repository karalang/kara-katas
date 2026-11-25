// LeetCode #1390 bench, Rust mirror of the ★ arm.

fn sum_four_divisors(nums: &[i32]) -> i32 {
    let mut total: i32 = 0;
    for &v in nums {
        let mut count = 0;
        let mut sum: i32 = 0;
        let mut d: i32 = 1;
        while d * d <= v && count <= 4 {
            if v % d == 0 {
                count += 1;
                sum += d;
                if d * d != v {
                    count += 1;
                    sum += v / d;
                }
            }
            d += 1;
        }
        if count == 4 {
            total += sum;
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 10000;
    let mut seed: i64 = 1390;
    let mut nums: Vec<i32> = Vec::new();
    for _ in 0..n {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        nums.push((1 + (a * 32768 + b) % 100000) as i32);
    }
    let mut check: i64 = 0;
    for _ in 0..300 {
        seed = (seed + check) % 2147483648;
        let i = next_random(&mut seed) % n;
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        nums[i as usize] = (1 + (a * 32768 + b) % 100000) as i32;
        check = (check * 131 + sum_four_divisors(&nums) as i64) % 1000000007;
    }
    println!("300 rounds over 10^4 values up to 10^5: checksum {}", check);
}
