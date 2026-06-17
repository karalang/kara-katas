// LeetCode #35 bench — Rust (mirror of search_insert.kara).
//
// Half-open lower_bound style: one search_insert (first index >= target) per query
// over a fixed strictly-increasing array of distinct values, TOTAL queries with
// cycling targets, each index folded into a checksum. `rustc -O` wraps on overflow;
// the bench also builds a `-C overflow-checks=on` variant to match Kāra's
// checked-by-default semantics (all values stay well inside i64, so neither variant
// traps — the safety tax isolates codegen).

fn search_insert(nums: &[i64], len: i64, target: i64) -> i64 {
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

fn main() {
    let n: i64 = 4096;
    let total: i64 = 14000000;
    let modulus: i64 = 1000000007;

    let mut nums: Vec<i64> = Vec::new();
    let mut p: i64 = 0;
    while p < n {
        nums.push(2 * p);
        p += 1;
    }

    let span = 2 * n;
    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        let target = k % span;
        let idx = search_insert(&nums, n, target);
        acc = (acc * 31 + idx) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
