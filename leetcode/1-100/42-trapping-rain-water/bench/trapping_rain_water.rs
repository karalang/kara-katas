// LeetCode #42 bench mirror — Rust, the converging two-pointer solver (★).
//
// Mirrors bench/trapping_rain_water.kara exactly: advance the shorter outer wall, settling
// each column with its running max. The buffer is allocated once and overwritten in place
// each iteration with a k-dependent jagged terrain; fold each answer into a rolling checksum.
// Same workload + sink as every other mirror.

fn trap(height: &[i64], n: i64) -> i64 {
    let mut left = 0i64;
    let mut right = n - 1;
    let mut left_max = 0i64;
    let mut right_max = 0i64;
    let mut water = 0i64;
    while left < right {
        if height[left as usize] < height[right as usize] {
            if height[left as usize] >= left_max {
                left_max = height[left as usize];
            } else {
                water += left_max - height[left as usize];
            }
            left += 1;
        } else {
            if height[right as usize] >= right_max {
                right_max = height[right as usize];
            } else {
                water += right_max - height[right as usize];
            }
            right -= 1;
        }
    }
    water
}

fn main() {
    let total: i64 = 200000;
    let n: i64 = 1000;
    let modulus: i64 = 1000000007;

    let mut height: Vec<i64> = vec![0; n as usize];
    let mut i = 0i64;
    while i < n {
        height[i as usize] = (i * 37) % 100;
        i += 1;
    }

    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        height[(k % n) as usize] = (k * 19) % 100;
        let ans = trap(&height, n);
        acc = (acc * 131 + ans) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
