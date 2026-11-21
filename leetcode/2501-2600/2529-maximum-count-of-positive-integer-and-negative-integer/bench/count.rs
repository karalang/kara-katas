// LeetCode #2529: Maximum Count of Positive Integer and Negative Integer
// -- Rust mirror of the benchmark (count.kara): the same lists, passes,
// order and checksum.

fn first_where(nums: &[i64], above: i64) -> i64 {
    let mut lo = 0;
    let mut hi = nums.len() as i64;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if nums[mid as usize] > above {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn maximum_count(nums: &[i64]) -> i64 {
    let negatives = first_where(nums, -1);
    let positives = nums.len() as i64 - first_where(nums, 0);
    negatives.max(positives)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2529;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let shift = next_random(&mut seed) % 4001 - 2000;
        let mut nums: Vec<i64> = (0..2000).map(|_| (next_random(&mut seed) % 4001 - 2000 + shift).max(-2000).min(2000)).collect();
        nums.sort();
        lists.push(nums);
    }
    let passes = 3000;
    let mut check: i64 = 0;
    for p in 0..passes {
        let start = check % 1000;
        for i in 0..1000 {
            check = (check * 31 + maximum_count(&lists[((start + i) % 1000) as usize]) + p) % 1000000007;
        }
    }
    println!("{passes} passes over 1000 lists of 2000 numbers: checksum {check}");
}
