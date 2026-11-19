// LeetCode #2334: Subarray With Elements Greater Than Varying Threshold --
// the bench, the ★ arm in Rust: the nearest smaller element on either
// side from a monotonic stack, and the widest run whose least element
// times its width exceeds the threshold.

fn valid_subarray_size(nums: &[i64], threshold: i64) -> i64 {
    let n = nums.len();
    let mut left = vec![-1i64; n];
    let mut right = vec![n as i64; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..n {
        while let Some(&top) = stack.last() {
            if nums[top] < nums[i] {
                break;
            }
            right[top] = i as i64;
            stack.pop();
        }
        if let Some(&top) = stack.last() {
            left[i] = top as i64;
        }
        stack.push(i);
    }
    let mut best = -1i64;
    for i in 0..n {
        let width = right[i] - left[i] - 1;
        if nums[i] * width > threshold {
            best = best.max(width);
        }
    }
    best
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let arrays: Vec<Vec<i64>> = (0..10i64)
        .map(|a| (0..100000i64).map(|i| scrambled(a * 100000 + i) % 1000000000 + 1).collect())
        .collect();
    let mut check = 0i64;
    for p in 0..5i64 {
        for a in 0..10i64 {
            let threshold = ((10 * a + p) * 7919 % 1000 + 1) * 1000000;
            check = (check * 31 + valid_subarray_size(&arrays[a as usize], threshold) + 1) % 1000000007;
        }
    }
    println!("5 passes over 10 arrays of 10^5 values: checksum {}", check);
}
