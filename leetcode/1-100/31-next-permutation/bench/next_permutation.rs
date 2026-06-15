// LeetCode #31 bench — Rust (mirror of next_permutation.kara).
//
// Canonical four-move next-permutation, enumerating all K! permutations REPEAT
// times and folding a rolling checksum. `rustc -O` wraps on overflow; the bench
// also builds a `-C overflow-checks=on` variant to match Kāra's checked-by-
// default semantics. The checksum modulus keeps every value well inside i64, so
// neither variant actually traps — the safety tax isolates codegen, not arith.

fn next_permutation(nums: &mut [i64], len: usize) {
    if len < 2 {
        return;
    }
    let mut i = len as i64 - 2;
    while i >= 0 && nums[i as usize] >= nums[i as usize + 1] {
        i -= 1;
    }
    if i >= 0 {
        let mut j = len - 1;
        while nums[j] <= nums[i as usize] {
            j -= 1;
        }
        nums.swap(i as usize, j);
    }
    let mut lo = (i + 1) as usize;
    let mut hi = len - 1;
    while lo < hi {
        nums.swap(lo, hi);
        lo += 1;
        hi -= 1;
    }
}

fn main() {
    let k: usize = 10;
    let fact: i64 = 3628800; // 10!
    let repeat: i64 = 8;
    let modulus: i64 = 2147483647; // 2^31 - 1

    let mut nums: [i64; 10] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    let mut acc: i64 = 0;

    for _ in 0..repeat {
        let mut step: i64 = 0;
        while step < fact {
            let mut h: i64 = 0;
            for i in 0..k {
                h = (h * 131 + nums[i]) % modulus;
            }
            acc = (acc + h) % modulus;
            next_permutation(&mut nums, k);
            step += 1;
        }
    }

    println!("{}", acc);
}
