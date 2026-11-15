// benchmark's Rust mirror of hills.kara (LeetCode #2210, the ★ arm): one
// pass keeping the last number that differs from the current one, a run
// counted once, at its end.

fn count_hill_valley(nums: &[i64]) -> i64 {
    let mut count = 0;
    let mut left = nums[0];
    for i in 1..nums.len() - 1 {
        if nums[i] == nums[i + 1] {
            continue;
        }
        let right = nums[i + 1];
        if (nums[i] > left && nums[i] > right) || (nums[i] < left && nums[i] < right) {
            count += 1;
        }
        if nums[i] != left {
            left = nums[i];
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2210;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..2000 {
        let top = [3, 10, 100][a % 3];
        let mut nums = Vec::new();
        for _ in 0..100 {
            nums.push(next_random(&mut seed) % top + 1);
        }
        arrays.push(nums);
    }
    // every array counted once per pass
    let mut check: i64 = 0;
    for p in 0..100 {
        for nums in &arrays {
            check = (check * 31 + count_hill_valley(nums) + p) % 1000000007;
        }
    }
    println!("100 passes over 2000 arrays: checksum {check}");
}
