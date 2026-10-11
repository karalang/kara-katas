// Benchmark for #376 -- mirror of wiggle.kara.

fn wiggle_max_length(nums: &[i64]) -> i64 {
    if nums.is_empty() {
        return 0;
    }
    let mut up = 1;
    let mut down = 1;
    for i in 1..nums.len() {
        if nums[i] > nums[i - 1] {
            up = down + 1;
        } else if nums[i] < nums[i - 1] {
            down = up + 1;
        }
    }
    up.max(down)
}

fn main() {
    let mut seed: i64 = 376;
    let mut checksum: i64 = 0;
    let mut nums = vec![0i64; 1000];
    for case in 0..20000 {
        let top = if case % 3 == 0 { 6 } else { 1001 };
        for x in nums.iter_mut() {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            *x = (seed / 65536) % top;
        }
        checksum = (checksum * 1009 + wiggle_max_length(&nums)) % 1000000007;
    }
    println!("checksum {}", checksum);
}
