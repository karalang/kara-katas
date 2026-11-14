// LeetCode #2134: Minimum Swaps to Group All 1's Together II -- the
// benchmark, the same algorithm as swaps.kara.

fn min_swaps(nums: &[i64]) -> i64 {
    let n = nums.len();
    let k = nums.iter().sum::<i64>() as usize;
    let mut inside = 0i64;
    for i in 0..k {
        inside += nums[i];
    }
    let mut most = inside;
    for i in k..n + k {
        inside += nums[i % n] - nums[(i - k) % n];
        most = most.max(inside);
    }
    k as i64 - most
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2134i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..20i64 {
        let mut nums = Vec::with_capacity(100000);
        for _ in 0..100000 {
            nums.push(if next_random(&mut seed) % (a + 2) == 0 { 1 } else { 0 });
        }
        arrays.push(nums);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..10i64 {
        for a in 0..20 {
            let at = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000) as usize;
            arrays[a][at] = 1 - arrays[a][at];
            let swaps = min_swaps(&arrays[a]);
            total += swaps;
            check = (check * 31 + swaps + round) % 1000000007;
        }
    }
    println!("200 solves: {} swaps in all, checksum {}", total, check);
}
