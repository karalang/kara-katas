// LeetCode #704 bench: the ★ arm in Rust. See the .kara twin for the
// workload.

fn search(nums: &[i64], target: i64) -> i64 {
    let mut lo: i64 = 0;
    let mut hi: i64 = nums.len() as i64 - 1;
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        if nums[mid as usize] == target {
            return mid;
        }
        if nums[mid as usize] < target {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 704;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        let mut nums: Vec<i64> = Vec::new();
        let mut v: i64 = -9999;
        for _ in 0..10000 {
            nums.push(v);
            v += 1 + next_random(&mut seed) % 2;
        }
        arrays.push(nums);
    }
    let mut found: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..5 {
        for nums in arrays.iter() {
            for target in -9999..10000 {
                let at = search(nums, target);
                if at >= 0 {
                    found += 1;
                }
                checksum = (checksum * 31 + at + 1) % 1000000007;
            }
        }
    }
    println!("5 rounds of 100 arrays of 10000: {found} found, checksum {checksum}");
}
