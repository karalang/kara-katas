// LeetCode #34 bench — Rust (mirror of search_range.kara).
//
// Two-bounds style: lower_bound + upper_bound per query over a fixed sorted array
// with duplicate runs, TOTAL queries with cycling targets, both endpoints folded
// into a checksum. `rustc -O` wraps on overflow; the bench also builds a
// `-C overflow-checks=on` variant to match Kāra's checked-by-default semantics
// (all values stay well inside i64, so neither variant traps — the safety tax
// isolates codegen).

fn lower_bound(nums: &[i64], len: i64, target: i64) -> i64 {
    let mut lo = 0i64;
    let mut hi = len;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if nums[mid as usize] < target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

fn upper_bound(nums: &[i64], len: i64, target: i64) -> i64 {
    let mut lo = 0i64;
    let mut hi = len;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if nums[mid as usize] <= target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

fn main() {
    let n: i64 = 4096;
    let run: i64 = 4;
    let total: i64 = 14000000;
    let modulus: i64 = 1000000007;

    let mut nums: Vec<i64> = Vec::new();
    let mut p: i64 = 0;
    while p < n {
        nums.push(2 * (p / run));
        p += 1;
    }

    let span = 2 * n;
    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        let target = k % span;
        let lo = lower_bound(&nums, n, target);
        let mut first = -1i64;
        let mut last = -1i64;
        if lo < n && nums[lo as usize] == target {
            first = lo;
            last = upper_bound(&nums, n, target) - 1;
        }
        acc = (acc * 31 + (first + 1)) % modulus;
        acc = (acc * 31 + (last + 1)) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
