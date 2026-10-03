// Benchmark workload for LeetCode #330 — mirrors patching_array.kara.

const LEN: i64 = 100000;
const PUNCHES: i64 = 1500;
const MODULUS: i64 = 1073741789;

fn min_patches(nums: &[i64], n: i64) -> i64 {
    let mut miss = 1;
    let mut i = 0;
    let mut patches = 0;
    while miss <= n {
        if i < nums.len() && nums[i] <= miss {
            miss += nums[i];
            i += 1;
        } else {
            miss += miss;
            patches += 1;
        }
    }
    patches
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 330;
    let mut nums: Vec<i64> = Vec::new();
    let mut total = 0;
    for _ in 0..LEN {
        let v = next(&mut seed) % 1001 + 50;
        nums.push(v);
        total += v;
    }
    nums.sort();
    let mut sink = 0;
    for _ in 0..PUNCHES {
        let hi = next(&mut seed);
        let lo = next(&mut seed);
        let n = (hi * 32768 + lo) % (2 * total) + 1;
        let answer = min_patches(&nums, n);
        sink = (sink * 1000003 + answer * 64 + n % 64) % MODULUS;
    }
    println!("{}", sink);
}
