// LeetCode #33 bench — Rust (mirror of search_rotated.kara).
//
// One-pass modified binary search over a fixed rotated-sorted array, TOTAL
// searches with cycling targets, folded into a checksum. `rustc -O` wraps on
// overflow; the bench also builds a `-C overflow-checks=on` variant to match
// Kāra's checked-by-default semantics (all values stay well inside i64, so
// neither variant traps — the safety tax isolates codegen).

fn search(nums: &[i64], len: i64, target: i64) -> i64 {
    let mut lo = 0i64;
    let mut hi = len - 1;
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        let m = nums[mid as usize];
        if m == target {
            return mid;
        }
        if nums[lo as usize] <= m {
            if nums[lo as usize] <= target && target < m {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else if m < target && target <= nums[hi as usize] {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    -1
}

fn main() {
    let n: i64 = 4096;
    let rot: i64 = 1365;
    let total: i64 = 18000000;
    let modulus: i64 = 1000000007;

    let mut nums: Vec<i64> = Vec::new();
    let mut p: i64 = 0;
    while p < n {
        nums.push(2 * ((p + rot) % n));
        p += 1;
    }

    let span = 2 * n;
    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        let target = k % span;
        let idx = search(&nums, n, target);
        acc = (acc + idx + 2) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
