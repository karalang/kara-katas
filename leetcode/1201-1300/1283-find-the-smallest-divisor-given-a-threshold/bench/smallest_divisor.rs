// LeetCode #1283 bench, Rust: the same binary search, workload and
// checksum as smallest_divisor.kara.

fn total(nums: &[i32], d: i64) -> i64 {
    let mut sum = 0i64;
    for &x in nums {
        sum += (x as i64 + d - 1) / d;
    }
    sum
}

fn smallest_divisor(nums: &[i32], threshold: i32) -> i32 {
    let mut lo: i64 = 1;
    let mut hi = *nums.iter().max().unwrap() as i64;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if total(nums, mid) <= threshold as i64 {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo as i32
}

fn main() {
    let mut seed: i64 = 1283;
    let mut nums: Vec<i32> = Vec::new();
    for _ in 0..50000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        nums.push((1 + seed % 1000000) as i32);
    }
    let mut check: i64 = 0;
    for r in 0..150i64 {
        let threshold = 50000 + (check + r * 7919) % 950001;
        check = (check * 131 + smallest_divisor(&nums, threshold as i32) as i64) % 1000000007;
    }
    println!("150 rounds over 5 * 10^4 numbers: checksum {}", check);
}
