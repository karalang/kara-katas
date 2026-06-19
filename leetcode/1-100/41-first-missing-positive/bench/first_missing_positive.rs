// LeetCode #41 bench mirror — Rust, the in-place cyclic-sort solver (★).
//
// Mirrors bench/first_missing_positive.kara exactly: swap each in-range value to its home
// index v-1, then scan for the first slot not holding its home value. The buffer is
// allocated once and overwritten in place each iteration with a k-rotated permutation of
// 1..N plus a punched-out gap; fold each answer into a rolling checksum. Same workload +
// sink as every other mirror.

fn first_missing_positive(nums: &mut [i64], n: i64) -> i64 {
    let mut i = 0i64;
    while i < n {
        let v = nums[i as usize];
        if v >= 1 && v <= n && nums[(v - 1) as usize] != v {
            let t = nums[(v - 1) as usize];
            nums[(v - 1) as usize] = v;
            nums[i as usize] = t;
        } else {
            i += 1;
        }
    }
    let mut j = 0i64;
    while j < n {
        if nums[j as usize] != j + 1 {
            return j + 1;
        }
        j += 1;
    }
    n + 1
}

fn main() {
    let total: i64 = 200000;
    let n: i64 = 100;
    let modulus: i64 = 1000000007;

    let mut nums: Vec<i64> = vec![0; n as usize];

    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        let rot = k % n;
        let mut i = 0i64;
        while i < n {
            nums[i as usize] = ((i + rot) % n) + 1;
            i += 1;
        }
        nums[(k % n) as usize] = n + 7;

        let ans = first_missing_positive(&mut nums, n);
        acc = (acc * 131 + ans) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
