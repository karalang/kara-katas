// LeetCode #2831: Find the Longest Equal Subarray -- the bench, mirrored
// from equal.kara: positions per value, then two pointers over each list.

fn longest_equal_subarray(nums: &[i64], k: i64) -> i64 {
    let n = nums.len();
    let mut places: Vec<Vec<i64>> = vec![Vec::new(); n + 1];
    for i in 0..n {
        places[nums[i] as usize].push(i as i64);
    }
    let mut best = 0;
    for pos in places.iter() {
        let mut l = 0usize;
        for r in 0..pos.len() {
            while pos[r] - pos[l] - (r - l) as i64 > k {
                l += 1;
            }
            best = best.max((r - l + 1) as i64);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds = 20;
    let n = 100000;
    let mut seed = 2831;
    let mut arrays: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..n).map(|_| next_random(&mut seed) % 1000 + 1).collect();
        let k = next_random(&mut seed) % 1001;
        arrays.push((nums, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in arrays.iter() {
            let a = longest_equal_subarray(nums, *k);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: lengths total {total}, checksum {check}");
}
