// LeetCode #1760: Minimum Limit of Balls in a Bag -- the bench in Rust,
// mirroring minimum_size.kara: a binary search on the penalty.
fn operations(nums: &[i32], penalty: i64) -> i64 {
    nums.iter().map(|&x| (x - 1) as i64 / penalty).sum()
}

fn minimum_size(nums: &[i32], max_operations: i32) -> i32 {
    let mut lo: i32 = 1;
    let mut hi = *nums.iter().max().unwrap();
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if operations(nums, mid as i64) <= max_operations as i64 {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    let mut seed: i64 = 1760;
    let mut bags: Vec<i32> = Vec::new();
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        bags.push((1 + (high * 32768 + seed / 65536) % 1000000000) as i32);
    }
    let mut check: i64 = 0;
    for call in 0..100i64 {
        let at = ((check + call * 7919) % 100000) as usize;
        bags[at] = (1 + (check * 13 + call) % 1000000000) as i32;
        let ops = 1 + (check + call * 104729) % 1000000000;
        check = (check * 31 + minimum_size(&bags, ops as i32) as i64) % 1000000007;
    }
    println!("100 calls over 100000 bags: checksum {}", check);
}
