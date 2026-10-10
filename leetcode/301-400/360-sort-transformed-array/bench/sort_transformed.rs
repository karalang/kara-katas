// Benchmark for #360 -- mirror of sort_transformed.kara.

fn f(x: i64, a: i64, b: i64, c: i64) -> i64 {
    a * x * x + b * x + c
}

fn sort_transformed_array(nums: &[i64], a: i64, b: i64, c: i64) -> Vec<i64> {
    let n = nums.len() as i64;
    let mut out = vec![0i64; nums.len()];
    let mut lo: i64 = 0;
    let mut hi: i64 = n - 1;
    if a >= 0 {
        let mut k = n - 1;
        while lo <= hi {
            let left = f(nums[lo as usize], a, b, c);
            let right = f(nums[hi as usize], a, b, c);
            if left >= right {
                out[k as usize] = left;
                lo += 1;
            } else {
                out[k as usize] = right;
                hi -= 1;
            }
            k -= 1;
        }
    } else {
        let mut k = 0;
        while lo <= hi {
            let left = f(nums[lo as usize], a, b, c);
            let right = f(nums[hi as usize], a, b, c);
            if left <= right {
                out[k as usize] = left;
                lo += 1;
            } else {
                out[k as usize] = right;
                hi -= 1;
            }
            k += 1;
        }
    }
    out
}

fn main() {
    let mut seed: i64 = 360;
    let mut checksum: i64 = 0;
    let mut nums = vec![0i64; 50000];
    for _ in 0..200 {
        let mut x: i64 = -1000000;
        for i in 0..50000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            x += (seed / 65536) % 81;
            nums[i] = x;
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let a = (seed / 65536) % 21 - 10;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let b = (seed / 65536) % 21 - 10;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let c = (seed / 65536) % 21 - 10;
        let out = sort_transformed_array(&nums, a, b, c);
        for &v in &out {
            checksum = (checksum * 31 + v % 1000000007 + 1000000007) % 1000000007;
        }
    }
    println!("checksum {}", checksum);
}
