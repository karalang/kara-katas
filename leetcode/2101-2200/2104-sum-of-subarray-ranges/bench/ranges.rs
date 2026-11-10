// LeetCode #2104: Sum of Subarray Ranges -- bench, Rust mirror of
// ranges.kara.

fn sub_array_ranges(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut sum = 0i64;
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..=n {
        while let Some(&top) = stack.last() {
            if !(i == n || nums[top] < nums[i]) {
                break;
            }
            stack.pop();
            let left = stack.last().map_or(-1, |&l| l as i64);
            sum += nums[top] * (top as i64 - left) * (i - top) as i64;
        }
        stack.push(i);
    }
    stack.clear();
    for i in 0..=n {
        while let Some(&top) = stack.last() {
            if !(i == n || nums[top] > nums[i]) {
                break;
            }
            stack.pop();
            let left = stack.last().map_or(-1, |&l| l as i64);
            sum -= nums[top] * (top as i64 - left) * (i - top) as i64;
        }
        stack.push(i);
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2104;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let mut nums = Vec::with_capacity(1000);
        for _ in 0..1000 {
            nums.push(wide_random(&mut seed) % 2000000001 - 1000000000);
        }
        arrays.push(nums);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..10 {
        for nums in &arrays {
            let got = sub_array_ranges(nums) % 1000000007;
            total = (total + got) % 1000000007;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("10000 arrays: total {}, checksum {}", total, check);
}
