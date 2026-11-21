// LeetCode #2460: Apply Operations to an Array -- the bench, the ★ arm in
// Rust: the operations in place, then the nonzero values moved forward by
// a write index and the rest filled with zeros.

fn apply_operations(mut nums: Vec<i64>) -> Vec<i64> {
    let n = nums.len();
    for i in 0..n - 1 {
        if nums[i] == nums[i + 1] {
            nums[i] *= 2;
            nums[i + 1] = 0;
        }
    }
    let mut k = 0;
    for i in 0..n {
        if nums[i] != 0 {
            nums[k] = nums[i];
            k += 1;
        }
    }
    for i in k..n {
        nums[i] = 0;
    }
    nums
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 1000 arrays of 2000 values from 0 to 3 built once; then 24 passes,
    // each setting one value of every array from the checksum so far,
    // then answering every array on a copy and folding every value of
    // the answer, plus the pass, into the checksum
    let mut seed = 2460;
    let mut arrays: Vec<Vec<i64>> = (0..1000).map(|_| (0..2000).map(|_| next_random(&mut seed) % 4).collect()).collect();
    let mut check = 0i64;
    for p in 0..24i64 {
        for a in 0..arrays.len() {
            arrays[a][((check + a as i64) % 2000) as usize] = check % 4;
            for v in apply_operations(arrays[a].clone()) {
                check = (check * 31 + v + p) % 1000000007;
            }
        }
    }
    println!("24 passes over 1000 arrays of 2000: checksum {check}");
}
