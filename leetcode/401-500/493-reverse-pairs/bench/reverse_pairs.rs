// Benchmark for #493: Rust mirror of the ★ arm (merge sort); see
// reverse_pairs.kara.

fn sort_count(nums: &mut Vec<i64>, low: usize, high: usize) -> i64 {
    if high - low <= 1 {
        return 0;
    }
    let mid = (low + high) / 2;
    let mut count = sort_count(nums, low, mid) + sort_count(nums, mid, high);
    let mut j = mid;
    for i in low..mid {
        while j < high && nums[i] > 2 * nums[j] {
            j += 1;
        }
        count += (j - mid) as i64;
    }
    let mut merged: Vec<i64> = Vec::new();
    let mut a = low;
    let mut b = mid;
    while a < mid || b < high {
        if b == high || (a < mid && nums[a] <= nums[b]) {
            merged.push(nums[a]);
            a += 1;
        } else {
            merged.push(nums[b]);
            b += 1;
        }
    }
    for k in 0..merged.len() {
        nums[low + k] = merged[k];
    }
    count
}

fn reverse_pairs(nums: &[i64]) -> i64 {
    let mut work = nums.to_vec();
    let n = work.len();
    sort_count(&mut work, 0, n)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 60 arrays of 50,000 numbers across the whole 32-bit range, built
    // once, then each counted once.
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut seed: i64 = 493;
    for _ in 0..60 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..50000 {
            let high = next_random(&mut seed);
            nums.push(high * 131072 + next_random(&mut seed) * 4 - 2147483648);
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for nums in &arrays {
        let pairs = reverse_pairs(nums);
        total += pairs;
        checksum = (checksum * 31 + pairs) % 1000000007;
    }
    println!("60 arrays of 50000: {total} reverse pairs, checksum {checksum}");
}
