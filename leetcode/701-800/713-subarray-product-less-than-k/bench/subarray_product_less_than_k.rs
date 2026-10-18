// LeetCode #713: Subarray Product Less Than K -- a sliding window.
// Benchmark mirror of the Kara star arm: extend the window right; while
// its product is k or more, drop numbers from the left; count the
// subarrays ending at each right end.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn num_subarray_product_less_than_k(nums: &[i64], k: i64) -> i64 {
    if k <= 1 {
        return 0;
    }
    let mut product = 1;
    let mut left = 0;
    let mut count = 0;
    for right in 0..nums.len() {
        product *= nums[right];
        while product >= k {
            product /= nums[left];
            left += 1;
        }
        count += (right - left + 1) as i64;
    }
    count
}

fn main() {
    let mut seed: i64 = 713;
    let tops = [2, 3, 5, 10, 20, 50, 100, 200, 500, 1000];
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for t in tops.iter() {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..30000 {
            nums.push(1 + next_random(&mut seed) % t);
        }
        arrays.push(nums);
    }
    let mut sum: i64 = 0;
    for _ in 0..200 {
        for nums in arrays.iter() {
            sum += num_subarray_product_less_than_k(nums, 1000000);
        }
    }
    println!("200 rounds of 10 arrays of 30000, k = 1000000: sum {}", sum);
}
