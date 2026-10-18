// LeetCode #718: Maximum Length of Repeated Subarray -- one rolling row.
// Benchmark mirror of the Kara star arm: the length of the common run
// ending at each pair of places, one row at a time, walked downwards.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn find_length(nums1: &[i64], nums2: &[i64]) -> i64 {
    let m = nums1.len();
    let n = nums2.len();
    let mut run = vec![0i64; n + 1];
    let mut best = 0;
    for i in 1..m + 1 {
        let mut j = n;
        while j >= 1 {
            if nums1[i - 1] == nums2[j - 1] {
                run[j] = run[j - 1] + 1;
                if run[j] > best {
                    best = run[j];
                }
            } else {
                run[j] = 0;
            }
            j -= 1;
        }
    }
    best
}

fn main() {
    let mut seed: i64 = 718;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..60 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..1000 {
            nums.push(next_random(&mut seed) % 10);
        }
        arrays.push(nums);
    }
    let mut sum = 0;
    for round in 0..40 {
        for k in 0..20 {
            sum += find_length(&arrays[k], &arrays[(k + round + 1) % 60]);
        }
    }
    println!("40 rounds of 20 pairs of 1000 numbers: sum {}", sum);
}
